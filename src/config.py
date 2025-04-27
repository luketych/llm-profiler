import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent.absolute()
WORKSPACE_DIR = BASE_DIR / 'workspace'

# Logging configuration
LOG_FILE = BASE_DIR / 'profiler.log'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_LEVEL = 'INFO'

# Git configuration
GIT_USER_NAME = os.getenv('GIT_USER_NAME', 'LLM Profiler')
GIT_USER_EMAIL = os.getenv('GIT_USER_EMAIL', 'profiler@example.com')

# File patterns
PYTHON_FILE_PATTERN = '*.py'
EXCLUDE_PATTERNS = [
    'venv',
    'env',
    '__pycache__',
    '.git',
    'node_modules',
    'dist',
    'build'
]

# Logging message templates
START_LOG_TEMPLATE = 'logger.info("START {function_name}")'
END_LOG_TEMPLATE = 'logger.info("END {function_name}")' 