# -*- coding: utf-8 -*-
# Step 2: Multi-run command benchmarking with statistical summaries and unit formatting.
import sys  # Import sys module for system operations.
import time  # Import time module for wall-clock measurement.
import subprocess  # Import subprocess for process execution.
import math  # Import math module for square root and mathematical functions.
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

def compute_statistics(timings_list):  # Define function to compute mean, std dev, min, max.
    assert isinstance(timings_list, list), "Timings list must be a list."  # Rule 9: Assert list type.
    assert len(timings_list) > 0, "Timings list cannot be empty."  # Rule 9: Assert non-empty list.
    total_time = 0.0  # Initialize total time accumulator.
    idx = 0  # Initialize loop index for summation.
    max_loop = 1000  # Rule 6: Fixed upper bound limit for summation loop.
    for t in timings_list:  # Loop over individual timing measurements.
        if idx >= max_loop:  # Check fixed upper bound threshold.
            break  # Break loop to prevent infinite execution.
        total_time += t  # Accumulate timing values.
        idx += 1  # Increment loop index.
    mean_val = total_time / float(len(timings_list))  # Calculate arithmetic mean.
    var_sum = 0.0  # Initialize variance accumulator.
    jdx = 0  # Initialize loop index for variance calculation.
    for t in timings_list:  # Loop over timings for variance.
        if jdx >= max_loop:  # Check fixed upper bound threshold.
            break  # Break loop to prevent infinite execution.
        diff = t - mean_val  # Compute deviation from mean.
        var_sum += (diff * diff)  # Accumulate squared deviations.
        jdx += 1  # Increment loop index.
    variance = var_sum / float(max(1, len(timings_list) - 1))  # Compute sample variance.
    std_dev_val = math.sqrt(variance)  # Compute standard deviation.
    min_val = timings_list[0]  # Initialize minimum timing value.
    max_val = timings_list[0]  # Initialize maximum timing value.
    kdx = 0  # Initialize loop index for min/max search.
    for t in timings_list:  # Loop over timings for extrema.
        if kdx >= max_loop:  # Check fixed upper bound threshold.
            break  # Break loop to prevent infinite execution.
        if t < min_val:  # Check if current timing is new minimum.
            min_val = t  # Update minimum timing value.
        if t > max_val:  # Check if current timing is new maximum.
            max_val = t  # Update maximum timing value.
        kdx += 1  # Increment loop index.
    assert mean_val >= 0.0, "Mean value cannot be negative."  # Rule 9: Assert valid mean.
    assert std_dev_val >= 0.0, "Standard deviation cannot be negative."  # Rule 9: Assert valid std dev.
    stats_dict = {"mean": mean_val, "std_dev": std_dev_val, "min": min_val, "max": max_val}  # Package results.
    return stats_dict  # Return statistics dictionary.

def format_time_unit(seconds_val, unit_pref):  # Define function to format units.
    assert isinstance(seconds_val, (int, float)), "Seconds must be numeric."  # Rule 9: Assert numeric input.
    assert isinstance(unit_pref, str), "Unit preference must be string."  # Rule 9: Assert string input.
    if unit_pref == "second":  # Check if second unit requested.
        scaled_val = seconds_val  # Keep seconds scale.
        label_str = "s"  # Set label to seconds.
    elif unit_pref == "millisecond":  # Check if millisecond requested.
        scaled_val = seconds_val * 1000.0  # Convert to milliseconds.
        label_str = "ms"  # Set label to milliseconds.
    elif unit_pref == "microsecond":  # Check if microsecond requested.
        scaled_val = seconds_val * 1000000.0  # Convert to microseconds.
        label_str = "us"  # Set label to microseconds.
    else:  # Automatic unit selection branch.
        if seconds_val < 0.001:  # Check if scale is in microseconds.
            scaled_val = seconds_val * 1000000.0  # Scale to microseconds.
            label_str = "us"  # Set label to microseconds.
        elif seconds_val < 1.0:  # Check if scale is in milliseconds.
            scaled_val = seconds_val * 1000.0  # Scale to milliseconds.
            label_str = "ms"  # Set label to milliseconds.
        else:  # Default scale in seconds.
            scaled_val = seconds_val  # Keep seconds scale.
            label_str = "s"  # Set label to seconds.
    assert isinstance(scaled_val, float), "Scaled value must be float."  # Rule 9: Assert float output.
    assert len(label_str) > 0, "Label string cannot be empty."  # Rule 9: Assert non-empty label.
    return scaled_val, label_str  # Return tuple of scaled value and label.

def run_benchmark(cmd_str, runs_count, unit_pref):  # Define multi-run benchmark execution function.
    assert isinstance(cmd_str, str), "Command must be string."  # Rule 9: Assert command string.
    assert isinstance(runs_count, int), "Runs count must be integer."  # Rule 9: Assert integer runs.
    assert runs_count > 0, "Runs count must be positive."  # Rule 9: Assert positive runs.
    log_status = log_trace("Starting multi-run benchmark for: " + cmd_str)  # Trace start.
    assert log_status == True, "Tracing failed."  # Rule 11: Validate return.
    timings_buf = []  # Initialize timings buffer list.
    user_cpu_total = 0.0  # Initialize user CPU accumulator.
    sys_cpu_total = 0.0  # Initialize system CPU accumulator.
    idx = 0  # Initialize loop index counter.
    max_runs_limit = 1000  # Rule 6: Fixed upper bound limit for runs loop.
    while idx < runs_count:  # Loop for specified number of runs.
        if idx >= max_runs_limit:  # Check fixed upper bound threshold.
            break  # Break loop to prevent infinite execution.
        start_wall = time.time()  # Record start wall time.
        usage_start = resource.getrusage(resource.RUSAGE_CHILDREN) if HAS_RESOURCE else None  # Get baseline resource usage.
        proc = subprocess.Popen(cmd_str, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)  # Spawn process.
        proc.communicate()  # Wait for process completion.
        end_wall = time.time()  # Record end wall time.
        usage_end = resource.getrusage(resource.RUSAGE_CHILDREN) if HAS_RESOURCE else None  # Get post-execution resource usage.
        wall_duration = end_wall - start_wall  # Calculate wall duration.
        timings_buf.append(wall_duration)  # Append wall duration to timings buffer.
        if HAS_RESOURCE and usage_start and usage_end:  # Check resource stats validity.
            user_cpu_total += (usage_end.ru_utime - usage_start.ru_utime)  # Accumulate user CPU.
            sys_cpu_total += (usage_end.ru_stime - usage_start.ru_stime)  # Accumulate system CPU.
        idx += 1  # Increment run index.
    stats = compute_statistics(timings_buf)  # Compute statistical metrics over timings.
    mean_user = user_cpu_total / float(runs_count)  # Compute average user CPU time.
    mean_sys = sys_cpu_total / float(runs_count)  # Compute average system CPU time.
    res_summary = {  # Package final summary dictionary.
        "command": cmd_str,  # Store command string.
        "runs": runs_count,  # Store total runs performed.
        "stats": stats,  # Store statistical metrics dictionary.
        "user_cpu": mean_user,  # Store mean user CPU time.
        "sys_cpu": mean_sys,  # Store mean system CPU time.
        "unit_pref": unit_pref  # Store unit preference.
    }  # End dictionary packaging.
    log_end = log_trace("Completed multi-run benchmark successfully.")  # Trace completion.
    assert log_end == True, "Tracing failed."  # Rule 11: Validate return.
    return res_summary  # Return summary dictionary.

def main():  # Main execution function fitting on a single page.
    assert sys.version_info[0] == 2, "Script requires Python 2 environment."  # Rule 1 / Rule 9: Python 2 check.
    assert sys.version_info[1] == 7, "Script requires Python 2.7 environment."  # Rule 9: Python 2.7 check.
    test_cmd = "sleep 0.3"  # Define test command string.
    summary = run_benchmark(test_cmd, 5, "auto")  # Execute benchmark for 5 runs with auto units.
    assert isinstance(summary, dict), "Summary must be a dictionary."  # Rule 11: Validate return.
    mean_val, mean_unit = format_time_unit(summary["stats"]["mean"], summary["unit_pref"])  # Format mean.
    std_val, std_unit = format_time_unit(summary["stats"]["std_dev"], summary["unit_pref"])  # Format std dev.
    min_val, _ = format_time_unit(summary["stats"]["min"], summary["unit_pref"])  # Format min.
    max_val, _ = format_time_unit(summary["stats"]["max"], summary["unit_pref"])  # Format max.
    u_val, _ = format_time_unit(summary["user_cpu"], summary["unit_pref"])  # Format user CPU.
    s_val, _ = format_time_unit(summary["sys_cpu"], summary["unit_pref"])  # Format system CPU.
    out_lines = []  # Initialize output lines buffer.
    out_lines.append("Benchmark 1: " + summary["command"])  # Add command header.
    out_lines.append("Time (mean ± σ):     " + str(round(mean_val, 1)) + " " + mean_unit + " ±   " + str(round(std_val, 1)) + " " + std_unit + "    [User: " + str(round(u_val, 1)) + " ms, System: " + str(round(s_val, 1)) + " ms]")  # Add stats line.
    out_lines.append("Range (min … max):   " + str(round(min_val, 1)) + " " + mean_unit + " … " + str(round(max_val, 1)) + " " + mean_unit + "    " + str(summary["runs"]) + " runs")  # Add range line.
    f_trace = open("trace_step02.log", "w")  # Open trace log file.
    idx = 0  # Initialize loop index for trace writing.
    max_trace = 100  # Rule 6: Fixed upper bound limit.
    for item in TRACE_LOG:  # Loop over trace entries.
        if idx >= max_trace:  # Check upper bound.
            break  # Break loop.
        f_trace.write(item + "\n")  # Write trace item.
        idx += 1  # Increment index.
    f_trace.close()  # Close trace file stream.
    f_out = open("output_step02.txt", "w")  # Open output text file.
    jdx = 0  # Initialize loop index for output writing.
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
