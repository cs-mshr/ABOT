```markdown
# Python and Poetry Installation Guide

This guide explains how to install Python and Poetry on macOS.

## Prerequisites

- macOS system
- Homebrew installed (if not, install it from [https://brew.sh](https://brew.sh))

## Step 1: Install Python

### Option 1: Using Homebrew
```bash
brew install python
```

### Option 2: Download from Python.org
Visit [https://www.python.org/downloads/](https://www.python.org/downloads/) and download the macOS installer.

## Step 2: Install Poetry

### Option 1: Using the Official Installer
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### Option 2: Using Homebrew
```bash
brew install poetry
```

## Step 3: Verify the Installations

### Check Python Version
```bash
python3 --version
```

### Check Poetry Version
```bash
poetry --version
```

## Step 4: Initialize a New Python Project with Poetry

Navigate to your project directory and run:
```bash
poetry init
```

This will guide you in creating a basic configuration file (`pyproject.toml`) for managing your dependencies.

## Additional Resources

- [Python Documentation](https://docs.python.org/3/)
- [Poetry Documentation](https://python-poetry.org/docs/)
```


STEPS of execution:
1. write all connectors
2. models for request and responses  -- use pydantic models
3. common model for data storage
4. fetcher service
5. arbitage manager  -- core logic          manager will only call service layer

main -->  manager --> service --> connector
