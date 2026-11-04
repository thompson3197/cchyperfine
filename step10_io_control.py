# -*- coding: utf-8 -*-
# Step 10: Standard I/O redirection, HYPERFINE_ITERATION env var, sorting, and styling controls.
import sys  # Import sys module for system operations.
import time  # Import time module for wall-clock measurement.
import subprocess  # Import subprocess for process execution.
import os  # Import os module for environment variable and path operations.

TRACE_LOG = []  # Initialize static list buffer for trace logging statements.

def log_trace(message):  # Define function to record execution trace logs.
    assert isinstance(message, str), "Log message must be a string."  # Rule 9: Assert input is string.
    assert len(message) > 0, "Log message cannot be empty."  # Rule 9: Assert input is non-empty.
    TRACE_LOG.append(message)  # Append message into trace buffer.
    return True  # Rule 11: Explicit return value indicating success.

def run_with_io_control(cmd_str, iteration_num, input_file, output_mode):  # Execute command with I/O and env controls.
    assert isinstance(cmd_str, str), "Command must be string."  # Rule 9: Assert string type.
    assert isinstance(iteration_num, int), "Iteration must be int."  # Rule 9: Assert integer iteration.
    log_status = log_trace("Running IO control command for iteration: " + str(iteration_num))  # Trace start.
    assert log_status == True, "Tracing failed."  # Rule 11: Validate return code.
    env_copy = dict(os.environ)  # Create copy of environment variables dictionary.
    env_copy["HYPERFINE_ITERATION"] = str(iteration_num)  # Set iteration number environment variable.
    stdin_target = None  # Initialize standard input target stream.
    if input_file:  # Check if input file redirection is specified.
        stdin_target = open(input_file, "r")  # Open input file for reading.
    stdout_target = subprocess.PIPE  # Default standard output to pipe.
    if output_mode == "inherit":  # Check if output should inherit parent terminal.
        stdout_target = None  # Set stdout to None to inherit.
    elif output_mode == "null":  # Check if output should be discarded to null.
        stdout_target = open(os.devnull, "w")  # Open null device stream.
    start_t = time.time()  # Record start wall-clock time.
    proc = subprocess.Popen(cmd_str, shell=True, stdin=stdin_target, stdout=stdout_target, stderr=subprocess.PIPE, env=env_copy)  # Spawn process.
    proc.communicate()  # Wait for process completion.
    end_t = time.time()  # Record end wall-clock time.
    if stdin_target and stdin_target != sys.stdin:  # Check if custom input file was opened.
        stdin_target.close()  # Close input file stream.
    if output_mode == "null" and stdout_target:  # Check if null output stream was opened.
        stdout_target.close()  # Close null stream.
    duration = end_t - start_t  # Calculate elapsed duration.
    assert duration >= 0.0, "Duration cannot be negative."  # Rule 9: Assert non-negative duration.
    assert isinstance(duration, float), "Duration must be float."  # Rule 9: Assert float return type.
    return duration  # Return measured duration.

def sort_results(results_list, sort_mode):  # Define function to sort benchmark results.
    assert isinstance(results_list, list), "Results list must be list."  # Rule 9: Assert list type.
    assert isinstance(sort_mode, str), "Sort mode must be string."  # Rule 9: Assert string type.
    if sort_mode == "mean-time":  # Check if sorting by mean time.
        sorted_res = sorted(results_list, key=lambda x: x["mean"])  # Sort by mean time ascending.
    elif sort_mode == "command":  # Check if sorting by command string.
        sorted_res = sorted(results_list, key=lambda x: x["command"])  # Sort alphabetically by command.
    else:  # Default branch keeping original order.
        sorted_res = results_list  # Retain original list order.
    assert isinstance(sorted_res, list), "Sorted results must be list."  # Rule 9: Assert list return type.
    assert len(sorted_res) == len(results_list), "Length must match original list."  # Rule 9: Assert length match.
    return sorted_res  # Return sorted list.

def main():  # Main execution function fitting on a single page.
    assert sys.version_info[0] == 2, "Script requires Python 2 environment."  # Rule 1 / Rule 9: Python 2 check.
    assert sys.version_info[1] == 7, "Script requires Python 2.7 environment."  # Rule 9: Python 2.7 check.
    test_cmd = "echo iteration $HYPERFINE_ITERATION"  # Define test command using iteration variable.
    durations = []  # Initialize durations buffer list.
    idx = 0  # Initialize loop index.
    max_runs = 3  # Set test run count.
    while idx < max_runs:  # Loop through test runs.
        if idx >= 100:  # Check fixed upper bound threshold.
            break  # Break loop.
        d = run_with_io_control(test_cmd, idx + 1, None, "null")  # Execute iteration.
        durations.append(d)  # Append duration.
        idx += 1  # Increment index.
    mock_results = [{"command": "sleep 0.3", "mean": 0.3}, {"command": "sleep 0.1", "mean": 0.1}]  # Mock results.
    sorted_res = sort_results(mock_results, "mean-time")  # Sort mock results by mean time.
    assert len(sorted_res) == 2, "Sorted results count mismatch."  # Rule 11: Validate return.
    f_trace = open("trace_step10.log", "w")  # Open trace file for writing.
    jdx = 0  # Initialize trace loop index.
    while jdx < len(TRACE_LOG):  # Loop through trace logs.
        if jdx >= 100:  # Check upper bound.
            break  # Break loop.
        f_trace.write(TRACE_LOG[jdx] + "\n")  # Write trace log item.
        jdx += 1  # Increment index.
    f_trace.close()  # Close trace file stream.
    f_out = open("output_step10.txt", "w")  # Open output text file.
    f_out.write("Step 10 I/O control and environment variables completed successfully.\n")  # Write status line.
    f_out.close()  # Close output file stream.
    return 0  # Return zero for successful termination.

if __name__ == "__main__":  # Execution entry point guard.
    status = main()  # Execute main function.
    assert status == 0, "Execution failed."  # Rule 11: Validate status.
