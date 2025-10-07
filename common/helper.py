from datetime import date, datetime
from decimal import Decimal

from common import config
from common.constants import ResponseExportTypes, ResponseExportTypesExtensions
from llm.config import PromptIteration


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
        and s.replace("_", "").replace(",", "").replace(" ", "").replace(".", "", 1).lstrip("-+").isdigit()
    ):
        return s.rjust(w)

    return s.ljust(w)


def format_query_output(prompts: list[PromptIteration]) -> str:
    latest_prompt = prompts[-1]
    sql = (latest_prompt.sql or "").strip()
    note = (latest_prompt.notes or "").strip()
    prompt = (latest_prompt.prompt or "").strip()

    if not latest_prompt.response:
        parts = []
        if note:
            parts.append(f"Notes: {note}")
        if sql:
            parts.append(f"SQL: {sql}")
        parts.append("No rows returned.")
        return "\n".join(parts)

    columns: list[str] = []
    seen = set()
    for r in latest_prompt.response:
        if not isinstance(r, dict):
            import json

            parts = []
            if note:
                parts.append(f"Notes: {note}")
            if sql:
                parts.append(f"SQL: {sql}")
            parts.extend([json.dumps(x, default=str) for x in (latest_prompt.response or [])])
            return "\n".join(parts)
        for k in r.keys():
            if k not in seen:
                seen.add(k)
                columns.append(str(k))

    widths = {col: min(len(col), config.TERMINAL_OUTPUT_COLUMN_WIDTH) for col in columns}
    numeric_cols = set()

    for col in columns:
        max_width = widths[col]
        for r in latest_prompt.response:
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
    for r in latest_prompt.response:
        line = " | ".join(_fmt_cell(col, r.get(col), widths, numeric_cols) for col in columns)
        row_lines.append(line)

    parts = []
    if prompt:
        parts.append(f"Prompt: {prompt}\n")
    if note:
        parts.append(f"Notes: {note}\n")
    if sql:
        parts.append(f"SQL: {sql}\n")
    parts.append(header)
    parts.append(separator)
    parts.extend(row_lines)
    parts.extend("\n")
    parts.append(f"{len(latest_prompt.response)} row(s).")
    parts.append(f"{len(prompts)} message(s).")

    return "\n".join(parts)


def get_file_extension(file_type: str) -> str:
    return {
        ResponseExportTypes.CSV.value: ResponseExportTypesExtensions.CSV.value,
        ResponseExportTypes.XML.value: ResponseExportTypesExtensions.XML.value,
        ResponseExportTypes.EXCEL.value: ResponseExportTypesExtensions.XLSX.value,
        ResponseExportTypes.PARQUET.value: ResponseExportTypesExtensions.PARQUET.value,
    }.get(file_type)


def custom_json_serial(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()

    if isinstance(obj, Decimal):
        return float(obj)

    raise TypeError("Type %s not serializable" % type(obj))
