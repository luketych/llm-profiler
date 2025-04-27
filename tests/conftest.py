import os
import pytest
from pathlib import Path
from git import Repo

@pytest.fixture
def temp_workspace(tmp_path):
    """Create a temporary workspace directory."""
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    return workspace

@pytest.fixture
def test_repo_url():
    """Return a test repository URL."""
    return "https://github.com/octocat/Hello-World.git"

@pytest.fixture
def mock_repo(temp_workspace):
    """Create a mock Git repository."""
    repo = Repo.init(temp_workspace)
    # Create a test file
    test_file = temp_workspace / "test.py"
    test_file.write_text("def test_function():\n    pass\n")
    # Add and commit the file
    repo.index.add(["test.py"])
    repo.index.commit("Initial commit")
    return repo

@pytest.fixture
def test_config():
    """Return test configuration."""
    return {
        "workspace_dir": "test_workspace",
        "log_file": "test.log",
        "log_level": "INFO"
    } 