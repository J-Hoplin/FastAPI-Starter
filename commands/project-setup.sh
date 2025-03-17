#!/bin/bash

# Maintainer: Hoplin
# Setup script for non-uv installed environments

echo "Setting up environment"
if ! command -v uv &> /dev/null; then
    echo "uv not found. Installing uv"
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        curl -LsSf https://astral.sh/uv/install.sh | sh
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        if command -v brew &> /dev/null; then
            brew install uv
        else
            curl -LsSf https://astral.sh/uv/install.sh | sh
        fi
    elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        echo "Please install uv manually: https://github.com/astral-sh/uv"
        exit 1
    else
        echo "Unsupported OS"
        exit 1
    fi

    if [[ -f ~/.bashrc ]]; then
        source ~/.bashrc
    elif [[ -f ~/.zshrc ]]; then
        source ~/.zshrc
    fi

    if ! command -v uv &> /dev/null; then
        echo "uv installation may have failed."
        exit 1
    fi

    echo "uv installed successfully"
fi

if [[ ! -f "pyproject.toml" ]]; then
    echo "pyproject.toml not found."
    exit 1
fi

if [[ ! -d ".venv" ]]; then
    echo "Creating virtual environment..."
    uv venv
    echo "Virtual environment created"
fi

echo "Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows
    source .venv/Scripts/activate
else
    # Unix-like systems
    source .venv/bin/activate
fi

echo "Installing dependencies from pyproject.toml..."
uv pip install -e .
echo "Dependencies installed successfully"

echo "Exporting dependencies to requirements.txt..."
uv pip freeze > requirements.txt
echo "requirements.txt generated"
