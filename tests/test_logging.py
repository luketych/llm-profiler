import pytest
import logging
import logging.handlers
from pathlib import Path
from io import StringIO
from src.config import LOG_FILE, LOG_FORMAT, LOG_LEVEL

def test_log_file_creation(tmp_path):
    """Test log file creation."""
    log_file = tmp_path / "test.log"
    handler = logging.FileHandler(log_file)
    logger = logging.getLogger("test_logger")
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    
    # Log a test message
    test_message = "Test log message"
    logger.info(test_message)
    
    # Check if file exists and contains the message
    assert log_file.exists()
    with open(log_file, 'r') as f:
        content = f.read()
        assert test_message in content

def test_log_levels():
    """Test different log levels."""
    logger = logging.getLogger("test_logger")
    
    # Test each log level
    levels = {
        "DEBUG": "Debug message",
        "INFO": "Info message",
        "WARNING": "Warning message",
        "ERROR": "Error message",
        "CRITICAL": "Critical message"
    }
    
    for level, message in levels.items():
        log_level = getattr(logging, level)
        logger.setLevel(log_level)
        getattr(logger, level.lower())(message)

def test_log_format():
    """Test log message formatting."""
    logger = logging.getLogger("test_logger")
    stream = StringIO()
    handler = logging.StreamHandler(stream)
    formatter = logging.Formatter(LOG_FORMAT)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    
    # Log a test message
    test_message = "Test format message"
    logger.info(test_message)
    
    # The format should include timestamp, logger name, level, and message
    output = stream.getvalue()
    assert "test_logger" in output
    assert "INFO" in output
    assert test_message in output

def test_log_rotation(tmp_path):
    """Test log file rotation."""
    log_file = tmp_path / "test.log"
    handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=100,
        backupCount=3
    )
    logger = logging.getLogger("test_logger")
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    
    # Write enough logs to trigger rotation
    for i in range(10):
        logger.info(f"Test message {i}" * 10)
    
    # Check if rotation files were created
    assert log_file.exists()
    assert (tmp_path / "test.log.1").exists()
    assert (tmp_path / "test.log.2").exists()
    assert (tmp_path / "test.log.3").exists() 