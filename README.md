# NautilusTrader Examples

This is a community-driven collection of simple, easy-to-follow examples, showcasing various **strategies**
and **features** of [NautilusTrader](https://nautilus-trader.github.io/).  

These examples are designed to help beginners in NautilusTrader quickly get oriented and create their first strategies.

---

## Examples Overview

All examples are in `/examples` folder.

| Examples                                             |
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
| 0014 MA cross strategy (simple, for any MA type)     |

## Learning materials & Docs

All examples are in `/docs` folder.

| Docs                          |
|:------------------------------|
| 2025-01 FAQ - from @ikeepo.md |

---

## Import Reference

To help developers navigate the extensive NautilusTrader framework, we maintain a comprehensive import reference
guide at file `src/!helpers/all_imports.py`. 

This guide:

- Lists all available imports, organized alphabetically by module path
- Helps prevent common import-related issues (e.g., when importing native Python vs PyO3 bindings)
- Makes it easier to find and use the framework's components

For example, when implementing technical indicators, beginners might wonder which import should they use (these could be offered by IDEs):
```python
from nautilus_trader.common.enums import LogColor               # ✓ This is the right one
from nautilus_trader.core.nautilus_pyo3 import LogColor         # ✗ Not recommended
from nautilus_trader.core.nautilus_pyo3.common import LogColor  # ✗ Not recommended
from nautilus_trader.core.rust.common import LogColor           # ✗ Not recommended
```
The import reference will guide you to the correct choice.

## Run / Development Setup

Any python package manager (conda, poetry, pyenv, virtualenv) will work with this project, but I can't recommend `uv` enough for the speed, reliability and comfort. It is really the best swiss-knife tool for:

- Installing python itself
- Managing dependencies
- Python environments

**How to use `uv` with repo above:**

1. **Install `uv` (one-time setup):**  
   Follow the [installation guide](https://docs.astral.sh/uv/getting-started/installation/) to get `uv` on your system.
2. **Download the repository and switch into folder** 
   * `cd nautilus_trader_examples`
3. **Setup environment:**
   1. Optional installation of required Python version
      * `uv python install 3.12`
         * This installs shared uv-managed Python and this step is required only if you don't have any Python in required version (3.11 or 3.12) installed in your system
   1. Create local python environment in local `.env` folder meeting requirements in `pyproject.toml`
      * `uv venv`
   1. Activate newly created local Python env   
      * MacOS/Unix: `source .venv/bin/activate`
      * Windows: `.venv\Scripts\activate`
   1. Sync all dependencies from `pyproject.toml` -> to Python venv
      * `uv sync --prerelease=allow`  
         * This command reads file `pyproject.toml` containing python + all dependencies and installs them into newly created `.venv` folder
         * Flag is `--pre-release=allow` is required to allow installation, because `cython` (dependency of `nautilus_trader`) is still in alpha version
   1. Run examples in the repo:
      * `cd "src/0001 Load 1-min bars from CSV file"`  # switch to the 1st example directory
      * `python run_backtest.py`                       # run example               

You can also set up any IDE to refer to the local `.venv` folder as Python environment, that you like PyCharm or VSCode.

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
You can either add your own examples from scratch or use the starter template located in 
`src/0000 Starter template for examples` as a foundation for your contribution.

To maintain a quality of examples, all contributions should meet the following criteria:  

1. **Minimalistic and focused:**  
   * Examples should ideally be as simple as possible and clearly demonstrate the usage of a single concept, feature or area of NautilusTrader.
2. **Self-contained:**  
   * Each example (and its directory) must include all the necessary components — such as code and required data — to run the example independently. 
   * If possible try to reuse existing market data
3. **Well-documented:**  
   * Examples should include reasonable comments, especially in key parts of the code where the main concept or feature being demonstrated is highlighted.

---

For more information about NautilusTrader and its powerful trading infrastructure, check out the [official documentation](https://nautilus-trader.github.io/).  

Happy Trading and Coding! ✨
