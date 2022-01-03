import scipy.stats as stats


def cleaner(data):
    for i in range(len(data)):
        if data.Price.iloc[i] > data.Price.min() * 5:
            data.Price.iloc[i] = None
    data.dropna(inplace=True)
    return (data)


def rsi_calc(data, periods=14, ema=True):
    close_delta = data.Price.diff()

    up = close_delta.clip(lower=0)
    down = -1 * close_delta.clip(upper=0)

    if ema is True:
        ma_up = up.ewm(com=periods - 1, adjust=True, min_periods=periods).mean()
        ma_down = down.ewm(com=periods - 1, adjust=True, min_periods=periods).mean()

    else:
        ma_up = up.rolling(window=periods, adjust=False).mean()
        ma_down = down.rolling(window=periods, adjust=False).mean()

    rsi = ma_up / ma_down
    rsi = 100 - (100 / (1 + rsi))

    return rsi


def calculator_main(data):
    data = cleaner(data)
    data["rsi"] = rsi_calc(data)
    data["price_z"] = stats.zscore(data.Price)
    data["vol_z"] = stats.zscore(data.Volume)
    data["mkt_cap_dom_z"] = stats.zscore(data["market cap dominance"])
    data["mkt_cap_z"] = stats.zscore(data["Market Cap"])
    return data
