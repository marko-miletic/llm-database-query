from common import config


def is_number(v) -> bool:
    return isinstance(v, (int, float))


def _to_str_terminal(v) -> str:
    string = "" if v is None else str(v)
    string = string.replace("\n", " ⏎ ").replace("\r", " ")
    if len(string) > config.TERMINAL_OUTPUT_COLUMN_WIDTH:
        string = string[: config.TERMINAL_OUTPUT_COLUMN_WIDTH - 1] + "…"

    return string


def _fmt_cell(col: str, val, widths: dict[str, int], numeric_cols: set[str]):
    s = _to_str_terminal(val)
    w = widths[col]

    if (
        col in numeric_cols
        and s
        and s.replace("_", "")
        .replace(",", "")
        .replace(" ", "")
        .replace(".", "", 1)
        .lstrip("-+")
        .isdigit()
    ):
        return s.rjust(w)

    return s.ljust(w)


def format_query_output(query_response: tuple[str, list[dict], str]) -> str:
    sql, rows, note = query_response
    sql = (sql or "").strip()
    note = (note or "").strip()

    if not rows:
        parts = []
        if note:
            parts.append(f"Notes: {note}")
        if sql:
            parts.append(f"SQL: {sql}")
        parts.append("No rows returned.")
        return "\n".join(parts)

    columns: list[str] = []
    seen = set()
    for r in rows:
        if not isinstance(r, dict):
            import json

            parts = []
            if note:
                parts.append(f"Notes: {note}")
            if sql:
                parts.append(f"SQL: {sql}")
            parts.extend([json.dumps(x, default=str) for x in rows])
            return "\n".join(parts)
        for k in r.keys():
            if k not in seen:
                seen.add(k)
                columns.append(str(k))

    widths = {
        col: min(len(col), config.TERMINAL_OUTPUT_COLUMN_WIDTH) for col in columns
    }
    numeric_cols = set()

    for col in columns:
        max_width = widths[col]
        for r in rows:
            val = r.get(col)
            if is_number(val):
                numeric_cols.add(col)
            s = _to_str_terminal(val)
            if len(s) > max_width:
                max_width = len(s)
        widths[col] = min(max(max_width, len(col)), config.TERMINAL_OUTPUT_COLUMN_WIDTH)

    header = " | ".join(col.ljust(widths[col]) for col in columns)
    separator = "-+-".join("-" * widths[col] for col in columns)

    row_lines = []
    for r in rows:
        line = " | ".join(
            _fmt_cell(col, r.get(col), widths, numeric_cols) for col in columns
        )
        row_lines.append(line)

    parts = []
    if note:
        parts.append(f"Notes: {note}")
    if sql:
        parts.append(f"SQL: {sql}")
    parts.append(header)
    parts.append(separator)
    parts.extend(row_lines)
    parts.append(f"\n{len(rows)} row(s).")

    return "\n".join(parts)
