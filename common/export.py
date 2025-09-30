from datetime import datetime
from pathlib import Path

import pandas as pd

from common import config
from common.constants import ResponseExportTypes
from common.helper import get_file_extension

def _get_full_path(file_name: str, file_format: str, sub_path: str | None = "Documents") -> Path:
    return Path.home() / sub_path / f"{file_name}.{get_file_extension(file_format)}"

def _get_file_name() -> str:
    return f"{config.EXPORT_FILE_BASE_NAME}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

def export_file(file_format: str, prompt_response: list[dict]) -> Path:
    file_format = file_format.upper()

    if file_format not in ResponseExportTypes:
        raise ValueError(f"Invalid export file format: {file_format}. Supported formats: {ResponseExportTypes}.")

    file_name = _get_file_name()
    full_path = _get_full_path(file_name, file_format)

    data_frame = pd.DataFrame(prompt_response)
    pandas_file_export_function = getattr(data_frame, f"to_{file_format}", None)
    pandas_file_export_function(full_path, index=False)

    return full_path
