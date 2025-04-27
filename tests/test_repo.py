import pytest
from pathlib import Path
from git import Repo
from src.main import clone_repo

def test_clone_repo_success(temp_workspace, test_repo_url):
    """Test successful repository cloning."""
    repo = clone_repo(test_repo_url, str(temp_workspace))
    assert isinstance(repo, Repo)
    assert repo.working_dir == str(temp_workspace)
    assert Path(temp_workspace / ".git").exists()

def test_clone_repo_invalid_url(temp_workspace):
    """Test cloning with invalid URL."""
    with pytest.raises(Exception):
        clone_repo("invalid_url", str(temp_workspace))

def test_clone_repo_existing_dir(temp_workspace, mock_repo):
    """Test cloning to existing directory."""
    with pytest.raises(Exception):
        clone_repo("https://github.com/octocat/Hello-World.git", str(temp_workspace))

def test_clone_repo_permissions(tmp_path):
    """Test cloning with permission issues."""
    # Create a directory with no write permissions
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    workspace.chmod(0o444)  # Read-only
    
    with pytest.raises(Exception):
        clone_repo("https://github.com/octocat/Hello-World.git", str(workspace))
    
    # Clean up
    workspace.chmod(0o777) 