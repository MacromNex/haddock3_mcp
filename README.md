# HADDOCK3 MCP Tools

> MCP tools for HADDOCK3 molecular docking and cyclic peptide computational analysis

## Table of Contents
- [Overview](#overview)
- [Installation](#installation)
- [Local Usage (Scripts)](#local-usage-scripts)
- [MCP Server Installation](#mcp-server-installation)
- [Using with Claude Code](#using-with-claude-code)
- [Using with Gemini CLI](#using-with-gemini-cli)
- [Available Tools](#available-tools)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)

## Overview

This MCP server provides comprehensive tools for HADDOCK3-based molecular docking workflows specifically designed for cyclic peptides. HADDOCK3 is a leading computational tool for biomolecular docking that integrates experimental data to guide structure prediction and protein-peptide complex modeling.

### Features
- **Protein-Peptide Docking**: Advanced molecular docking with HADDOCK3's multi-stage protocol
- **Cyclic Peptide Cyclisation**: Convert linear peptides to cyclic forms with specialized distance restraints
- **Information-Driven Docking**: Integrate experimental data (NMR, mutagenesis, cross-linking) to guide docking
- **Batch Processing**: High-throughput virtual screening of peptide libraries
- **Job Management**: Asynchronous processing with real-time monitoring and result retrieval
- **Experimental Data Integration**: Support for active/passive residues and distance restraints

### Directory Structure
```
./
├── README.md                    # This file
├── env/                         # Conda environment with HADDOCK3
├── src/
│   └── server.py               # MCP server
│   └── jobs/                   # Job management system
├── scripts/
│   ├── protein_peptide_docking.py          # Basic docking protocol
│   ├── cyclic_peptide_cyclisation.py       # Peptide cyclisation
│   ├── information_driven_docking.py       # Experimental data-guided docking
│   └── lib/                    # Shared utilities
├── examples/
│   └── data/                   # Demo data for testing
│       ├── structures/         # Sample PDB structures (proteins & peptides)
│       ├── restraints/         # Experimental restraints files
│       └── sequences/          # Sample peptide sequences
├── configs/                    # Configuration templates
└── repo/                       # Original HADDOCK3 repository
```

---

## Installation

### Quick Setup

Run the automated setup script:

```bash
./quick_setup.sh
```

This will create the environment and install all dependencies automatically.

### Manual Setup (Advanced)

For manual installation or customization, follow these steps.

#### Prerequisites
- Conda or Mamba (mamba recommended for faster installation)
- Python 3.10+
- GCC/G++ compiler for HADDOCK3 C/C++ extensions
- 8+ GB RAM for typical docking jobs
- 10+ GB disk space per job

#### Create Environment

Please follow the information in `reports/step3_environment.md` for the complete procedure. An example workflow is shown below:

```bash
# Navigate to the MCP directory
cd /home/xux/Desktop/CycPepMCP/CycPepMCP/tool-mcps/haddock3_mcp

# Create conda environment (use mamba if available)
mamba create -p ./env python=3.12 pip -y
# or: conda create -p ./env python=3.12 pip -y

# Activate environment
mamba activate ./env
# or: conda activate ./env

# Install Core Scientific Dependencies
mamba run -p ./env pip install numpy scipy pandas biopython pdb-tools

# Install MCP dependencies
mamba run -p ./env pip install loguru click tqdm fastmcp

# Install HADDOCK3 (editable installation)
cd repo/haddock3
mamba run -p ../../env pip install -e .
cd ../..

# Force clean FastMCP installation (if needed)
mamba run -p ./env pip install --force-reinstall --no-cache-dir fastmcp
```

### Verify Installation

```bash
# Test core functionality
mamba run -p ./env python -c "
import numpy as np
import scipy as sp
import pandas as pd
import Bio
import haddock
import fastmcp
print('All critical imports successful')
"

# Check HADDOCK3 version
mamba run -p ./env haddock3 --version
# Expected output: haddock3 - 2025.11.0
```

---

## Local Usage (Scripts)

You can use the scripts directly without MCP for local processing.

### Available Scripts

| Script | Description | Runtime | Example |
|--------|-------------|---------|---------|
| `protein_peptide_docking.py` | Basic protein-peptide docking | 1-4 hours | See below |
| `cyclic_peptide_cyclisation.py` | Linear to cyclic peptide conversion | 30-90 min | See below |
| `information_driven_docking.py` | Experimental data-guided docking | 1-6 hours | See below |

### Script Examples

#### Protein-Peptide Docking

```bash
# Activate environment
mamba activate ./env

# Basic usage with demo data
python scripts/protein_peptide_docking.py

# Custom run with specific files
python scripts/protein_peptide_docking.py \
  --input-protein examples/data/structures/1NX1_protein.pdb \
  --input-peptide examples/data/structures/DAIDALSSDFT_3conformations.pdb \
  --ncores 8 \
  --output my_docking_results
```

**Parameters:**
- `--input-protein`: Protein structure in PDB format (required)
- `--input-peptide`: Peptide structure(s) - multiple conformations supported (required)
- `--restraints`: Ambiguous interaction restraints (.tbl format)
- `--ncores`: Number of CPU cores to use (default: 4)
- `--output`: Output directory name (default: auto-generated)

#### Cyclic Peptide Cyclisation

```bash
# Basic cyclisation with demo data
python scripts/cyclic_peptide_cyclisation.py

# Custom peptide with specified length
python scripts/cyclic_peptide_cyclisation.py \
  --input my_linear_peptide.pdb \
  --length 14 \
  --ncores 4 \
  --output cyclic_peptide_results
```

**Parameters:**
- `--input`: Linear peptide structure in PDB format (required)
- `--length`: Number of residues (auto-detected if not specified)
- `--ncores`: Number of CPU cores (default: 4)
- `--output`: Output directory name (default: auto-generated)

#### Information-Driven Docking

```bash
# Advanced usage with experimental restraints
python scripts/information_driven_docking.py \
  --input-protein examples/data/structures/1NX1_protein.pdb \
  --input-peptide examples/data/structures/DAIDALSSDFT_3conformations.pdb \
  --active-protein "36,109,113" \
  --active-peptide "1,5,8" \
  --passive-protein "34,38,110,111" \
  --passive-peptide "2,6,9" \
  --ncores 8
```

**Parameters:**
- `--input-protein`, `--input-peptide`: Structure files (required)
- `--active-protein`: Protein residues with strong experimental evidence
- `--active-peptide`: Peptide residues with strong experimental evidence
- `--passive-protein`: Protein residues with weak evidence or neighbors
- `--passive-peptide`: Peptide residues with weak evidence or neighbors

---

## MCP Server Installation

### Option 1: Using fastmcp (Recommended)

```bash
# Install MCP server for Claude Code
fastmcp install src/server.py --name haddock3-tools
```

### Option 2: Manual Installation for Claude Code

```bash
# Add MCP server to Claude Code
claude mcp add haddock3-tools -- $(pwd)/env/bin/python $(pwd)/src/server.py

# Verify installation
claude mcp list
```

### Option 3: Configure in settings.json

Add to `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "haddock3-tools": {
      "command": "/home/xux/Desktop/CycPepMCP/CycPepMCP/tool-mcps/haddock3_mcp/env/bin/python",
      "args": ["/home/xux/Desktop/CycPepMCP/CycPepMCP/tool-mcps/haddock3_mcp/src/server.py"]
    }
  }
}
```

---

## Using with Claude Code

After installing the MCP server, you can use it directly in Claude Code.

### Quick Start

```bash
# Start Claude Code
claude
```

### Example Prompts

#### Tool Discovery
```
What HADDOCK3 tools are available from haddock3-tools?
```

#### Protein-Peptide Docking
```
Submit a protein-peptide docking job using:
- Protein: @examples/data/structures/1NX1_protein.pdb
- Peptide: @examples/data/structures/DAIDALSSDFT_3conformations.pdb
Name the job "hiv_protease_docking"
```

#### Cyclic Peptide Cyclisation
```
Cyclise this linear peptide into cyclic form:
@examples/data/structures/1sfi_peptide-ensemble.pdb
```

#### Check Job Status
```
Check the status of job abc12345 and show me the logs if it's running
```

#### Information-Driven Docking
```
Perform information-driven docking with experimental data:
- Protein: @examples/data/structures/1NX1_protein.pdb
- Peptide: @examples/data/structures/DAIDALSSDFT_3conformations.pdb
- Active protein residues: 36,109,113 (from NMR data)
- Active peptide residues: 1,5,8 (key binding residues)
- Passive residues: neighbors of active sites
```

#### Batch Processing
```
Submit batch docking jobs for these peptides against 1NX1 protein:
- @examples/data/structures/DAIDALSSDFT_alpha.pdb
- @examples/data/structures/DAIDALSSDFT_ext.pdb
- @examples/data/structures/DAIDALSSDFT_polyII.pdb

Monitor progress and show results when completed.
```

### Using @ References

In Claude Code, use `@` to reference files and directories:

| Reference | Description |
|-----------|-------------|
| `@examples/data/structures/1NX1_protein.pdb` | HIV-1 protease protein |
| `@examples/data/structures/DAIDALSSDFT_3conformations.pdb` | Peptide ensemble |
| `@examples/data/restraints/ambig.tbl` | Experimental restraints |
| `@configs/protein_peptide_docking_config.json` | Configuration template |

---

## Using with Gemini CLI

### Configuration

Add to `~/.gemini/settings.json`:

```json
{
  "mcpServers": {
    "haddock3-tools": {
      "command": "/home/xux/Desktop/CycPepMCP/CycPepMCP/tool-mcps/haddock3_mcp/env/bin/python",
      "args": ["/home/xux/Desktop/CycPepMCP/CycPepMCP/tool-mcps/haddock3_mcp/src/server.py"]
    }
  }
}
```

### Example Prompts

```bash
# Start Gemini CLI
gemini

# Example prompts (same as Claude Code)
> What HADDOCK3 tools are available?
> Submit protein-peptide docking for HIV protease with peptide ensemble
> Check job status and retrieve results when complete
```

---

## Available Tools

### Quick Operations (Submit API)

All HADDOCK3 operations are long-running and use the submit API with job tracking:

| Tool | Description | Runtime | Parameters |
|------|-------------|---------|------------|
| `submit_protein_peptide_docking` | Basic protein-peptide docking | 1-4 hours | `protein_file`, `peptide_file`, `restraints_file`, `job_name` |
| `submit_cyclic_peptide_cyclisation` | Linear to cyclic conversion | 30-90 min | `peptide_file`, `peptide_length`, `job_name` |
| `submit_information_driven_docking` | Experimental data-guided docking | 1-6 hours | `protein_file`, `peptide_file`, `active_*/passive_*_residues`, `job_name` |
| `submit_batch_protein_peptide_docking` | Batch processing multiple peptides | Per job | `protein_file`, `peptide_files`, `restraints_file`, `job_name` |

### Job Management Tools

| Tool | Description |
|------|-------------|
| `get_job_status` | Check job progress and runtime |
| `get_job_result` | Get results when completed |
| `get_job_log` | View execution logs (with tail option) |
| `cancel_job` | Cancel running job |
| `list_jobs` | List all jobs (filterable by status) |

### Utility Tools

| Tool | Description |
|------|-------------|
| `validate_haddock_environment` | Check HADDOCK3 installation |
| `get_example_data_paths` | List available example data |
| `get_server_info` | Server capabilities and tool info |

---

## Examples

### Example 1: Basic Protein-Peptide Docking

**Goal:** Dock a peptide to HIV-1 protease using HADDOCK3

**Using Script:**
```bash
mamba activate ./env
python scripts/protein_peptide_docking.py \
  --input-protein examples/data/structures/1NX1_protein.pdb \
  --input-peptide examples/data/structures/DAIDALSSDFT_3conformations.pdb \
  --output hiv_protease_docking
```

**Using MCP (in Claude Code):**
```
Submit protein-peptide docking job:
- Protein: @examples/data/structures/1NX1_protein.pdb
- Peptide: @examples/data/structures/DAIDALSSDFT_3conformations.pdb
- Job name: "hiv_protease_analysis"

Monitor the job and show me the results when complete.
```

**Expected Output:**
- Docked protein-peptide complexes
- HADDOCK binding scores
- Structural clustering results
- Interface contact analysis

### Example 2: Cyclic Peptide Cyclisation

**Goal:** Convert linear peptide to cyclic form using distance restraints

**Using Script:**
```bash
python scripts/cyclic_peptide_cyclisation.py \
  --input examples/data/structures/1sfi_peptide-ensemble.pdb \
  --length 14 \
  --output cyclisation_results
```

**Using MCP (in Claude Code):**
```
Cyclise this linear peptide ensemble into cyclic form:
@examples/data/structures/1sfi_peptide-ensemble.pdb

Use automatic length detection and name the job "peptide_cyclisation_14mer"
```

**Expected Output:**
- Cyclised peptide conformations
- Conformational ensemble analysis
- Cyclisation quality assessment
- RMSD-based clustering

### Example 3: Information-Driven Docking with Experimental Data

**Goal:** Use NMR and mutagenesis data to guide peptide docking

**Using MCP (in Claude Code):**
```
I have experimental data for protein-peptide binding:

Protein: @examples/data/structures/1NX1_protein.pdb
Peptide: @examples/data/structures/DAIDALSSDFT_3conformations.pdb

From NMR chemical shift perturbation:
- Active protein residues: 36,109,113 (large shifts)
- Active peptide residues: 1,5,8 (critical for binding)

From mutagenesis studies:
- Passive protein residues: 34,38,110,111 (moderate effects)
- Passive peptide residues: 2,6,9 (neighboring residues)

Submit information-driven docking with this experimental data.
Monitor progress and analyze the restraint satisfaction in the results.
```

**Expected Output:**
- High-confidence docking solutions
- Experimental restraint satisfaction analysis
- Interface validation with confidence scores
- Clusters ranked by experimental consistency

### Example 4: Virtual Screening Pipeline

**Goal:** Screen multiple peptide conformations for drug discovery

**Using MCP (in Claude Code):**
```
I want to screen different peptide conformations against HIV protease:

Target: @examples/data/structures/1NX1_protein.pdb

Peptide library:
- @examples/data/structures/DAIDALSSDFT_alpha.pdb
- @examples/data/structures/DAIDALSSDFT_ext.pdb
- @examples/data/structures/DAIDALSSDFT_polyII.pdb

Submit batch docking jobs for all peptides.
Monitor progress and identify the best-scoring complexes.
Rank results by HADDOCK score and cluster size.
```

**Expected Output:**
- Multiple docking job IDs for parallel processing
- Comparative analysis of peptide conformations
- Ranking by binding affinity predictions
- Identification of optimal peptide structure

---

## Demo Data

The `examples/data/` directory contains validated datasets for testing:

### Structural Data

| File | Size | Description | Use Cases |
|------|------|-------------|-----------|
| `1NX1_protein.pdb` | 131 KB | HIV-1 protease structure | Protein-peptide docking, Info-driven docking |
| `1nx1_refe.pdb` | 113 KB | Reference complex for validation | All workflows (validation) |
| `DAIDALSSDFT_3conformations.pdb` | 23 KB | Peptide ensemble (3 conformations) | Docking workflows |
| `DAIDALSSDFT_alpha.pdb` | 7 KB | Alpha-helical peptide conformation | Virtual screening |
| `DAIDALSSDFT_ext.pdb` | 7 KB | Extended peptide conformation | Virtual screening |
| `DAIDALSSDFT_polyII.pdb` | 7 KB | Polyproline II conformation | Virtual screening |
| `1sfi_peptide-ensemble.pdb` | 34 KB | Linear peptide for cyclisation | Cyclisation workflow |
| `1sfi_peptide-bound.pdb` | 8 KB | Reference cyclic structure | Cyclisation validation |
| `3wne_peptide-ensemble.pdb` | 14 KB | Small peptide ensemble (6 residues) | Small peptide cyclisation |

### Restraints Data

| File | Description | Use Cases |
|------|-------------|-----------|
| `restraints/ambig.tbl` | Ambiguous interaction restraints for 1NX1-peptide | Docking protocols |
| `restraints/1sfi_unambig.tbl` | Distance restraints for 1SFI cyclisation | Cyclisation workflow |
| `restraints/3wne_unambig.tbl` | Distance restraints for 3WNE cyclisation | Small peptide cyclisation |

---

## Configuration Files

The `configs/` directory contains configuration templates:

| Config | Description | Parameters |
|--------|-------------|------------|
| `protein_peptide_docking_config.json` | Basic docking settings | cores, sampling, scoring |
| `cyclic_peptide_cyclisation_config.json` | Cyclisation protocol | restraints, clustering |
| `information_driven_docking_config.json` | Experimental data integration | restraint types, validation |
| `default_config.json` | Common settings | timeout, memory, paths |

### Config Example

```json
{
  "ncores": 8,
  "sampling": {
    "structures_it0": 1000,
    "structures_it1": 200,
    "structures_itw": 200
  },
  "clustering": {
    "clustfcc": true,
    "min_population": 4,
    "threshold": 7.5
  },
  "scoring": {
    "w_elec": 0.2,
    "w_vdw": 1.0,
    "w_desolv": 1.0,
    "w_air": 0.1
  }
}
```

---

## Troubleshooting

### Environment Issues

**Problem:** Environment not found or import errors
```bash
# Recreate environment
mamba create -p ./env python=3.12 pip -y
mamba activate ./env
mamba run -p ./env pip install numpy scipy pandas biopython pdb-tools
mamba run -p ./env pip install loguru click tqdm fastmcp

# Reinstall HADDOCK3
cd repo/haddock3
mamba run -p ../../env pip install -e .
cd ../..
```

**Problem:** HADDOCK3 import errors
```bash
# Verify HADDOCK3 installation
mamba run -p ./env python -c "import haddock; print('HADDOCK3 OK')"
mamba run -p ./env haddock3 --version

# Check for missing dependencies
mamba run -p ./env python -c "import Bio; print('Biopython OK')"
```

**Problem:** FastMCP conflicts
```bash
# Force clean reinstall
mamba run -p ./env pip install --force-reinstall --no-cache-dir fastmcp
```

### MCP Issues

**Problem:** Server not found in Claude Code
```bash
# Check MCP registration
claude mcp list

# Re-add if needed
claude mcp remove haddock3-tools
claude mcp add haddock3-tools -- $(pwd)/env/bin/python $(pwd)/src/server.py

# Test server directly
mamba run -p ./env python src/server.py
```

**Problem:** Tools not working
```bash
# Test server functionality
mamba run -p ./env python -c "
from src.server import mcp
tools = list(mcp.list_tools().keys())
print(f'Available tools: {len(tools)}')
for tool in tools:
    print(f'  - {tool}')
"
```

**Problem:** Job submission failures
```bash
# Check job directory permissions
ls -la jobs/
mkdir -p jobs
chmod 755 jobs

# Verify example data exists
ls -la examples/data/structures/
```

### Job Issues

**Problem:** Job stuck in pending
```bash
# Check job status
python -c "
from src.jobs.manager import job_manager
jobs = job_manager.list_jobs()
print(jobs)
"

# Check job directory
ls -la jobs/<job_id>/
```

**Problem:** Job failed with HADDOCK3 errors
```bash
# View detailed logs
python -c "
from src.jobs.manager import job_manager
log = job_manager.get_job_log('<job_id>')
print('\n'.join(log['log_lines'][-50:]))  # Last 50 lines
"

# Check HADDOCK3 configuration
cat jobs/<job_id>/output/config.cfg
```

**Problem:** File path errors
```bash
# Verify file paths are absolute
python -c "
import os
print('Current directory:', os.getcwd())
print('Example files:')
for f in ['examples/data/structures/1NX1_protein.pdb']:
    abs_path = os.path.abspath(f)
    exists = os.path.exists(abs_path)
    print(f'  {abs_path}: {exists}')
"
```

### Resource Issues

**Problem:** Out of memory during docking
- Reduce `ncores` parameter to 4 or less
- Monitor system memory usage: `htop` or `free -h`
- Use smaller peptide ensembles or reduce sampling parameters

**Problem:** Disk space full
```bash
# Check disk usage
df -h .
du -sh jobs/*

# Clean old job directories
find jobs/ -name "*" -type d -mtime +7 -exec rm -rf {} \;
```

**Problem:** Long runtime (>6 hours)
- Check if job is actually running: `get_job_log` for recent activity
- Consider reducing sampling in configuration
- Verify adequate CPU cores available

---

## Development

### Running Tests

```bash
# Activate environment
mamba activate ./env

# Test server startup
python src/server.py

# Test job manager
python -c "
from src.jobs.manager import job_manager
print('Job manager status:', job_manager.list_jobs())
"

# Run integration tests
python tests/test_integration.py
```

### Starting Dev Server

```bash
# Run MCP server in development mode
mamba run -p ./env fastmcp dev src/server.py

# Test with Claude Code
claude
```

### Performance Optimization

```bash
# Monitor job performance
watch -n 30 "ps aux | grep python | grep -v grep"

# Check HADDOCK3 resource usage
htop  # Look for haddock3 and related processes
```

---

## License

Based on HADDOCK3 software suite. Please cite:

1. **HADDOCK3**: Giulini, M., et al. "Information-driven modeling and simulation of protein-protein interactions" J. Chem. Inf. Model. (2025)
2. **Cyclisation Protocol**: Trellet, M., et al. "A unified conformational selection and induced fit approach to protein-peptide docking" J. Chem. Theory Comput. (2022)
3. **Information-Driven Docking**: Reys, V., et al. "The HADDOCK2.4 web server for integrative modeling of biomolecular complexes" Nature Protocols (2024)

## Credits

Based on [HADDOCK3](https://github.com/haddocking/haddock3) - High Ambiguity Driven protein-protein DOCKing version 3