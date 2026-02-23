"""
Shared library for HADDOCK3 MCP scripts.

This library contains common functions extracted from the use case scripts
to minimize code duplication and provide consistent functionality.
"""

__version__ = "1.0.0"
__author__ = "HADDOCK3 MCP Tool"

from .haddock import run_haddock3, find_haddock_env
from .validation import validate_input_file, validate_pdb_format
from .utils import parse_residue_list, create_work_directory

__all__ = [
    "run_haddock3",
    "find_haddock_env",
    "validate_input_file",
    "validate_pdb_format",
    "parse_residue_list",
    "create_work_directory"
]