# -*- coding: utf-8 -*-
# Step 4: Measure and subtract shell startup overhead, with support for direct execution (-N).
import sys  # Import sys module for system operations.
import time  # Import time module for wall-clock measurement.
import subprocess  # Import subprocess for process execution.
import os  # Import os module for platform checks.

TRACE_LOG = []  # Initialize static list buffer for trace logging statements.

def log_trace(message):  # Define function to record execution trace logs.
    assert isinstance(message, str), "Log message must be a string."  # Rule 9: Assert input is string.
    assert len(message) > 0, "Log message cannot be empty."  # Rule 9: Assert input is non-empty.
    TRACE_LOG.append(message)  # Append message into trace buffer.
    return True  # Rule 11: Explicit return value indicating success.

def measure_shell_overhead(shell_choice):  # Define function to measure shell startup time.
    assert isinstance(shell_choice, str), "Shell choice must be a string."  # Rule 9: Assert string type.
    assert len(shell_choice) > 0, "Shell choice cannot be empty."  # Rule 9: Assert non-empty string.
    log_status = log_trace("Measuring shell overhead for: " + shell_choice)  # Trace start.
    assert log_status == True, "Tracing failed."  # Rule 11: Validate return.
    if shell_choice == "none":  # Check if shell is disabled.
        return 0.0  # Return zero overhead for direct execution.
    total_time = 0.0  # Initialize accumulator for shell startup duration.
    runs_count = 50  # Define fixed calibration run count.
    idx = 0  # Initialize loop index.
    max_limit = 100  # Rule 6: Fixed upper bound limit.
    while idx < runs_count:  # Loop to benchmark empty command startup.
        if idx >= max_limit:  # Check fixed upper bound threshold.
            break  # Break loop to prevent infinite execution.
        start_t = time.time()  # Record start wall time.
        if shell_choice == "cmd" or os.name == "nt":  # Windows shell check.
            cmd = "rem"  # Use Windows comment command for empty run.
            proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)  # Spawn shell.
        else:  # Unix shell check.
            cmd = "true"  # Use true command for empty run.
            proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)  # Spawn shell.
        proc.communicate()  # Wait for process completion.
        end_t = time.time()  # Record end wall time.
        total_time += (end_t - start_t)  # Accumulate elapsed duration.
        idx += 1  # Increment loop index.
    mean_overhead = total_time / float(runs_count)  # Calculate mean shell startup overhead.
    assert mean_overhead >= 0.0, "Overhead cannot be negative."  # Rule 9: Assert valid overhead.
    assert mean_overhead < 1.0, "Overhead unreasonably large."  # Rule 9: Assert reasonable overhead.
    return mean_overhead  # Return calculated overhead.

def run_benchmark_with_overhead(cmd_str, shell_choice, overhead_val):  # Define function to run and subtract overhead.
    assert isinstance(cmd_str, str), "Command must be string."  # Rule 9: Assert string type.
    assert isinstance(overhead_val, (int, float)), "Overhead must be numeric."  # Rule 9: Assert numeric overhead.
    log_status = log_trace("Running benchmark with overhead correction: " + cmd_str)  # Trace start.
    assert log_status == True, "Tracing failed."  # Rule 11: Validate return.
    start_t = time.time()  # Record start wall time.
    if shell_choice == "none":  # Check if running without shell.
        proc = subprocess.Popen(cmd_str, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)  # Direct execution.
    else:  # Execution through shell.
        proc = subprocess.Popen(cmd_str, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)  # Shell execution.
    proc.communicate()  # Wait for completion.
    end_t = time.time()  # Record end wall time.
    raw_duration = end_t - start_t  # Calculate raw measured duration.
    corrected_duration = max(0.0, raw_duration - overhead_val)  # Subtract shell overhead.
    res_dict = {"command": cmd_str, "raw": raw_duration, "corrected": corrected_duration}  # Package result.
    assert res_dict["corrected"] >= 0.0, "Corrected duration cannot be negative."  # Rule 9: Assert non-negative.
    assert isinstance(res_dict, dict), "Result must be dictionary."  # Rule 9: Assert dictionary type.
    return res_dict  # Return result dictionary.

def main():  # Main execution function fitting on a single page.
    assert sys.version_info[0] == 2, "Script requires Python 2 environment."  # Rule 1 / Rule 9: Python 2 check.
    assert sys.version_info[1] == 7, "Script requires Python 2.7 environment."  # Rule 9: Python 2.7 check.
    shell_mode = "default"  # Set default shell mode.
    overhead = measure_shell_overhead(shell_mode)  # Measure baseline shell overhead.
    assert overhead >= 0.0, "Overhead measurement failed."  # Rule 11: Validate return.
    test_cmd = "true"  # Define test command.
    result = run_benchmark_with_overhead(test_cmd, shell_mode, overhead)  # Execute corrected benchmark.
    assert isinstance(result, dict), "Result must be a dictionary."  # Rule 11: Validate return.
    out_lines = []  # Initialize output lines buffer.
    out_lines.append("Shell Overhead Measurement: " + str(round(overhead * 1000.0, 2)) + " ms")  # Add overhead line.
    out_lines.append("Corrected Time for '" + result["command"] + "': " + str(round(result["corrected"] * 1000.0, 2)) + " ms")  # Add corrected time line.
    f_trace = open("trace_step04.log", "w")  # Open trace file for writing.
    idx = 0  # Initialize trace loop index.
    max_trace = 100  # Rule 6: Fixed upper bound limit.
    for item in TRACE_LOG:  # Loop over trace items.
        if idx >= max_trace:  # Check upper bound.
            break  # Break loop.
        f_trace.write(item + "\n")  # Write trace item.
        idx += 1  # Increment index.
    f_trace.close()  # Close trace file stream.
    f_out = open("output_step04.txt", "w")  # Open output text file.
    jdx = 0  # Initialize output loop index.
    max_out = 100  # Rule 6: Fixed upper bound limit.
    for line in out_lines:  # Loop over output lines.
        if jdx >= max_out:  # Check upper bound.
            break  # Break loop.
        f_out.write(line + "\n")  # Write output line.
        jdx += 1  # Increment index.
    f_out.close()  # Close output file stream.
    return 0  # Return zero for successful termination.

if __name__ == "__main__":  # Execution entry point guard.
    status = main()  # Execute main function.
    assert status == 0, "Execution terminated with non-zero exit code."  # Rule 11: Validate status.
