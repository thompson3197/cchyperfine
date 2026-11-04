# cchyperfine 🚀

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1234567.svg)](https://doi.org/10.5281/zenodo.1234567)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 2.7](https://img.shields.io/badge/python-2.7-blue.svg)](https://www.python.org/download/releases/2.7/)

`cchyperfine` is a high-precision command-line benchmarking engine built in **Python 2.7**, modeled after [hyperfine](https://github.com/sharkdp/hyperfine). It provides robust statistical performance analysis, shell overhead subtraction, Median Absolute Deviation (MAD) outlier detection, parameter matrix sweeps, and multi-format reporting.

## Features

- **Shell Overhead Isolation:** Measures and subtracts empty shell invocation latency.
- **Statistical Rigor:** Computes sample means, standard deviations, and robust MAD outlier filtering.
- **Lifecycle Hooks:** Supports `warmup`, `setup`, `prepare`, `conclude`, and `cleanup` hooks.
- **Parameter Sweeps:** Automatically substitutes parameters (`-P` / `-L`) across combinatorial test matrices.
- **Multi-Format Export:** Serializes results to JSON (Hyperfine schema compatible), CSV, Markdown, AsciiDoc, and Org-mode.

## Quickstart

1. Clone the repository and navigate into the source directory:
   ```bash
   git clone [https://github.com/yourusername/cchyperfine.git](https://github.com/yourusername/cchyperfine.git)
   cd cchyperfine
