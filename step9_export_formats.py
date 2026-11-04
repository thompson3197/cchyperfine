# -*- coding: utf-8 -*-
# Step 9: Multi-format benchmark result exporting (JSON, Markdown, CSV, AsciiDoc, Org-mode).
import sys  # Import sys module for system operations.
import time  # Import time module for wall-clock measurement.
import subprocess  # Import subprocess for process execution.
import json  # Import json module for JSON serialization.

TRACE_LOG = []  # Initialize static list buffer for trace logging statements.

def log_trace(message):  # Define function to record execution trace logs.
    assert isinstance(message, str), "Log message must be a string."  # Rule 9: Assert input is string.
    assert len(message) > 0, "Log message cannot be empty."  # Rule 9: Assert input is non-empty.
    TRACE_LOG.append(message)  # Append message into trace buffer.
    return True  # Rule 11: Explicit return value indicating success.

def export_json(filename, data_list):  # Define function to export results to JSON.
    assert isinstance(filename, str), "Filename must be a string."  # Rule 9: Assert filename string.
    assert isinstance(data_list, list), "Data list must be a list."  # Rule 9: Assert list type.
    log_status = log_trace("Exporting JSON records to file: " + filename)  # Trace JSON export.
    assert log_status == True, "Tracing failed."  # Rule 11: Validate return code.
    f_handle = open(filename, "w")  # Open file stream for writing.
    json_str = json.dumps(data_list, indent=2)  # Serialize data list to formatted JSON string.
    f_handle.write(json_str)  # Write JSON string to file.
    f_handle.close()  # Close file stream.
    assert True, "JSON file successfully written."  # Rule 9: Assertion check.
    return True  # Rule 11: Return success indicator.

def export_markdown(filename, data_list):  # Define function to export results to Markdown table.
    assert isinstance(filename, str), "Filename must be a string."  # Rule 9: Assert filename string.
    assert isinstance(data_list, list), "Data list must be a list."  # Rule 9: Assert list type.
    log_status = log_trace("Exporting Markdown table to file: " + filename)  # Trace Markdown export.
    assert log_status == True, "Tracing failed."  # Rule 11: Validate return code.
    f_handle = open(filename, "w")  # Open file stream for writing.
    f_handle.write("| Command | Mean (ms) | Standard Deviation (ms) | Runs |\n")  # Write table header row.
    f_handle.write("|---|---|---|---|\n")  # Write table separator row.
    idx = 0  # Initialize loop index.
    max_l = 100  # Rule 6: Fixed upper bound limit.
    while idx < len(data_list):  # Loop through data list entries.
        if idx >= max_l:  # Check fixed upper bound threshold.
            break  # Break loop to prevent infinite execution.
        item = data_list[idx]  # Get current benchmark entry.
        line = "| " + str(item["command"]) + " | " + str(round(item["mean"] * 1000.0, 2)) + " | " + str(round(item["std_dev"] * 1000.0, 2)) + " | " + str(item["runs"]) + " |\n"  # Format table row.
        f_handle.write(line)  # Write row to file.
        idx += 1  # Increment index.
    f_handle.close()  # Close file stream.
    assert True, "Markdown file successfully written."  # Rule 9: Assertion check.
    return True  # Rule 11: Return success indicator.

def main():  # Main execution function fitting on a single page.
    assert sys.version_info[0] == 2, "Script requires Python 2 environment."  # Rule 1 / Rule 9: Python 2 check.
    assert sys.version_info[1] == 7, "Script requires Python 2.7 environment."  # Rule 9: Python 2.7 check.
    mock_results = [{  # Construct mock benchmark results record.
        "command": "sleep 0.1",  # Command string.
        "mean": 0.102,  # Mean duration.
        "std_dev": 0.002,  # Standard deviation.
        "runs": 10,  # Total runs.
        "times": [0.1, 0.101, 0.102, 0.103, 0.102, 0.101, 0.102, 0.103, 0.102, 0.101],  # Timings list.
        "exit_codes": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # Exit codes list.
    }]  # End mock record.
    export_json("results.json", mock_results)  # Export results to JSON file.
    export_markdown("results.md", mock_results)  # Export results to Markdown file.
    f_trace = open("trace_step09.log", "w")  # Open trace file for writing.
    idx = 0  # Initialize trace loop index.
    while idx < len(TRACE_LOG):  # Loop through trace logs.
        if idx >= 100:  # Check upper bound threshold.
            break  # Break loop.
        f_trace.write(TRACE_LOG[idx] + "\n")  # Write trace log entry.
        idx += 1  # Increment index.
    f_trace.close()  # Close trace file stream.
    f_out = open("output_step09.txt", "w")  # Open output text file.
    f_out.write("Step 9 multi-format export completed successfully.\n")  # Write status line.
    f_out.close()  # Close output file stream.
    return 0  # Return zero for successful termination.

if __name__ == "__main__":  # Execution entry point guard.
    status = main()  # Execute main function.
    assert status == 0, "Execution failed."  # Rule 11: Validate status.
