# Ramulator Validation Exercise

This exercise validates a port validation test from Ramulator1 to Ramulator2.

## Setup

This exercise depends on the following external repositories:

```bash
# Required for used traces and optinal for understanding the architecture
git clone https://github.com/CMU-SAFARI/ramulator.git

# Required for running the validation test
git clone https://github.com/CMU-SAFARI/ramulator2.git
```

**Note**: Please build Ramulator and Ramulator2 following their own README instructions before continuing.

Before running the test, make sure to unzip all trace files and copy the files to the correct directory used in the simulation:

```bash
cd ramulator/cputraces
gunzip -k 401.bzip2.gz
gunzip -k 403.gcc.gz
gunzip -k 429.mcf.gz
mkdir ../../ramulator2/cputraces/
cp 401.bzip2 403.gcc 429.mcf ../../ramulator2/cputraces/
```

```bash
cd ../../ramulator2/ && mkdir ./tests
cp ../tests/validation_test.py ./tests/
cp ../validation_config.yaml ./
```

## Running the Validation Test

After copying the test script and config, you can run the validation test in Ramulator2 using:

```bash
python3 tests/validation_test.py
```

This will execute the test and sanity checks in the terminal. The test will pass or fail based on the validation of these metrics.

You can also check the generated simulation statistics in `./ramulator2/DDR4.stats`.

## Steps Performed

1. **Ramulator1 Observation**
   - Examined the `test_spec.py` and `test_ramulator.py` files in the Ramulator1 repository.
   - Unzipped the traces `401.bzip2.gz`, `403.gcc`, and `429.mcf` in `cputraces/` using:
     ```bash
     gunzip -k cputraces/401.bzip2.gz
     gunzip -k cputraces/403.gcc.gz
     gunzip -k cputraces/429.mcf.gz
     ```
   - Ran Ramulator1 with the DDR4 configuration:
     ```bash
     ./ramulator configs/DDR4-config.cfg --mode=cpu cputraces/401.bzip2
     ```
   - Observed the execution and verified that statistics were written to `DDR4.stats`.

2. **Ramulator2 Test Preparation**
   - Reviewed the files in `ramulator2/src/test` and saw that they are not relevant to this exercise.
   - Created `validation_config.yaml` with settings similar to Ramulator1 DDR4 configuration.
   - Wrote `validation_test.py` script that:
     - Runs Ramulator2 using the specified config.
     - Collects key output metrics such as `total_num_read_requests`, `memory_system_cycles`, `avg_read_latency_0`, `row_hits_0`, and `row_misses_0`.
     - Checks that metrics are within expected sanity ranges.

3. **Purpose of the Test**
   - Ensure that Ramulator2 produces meaningful and reasonable simulation results.
   - Validate multiple traces in a single test run.
   - Verify the correct behavior of the memory system without directly comparing to Ramulator1 outputs.

## Validation Metrics

### What is being validated

The validation test ensures that Ramulator2 correctly simulates CPU traces and produces sane memory system statistics. It confirms that the simulation executes as expected for multiple traces and configurations.

### Metrics Checked

- `total_num_read_requests` — checks that the simulation generates read requests.
- `memory_system_cycles` — ensures that the memory system runs for a more than zero number of cycles.
- `avg_read_latency_0` — measures the average latency of read requests for core 0.
- `row_hits_0` — counts the number of row buffer hits.
- `row_misses_0` — counts the number of row buffer misses.

### Why These Metrics Are Relevant

These metrics provide a sanity check for the memory system simulation. They indicate whether the simulation is running correctly, whether requests are being handled as expected. Monitoring these ensures that Ramulator2 is producing reliable results.
