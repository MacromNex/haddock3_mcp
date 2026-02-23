#!/usr/bin/env python3
"""
Use Case 2: Cyclic Peptide Cyclisation Using HADDOCK3

This script demonstrates how to cyclise linear peptides into cyclic peptides
using HADDOCK3's specialized cyclisation protocol. This is particularly useful
for generating realistic cyclic peptide conformations from linear sequences.

Author: HADDOCK3 MCP Tool
Usage: python examples/use_case_2_cyclic_peptide_cyclisation.py [options]

Reference: https://doi.org/10.1021/acs.jctc.2c00075
"""

import argparse
import subprocess
import sys
from pathlib import Path
import shutil
import tempfile


def create_distance_restraints(peptide_length, output_file):
    """
    Create distance restraints to bring N and C termini together for cyclisation.

    Args:
        peptide_length (int): Length of the peptide
        output_file (str): Path to output restraints file
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


def create_cyclisation_config(peptide_pdb, peptide_length, output_dir, ncores=4):
    """
    Create a HADDOCK3 configuration file for peptide cyclisation.

    Args:
        peptide_pdb (str): Path to peptide PDB file
        peptide_length (int): Number of residues in the peptide
        output_dir (str): Output directory name
        ncores (int): Number of CPU cores to use

    Returns:
        str: Configuration file content
    """
    config = f"""# ==================================================
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
tolerance = 5
sampling_factor = 10
tadfactor = 4
mdsteps_rigid = 2000
mdsteps_cool1 = 2000
mdsteps_cool2 = 4000
mdsteps_cool3 = 4000
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
n_clusters = 50  # Number of desired clusters
min_population = 1  # Include singletons
plot_matrix = true  # Plot the RMSD matrix

# Select top clusters
[seletopclusts]
top_clusters = 50
top_models = 1

# Evaluate clustered structures
[caprieval]

# SECOND STAGE: Create actual covalent bond and refine
# Rebuild topology with cyclic bond
[topoaa]
cyclicpept_dist = 3.5
disulphide_dist = 4.0
[topoaa.mol1]
cyclicpept = true

# Scoring to accept new topology
[emscoring]
# Required to make the next module accept the new PDB files
# after calling topoaa a second time

# Final flexible refinement with covalent bond
[flexref]
unambig_fname = "cyclisation_restraints.tbl"
tolerance = 5
sampling_factor = 1
tadfactor = 4
mdsteps_rigid = 2000
mdsteps_cool1 = 2000
mdsteps_cool2 = 4000
mdsteps_cool3 = 4000
# Keep peptide fully flexible
nfle = 1
fle_sta_1 = 1
fle_end_1 = {peptide_length}
fle_seg_1 = "B"
# Turn off electrostatic for final refinement
elecflag = false

# Final MD refinement in explicit water
[mdref]
watersteps = 5000
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
n_clusters = 50  # Number of desired clusters
min_population = 1  # Include singletons
plot_matrix = true  # Plot the RMSD matrix

# Select final top models
[seletopclusts]
top_clusters = 50
top_models = 1

# Final evaluation
[caprieval]

# ==================================================
"""
    return config


def estimate_peptide_length(pdb_file):
    """
    Estimate the number of residues in a peptide PDB file.

    Args:
        pdb_file (str): Path to PDB file

    Returns:
        int: Number of residues
    """
    try:
        with open(pdb_file, 'r') as f:
            residues = set()
            for line in f:
                if line.startswith("ATOM") and line[12:16].strip() == "CA":
                    resnum = int(line[22:26].strip())
                    residues.add(resnum)
        return len(residues)
    except Exception:
        return 14  # Default for demo peptide


def run_haddock3(config_file, work_dir, peptide_length):
    """
    Execute HADDOCK3 cyclisation with the given configuration file.

    Args:
        config_file (str): Path to configuration file
        work_dir (str): Working directory
        peptide_length (int): Length of peptide for restraints

    Returns:
        tuple: (success, output_dir)
    """
    try:
        # Create restraints file in work directory
        restraints_file = Path(work_dir) / "cyclisation_restraints.tbl"
        create_distance_restraints(peptide_length, restraints_file)

        original_dir = Path.cwd()
        Path(work_dir).mkdir(exist_ok=True)

        print(f"Running HADDOCK3 cyclisation with configuration: {config_file}")
        print("This may take 30 minutes to several hours...")

        # Run HADDOCK3
        result = subprocess.run([
            "mamba", "run", "-p", str(original_dir / "env"),
            "haddock3", str(config_file)
        ],
        cwd=work_dir,
        capture_output=True,
        text=True,
        timeout=7200  # 2 hour timeout
        )

        if result.returncode == 0:
            print("HADDOCK3 cyclisation completed successfully!")
            # Find the output directory
            run_dirs = [d for d in Path(work_dir).iterdir() if d.is_dir() and d.name.startswith("run")]
            if run_dirs:
                output_dir = run_dirs[0]
                print(f"Cyclic peptide structures available in: {output_dir}")
                return True, output_dir
        else:
            print("HADDOCK3 cyclisation failed!")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False, None

    except subprocess.TimeoutExpired:
        print("HADDOCK3 timed out after 2 hours")
        return False, None
    except Exception as e:
        print(f"Error running HADDOCK3: {e}")
        return False, None


def main():
    parser = argparse.ArgumentParser(
        description="Cyclise linear peptides using HADDOCK3",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Basic usage with demo data
    python examples/use_case_2_cyclic_peptide_cyclisation.py

    # Custom peptide
    python examples/use_case_2_cyclic_peptide_cyclisation.py \\
        --peptide my_linear_peptide.pdb \\
        --length 12

    # High-throughput mode
    python examples/use_case_2_cyclic_peptide_cyclisation.py \\
        --peptide examples/data/1sfi_peptide-ensemble.pdb \\
        --ncores 20 \\
        --output cyclic_peptide_run

Note: This protocol creates backbone cyclic peptides. For disulfide-bridged
peptides, you may need additional restraints.
        """
    )

    parser.add_argument("--peptide",
                       default="examples/data/structures/1sfi_peptide-ensemble.pdb",
                       help="Path to linear peptide PDB file")

    parser.add_argument("--length", type=int,
                       help="Number of residues in peptide (auto-detected if not specified)")

    parser.add_argument("--output",
                       default="peptide_cyclisation",
                       help="Output directory name")

    parser.add_argument("--ncores", type=int, default=4,
                       help="Number of CPU cores to use")

    parser.add_argument("--work-dir",
                       default="./cyclisation_work",
                       help="Working directory for HADDOCK3")

    parser.add_argument("--dry-run", action="store_true",
                       help="Only create configuration file, don't run HADDOCK3")

    args = parser.parse_args()

    # Check if input file exists
    peptide_path = Path(args.peptide)
    if not peptide_path.exists():
        print(f"Error: Peptide file not found: {peptide_path}")
        print("Use --peptide to specify a different file or run with demo data")
        return 1

    # Determine peptide length
    peptide_length = args.length if args.length else estimate_peptide_length(peptide_path)
    print(f"Peptide length: {peptide_length} residues")

    # Create working directory
    work_dir = Path(args.work_dir)
    work_dir.mkdir(exist_ok=True)

    # Generate configuration file
    config_content = create_cyclisation_config(
        peptide_pdb=str(peptide_path.resolve()),
        peptide_length=peptide_length,
        output_dir=args.output,
        ncores=args.ncores
    )

    config_file = work_dir / "cyclisation_config.cfg"
    with open(config_file, 'w') as f:
        f.write(config_content)

    print(f"Configuration file created: {config_file}")

    if args.dry_run:
        print("Dry run completed. Configuration file ready.")
        print(f"To run manually: mamba activate ./env && cd {work_dir} && haddock3 {config_file.name}")
        return 0

    # Run HADDOCK3
    success, output_dir = run_haddock3(config_file, work_dir, peptide_length)

    if success:
        print(f"\\n🎉 Peptide cyclisation completed successfully!")
        print(f"Cyclic peptide conformations are in: {output_dir}")
        print(f"\\nNext steps:")
        print(f"1. Examine the final cyclic structures")
        print(f"2. Analyze the conformational ensemble")
        print(f"3. Check the quality of the cyclic bond formation")
        print(f"4. Use the cyclic peptides for further docking studies")
        return 0
    else:
        print("\\n❌ Cyclisation failed. Check the configuration and input files.")
        return 1


if __name__ == "__main__":
    sys.exit(main())