#!/usr/bin/env python3
"""
Script: cyclic_peptide_cyclisation.py
Description: Cyclise linear peptides into cyclic peptides using HADDOCK3's specialized protocol

Original Use Case: examples/use_case_2_cyclic_peptide_cyclisation.py
Dependencies Removed: None (was already minimal)

Usage:
    python scripts/cyclic_peptide_cyclisation.py --input <peptide.pdb> --length <num_residues> --output <output_dir>

Example:
    python scripts/cyclic_peptide_cyclisation.py --input examples/data/structures/1sfi_peptide-ensemble.pdb --length 14 --output results/cyclisation_result
"""

# ==============================================================================
# Minimal Imports (only essential packages)
# ==============================================================================
import argparse
import subprocess
import sys
from pathlib import Path
import tempfile
from typing import Union, Optional, Dict, Any, List, Tuple
import json

# ==============================================================================
# Configuration (extracted from use case)
# ==============================================================================
DEFAULT_CONFIG = {
    "ncores": 4,
    "timeout": 3600,  # 1 hour
    "tolerance": 5,
    "sampling_factor": 10,
    "tadfactor": 4,
    "md_steps": {
        "rigid": 2000,
        "cool1": 2000,
        "cool2": 4000,
        "cool3": 4000
    },
    "clustering": {
        "n_clusters": 50,
        "min_population": 1,
        "top_clusters": 50,
        "top_models": 1
    },
    "cyclisation": {
        "distance": 3.5,
        "disulphide_distance": 4.0
    },
    "water_steps": 5000
}

# ==============================================================================
# Inlined Utility Functions (simplified from use case)
# ==============================================================================
def create_distance_restraints(peptide_length: int, output_file: Path) -> None:
    """
    Create distance restraints to bring N and C termini together for cyclisation.
    Simplified from examples/use_case_2_cyclic_peptide_cyclisation.py
    """
    restraints = f"""!
! Distance restraints for peptide cyclisation
! These restraints bring the N and C termini together
!
! N-terminus (residue 1) to C-terminus (residue {peptide_length})
assign (segid B and resid 1 and name N) (segid B and resid {peptide_length} and name C) 1.4 0.2 0.2
assign (segid B and resid 1 and name CA) (segid B and resid {peptide_length} and name CA) 2.5 0.5 0.5
assign (segid B and resid 1 and name CB) (segid B and resid {peptide_length} and name CB) 3.5 1.0 1.0
"""
    with open(output_file, 'w') as f:
        f.write(restraints)

def create_cyclisation_config(peptide_pdb: str, peptide_length: int, output_dir: str,
                             config: Dict[str, Any]) -> str:
    """
    Create a HADDOCK3 configuration file for peptide cyclisation.
    Simplified from examples/use_case_2_cyclic_peptide_cyclisation.py
    """
    ncores = config.get("ncores", 4)
    tolerance = config.get("tolerance", 5)
    sampling_factor = config.get("sampling_factor", 10)
    tadfactor = config.get("tadfactor", 4)
    md = config.get("md_steps", {})
    cluster = config.get("clustering", {})
    cyclic = config.get("cyclisation", {})
    water_steps = config.get("water_steps", 5000)

    return f"""# ==================================================
#      Peptide cyclisation protocol with HADDOCK3
#
#  This example workflow will take a peptide
#  and generate cyclised conformations in a two step
#  process, first using distance restraints to bring the
#  termini together, then rebuilding the topology to
#  create the covalent cyclic bond and refining again.
#
#  Protocol described in: https://doi.org/10.1021/acs.jctc.2c00075
# ==================================================

run_dir = "{output_dir}"

# execution mode
mode = "local"
ncores = {ncores}
debug = false
concat = 1

# input peptide structure
molecules = [
    "{peptide_pdb}",
    ]

# ==================================================

# Generate initial topology
[topoaa]

# First refinement: bring termini together using distance restraints
[flexref]
unambig_fname = "cyclisation_restraints.tbl"
tolerance = {tolerance}
sampling_factor = {sampling_factor}
tadfactor = {tadfactor}
mdsteps_rigid = {md.get("rigid", 2000)}
mdsteps_cool1 = {md.get("cool1", 2000)}
mdsteps_cool2 = {md.get("cool2", 4000)}
mdsteps_cool3 = {md.get("cool3", 4000)}
# Give full flexibility to the peptide
nfle = 1
fle_sta_1 = 1
fle_end_1 = {peptide_length}
fle_seg_1 = "B"
# Turn off electrostatic for initial cyclisation
elecflag = false

# MD refinement to relax the structure
[mdref]
unambig_fname = "cyclisation_restraints.tbl"
# Keep peptide fully flexible
nfle = 1
fle_sta_1 = 1
fle_end_1 = {peptide_length}
fle_seg_1 = "B"

# Evaluate intermediate structures
[caprieval]

# Calculate RMSD matrix for clustering
[rmsdmatrix]

# Cluster based on RMSD
[clustrmsd]
criterion = "maxclust"  # Use maximum number of clusters
n_clusters = {cluster.get("n_clusters", 50)}  # Number of desired clusters
min_population = {cluster.get("min_population", 1)}  # Include singletons
plot_matrix = true  # Plot the RMSD matrix

# Select top clusters
[seletopclusts]
top_clusters = {cluster.get("top_clusters", 50)}
top_models = {cluster.get("top_models", 1)}

# Evaluate clustered structures
[caprieval]

# SECOND STAGE: Create actual covalent bond and refine
# Rebuild topology with cyclic bond
[topoaa]
cyclicpept_dist = {cyclic.get("distance", 3.5)}
disulphide_dist = {cyclic.get("disulphide_distance", 4.0)}
[topoaa.mol1]
cyclicpept = true

# Scoring to accept new topology
[emscoring]
# Required to make the next module accept the new PDB files
# after calling topoaa a second time

# Final flexible refinement with covalent bond
[flexref]
unambig_fname = "cyclisation_restraints.tbl"
tolerance = {tolerance}
sampling_factor = 1
tadfactor = {tadfactor}
mdsteps_rigid = {md.get("rigid", 2000)}
mdsteps_cool1 = {md.get("cool1", 2000)}
mdsteps_cool2 = {md.get("cool2", 4000)}
mdsteps_cool3 = {md.get("cool3", 4000)}
# Keep peptide fully flexible
nfle = 1
fle_sta_1 = 1
fle_end_1 = {peptide_length}
fle_seg_1 = "B"
# Turn off electrostatic for final refinement
elecflag = false

# Final MD refinement in explicit water
[mdref]
watersteps = {water_steps}
# Keep peptide fully flexible
nfle = 1
fle_sta_1 = 1
fle_end_1 = {peptide_length}
fle_seg_1 = "B"

# Final evaluation
[caprieval]

# Final clustering
[rmsdmatrix]

[clustrmsd]
criterion = "maxclust"  # Use maximum number of clusters
n_clusters = {cluster.get("n_clusters", 50)}  # Number of desired clusters
min_population = {cluster.get("min_population", 1)}  # Include singletons
plot_matrix = true  # Plot the RMSD matrix

# Select final top models
[seletopclusts]
top_clusters = {cluster.get("top_clusters", 50)}
top_models = {cluster.get("top_models", 1)}

# Final evaluation
[caprieval]

# ==================================================
"""

def get_peptide_length_from_pdb(pdb_file: Path) -> int:
    """Extract peptide length from PDB file by counting residues."""
    try:
        residue_numbers = set()
        with open(pdb_file, 'r') as f:
            for line in f:
                if line.startswith(('ATOM', 'HETATM')):
                    # Extract residue number (columns 23-26)
                    try:
                        res_num = int(line[22:26].strip())
                        residue_numbers.add(res_num)
                    except ValueError:
                        continue

        if residue_numbers:
            return max(residue_numbers)
        else:
            raise ValueError("No valid residues found in PDB file")
    except Exception as e:
        raise ValueError(f"Error reading PDB file {pdb_file}: {e}")

def validate_input_file(file_path: Path, file_type: str) -> bool:
    """Validate that input file exists and has correct format."""
    if not file_path.exists():
        raise FileNotFoundError(f"{file_type} file not found: {file_path}")

    if file_type == "pdb" and not file_path.suffix.lower() == ".pdb":
        raise ValueError(f"Expected PDB file, got: {file_path.suffix}")

    return True

def run_haddock3(config_file: Path, work_dir: Path, timeout: int = 3600) -> Tuple[bool, Optional[Path]]:
    """Execute HADDOCK3 with the given configuration. Simplified from use case."""
    try:
        print(f"Running HADDOCK3 with configuration: {config_file}")
        print("This may take several minutes to hours depending on the system size...")

        # Find environment path
        env_path = Path.cwd() / "env"
        if not env_path.exists():
            # Try relative to script
            env_path = Path(__file__).parent.parent / "env"

        # Run HADDOCK3
        result = subprocess.run([
            "mamba", "run", "-p", str(env_path),
            "haddock3", str(config_file)
        ],
        cwd=work_dir,
        capture_output=True,
        text=True,
        timeout=timeout
        )

        if result.returncode == 0:
            print("HADDOCK3 completed successfully!")
            # Find the output directory
            run_dirs = [d for d in work_dir.iterdir() if d.is_dir() and d.name.startswith("run")]
            if run_dirs:
                output_dir = run_dirs[0]  # Take the first run directory
                print(f"Results available in: {output_dir}")
                return True, output_dir
        else:
            print("HADDOCK3 failed!")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False, None

    except subprocess.TimeoutExpired:
        print(f"HADDOCK3 timed out after {timeout} seconds")
        return False, None
    except Exception as e:
        print(f"Error running HADDOCK3: {e}")
        return False, None

# ==============================================================================
# Core Function (main logic extracted from use case)
# ==============================================================================
def run_cyclic_peptide_cyclisation(
    peptide_file: Union[str, Path],
    peptide_length: Optional[int] = None,
    output_dir: Optional[Union[str, Path]] = None,
    config: Optional[Dict[str, Any]] = None,
    work_dir: Optional[Union[str, Path]] = None,
    dry_run: bool = False,
    **kwargs
) -> Dict[str, Any]:
    """
    Main function for cyclic peptide cyclisation using HADDOCK3.

    Args:
        peptide_file: Path to peptide PDB file (linear peptide)
        peptide_length: Length of peptide in residues (auto-detected if None)
        output_dir: Output directory name for results
        config: Configuration dict (uses DEFAULT_CONFIG if not provided)
        work_dir: Working directory for HADDOCK3 (default: ./cyclisation_work)
        dry_run: Only create configuration file, don't run HADDOCK3
        **kwargs: Override specific config parameters

    Returns:
        Dict containing:
            - success: Whether cyclisation completed successfully
            - output_dir: Path to output directory (if successful)
            - config_file: Path to configuration file
            - restraints_file: Path to distance restraints file
            - work_dir: Working directory used
            - peptide_length: Length of peptide used
            - metadata: Execution metadata

    Example:
        >>> result = run_cyclic_peptide_cyclisation("linear_peptide.pdb", peptide_length=14)
        >>> print(result['output_dir'])
    """
    # Setup
    peptide_file = Path(peptide_file)
    config = {**DEFAULT_CONFIG, **(config or {}), **kwargs}

    if output_dir is None:
        output_dir = "cyclic_peptide_cyclisation"

    if work_dir is None:
        work_dir = Path("./cyclisation_work")
    else:
        work_dir = Path(work_dir)

    # Validate inputs
    validate_input_file(peptide_file, "peptide")

    # Auto-detect peptide length if not provided
    if peptide_length is None:
        peptide_length = get_peptide_length_from_pdb(peptide_file)
        print(f"Auto-detected peptide length: {peptide_length} residues")

    # Create working directory
    work_dir.mkdir(exist_ok=True)

    # Create distance restraints file
    restraints_file = work_dir / "cyclisation_restraints.tbl"
    create_distance_restraints(peptide_length, restraints_file)

    # Generate configuration file
    config_content = create_cyclisation_config(
        peptide_pdb=str(peptide_file.resolve()),
        peptide_length=peptide_length,
        output_dir=output_dir,
        config=config
    )

    config_file = work_dir / "cyclisation_config.cfg"
    with open(config_file, 'w') as f:
        f.write(config_content)

    result = {
        "success": False,
        "output_dir": None,
        "config_file": str(config_file),
        "restraints_file": str(restraints_file),
        "work_dir": str(work_dir),
        "peptide_length": peptide_length,
        "metadata": {
            "peptide_file": str(peptide_file),
            "config": config,
            "dry_run": dry_run
        }
    }

    print(f"Configuration file created: {config_file}")
    print(f"Distance restraints created: {restraints_file}")

    if dry_run:
        print("Dry run completed. Configuration files ready.")
        result["success"] = True
        return result

    # Run HADDOCK3
    success, output_path = run_haddock3(config_file, work_dir, config.get("timeout", 3600))

    result["success"] = success
    if success and output_path:
        result["output_dir"] = str(output_path)

    return result

# ==============================================================================
# CLI Interface
# ==============================================================================
def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--input', '-i', required=True,
                       help='Input peptide PDB file path (linear peptide)')
    parser.add_argument('--length', '-l', type=int,
                       help='Length of peptide in residues (auto-detected if not provided)')
    parser.add_argument('--output', '-o', default="cyclic_peptide_cyclisation",
                       help='Output directory name')
    parser.add_argument('--config', '-c',
                       help='Config file (JSON)')
    parser.add_argument('--work-dir', '-w', default="./cyclisation_work",
                       help='Working directory for HADDOCK3')
    parser.add_argument('--ncores', type=int,
                       help='Number of CPU cores to use')
    parser.add_argument('--dry-run', action="store_true",
                       help='Only create configuration file, dont run HADDOCK3')

    args = parser.parse_args()

    # Load config if provided
    config = None
    if args.config:
        with open(args.config) as f:
            config = json.load(f)

    # Override config with CLI arguments
    cli_overrides = {}
    if args.ncores:
        cli_overrides["ncores"] = args.ncores

    # Run
    try:
        result = run_cyclic_peptide_cyclisation(
            peptide_file=args.input,
            peptide_length=args.length,
            output_dir=args.output,
            config=config,
            work_dir=args.work_dir,
            dry_run=args.dry_run,
            **cli_overrides
        )

        if result["success"]:
            if args.dry_run:
                print("✅ Configuration created successfully")
                print(f"Config file: {result['config_file']}")
                print(f"Restraints file: {result['restraints_file']}")
                print(f"Peptide length: {result['peptide_length']} residues")
            else:
                print("🎉 Cyclic peptide cyclisation completed successfully!")
                print(f"Results are in: {result['output_dir']}")
                print(f"Peptide length: {result['peptide_length']} residues")
        else:
            print("❌ Cyclisation failed. Check the configuration and input files.")
            return 1

        return 0

    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == '__main__':
    main()