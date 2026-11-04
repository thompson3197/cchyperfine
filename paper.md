---

### 3. `paper.md` (JOSS Paper Markdown Draft)
```markdown
---
title: 'cchyperfine: A High-Precision Command-Line Benchmarking Engine with Statistical Error Propagation and Outlier Detection'
tags:
  - Python
  - benchmarking
  - performance evaluation
  - statistics
  - command-line tools
authors:
  - name: Lead Architect
    orcid: 0000-0000-0000-0000
    affiliation: 1
affiliations:
  - name: Independent Systems Researcher, USA
    index: 1
date: 03 November 2026
bibliography: paper.bib
---

# Summary

Measuring command-line execution duration using traditional utilities such as `time(1)` often fails to isolate transient noise, operating system context switches, and intermediate shell startup overhead. `cchyperfine` is a comprehensive benchmarking engine designed for Python 2.7 environments that delivers high-precision wall-clock and CPU resource profiling (user and kernel space). It features automated run count estimation, shell overhead calibration, lifecycle hooks, Median Absolute Deviation (MAD) outlier detection, parameter matrix sweeps, and multi-format reporting.

# Statement of Need

Developers and systems engineers frequently need to evaluate minor performance regressions in scripts or compiled binaries where differences are measured in milliseconds. Standard tools lack automated statistical confidence intervals, cold-cache fingerprinting, or error propagation during comparative multi-command analyses. `cchyperfine` addresses this gap by offering a deterministic, modular framework adhering to strict systems constraints, making it ideal for resource-constrained embedded environments and legacy Python 2.7 pipelines.

# Core Architecture

## Shell Overhead Subtraction
To isolate the true runtime of a target command $T$, `cchyperfine` measures the baseline invocation cost of the intermediate shell $S$ over $N = 50$ dry runs. The true execution time $t_{\text{exec}}$ is calculated as:

$$t_{\text{exec}} = t_{\text{total}} - \frac{1}{N}\sum_{i=1}^{N} t_{S, i}$$

## Statistical Error Propagation
When comparing two commands $A$ and $B$ with mean runtimes $\mu_A, \mu_B$ and standard deviations $\sigma_A, \sigma_B$, the speedup ratio $R = \mu_B / \mu_A$ carries a propagated error $\sigma_R$ computed via standard differential error propagation:

$$\sigma_R = R \cdot \sqrt{ \left(\frac{\sigma_A}{\mu_A}\right)^2 + \left(\frac{\sigma_B}{\mu_B}\right)^2 }$$

# References
