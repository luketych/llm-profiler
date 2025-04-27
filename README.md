# LLM Profiler

A semi-automated tool for inserting logging statements into Python codebases.

## Features

- Clones source code repositories
- Identifies functions in Python code
- Inserts logging statements at function boundaries
- Commits changes incrementally
- Runs tests after each change
- Requires human approval before proceeding

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd llm-profiler
```

2. Install dependencies using Poetry:
```bash
# Install Poetry if you haven't already
pipx install poetry

# Install project dependencies
pipx run poetry install
```

## Usage

```bash
# Run using the installed CLI script
pipx run poetry run llm-profiler <repository-url> [--target-dir TARGET_DIR]
```

### Arguments

- `repository-url`: URL of the repository to process
- `--target-dir`: Target directory for cloning (default: ./workspace)

## Development

The project is structured into milestones:

1. Initial Setup
2. Code Analysis
3. Logging Insertion
4. Version Control
5. Testing and Approval

## License

MIT License 