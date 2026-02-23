#!/bin/bash
# Quick Setup Script for HADDOCK3 MCP
# HADDOCK3: High Ambiguity Driven protein-protein DOCKing
# Integrative modeling of biomolecular interactions with experimental data
# Source: https://github.com/haddocking/haddock3

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== Setting up HADDOCK3 MCP ==="

# Step 1: Create Python environment
echo "[1/5] Creating Python 3.12 environment..."
(command -v mamba >/dev/null 2>&1 && mamba create -p ./env python=3.12 pip -y) || \
(command -v conda >/dev/null 2>&1 && conda create -p ./env python=3.12 pip -y) || \
(echo "Warning: Neither mamba nor conda found, creating venv instead" && python3 -m venv ./env)

# Step 2: Install core dependencies
echo "[2/5] Installing core dependencies..."
./env/bin/pip install numpy scipy pandas biopython pdb-tools

# Step 3: Install utility packages
echo "[3/5] Installing utility packages..."
./env/bin/pip install loguru click tqdm

# Step 4: Install fastmcp
echo "[4/5] Installing fastmcp..."
./env/bin/pip install --ignore-installed fastmcp

# Step 5: Install HADDOCK3 from repo
echo "[5/5] Installing HADDOCK3..."
cd repo/haddock3 && ../../env/bin/pip install -e . && cd ../..

echo ""
echo "=== HADDOCK3 MCP Setup Complete ==="
echo "Usage: haddock3 <configuration-file.toml>"
echo "For MPI support: pip install 'haddock3[mpi]'"
echo "Documentation: https://www.bonvinlab.org/haddock3-user-manual"
echo "To run the MCP server: ./env/bin/python src/server.py"
