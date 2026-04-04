/**
 * Tree-sitter Grammar for EpochScript
 * Auto-generated from C++ definitions - DO NOT EDIT MANUALLY.
 *
 * ===========================================================================
 * IMPORTANT NOTE ON SESSIONS
 * ===========================================================================
 * Session(start, end, tz) requires start < end within the SAME DAY.
 *
 * INVALID: Session(start="16:00", end="09:30", tz="America/New_York")
 *   - This does NOT create an overnight session! start must be < end.
 *
 * For overnight sessions (e.g., 16:00 to 09:30), use daily bars and lag:
 *   daily_close = src.c  // on 1D bars
 *   overnight_return = daily_close / (daily_close >> 1) - 1
 *
 * ===========================================================================
 */

/// <reference types="tree-sitter-cli/dsl" />
// @ts-check

const PREC = {
  pipeline: 1,      // Lowest - left associative chaining
  ternary: 2,
  or: 3,
  xor: 4,           // ^ operator (logical XOR) - between or and and
  and: 5,
  not: 6,
  compare: 7,
  lag: 8,           // >> operator (lag)
  lead: 8,          // << operator (lead) - same precedence as lag
  add: 9,
  mul: 10,
  unary: 11,
  power: 12,
  call: 13,
  subscript: 14,
  attribute: 15,
};

// Built-in schema types (reserved keywords)
const BUILTIN_TYPES = [
  'Timestamp', 'Time', 'Duration', 'Session', 'SessionDelta', 'EventMarkerSchema', 'TableReportSchema', 'CardLayout',
  'SummaryTableLayout', 'ReferenceLineSchema', 'ReferenceLine', 'LineSeriesSchema', 'LineSeriesSpec', 'LabeledLineSeriesSchema', 'LabeledLineSeriesSpec', 'PlotBandSchema',
  'PlotBand', 'ScatterSeriesSchema', 'ScatterSeriesSpec', 'BarSeriesSchema', 'BarSeriesSpec', 'WeightedKeywordSchema', 'TopicDictionarySchema', 'KeywordPatternSchema',
  'AssetFilterSchema', 'AssetFilter', 'ColumnSpec', 'RowSpec',
];

// Built-in functions (use fn(args) syntax, not fn()(args))
const BUILTIN_FUNCTIONS = [
  'abs', 'acos', 'asin', 'atan', 'ceil', 'cos', 'cosh', 'exp',
  'floor', 'ln', 'log10', 'round', 'sin', 'sinh', 'sqrt', 'tan',
  'tanh', 'todeg', 'torad', 'trunc', 'ffill', 'ffill_day', 'str', 'crossover',
  'crossunder', 'crossany', 'coalesce', 'conditional_select', 'where', 'is_valid', 'is_null', 'logical_xor',
  'logical_and_not', 'earnings', 'analyst_ratings', 'ipos', 'splits', 'ticker_events', 'short_interest', 'short_volume',
  'balance_sheet', 'cash_flow', 'income_statement', 'dividends', 'economic_indicators', 'economic_revisions', 'common_treasury_auctions', 'agg',
  'valuewhen', 'barssince', 'diff', 'nz', 'isna', 'notna', 'prev', 'returns',
  'rank', 'quantile', 'weighted_mean', 'ema', 'sma', 'wma', 'hma', 'dema',
  'tema', 'kama', 'trima', 'wilders', 'zlema', 'rsi', 'trix', 'cmo',
  'fosc', 'roc', 'rocr', 'stochrsi', 'apo', 'ppo', 'dpo', 'vhf',
  'md', 'ulcer_index', 'percentrank', 'streak_length', 'nlargest', 'nsmallest', 'hurst_exponent', 'rolling_hurst_exponent',
  'decay', 'edecay', 'stderr', 'forward_returns', 'arg_max', 'arg_min', 'highestbars', 'lowestbars',
  'cci', 'mfi', 'willr', 'atr', 'natr', 'cvi', 'mass', 'adx',
  'adxr', 'dx', 'aroonosc', 'vwma', 'qstick', 'psl', 'ultosc', 'psar',
  'adosc', 'kvo', 'vosc', 'intraday_returns', 'rising', 'falling', 'corr', 'cov',
  'beta', 'ewm_cov', 'tr', 'price_distance', 'bband_percent', 'bband_width', 'ao', 'bop',
  'avgprice', 'medprice', 'typprice', 'wcprice', 'obv', 'ad', 'emv', 'nvi',
  'pvi', 'marketfi', 'wad', 'vwap', 'hold_until', 'trade_count', 'switch', 'is_study_asset',
  'day_of_week', 'month_of_year', 'quarter', 'week_of_month', 'is_month_start', 'is_month_end', 'is_quarter_start', 'is_quarter_end',
  'is_year_start', 'is_year_end', 'is_week_start', 'is_week_end', 'is_opex', 'calendar_shift',
];

// Compiler macros (single-stage, expand to N impl nodes)
const COMPILER_MACROS = [
  'resample', 'candlestick_pattern', 'macro_data', 'pair_stat', 'volatility', 'select', 'aroon', 'supertrend',
  'ichimoku', 'macd', 'stoch', 'bbands', 'donchian_channel', 'keltner_channels', 'pivot_point_sr',
];

// Enum types - Use: Color.Blue, Icon.ChartIcon, DashStyle.Solid
const ENUM_TYPES = [
  'AdjustmentType', 'AggregationType', 'ArrayMatchMode', 'AssetCategory', 'AssetClassUI', 'AssetFilterOp', 'AssetFilterRank', 'AssetGroupingMode',
  'BalanceSheetTimeframe', 'BarMode', 'BasicVolatilityType', 'BoostingType', 'BoundaryType', 'BoxplotMode', 'CSBarMode', 'CSBoxplotMode',
  'CSSelectDirection', 'CSSelectMode', 'CalendarSource', 'CandlestickPattern', 'CardRenderType', 'CardSlot', 'CategoryAxisType', 'Color',
  'ContainsOperation', 'CorrelationMethod', 'DashStyle', 'DatetimeExtractionType', 'DayAnchorType', 'DayOfWeek', 'DistributionType', 'DividendType',
  'EiaFrequency', 'FillDirection', 'FillMethod', 'FinanceRatioType', 'HeatmapMode', 'HolidayCalendar', 'Icon', 'KalmanModelType',
  'LinkageMethod', 'MAType', 'MLWindowType', 'MacroEconomicsIndicator', 'MarkerSymbol', 'Month', 'OrdinalType', 'PairMetric',
  'PeriodType', 'ProfileType', 'Quarter', 'ReferenceCryptoPair', 'ReferenceFXPair', 'ReferenceFutures', 'ReferenceIndex', 'ReferenceStock',
  'ReportingPeriod', 'ReturnType', 'ReturnsType', 'RiskMeasure', 'RiskMode', 'RolloverType', 'SelectDirection', 'SessionAnchor',
  'SessionTimeframe', 'SessionType', 'SizeBy', 'SizeType', 'SortByValue', 'StackType', 'StepType', 'StockExchange',
  'StockSector', 'StopUnit', 'StreakDirection', 'StringCaseOperation', 'StringCheckOperation', 'TableMode', 'TimeDiffUnit', 'TradingHoursType',
  'TreasuryAuctionType', 'TreasurySecurityType', 'TreasuryTerm', 'TrimOperation', 'VolMethod', 'VolatilityEstimatorType', 'WeekOfMonth', 'Weekday',
  'WindowType',
];

module.exports = grammar({
  name: 'epochscript',

  // Whitespace and comments are automatically skipped
  extras: $ => [
    /\s/,
    $.comment,
  ],

  // Word boundary for keywords
  word: $ => $.identifier,

  // No conflicts needed - grammar is unambiguous

  rules: {
    // =========================================================================
    // MODULE (Entry Point)
    // =========================================================================

    module: $ => repeat($._statement),

    // =========================================================================
    // STATEMENTS
    // =========================================================================

    _statement: $ => choice(
      $.assignment_statement,
      $.expression_statement,
    ),

    // Assignment: var = expr
    assignment_statement: $ => seq(
      field('left', $._assignment_target),
      '=',
      field('right', $.expression),
    ),

    _assignment_target: $ => choice(
      $.identifier,
      $.tuple_pattern,
    ),

    // Tuple unpacking: a, b, c
    tuple_pattern: $ => seq(
      $.identifier,
      repeat1(seq(',', $.identifier)),
      optional(','),
    ),

    // Expression as statement
    expression_statement: $ => $.expression,

    // Comments: # text
    comment: $ => token(seq('#', /.*/)),

    // =========================================================================
    // EXPRESSIONS
    // =========================================================================

    expression: $ => choice(
      $.pipeline_expression,
      $.ternary_expression,
      $.or_expression,
      $.xor_expression,
      $.and_expression,
      $.not_expression,
      $.comparison_expression,
      $.lag_expression,
      $.lead_expression,
      $.binary_expression,
      $.unary_expression,
      $.power_expression,
      $.call_expression,
      $.attribute_expression,
      $.subscript_expression,
      $.parenthesized_expression,
      $.builtin_type,
      $.builtin_function,
      ...(COMPILER_MACROS.length > 0 ? [$.compiler_macro] : []),
      $.enum_type,
      $.identifier,
      $.timeframe,
      $.integer,
      $.float,
      $.string,
      $.true,
      $.false,
      $.list_literal,
      $.tuple_literal,
      $.dict_literal,
    ),

    // =========================================================================
    // PIPELINE OPERATOR: src.c | sma(period=20)
    // =========================================================================

    pipeline_expression: $ => prec.left(PREC.pipeline, seq(
      field('left', $.expression),
      '|',
      field('right', $.expression),
    )),

    // =========================================================================
    // LAG OPERATOR: src.c >> 1 (get previous values)
    // =========================================================================

    lag_expression: $ => prec.left(PREC.lag, seq(
      field('value', $.expression),
      '>>',
      field('periods', $.expression),
    )),

    // =========================================================================
    // LEAD OPERATOR: src.c << 1 (get future values)
    // =========================================================================

    lead_expression: $ => prec.left(PREC.lead, seq(
      field('value', $.expression),
      '<<',
      field('periods', $.expression),
    )),

    // =========================================================================
    // TERNARY AND BOOLEAN
    // =========================================================================

    // Ternary: value if condition else other
    ternary_expression: $ => prec.right(PREC.ternary, seq(
      field('body', $.expression),
      'if',
      field('condition', $.expression),
      'else',
      field('orelse', $.expression),
    )),

    // Boolean OR
    or_expression: $ => prec.left(PREC.or, seq(
      field('left', $.expression),
      'or',
      field('right', $.expression),
    )),

    // Boolean XOR (^ operator)
    xor_expression: $ => prec.left(PREC.xor, seq(
      field('left', $.expression),
      '^',
      field('right', $.expression),
    )),

    // Boolean AND
    and_expression: $ => prec.left(PREC.and, seq(
      field('left', $.expression),
      'and',
      field('right', $.expression),
    )),

    // Boolean NOT
    not_expression: $ => prec(PREC.not, seq(
      'not',
      field('operand', $.expression),
    )),

    // =========================================================================
    // COMPARISON
    // =========================================================================

    comparison_expression: $ => prec.left(PREC.compare, seq(
      field('left', $.expression),
      field('operator', $.comparison_operator),
      field('right', $.expression),
    )),

    comparison_operator: $ => choice(
      '<',
      '>',
      '<=',
      '>=',
      '==',
      '!=',
    ),

    // =========================================================================
    // ARITHMETIC
    // =========================================================================

    // Binary operators (arithmetic)
    binary_expression: $ => choice(
      // Additive
      prec.left(PREC.add, seq(
        field('left', $.expression),
        field('operator', alias(choice('+', '-'), $.additive_operator)),
        field('right', $.expression),
      )),
      // Multiplicative
      prec.left(PREC.mul, seq(
        field('left', $.expression),
        field('operator', alias(choice('*', '/', '%'), $.multiplicative_operator)),
        field('right', $.expression),
      )),
    ),

    // Unary operators
    unary_expression: $ => prec.right(PREC.unary, seq(
      field('operator', choice('-', '+')),
      field('operand', $.expression),
    )),

    // Power operator (**)
    power_expression: $ => prec.right(PREC.power, seq(
      field('base', $.expression),
      '**',
      field('exponent', $.expression),
    )),

    // =========================================================================
    // POSTFIX EXPRESSIONS (Call, Attribute, Subscript)
    // =========================================================================

    // Function call: func(args) or component(options)(inputs)
    call_expression: $ => prec(PREC.call, seq(
      field('function', $.expression),
      field('arguments', $.argument_list),
    )),

    // Attribute access: obj.attr
    attribute_expression: $ => prec.left(PREC.attribute, seq(
      field('object', $.expression),
      '.',
      field('attribute', $.identifier),
    )),

    // Subscript: tuple[index] - for indexing results
    subscript_expression: $ => prec(PREC.subscript, seq(
      field('value', $.expression),
      '[',
      field('index', $.expression),
      ']',
    )),

    // Argument list: (arg1, arg2, key=value)
    argument_list: $ => seq(
      '(',
      optional(seq(
        $._argument,
        repeat(seq(',', $._argument)),
        optional(','),
      )),
      ')',
    ),

    _argument: $ => choice(
      $.expression,
      $.keyword_argument,
    ),

    keyword_argument: $ => seq(
      field('name', choice($.identifier, $.builtin_function, $.compiler_macro, $.enum_type)),
      '=',
      field('value', $.expression),
    ),

    // =========================================================================
    // PRIMARY EXPRESSIONS
    // =========================================================================

    parenthesized_expression: $ => seq(
      '(',
      $.expression,
      ')',
    ),

    // =========================================================================
    // BUILT-IN TYPES (Reserved Keywords)
    // Uses BUILTIN_TYPES constant defined at top of file
    // =========================================================================

    builtin_type: $ => choice(...BUILTIN_TYPES),

    // =========================================================================
    // BUILT-IN FUNCTIONS (use fn(args) syntax, not fn()(args))
    // Uses BUILTIN_FUNCTIONS constant defined at top of file
    // =========================================================================

    builtin_function: $ => choice(...BUILTIN_FUNCTIONS),

    // =========================================================================
    // COMPILER MACROS (single-stage, expand to N impl nodes)
    // Uses COMPILER_MACROS constant defined at top of file
    // =========================================================================

    ...(COMPILER_MACROS.length > 0 ? {
      compiler_macro: $ => choice(...COMPILER_MACROS),
    } : {}),

    // Enum types - Use: Color.Blue, Icon.ChartIcon, DashStyle.Solid
    enum_type: $ => choice(...ENUM_TYPES),

    // =========================================================================
    // LITERALS
    // =========================================================================

    // Timeframe literals (pandas offset style):
    // Basic: 1D, 4H, 15Min, 30s
    // Start/End: 1ME, 1MS, 1QE, 1QS, 1YE, 1YS
    // Weekly with anchor: 1W-SUN, 1W-MON, 1W-FRI
    // Weekly with ordinal: 1W-MON-1st, 1W-MON-2nd, 1W-FRI-Last
    timeframe: $ => token(choice(
      // Minutes with "Min" suffix: 1Min, 5Min, 15Min
      /[1-9][0-9]*Min/,
      // Weekly with day anchor and optional ordinal: 1W-MON, 1W-FRI-Last
      /[1-9][0-9]*W-(SUN|MON|TUE|WED|THU|FRI|SAT)(-(1st|2nd|3rd|4th|Last))?/,
      // Month/Quarter/Year with Start/End: 1ME, 1MS, 1QE, 1QS, 1YE, 1YS
      /[1-9][0-9]*[MQY][SE]/,
      // Basic: 1D, 4H, 1W, 1M, 1Q, 1Y (seconds, hours, days, weeks)
      /[1-9][0-9]*[sHDWMQY]/,
    )),

    // Integer literals
    integer: $ => token(choice(
      /0/,
      /[1-9][0-9]*/,
    )),

    // Float literals
    float: $ => token(choice(
      // Decimal float: 3.14, .5, 3.
      /[0-9]+\.[0-9]*/,
      /[0-9]*\.[0-9]+/,
      // Exponent float: 1e5, 2.5e-3
      /[0-9]+[eE][+-]?[0-9]+/,
      /[0-9]+\.[0-9]*[eE][+-]?[0-9]+/,
      /[0-9]*\.[0-9]+[eE][+-]?[0-9]+/,
    )),

    // String literals
    string: $ => choice(
      seq("'", optional($.string_content_single), "'"),
      seq('"', optional($.string_content_double), '"'),
      seq("'''", optional($.string_content_triple_single), "'''"),
      seq('"""', optional($.string_content_triple_double), '"""'),
    ),

    // String contents (using token.immediate to avoid whitespace issues)
    string_content_single: $ => token.immediate(prec(1, /[^'\\]*(\\.[^'\\]*)*/)),
    string_content_double: $ => token.immediate(prec(1, /[^"\\]*(\\.[^"\\]*)*/)),
    string_content_triple_single: $ => token.immediate(prec(1, /([^']|'[^']|''[^'])*/)),
    string_content_triple_double: $ => token.immediate(prec(1, /([^"]|"[^"]|""[^"])*/)),

    // Boolean literals (accept both Python-style and lowercase)
    true: $ => choice('True', 'true'),
    false: $ => choice('False', 'false'),

    // =========================================================================
    // CONTAINER LITERALS
    // =========================================================================

    // List: [1, 2, 3]
    list_literal: $ => seq(
      '[',
      optional(seq(
        $.expression,
        repeat(seq(',', $.expression)),
        optional(','),
      )),
      ']',
    ),

    // Tuple: (a, b) or (a,) - note: (a) is parenthesized_expression
    tuple_literal: $ => choice(
      // Empty tuple
      seq('(', ')'),
      // Single element tuple (requires trailing comma)
      seq('(', $.expression, ',', ')'),
      // Multi-element tuple
      seq(
        '(',
        $.expression,
        repeat1(seq(',', $.expression)),
        optional(','),
        ')',
      ),
    ),

    // Dict: {key: value, ...} - only allowed in schema constructor kwargs
    // Keys can be identifiers, strings, or enum access (Color.Success)
    dict_literal: $ => seq(
      '{',
      optional(seq(
        $.dict_entry,
        repeat(seq(',', $.dict_entry)),
        optional(','),
      )),
      '}',
    ),

    // Dict keys can be identifiers, strings, or enum access (Color.Success)
    dict_entry: $ => seq(
      field('key', choice($.attribute_expression, $.identifier, $.string)),
      ':',
      field('value', $.expression),
    ),

    // =========================================================================
    // LEXICAL ELEMENTS
    // =========================================================================

    // Identifier: starts with letter or underscore
    // Cannot be a reserved keyword
    identifier: $ => /[a-zA-Z_][a-zA-Z0-9_]*/,
  },
});
