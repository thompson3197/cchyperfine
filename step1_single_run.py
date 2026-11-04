# -*- coding: utf-8 -*-
# Step 1 corrected: Time a single run with cross-platform fallback for resource.
import sys  # Import sys module for system operations.
import time  # Import time module for wall-clock measurement.
import subprocess  # Import subprocess for process execution.
try:  # Try block to import Unix resource module safely.
    import resource  # Import resource module for process CPU stats.
    HAS_RESOURCE = True  # Set flag indicating resource module availability.
except ImportError:  # Catch import error on Windows platforms.
    HAS_RESOURCE = False  # Set flag indicating resource module is missing.

TRACE_LOG = []  # Initialize static list buffer for trace logging statements.

def log_trace(message):  # Define function to record execution trace logs.
    assert isinstance(message, str), "Log message must be a string."  # Rule 9: Assert input is string.
    assert len(message) > 0, "Log message cannot be empty."  # Rule 9: Assert input is non-empty.
    TRACE_LOG.append(message)  # Append message into trace buffer.
    return True  # Rule 11: Explicit return value indicating success.

def time_command(cmd_str):  # Define short function to execute and time a command.
    assert isinstance(cmd_str, str), "Command must be a valid string."  # Rule 9: Assert string parameter.
    assert len(cmd_str) > 0, "Command string cannot be empty."  # Rule 9: Assert non-empty command.
    log_status = log_trace("Preparing execution for: " + cmd_str)  # Trace execution start.
    assert log_status == True, "Tracing failed."  # Rule 11: Validate return code.
    start_wall = time.time()  # Record start wall-clock time in seconds.
    if HAS_RESOURCE:  # Check if resource module is available on platform.
        usage_start = resource.getrusage(resource.RUSAGE_CHILDREN)  # Query child usage baseline.
    else:  # Fallback branch for platforms lacking resource module.
        usage_start = None  # Assign None when resource stats unavailable.
    proc = subprocess.Popen(cmd_str, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)  # Spawn child process.
    stdout_data, stderr_data = proc.communicate()  # Wait for completion and read output.
    rc = proc.returncode  # Extract process return code.
    end_wall = time.time()  # Record end wall-clock time in seconds.
    if HAS_RESOURCE:  # Check if resource module is available.
        usage_end = resource.getrusage(resource.RUSAGE_CHILDREN)  # Query child usage post-execution.
    else:  # Fallback branch when resource unavailable.
        usage_end = None  # Assign None when resource stats unavailable.
    wall_time = end_wall - start_wall  # Calculate total elapsed wall-clock duration.
    if HAS_RESOURCE and usage_start and usage_end:  # Check if valid resource metrics exist.
        user_cpu = usage_end.ru_utime - usage_start.ru_utime  # Calculate user CPU time.
        sys_cpu = usage_end.ru_stime - usage_start.ru_stime  # Calculate system CPU time.
    else:  # Fallback when resource metrics cannot be measured.
        user_cpu = 0.0  # Default user CPU time to zero.
        sys_cpu = 0.0  # Default system CPU time to zero.
    res_dict = {  # Construct fixed structure result dictionary.
        "command": cmd_str,  # Store evaluated command string.
        "return_code": rc,  # Store child process exit code.
        "wall_time": wall_time,  # Store wall-clock duration.
        "user_cpu": user_cpu,  # Store user CPU time.
        "sys_cpu": sys_cpu  # Store system CPU time.
    }  # End dictionary construction.
    log_end = log_trace("Completed timing with return code: " + str(rc))  # Trace completion.
    assert log_end == True, "Tracing failed."  # Rule 11: Validate return code.
    return res_dict  # Return calculated result dictionary.

def main():  # Main execution function fitting on a single page.
    assert sys.version_info[0] == 2, "Script requires Python 2 environment."  # Rule 1 / Rule 9: Python 2 check.
    assert sys.version_info[1] == 7, "Script requires Python 2.7 environment."  # Rule 9: Python 2.7 check.
    test_cmd = "echo hello | wc -c"  # Define command string for testing.
    result = time_command(test_cmd)  # Invoke timing function for benchmark command.
    assert isinstance(result, dict), "Result must be a dictionary."  # Rule 11: Validate return value.
    out_lines = []  # Initialize output lines buffer.
    out_lines.append("Benchmark Result for: " + result["command"])  # Add command header.
    out_lines.append("Elapsed Time (Wall): " + str(round(result["wall_time"] * 1000.0, 2)) + " ms")  # Format wall time.
    out_lines.append("User CPU Time: " + str(round(result["user_cpu"] * 1000.0, 2)) + " ms")  # Format user CPU.
    out_lines.append("System CPU Time: " + str(round(result["sys_cpu"] * 1000.0, 2)) + " ms")  # Format system CPU.
    f_trace = open("trace_step01.log", "w")  # Open trace file for writing.
    idx = 0  # Initialize index variable for loop bound check.
    max_trace_items = 100  # Rule 6: Fixed upper bound loop limit.
    for item in TRACE_LOG:  # Loop over trace list items.
        if idx >= max_trace_items:  # Check fixed upper limit threshold.
            break  # Break to prevent runaway execution.
        f_trace.write(item + "\n")  # Write line to trace log file.
        idx += 1  # Increment loop index variable.
    f_trace.close()  # Close trace output file stream.
    f_out = open("output_step01.txt", "w")  # Open primary output text file.
    jdx = 0  # Initialize loop index for output writing.
    max_out_items = 100  # Rule 6: Fixed upper bound limit.
    for line in out_lines:  # Loop over output content lines.
        if jdx >= max_out_items:  # Check fixed upper limit threshold.
            break  # Break loop if upper bound met.
        f_out.write(line + "\n")  # Write formatted result line to file.
        jdx += 1  # Increment loop index.
    f_out.close()  # Close output file stream.
    return 0  # Return zero for successful script termination.

if __name__ == "__main__":  # Execution entry point guard.
    status = main()  # Execute main logic.
    assert status == 0, "Execution terminated with non-zero exit code."  # Rule 11: Verify return status.
