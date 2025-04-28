#!/usr/bin/env python3

import os
import ast
import logging
from pathlib import Path
from typing import List, Set, Dict, Any

logger = logging.getLogger(__name__)

def walk_repo_files(repo_path: str, exclude_patterns: List[str] = None) -> List[Path]:
    """
    Walk through repository files and return Python files.
    
    Args:
        repo_path (str): Path to the repository
        exclude_patterns (List[str]): List of patterns to exclude
        
    Returns:
        List[Path]: List of Python file paths
    """
    if exclude_patterns is None:
        exclude_patterns = [
            "venv/",
            ".venv/",
            "env/",
            ".env/",
            "__pycache__/",
            "*.pyc",
            "*.pyo",
            "*.pyd",
            ".git/",
            "node_modules/",
            "dist/",
            "build/",
            "*.egg-info/"
        ]
    
    python_files = []
    repo_path = Path(repo_path)
    
    for root, _, files in os.walk(repo_path):
        root_path = Path(root)
        
        # Skip excluded directories
        if any(pattern in str(root_path) for pattern in exclude_patterns):
            continue
            
        for file in files:
            if file.endswith('.py'):
                file_path = root_path / file
                # Skip excluded files
                if not any(pattern in str(file_path) for pattern in exclude_patterns):
                    python_files.append(file_path)
    
    return python_files

def parse_and_find_functions(file_path: Path) -> List[Dict[str, Any]]:
    """
    Parse a Python file and find all function definitions.
    
    Args:
        file_path (Path): Path to the Python file
        
    Returns:
        List[Dict[str, Any]]: List of function information dictionaries
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        tree = ast.parse(content)
        functions = []
        
        class FunctionVisitor(ast.NodeVisitor):
            def visit_FunctionDef(self, node):
                # Skip if this is a class method (will be handled in visit_ClassDef)
                if not isinstance(node.parent, ast.ClassDef):
                    function_info = {
                        'name': node.name,
                        'lineno': node.lineno,
                        'end_lineno': node.end_lineno,
                        'is_method': False,
                        'decorators': [d.id for d in node.decorator_list if isinstance(d, ast.Name)],
                        'args': [arg.arg for arg in node.args.args],
                        'returns': ast.unparse(node.returns) if node.returns else None
                    }
                    functions.append(function_info)
                self.generic_visit(node)
                
            def visit_ClassDef(self, node):
                for class_node in node.body:
                    if isinstance(class_node, ast.FunctionDef):
                        function_info = {
                            'name': f"{node.name}.{class_node.name}",
                            'lineno': class_node.lineno,
                            'end_lineno': class_node.end_lineno,
                            'is_method': True,
                            'decorators': [d.id for d in class_node.decorator_list if isinstance(d, ast.Name)],
                            'args': [arg.arg for arg in class_node.args.args],
                            'returns': ast.unparse(class_node.returns) if class_node.returns else None
                        }
                        functions.append(function_info)
                self.generic_visit(node)
        
        # Add parent references to nodes
        for node in ast.walk(tree):
            for child in ast.iter_child_nodes(node):
                child.parent = node
        
        visitor = FunctionVisitor()
        visitor.visit(tree)
        return functions
    except Exception as e:
        logger.error(f"Error parsing file {file_path}: {str(e)}")
        return []

def analyze_repository(repo_path: str, exclude_patterns: List[str] = None) -> Dict[str, List[Dict[str, Any]]]:
    """
    Analyze a repository and find all functions.
    
    Args:
        repo_path (str): Path to the repository
        exclude_patterns (List[str]): List of patterns to exclude
        
    Returns:
        Dict[str, List[Dict[str, Any]]]: Dictionary mapping file paths to their functions
    """
    python_files = walk_repo_files(repo_path, exclude_patterns)
    results = {}
    
    for file_path in python_files:
        functions = parse_and_find_functions(file_path)
        if functions:
            results[str(file_path)] = functions
    
    return results 