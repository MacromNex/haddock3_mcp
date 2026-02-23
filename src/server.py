"""MCP Server for HADDOCK3 Cyclic Peptide Tools

Provides submit (asynchronous) APIs for HADDOCK3 molecular docking and cyclisation tasks.
All operations are long-running (30 minutes to 6 hours) and use the job management system.
"""

from fastmcp import FastMCP
from pathlib import Path
from typing import Optional, List
import sys

# Setup paths
SCRIPT_DIR = Path(__file__).parent.resolve()
MCP_ROOT = SCRIPT_DIR.parent
SCRIPTS_DIR = MCP_ROOT / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))
sys.path.insert(0, str(SCRIPTS_DIR))

from jobs.manager import job_manager
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create MCP server
mcp = FastMCP("haddock3-cycpep")

# ==============================================================================
# Job Management Tools (for async operations)
# ==============================================================================

@mcp.tool()
def get_job_status(job_id: str) -> dict:
    """
    Get the status of a submitted HADDOCK3 computation job.

    Args:
        job_id: The job ID returned from a submit_* function

    Returns:
        Dictionary with job status, timestamps, runtime, and any errors
    """
    return job_manager.get_job_status(job_id)

@mcp.tool()
def get_job_result(job_id: str) -> dict:
    """
    Get the results of a completed HADDOCK3 computation job.

    Args:
        job_id: The job ID of a completed job

    Returns:
        Dictionary with the job results including HADDOCK3 output files,
        cluster results, final models, and analysis data
    """
    return job_manager.get_job_result(job_id)

@mcp.tool()
def get_job_log(job_id: str, tail: int = 50) -> dict:
    """
    Get log output from a running or completed HADDOCK3 job.

    Args:
        job_id: The job ID to get logs for
        tail: Number of lines from end (default: 50, use 0 for all)

    Returns:
        Dictionary with log lines and total line count
    """
    return job_manager.get_job_log(job_id, tail)

@mcp.tool()
def cancel_job(job_id: str) -> dict:
    """
    Cancel a running HADDOCK3 computation job.

    Args:
        job_id: The job ID to cancel

    Returns:
        Success or error message
    """
    return job_manager.cancel_job(job_id)

@mcp.tool()
def list_jobs(status: Optional[str] = None) -> dict:
    """
    List all submitted HADDOCK3 computation jobs.

    Args:
        status: Filter by status (pending, running, completed, failed, cancelled)

    Returns:
        List of jobs with their status, runtime, and script information
    """
    return job_manager.list_jobs(status)

# ==============================================================================
# HADDOCK3 Submit Tools (for long-running operations > 30 min)
# ==============================================================================

@mcp.tool()
def submit_protein_peptide_docking(
    protein_file: str,
    peptide_file: str,
    output_dir: Optional[str] = None,
    restraints_file: Optional[str] = None,
    job_name: Optional[str] = None
) -> dict:
    """
    Submit a protein-peptide docking job using HADDOCK3.

    This task typically takes 1-4 hours. Use get_job_status() to monitor
    progress and get_job_result() to retrieve results when completed.

    Args:
        protein_file: Path to protein PDB structure file
        peptide_file: Path to peptide PDB structure file (can contain multiple conformations)
        output_dir: Optional output directory (created if not specified)
        restraints_file: Optional ambiguous restraints file (.tbl format)
        job_name: Optional name for the job (for easier tracking)

    Returns:
        Dictionary with job_id for tracking. Use:
        - get_job_status(job_id) to check progress
        - get_job_result(job_id) to get results when completed
        - get_job_log(job_id) to see execution logs
    """
    script_path = str(SCRIPTS_DIR / "protein_peptide_docking.py")

    # Validate input files
    if not Path(protein_file).exists():
        return {"status": "error", "error": f"Protein file not found: {protein_file}"}
    if not Path(peptide_file).exists():
        return {"status": "error", "error": f"Peptide file not found: {peptide_file}"}
    if restraints_file and not Path(restraints_file).exists():
        return {"status": "error", "error": f"Restraints file not found: {restraints_file}"}

    return job_manager.submit_job(
        script_path=script_path,
        args={
            "input_protein": protein_file,
            "input_peptide": peptide_file,
            "output_dir": output_dir,
            "restraints_file": restraints_file
        },
        job_name=job_name or f"protein_peptide_docking_{Path(peptide_file).stem}"
    )

@mcp.tool()
def submit_cyclic_peptide_cyclisation(
    peptide_file: str,
    peptide_length: Optional[int] = None,
    output_dir: Optional[str] = None,
    job_name: Optional[str] = None
) -> dict:
    """
    Submit a cyclic peptide cyclisation job using HADDOCK3.

    This task typically takes 30-90 minutes. Cyclises linear peptides
    into cyclic forms using distance restraints and specialized protocols.

    Args:
        peptide_file: Path to linear peptide PDB structure file
        peptide_length: Length of peptide in residues (auto-detected if not provided)
        output_dir: Optional output directory (created if not specified)
        job_name: Optional name for the job

    Returns:
        Dictionary with job_id for tracking
    """
    script_path = str(SCRIPTS_DIR / "cyclic_peptide_cyclisation.py")

    # Validate input file
    if not Path(peptide_file).exists():
        return {"status": "error", "error": f"Peptide file not found: {peptide_file}"}

    return job_manager.submit_job(
        script_path=script_path,
        args={
            "input": peptide_file,
            "peptide_length": peptide_length,
            "output_dir": output_dir
        },
        job_name=job_name or f"cyclisation_{Path(peptide_file).stem}"
    )

@mcp.tool()
def submit_information_driven_docking(
    protein_file: str,
    peptide_file: str,
    active_protein_residues: Optional[str] = None,
    active_peptide_residues: Optional[str] = None,
    passive_protein_residues: Optional[str] = None,
    passive_peptide_residues: Optional[str] = None,
    output_dir: Optional[str] = None,
    job_name: Optional[str] = None
) -> dict:
    """
    Submit an information-driven docking job using experimental restraints.

    This task typically takes 1-6 hours. Uses experimental data to guide
    the docking process with active and passive residues.

    Args:
        protein_file: Path to protein PDB structure file
        peptide_file: Path to peptide PDB structure file
        active_protein_residues: Comma-separated protein residues with strong experimental evidence (e.g., "36,109,113")
        active_peptide_residues: Comma-separated peptide residues with strong experimental evidence (e.g., "1,5,8")
        passive_protein_residues: Comma-separated protein residues with weak evidence or neighbors
        passive_peptide_residues: Comma-separated peptide residues with weak evidence or neighbors
        output_dir: Optional output directory (created if not specified)
        job_name: Optional name for the job

    Returns:
        Dictionary with job_id for tracking
    """
    script_path = str(SCRIPTS_DIR / "information_driven_docking.py")

    # Validate input files
    if not Path(protein_file).exists():
        return {"status": "error", "error": f"Protein file not found: {protein_file}"}
    if not Path(peptide_file).exists():
        return {"status": "error", "error": f"Peptide file not found: {peptide_file}"}

    # Validate that at least some restraint information is provided
    if not any([active_protein_residues, active_peptide_residues,
                passive_protein_residues, passive_peptide_residues]):
        return {
            "status": "error",
            "error": "At least one set of restraint residues must be provided for information-driven docking"
        }

    return job_manager.submit_job(
        script_path=script_path,
        args={
            "input_protein": protein_file,
            "input_peptide": peptide_file,
            "active_protein_residues": active_protein_residues,
            "active_peptide_residues": active_peptide_residues,
            "passive_protein_residues": passive_protein_residues,
            "passive_peptide_residues": passive_peptide_residues,
            "output_dir": output_dir
        },
        job_name=job_name or f"info_docking_{Path(peptide_file).stem}"
    )

# ==============================================================================
# Batch Processing Tools
# ==============================================================================

@mcp.tool()
def submit_batch_protein_peptide_docking(
    protein_file: str,
    peptide_files: List[str],
    restraints_file: Optional[str] = None,
    output_base_dir: Optional[str] = None,
    job_name: Optional[str] = None
) -> dict:
    """
    Submit multiple protein-peptide docking jobs in batch.

    Processes multiple peptide structures against the same protein.
    Each peptide gets its own separate job for parallel processing.

    Args:
        protein_file: Path to protein PDB structure file
        peptide_files: List of paths to peptide PDB structure files
        restraints_file: Optional restraints file to use for all dockings
        output_base_dir: Base directory for outputs (subdirs created per peptide)
        job_name: Optional base name for the batch jobs

    Returns:
        Dictionary with list of submitted job_ids
    """
    if not Path(protein_file).exists():
        return {"status": "error", "error": f"Protein file not found: {protein_file}"}

    job_ids = []
    errors = []

    for i, peptide_file in enumerate(peptide_files):
        if not Path(peptide_file).exists():
            errors.append(f"Peptide file not found: {peptide_file}")
            continue

        # Create output directory for this peptide
        peptide_name = Path(peptide_file).stem
        if output_base_dir:
            output_dir = Path(output_base_dir) / f"docking_{peptide_name}"
        else:
            output_dir = None

        # Submit individual job
        result = submit_protein_peptide_docking(
            protein_file=protein_file,
            peptide_file=peptide_file,
            output_dir=str(output_dir) if output_dir else None,
            restraints_file=restraints_file,
            job_name=f"{job_name or 'batch'}_{i+1}_{peptide_name}"
        )

        if result.get("status") == "submitted":
            job_ids.append(result["job_id"])
        else:
            errors.append(f"Failed to submit {peptide_file}: {result.get('error', 'Unknown error')}")

    return {
        "status": "submitted" if job_ids else "error",
        "job_ids": job_ids,
        "total_submitted": len(job_ids),
        "total_failed": len(errors),
        "errors": errors if errors else None,
        "message": f"Submitted {len(job_ids)} docking jobs. Use list_jobs() to monitor all jobs."
    }

# ==============================================================================
# Utility Tools
# ==============================================================================

@mcp.tool()
def validate_haddock_environment() -> dict:
    """
    Validate that HADDOCK3 environment is properly configured.

    Checks for HADDOCK3 installation, conda environment, and dependencies.

    Returns:
        Dictionary with validation results and environment information
    """
    try:
        from scripts.lib.haddock import find_haddock_env
        # Try to find HADDOCK environment
        env_info = find_haddock_env()
        return {
            "status": "success",
            "haddock3_available": True,
            "environment_info": env_info,
            "message": "HADDOCK3 environment is properly configured"
        }
    except ImportError:
        return {
            "status": "warning",
            "haddock3_available": False,
            "error": "HADDOCK3 library modules not found in scripts/lib/",
            "message": "HADDOCK3 environment validation requires HADDOCK3 installation"
        }
    except Exception as e:
        return {
            "status": "error",
            "haddock3_available": False,
            "error": str(e),
            "message": "HADDOCK3 environment not found or misconfigured"
        }

@mcp.tool()
def get_example_data_paths() -> dict:
    """
    Get paths to example data files for testing HADDOCK3 tools.

    Returns:
        Dictionary with paths to example protein and peptide structures
    """
    examples_dir = MCP_ROOT / "examples" / "data" / "structures"

    example_files = {
        "protein_structures": [],
        "peptide_structures": [],
        "other_files": []
    }

    if examples_dir.exists():
        for file_path in examples_dir.glob("*.pdb"):
            if "protein" in file_path.name.lower():
                example_files["protein_structures"].append(str(file_path))
            elif "peptide" in file_path.name.lower() or any(x in file_path.name for x in ["sfi", "DAID"]):
                example_files["peptide_structures"].append(str(file_path))
            else:
                example_files["other_files"].append(str(file_path))

    return {
        "status": "success",
        "examples_directory": str(examples_dir),
        "available_files": example_files,
        "total_files": sum(len(files) for files in example_files.values())
    }

@mcp.tool()
def get_server_info() -> dict:
    """
    Get information about the HADDOCK3 MCP server and available tools.

    Returns:
        Dictionary with server capabilities and tool descriptions
    """
    return {
        "server_name": "haddock3-cycpep",
        "version": "1.0.0",
        "description": "MCP server for HADDOCK3 cyclic peptide molecular docking and cyclisation",
        "available_tools": {
            "job_management": [
                "get_job_status", "get_job_result", "get_job_log",
                "cancel_job", "list_jobs"
            ],
            "docking_tools": [
                "submit_protein_peptide_docking",
                "submit_cyclic_peptide_cyclisation",
                "submit_information_driven_docking"
            ],
            "batch_tools": [
                "submit_batch_protein_peptide_docking"
            ],
            "utility_tools": [
                "validate_haddock_environment",
                "get_example_data_paths",
                "get_server_info"
            ]
        },
        "typical_runtimes": {
            "protein_peptide_docking": "1-4 hours",
            "cyclic_peptide_cyclisation": "30-90 minutes",
            "information_driven_docking": "1-6 hours"
        },
        "requirements": {
            "haddock3": "Required for all docking operations",
            "conda_environment": "./env or detected HADDOCK3 environment",
            "minimum_cores": 4,
            "recommended_memory": "8 GB RAM"
        }
    }

# ==============================================================================
# Entry Point
# ==============================================================================

if __name__ == "__main__":
    mcp.run()