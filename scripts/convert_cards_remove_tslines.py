#!/usr/bin/env python3
"""
Convert cards() to summary_table() and remove timeseries_lines() from EpochScript.

Handles:
1. JSON definition files (script field)
2. .epochscript files (raw text)

Conversion rules:
- cards(layout=CardLayout(...)) → summary_table(layout=SummaryTableLayout(...))
  - card_agg → grid_agg
  - card_color → grid_color
  - card_color_map → grid_color_map
  - card_slot → removed
  - Cell titles → col_headers
  - Add row_size=1, col_size=N, row_headers, col_headers, grid_row/grid_col
- timeseries_lines(...) → removed entirely
"""

import json
import re
import sys
from pathlib import Path


def find_matching_paren(text: str, start: int) -> int:
    """Find the matching closing paren for the opening paren at `start`."""
    depth = 0
    i = start
    in_string = False
    string_char = None
    while i < len(text):
        c = text[i]
        if in_string:
            if c == '\\':
                i += 2
                continue
            if c == string_char:
                in_string = False
        else:
            if c in ('"', "'"):
                in_string = True
                string_char = c
            elif c == '(':
                depth += 1
            elif c == ')':
                depth -= 1
                if depth == 0:
                    return i
            elif c == '[':
                depth += 1
            elif c == ']':
                depth -= 1
        i += 1
    return -1


def remove_timeseries_lines(script: str) -> str:
    """Remove all timeseries_lines(...)(...)  reporter blocks from script."""
    result = script
    while True:
        idx = result.find('timeseries_lines(')
        if idx == -1:
            break

        # Find the full block: timeseries_lines(options)(inputs)
        # First find the options paren
        opt_start = idx + len('timeseries_lines')
        opt_end = find_matching_paren(result, opt_start)
        if opt_end == -1:
            break

        # Check for second paren (inputs)
        rest = result[opt_end + 1:]
        # Skip whitespace
        j = 0
        while j < len(rest) and rest[j] in ' \t\n\r':
            j += 1

        if j < len(rest) and rest[j] == '(':
            inp_start = opt_end + 1 + j
            inp_end = find_matching_paren(result, inp_start)
            if inp_end == -1:
                break
            block_end = inp_end + 1
        else:
            block_end = opt_end + 1

        # Find the start of the line (for clean removal)
        line_start = idx
        while line_start > 0 and result[line_start - 1] in ' \t':
            line_start -= 1

        # Find the end of the line
        line_end = block_end
        while line_end < len(result) and result[line_end] in ' \t':
            line_end += 1
        if line_end < len(result) and result[line_end] == '\n':
            line_end += 1

        # Also remove any preceding blank line
        if line_start > 0 and result[line_start - 1] == '\n':
            # Check if the line before is also blank
            prev_line_start = line_start - 1
            while prev_line_start > 0 and result[prev_line_start - 1] in ' \t':
                prev_line_start -= 1
            if prev_line_start > 0 and result[prev_line_start - 1] == '\n':
                line_start = prev_line_start

        result = result[:line_start] + result[line_end:]

    return result


def extract_cells_from_cardlayout(layout_str: str):
    """Extract cell info from CardLayout cells=[...] string."""
    # Find the cells=[ part
    cells_match = re.search(r'cells\s*=\s*\[', layout_str)
    if not cells_match:
        return [], ""

    # Find matching ]
    bracket_start = cells_match.end() - 1
    depth = 0
    i = bracket_start
    in_string = False
    string_char = None
    while i < len(layout_str):
        c = layout_str[i]
        if in_string:
            if c == '\\':
                i += 2
                continue
            if c == string_char:
                in_string = False
        else:
            if c in ('"', "'"):
                in_string = True
                string_char = c
            elif c == '[':
                depth += 1
            elif c == ']':
                depth -= 1
                if depth == 0:
                    break
        i += 1

    cells_str = layout_str[bracket_start + 1:i]

    # Parse individual ColumnSpec entries
    cells = []
    for cs_match in re.finditer(r'ColumnSpec\s*\(', cells_str):
        cs_start = cs_match.end() - 1
        cs_end = find_matching_paren(cells_str, cs_start)
        if cs_end == -1:
            continue
        cs_inner = cells_str[cs_start + 1:cs_end]
        cells.append(parse_columnspec(cs_inner))

    return cells


def parse_columnspec(inner: str) -> dict:
    """Parse ColumnSpec inner content into a dict of field=value pairs."""
    result = {}
    # Match field=value patterns, handling nested parens and strings
    i = 0
    while i < len(inner):
        # Skip whitespace and commas
        while i < len(inner) and inner[i] in ' \t\n\r,':
            i += 1
        if i >= len(inner):
            break

        # Find field name
        field_match = re.match(r'(\w+)\s*=\s*', inner[i:])
        if not field_match:
            i += 1
            continue

        field_name = field_match.group(1)
        val_start = i + field_match.end()

        # Find value end - could be a string, enum, or nested call
        val_end = find_value_end(inner, val_start)
        value = inner[val_start:val_end].strip()
        result[field_name] = value
        i = val_end

    return result


def find_value_end(text: str, start: int) -> int:
    """Find the end of a value in a comma-separated list."""
    i = start
    depth = 0
    in_string = False
    string_char = None
    while i < len(text):
        c = text[i]
        if in_string:
            if c == '\\':
                i += 2
                continue
            if c == string_char:
                in_string = False
        else:
            if c in ('"', "'"):
                in_string = True
                string_char = c
            elif c in ('(', '['):
                depth += 1
            elif c in (')', ']'):
                if depth == 0:
                    return i
                depth -= 1
            elif c == ',' and depth == 0:
                return i
        i += 1
    return i


def convert_cards_block(match_text: str, indent: str) -> str:
    """Convert a full cards(...)(inputs) block to summary_table."""
    # Extract the CardLayout content
    layout_match = re.search(r'CardLayout\s*\(', match_text)
    if not layout_match:
        return match_text  # Can't parse, leave as-is

    layout_start = layout_match.end() - 1
    layout_end = find_matching_paren(match_text, layout_start)
    if layout_end == -1:
        return match_text

    layout_inner = match_text[layout_start + 1:layout_end]

    # Extract title
    title_match = re.search(r"title\s*=\s*'([^']*)'", layout_inner)
    if not title_match:
        title_match = re.search(r'title\s*=\s*"([^"]*)"', layout_inner)
    title = title_match.group(1) if title_match else 'Summary'

    # Extract cells
    cells = extract_cells_from_cardlayout(layout_inner)
    if not cells:
        return match_text  # No cells found, leave as-is

    n_cells = len(cells)

    # Extract category if present
    cat_match = re.search(r"category\s*=\s*'([^']*)'", match_text)
    if not cat_match:
        cat_match = re.search(r'category\s*=\s*"([^"]*)"', match_text)
    category = cat_match.group(1) if cat_match else None

    # Extract inputs (the second paren group)
    # Find first ) after layout, then find next )(
    first_close = match_text.find(')')
    # Actually, find the closing of cards(...)
    cards_paren_start = match_text.index('(')
    cards_paren_end = find_matching_paren(match_text, cards_paren_start)

    # Find inputs paren
    rest_after = match_text[cards_paren_end + 1:]
    inp_match = re.search(r'\s*\(', rest_after)
    if inp_match:
        inp_abs_start = cards_paren_end + 1 + inp_match.end() - 1
        inp_abs_end = find_matching_paren(match_text, inp_abs_start)
        inputs_str = match_text[inp_abs_start + 1:inp_abs_end].strip() if inp_abs_end != -1 else ""
    else:
        inputs_str = ""

    # Build col_headers from cell titles
    col_headers = []
    for cell in cells:
        cell_title = cell.get('title', '').strip("'\"")
        col_headers.append(cell_title)

    # Build new cells
    new_cells = []
    for i, cell in enumerate(cells):
        parts = []
        parts.append(f"grid_row=0")
        parts.append(f"grid_col={i}")

        # Map card_agg → grid_agg
        if 'card_agg' in cell:
            parts.append(f"grid_agg={cell['card_agg']}")

        # Keep type
        if 'type' in cell:
            parts.append(f"type={cell['type']}")

        # Keep dp
        if 'dp' in cell:
            parts.append(f"dp={cell['dp']}")

        # Map card_color → grid_color
        if 'card_color' in cell:
            parts.append(f"grid_color={cell['card_color']}")

        # Map card_color_map → grid_color_map
        if 'card_color_map' in cell:
            parts.append(f"grid_color_map={cell['card_color_map']}")

        # Drop: card_slot, title (moved to col_headers)

        new_cells.append(f"ColumnSpec({', '.join(parts)})")

    # Format col_headers
    col_headers_str = "[" + ", ".join(f"'{h}'" for h in col_headers) + "]"

    # Build the summary_table block
    inner_indent = indent + "    "
    cell_indent = inner_indent + "    "

    lines = []
    lines.append(f"{indent}summary_table(")
    lines.append(f"{inner_indent}layout=SummaryTableLayout(")
    lines.append(f"{cell_indent}title='{title}',")
    lines.append(f"{cell_indent}row_size=1,")
    lines.append(f"{cell_indent}col_size={n_cells},")
    lines.append(f"{cell_indent}row_headers=['{title}'],")
    lines.append(f"{cell_indent}col_headers={col_headers_str},")
    lines.append(f"{cell_indent}cells=[")

    for j, nc in enumerate(new_cells):
        comma = "," if j < len(new_cells) - 1 else ""
        lines.append(f"{cell_indent}    {nc}{comma}")

    lines.append(f"{cell_indent}]")
    lines.append(f"{inner_indent}),")
    if category:
        lines.append(f"{inner_indent}category='{category}'")
    lines.append(f"{indent})")
    if inputs_str:
        lines.append(f"({inputs_str})")

    return "\n".join(lines)


def convert_cards_in_script(script: str) -> str:
    """Find and convert all cards(...)(inputs) blocks in a script."""
    result = script
    iterations = 0
    while iterations < 20:  # Safety limit
        # Find next cards( occurrence
        idx = result.find('cards(')
        if idx == -1:
            # Also check for cards\n(
            idx = result.find('cards\n')
            if idx == -1:
                break
            # Skip if it's not followed by (
            rest = result[idx + 5:].lstrip()
            if not rest.startswith('('):
                break

        iterations += 1

        # Determine indent
        line_start = result.rfind('\n', 0, idx)
        if line_start == -1:
            line_start = 0
        else:
            line_start += 1
        indent = result[line_start:idx]
        if not indent.replace(' ', '').replace('\t', '') == '':
            indent = ''

        # Find the full block: cards(options)(inputs)
        opt_start = result.index('(', idx)
        opt_end = find_matching_paren(result, opt_start)
        if opt_end == -1:
            break

        # Check for second paren (inputs)
        rest_after = result[opt_end + 1:]
        j = 0
        while j < len(rest_after) and rest_after[j] in ' \t\n\r':
            j += 1

        if j < len(rest_after) and rest_after[j] == '(':
            inp_start = opt_end + 1 + j
            inp_end = find_matching_paren(result, inp_start)
            if inp_end == -1:
                break
            block_end = inp_end + 1
        else:
            block_end = opt_end + 1

        full_block = result[idx:block_end]

        # Convert
        converted = convert_cards_block(full_block, indent)

        # Replace in result
        # Include the indent in the replacement
        result = result[:line_start] + converted + result[block_end:]

    return result


def process_json_definition(filepath: Path, remove_tslines: bool = True, convert_cards: bool = True) -> bool:
    """Process a JSON definition file. Returns True if modified."""
    text = filepath.read_text()
    data = json.loads(text)

    # Field is "source" in these definitions
    field = "source" if "source" in data else "script"
    script = data.get(field, "")
    if not script:
        return False

    original = script

    if remove_tslines and 'timeseries_lines' in script:
        script = remove_timeseries_lines(script)

    if convert_cards and 'cards(' in script:
        script = convert_cards_in_script(script)

    if script == original:
        return False

    data[field] = script
    filepath.write_text(json.dumps(data, indent=3, ensure_ascii=False) + "\n")
    return True


def process_epochscript_file(filepath: Path, remove_tslines: bool = True, convert_cards: bool = True) -> bool:
    """Process an .epochscript file. Returns True if modified."""
    script = filepath.read_text()
    original = script

    if remove_tslines and 'timeseries_lines' in script:
        script = remove_timeseries_lines(script)

    if convert_cards and 'cards(' in script:
        script = convert_cards_in_script(script)

    if script == original:
        return False

    filepath.write_text(script)
    return True


def main():
    claude_research_defs = Path("/home/adesola/EpochDev/ClaudeCodeResearch/project/definitions/test_runner")
    script_templates = Path("/home/adesola/EpochDev/ScriptTemplates")

    modified = []
    errors = []

    # Process ClaudeCodeResearch JSON definitions
    print("=== Processing ClaudeCodeResearch definitions ===")
    for f in sorted(claude_research_defs.glob("*.json")):
        text = f.read_text()
        if 'timeseries_lines' not in text and 'cards(' not in text:
            continue
        try:
            if process_json_definition(f):
                modified.append(str(f))
                print(f"  MODIFIED: {f.name}")
        except Exception as e:
            errors.append((str(f), str(e)))
            print(f"  ERROR: {f.name}: {e}")

    # Process ScriptTemplates .epochscript files
    print("\n=== Processing ScriptTemplates ===")
    for f in sorted(script_templates.rglob("*.epochscript")):
        text = f.read_text()
        if 'timeseries_lines' not in text and 'cards(' not in text:
            continue
        try:
            if process_epochscript_file(f):
                modified.append(str(f))
                print(f"  MODIFIED: {f.name}")
        except Exception as e:
            errors.append((str(f), str(e)))
            print(f"  ERROR: {f.name}: {e}")

    print(f"\n=== Summary ===")
    print(f"Modified: {len(modified)} files")
    if errors:
        print(f"Errors: {len(errors)}")
        for path, err in errors:
            print(f"  {path}: {err}")

    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
