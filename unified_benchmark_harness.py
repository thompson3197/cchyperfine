# -*- coding: utf-8 -*-
# Unified benchmark harness combining core steps and advanced extensions in Python 2.7.
import sys  # Import sys module for system operations.
import time  # Import time module for wall-clock measurement.
import subprocess  # Import subprocess for process execution.
import os  # Import os module for environment and platform checks.
import math  # Import math module for statistical calculations.
import json  # Import json module for result serialization.

TRACE_LOG = []  # Initialize static list buffer for trace logging statements.

def log_trace(message):  # Define function to record execution trace logs.
    assert isinstance(message, str), "Log message must be a string."  # Rule 9: Assert input is string.
    assert len(message) > 0, "Log message cannot be empty."  # Rule 9: Assert input is non-empty.
    TRACE_LOG.append(message)  # Append message into trace buffer.
    return True  # Rule 11: Explicit return value indicating success.

def execute_command_harness(cmd_str, core_id):  # Define function to execute pinned command.
    assert isinstance(cmd_str, str), "Command must be string."  # Rule 9: Assert string type.
    assert isinstance(core_id, int), "Core ID must be integer."  # Rule 9: Assert integer core ID.
    log_status = log_trace("Executing harness command on core " + str(core_id) + ": " + cmd_str)  # Trace start.
    assert log_status == True, "Tracing failed."  # Rule 11: Validate return code.
    final_cmd = cmd_str  # Copy original command string.
    if os.name != "nt":  # Check if running on Unix/Linux platform supporting taskset.
        final_cmd = "taskset -c " + str(core_id) + " " + cmd_str  # Prefix command with taskset affinity.
    start_t = time.time()  # Record start wall-clock time.
    proc = subprocess.Popen(final_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)  # Spawn process.
    proc.communicate()  # Wait for process completion.
    end_t = time.time()  # Record end wall-clock time.
    duration = end_t - start_t  # Calculate elapsed duration.
    assert duration >= 0.0, "Duration cannot be negative."  # Rule 9: Assert non-negative duration.
    assert isinstance(duration, float), "Duration must be float."  # Rule 9: Assert float return type.
    return duration  # Return measured duration.

def compute_statistics(timings_list):  # Define function to compute mean and std dev.
    assert isinstance(timings_list, list), "Timings list must be a list."  # Rule 9: Assert list type.
    assert len(timings_list) > 0, "Timings list cannot be empty."  # Rule 9: Assert non-empty list.
    total = 0.0  # Initialize total time accumulator.
    idx = 0  # Initialize loop index.
    max_l = 1000  # Rule 6: Fixed upper bound limit.
    while idx < len(timings_list):  # Loop through timings list.
        if idx >= max_l:  # Check fixed upper bound threshold.
            break  # Break loop to prevent infinite execution.
        total += timings_list[idx]  # Accumulate timing value.
        idx += 1  # Increment index.
    mean_val = total / float(len(timings_list))  # Calculate arithmetic mean.
    var_sum = 0.0  # Initialize variance sum accumulator.
    jdx = 0  # Initialize second index.
    while jdx < len(timings_list):  # Loop for variance calculation.
        if jdx >= max_l:  # Check fixed upper bound threshold.
            break  # Break loop.
        diff = timings_list[jdx] - mean_val  # Compute deviation from mean.
        var_sum += (diff * diff)  # Accumulate squared deviation.
        jdx += 1  # Increment index.
    std_val = math.sqrt(var_sum / float(max(1, len(timings_list) - 1)))  # Compute standard deviation.
    assert mean_val >= 0.0, "Mean cannot be negative."  # Rule 9: Assert valid mean.
    assert std_val >= 0.0, "Std dev cannot be negative."  # Rule 9: Assert valid std dev.
    return {"mean": mean_val, "std_dev": std_val}  # Return statistics dictionary.

def main():  # Main execution function fitting on a single page.
    assert sys.version_info[0] == 2, "Script requires Python 2 environment."  # Rule 1 / Rule 9: Python 2 check.
    assert sys.version_info[1] == 7, "Script requires Python 2.7 environment."  # Rule 9: Python 2.7 check.
    test_cmd = "sleep 0.1"  # Define test benchmark command.
    timings_buf = []  # Initialize static timings buffer list.
    runs = 3  # Set execution run count.
    kdx = 0  # Initialize loop index.
    max_runs = 10  # Rule 6: Fixed upper bound limit.
    while kdx < runs:  # Loop through benchmark runs.
        if kdx >= max_runs:  # Check fixed upper bound threshold.
            break  # Break loop.
        d = execute_command_harness(test_cmd, 0)  # Execute command on core 0.
        timings_buf.append(d)  # Append duration measurement.
        kdx += 1  # Increment index.
    stats = compute_statistics(timings_buf)  # Compute statistical summary.
    assert isinstance(stats, dict), "Stats must be a dictionary."  # Rule 11: Validate return.
    out_lines = []  # Initialize output lines buffer.
    out_lines.append("Unified Benchmark Harness Results:")  # Add header.
    out_lines.append("Command: " + test_cmd)  # Add command line.
    out_lines.append("Mean Duration: " + str(round(stats["mean"] * 1000.0, 2)) + " ms")  # Add mean line.
    out_lines.append("Standard Deviation: " + str(round(stats["std_dev"] * 1000.0, 2)) + " ms")  # Add std dev line.
    f_trace = open("trace_unified.log", "w")  # Open trace log file for writing.
    idx = 0  # Initialize trace loop index.
    while idx < len(TRACE_LOG):  # Loop through trace logs.
        if idx >= 100:  # Check upper bound threshold.
            break  # Break loop.
        f_trace.write(TRACE_LOG[idx] + "\n")  # Write trace log entry.
        idx += 1  # Increment index.
    f_trace.close()  # Close trace file stream.
    f_out = open("output_unified.txt", "w")  # Open output text file.
    jdx = 0  # Initialize output loop index.
    while jdx < len(out_lines):  # Loop through output lines.
        if jdx >= 100:  # Check upper bound threshold.
            break  # Break loop.
        f_out.write(out_lines[jdx] + "\n")  # Write output line.
        jdx += 1  # Increment index.
    f_out.close()  # Close output file stream.
    return 0  # Return zero for successful termination.

if __name__ == "__main__":  # Execution entry point guard.
    status = main()  # Execute main function.
    assert status == 0, "Execution failed."  # Rule 11: Validate status.
