# -*- coding: utf-8 -*-
# Going Further 3: System environment auditor for load averages and variance checks.
import sys  # Import sys module for system operations.
import os  # Import os module for platform inspection.

TRACE_LOG = []  # Initialize static list buffer for trace logging statements.

def log_trace(message):  # Define function to record execution trace logs.
    assert isinstance(message, str), "Log message must be a string."  # Rule 9: Assert input is string.
    assert len(message) > 0, "Log message cannot be empty."  # Rule 9: Assert input is non-empty.
    TRACE_LOG.append(message)  # Append message into trace buffer.
    return True  # Rule 11: Explicit return value indicating success.

def audit_system_environment():  # Define function to audit host system stability.
    log_status = log_trace("Starting system environment audit.")  # Trace audit start.
    assert log_status == True, "Tracing failed."  # Rule 11: Validate return code.
    load_avg = (0.0, 0.0, 0.0)  # Initialize default load averages tuple.
    if hasattr(os, "getloadavg"):  # Check if getloadavg is supported by platform.
        load_avg = os.getloadavg()  # Retrieve system load averages.
    warnings_list = []  # Initialize warnings list buffer.
    if load_avg[0] > 2.0:  # Check if 1-minute load average is high.
        warnings_list.append("Warning: High CPU load average detected (" + str(load_avg[0]) + "). Benchmarks may be noisy.")  # Append warning.
    audit_report = {"load_avg": load_avg, "warnings": warnings_list}  # Package audit report.
    assert isinstance(audit_report, dict), "Report must be a dictionary."  # Rule 9: Assert dictionary return type.
    assert isinstance(audit_report["warnings"], list), "Warnings must be a list."  # Rule 9: Assert list type.
    return audit_report  # Return audit report dictionary.

def main():  # Main execution function fitting on a single page.
    assert sys.version_info[0] == 2, "Script requires Python 2 environment."  # Rule 1 / Rule 9: Python 2 check.
    assert sys.version_info[1] == 7, "Script requires Python 2.7 environment."  # Rule 9: Python 2.7 check.
    report = audit_system_environment()  # Execute environment audit.
    assert isinstance(report, dict), "Report must be dictionary."  # Rule 11: Validate return value.
    out_lines = []  # Initialize output lines buffer.
    out_lines.append("System Environment Audit Report:")  # Add header line.
    out_lines.append("Load Averages (1m, 5m, 15m): " + str(report["load_avg"]))  # Add load average line.
    idx = 0  # Initialize loop index for warnings.
    max_l = 100  # Rule 6: Fixed upper bound limit.
    while idx < len(report["warnings"]):  # Loop through warnings list.
        if idx >= max_l:  # Check fixed upper bound threshold.
            break  # Break loop.
        out_lines.append(report["warnings"][idx])  # Append warning line.
        idx += 1  # Increment index.
    f_trace = open("trace_gf3.log", "w")  # Open trace log file for writing.
    jdx = 0  # Initialize trace loop index.
    while jdx < len(TRACE_LOG):  # Loop through trace logs.
        if jdx >= max_l:  # Check fixed upper bound threshold.
            break  # Break loop.
        f_trace.write(TRACE_LOG[jdx] + "\n")  # Write trace log item.
        jdx += 1  # Increment index.
    f_trace.close()  # Close trace file stream.
    f_out = open("output_gf3.txt", "w")  # Open output text file for writing.
    kdx = 0  # Initialize output loop index.
    while kdx < len(out_lines):  # Loop through output lines.
        if kdx >= max_l:  # Check fixed upper bound threshold.
            break  # Break loop.
        f_out.write(out_lines[kdx] + "\n")  # Write output line.
        kdx += 1  # Increment index.
    f_out.close()  # Close output file stream.
    return 0  # Return zero for successful termination.

if __name__ == "__main__":  # Execution entry point guard.
    status = main()  # Execute main function.
    assert status == 0, "Execution failed."  # Rule 11: Validate status.
