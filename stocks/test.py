from twelvedata import TDClient
import pandas
# https://twelvedata.com/account

td = TDClient(apikey="")


ts = td.time_series(
    symbol="INTC",
    interval="30min",
    outputsize=25
).as_pandas()

print(ts)