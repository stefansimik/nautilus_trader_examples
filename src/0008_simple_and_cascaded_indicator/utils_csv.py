import pandas as pd

from nautilus_trader.model.data import Bar, BarType
from nautilus_trader.model.instruments import Instrument
from nautilus_trader.persistence.wranglers import BarDataWrangler


def load_bars_from_ninjatrader_csv(
    csv_path: str, instrument: Instrument, bar_type: BarType
) -> list[Bar]:
    # Load data into pandas DataFrame with required format
    # Expects columns ['open', 'high', 'low', 'close', 'volume'] with 'timestamp' index.
    # The 'volume' column is optional ; if one does not exist wrangler's process method provides default volume
    df = (
        pd.read_csv(csv_path, sep=";", decimal=".", header=0, index_col=False)
        .rename(columns={"timestamp_utc": "timestamp"})
        .reindex(columns=["timestamp", "open", "high", "low", "close", "volume"])
        .assign(timestamp=lambda dft: pd.to_datetime(dft["timestamp"], format="%Y-%m-%d %H:%M:%S"))
        .set_index("timestamp")
    )

    # Wranglers take pd.DataFrame as input and produce real bars/ticks/quotes (there are many type of wranglers
    wrangler = BarDataWrangler(bar_type, instrument)
    bars: list[Bar] = wrangler.process(df, default_volume=1000000.0)
    return bars
