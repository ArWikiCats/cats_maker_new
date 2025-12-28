import difflib
import logging
from typing import Optional, Union

from .printe_helper import make_str


class LoggerWrap:
    """Project-scoped logger with colorized helpers."""

    def __init__(self, name: str, level: int = logging.INFO, disable_log: bool = False) -> None:
        """Initialize the wrapped logger and optionally disable output."""
        self._logger = logging.getLogger(name)

        # Prevent leaking to root logger
        self._logger.propagate = False

        if disable_log:
            self._logger.disabled = True
            return

        if not self._logger.handlers:
            self._logger.setLevel(level)

            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)

            self._logger.addHandler(handler)

    def logger(self) -> logging.Logger:
        """Expose the raw ``logging.Logger`` instance."""
        return self._logger

    def debug(self, msg: str, *args, **kwargs) -> None:
        """Log a debug message after formatting color codes."""
        self._logger.debug(make_str(msg), *args, **kwargs)

    def info(self, msg: str, *args, **kwargs) -> None:
        """Log an info message after formatting color codes."""
        self._logger.info(make_str(msg), *args, **kwargs)

    def warning(self, msg: str, *args, **kwargs) -> None:
        """Log a warning message with formatted content."""
        self._logger.warning(make_str(msg), *args, **kwargs)

    def error(self, msg: str, *args, **kwargs) -> None:
        """Log an error message with formatted content."""
        self._logger.error(make_str(msg), *args, **kwargs)

    def critical(self, msg: str, *args, **kwargs) -> None:
        """Log a critical message with formatted content."""
        self._logger.critical(make_str(msg), *args, **kwargs)

    def exception(self, msg: str, *args, **kwargs) -> None:
        """Log an exception with traceback using formatted content."""
        self._logger.exception(make_str(msg), *args, **kwargs)

    def log(self, level: int, msg: str, *args, **kwargs) -> None:
        """Log at an arbitrary level with formatted content."""
        self._logger.log(level, make_str(msg), *args, **kwargs)

    def showDiff(self, oldtext: str, newtext: str) -> None:
        """Show the difference between two text strings using the logger."""

        diff = difflib.unified_diff(
            oldtext.splitlines(),
            newtext.splitlines(),
            lineterm="",
            fromfile="Old Text",
            tofile="New Text",
        )
        for line in diff:
            if line.startswith("+") and not line.startswith("+++"):
                self._logger.warning(make_str(f"<<lightgreen>>{line}<<default>>"))
            elif line.startswith("-") and not line.startswith("---"):
                self._logger.warning(make_str(f"<<lightred>>{line}<<default>>"))
            else:
                self._logger.warning(make_str(line))

    def output(self, msg: str, *args, **kwargs) -> None:
        """Alias for info logging while preserving formatting."""
        self._logger.info(make_str(msg), *args, **kwargs)


logger = LoggerWrap("mknew")


def config_logger(level: Optional[Union[int, str]] = None, name: str = "mknew") -> None:
    """Configure the root logger with sensible defaults for the project."""
    global logger
    _levels = [
        "CRITICAL",
        "ERROR",
        "WARNING",
        "INFO",
        "DEBUG",
        "NOTSET",
    ]

    if not level:
        level = logging.DEBUG

    logger = LoggerWrap(name, level=level)

    # logging.basicConfig(
    #     filename=name,
    #     level=level,
    #     format="%(levelname)s - %(message)s",
    #     datefmt="%Y-%m-%d %H:%M:%S",
    # )


__all__ = [
    "logger",
    "LoggerWrap",
    "config_logger",
]
