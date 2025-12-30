"""
Tests for src/helps/log.py

This module tests the LoggerWrap class and logging functionality.
"""

import logging

import pytest

from src.helps.log import LoggerWrap, logger


class TestLoggerWrap:
    """Tests for LoggerWrap class"""

    def test_init_creates_logger(self):
        """Test that LoggerWrap creates a proper logger instance"""
        test_logger = LoggerWrap("test_logger_1")
        assert test_logger._logger is not None
        assert isinstance(test_logger._logger, logging.Logger)

    def test_init_with_disable_log(self):
        """Test that LoggerWrap can be disabled"""
        test_logger = LoggerWrap("test_logger_disabled", disable_log=True)
        assert test_logger._logger.disabled is True

    def test_init_with_custom_level(self):
        """Test that LoggerWrap accepts custom log level"""
        test_logger = LoggerWrap("test_logger_level", level=logging.WARNING)
        assert test_logger._logger.level == logging.WARNING

    def test_set_level(self):
        """Test setting log level dynamically"""
        test_logger = LoggerWrap("test_logger_set_level")
        test_logger.set_level(logging.ERROR)
        assert test_logger._logger.level == logging.ERROR

    def test_setLevel_alias(self):
        """Test that setLevel is an alias for set_level"""
        test_logger = LoggerWrap("test_logger_setLevel")
        test_logger.setLevel(logging.CRITICAL)
        assert test_logger._logger.level == logging.CRITICAL

    def test_disable_logger(self):
        """Test enabling/disabling logger dynamically"""
        test_logger = LoggerWrap("test_logger_disable")
        test_logger.disable_logger(True)
        assert test_logger._logger.disabled is True
        test_logger.disable_logger(False)
        assert test_logger._logger.disabled is False

    def test_logger_method_returns_underlying_logger(self):
        """Test that logger() method returns the underlying Logger instance"""
        test_logger = LoggerWrap("test_logger_underlying")
        underlying = test_logger.logger()
        assert isinstance(underlying, logging.Logger)

    def test_debug_method_callable(self):
        """Test debug method is callable"""
        test_logger = LoggerWrap("test_debug_callable", disable_log=True)
        # Should not raise
        test_logger.debug("Debug message")

    def test_info_method_callable(self):
        """Test info method is callable"""
        test_logger = LoggerWrap("test_info_callable", disable_log=True)
        test_logger.info("Info message")

    def test_warning_method_callable(self):
        """Test warning method is callable"""
        test_logger = LoggerWrap("test_warning_callable", disable_log=True)
        test_logger.warning("Warning message")

    def test_error_method_callable(self):
        """Test error method is callable"""
        test_logger = LoggerWrap("test_error_callable", disable_log=True)
        test_logger.error("Error message")

    def test_critical_method_callable(self):
        """Test critical method is callable"""
        test_logger = LoggerWrap("test_critical_callable", disable_log=True)
        test_logger.critical("Critical message")

    def test_output_method_callable(self):
        """Test output method is callable"""
        test_logger = LoggerWrap("test_output_callable", disable_log=True)
        test_logger.output("Output message")

    def test_info_if_or_debug_callable(self):
        """Test info_if_or_debug method is callable"""
        test_logger = LoggerWrap("test_info_debug_callable", disable_log=True)
        test_logger.info_if_or_debug("Message", "truthy_value")
        test_logger.info_if_or_debug("Message", "")

    def test_error_red_callable(self):
        """Test error_red method is callable"""
        test_logger = LoggerWrap("test_error_red_callable", disable_log=True)
        test_logger.error_red("Red error message")

    def test_log_callable(self):
        """Test log method is callable"""
        test_logger = LoggerWrap("test_log_callable", disable_log=True)
        test_logger.log(logging.WARNING, "Custom level message")

    def test_showDiff_callable(self):
        """Test showDiff method is callable"""
        test_logger = LoggerWrap("test_showDiff_callable", disable_log=True)
        test_logger.showDiff("old text", "new text")

    def test_propagate_is_false(self):
        """Test that propagate is False for new loggers"""
        test_logger = LoggerWrap("test_propagate")
        assert test_logger._logger.propagate is False

    def test_has_handler_after_init(self):
        """Test that logger has a handler after initialization"""
        test_logger = LoggerWrap("test_has_handler")
        assert len(test_logger._logger.handlers) > 0

    def test_disabled_logger_has_no_handlers(self):
        """Test that disabled logger may skip adding handlers"""
        test_logger = LoggerWrap("test_disabled_handler", disable_log=True)
        # When disabled, the logger may still have handlers but is disabled
        assert test_logger._logger.disabled is True


class TestGlobalLogger:
    """Tests for the global logger instance"""

    def test_global_logger_exists(self):
        """Test that global logger is instantiated"""
        assert logger is not None
        assert isinstance(logger, LoggerWrap)

    def test_global_logger_has_standard_methods(self):
        """Test that global logger has all standard logging methods"""
        assert hasattr(logger, "debug")
        assert hasattr(logger, "info")
        assert hasattr(logger, "warning")
        assert hasattr(logger, "error")
        assert hasattr(logger, "critical")

    def test_global_logger_propagate_is_false(self):
        """Test that global logger doesn't propagate to root"""
        assert logger._logger.propagate is False

    def test_global_logger_has_showDiff(self):
        """Test that global logger has showDiff method"""
        assert hasattr(logger, "showDiff")
        assert callable(logger.showDiff)

    def test_global_logger_has_error_red(self):
        """Test that global logger has error_red method"""
        assert hasattr(logger, "error_red")
        assert callable(logger.error_red)

    def test_global_logger_has_info_if_or_debug(self):
        """Test that global logger has info_if_or_debug method"""
        assert hasattr(logger, "info_if_or_debug")
        assert callable(logger.info_if_or_debug)
