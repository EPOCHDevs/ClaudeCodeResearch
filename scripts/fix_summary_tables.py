#!/usr/bin/env python3
"""Convert bad summary_table syntax to correct SummaryTableLayout pattern.

Bad pattern:
    summary_table(
        title='...',
        category='...',
        agg=AggregationType.X,
        schema=TableReportSchema(columns=[
            ColumnSpec(title='Col1', type=CardRenderType.Y, dp=N),
        ]),
        series=TableSeriesSchema(series=[
            TableSeriesSpec(name='Row1'),
        ])
    )(inputs...)

Correct pattern:
    summary_table(
        layout=SummaryTableLayout(
            title='...',
            row_size=R, col_size=C,
            row_headers=['Row1', ...],
            col_headers=['Col1', ...],
            cells=[
                ColumnSpec(grid_row=0, grid_col=0, grid_agg=AggregationType.X, type=CardRenderType.Y, dp=N),
            ]
        ),
        category='...'
    )(inputs...)
"""
import json
import glob
import re
import sys
import os


def parse_bad_summary_table(block_text):
    """Parse a bad summary_table block and extract components."""
    result = {}

    # Extract title
    m = re.search(r"title=['\"](.+?)['\"]", block_text)
    if m:
        result['title'] = m.group(1)

    # Extract category
    m = re.search(r"category=['\"](.+?)['\"]", block_text)
    if m:
        result['category'] = m.group(1)

    # Extract agg type
    m = re.search(r"agg=AggregationType\.(\w+)", block_text)
    if m:
        result['agg'] = m.group(1)

    # Extract columns from schema=TableReportSchema(columns=[...])
    cols = []
    col_pattern = re.finditer(r"ColumnSpec\(title=['\"](.+?)['\"]([^)]*)\)", block_text)
    for cm in col_pattern:
        col = {'title': cm.group(1)}
        rest = cm.group(2)
        # Extract type
        tm = re.search(r"type=CardRenderType\.(\w+)", rest)
        if tm:
            col['type'] = tm.group(1)
        # Extract dp
        dm = re.search(r"dp=(\d+)", rest)
        if dm:
            col['dp'] = int(dm.group(1))
        cols.append(col)
    result['columns'] = cols

    # Extract series names from series=TableSeriesSchema(series=[...])
    rows = []
    row_pattern = re.finditer(r"TableSeriesSpec\(name=['\"](.+?)['\"]", block_text)
    for rm in row_pattern:
        rows.append(rm.group(1))
    result['rows'] = rows

    # Extract inputs (the part after the closing paren)
    m = re.search(r"\)\((.+?)\)\s*$", block_text, re.DOTALL)
    if m:
        result['inputs'] = m.group(1).strip()

    return result


def build_correct_summary_table(parsed, indent=''):
    """Build the correct summary_table syntax from parsed components."""
    title = parsed.get('title', 'Table')
    category = parsed.get('category', 'Reports')
    agg = parsed.get('agg', 'Mean')
    columns = parsed.get('columns', [])
    rows = parsed.get('rows', [])
    inputs = parsed.get('inputs', '')

    # If no rows, it's a single-row table
    if not rows:
        row_size = 1
        row_headers = None
    else:
        row_size = len(rows)
        row_headers = rows

    col_size = len(columns) if columns else 1
    col_headers = [c['title'] for c in columns] if columns else ['Value']

    # Build cells
    cells = []
    for r in range(row_size):
        for c in range(col_size):
            col_spec = columns[c] if c < len(columns) else {}
            cell_parts = [
                f"grid_row={r}",
                f"grid_col={c}",
                f"grid_agg=AggregationType.{agg}",
            ]
            if col_spec.get('type'):
                cell_parts.append(f"type=CardRenderType.{col_spec['type']}")
            if col_spec.get('dp') is not None:
                cell_parts.append(f"dp={col_spec['dp']}")
            cells.append(f"ColumnSpec({', '.join(cell_parts)})")

    # Build the output
    lines = []
    lines.append(f"{indent}summary_table(")
    lines.append(f"{indent}    layout=SummaryTableLayout(")
    lines.append(f"{indent}        title='{title}',")
    lines.append(f"{indent}        row_size={row_size},")
    lines.append(f"{indent}        col_size={col_size},")
    if row_headers:
        rh_str = ', '.join(f"'{r}'" for r in row_headers)
        lines.append(f"{indent}        row_headers=[{rh_str}],")
    ch_str = ', '.join(f"'{c}'" for c in col_headers)
    lines.append(f"{indent}        col_headers=[{ch_str}],")
    lines.append(f"{indent}        cells=[")
    for cell in cells:
        lines.append(f"{indent}            {cell},")
    lines.append(f"{indent}        ]")
    lines.append(f"{indent}    ),")
    lines.append(f"{indent}    category='{category}'")
    lines.append(f"{indent})({inputs})")

    return '\n'.join(lines)


def find_bad_blocks(source):
    """Find all bad summary_table blocks in source, return list of (start_idx, end_idx, block_text)."""
    lines = source.split('\n')
    blocks = []
    i = 0
    while i < len(lines):
        stripped = lines[i].strip()
        if stripped.startswith('summary_table('):
            # Check if this is a bad pattern (no layout=SummaryTableLayout in next few lines)
            lookahead = '\n'.join(lines[i:min(i+8, len(lines))])
            if 'layout=SummaryTableLayout' not in lookahead:
                # Find the end of this block by tracking parens
                depth = 0
                start = i
                j = i
                while j < len(lines):
                    depth += lines[j].count('(') - lines[j].count(')')
                    if depth <= 0:
                        break
                    j += 1
                block_text = '\n'.join(lines[start:j+1])
                blocks.append((start, j, block_text))
                i = j + 1
                continue
        i += 1
    return blocks


def fix_file(filepath, dry_run=False):
    """Fix all bad summary_table calls in a definition file."""
    with open(filepath) as f:
        data = json.load(f)

    source = data.get('source', '')
    if 'summary_table(' not in source:
        return 0

    blocks = find_bad_blocks(source)
    if not blocks:
        return 0

    lines = source.split('\n')
    fixed_count = 0

    # Process blocks in reverse order to maintain line numbers
    for start, end, block_text in reversed(blocks):
        parsed = parse_bad_summary_table(block_text)
        if not parsed.get('inputs'):
            print(f"  WARNING: Could not parse inputs for block at line {start}")
            continue

        # Detect indent from original
        indent = ''
        orig_line = lines[start]
        indent = orig_line[:len(orig_line) - len(orig_line.lstrip())]

        replacement = build_correct_summary_table(parsed, indent)

        # Replace lines
        lines[start:end+1] = replacement.split('\n')
        fixed_count += 1

    if fixed_count > 0 and not dry_run:
        data['source'] = '\n'.join(lines)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
            f.write('\n')

    return fixed_count


def main():
    dry_run = '--dry-run' in sys.argv

    files = sorted(glob.glob('project/definitions/test_runner/*.json'))
    total_fixed = 0
    files_fixed = 0

    for fp in files:
        name = os.path.basename(fp)
        count = fix_file(fp, dry_run=dry_run)
        if count > 0:
            prefix = "[DRY RUN] " if dry_run else ""
            print(f"{prefix}Fixed {count} summary_table(s) in {name}")
            total_fixed += count
            files_fixed += 1

    print(f"\nTotal: {total_fixed} summary_tables fixed in {files_fixed} files")
    if dry_run:
        print("(dry run - no files modified)")


if __name__ == '__main__':
    main()
