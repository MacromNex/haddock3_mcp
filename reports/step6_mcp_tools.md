# Step 6: MCP Tools Documentation

## Server Information
- **Server Name**: haddock3-cycpep
- **Version**: 1.0.0
- **Created Date**: 2025-12-31
- **Server Path**: `src/server.py`
- **Job Manager**: `src/jobs/manager.py`
- **Dependencies**: fastmcp, loguru, pathlib, threading, subprocess

## Overview

This MCP server provides asynchronous (submit-based) APIs for HADDOCK3 molecular docking and cyclisation operations specifically designed for cyclic peptides. All operations are long-running (30 minutes to 6 hours) and use a sophisticated job management system for tracking and retrieving results.

**Key Features:**
- ✅ Submit API for all long-running HADDOCK3 operations
- ✅ Job queue management with persistent storage
- ✅ Real-time progress tracking and logging
- ✅ Batch processing support
- ✅ Result parsing and structured output
- ✅ Error handling and recovery
- ✅ No synchronous tools (all operations are computationally intensive)

---

## Job Management Tools

All HADDOCK3 operations return a `job_id` that can be used with these management tools:

| Tool | Description | Returns |
|------|-------------|---------|
| `get_job_status` | Check job progress and runtime | Status, timestamps, runtime info |
| `get_job_result` | Get completed job results | HADDOCK3 outputs, structures, analysis |
| `get_job_log` | View job execution logs | Log lines, error messages |
| `cancel_job` | Cancel running job | Success/error status |
| `list_jobs` | List all jobs (filterable) | Job summaries with status |

### Job Status Flow
```
submit_* → PENDING → RUNNING → COMPLETED/FAILED/CANCELLED
                       ↓
                 get_job_log (anytime)
                       ↓
              get_job_result (when completed)
```

---

## HADDOCK3 Submit Tools

### Protein-Peptide Docking

**Tool**: `submit_protein_peptide_docking`

**Description**: Submit protein-peptide docking using HADDOCK3's molecular docking protocol

**Runtime**: 1-4 hours (depends on protein/peptide complexity and sampling)

**Parameters**:
```python
submit_protein_peptide_docking(
    protein_file: str,           # Path to protein PDB structure
    peptide_file: str,           # Path to peptide PDB (multiple conformations supported)
    output_dir: Optional[str],   # Output directory (auto-created if None)
    restraints_file: Optional[str], # Ambiguous restraints (.tbl format)
    job_name: Optional[str]      # Custom job name for tracking
)
```

**Source Script**: `scripts/protein_peptide_docking.py`

**Example Usage**:
```python
result = submit_protein_peptide_docking(
    protein_file="examples/data/structures/protein.pdb",
    peptide_file="examples/data/structures/cyclic_peptide.pdb",
    job_name="my_docking_run"
)
job_id = result["job_id"]

# Monitor progress
status = get_job_status(job_id)
log = get_job_log(job_id)

# Get results when completed
final_result = get_job_result(job_id)
```

---

### Cyclic Peptide Cyclisation

**Tool**: `submit_cyclic_peptide_cyclisation`

**Description**: Cyclise linear peptides into cyclic forms using HADDOCK3's cyclisation protocol

**Runtime**: 30-90 minutes (depends on peptide length and complexity)

**Parameters**:
```python
submit_cyclic_peptide_cyclisation(
    peptide_file: str,              # Path to linear peptide PDB
    peptide_length: Optional[int],  # Residue count (auto-detected if None)
    output_dir: Optional[str],      # Output directory (auto-created if None)
    job_name: Optional[str]         # Custom job name for tracking
)
```

**Source Script**: `scripts/cyclic_peptide_cyclisation.py`

**Example Usage**:
```python
result = submit_cyclic_peptide_cyclisation(
    peptide_file="linear_peptide.pdb",
    peptide_length=12,
    job_name="cyclise_12mer"
)
```

---

### Information-Driven Docking

**Tool**: `submit_information_driven_docking`

**Description**: Perform information-driven docking using experimental restraints and active/passive residues

**Runtime**: 1-6 hours (depends on restraint complexity and sampling requirements)

**Parameters**:
```python
submit_information_driven_docking(
    protein_file: str,                      # Path to protein PDB structure
    peptide_file: str,                      # Path to peptide PDB structure
    active_protein_residues: Optional[str], # "36,109,113" - strong evidence
    active_peptide_residues: Optional[str], # "1,5,8" - strong evidence
    passive_protein_residues: Optional[str], # Weak evidence/neighbors
    passive_peptide_residues: Optional[str], # Weak evidence/neighbors
    output_dir: Optional[str],              # Output directory
    job_name: Optional[str]                 # Custom job name
)
```

**Source Script**: `scripts/information_driven_docking.py`

**Example Usage**:
```python
result = submit_information_driven_docking(
    protein_file="protein.pdb",
    peptide_file="peptide.pdb",
    active_protein_residues="36,109,113",
    active_peptide_residues="1,5,8",
    passive_protein_residues="35,37,108,110,112,114",
    job_name="info_guided_docking"
)
```

---

## Batch Processing Tools

### Batch Protein-Peptide Docking

**Tool**: `submit_batch_protein_peptide_docking`

**Description**: Submit multiple peptides for docking against the same protein in parallel

**Parameters**:
```python
submit_batch_protein_peptide_docking(
    protein_file: str,               # Single protein for all dockings
    peptide_files: List[str],        # List of peptide PDB files
    restraints_file: Optional[str],  # Common restraints (optional)
    output_base_dir: Optional[str],  # Base directory for outputs
    job_name: Optional[str]          # Base name for batch jobs
)
```

**Returns**: List of job_ids for individual docking jobs

**Example Usage**:
```python
peptides = ["peptide1.pdb", "peptide2.pdb", "peptide3.pdb"]
result = submit_batch_protein_peptide_docking(
    protein_file="target_protein.pdb",
    peptide_files=peptides,
    job_name="screening_batch"
)

job_ids = result["job_ids"]
for job_id in job_ids:
    status = get_job_status(job_id)
    print(f"Job {job_id}: {status['status']}")
```

---

## Utility Tools

### Environment Validation

**Tool**: `validate_haddock_environment`

**Description**: Check HADDOCK3 installation and environment configuration

**Returns**: Environment status, HADDOCK3 availability, configuration details

### Example Data Access

**Tool**: `get_example_data_paths`

**Description**: Get paths to available example data files for testing

**Returns**: Lists of available protein and peptide structure files

### Server Information

**Tool**: `get_server_info`

**Description**: Get comprehensive server information including tool capabilities

**Returns**: Server metadata, tool categories, runtime estimates, requirements

---

## Configuration and File Formats

### Input Files

| File Type | Format | Description | Example |
|-----------|--------|-------------|---------|
| Protein Structure | `.pdb` | Standard PDB format | Single chain protein |
| Peptide Structure | `.pdb` | PDB with multiple conformations supported | Linear or pre-cyclised peptide |
| Restraints | `.tbl` | HADDOCK3 table format | Ambiguous/unambiguous restraints |

### Output Structure

Each job creates a structured output directory:

```
jobs/{job_id}/
├── metadata.json          # Job metadata and status
├── job.log               # Execution log
├── output/               # HADDOCK3 output directory
│   ├── config.cfg       # Used configuration
│   ├── restraints.tbl   # Applied restraints
│   └── structures/      # Final docked structures
├── work/                # HADDOCK3 working directory
│   ├── clustfcc*/       # Clustering results
│   └── {modules}/       # HADDOCK3 module outputs
└── results.json         # Parsed results summary
```

### Results Format

```json
{
  "job_id": "abc12345",
  "output_files": [
    {
      "path": "/path/to/structure.pdb",
      "name": "cluster01_1.pdb",
      "size": 45210
    }
  ],
  "haddock_results": {
    "cluster_dir": "/path/to/clustfcc_output",
    "cluster_summary": "/path/to/clusters.txt",
    "final_models": [
      "/path/to/top_model_1.pdb",
      "/path/to/top_model_2.pdb"
    ]
  },
  "summary": {
    "total_clusters": 5,
    "top_cluster_size": 15,
    "best_haddock_score": -45.2
  }
}
```

---

## Performance Characteristics

| Operation | Typical Runtime | Memory Usage | CPU Scaling | Recommended Cores |
|-----------|----------------|--------------|-------------|-------------------|
| Protein-Peptide Docking | 1-4 hours | 1-4 GB | Linear | 4-8 cores |
| Cyclisation | 30-90 minutes | 0.5-2 GB | Linear | 4 cores |
| Information-Driven | 1-6 hours | 1-6 GB | Linear | 4-8 cores |
| Batch (per job) | As above | As above | Parallel | 8+ cores |

### Resource Requirements

**Minimum System:**
- 4 CPU cores
- 4 GB RAM
- 10 GB disk space per job
- HADDOCK3 conda environment

**Recommended System:**
- 8+ CPU cores
- 8+ GB RAM
- Fast SSD storage
- Dedicated HADDOCK3 environment with all dependencies

---

## Error Handling and Recovery

### Common Error Scenarios

| Error Type | Cause | Recovery |
|------------|-------|----------|
| File Not Found | Missing input PDB files | Check file paths and permissions |
| HADDOCK3 Environment | Missing or misconfigured HADDOCK3 | Use `validate_haddock_environment()` |
| Insufficient Resources | Out of memory/disk space | Monitor system resources |
| Job Timeout | Very long calculations | Increase timeout in config |
| Restraint Errors | Invalid restraint format | Check residue numbering |

### Job Recovery

Jobs are persistent and survive server restarts:

```python
# After server restart, jobs can still be queried
old_jobs = list_jobs()
for job in old_jobs["jobs"]:
    if job["status"] == "running":
        # Job may have completed during downtime
        current_status = get_job_status(job["job_id"])
```

---

## Workflow Examples

### 1. Simple Protein-Peptide Docking

```python
# Submit docking job
result = submit_protein_peptide_docking(
    protein_file="target.pdb",
    peptide_file="ligand.pdb",
    job_name="simple_dock"
)
job_id = result["job_id"]

# Monitor until completion
import time
while True:
    status = get_job_status(job_id)
    print(f"Status: {status['status']}")

    if status["status"] == "completed":
        final_result = get_job_result(job_id)
        print("✅ Docking completed!")
        print(f"Results in: {final_result['result']['output_files']}")
        break
    elif status["status"] == "failed":
        error_log = get_job_log(job_id)
        print(f"❌ Job failed: {status.get('error')}")
        break

    time.sleep(60)  # Check every minute
```

### 2. Information-Driven Docking Workflow

```python
# Step 1: Submit with experimental data
result = submit_information_driven_docking(
    protein_file="protein.pdb",
    peptide_file="peptide.pdb",
    active_protein_residues="36,109,113",  # From NMR/mutagenesis
    active_peptide_residues="1,5,8",       # Key binding residues
    passive_protein_residues="35,37,108,110",  # Neighbors
    job_name="nmr_guided_dock"
)

print(f"Submitted job: {result['job_id']}")

# Step 2: Monitor with detailed logging
job_id = result["job_id"]
while get_job_status(job_id)["status"] in ["pending", "running"]:
    # Check progress every 5 minutes
    log_tail = get_job_log(job_id, tail=10)
    print("Recent log lines:")
    for line in log_tail["log_lines"][-3:]:
        print(f"  {line.strip()}")

    time.sleep(300)

# Step 3: Analyze results
final_result = get_job_result(job_id)
if final_result["status"] == "success":
    models = final_result["result"]["haddock_results"]["final_models"]
    print(f"Generated {len(models)} final models")
```

### 3. Batch Screening Workflow

```python
# Prepare peptide library
peptide_files = [f"library/peptide_{i:03d}.pdb" for i in range(1, 101)]

# Submit batch job
batch_result = submit_batch_protein_peptide_docking(
    protein_file="target_protein.pdb",
    peptide_files=peptide_files,
    job_name="peptide_screening"
)

job_ids = batch_result["job_ids"]
print(f"Submitted {len(job_ids)} docking jobs")

# Monitor batch progress
completed = 0
failed = 0

while completed + failed < len(job_ids):
    current_completed = 0
    current_failed = 0

    for job_id in job_ids:
        status = get_job_status(job_id)["status"]
        if status == "completed":
            current_completed += 1
        elif status == "failed":
            current_failed += 1

    if current_completed > completed or current_failed > failed:
        completed = current_completed
        failed = current_failed
        remaining = len(job_ids) - completed - failed

        print(f"Progress: {completed} completed, {failed} failed, {remaining} running")

    time.sleep(300)  # Check every 5 minutes

print("✅ Batch screening completed!")

# Collect results
successful_results = []
for job_id in job_ids:
    status = get_job_status(job_id)
    if status["status"] == "completed":
        result = get_job_result(job_id)
        successful_results.append({
            "job_id": job_id,
            "job_name": status["job_name"],
            "runtime": status.get("runtime_formatted"),
            "models": result["result"]["haddock_results"]["final_models"]
        })

print(f"Successfully completed: {len(successful_results)} out of {len(job_ids)} jobs")
```

---

## Installation and Setup

### 1. Dependencies

```bash
# Install MCP dependencies
pip install fastmcp loguru

# Ensure HADDOCK3 is available
# (Follow HADDOCK3 installation instructions)
```

### 2. Environment Setup

```bash
# Verify HADDOCK3 environment
validate_haddock_environment()

# Check example data
get_example_data_paths()
```

### 3. Server Startup

```bash
# Start MCP server
python src/server.py

# Or use FastMCP development mode
fastmcp dev src/server.py
```

### 4. Basic Test

```python
from src.server import get_server_info, job_manager

# Verify server
info = get_server_info()
print(f"Server: {info['server_name']} v{info['version']}")

# Verify job manager
jobs = job_manager.list_jobs()
print(f"Job system operational: {jobs['status'] == 'success'}")
```

---

## Success Criteria Assessment

- ✅ **MCP server created**: `src/server.py` with FastMCP integration
- ✅ **Job manager implemented**: Async operation support with persistence
- ✅ **Submit tools created**: All 3 HADDOCK3 scripts wrapped as submit tools
- ✅ **Batch processing support**: Multi-peptide docking capabilities
- ✅ **Job management tools**: Complete lifecycle management (status, result, log, cancel, list)
- ✅ **Clear tool descriptions**: Comprehensive docstrings for LLM usage
- ✅ **Error handling**: Structured error responses and recovery
- ✅ **Server starts successfully**: Validated import and initialization
- ✅ **Documentation provided**: Complete tool and workflow documentation

---

## Tool Classification Summary

| Original Script | API Type | Runtime | Batch Support | MCP Tool | Status |
|----------------|----------|---------|---------------|----------|---------|
| `protein_peptide_docking.py` | Submit | 1-4 hours | Yes | `submit_protein_peptide_docking` | ✅ |
| `cyclic_peptide_cyclisation.py` | Submit | 30-90 min | No | `submit_cyclic_peptide_cyclisation` | ✅ |
| `information_driven_docking.py` | Submit | 1-6 hours | No | `submit_information_driven_docking` | ✅ |

**Total Tools Created**: 12
- 5 Job Management Tools
- 3 HADDOCK3 Submit Tools
- 1 Batch Processing Tool
- 3 Utility Tools

---

## Next Steps

This MCP server is ready for production use with HADDOCK3 cyclic peptide workflows:

1. **Deploy** the server in a HADDOCK3-enabled environment
2. **Integrate** with LLM agents for automated molecular docking workflows
3. **Scale** using the batch processing capabilities for virtual screening
4. **Monitor** job performance and optimize resource allocation
5. **Extend** with additional HADDOCK3 protocols as needed

The server provides a complete interface for computational cyclic peptide research, enabling automated structure-based drug design workflows through the MCP protocol.