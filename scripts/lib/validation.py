"""
Input validation utilities for HADDOCK3 MCP scripts.

Functions for validating input files and parameters.
"""

from pathlib import Path
from typing import List


def validate_input_file(file_path: Path, file_type: str) -> bool:
    """
    Validate that input file exists and has correct format.

    Args:
        file_path: Path to the file to validate
        file_type: Type of file (e.g., "protein", "peptide", "pdb", "restraints")

    Returns:
        bool: True if valid

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If file has wrong format
    """
    if not file_path.exists():
        raise FileNotFoundError(f"{file_type} file not found: {file_path}")

    if file_type in ["protein", "peptide", "pdb"] and not file_path.suffix.lower() == ".pdb":
        raise ValueError(f"Expected PDB file, got: {file_path.suffix}")

    if file_type == "restraints" and not file_path.suffix.lower() == ".tbl":
        raise ValueError(f"Expected restraints file (.tbl), got: {file_path.suffix}")

    return True


def validate_pdb_format(pdb_file: Path) -> bool:
    """
    Basic validation of PDB file format.

    Args:
        pdb_file: Path to PDB file

    Returns:
        bool: True if basic format checks pass

    Raises:
        ValueError: If PDB format is invalid
    """
    try:
        with open(pdb_file, 'r') as f:
            lines = f.readlines()

        if not lines:
            raise ValueError(f"Empty PDB file: {pdb_file}")

        # Check for at least some ATOM records
        atom_count = sum(1 for line in lines if line.startswith(('ATOM', 'HETATM')))
        if atom_count == 0:
            raise ValueError(f"No ATOM records found in PDB file: {pdb_file}")

        return True

    except Exception as e:
        raise ValueError(f"Error reading PDB file {pdb_file}: {e}")


def get_peptide_length_from_pdb(pdb_file: Path) -> int:
    """
    Extract peptide length from PDB file by counting residues.

    Args:
        pdb_file: Path to PDB file

    Returns:
        int: Number of residues

    Raises:
        ValueError: If unable to determine length
    """
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


def validate_residue_list(residues: List[int], max_residue: int) -> bool:
    """
    Validate that residue numbers are within valid range.

    Args:
        residues: List of residue numbers
        max_residue: Maximum valid residue number

    Returns:
        bool: True if all residues are valid

    Raises:
        ValueError: If any residue is invalid
    """
    for res in residues:
        if res < 1 or res > max_residue:
            raise ValueError(f"Residue number {res} out of range (1-{max_residue})")
    return True