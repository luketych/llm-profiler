import pytest
from click.testing import CliRunner
from src.cli import main

@pytest.fixture
def cli_runner():
    """Create a CLI runner for testing."""
    return CliRunner()

def test_cli_help(cli_runner):
    """Test help message."""
    result = cli_runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.output
    assert "Options:" in result.output
    assert "Arguments:" in result.output

def test_cli_missing_repo_url(cli_runner):
    """Test missing repository URL."""
    result = cli_runner.invoke(main)
    assert result.exit_code != 0
    assert "Error: Missing argument 'REPO_URL'" in result.output

def test_cli_invalid_repo_url(cli_runner):
    """Test invalid repository URL."""
    result = cli_runner.invoke(main, ["invalid_url"])
    assert result.exit_code != 0
    assert "Error:" in result.output

def test_cli_custom_target_dir(cli_runner, tmp_path):
    """Test custom target directory."""
    target_dir = str(tmp_path / "custom_workspace")
    result = cli_runner.invoke(main, [
        "https://github.com/octocat/Hello-World.git",
        "--target-dir", target_dir
    ])
    assert result.exit_code == 0
    assert "Successfully cloned repository" in result.output

def test_cli_existing_target_dir(cli_runner, tmp_path):
    """Test existing target directory."""
    target_dir = tmp_path / "existing_workspace"
    target_dir.mkdir()
    
    result = cli_runner.invoke(main, [
        "https://github.com/octocat/Hello-World.git",
        "--target-dir", str(target_dir)
    ])
    assert result.exit_code == 0
    assert "Successfully cloned repository" in result.output 