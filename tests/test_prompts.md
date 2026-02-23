# HADDOCK3 MCP Integration Test Prompts

## Tool Discovery Tests

### Prompt 1: List All Tools
"What MCP tools are available for HADDOCK3 molecular docking? Give me a brief description of each tool category."

### Prompt 2: Tool Details
"Explain how to use the submit_protein_peptide_docking tool, including all parameters and what files I need to provide."

### Prompt 3: Server Information
"Get information about the HADDOCK3 MCP server including available tools and typical runtimes."

## Environment Validation Tests

### Prompt 4: Validate Environment
"Check if the HADDOCK3 environment is properly configured for running molecular docking jobs."

### Prompt 5: Example Data Access
"What example data files are available for testing HADDOCK3 docking workflows?"

## Job Management Tests

### Prompt 6: List Jobs
"Show me all currently submitted HADDOCK3 jobs and their status."

### Prompt 7: List Completed Jobs Only
"List all completed HADDOCK3 jobs from previous runs."

## Submit API Tests - Basic Docking

### Prompt 8: Submit Basic Protein-Peptide Docking
"Submit a protein-peptide docking job using these files:
- Protein: examples/data/structures/1NX1_protein.pdb
- Peptide: examples/data/structures/1sfi_peptide-ensemble.pdb
Name the job 'test_basic_docking'"

### Prompt 9: Submit Cyclisation Job
"Submit a cyclic peptide cyclisation job using the file examples/data/structures/DAIDALSSDFT_ext.pdb with job name 'test_cyclisation'"

### Prompt 10: Check Job Status
"What's the current status of job <job_id>? Show me runtime information and current progress."

### Prompt 11: Get Job Logs
"Show me the last 30 lines of logs for job <job_id> to see what's happening."

### Prompt 12: Cancel Running Job
"Cancel the running job <job_id> if it's taking too long."

## Submit API Tests - Advanced Docking

### Prompt 13: Information-Driven Docking
"Submit an information-driven docking job with these parameters:
- Protein: examples/data/structures/1NX1_protein.pdb
- Peptide: examples/data/structures/1sfi_peptide-ensemble.pdb
- Active protein residues: '36,109,113'
- Active peptide residues: '1,5,8'
- Job name: 'info_guided_test'"

### Prompt 14: Batch Docking
"Submit a batch protein-peptide docking job with:
- Protein: examples/data/structures/1NX1_protein.pdb
- Peptides: ['examples/data/structures/1sfi_peptide-ensemble.pdb', 'examples/data/structures/test_peptide.pdb']
- Job name: 'batch_screening_test'"

## Results and Analysis Tests

### Prompt 15: Get Completed Results
"Get the final results for completed job <job_id>. Show me the output files and HADDOCK3 analysis."

### Prompt 16: Analyze Batch Results
"Get results from all jobs in the batch <batch_job_id> and summarize the docking outcomes."

## Error Handling Tests

### Prompt 17: Invalid File Path
"Submit a docking job with a non-existent protein file to test error handling."

### Prompt 18: Missing Required Parameters
"Submit an information-driven docking job without specifying any active residues."

### Prompt 19: Invalid Job ID
"Get the status of a non-existent job ID 'invalid_job_123' to test error responses."

## End-to-End Workflow Tests

### Prompt 20: Complete Docking Workflow
"I want to perform protein-peptide docking with the following workflow:
1. First validate that HADDOCK3 environment is ready
2. Get available example data paths
3. Submit a docking job using 1NX1_protein.pdb and 1sfi_peptide-ensemble.pdb
4. Monitor the job progress with status checks
5. When completed, show me the final results
Name the job 'complete_workflow_test'"

### Prompt 21: Cyclisation and Docking Pipeline
"Run this complete pipeline:
1. First cyclise the linear peptide DAIDALSSDFT_ext.pdb
2. Once cyclisation completes, use the cyclised peptide to dock against 1NX1_protein.pdb
3. Monitor both jobs and show final structures from the docking
Name the jobs 'pipeline_cyclise' and 'pipeline_dock'"

### Prompt 22: Comparative Docking Study
"Perform a comparative docking study:
1. Submit information-driven docking with active residues
2. Submit regular docking without restraints
3. Use the same protein (1NX1_protein.pdb) and peptide (1sfi_peptide-ensemble.pdb)
4. Compare the results when both complete
Name jobs 'comparison_info' and 'comparison_free'"

### Prompt 23: Virtual Screening Simulation
"Simulate a virtual screening workflow:
1. Prepare a batch docking of multiple peptides against 1NX1_protein.pdb
2. Use all available peptide files in examples/data/structures/
3. Monitor the batch progress
4. Collect and rank results by HADDOCK score
5. Identify the top 3 binding peptides
Name it 'virtual_screening_batch'"

## Performance and Monitoring Tests

### Prompt 24: Job Queue Management
"Show me how to manage multiple concurrent jobs:
1. Submit 3 different docking jobs
2. List all running jobs
3. Monitor progress of each
4. Show how to prioritize or cancel specific jobs if needed"

### Prompt 25: Resource Monitoring
"Submit a resource-intensive job and monitor:
1. Job execution logs in real-time
2. Check if the job is progressing normally
3. Estimate remaining runtime based on current progress
4. Show how to handle jobs that might be stuck"

## Integration Validation Tests

### Prompt 26: Tool Chain Validation
"Validate the complete tool chain by:
1. Checking server info and available tools
2. Validating HADDOCK3 environment
3. Testing job submission, monitoring, and result retrieval
4. Confirming all 12 tools work correctly"

### Prompt 27: File Format Validation
"Test file format handling:
1. Try submitting jobs with different PDB file types
2. Test with multi-conformation peptide files
3. Validate error handling for corrupted files
4. Check output file accessibility"

## Stress Testing Scenarios

### Prompt 28: Multiple Job Submission
"Test concurrent job handling by submitting multiple jobs simultaneously and monitoring system performance."

### Prompt 29: Large File Handling
"Test with larger protein/peptide complexes to validate memory and storage handling."

### Prompt 30: Long-Running Job Management
"Submit a job expected to run for several hours and test:
1. Job persistence across server restarts
2. Log file rotation and management
3. Progress tracking over extended periods
4. Cleanup of completed jobs"

## Expected Behaviors

**For Job Submission (Prompts 8-14):**
- Should return job_id immediately
- Status should be 'submitted' or 'pending'
- Job should appear in job list

**For Job Monitoring (Prompts 10-11):**
- Status updates: pending → running → completed/failed
- Log output should show HADDOCK3 progress
- Runtime tracking should work

**For Job Results (Prompts 15-16):**
- Final results include PDB structures
- HADDOCK3 analysis data provided
- Output files accessible

**For Error Handling (Prompts 17-19):**
- Clear error messages returned
- No server crashes or hangs
- Structured error responses

**For End-to-End Workflows (Prompts 20-23):**
- Multi-step processes execute correctly
- Dependencies handled properly
- Results are coherent and complete

**Performance Expectations:**
- Job submission: < 5 seconds
- Status checks: < 2 seconds
- Result retrieval: < 10 seconds
- Log access: < 3 seconds

**Error Recovery:**
- Invalid inputs handled gracefully
- Server remains responsive
- Jobs can be cancelled safely
- Failed jobs don't affect others

These test prompts cover all aspects of the HADDOCK3 MCP server functionality including job lifecycle management, batch processing, error handling, and real-world molecular docking workflows.