# -*- coding: utf-8 -*-
# Going Further 2: Peak memory usage profiling during process execution.
import sys  # Import sys module for system operations.
import time  # Import time module for wall-clock measurement.
import subprocess  # Import subprocess for process execution.
try:  # Try block to import Unix resource module safely.
    import resource  # Import resource module for process memory stats.
    HAS_RESOURCE = True  # Set flag indicating resource module availability.
except ImportError:  # Catch import error on Windows platforms.
    HAS_RESOURCE = False  # Set flag indicating resource module is missing.

TRACE_LOG = []  # Initialize static list buffer for trace logging statements.

def log_trace(message):  # Define function to record execution trace logs.
    assert isinstance(message, str), "Log message must be a string."  # Rule 9: Assert input is string.
    assert len(message) > 0, "Log message cannot be empty."  # Rule 9: Assert input is non-empty.
    TRACE_LOG.append(message)  # Append message into trace buffer.
    return True  # Rule 11: Explicit return value indicating success.

def profile_memory(cmd_str):  # Define function to profile peak memory usage.
    assert isinstance(cmd_str, str), "Command must be string."  # Rule 9: Assert string type.
    assert len(cmd_str) > 0, "Command cannot be empty."  # Rule 9: Assert non-empty string.
    log_status = log_trace("Profiling memory for command: " + cmd_str)  # Trace start.
    assert log_status == True, "Tracing failed."  # Rule 11: Validate return code.
    start_t = time.time()  # Record start wall-clock time.
    proc = subprocess.Popen(cmd_str, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)  # Spawn child process.
    proc.communicate()  # Wait for process completion.
    end_t = time.time()  # Record end wall-clock time.
    peak_rss = 0.0  # Initialize peak RSS variable.
    if HAS_RESOURCE:  # Check if resource statistics are supported on platform.
        usage = resource.getrusage(resource.RUSAGE_CHILDREN)  # Query child resource usage.
        peak_rss = float(usage.ru_maxrss)  # Extract max resident set size.
        if sys.platform == "darwin":  # Check if platform is macOS.
            peak_rss = peak_rss / 1024.0  # Convert macOS bytes to kilobytes.
    res_dict = {"command": cmd_str, "duration": end_t - start_t, "peak_rss_kb": peak_rss}  # Package result.
    assert isinstance(res_dict, dict), "Result must be a dictionary."  # Rule 9: Assert dictionary type.
    assert res_dict["peak_rss_kb"] >= 0.0, "Peak RSS cannot be negative."  # Rule 9: Assert valid RSS.
    return res_dict  # Return result dictionary.

def main():  # Main execution function fitting on a single page.
    assert sys.version_info[0] == 2, "Script requires Python 2 environment."  # Rule 1 / Rule 9: Python 2 check.
    assert sys.version_info[1] == 7, "Script requires Python 2.7 environment."  # Rule 9: Python 2.7 check.
    test_cmd = "python -c \"print('Hello Memory')\""  # Define test command.
    result = profile_memory(test_cmd)  # Execute memory profiling.
    assert isinstance(result, dict), "Result must be dictionary."  # Rule 11: Validate return.
    out_lines = []  # Initialize output lines buffer.
    out_lines.append("Memory Profiling Results for: " + result["command"])  # Add header.
    out_lines.append("Peak Resident Set Size (RSS): " + str(round(result["peak_rss_kb"], 2)) + " KB")  # Add RSS line.
    f_trace = open("trace_gf2.log", "w")  # Open trace file for writing.
    idx = 0  # Initialize trace loop index.
    while idx < len(TRACE_LOG):  # Loop through trace logs.
        if idx >= 100:  # Check fixed upper bound threshold.
            break  # Break loop.
        f_trace.write(TRACE_LOG[idx] + "\n")  # Write trace log item.
        idx += 1  # Increment index.
    f_trace.close()  # Close trace file stream.
    f_out = open("output_gf2.txt", "w")  # Open output text file.
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
