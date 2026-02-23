# HADDOCK3 MCP Scripts

Clean, self-contained scripts extracted from verified use cases for MCP tool wrapping.

## Design Principles

1. **Minimal Dependencies**: Only essential packages imported (standard library only)
2. **Self-Contained**: Functions inlined where possible, shared library for common operations
3. **Configurable**: Parameters in config files, not hardcoded
4. **MCP-Ready**: Each script has a main function ready for MCP wrapping

## Scripts

| Script | Description | Dependencies | Config |
|--------|-------------|--------------|--------|
| `protein_peptide_docking.py` | Protein-peptide docking using HADDOCK3 | Standard library only | `configs/protein_peptide_docking_config.json` |
| `cyclic_peptide_cyclisation.py` | Cyclise linear peptides into cyclic forms | Standard library only | `configs/cyclic_peptide_cyclisation_config.json` |
| `information_driven_docking.py` | Information-driven docking with experimental restraints | Standard library only | `configs/information_driven_docking_config.json` |

## Usage

### Environment Setup
```bash
# Activate environment (prefer mamba over conda)
mamba activate ./env  # or: conda activate ./env
```

### Script Execution

#### 1. Protein-Peptide Docking
```bash
# Basic usage
python scripts/protein_peptide_docking.py \\
  --input-protein examples/data/structures/1NX1_protein.pdb \\
  --input-peptide examples/data/structures/DAIDALSSDFT_3conformations.pdb \\
  --output results/docking_result

# With custom config
python scripts/protein_peptide_docking.py \\
  --input-protein protein.pdb \\
  --input-peptide peptide.pdb \\
  --config configs/protein_peptide_docking_config.json \\
  --output my_docking_result \\
  --ncores 8
```

#### 2. Cyclic Peptide Cyclisation
```bash
# Basic usage (auto-detects peptide length)
python scripts/cyclic_peptide_cyclisation.py \\
  --input examples/data/structures/1sfi_peptide-ensemble.pdb \\
  --output results/cyclisation_result

# With specified length
python scripts/cyclic_peptide_cyclisation.py \\
  --input linear_peptide.pdb \\
  --length 14 \\
  --config configs/cyclic_peptide_cyclisation_config.json \\
  --output my_cyclisation_result
```

#### 3. Information-Driven Docking
```bash
# With experimental restraints
python scripts/information_driven_docking.py \\
  --input-protein examples/data/structures/1NX1_protein.pdb \\
  --input-peptide examples/data/structures/DAIDALSSDFT_3conformations.pdb \\
  --active-protein "36,109,113" \\
  --active-peptide "1,5,8" \\
  --passive-protein "34,38,110,111" \\
  --passive-peptide "2,6,9" \\
  --output results/info_docking_result

# Fast scoring mode
python scripts/information_driven_docking.py \\
  --input-protein protein.pdb \\
  --input-peptide peptide.pdb \\
  --active-protein "10,15,20" \\
  --active-peptide "3,7" \\
  --scoring-mode fast \\
  --ncores 12
```

### Testing (Dry Run Mode)
All scripts support `--dry-run` to create configuration files without running HADDOCK3:
```bash
python scripts/protein_peptide_docking.py \\
  --input-protein examples/data/structures/1NX1_protein.pdb \\
  --input-peptide examples/data/structures/DAIDALSSDFT_3conformations.pdb \\
  --dry-run
```

## Shared Library

Common functions are in `scripts/lib/`:

### `lib/haddock.py`
- `run_haddock3()`: Execute HADDOCK3 with configuration
- `find_haddock_env()`: Locate HADDOCK3 environment

### `lib/validation.py`
- `validate_input_file()`: Validate input files
- `validate_pdb_format()`: Check PDB format
- `get_peptide_length_from_pdb()`: Extract peptide length

### `lib/utils.py`
- `parse_residue_list()`: Parse comma-separated residues
- `load_config_file()`: Load JSON configuration
- `merge_configs()`: Merge configuration dictionaries

## For MCP Wrapping (Step 6)

Each script exports a main function that can be wrapped:

```python
from scripts.protein_peptide_docking import run_protein_peptide_docking
from scripts.cyclic_peptide_cyclisation import run_cyclic_peptide_cyclisation
from scripts.information_driven_docking import run_information_driven_docking

# In MCP tool:
@mcp.tool()
def dock_protein_peptide(protein_file: str, peptide_file: str, output_dir: str = None):
    """Dock a cyclic peptide to a protein using HADDOCK3."""
    return run_protein_peptide_docking(protein_file, peptide_file, output_dir)

@mcp.tool()
def cyclise_peptide(peptide_file: str, output_dir: str = None):
    """Cyclise a linear peptide using HADDOCK3."""
    return run_cyclic_peptide_cyclisation(peptide_file, output_dir=output_dir)

@mcp.tool()
def dock_with_restraints(protein_file: str, peptide_file: str,
                        active_protein: List[int], active_peptide: List[int],
                        output_dir: str = None):
    """Perform information-driven docking with experimental restraints."""
    return run_information_driven_docking(
        protein_file, peptide_file,
        active_protein_residues=active_protein,
        active_peptide_residues=active_peptide,
        output_dir=output_dir
    )
```

## Configuration Files

Configuration files are in `configs/`:
- `protein_peptide_docking_config.json`: Default settings for protein-peptide docking
- `cyclic_peptide_cyclisation_config.json`: Settings for cyclisation protocol
- `information_driven_docking_config.json`: Settings for information-driven docking
- `default_config.json`: Common default settings

All scripts can use custom configuration files via `--config` parameter.

## Dependencies

### Runtime Requirements
- Python 3.8+
- HADDOCK3 (installed in conda/mamba environment)
- Standard library only (no external Python packages)

### Input File Formats
- **Protein/Peptide**: PDB format (.pdb)
- **Restraints**: HADDOCK table format (.tbl)
- **Configuration**: JSON format (.json)

### Output Formats
- **Structures**: PDB format
- **Configuration**: HADDOCK3 configuration (.cfg)
- **Restraints**: HADDOCK table format (.tbl)

## Error Handling

All scripts include comprehensive error handling:
- Input file validation
- PDB format checking
- Configuration validation
- HADDOCK3 execution monitoring
- Timeout handling

## Performance Notes

- **Protein-Peptide Docking**: 1-4 hours (depends on sampling)
- **Cyclisation**: 30-90 minutes (smaller systems)
- **Information-Driven**: 1-6 hours (enhanced sampling)

Use `--ncores` to specify CPU cores for optimal performance.

## Troubleshooting

### Common Issues

1. **File not found**: Check file paths are correct and files exist
2. **Environment not activated**: Ensure HADDOCK3 environment is active
3. **Insufficient memory**: Reduce sampling or use fewer cores
4. **Timeout**: Increase timeout in configuration or use fast mode

### Debug Mode

Use `--dry-run` to test configuration without running HADDOCK3:
```bash
python scripts/script_name.py --input file.pdb --dry-run
```

This creates configuration files that can be manually inspected and executed.