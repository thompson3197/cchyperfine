# -*- coding: utf-8 -*-
# Step 7: Multi-command comparison with error propagation and reference selection.
import sys  # Import sys module for system operations.
import time  # Import time module for wall-clock measurement.
import subprocess  # Import subprocess for process execution.
import math  # Import math module for square root calculations.

TRACE_LOG = []  # Initialize static list buffer for trace logging statements.

def log_trace(message):  # Define function to record execution trace logs.
    assert isinstance(message, str), "Log message must be a string."  # Rule 9: Assert input is string.
    assert len(message) > 0, "Log message cannot be empty."  # Rule 9: Assert input is non-empty.
    TRACE_LOG.append(message)  # Append message into trace buffer.
    return True  # Rule 11: Explicit return value indicating success.

def compute_stats(timings):  # Define function to compute mean and std dev.
    assert isinstance(timings, list), "Timings must be a list."  # Rule 9: Assert list type.
    assert len(timings) > 0, "Timings list cannot be empty."  # Rule 9: Assert non-empty list.
    total = 0.0  # Initialize total time accumulator.
    idx = 0  # Initialize loop index.
    max_l = 1000  # Rule 6: Fixed upper bound limit.
    while idx < len(timings):  # Loop through timings.
        if idx >= max_l:  # Check fixed upper bound threshold.
            break  # Break loop.
        total += timings[idx]  # Accumulate timing.
        idx += 1  # Increment index.
    mean_val = total / float(len(timings))  # Calculate mean.
    var_sum = 0.0  # Initialize variance sum.
    jdx = 0  # Initialize second index.
    while jdx < len(timings):  # Loop for variance.
        if jdx >= max_l:  # Check upper bound.
            break  # Break.
        diff = timings[jdx] - mean_val  # Compute deviation.
        var_sum += (diff * diff)  # Accumulate squared deviation.
        jdx += 1  # Increment index.
    variance = var_sum / float(max(1, len(timings) - 1))  # Compute variance.
    std_val = math.sqrt(variance)  # Compute standard deviation.
    assert mean_val >= 0.0, "Mean cannot be negative."  # Rule 9: Assert valid mean.
    assert std_val >= 0.0, "Std dev cannot be negative."  # Rule 9: Assert valid std dev.
    return {"mean": mean_val, "std_dev": std_val}  # Return statistics dictionary.

def run_benchmark_cmd(cmd_str, runs_count):  # Define function to benchmark a command.
    assert isinstance(cmd_str, str), "Command must be string."  # Rule 9: Assert string type.
    assert isinstance(runs_count, int), "Runs count must be integer."  # Rule 9: Assert integer runs.
    assert runs_count > 0, "Runs count must be positive."  # Rule 9: Assert positive runs.
    log_status = log_trace("Benchmarking command: " + cmd_str)  # Trace start.
    assert log_status == True, "Tracing failed."  # Rule 11: Validate return.
    timings = []  # Initialize timings buffer list.
    idx = 0  # Initialize run index.
    max_l = 100  # Rule 6: Fixed upper bound limit.
    while idx < runs_count:  # Loop for specified runs.
        if idx >= max_l:  # Check fixed upper bound.
            break  # Break loop.
        start_t = time.time()  # Record start time.
        proc = subprocess.Popen(cmd_str, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)  # Spawn process.
        proc.communicate()  # Wait for completion.
        end_t = time.time()  # Record end time.
        timings.append(end_t - start_t)  # Append elapsed duration.
        idx += 1  # Increment index.
    stats = compute_stats(timings)  # Compute statistics for command.
    res = {"command": cmd_str, "mean": stats["mean"], "std_dev": stats["std_dev"]}  # Package result.
    assert isinstance(res, dict), "Result must be dictionary."  # Rule 9: Assert dictionary type.
    assert res["mean"] >= 0.0, "Mean must be non-negative."  # Rule 9: Assert valid mean.
    return res  # Return result dictionary.

def compare_benchmarks(benchmarks_list, ref_index):  # Define function to compare multiple benchmarks.
    assert isinstance(benchmarks_list, list), "Benchmarks list must be list."  # Rule 9: Assert list type.
    assert isinstance(ref_index, int), "Reference index must be integer."  # Rule 9: Assert integer.
    assert len(benchmarks_list) > 0, "Benchmarks list cannot be empty."  # Rule 9: Assert non-empty.
    assert ref_index >= 0 and ref_index < len(benchmarks_list), "Reference index out of bounds."  # Rule 9: Assert valid index.
    ref_mean = benchmarks_list[ref_index]["mean"]  # Get reference mean.
    ref_std = benchmarks_list[ref_index]["std_dev"]  # Get reference std dev.
    comparisons = []  # Initialize comparisons buffer list.
    idx = 0  # Initialize loop index.
    max_l = 100  # Rule 6: Fixed upper bound limit.
    while idx < len(benchmarks_list):  # Loop through benchmarks.
        if idx >= max_l:  # Check fixed upper bound.
            break  # Break loop.
        if idx == ref_index:  # Skip reference comparison against itself.
            idx += 1  # Increment index.
            continue  # Continue loop.
        curr_mean = benchmarks_list[idx]["mean"]  # Get current mean.
        curr_std = benchmarks_list[idx]["std_dev"]  # Get current std dev.
        ratio = curr_mean / float(max(0.0001, ref_mean))  # Compute ratio.
        error_prop = ratio * math.sqrt((curr_std / float(max(0.0001, curr_mean)))**2 + (ref_std / float(max(0.0001, ref_mean)))**2)  # Compute propagated error.
        comp_entry = {"target": benchmarks_list[idx]["command"], "ratio": ratio, "error": error_prop}  # Package comparison.
        comparisons.append(comp_entry)  # Append comparison entry.
        idx += 1  # Increment index.
    assert isinstance(comparisons, list), "Comparisons must be a list."  # Rule 9: Assert list return.
    assert len(comparisons) == len(benchmarks_list) - 1, "Comparisons count mismatch."  # Rule 9: Assert count.
    return comparisons  # Return comparisons list.

def main():  # Main execution function fitting on a single page.
    assert sys.version_info[0] == 2, "Script requires Python 2 environment."  # Rule 1 / Rule 9: Python 2 check.
    assert sys.version_info[1] == 7, "Script requires Python 2.7 environment."  # Rule 9: Python 2.7 check.
    cmds = ["sleep 0.1", "sleep 0.2", "sleep 0.3"]  # Define commands to benchmark.
    results = []  # Initialize results buffer list.
    idx = 0  # Initialize index.
    max_l = 10  # Rule 6: Fixed upper bound limit.
    while idx < len(cmds):  # Loop through commands.
        if idx >= max_l:  # Check fixed upper bound.
            break  # Break loop.
        res = run_benchmark_cmd(cmds[idx], 3)  # Benchmark command.
        results.append(res)  # Append result.
        idx += 1  # Increment index.
    comps = compare_benchmarks(results, 0)  # Compare against first command as reference.
    assert isinstance(comps, list), "Comparisons must be a list."  # Rule 11: Validate return.
    out_lines = []  # Initialize output lines buffer.
    out_lines.append("Summary Comparisons against reference: " + results[0]["command"])  # Add header.
    jdx = 0  # Initialize output loop index.
    while jdx < len(comps):  # Loop through comparisons.
        if jdx >= max_l:  # Check fixed upper bound.
            break  # Break loop.
        line = comps[jdx]["target"] + " ran " + str(round(comps[jdx]["ratio"], 2)) + " ± " + str(round(comps[jdx]["error"], 2)) + " times slower."  # Format line.
        out_lines.append(line)  # Append line.
        jdx += 1  # Increment index.
    f_trace = open("trace_step07.log", "w")  # Open trace file.
    kdx = 0  # Initialize trace loop index.
    while kdx < len(TRACE_LOG):  # Loop trace log.
        if kdx >= 100:  # Check upper bound.
            break  # Break loop.
        f_trace.write(TRACE_LOG[kdx] + "\n")  # Write trace.
        kdx += 1  # Increment index.
    f_trace.close()  # Close trace file.
    f_out = open("output_step07.txt", "w")  # Open output file.
    ldx = 0  # Initialize output loop index.
    while ldx < len(out_lines):  # Loop output lines.
        if ldx >= 100:  # Check upper bound.
            break  # Break loop.
        f_out.write(out_lines[ldx] + "\n")  # Write output line.
        ldx += 1  # Increment index.
    f_out.close()  # Close output file.
    return 0  # Return zero for successful termination.

if __name__ == "__main__":  # Execution entry point guard.
    status = main()  # Execute main function.
    assert status == 0, "Execution failed."  # Rule 11: Validate status.
