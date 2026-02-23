"""
General utility functions for HADDOCK3 MCP scripts.

Common helper functions used across multiple scripts.
"""

from pathlib import Path
from typing import List, Dict, Any, Union
import json


def parse_residue_list(residue_string: str) -> List[int]:
    """
    Parse comma-separated residue string to list of integers.

    Args:
        residue_string: Comma-separated string of residue numbers

    Returns:
        List of residue numbers

    Example:
        >>> parse_residue_list("1,5,8,12")
        [1, 5, 8, 12]
    """
    if not residue_string:
        return []
    return [int(x.strip()) for x in residue_string.split(",") if x.strip()]


def create_work_directory(work_dir: Union[str, Path]) -> Path:
    """
    Create and return a working directory path.

    Args:
        work_dir: Working directory path

    Returns:
        Path object for the working directory
    """
    work_path = Path(work_dir)
    work_path.mkdir(parents=True, exist_ok=True)
    return work_path


def load_config_file(config_file: Union[str, Path]) -> Dict[str, Any]:
    """
    Load configuration from JSON file.

    Args:
        config_file: Path to JSON configuration file

    Returns:
        Configuration dictionary

    Raises:
        FileNotFoundError: If config file doesn't exist
        json.JSONDecodeError: If config file is invalid JSON
    """
    config_path = Path(config_file)
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with open(config_path) as f:
        return json.load(f)


def merge_configs(default_config: Dict[str, Any], user_config: Dict[str, Any],
                  cli_overrides: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge configuration dictionaries with precedence: CLI > user_config > default.

    Args:
        default_config: Default configuration
        user_config: User-provided configuration
        cli_overrides: Command-line overrides

    Returns:
        Merged configuration dictionary
    """
    config = default_config.copy()

    # Update with user config
    if user_config:
        config.update(user_config)

    # Update with CLI overrides
    if cli_overrides:
        config.update(cli_overrides)

    return config


def format_residue_string(residues: List[int]) -> str:
    """
    Format list of residues as colon-separated string for HADDOCK restraints.

    Args:
        residues: List of residue numbers

    Returns:
        Formatted residue string

    Example:
        >>> format_residue_string([1, 5, 8, 12])
        "1:5:8:12"
    """
    if not residues:
        return "1"  # Default fallback
    return ":".join(map(str, residues))


def summarize_result(result: Dict[str, Any], operation: str) -> str:
    """
    Create a human-readable summary of operation results.

    Args:
        result: Result dictionary from script operation
        operation: Name of the operation

    Returns:
        Formatted summary string
    """
    lines = [f"\n{operation} Summary:"]
    lines.append("=" * (len(operation) + 9))

    if result.get("success"):
        lines.append("✅ Status: SUCCESS")
        if result.get("output_dir"):
            lines.append(f"📁 Results: {result['output_dir']}")
    else:
        lines.append("❌ Status: FAILED")

    lines.append(f"⚙️  Config: {result.get('config_file', 'N/A')}")
    lines.append(f"📂 Work Dir: {result.get('work_dir', 'N/A')}")

    # Add specific information based on operation
    if "restraints" in result:
        if isinstance(result["restraints"], dict):
            lines.append(f"🔗 Restraints: {len(result['restraints'])} files")
        else:
            lines.append(f"🔗 Restraints: {result['restraints']}")

    if "peptide_length" in result:
        lines.append(f"🧬 Peptide Length: {result['peptide_length']} residues")

    return "\n".join(lines)