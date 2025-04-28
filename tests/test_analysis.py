import pytest
from pathlib import Path
from src.analysis import walk_repo_files, parse_and_find_functions, analyze_repository

@pytest.fixture
def test_repo(tmp_path):
    """Create a test repository structure."""
    repo = tmp_path / "test_repo"
    repo.mkdir()
    
    # Create some Python files
    (repo / "src").mkdir()
    (repo / "tests").mkdir()
    (repo / "venv").mkdir()  # Should be excluded
    
    # Create test files
    (repo / "src" / "main.py").write_text("""
def hello():
    print("Hello, world!")

class TestClass:
    def test_method(self):
        pass""".strip())
    
    (repo / "tests" / "test_main.py").write_text("""
def test_hello():
    assert True""".strip())
    
    return repo

def test_walk_repo_files(test_repo):
    """Test repository file traversal."""
    files = walk_repo_files(str(test_repo))
    assert len(files) == 2
    assert any("main.py" in str(f) for f in files)
    assert any("test_main.py" in str(f) for f in files)
    
    # Test with custom exclude patterns
    files = walk_repo_files(str(test_repo), exclude_patterns=["tests/"])
    assert len(files) == 1
    assert "main.py" in str(files[0])

def test_parse_and_find_functions(test_repo):
    """Test function parsing."""
    main_file = test_repo / "src" / "main.py"
    functions = parse_and_find_functions(main_file)
    
    assert len(functions) == 2
    assert any(f["name"] == "hello" for f in functions)
    assert any(f["name"] == "TestClass.test_method" for f in functions)
    
    # Test function details
    hello_func = next(f for f in functions if f["name"] == "hello")
    assert hello_func["lineno"] == 1  # First line after strip()
    assert not hello_func["is_method"]
    assert hello_func["args"] == []
    
    method = next(f for f in functions if f["name"] == "TestClass.test_method")
    assert method["is_method"]
    assert method["args"] == ["self"]

def test_analyze_repository(test_repo):
    """Test full repository analysis."""
    results = analyze_repository(str(test_repo))
    
    assert len(results) == 2
    assert any("main.py" in path for path in results.keys())
    assert any("test_main.py" in path for path in results.keys())
    
    # Test with custom exclude patterns
    results = analyze_repository(str(test_repo), exclude_patterns=["tests/"])
    assert len(results) == 1
    assert "main.py" in list(results.keys())[0] 