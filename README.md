# Sonnet

# Nautilus Trader Examples

This is a community-driven collection of simple, easy-to-follow examples, showcasing various **strategies**
and **features** of [Nautilus Trader](https://nautilus-trader.github.io/).  

These examples are designed to help beginners in Nautilus Trader quickly get oriented and create their first strategies.

---

## Examples Overview

| Example | Tags |
|---------|------|
| 0000 Starter template for examples | `template`, `starter`, `basic` |
| 0001 Load 1-min bars from CSV file | `csv`, `data-loading`, `bars`, `1-min` |
| 0002 Use Clock's Timer and Alert + Bracket order | `clock`, `timer`, `alerts`, `bracket-order`, `orders` |
| 0003 Use CacheConfig | `cache`, `configuration` |
| 0004 Export data and use ParquetDataCatalog | `parquet`, `data-export`, `data-catalog` |
| 0005 MRE (Minimalistic example with artificial bars) | `minimal`, `artificial-bars`, `simulation` |
| 0006 Internally generated 5-min bars | `bars-generation`, `5-min`, `internal` |
| 0007 Accessing Portfolio and Cache | `portfolio`, `cache`, `data-access` |
| 0008 Simple indicator + Cascaded Indicator | `indicators`, `cascaded-indicators`, `technical-analysis` |
| 0009 Custom event with msgbus.publish() | `events`, `message-bus`, `publishing` |
| 0010 Using Actor + publish_data() | `actor`, `data-publishing`, `messaging` |
| 0011 Using Actor + publish_signal() | `actor`, `signal-publishing`, `messaging` |
| 0012 Finite State Machine | `fsm`, `state-machine` |
| 0013 Adaptive Bar Ordering (for OHLC bars) | `adaptive`, `bars`, `ohlc`, `ordering` |  

---

## Run / Development Setup

Any python package manager (conda, poetry, pyenv, virtualenv) will work with this project, but I can't recommend `uv` enough for the speed, reliability and comfort. It is really the best swiss-knife tool for:
- for installing python itself
- managing dependencies
- managing python environments

**How to use `uv` with repo above:**

1. One time `uv` installation: `https://docs.astral.sh/uv/getting-started/installation/`
2. Download repo above
3. `cd nautilus_trader_examples` into the folder 
   * and run `uv sync` 
   * Note: this command reads file `pyproject.toml` containing python + all dependencies and installs them into newly created `.venv` folder
4. Activate your env: `source .venv/bin/activate`

You can also setup any IDE to refer to the `.venv` folder as Python environment, that you like (PyCharm, VSCode, ...)

To become better friend with `uv` tool, I can recommend:
* Great tutorial: https://www.saaspegasus.com/guides/uv-deep-dive/   (great finding by @faysou)
* Quick reference: https://htmlpreview.github.io/?https://github.com/stefansimik/dev_guides/blob/main/uv/uv_quick_reference.html
* Official docs: https://docs.astral.sh/uv/

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