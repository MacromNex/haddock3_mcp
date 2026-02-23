# HADDOCK3 MCP Configuration Files

JSON configuration files for HADDOCK3 MCP scripts with default parameters and documentation.

## Configuration Files

### `default_config.json`
Common default settings shared across all scripts:
- Execution parameters (cores, timeout, mode)
- Environment settings (conda path, commands)
- File format specifications
- Validation settings
- Path patterns

### `protein_peptide_docking_config.json`
Specific settings for protein-peptide docking:
- Sampling parameters (200 structures)
- Flexibility settings (peptide chain B)
- MD steps for each refinement phase
- Clustering parameters for final selection

### `cyclic_peptide_cyclisation_config.json`
Settings for cyclic peptide cyclisation protocol:
- Cyclisation distance parameters
- Multi-stage refinement settings
- Clustering for conformational sampling
- Water refinement parameters

### `information_driven_docking_config.json`
Configuration for information-driven docking:
- Sampling modes (fast vs. full)
- Selection criteria for each stage
- Flexibility definitions (protein + peptide)
- Enhanced clustering parameters

## Usage

### Loading Configuration in Scripts
```python
import json

# Load specific config
with open('configs/protein_peptide_docking_config.json') as f:
    config = json.load(f)

# Use in script
result = run_protein_peptide_docking(
    protein_file="protein.pdb",
    peptide_file="peptide.pdb",
    config=config
)
```

### CLI Usage
```bash
# Use specific configuration
python scripts/protein_peptide_docking.py \\
    --input-protein protein.pdb \\
    --input-peptide peptide.pdb \\
    --config configs/protein_peptide_docking_config.json

# Override specific parameters
python scripts/protein_peptide_docking.py \\
    --input-protein protein.pdb \\
    --input-peptide peptide.pdb \\
    --config configs/protein_peptide_docking_config.json \\
    --ncores 8  # Overrides config value
```

## Configuration Structure

All configuration files follow this pattern:

```json
{
  "_description": "Human-readable description of the configuration",
  "_source": "Original source of the settings",

  "parameter_category": {
    "parameter_name": "value",
    "_description": "Explanation of this category"
  }
}
```

### Common Parameters

#### Execution Settings
- `ncores`: Number of CPU cores (default: 4)
- `timeout`: Maximum execution time in seconds
- `mode`: Execution mode ("local")

#### Sampling Parameters
- `sampling`: Number of structures to generate
- `tolerance`: Constraint violation tolerance
- `sampling_factor`: Multiplication factor for sampling

#### Flexibility Settings
- `flexible.start/end/segment`: Residue ranges and chain IDs
- Parameters define which parts of molecules are flexible during refinement

#### MD Parameters
- `md_steps.rigid/cool1/cool2/cool3`: Molecular dynamics steps
- `water_steps`: Steps for explicit water refinement

#### Clustering Settings
- `min_population`: Minimum cluster size
- `top_models/top_clusters`: Number of final structures

## Customization

### Creating Custom Configurations

1. **Start with defaults**:
```bash
cp configs/protein_peptide_docking_config.json configs/my_custom_config.json
```

2. **Edit parameters**:
```json
{
  "_description": "My custom docking configuration",
  "ncores": 16,
  "sampling": 500,
  "md_steps": {
    "rigid": 10000,
    "cool1": 10000,
    "cool2": 20000,
    "cool3": 20000
  }
}
```

3. **Use in scripts**:
```bash
python scripts/protein_peptide_docking.py \\
    --config configs/my_custom_config.json \\
    --input-protein protein.pdb \\
    --input-peptide peptide.pdb
```

### Parameter Guidelines

#### For Fast Testing
- Reduce `sampling` (100-200)
- Reduce `md_steps` (2000-5000)
- Use `scoring_mode`: "fast"

#### For Production Runs
- Increase `sampling` (500-1000)
- Increase `md_steps` (5000-20000)
- Use `scoring_mode`: "full"

#### For Large Systems
- Increase `timeout` (7200-14400 seconds)
- Increase `ncores` (8-32)
- Consider reducing `sampling` initially

## Configuration Validation

Scripts automatically validate configuration parameters:
- Required fields are checked
- Numeric ranges are validated
- File paths are verified
- Default values are applied for missing parameters

## Examples

### High-Throughput Configuration
```json
{
  "_description": "High-throughput configuration with reduced sampling",
  "ncores": 16,
  "timeout": 1800,
  "sampling": 100,
  "scoring_mode": "fast",
  "md_steps": {
    "rigid": 2000,
    "cool1": 2000,
    "cool2": 4000,
    "cool3": 4000
  }
}
```

### Detailed Analysis Configuration
```json
{
  "_description": "Detailed analysis with extensive sampling",
  "ncores": 8,
  "timeout": 14400,
  "sampling": 1000,
  "scoring_mode": "full",
  "md_steps": {
    "rigid": 10000,
    "cool1": 10000,
    "cool2": 20000,
    "cool3": 20000
  },
  "clustering": {
    "min_population": 2,
    "top_models": 20
  }
}
```