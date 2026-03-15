import subprocess
import os
import yaml

config_file = os.path.join(os.path.dirname(__file__), "..", "validation_config.yaml")
ramulator2_bin = os.path.join(os.path.dirname(__file__), "..", "ramulator2")

# Load the config
with open(config_file, 'r') as f:
    config = yaml.safe_load(f)

# Temorary yaml
temp_config_file = os.path.join(os.path.dirname(__file__), "..", "tmp_config.yaml")
with open(temp_config_file, 'w') as f:
    yaml.safe_dump(config, f)

# Change the working directory
os.chdir(os.path.join(os.path.dirname(__file__), ".."))

# write to file to avoid buffer deadlock
log_file = "DDR4.stats"
with open(log_file, 'w') as f:
    proc = subprocess.Popen([ramulator2_bin, "-f", temp_config_file], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text = True)
    # Print output in real-time and write to file
    output = ""
    for line in proc.stdout:
        print(line, end="")
        f.write(line)
        output += line
    
    try:
        proc.wait(timeout=60)  # wait for 60 seconds
    except subprocess.TimeoutExpired:
        proc.kill()
        print("Ramulator2 timeout expired")

print("=== OUTPUT ===")
print(output)

# Parse metrics from the outputs
metrics = {}
for line in output.splitlines():
    line = line.strip()
    if line.startswith("total_num_read_requests"):
        metrics["total_num_read_requests"] = int(line.split(":")[-1])
    elif line.startswith("memory_system_cycles"):
        metrics["memory_system_cycles"] = int(line.split(":")[-1])
    elif line.startswith("avg_read_latency_0"):
        metrics["avg_read_latency_0"] = float(line.split(":")[-1])
    elif line.startswith("row_hits_0"):
        metrics["row_hits_0"] = int(line.split(":")[-1])
    elif line.startswith("row_misses_0"):
        metrics["row_misses_0"] = int(line.split(":")[-1])

# Basic sanity validations
for key, check, msg in [
    ("total_num_read_requests", lambda x: x > 0, "No read requests detected"),
    ("memory_system_cycles", lambda x: x > 0, "Memory system cycles should be > 0"),
    ("avg_read_latency_0", lambda x: x > 0, "Average read latency should be > 0"),
    ("row_hits_0", lambda x: x >= 0, "Row hits cannot be negative"),
    ("row_misses_0", lambda x: x >= 0, "Row misses cannot be negative")
]:
    if key in metrics:
        assert check(metrics[key]), msg

print("Ramulator2 test passed. Metrics collected:")
for k, v in metrics.items():
    print(f"{k}: {v}")

# Delete temporary yaml
if os.path.exists(temp_config_file):
    os.remove(temp_config_file)
    print(f"Temporary config file {temp_config_file} deleted.")