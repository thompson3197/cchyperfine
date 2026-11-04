# -*- coding: utf-8 -*-
# Step 6: Failure detection, timing warnings, MAD outliers, and cold cache analysis.
import sys  # Import sys module for system operations.
import time  # Import time module for wall-clock measurement.
import subprocess  # Import subprocess for process execution.
import math  # Import math module for mathematical calculations.

TRACE_LOG = []  # Initialize static list buffer for trace logging statements.

def log_trace(message):  # Define function to record execution trace logs.
    assert isinstance(message, str), "Log message must be a string."  # Rule 9: Assert input is string.
    assert len(message) > 0, "Log message cannot be empty."  # Rule 9: Assert input is non-empty.
    TRACE_LOG.append(message)  # Append message into trace buffer.
    return True  # Rule 11: Explicit return value indicating success.

def compute_median(timings_list):  # Define function to calculate median of a list.
    assert isinstance(timings_list, list), "Timings list must be a list."  # Rule 9: Assert list type.
    assert len(timings_list) > 0, "Timings list cannot be empty."  # Rule 9: Assert non-empty list.
    sorted_list = sorted(timings_list)  # Sort list elements in ascending order.
    length = len(sorted_list)  # Get length of sorted list.
    mid = length // 2  # Find middle index.
    if length % 2 == 1:  # Check if length is odd.
        med_val = sorted_list[mid]  # Take middle element for odd length.
    else:  # Branch for even length list.
        med_val = (sorted_list[mid - 1] + sorted_list[mid]) / 2.0  # Average two middle elements.
    assert isinstance(med_val, (int, float)), "Median must be numeric."  # Rule 9: Assert numeric median.
    assert med_val >= 0.0, "Median cannot be negative."  # Rule 9: Assert non-negative median.
    return med_val  # Return calculated median value.

def detect_outliers_mad(timings_list):  # Define function to detect outliers using MAD.
    assert isinstance(timings_list, list), "Timings list must be a list."  # Rule 9: Assert list type.
    assert len(timings_list) > 0, "Timings list cannot be empty."  # Rule 9: Assert non-empty list.
    median_val = compute_median(timings_list)  # Compute median of timings.
    abs_devs = []  # Initialize list for absolute deviations.
    idx = 0  # Initialize loop index.
    max_loop = 1000  # Rule 6: Fixed upper bound limit.
    while idx < len(timings_list):  # Loop through timings.
        if idx >= max_loop:  # Check fixed upper bound threshold.
            break  # Break loop to prevent infinite execution.
        dev = abs(timings_list[idx] - median_val)  # Calculate absolute deviation.
        abs_devs.append(dev)  # Append absolute deviation.
        idx += 1  # Increment loop index.
    mad_val = compute_median(abs_devs)  # Compute median absolute deviation (MAD).
    outliers_list = []  # Initialize list for outlier flags or indices.
    jdx = 0  # Initialize second loop index.
    while jdx < len(timings_list):  # Loop through timings again for outliers.
        if jdx >= max_loop:  # Check fixed upper bound threshold.
            break  # Break loop.
        if mad_val > 0.0:  # Check if MAD is non-zero.
            modified_z = 0.6745 * (timings_list[jdx] - median_val) / mad_val  # Calculate modified Z-score.
            if abs(modified_z) > 3.5:  # Check if Z-score exceeds outlier threshold.
                outliers_list.append(jdx)  # Record outlier index.
        jdx += 1  # Increment second index.
    assert isinstance(outliers_list, list), "Outliers result must be a list."  # Rule 9: Assert list return.
    assert isinstance(mad_val, (int, float)), "MAD must be numeric."  # Rule 9: Assert numeric MAD.
    return outliers_list, mad_val  # Return outliers list and MAD value.

def run_benchmark_step6(cmd_str, ignore_failure):  # Define step 6 execution function.
    assert isinstance(cmd_str, str), "Command must be string."  # Rule 9: Assert string type.
    assert isinstance(ignore_failure, bool), "Ignore failure must be boolean."  # Rule 9: Assert boolean.
    log_status = log_trace("Running benchmark step 6 for: " + cmd_str)  # Trace start.
    assert log_status == True, "Tracing failed."  # Rule 11: Validate return.
    warnings_buf = []  # Initialize static warnings buffer.
    timings_buf = []  # Initialize timings buffer.
    runs_count = 5  # Set fixed runs count for test.
    idx = 0  # Initialize loop index.
    max_limit = 100  # Rule 6: Fixed upper bound limit.
    while idx < runs_count:  # Loop for benchmark runs.
        if idx >= max_limit:  # Check fixed upper bound threshold.
            break  # Break loop.
        start_t = time.time()  # Record start time.
        proc = subprocess.Popen(cmd_str, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)  # Spawn process.
        proc.communicate()  # Wait for completion.
        rc = proc.returncode  # Extract exit code.
        end_t = time.time()  # Record end time.
        if idx == 0 and rc != 0:  # Check if first run failed.
            if not ignore_failure:  # Check if failure should abort.
                log_fail = log_trace("Command failed with exit code: " + str(rc))  # Trace failure.
                assert log_fail == True, "Tracing failed."  # Rule 11: Validate return.
                return {"success": False, "error": "Non-zero exit code: " + str(rc), "warnings": warnings_buf}  # Return failure.
            else:  # Branch when ignoring failure.
                warnings_buf.append("Warning: Ignoring non-zero exit code.")  # Append warning.
        timings_buf.append(end_t - start_t)  # Append timing measurement.
        idx += 1  # Increment index.
    mean_time = sum(timings_buf) / float(len(timings_buf))  # Compute mean time.
    if mean_time < 0.005:  # Check if execution is extremely fast (< 5ms).
        warnings_buf.append("Warning: Command takes less than 5ms; result may be inaccurate. Consider using -N.")  # Append fast warning.
    if len(timings_buf) > 1 and timings_buf[0] > (2.0 * timings_buf[1]):  # Check slow first run (cold cache).
        warnings_buf.append("Warning: First run was significantly slower than subsequent runs (cold cache signature). Consider using --warmup or --prepare.")  # Append cache warning.
    outliers, mad_val = detect_outliers_mad(timings_buf)  # Detect statistical outliers using MAD.
    if len(outliers) > 0:  # Check if outliers were detected.
        warnings_buf.append("Warning: Statistical outliers detected. Consider running on a quiet machine and using --warmup/--prepare.")  # Append outlier warning.
    res_dict = {"success": True, "timings": timings_buf, "warnings": warnings_buf, "mad": mad_val}  # Package result.
    assert isinstance(res_dict, dict), "Result must be a dictionary."  # Rule 9: Assert dictionary type.
    assert len(res_dict["warnings"]) == len(warnings_buf), "Warnings count must match."  # Rule 9: Assert count match.
    return res_dict  # Return result dictionary.

def main():  # Main execution function fitting on a single page.
    assert sys.version_info[0] == 2, "Script requires Python 2 environment."  # Rule 1 / Rule 9: Python 2 check.
    assert sys.version_info[1] == 7, "Script requires Python 2.7 environment."  # Rule 9: Python 2.7 check.
    test_cmd = "true"  # Define test command.
    result = run_benchmark_step6(test_cmd, True)  # Execute step 6 benchmark.
    assert isinstance(result, dict), "Result must be a dictionary."  # Rule 11: Validate return.
    out_lines = []  # Initialize output lines buffer.
    out_lines.append("Step 6 Benchmark Completed for: " + test_cmd)  # Add header.
    for w in result["warnings"]:  # Loop through warnings.
        out_lines.append(w)  # Append warning line.
    f_trace = open("trace_step06.log", "w")  # Open trace file.
    idx = 0  # Initialize index.
    max_t = 100  # Fixed upper bound.
    for item in TRACE_LOG:  # Loop trace log.
        if idx >= max_t:  # Check upper bound.
            break  # Break.
        f_trace.write(item + "\n")  # Write trace.
        idx += 1  # Increment.
    f_trace.close()  # Close trace file.
    f_out = open("output_step06.txt", "w")  # Open output file.
    jdx = 0  # Initialize index.
    max_o = 100  # Fixed upper bound.
    for line in out_lines:  # Loop output lines.
        if jdx >= max_o:  # Check upper bound.
            break  # Break.
        f_out.write(line + "\n")  # Write line.
        jdx += 1  # Increment.
    f_out.close()  # Close output file.
    return 0  # Return zero.

if __name__ == "__main__":  # Execution entry point guard.
    status = main()  # Execute main.
    assert status == 0, "Execution failed."  # Rule 11: Validate status.
