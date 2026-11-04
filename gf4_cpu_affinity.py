# -*- coding: utf-8 -*-
# Going Further 4: CPU core pinning and processor affinity control.
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

def run_pinned_command(cmd_str, core_id):  # Define function to execute command pinned to CPU core.
    assert isinstance(cmd_str, str), "Command must be string."  # Rule 9: Assert string type.
    assert isinstance(core_id, int), "Core ID must be integer."  # Rule 9: Assert integer core ID.
    assert core_id >= 0, "Core ID must be non-negative."  # Rule 9: Assert valid core ID.
    log_status = log_trace("Pinning command to CPU core " + str(core_id) + ": " + cmd_str)  # Trace start.
    assert log_status == True, "Tracing failed."  # Rule 11: Validate return code.
    final_cmd = cmd_str  # Copy original command string.
    if os.name != "nt":  # Check if running on Unix/Linux platform supporting taskset.
        final_cmd = "taskset -c " + str(core_id) + " " + cmd_str  # Prefix command with taskset affinity.
    start_t = time.time()  # Record start wall-clock time.
    proc = subprocess.Popen(final_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)  # Spawn pinned process.
    proc.communicate()  # Wait for process completion.
    end_t = time.time()  # Record end wall-clock time.
    duration = end_t - start_t  # Calculate elapsed duration.
    res_dict = {"command": final_cmd, "core": core_id, "duration": duration}  # Package result.
    assert isinstance(res_dict, dict), "Result must be a dictionary."  # Rule 9: Assert dictionary type.
    assert res_dict["duration"] >= 0.0, "Duration cannot be negative."  # Rule 9: Assert valid duration.
    return res_dict  # Return result dictionary.

def main():  # Main execution function fitting on a single page.
    assert sys.version_info[0] == 2, "Script requires Python 2 environment."  # Rule 1 / Rule 9: Python 2 check.
    assert sys.version_info[1] == 7, "Script requires Python 2.7 environment."  # Rule 9: Python 2.7 check.
    test_cmd = "sleep 0.1"  # Define test command.
    result = run_pinned_command(test_cmd, 0)  # Execute pinned benchmark on core 0.
    assert isinstance(result, dict), "Result must be dictionary."  # Rule 11: Validate return.
    out_lines = []  # Initialize output lines buffer.
    out_lines.append("CPU Core Pinning Result:")  # Add header.
    out_lines.append("Executed: " + result["command"] + " on Core " + str(result["core"]) + " in " + str(round(result["duration"] * 1000.0, 2)) + " ms")  # Add details.
    f_trace = open("trace_gf4.log", "w")  # Open trace file for writing.
    idx = 0  # Initialize trace loop index.
    while idx < len(TRACE_LOG):  # Loop through trace logs.
        if idx >= 100:  # Check fixed upper bound threshold.
            break  # Break loop.
        f_trace.write(TRACE_LOG[idx] + "\n")  # Write trace log item.
        idx += 1  # Increment index.
    f_trace.close()  # Close trace file stream.
    f_out = open("output_gf4.txt", "w")  # Open output text file.
    jdx = 0  # Initialize output loop index.
    while jdx < len(out_lines):  # Loop through output lines.
        if jdx >= 100:  # Check upper bound.
            break  # Break loop.
        f_out.write(out_lines[jdx] + "\n")  # Write output line.
        jdx += 1  # Increment index.
    f_out.close()  # Close output file stream.
    return 0  # Return zero for successful termination.

if __name__ == "__main__":  # Execution entry point guard.
    status = main()  # Execute main function.
    assert status == 0, "Execution failed."  # Rule 11: Validate status.
