import traceback
from typing import Optional


class CustomException(Exception):
    """
    Production-grade custom exception.

    Captures:
    - Custom message
    - Original exception (if any)
    - File name
    - Line number
    - Full traceback
    """

    def __init__(self, message: str, original_exception: Optional[Exception] = None):
        super().__init__(message)

        self.message = message
        self.original_exception = original_exception

        if original_exception:
            tb = original_exception.__traceback__

            if tb:
                # Move to last traceback frame
                while tb.tb_next:
                    tb = tb.tb_next

                self.file_name = tb.tb_frame.f_code.co_filename
                self.line_number = tb.tb_lineno
            else:
                self.file_name = "Unknown"
                self.line_number = "Unknown"

            self.traceback = "".join(
                traceback.format_exception(
                    type(original_exception),
                    original_exception,
                    original_exception.__traceback__,
                )
            )
        else:
            self.file_name = "Unknown"
            self.line_number = "Unknown"
            self.traceback = None

    def __str__(self) -> str:
        base_message = (
            f"Error in file [{self.file_name}] "
            f"at line [{self.line_number}]: {self.message}"
        )

        if self.original_exception:
            base_message += f"\nOriginal Error: {repr(self.original_exception)}"

        if self.traceback:
            base_message += f"\nTraceback:\n{self.traceback}"

        return base_message

    def to_dict(self):
        """
        Structured format for API responses / monitoring.
        """
        return {
            "message": self.message,
            "file": self.file_name,
            "line": self.line_number,
            "original_error": repr(self.original_exception),
        }
