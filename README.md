# Nautilus Trader Examples

This is a community-driven collection of simple, easy-to-follow examples, showcasing various **strategies**
and **features** of [Nautilus Trader](https://nautilus-trader.github.io/).  

These examples are designed to help beginners in Nautilus Trader quickly get oriented and create their first strategies.

---

## Examples Overview

| Example                                              |
|:-----------------------------------------------------|
| 0000 Starter template for examples                   |
| 0001 Load 1-min bars from CSV file                   |
| 0002 Use Clock's Timer and Alert + Bracket order     |
| 0003 Use CacheConfig                                 |
| 0004 Export data and use ParquetDataCatalog          |
| 0005 MRE (Minimalistic example with artificial bars) |
| 0006 Internally generated 5-min bars                 |
| 0007 Accessing Portfolio and Cache                   |
| 0008 Simple indicator + Cascaded Indicator           |
| 0009 Custom event with msgbus.publish()              |
| 0010 Using Actor + publish_data()                    |
| 0011 Using Actor + publish_signal()                  |
| 0012 Finite State Machine                            |
| 0013 Adaptive Bar Ordering (for OHLC bars)           |

---

## Import Reference

To help developers navigate the extensive Nautilus Trader framework, we maintain a comprehensive import reference guide at `imports.py`. This guide:

- Lists all available imports, organized alphabetically by module path
- Helps prevent common import-related issues (e.g., when importing native Python vs PyO3 bindings)
- Makes it easier to find and use the framework's components

For example, when implementing technical indicators, beginners might wonder which import should they use use:
```python
from nautilus_trader.indicators.average.ema import ExponentialMovingAverage  # ✓ Preferred
# or
from nautilus_trader.core.nautilus_pyo3 import ExponentialMovingAverage      # ✗ Not recommended
```
The import reference will guide you to the correct choice.

## Run / Development Setup

Any python package manager (conda, poetry, pyenv, virtualenv) will work with this project, but I can't recommend `uv` enough for the speed, reliability and comfort. It is really the best swiss-knife tool for:

- installing python itself
- managing dependencies
- managing python environments

**How to use `uv` with repo above:**

1. **Install `uv` (one-time setup):**  
   Follow the [installation guide](https://docs.astral.sh/uv/getting-started/installation/) to get `uv` on your system.
2. **Download the repository and switch into folder** 
   * `cd nautilus_trader_examples`
3. **Run commands:**
   * `uv sync --pre-release=allow`  
      * This command reads file `pyproject.toml` containing python + all dependencies and installs them into newly created `.venv` folder
      * Flag is `--pre-release=allow` is required to allow installation, because `cython` (dependency of `nautilus_trader`) is still in alpha version
   * `source .venv/bin/activate`
      * this command activates python environment from local `.venv` folder

You can also set up any IDE to refer to the `.venv` folder as Python environment, that you like PyCharm or VSCode.

### More resources about `uv` tool
- **Tutorial:**  
  [https://www.saaspegasus.com/guides/uv-deep-dive/](https://www.saaspegasus.com/guides/uv-deep-dive/)
- **Quick reference:**  
  [https://htmlpreview.github.io/?https://github.com/stefansimik/dev_guides/blob/main/uv/uv_quick_reference.html](https://htmlpreview.github.io/?https://github.com/stefansimik/dev_guides/blob/main/uv/uv_quick_reference.html)
- **Official docs:**  
  [https://docs.astral.sh/uv/](https://docs.astral.sh/uv/)

---

## Contribution Guidelines  

Contributions are highly appreciated! 🚀 

Feel free to submit pull requests and share your own examples to make this repository even better!

To maintain a high quality of examples, all contributions should meet the following criteria:  

1. **Minimalistic and focused:**  
   * Examples should ideally be as simple as possible and clearly demonstrate the usage of a single concept, feature or area of Nautilus Trader.
2. **Self-contained:**  
   * Each example (and its directory) must include all the necessary components — such as code and required data — to run the example independently. 
   * If possible try to reuse existing market data
3. **Well-documented:**  
   * Examples should include reasonable comments, especially in key parts of the code where the main concept or feature being demonstrated is highlighted.

---

For more information about Nautilus Trader and its powerful trading infrastructure, check out the [official documentation](https://nautilus-trader.github.io/).  

Happy Trading and Coding! ✨