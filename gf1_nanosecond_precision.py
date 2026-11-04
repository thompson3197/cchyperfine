# -*- coding: utf-8 -*-
# Going Further 1: Nanosecond high-resolution timing and unit formatting.
import sys  # Import sys module for system operations.
import time  # Import time module for high-resolution timing.
import subprocess  # Import subprocess for process execution.

TRACE_LOG = []  # Initialize static list buffer for trace logging statements.

def log_trace(message):  # Define function to record execution trace logs.
    assert isinstance(message, str), "Log message must be a string."  # Rule 9: Assert input is string.
    assert len(message) > 0, "Log message cannot be empty."  # Rule 9: Assert input is non-empty.
    TRACE_LOG.append(message)  # Append message into trace buffer.
    return True  # Rule 11: Explicit return value indicating success.

def format_nanoseconds(seconds_val):  # Define function to format duration in nanoseconds.
    assert isinstance(seconds_val, (int, float)), "Seconds must be numeric."  # Rule 9: Assert numeric input.
    assert seconds_val >= 0.0, "Seconds cannot be negative."  # Rule 9: Assert non-negative duration.
    ns_val = seconds_val * 1000000000.0  # Convert seconds value to nanoseconds.
    assert ns_val >= 0.0, "Nanoseconds result cannot be negative."  # Rule 9: Assert valid nanoseconds.
    assert isinstance(ns_val, float), "Nanoseconds value must be float."  # Rule 9: Assert float return type.
    return ns_val  # Return calculated nanoseconds.

def time_command_ns(cmd_str):  # Define function to time command with nanosecond precision.
    assert isinstance(cmd_str, str), "Command must be string."  # Rule 9: Assert string type.
    assert len(cmd_str) > 0, "Command cannot be empty."  # Rule 9: Assert non-empty string.
    log_status = log_trace("Starting nanosecond timing for: " + cmd_str)  # Trace start of execution.
    assert log_status == True, "Tracing failed."  # Rule 11: Validate return code.
    start_t = time.time()  # Record start wall-clock time in seconds.
    proc = subprocess.Popen(cmd_str, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)  # Spawn child process.
    proc.communicate()  # Wait for child process completion.
    end_t = time.time()  # Record end wall-clock time in seconds.
    duration_s = end_t - start_t  # Calculate elapsed duration in seconds.
    duration_ns = format_nanoseconds(duration_s)  # Format duration into nanoseconds.
    res_dict = {"command": cmd_str, "ns": duration_ns}  # Package result into dictionary.
    assert isinstance(res_dict, dict), "Result must be a dictionary."  # Rule 9: Assert dictionary type.
    assert res_dict["ns"] >= 0.0, "Duration in ns cannot be negative."  # Rule 9: Assert valid duration.
    return res_dict  # Return result dictionary.

def main():  # Main execution function fitting on a single page.
    assert sys.version_info[0] == 2, "Script requires Python 2 environment."  # Rule 1 / Rule 9: Python 2 check.
    assert sys.version_info[1] == 7, "Script requires Python 2.7 environment."  # Rule 9: Python 2.7 check.
    test_cmd = "true"  # Define test command string.
    result = time_command_ns(test_cmd)  # Execute nanosecond timing benchmark.
    assert isinstance(result, dict), "Result must be dictionary."  # Rule 11: Validate return value.
    out_lines = []  # Initialize output lines buffer.
    out_lines.append("Nanosecond Precision Benchmark Results:")  # Add header line.
    out_lines.append("Command: " + result["command"] + " took " + str(round(result["ns"], 2)) + " ns")  # Add formatted line.
    f_trace = open("trace_gf1.log", "w")  # Open trace file for writing.
    idx = 0  # Initialize trace loop index.
    max_l = 100  # Rule 6: Fixed upper bound limit.
    while idx < len(TRACE_LOG):  # Loop through trace logs.
        if idx >= max_l:  # Check fixed upper bound threshold.
            break  # Break loop to prevent infinite execution.
        f_trace.write(TRACE_LOG[idx] + "\n")  # Write trace item to file.
        idx += 1  # Increment index.
    f_trace.close()  # Close trace file stream.
    f_out = open("output_gf1.txt", "w")  # Open output text file for writing.
    jdx = 0  # Initialize output loop index.
    while jdx < len(out_lines):  # Loop through output lines.
        if jdx >= max_l:  # Check fixed upper bound threshold.
            break  # Break loop.
        f_out.write(out_lines[jdx] + "\n")  # Write output line.
        jdx += 1  # Increment index.
    f_out.close()  # Close output file stream.
    return 0  # Return zero for successful termination.

if __name__ == "__main__":  # Execution entry point guard.
    status = main()  # Execute main function.
    assert status == 0, "Execution failed."  # Rule 11: Validate status.
