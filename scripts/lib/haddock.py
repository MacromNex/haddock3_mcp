"""
HADDOCK3 execution utilities for MCP scripts.

Common functions for running HADDOCK3 and managing environments.
"""

import subprocess
from pathlib import Path
from typing import Tuple, Optional


def find_haddock_env() -> Path:
    """Find the HADDOCK3 environment path."""
    # Try current directory first
    env_path = Path.cwd() / "env"
    if env_path.exists():
        return env_path

    # Try relative to script directory
    env_path = Path(__file__).parent.parent.parent / "env"
    if env_path.exists():
        return env_path

    # Default fallback
    return Path.cwd() / "env"


def run_haddock3(config_file: Path, work_dir: Path, timeout: int = 3600,
                description: str = "HADDOCK3") -> Tuple[bool, Optional[Path]]:
    """
    Execute HADDOCK3 with the given configuration.

    Args:
        config_file: Path to HADDOCK3 configuration file
        work_dir: Working directory for execution
        timeout: Timeout in seconds (default: 1 hour)
        description: Description for log messages

    Returns:
        tuple: (success, output_dir)
    """
    try:
        print(f"Running {description} with configuration: {config_file}")
        print("This may take several minutes to hours depending on the system size...")

        # Find environment path
        env_path = find_haddock_env()

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
            print(f"{description} completed successfully!")
            # Find the output directory
            run_dirs = [d for d in work_dir.iterdir() if d.is_dir() and d.name.startswith("run")]
            if run_dirs:
                output_dir = run_dirs[0]  # Take the first run directory
                print(f"Results available in: {output_dir}")
                return True, output_dir
        else:
            print(f"{description} failed!")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False, None

    except subprocess.TimeoutExpired:
        print(f"{description} timed out after {timeout} seconds")
        return False, None
    except Exception as e:
        print(f"Error running {description}: {e}")
        return False, None