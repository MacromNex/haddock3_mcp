# Step 3: Use Cases Report

## Scan Information
- **Scan Date**: 2025-12-31
- **Filter Applied**: cyclic peptide docking using HADDOCK, information-driven docking protocol, protein-peptide interactions
- **Python Version**: 3.12.12
- **Environment Strategy**: Single environment (Python >= 3.10)
- **Repository**: HADDOCK3 2025.11.0

## Use Cases Identified and Extracted

### UC-001: Protein-Peptide Docking
- **Description**: Basic protein-peptide docking protocol for cyclic and linear peptides using HADDOCK3's multi-stage workflow
- **Script Path**: `examples/use_case_1_protein_peptide_docking.py`
- **Complexity**: Medium
- **Priority**: High
- **Environment**: `./env`
- **Source**: `repo/haddock3/examples/docking-protein-peptide/`

**Inputs:**
| Name | Type | Description | Parameter |
|------|------|-------------|----------|
| protein_pdb | file | Protein structure in PDB format | --protein |
| peptide_pdb | file | Peptide structure(s) - can contain multiple conformations | --peptide |
| restraints | file | Ambiguous interaction restraints (experimental data) | --restraints |
| ncores | integer | Number of CPU cores to use | --ncores |
| output_dir | string | Output directory name | --output |

**Outputs:**
| Name | Type | Description |
|------|------|-------------|
| docked_complexes | directory | Protein-peptide complex structures |
| binding_scores | file | HADDOCK scores and energy terms |
| cluster_analysis | file | Structural clustering results |
| interface_contacts | file | Contact analysis at binding interface |

**Example Usage:**
```bash
# Basic usage with demo data
python examples/use_case_1_protein_peptide_docking.py

# Custom run with high-performance settings
python examples/use_case_1_protein_peptide_docking.py \
    --protein examples/data/structures/1NX1_protein.pdb \
    --peptide examples/data/structures/DAIDALSSDFT_3conformations.pdb \
    --restraints examples/data/restraints/ambig.tbl \
    --ncores 20 \
    --output production_docking_run
```

**Example Data**:
- `examples/data/structures/1NX1_protein.pdb` (HIV-1 protease)
- `examples/data/structures/DAIDALSSDFT_3conformations.pdb` (peptide ensemble)
- `examples/data/restraints/ambig.tbl` (experimental restraints)

---

### UC-002: Cyclic Peptide Cyclisation
- **Description**: Convert linear peptides to cyclic peptides using HADDOCK3's specialized cyclisation protocol with distance restraints and topology rebuilding
- **Script Path**: `examples/use_case_2_cyclic_peptide_cyclisation.py`
- **Complexity**: Medium
- **Priority**: High
- **Environment**: `./env`
- **Source**: `repo/haddock3/examples/peptide-cyclisation/`

**Inputs:**
| Name | Type | Description | Parameter |
|------|------|-------------|----------|
| peptide_pdb | file | Linear peptide structure or ensemble | --peptide |
| peptide_length | integer | Number of residues (auto-detected if not specified) | --length |
| ncores | integer | Number of CPU cores to use | --ncores |
| output_dir | string | Output directory name | --output |

**Outputs:**
| Name | Type | Description |
|------|------|-------------|
| cyclic_structures | directory | Cyclised peptide conformations |
| conformational_ensemble | file | Multiple cyclic conformations |
| cyclisation_quality | file | Quality assessment of bond formation |
| rmsd_clusters | file | Conformational clustering analysis |

**Example Usage:**
```bash
# Basic cyclisation with demo data
python examples/use_case_2_cyclic_peptide_cyclisation.py

# Custom peptide with specified length
python examples/use_case_2_cyclic_peptide_cyclisation.py \
    --peptide my_linear_peptide.pdb \
    --length 14 \
    --ncores 8 \
    --output cyclic_peptide_ensemble
```

**Example Data**:
- `examples/data/structures/1sfi_peptide-ensemble.pdb` (14-residue peptide)
- `examples/data/structures/3wne_peptide-ensemble.pdb` (6-residue peptide)
- `examples/data/restraints/1sfi_unambig.tbl` (cyclisation restraints)

---

### UC-003: Information-Driven Docking Protocol
- **Description**: Advanced docking protocol that incorporates experimental restraints from NMR, mutagenesis, cross-linking, and other experimental techniques to guide docking
- **Script Path**: `examples/use_case_3_information_driven_docking.py`
- **Complexity**: Complex
- **Priority**: High
- **Environment**: `./env`
- **Source**: `repo/haddock3/examples/docking-protein-peptide/` + HADDOCK3 information-driven protocols

**Inputs:**
| Name | Type | Description | Parameter |
|------|------|-------------|----------|
| protein_pdb | file | Protein structure in PDB format | --protein |
| peptide_pdb | file | Peptide structure(s) | --peptide |
| active_protein | list | Active residues on protein (strong experimental evidence) | --active-protein |
| passive_protein | list | Passive residues on protein (weak evidence) | --passive-protein |
| active_peptide | list | Active residues on peptide (strong experimental evidence) | --active-peptide |
| passive_peptide | list | Passive residues on peptide (weak evidence) | --passive-peptide |
| distance_restraints | file | Specific distance restraints from experiments | --distance-restraints |
| scoring_mode | choice | "fast" or "full" sampling mode | --scoring-mode |

**Outputs:**
| Name | Type | Description |
|------|------|-------------|
| high_confidence_complexes | directory | Experimentally-validated docking solutions |
| restraint_satisfaction | file | Analysis of experimental restraint satisfaction |
| interface_validation | file | Detailed interface analysis with confidence scores |
| cluster_ranking | file | Clusters ranked by experimental data consistency |

**Example Usage:**
```bash
# Basic information-driven docking
python examples/use_case_3_information_driven_docking.py

# Advanced usage with experimental restraints
python examples/use_case_3_information_driven_docking.py \
    --protein examples/data/structures/1NX1_protein.pdb \
    --peptide examples/data/structures/DAIDALSSDFT_3conformations.pdb \
    --active-protein "36,109,113" \
    --active-peptide "1,5,8" \
    --passive-protein "34,38,110,111" \
    --passive-peptide "2,6,9" \
    --scoring-mode full \
    --ncores 20
```

**Example Data**:
- Same structural data as UC-001
- Additional experimental restraints from literature
- Active/passive residue definitions based on mutagenesis studies

---

## Demo Data Summary

### Structural Data Index

| File | Size | Description | Use Cases |
|------|------|-------------|-----------|
| `1NX1_protein.pdb` | 131 KB | HIV-1 protease protein structure | UC-001, UC-003 |
| `1nx1_refe.pdb` | 113 KB | Reference complex for validation | All (reference) |
| `DAIDALSSDFT_3conformations.pdb` | 23 KB | Peptide ensemble (3 conformations) | UC-001, UC-003 |
| `DAIDALSSDFT_alpha.pdb` | 7 KB | Peptide in alpha-helical conformation | Alternative input |
| `DAIDALSSDFT_ext.pdb` | 7 KB | Extended peptide conformation | Alternative input |
| `DAIDALSSDFT_polyII.pdb` | 7 KB | Polyproline II peptide conformation | Alternative input |
| `1sfi_peptide-ensemble.pdb` | 34 KB | Linear peptide ensemble for cyclisation | UC-002 |
| `1sfi_peptide-bound.pdb` | 8 KB | Reference cyclic peptide structure | UC-002 (validation) |
| `3wne_peptide-ensemble.pdb` | 14 KB | Small peptide ensemble (6 residues) | UC-002 (alternative) |
| `3wne_peptide-bound.pdb` | 3 KB | Small cyclic peptide reference | UC-002 (validation) |

### Restraints Data Index

| File | Size | Description | Use Cases |
|------|------|-------------|-----------|
| `ambig.tbl` | 10 KB | Ambiguous interaction restraints for 1NX1-peptide | UC-001, UC-003 |
| `1sfi_unambig.tbl` | 252 B | Distance restraints for 1SFI cyclisation | UC-002 |
| `3wne_unambig.tbl` | 122 B | Distance restraints for 3WNE cyclisation | UC-002 |

## Summary Statistics

| Metric | Count |
|--------|-------|
| **Total Use Cases Found** | 15+ (in repository) |
| **Use Cases Extracted** | 3 |
| **Scripts Created** | 3 |
| **High Priority** | 3 |
| **Medium Priority** | 0 |
| **Low Priority** | 0 |
| **Demo Data Files Copied** | 13 |
| **Example Configurations** | 3 |

## Coverage Analysis

### Cyclic Peptide Workflow Coverage
- ✅ **Linear to Cyclic Conversion**: UC-002 covers peptide cyclisation
- ✅ **Protein-Peptide Docking**: UC-001 covers basic docking protocol
- ✅ **Experimental Data Integration**: UC-003 covers information-driven approaches
- ✅ **Multiple Conformations**: All use cases handle ensemble inputs
- ✅ **Validation Protocols**: Reference structures provided for all examples

### HADDOCK3 Protocol Coverage
- ✅ **Rigid Body Docking**: Covered in UC-001, UC-003
- ✅ **Flexible Refinement**: Covered in all use cases
- ✅ **Water Refinement**: Covered in UC-002, UC-003
- ✅ **Clustering Analysis**: Covered in all use cases
- ✅ **Energy Minimization**: Covered in UC-001, UC-003
- ✅ **Topology Rebuilding**: Specialized for UC-002 cyclisation

### Experimental Data Types Supported
- ✅ **NMR Chemical Shift Perturbations**: Active/passive residue definitions
- ✅ **Mutagenesis Data**: Interface residue mapping
- ✅ **Cross-linking Mass Spectrometry**: Distance restraints
- ✅ **Hydrogen-Deuterium Exchange**: Solvent accessibility constraints
- ✅ **Computational Predictions**: Binding site predictions

## Technical Implementation

### Script Features
- **CLI Interface**: All scripts use argparse for command-line usage
- **Error Handling**: Comprehensive error checking and user feedback
- **Dry Run Mode**: Configuration testing without execution
- **Progress Monitoring**: Real-time progress updates and timeouts
- **Flexible Input**: Support for custom files and demo data
- **Documentation**: Extensive help text and usage examples

### Configuration Management
- **Auto-generated Configs**: Scripts create HADDOCK3 .cfg files dynamically
- **Parameter Validation**: Input validation before execution
- **Restraint Generation**: Automatic creation of restraint files
- **Path Resolution**: Robust file path handling

### Output Management
- **Structured Results**: Organized output directories
- **Analysis Tools**: Built-in result interpretation
- **Visualization**: Integration with plotting tools
- **Quality Assessment**: Automated model validation

## Quality Assurance

### Testing Status
- ✅ **Syntax Validation**: All scripts pass Python syntax checks
- ✅ **Import Testing**: Required modules verified
- ✅ **CLI Testing**: Command-line interfaces functional
- ✅ **Dry Run Testing**: Configuration generation successful
- ✅ **Documentation**: Complete usage examples provided

### Known Limitations
- **Runtime Requirements**: Some protocols require 1-4 hours execution time
- **Memory Usage**: Large systems may need 8+ GB RAM
- **CPU Scaling**: Performance scales with available cores
- **CNS Dependency**: Optional warnings may appear for CNS binary

## Integration with MCP

### MCP Tool Potential
Each use case can be converted to MCP tools with the following capabilities:

1. **Protein-Peptide Docking Tool**
   - Input: Protein PDB, Peptide PDB, Restraints
   - Output: Docked complexes with scores
   - Parameters: Sampling, cores, scoring mode

2. **Peptide Cyclisation Tool**
   - Input: Linear peptide PDB
   - Output: Cyclic peptide ensemble
   - Parameters: Cyclisation strategy, cluster count

3. **Information-Driven Docking Tool**
   - Input: Structures + experimental data
   - Output: High-confidence complexes
   - Parameters: Restraint types, validation mode

### Workflow Integration
- **Sequential Processing**: Cyclisation → Docking → Analysis
- **Batch Processing**: Multiple peptides or targets
- **Validation Pipelines**: Experimental data consistency checks
- **Results Management**: Automated analysis and reporting

## References

1. **HADDOCK3 Software**: Giulini, M., et al. J. Chem. Inf. Model. (2025). doi: 10.1021/acs.jcim.5c00969
2. **Cyclisation Protocol**: Trellet, M., et al. J. Chem. Theory Comput. (2022). doi: 10.1021/acs.jctc.2c00075
3. **Information-Driven Docking**: Reys, V., et al. Nature Protocols (2024). doi: 10.1038/s41596-024-01011-0

This use case analysis demonstrates comprehensive coverage of cyclic peptide computational workflows using HADDOCK3, with practical implementations ready for MCP integration.