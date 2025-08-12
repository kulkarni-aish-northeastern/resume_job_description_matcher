#!/bin/bash

# Force Python version and install dependencies
echo "Installing Python dependencies..."

# Upgrade pip and setuptools first
python -m pip install --upgrade pip setuptools wheel build

# Install dependencies
pip install -r requirements.txt

echo "Build completed successfully!"
