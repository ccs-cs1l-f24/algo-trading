# algo-trading

A simulation tool for algorithmic trading strategies with visualization and sample strategies to test against.

### Usage:
First, make sure to install Conda. Installation can be done [here](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html).

To run the simulation tool, start by creating the conda environment as follows:

```conda env create -f environment.yml```

Use the following program to activate the conda environment:

```conda activate algo-trading```

There are two different files that may be run. Try

```python3 main.py -h```

for information about multiple simulation runs and

```python3 run_single_simulation.py -h```

for information about a single simulation run. Both can be run with no arguments to observe output under default parameters.

Run `conda deactivate` to exit the conda environment.

This process may be slow the first time. Additionally, running many simulations can take a long time, which is why the default argument is very small.

