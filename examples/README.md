# HADDOCK3 MCP Examples

This directory contains use case examples for cyclic peptide docking using HADDOCK3. Each example demonstrates a different aspect of the HADDOCK3 workflow for computational peptide analysis.

## Available Use Cases

### UC-001: Protein-Peptide Docking
**Script**: `use_case_1_protein_peptide_docking.py`
**Purpose**: Basic protein-peptide docking protocol

Demonstrates how to dock cyclic or linear peptides to protein targets using HADDOCK3's multi-stage docking protocol.

```bash
# Basic usage with demo data
python examples/use_case_1_protein_peptide_docking.py

# Custom input files
python examples/use_case_1_protein_peptide_docking.py \
    --protein examples/data/structures/1NX1_protein.pdb \
    --peptide examples/data/structures/DAIDALSSDFT_3conformations.pdb \
    --restraints examples/data/restraints/ambig.tbl \
    --ncores 8
```

**Input Requirements**:
- Protein PDB structure
- Peptide PDB structure(s) - can contain multiple conformations
- Ambiguous interaction restraints (experimental data)

**Outputs**:
- Docked peptide-protein complexes
- Binding scores and cluster analysis
- Interface contact maps

### UC-002: Cyclic Peptide Cyclisation
**Script**: `use_case_2_cyclic_peptide_cyclisation.py`
**Purpose**: Convert linear peptides to cyclic peptides

Uses HADDOCK3's specialized cyclisation protocol to generate realistic cyclic peptide conformations from linear sequences.

```bash
# Basic cyclisation with demo data
python examples/use_case_2_cyclic_peptide_cyclisation.py

# Custom peptide cyclisation
python examples/use_case_2_cyclic_peptide_cyclisation.py \
    --peptide examples/data/structures/1sfi_peptide-ensemble.pdb \
    --length 14 \
    --ncores 8
```

**Input Requirements**:
- Linear peptide PDB structure
- Peptide length (auto-detected if not specified)

**Outputs**:
- Cyclic peptide conformations
- Conformational ensemble analysis
- Quality assessment of cyclisation

**Reference**: [Trellet et al., J. Chem. Theory Comput. 2022](https://doi.org/10.1021/acs.jctc.2c00075)

### UC-003: Information-Driven Docking
**Script**: `use_case_3_information_driven_docking.py`
**Purpose**: Advanced docking guided by experimental data

Incorporates experimental restraints (NMR, mutagenesis, cross-linking) to guide the docking process for more accurate predictions.

```bash
# Basic information-driven docking
python examples/use_case_3_information_driven_docking.py

# With custom experimental restraints
python examples/use_case_3_information_driven_docking.py \
    --protein examples/data/structures/1NX1_protein.pdb \
    --peptide examples/data/structures/DAIDALSSDFT_3conformations.pdb \
    --active-protein "36,109,113" \
    --active-peptide "1,5,8" \
    --passive-protein "34,38,110,111" \
    --passive-peptide "2,6,9"
```

**Input Requirements**:
- Protein and peptide structures
- Experimental data defining:
  - Active residues (strong evidence for binding)
  - Passive residues (weaker evidence or interface neighbors)
  - Optional: specific distance restraints

**Outputs**:
- High-confidence protein-peptide complexes
- Experimental data validation
- Interface analysis with confidence scores

## Demo Data Index

### Structures (`examples/data/structures/`)

| File | Description | Source | Use Case |
|------|-------------|---------|----------|
| `1NX1_protein.pdb` | HIV-1 protease protein | PDB: 1NX1 | UC-001, UC-003 |
| `1nx1_refe.pdb` | Reference complex structure | PDB: 1NX1 | Validation |
| `DAIDALSSDFT_3conformations.pdb` | Linear peptide (3 conformations) | Generated | UC-001, UC-003 |
| `DAIDALSSDFT_alpha.pdb` | Peptide in alpha conformation | Generated | Alternative input |
| `DAIDALSSDFT_ext.pdb` | Peptide in extended conformation | Generated | Alternative input |
| `DAIDALSSDFT_polyII.pdb` | Peptide in polyproline II conformation | Generated | Alternative input |
| `1sfi_peptide-bound.pdb` | Cyclic peptide (bound state) | PDB: 1SFI | UC-002 reference |
| `1sfi_peptide-ensemble.pdb` | Linear peptide ensemble for cyclisation | PDB: 1SFI | UC-002 |
| `3wne_peptide-bound.pdb` | Small cyclic peptide (bound) | PDB: 3WNE | UC-002 reference |
| `3wne_peptide-ensemble.pdb` | Small linear peptide ensemble | PDB: 3WNE | UC-002 alternative |

### Restraints (`examples/data/restraints/`)

| File | Description | Use Case |
|------|-------------|----------|
| `ambig.tbl` | Ambiguous interaction restraints for 1NX1-peptide | UC-001, UC-003 |
| `1sfi_unambig.tbl` | Distance restraints for 1SFI cyclisation | UC-002 |
| `3wne_unambig.tbl` | Distance restraints for 3WNE cyclisation | UC-002 |

## System Requirements

### Computational Resources
- **Minimum**: 4 CPU cores, 8 GB RAM
- **Recommended**: 8+ CPU cores, 16+ GB RAM
- **Runtime**: 30 minutes to 4 hours depending on system size

### Software Dependencies
- HADDOCK3 2025.11.0+
- Python 3.12+
- Biopython, NumPy, SciPy, Pandas
- FreeSASA (for surface calculations)

## Quick Start

1. **Setup Environment**:
```bash
# Activate the HADDOCK3 environment
mamba activate ./env

# Verify installation
haddock3 --version
```

2. **Run Demo Examples**:
```bash
# Test protein-peptide docking (15-30 minutes)
python examples/use_case_1_protein_peptide_docking.py --dry-run

# Test peptide cyclisation (30-60 minutes)
python examples/use_case_2_cyclic_peptide_cyclisation.py --dry-run

# Test information-driven docking (45-90 minutes)
python examples/use_case_3_information_driven_docking.py --dry-run
```

3. **Customize for Your System**:
   - Replace demo PDB files with your structures
   - Modify restraints based on your experimental data
   - Adjust computational parameters (ncores, sampling)

## Understanding the Results

### Output Directory Structure
```
run_directory/
├── 00_topoaa/           # Topology generation
├── 01_rigidbody/        # Rigid body docking
├── 02_caprieval/        # Evaluation metrics
├── 03_seletop/          # Model selection
├── 04_flexref/          # Flexible refinement
├── 05_caprieval/        # Re-evaluation
├── 06_emref/            # Energy minimization
├── 07_clustfcc/         # Clustering
└── 08_seletopclusts/    # Final selection
```

### Key Output Files
- `*.pdb`: Docked/cyclised structures
- `*_scores.txt`: Binding scores and energies
- `*_capri.txt`: Model quality assessment
- `contact_*.txt`: Interface contact analysis

### Interpretation Guidelines
1. **HADDOCK Score**: Lower values indicate better models
2. **CAPRI Quality**: High/Medium/Acceptable/Incorrect
3. **Interface Contacts**: Number of intermolecular contacts
4. **Energy Terms**: Van der Waals, electrostatic, desolvation

## Troubleshooting

### Common Issues

1. **"No module named 'haddock'"**
   ```bash
   # Solution: Activate environment
   mamba activate ./env
   ```

2. **"CNS binary could not be executed"**
   - Usually not critical for basic usage
   - CNS is used for advanced energy calculations

3. **"HADDOCK3 timed out"**
   - Reduce sampling parameters
   - Use `--scoring-mode fast`
   - Increase timeout in script

4. **Memory errors**
   - Reduce ncores parameter
   - Use smaller peptides for testing
   - Close other applications

### Performance Optimization

- **Fast testing**: Use `--scoring-mode fast`
- **Production runs**: Increase ncores to match your system
- **Large systems**: Consider using HPC resources
- **Memory efficiency**: Process peptides in batches

## Further Reading

- [HADDOCK3 Documentation](https://www.bonvinlab.org/haddock3)
- [HADDOCK3 Best Practices](https://www.bonvinlab.org/software/bpg/)
- [Peptide Cyclisation Protocol](https://doi.org/10.1021/acs.jctc.2c00075)
- [Information-Driven Docking](https://doi.org/10.1038/s41596-024-01011-0)

## Citation

If you use these examples in your research, please cite:

> Giulini, M., et al. "HADDOCK3: A modular and versatile platform for integrative modelling of biomolecular complexes." J. Chem. Inf. Model. (2025). doi: 10.1021/acs.jcim.5c00969