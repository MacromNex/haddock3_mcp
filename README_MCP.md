# HADDOCK3 Cyclic Peptide MCP Server

A Model Context Protocol (MCP) server providing asynchronous APIs for HADDOCK3 molecular docking and cyclisation operations specifically designed for cyclic peptides.

## 🚀 Quick Start

```bash
# Install dependencies
pip install fastmcp loguru

# Start the MCP server
python src/server.py

# Or use development mode
fastmcp dev src/server.py
```

## 📋 Overview

This MCP server wraps HADDOCK3's cyclic peptide tools into a job-based API system, enabling:

- **Protein-Peptide Docking** (1-4 hours)
- **Cyclic Peptide Cyclisation** (30-90 minutes)
- **Information-Driven Docking** (1-6 hours)
- **Batch Processing** for virtual screening
- **Real-time Job Tracking** with logs and progress
- **Persistent Job Storage** surviving server restarts

## 🛠 Available Tools

### Job Management
- `get_job_status(job_id)` - Check progress and runtime
- `get_job_result(job_id)` - Retrieve completed results
- `get_job_log(job_id, tail=50)` - View execution logs
- `cancel_job(job_id)` - Cancel running jobs
- `list_jobs(status=None)` - List all jobs

### HADDOCK3 Operations
- `submit_protein_peptide_docking()` - Dock peptides to proteins
- `submit_cyclic_peptide_cyclisation()` - Cyclise linear peptides
- `submit_information_driven_docking()` - Use experimental restraints
- `submit_batch_protein_peptide_docking()` - Process multiple peptides

### Utilities
- `validate_haddock_environment()` - Check HADDOCK3 setup
- `get_example_data_paths()` - Find test data
- `get_server_info()` - Server capabilities

## 📖 Usage Examples

### Simple Protein-Peptide Docking

```python
# Submit a docking job
result = submit_protein_peptide_docking(
    protein_file="protein.pdb",
    peptide_file="cyclic_peptide.pdb",
    job_name="my_docking"
)

job_id = result["job_id"]

# Monitor progress
while True:
    status = get_job_status(job_id)

    if status["status"] == "completed":
        # Get final results
        result = get_job_result(job_id)
        print("✅ Docking completed!")
        break
    elif status["status"] == "failed":
        # Check error logs
        log = get_job_log(job_id)
        print("❌ Job failed")
        break

    time.sleep(60)  # Check every minute
```

### Information-Driven Docking

```python
# Use experimental data to guide docking
result = submit_information_driven_docking(
    protein_file="target.pdb",
    peptide_file="ligand.pdb",
    active_protein_residues="36,109,113",  # Strong evidence
    active_peptide_residues="1,5,8",       # Key binding sites
    passive_protein_residues="35,37,110",  # Weak evidence
    job_name="nmr_guided_docking"
)

print(f"Job submitted: {result['job_id']}")
```

### Batch Virtual Screening

```python
# Screen multiple peptides against one target
peptides = ["peptide1.pdb", "peptide2.pdb", "peptide3.pdb"]

result = submit_batch_protein_peptide_docking(
    protein_file="target.pdb",
    peptide_files=peptides,
    job_name="virtual_screen"
)

# Monitor all jobs
for job_id in result["job_ids"]:
    status = get_job_status(job_id)
    print(f"Job {job_id}: {status['status']}")
```

## 🏗 Architecture

```
src/
├── server.py              # Main MCP server with FastMCP
├── jobs/
│   └── manager.py         # Job queue and lifecycle management
└── tools/                 # Tool implementations

jobs/                      # Persistent job storage
├── {job_id}/
│   ├── metadata.json     # Job status and info
│   ├── job.log          # Execution log
│   ├── output/          # HADDOCK3 results
│   └── work/            # Working directory

scripts/                   # Original HADDOCK3 scripts
├── protein_peptide_docking.py
├── cyclic_peptide_cyclisation.py
├── information_driven_docking.py
└── lib/                  # Shared utilities
```

## 📁 Output Structure

Each job creates a structured output directory:

```
jobs/{job_id}/
├── metadata.json          # Job metadata and status
├── job.log               # Complete execution log
├── results.json          # Parsed results summary
├── output/               # HADDOCK3 output files
│   ├── config.cfg       # Configuration used
│   ├── restraints.tbl   # Restraints applied
│   └── structures/      # Final structures
└── work/                # HADDOCK3 working directory
    ├── clustfcc*/       # Clustering analysis
    └── {modules}/       # Individual module outputs
```

## ⚙ Configuration

### System Requirements

**Minimum:**
- 4 CPU cores, 4 GB RAM
- HADDOCK3 conda environment
- Python 3.8+ with fastmcp, loguru

**Recommended:**
- 8+ CPU cores, 8+ GB RAM
- Fast SSD storage
- Dedicated compute environment

### HADDOCK3 Setup

This server requires a working HADDOCK3 installation. The scripts will attempt to:

1. Find HADDOCK3 conda environment
2. Validate installation
3. Execute with proper environment activation

Use `validate_haddock_environment()` to check setup.

### Example Data

Place test structures in:
```
examples/data/structures/
├── protein.pdb          # Target protein
├── peptide.pdb          # Cyclic peptide ligand
└── restraints.tbl       # Optional restraints
```

## 🔧 Development

### Testing

```bash
# Test server startup
python src/server.py --help

# Test job manager
python -c "
from src.jobs.manager import job_manager
result = job_manager.list_jobs()
print(f'Job manager status: {result[\"status\"]}')
"

# Validate HADDOCK3 environment
python -c "
from src.server import validate_haddock_environment
result = validate_haddock_environment()
print(f'HADDOCK3 status: {result[\"haddock3_available\"]}')
"
```

### Adding New Tools

1. Create script in `scripts/` following existing patterns
2. Add submit tool in `src/server.py`:
```python
@mcp.tool()
def submit_new_tool(params) -> dict:
    script_path = str(SCRIPTS_DIR / "new_tool.py")
    return job_manager.submit_job(
        script_path=script_path,
        args=params,
        job_name=job_name
    )
```

## 📊 Performance

| Operation | Runtime | Memory | Cores | Output |
|-----------|---------|--------|-------|---------|
| Protein-Peptide Docking | 1-4 hours | 1-4 GB | 4-8 | Docked complexes |
| Cyclisation | 30-90 min | 0.5-2 GB | 4 | Cyclic structures |
| Info-Driven Docking | 1-6 hours | 1-6 GB | 4-8 | Restrained complexes |

Runtime scales with:
- Protein/peptide size
- Sampling parameters (higher = longer)
- Number of restraints
- Available CPU cores

## 📚 Documentation

- **[Step 6 Report](reports/step6_mcp_tools.md)** - Complete tool documentation
- **[Step 5 Report](reports/step5_scripts.md)** - Script extraction details
- **[Scripts README](scripts/README.md)** - Individual script documentation
- **[Config Documentation](configs/)** - HADDOCK3 configuration files

## 🤝 Integration

This MCP server is designed for integration with:

- **LLM Agents** for automated molecular docking workflows
- **Jupyter Notebooks** for interactive cyclic peptide research
- **Computational Pipelines** for high-throughput screening
- **Web Interfaces** through the MCP protocol

Example LLM integration:
```python
# LLM can automatically submit and monitor jobs
"Please dock this cyclic peptide to the target protein and analyze the results"

# → submit_protein_peptide_docking()
# → get_job_status() monitoring
# → get_job_result() when complete
# → Automated analysis and reporting
```

## ⚠ Important Notes

- **All operations are asynchronous** - use job management tools
- **Jobs persist across server restarts** - metadata is saved to disk
- **Resource monitoring recommended** - HADDOCK3 can be memory intensive
- **Backup job data** - results contain valuable computational outputs
- **HADDOCK3 license required** - ensure proper licensing for production use

## 🆘 Troubleshooting

| Issue | Cause | Solution |
|-------|-------|---------|
| "HADDOCK3 not found" | Missing environment | Install HADDOCK3, check PATH |
| Job stuck in "pending" | Resource constraints | Check system resources |
| "File not found" | Invalid paths | Verify input file locations |
| Import errors | Missing dependencies | `pip install fastmcp loguru` |

Check logs with `get_job_log(job_id)` for detailed error information.

---

**Built with**: [FastMCP](https://github.com/jlowin/fastmcp) • [HADDOCK3](https://github.com/haddocking/haddock3) • Python 3.8+

For detailed documentation see [`reports/step6_mcp_tools.md`](reports/step6_mcp_tools.md).