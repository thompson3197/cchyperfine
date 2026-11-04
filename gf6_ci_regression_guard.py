# -*- coding: utf-8 -*-
# Going Further 6: CI performance regression guard and statistical comparison.
import sys  # Import sys module for system operations.

TRACE_LOG = []  # Initialize static list buffer for trace logging statements.

def log_trace(message):  # Define function to record execution trace logs.
    assert isinstance(message, str), "Log message must be a string."  # Rule 9: Assert input is string.
    assert len(message) > 0, "Log message cannot be empty."  # Rule 9: Assert input is non-empty.
    TRACE_LOG.append(message)  # Append message into trace buffer.
    return True  # Rule 11: Explicit return value indicating success.

def check_regression(baseline_mean, current_mean, threshold_pct):  # Define function to check for regression.
    assert isinstance(baseline_mean, (int, float)), "Baseline mean must be numeric."  # Rule 9: Assert numeric baseline.
    assert isinstance(current_mean, (int, float)), "Current mean must be numeric."  # Rule 9: Assert numeric current.
    assert baseline_mean > 0.0, "Baseline mean must be positive."  # Rule 9: Assert positive baseline.
    assert threshold_pct > 0.0, "Threshold percentage must be positive."  # Rule 9: Assert positive threshold.
    log_status = log_trace("Checking regression against baseline: " + str(baseline_mean))  # Trace regression check.
    assert log_status == True, "Tracing failed."  # Rule 11: Validate return code.
    diff_pct = ((current_mean - baseline_mean) / float(baseline_mean)) * 100.0  # Calculate percentage difference.
    is_regression = diff_pct > threshold_pct  # Determine if regression threshold is exceeded.
    res_dict = {"diff_pct": diff_pct, "is_regression": is_regression}  # Package result.
    assert isinstance(res_dict, dict), "Result must be a dictionary."  # Rule 9: Assert dictionary return type.
    assert isinstance(res_dict["is_regression"], bool), "Regression flag must be boolean."  # Rule 9: Assert boolean type.
    return res_dict  # Return result dictionary.

def main():  # Main execution function fitting on a single page.
    assert sys.version_info[0] == 2, "Script requires Python 2 environment."  # Rule 1 / Rule 9: Python 2 check.
    assert sys.version_info[1] == 7, "Script requires Python 2.7 environment."  # Rule 9: Python 2.7 check.
    baseline = 0.100  # Define baseline mean duration in seconds.
    current = 0.125   # Define current run mean duration in seconds.
    threshold = 15.0  # Define allowed regression percentage threshold.
    regression_res = check_regression(baseline, current, threshold)  # Check for performance regression.
    assert isinstance(regression_res, dict), "Result must be dictionary."  # Rule 11: Validate return value.
    out_lines = []  # Initialize output lines buffer.
    out_lines.append("CI Performance Regression Audit:")  # Add header line.
    out_lines.append("Percentage Difference: " + str(round(regression_res["diff_pct"], 2)) + "%")  # Add difference line.
    out_lines.append("Regression Triggered (>15% slower): " + str(regression_res["is_regression"]))  # Add trigger line.
    f_trace = open("trace_gf6.log", "w")  # Open trace file for writing.
    idx = 0  # Initialize trace loop index.
    max_l = 100  # Rule 6: Fixed upper bound limit.
    while idx < len(TRACE_LOG):  # Loop through trace logs.
        if idx >= max_l:  # Check fixed upper bound threshold.
            break  # Break loop.
        f_trace.write(TRACE_LOG[idx] + "\n")  # Write trace log item.
        idx += 1  # Increment index.
    f_trace.close()  # Close trace file stream.
    f_out = open("output_gf6.txt", "w")  # Open output text file for writing.
    jdx = 0  # Initialize output loop index.
    while jdx < len(out_lines):  # Loop through output lines.
        if jdx >= max_l:  # Check fixed upper bound threshold.
            break  # Break loop.
        f_out.write(out_lines[jdx] + "\n")  # Write output line.
        jdx += 1  # Increment index.
    f_out.close()  # Close output file stream.
    if regression_res["is_regression"]:  # Check if performance regression occurred.
        return 1  # Return non-zero exit code to fail CI pipeline.
    return 0  # Return zero for successful termination.

if __name__ == "__main__":  # Execution entry point guard.
    status = main()  # Execute main function.
    if status != 0:  # Check if CI regression guard triggered failure.
        sys.exit(status)  # Exit with status code to signal pipeline failure.
