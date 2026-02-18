import sys
import traceback
from typing import Optional


class CustomException(Exception):
    """
    Production-grade custom exception for ML pipelines.

    Captures:
    - Original exception
    - File name
    - Line number
    - Full traceback
    """

    def __init__(self, message: str, original_exception: Optional[Exception] = None):
        super().__init__(message)
        self.message = message
        self.original_exception = original_exception

        # Capture traceback info
        # _, _, exc_tb = sys.exc_info()
        exc_type, exc_value, exc_tb = sys.exc_info() # for future read

        if exc_tb is not None:
            self.file_name = exc_tb.tb_frame.f_code.co_filename
            self.line_number = exc_tb.tb_lineno
            self.traceback = traceback.format_exc()
        else:
            self.file_name = "Unknown"
            self.line_number = "Unknown"
            self.traceback = None

    def __str__(self) -> str:
        base_message = (
            f"Error in file [{self.file_name}] "
            f"at line [{self.line_number}]: {self.message}"
        )

        if self.traceback:
            return f"{base_message}\nTraceback:\n{self.traceback}"

        return base_message
