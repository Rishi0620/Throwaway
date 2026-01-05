import traceback
import ta
from stocksymbol import StockSymbol
from tradingview_ta import TA_Handler, Interval
from flask import Flask
import yfinance as yf
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import mean_squared_error
import numpy as np
from datetime import date, timedelta, datetime
import time
from garman_klass_volatility_target_sl import target_sl_gkyz_daily


def target_sl_buy(symbol):
    url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}?from=2000-01-01&apikey=HlLnwPHGLYdEUVKc6vEOY4e9SBDO9b7R"
    data_needed = get_jsonparsed_data(url)
    historical_data = data_needed.get("historical", [])
    stock_data = pd.DataFrame(historical_data)
    close_price_current = (stock_data.iloc[0]['close'])
    try:
        data = stock_data

        data.columns = data.columns.get_level_values(0)
        close_price = data['close'].iloc[-1]
        daily_returns = data["close"].pct_change().dropna()
        daily_volume = data["volume"].pct_change().dropna()

        dates = data['date'].to_list()
        print(dates)
        dates_list = dates

        data['EMA20'] = data['close'].ewm(span=20, adjust=False).mean()
        data['EMA50'] = data['close'].ewm(span=50, adjust=False).mean()
        data['EMA100'] = data['close'].ewm(span=100, adjust=False).mean()
        data['EMA200'] = data['close'].ewm(span=200, adjust=False).mean()

        moving_avg = data['volume'].rolling(window=50).mean()
        data = data.dropna()

        date_array = []

        for i in range(1, len(data)):
            if daily_returns.iloc[i-1] >= 0.02:
                stock_info = data.iloc[i]
                date_1 = dates_list[i-1]
                low = stock_info["low"]
                high = stock_info["high"]
                close = stock_info["close"]
                open_stock = stock_info["open"]
                volume = stock_info["volume"]
                change_volume = daily_volume.iloc[i-1]
                moving_average_volume = moving_avg.iloc[i-1]

                moving_average_20 = stock_info['EMA20']
                moving_average_50 = stock_info['EMA50']
                moving_average_100 = stock_info["EMA100"]
                moving_average_200 = stock_info['EMA200']

                if moving_average_volume:
                    velocity_volume = ((volume - moving_average_volume) / moving_average_volume) * 100
                    if (velocity_volume > 25) and change_volume > 0.25:
                        if (close - open_stock > 0) and (((high - close) / high) < 0.0010):
                            if ((abs(moving_average_20 - low) / close) < 0.0015) and (close > moving_average_20):
                                date_array.append(date_1)
                                continue
                            elif (low < moving_average_20) and (close > moving_average_20):
                                date_array.append(date_1)
                                continue
                            elif (low < moving_average_20) and (close > moving_average_20):
                                date_array.append(date_1)
                                continue
                            elif (((close - moving_average_20) / close) > 0.0025) and (open_stock < moving_average_20):
                                date_array.append(date_1)
                                continue

                            elif ((abs(moving_average_50 - low) / close) < 0.0015) and (close > moving_average_50):
                                date_array.append(date_1)
                                continue
                            elif (low < moving_average_50) and (close > moving_average_50):
                                date_array.append(date_1)
                                continue
                            elif (low < moving_average_50) and (close > moving_average_50):
                                date_array.append(date_1)
                                continue
                            elif (((close - moving_average_50) / close) > 0.0025) and (open_stock < moving_average_50):
                                date_array.append(date_1)
                                continue

                            elif ((abs(moving_average_100 - low) / close) < 0.0015) and (close > moving_average_100):
                                date_array.append(date_1)
                                continue
                            elif (low < moving_average_100) and (close > moving_average_100):
                                date_array.append(date_1)
                                continue
                            elif (low < moving_average_100) and (close > moving_average_100):
                                date_array.append(date_1)
                                continue
                            elif (((close - moving_average_100) / close) > 0.0025) and (open_stock < moving_average_100):
                                date_array.append(date_1)
                                continue

                            elif ((abs(moving_average_200 - low) / close) < 0.0015) and (close > moving_average_200):
                                date_array.append(date_1)
                                continue
                            elif (low < moving_average_200) and (close > moving_average_200):
                                date_array.append(date_1)
                                continue
                            elif (low < moving_average_200) and (close > moving_average_200):
                                date_array.append(date_1)
                                continue
                            elif (((close - moving_average_200) / close) > 0.0050) and (open_stock < moving_average_200):
                                date_array.append(date_1)
                                continue
                            else:
                                pass

                if open_stock < close:
                    if ((abs(moving_average_20 - low) / close) < 0.0015) and (close > moving_average_20):
                            date_array.append(date_1)
                            continue
                    elif (low < moving_average_20) and (close > moving_average_20):
                            date_array.append(date_1)
                            continue
                    elif (low < moving_average_20) and (close > moving_average_20):
                            date_array.append(date_1)
                            continue
                    elif (((close - moving_average_20) / close) > 0.0025) and (open_stock < moving_average_20):
                            date_array.append(date_1)
                            continue

                    elif ((abs(moving_average_50 - low) / close) < 0.0015) and (close > moving_average_50):
                            date_array.append(date_1)
                            continue
                    elif (low < moving_average_50) and (close > moving_average_50):
                            date_array.append(date_1)
                            continue
                    elif (low < moving_average_50) and (close > moving_average_50):
                            date_array.append(date_1)
                            continue
                    elif (((close - moving_average_50) / close) > 0.0025) and (open_stock < moving_average_50):
                            date_array.append(date_1)
                            continue

                    elif ((abs(moving_average_100 - low) / close) < 0.0015) and (close > moving_average_100):
                            date_array.append(date_1)
                            continue
                    elif (low < moving_average_100) and (close > moving_average_100):
                            date_array.append(date_1)
                            continue
                    elif (low < moving_average_100) and (close > moving_average_100):
                            date_array.append(date_1)
                            continue
                    elif (((close - moving_average_100) / close) > 0.0025) and (open_stock < moving_average_100):
                            date_array.append(date_1)
                            continue

                    elif ((abs(moving_average_200 - low) / close) < 0.0015) and (close > moving_average_200):
                            date_array.append(date_1)
                            continue
                    elif (low < moving_average_200) and (close > moving_average_200):
                            date_array.append(date_1)
                            continue
                    elif (low < moving_average_200) and (close > moving_average_200):
                            date_array.append(date_1)
                            continue
                    elif (((close - moving_average_200) / close) > 0.0025) and (open_stock < moving_average_200):
                            date_array.append(date_1)
                            continue
                    else:
                        pass

        prices_period = []
        current_prices = []

        for date_2 in date_array:
            final_prices = []
            index = dates_list.index(date_2)
            final_index = index + 1
            if final_index > len(data):
                continue
            current_price = data.iloc[index]['close']
            current_prices.append(current_price)
            for i in range(index + 1, final_index + 1):
                final_prices.append(data.iloc[i]["close"])

            prices_period.append(final_prices)

        prices_computing = []

        for element in prices_period:
            prices_computing.append(max(element))

        returns = []

        for i in range(len(current_prices)):
            returns.append((prices_computing[i]/current_prices[i])-1)

        mean_prices = np.mean(returns)
        standard_dev = np.std(returns)

        print(mean_prices, standard_dev, close_price_current)

        while mean_prices - standard_dev > 0:
            mean_prices -= standard_dev/4

        stop_loss = mean_prices

        while stop_loss > -0.01:
            stop_loss = stop_loss - standard_dev

        print(mean_prices, standard_dev, close_price_current)

        while stop_loss > -0.01:
            stop_loss = stop_loss - standard_dev

        target1_val = (1 + mean_prices) * close_price_current

        while target1_val < close_price_current:
            mean_prices = mean_prices + standard_dev
            target1_val = (1 + mean_prices) * close_price_current

        sl1_val = (1 + stop_loss) * close_price_current

        print(f"Target 1: {(1 + mean_prices) * close_price_current:.2f}; Stop Loss 1: {(1 + stop_loss) * close_price_current:.2f}")

        mean_prices = mean_prices + standard_dev
        stop_loss = stop_loss - standard_dev

        target2_val = (1 + mean_prices) * close_price_current
        sl2_val = (1 + stop_loss) * close_price_current

        print(f"Target 2: {(1 + mean_prices) * close_price_current:.2f}; Stop Loss 2: {(1 + stop_loss) * close_price_current:.2f}")

        mean_prices = mean_prices + standard_dev
        stop_loss = stop_loss - standard_dev

        target3_val = (1 + mean_prices) * close_price_current
        sl3_val = (1 + stop_loss) * close_price_current

        print(f"Target 3: {(1+mean_prices) * close_price_current:.2f}; Stop Loss 3: {(1+stop_loss) * close_price_current:.2f}")

    except:
        data = stock_data

        close_price = data['close'].iloc[-1]

        data.columns = data.columns.get_level_values(0)
        daily_returns = data["close"].pct_change().dropna()
        daily_volume = data["volume"].pct_change().dropna()

        dates = data['date'].to_list()
        dates_list = dates

        data['EMA20'] = data['close'].ewm(span=20, adjust=False).mean()
        data['EMA50'] = data['close'].ewm(span=50, adjust=False).mean()
        data['EMA100'] = data['close'].ewm(span=100, adjust=False).mean()
        data['EMA200'] = data['close'].ewm(span=200, adjust=False).mean()

        moving_avg = data['Volume'].rolling(window=50).mean()
        data = data.dropna()

        date_array = []

        for i in range(1, len(data)):
            if daily_returns.iloc[i - 1] >= 0.02:
                stock_info = data.iloc[i]
                date_1 = dates_list[i - 1]
                low = stock_info["low"]
                high = stock_info["high"]
                close = stock_info["close"]
                open_stock = stock_info["open"]
                volume = stock_info["volume"]
                change_volume = daily_volume.iloc[i - 1]
                moving_average_volume = moving_avg.iloc[i - 1]

                moving_average_20 = stock_info['EMA20']
                moving_average_50 = stock_info['EMA50']
                moving_average_100 = stock_info["EMA100"]
                moving_average_200 = stock_info['EMA200']

                if moving_average_volume:
                    velocity_volume = ((volume - moving_average_volume) / moving_average_volume) * 100
                    if (velocity_volume > 25) and change_volume > 0.25:
                        if (close - open_stock > 0) and (((high - close) / high) < 0.0010):
                            if ((abs(moving_average_20 - low) / close) < 0.0015) and (close > moving_average_20):
                                date_array.append(date_1)
                                continue
                            elif (low < moving_average_20) and (close > moving_average_20):
                                date_array.append(date_1)
                                continue
                            elif (low < moving_average_20) and (close > moving_average_20):
                                date_array.append(date_1)
                                continue
                            elif (((close - moving_average_20) / close) > 0.0025) and (open_stock < moving_average_20):
                                date_array.append(date_1)
                                continue

                            elif ((abs(moving_average_50 - low) / close) < 0.0015) and (close > moving_average_50):
                                date_array.append(date_1)
                                continue
                            elif (low < moving_average_50) and (close > moving_average_50):
                                date_array.append(date_1)
                                continue
                            elif (low < moving_average_50) and (close > moving_average_50):
                                date_array.append(date_1)
                                continue
                            elif (((close - moving_average_50) / close) > 0.0025) and (open_stock < moving_average_50):
                                date_array.append(date_1)
                                continue

                            elif ((abs(moving_average_100 - low) / close) < 0.0015) and (close > moving_average_100):
                                date_array.append(date_1)
                                continue
                            elif (low < moving_average_100) and (close > moving_average_100):
                                date_array.append(date_1)
                                continue
                            elif (low < moving_average_100) and (close > moving_average_100):
                                date_array.append(date_1)
                                continue
                            elif (((close - moving_average_100) / close) > 0.0025) and (
                                    open_stock < moving_average_100):
                                date_array.append(date_1)
                                continue

                            elif ((abs(moving_average_200 - low) / close) < 0.0015) and (close > moving_average_200):
                                date_array.append(date_1)
                                continue
                            elif (low < moving_average_200) and (close > moving_average_200):
                                date_array.append(date_1)
                                continue
                            elif (low < moving_average_200) and (close > moving_average_200):
                                date_array.append(date_1)
                                continue
                            elif (((close - moving_average_200) / close) > 0.0050) and (
                                    open_stock < moving_average_200):
                                date_array.append(date_1)
                                continue
                            else:
                                pass

                if open_stock < close:
                    if ((abs(moving_average_20 - low) / close) < 0.0015) and (close > moving_average_20):
                        date_array.append(date_1)
                        continue
                    elif (low < moving_average_20) and (close > moving_average_20):
                        date_array.append(date_1)
                        continue
                    elif (low < moving_average_20) and (close > moving_average_20):
                        date_array.append(date_1)
                        continue
                    elif (((close - moving_average_20) / close) > 0.0025) and (open_stock < moving_average_20):
                        date_array.append(date_1)
                        continue

                    elif ((abs(moving_average_50 - low) / close) < 0.0015) and (close > moving_average_50):
                        date_array.append(date_1)
                        continue
                    elif (low < moving_average_50) and (close > moving_average_50):
                        date_array.append(date_1)
                        continue
                    elif (low < moving_average_50) and (close > moving_average_50):
                        date_array.append(date_1)
                        continue
                    elif (((close - moving_average_50) / close) > 0.0025) and (open_stock < moving_average_50):
                        date_array.append(date_1)
                        continue

                    elif ((abs(moving_average_100 - low) / close) < 0.0015) and (close > moving_average_100):
                        date_array.append(date_1)
                        continue
                    elif (low < moving_average_100) and (close > moving_average_100):
                        date_array.append(date_1)
                        continue
                    elif (low < moving_average_100) and (close > moving_average_100):
                        date_array.append(date_1)
                        continue
                    elif (((close - moving_average_100) / close) > 0.0025) and (open_stock < moving_average_100):
                        date_array.append(date_1)
                        continue

                    elif ((abs(moving_average_200 - low) / close) < 0.0015) and (close > moving_average_200):
                        date_array.append(date_1)
                        continue
                    elif (low < moving_average_200) and (close > moving_average_200):
                        date_array.append(date_1)
                        continue
                    elif (low < moving_average_200) and (close > moving_average_200):
                        date_array.append(date_1)
                        continue
                    elif (((close - moving_average_200) / close) > 0.0025) and (open_stock < moving_average_200):
                        date_array.append(date_1)
                        continue
                    else:
                        pass

        prices_period = []
        current_prices = []

        for date_2 in date_array:
            final_prices = []
            index = dates_list.index(date_2)
            final_index = index + 1
            if final_index > len(data):
                continue
            current_price = data.iloc[index]['close']
            current_prices.append(current_price)
            for i in range(index + 1, final_index + 1):
                final_prices.append(data.iloc[i]["close"])

            prices_period.append(final_prices)

        prices_computing = []

        for element in prices_period:
            prices_computing.append(max(element))

        returns = []

        for i in range(len(current_prices)):
            returns.append((prices_computing[i] / current_prices[i]) - 1)


        mean_prices = np.mean(returns)
        standard_dev = np.std(returns)

        while mean_prices - standard_dev > 0:
            mean_prices -= standard_dev/4

        stop_loss = mean_prices

        while stop_loss > -0.01:
            stop_loss = stop_loss - standard_dev


        print(mean_prices, standard_dev, close_price_current)

        target_security = target_sl_gkyz_daily(symbol) * 0.25
        print(symbol, target_security)

        target1_val = (1 + target_security) * close_price_current

        '''while target1_val < close_price_current:
            mean_prices = mean_prices + standard_dev
            target1_val = (1 + mean_prices) * close_price_current'''

        sl1_val = (1 - (target_security/0.5)) * close_price_current

        print(f"Target 1: {(1 + mean_prices) * close_price_current:.2f}; Stop Loss 1: {(1 + stop_loss) * close_price_current:.2f}")

        mean_prices = mean_prices + standard_dev
        stop_loss = stop_loss - standard_dev

        target2_val = (1 + mean_prices) * close_price_current
        sl2_val = (1 + stop_loss) * close_price_current

        print(f"Target 2: {(1 + mean_prices) * close_price_current:.2f}; Stop Loss 2: {(1 + stop_loss) * close_price_current:.2f}")

        mean_prices = mean_prices + standard_dev
        stop_loss = stop_loss - standard_dev

        target3_val = (1 + mean_prices) * close_price_current
        sl3_val = (1 + stop_loss) * close_price_current

        print(f"Target 3: {(1+mean_prices) * close_price_current:.2f}; Stop Loss 3: {(1+stop_loss) * close_price_current:.2f}")

    return target1_val, target2_val, target3_val, sl1_val, sl2_val, sl3_val


def target_sl_sell(symbol):
    from datetime import date
    url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}?from=2000-01-01&apikey=HlLnwPHGLYdEUVKc6vEOY4e9SBDO9b7R"
    data_needed = get_jsonparsed_data(url)
    historical_data = data_needed.get("historical", [])
    stock_data = pd.DataFrame(historical_data)
    close_price_current = (stock_data.iloc[0]['close'])
    try:
        data = stock_data

        data.columns = data.columns.get_level_values(0)
        close_price = data['close'].iloc[-1]
        daily_returns = data["close"].pct_change().dropna()

        dates = data['date'].to_list()
        dates_list = dates

        data['EMA20'] = data['close'].ewm(span=20, adjust=False).mean()
        data['EMA50'] = data['close'].ewm(span=50, adjust=False).mean()
        data['EMA100'] = data['close'].ewm(span=100, adjust=False).mean()
        data['EMA200'] = data['close'].ewm(span=200, adjust=False).mean()

        moving_avg = data['volume'].rolling(window=50).mean()
        data = data.dropna()

        date_array = []

        for i in range(1, len(data)):
            if daily_returns.iloc[i-1] <= -0.02:
                stock_info = data.iloc[i]
                date_1 = dates_list[i-1]
                low = stock_info["low"]
                high = stock_info["high"]
                close = stock_info["close"]
                open_stock = stock_info["open"]

                moving_average_20 = stock_info['EMA20']
                moving_average_50 = stock_info['EMA50']
                moving_average_100 = stock_info["EMA100"]
                moving_average_200 = stock_info['EMA200']

                if open_stock > close:
                    if ((abs(moving_average_20 - high) / close) < 0.0015) and (close < moving_average_20):
                        date_array.append(date_1)
                        continue
                    elif (high > moving_average_20) and (close < moving_average_20):
                        date_array.append(date_1)
                        continue
                    elif (high > moving_average_20) and (close < moving_average_20):
                        date_array.append(date_1)
                        continue
                    elif ((abs(close - moving_average_20) / close) < 0.0025) and (close < moving_average_20) and (
                            open_stock > moving_average_20):
                        date_array.append(date_1)
                        continue

                    elif ((abs(moving_average_50 - high) / close) < 0.0015) and (close < moving_average_50):
                        date_array.append(date_1)
                        continue
                    elif (high > moving_average_50) and (close < moving_average_50):
                        date_array.append(date_1)
                        continue
                    elif (high > moving_average_50) and (close < moving_average_50):
                        date_array.append(date_1)
                        continue
                    elif ((abs(close - moving_average_50) / close) < 0.0025) and (close < moving_average_50) and (
                            open_stock > moving_average_50):
                        date_array.append(date_1)
                        continue

                    elif ((abs(moving_average_100 - high) / close) < 0.0015) and (close < moving_average_100):
                        date_array.append(date_1)
                        continue
                    elif (high > moving_average_100) and (close < moving_average_100):
                        date_array.append(date_1)
                        continue
                    elif (high > moving_average_100) and (close < moving_average_100):
                        date_array.append(date_1)
                        continue
                    elif ((abs(close - moving_average_100) / close) < 0.0025) and (close < moving_average_100) and (
                            open_stock > moving_average_100):
                        date_array.append(date_1)
                        continue

                    elif ((abs(moving_average_200 - high) / close) < 0.0015) and (close < moving_average_200):
                        date_array.append(date_1)
                        continue
                    elif (high > moving_average_200) and (close < moving_average_200):
                        date_array.append(date_1)
                        continue
                    elif (high > moving_average_200) and (close < moving_average_200):
                        date_array.append(date_1)
                        continue
                    elif ((abs(close - moving_average_200) / close) < 0.0025) and (close < moving_average_200) and (
                            open_stock > moving_average_200):
                        date_array.append(date_1)
                        continue
                    else:
                        pass

        prices_period = []
        current_prices = []
        for date_2 in date_array:
            final_prices = []
            index = dates_list.index(date_2)
            final_index = index + 1
            if final_index > len(data):
                continue
            current_price = data.iloc[index]['Close']
            current_prices.append(current_price)
            for i in range(index + 1, final_index + 1):
                final_prices.append(data.iloc[i]["Close"])

            prices_period.append(final_prices)



        prices_computing = []

        for element in prices_period:
            prices_computing.append(max(element))

        returns = []

        for i in range(len(current_prices)):
            returns.append((prices_computing[i]/current_prices[i])-1)


        mean_prices = -(np.mean(returns))
        standard_dev = (np.std(returns))

        print(mean_prices, standard_dev, close_price_current)

        while mean_prices - standard_dev > 0:
            mean_prices -= standard_dev/4

        stop_loss = mean_prices

        while stop_loss > -0.01:
            stop_loss = stop_loss - standard_dev

        print(mean_prices, standard_dev, close_price_current)

        while stop_loss > -0.01:
            stop_loss = stop_loss - standard_dev

        target_security = target_sl_gkyz_daily(symbol) * 0.25

        target1_val = (1 - target_security) * close_price_current

        # while target1_val < close_price_current:
        #   mean_prices = mean_prices + standard_dev
        #  target1_val = (1 + mean_prices) * close_price_current

        sl1_val = (1 + (target_security / 0.5)) * close_price_current

        print(f"Target 1: {(1 - mean_prices) * close_price_current:.2f}; Stop Loss 1: {(1 - stop_loss) * close_price_current:.2f}")

        mean_prices = mean_prices + standard_dev
        stop_loss = stop_loss - standard_dev

        target2_val = (1 - mean_prices) * close_price_current
        sl2_val = (1 - stop_loss) * close_price_current

        print(f"Target 2: {(1 - mean_prices) * close_price_current:.2f}; Stop Loss 2: {(1 - stop_loss) * close_price_current:.2f}")

        mean_prices = mean_prices + standard_dev
        stop_loss = stop_loss - standard_dev

        target3_val = (1 - mean_prices) * close_price_current
        sl3_val = (1 - stop_loss) * close_price_current

        print(f"Target 3: {(1-mean_prices) * close_price_current:.2f}; Stop Loss 3: {(1-stop_loss) * close_price_current:.2f}")

    except:
        data = stock_data

        data.columns = data.columns.get_level_values(0)
        close_price = data['close'].iloc[-1]
        daily_returns = data["close"].pct_change().dropna()
        daily_volume = data["volume"].pct_change().dropna()

        dates = data['date'].to_list()
        dates_list = dates

        data['EMA20'] = data['close'].ewm(span=20, adjust=False).mean()
        data['EMA50'] = data['close'].ewm(span=50, adjust=False).mean()
        data['EMA100'] = data['close'].ewm(span=100, adjust=False).mean()
        data['EMA200'] = data['close'].ewm(span=200, adjust=False).mean()

        moving_avg = data['volume'].rolling(window=50).mean()
        data = data.dropna()

        date_array = []

        for i in range(1, len(data)):
            if daily_returns.iloc[i - 1] <= -0.02:
                stock_info = data.iloc[i]
                date_1 = dates_list[i - 1]
                low = stock_info["low"]
                high = stock_info["high"]
                close = stock_info["close"]
                open_stock = stock_info["open"]

                moving_average_20 = stock_info['EMA20']
                moving_average_50 = stock_info['EMA50']
                moving_average_100 = stock_info["EMA100"]
                moving_average_200 = stock_info['EMA200']

                if open_stock > close:
                    if ((abs(moving_average_20 - high) / close) < 0.0015) and (close < moving_average_20):
                        date_array.append(date_1)
                        continue
                    elif (high > moving_average_20) and (close < moving_average_20):
                        date_array.append(date_1)
                        continue
                    elif (high > moving_average_20) and (close < moving_average_20):
                        date_array.append(date_1)
                        continue
                    elif ((abs(close - moving_average_20) / close) < 0.0025) and (close < moving_average_20) and (
                            open_stock > moving_average_20):
                        date_array.append(date_1)
                        continue

                    elif ((abs(moving_average_50 - high) / close) < 0.0015) and (close < moving_average_50):
                        date_array.append(date_1)
                        continue
                    elif (high > moving_average_50) and (close < moving_average_50):
                        date_array.append(date_1)
                        continue
                    elif (high > moving_average_50) and (close < moving_average_50):
                        date_array.append(date_1)
                        continue
                    elif ((abs(close - moving_average_50) / close) < 0.0025) and (close < moving_average_50) and (
                            open_stock > moving_average_50):
                        date_array.append(date_1)
                        continue

                    elif ((abs(moving_average_100 - high) / close) < 0.0015) and (close < moving_average_100):
                        date_array.append(date_1)
                        continue
                    elif (high > moving_average_100) and (close < moving_average_100):
                        date_array.append(date_1)
                        continue
                    elif (high > moving_average_100) and (close < moving_average_100):
                        date_array.append(date_1)
                        continue
                    elif ((abs(close - moving_average_100) / close) < 0.0025) and (close < moving_average_100) and (
                            open_stock > moving_average_100):
                        date_array.append(date_1)
                        continue

                    elif ((abs(moving_average_200 - high) / close) < 0.0015) and (close < moving_average_200):
                        date_array.append(date_1)
                        continue
                    elif (high > moving_average_200) and (close < moving_average_200):
                        date_array.append(date_1)
                        continue
                    elif (high > moving_average_200) and (close < moving_average_200):
                        date_array.append(date_1)
                        continue
                    elif ((abs(close - moving_average_200) / close) < 0.0025) and (close < moving_average_200) and (
                            open_stock > moving_average_200):
                        date_array.append(date_1)
                        continue
                    else:
                        pass

        prices_period = []
        current_prices = []

        for date_2 in date_array:
            final_prices = []
            index = dates_list.index(date_2)
            final_index = index + 1
            if final_index > len(data):
                continue
            current_price = data.iloc[index]['close']
            current_prices.append(current_price)
            for i in range(index + 1, final_index + 1):
                final_prices.append(data.iloc[i]["close"])

            prices_period.append(final_prices)

        prices_computing = []

        for element in prices_period:
            prices_computing.append(max(element))

        returns = []

        for i in range(len(current_prices)):
            returns.append((prices_computing[i] / current_prices[i]) - 1)

        mean_prices = -(np.mean(returns))
        standard_dev = np.std(returns)

        while mean_prices - standard_dev > 0:
            mean_prices -= standard_dev/4

        stop_loss = mean_prices

        while stop_loss > -0.01:
            stop_loss = stop_loss - standard_dev

        print(mean_prices, standard_dev, close_price_current)

        while stop_loss > -0.01:
            stop_loss = stop_loss - standard_dev

        target1_val = (1 - mean_prices) * close_price_current

        while target1_val > close_price_current:
            mean_prices = mean_prices + standard_dev
            target1_val = (1 - mean_prices) * close_price_current

        sl1_val = (1 - stop_loss) * close_price_current

        print(f"Target 1: {(1 - mean_prices) * close_price_current:.2f}; Stop Loss 1: {(1 - stop_loss) * close_price_current:.2f}")

        mean_prices = mean_prices + standard_dev
        stop_loss = stop_loss - standard_dev

        target2_val = (1 - mean_prices) * close_price_current
        sl2_val = (1 - stop_loss) * close_price_current

        print(f"Target 2: {(1 - mean_prices) * close_price_current:.2f}; Stop Loss 2: {(1 - stop_loss) * close_price_current:.2f}")

        mean_prices = mean_prices + close_price_current
        stop_loss = stop_loss - close_price_current

        target3_val = (1 - mean_prices) * close_price_current
        sl3_val = (1 - stop_loss) * close_price_current

        print(f"Target 3: {(1 - mean_prices) * close_price_current:.2f}; Stop Loss 3: {(1 - stop_loss) * close_price_current:.2f}")

    return target1_val, target2_val, target3_val, sl1_val, sl2_val, sl3_val


def handlerData(symbol):
    df = yf.download(f"{symbol}", interval='1d')

    change = (df["Close"].iloc[-1] / df["Close"].iloc[-2] - 1) * 100
    df["rsi"] = ta.momentum.RSIIndicator(df["Close"][f"{symbol}"]).rsi()
    df["EMA20"] = ta.trend.EMAIndicator(df["Close"][f"{symbol}"], window=20).ema_indicator()
    df["EMA50"] = ta.trend.EMAIndicator(df["Close"][f"{symbol}"], window=50).ema_indicator()
    df["EMA100"] = ta.trend.EMAIndicator(df["Close"][f"{symbol}"], window=100).ema_indicator()
    df["EMA200"] = ta.trend.EMAIndicator(df["Close"][f"{symbol}"], window=200).ema_indicator()
    df["psar"] = ta.trend.PSARIndicator(df["High"][f"{symbol}"], df["Low"][f"{symbol}"],
                                        df["Close"][f"{symbol}"]).psar()

    indicators = {
        'open': df["Open"][f"{symbol}"].iloc[-1],
        'high': df["High"][f"{symbol}"].iloc[-1],
        'low': df["Low"][f"{symbol}"].iloc[-1],
        'close': df["Close"][f"{symbol}"].iloc[-1],
        'rsi': df["rsi"].iloc[-1],
        'EMA20': df["EMA20"].iloc[-1],
        'EMA50': df["EMA50"].iloc[-1],
        'EMA100': df["EMA100"].iloc[-1],
        'EMA200': df['EMA200'].iloc[-1],
        'P.SAR': df['psar'].iloc[-1],
        'change': change[symbol]
    }

    return indicators

def recommendation_summary_technical(symbol):
  def WMA(series, window):
      weights = np.arange(1, window + 1)
      return series.rolling(window).apply(lambda x: np.dot(x, weights) / weights.sum(), raw=True)

  def HMA(series, window):
      half = int(window / 2)
      sqrt_w = int(np.sqrt(window))
      wma_half = WMA(series, half)
      wma_full = WMA(series, window)
      raw_hma = 2 * wma_half - wma_full
      return WMA(raw_hma, sqrt_w)

  def get_tradingview_style_summary(symbol):
      df = yf.download(symbol, interval='1d')
      if df.empty or len(df) < 100:
          return f"Insufficient data for {symbol}"

      df.dropna(inplace=True)
      df.columns = df.columns.get_level_values(0)

      df['rsi'] = ta.momentum.RSIIndicator(df['Close']).rsi()
      df['stoch_k'] = ta.momentum.StochasticOscillator(df['High'], df['Low'], df['Close']).stoch()
      df['cci'] = ta.trend.CCIIndicator(df['High'], df['Low'], df['Close']).cci()
      df['adx'] = ta.trend.ADXIndicator(df['High'], df['Low'], df['Close']).adx()
      df['ao'] = ta.momentum.AwesomeOscillatorIndicator(df['High'], df['Low']).awesome_oscillator()
      df['momentum'] = ta.momentum.ROCIndicator(df['Close'], window=10).roc()
      df['macd_diff'] = ta.trend.MACD(df['Close']).macd_diff()
      df['willr'] = ta.momentum.WilliamsRIndicator(df['High'], df['Low'], df['Close']).williams_r()
      df['uo'] = ta.momentum.UltimateOscillator(df['High'], df['Low'], df['Close']).ultimate_oscillator()

      df['ema_10'] = ta.trend.EMAIndicator(df['Close'], window=10).ema_indicator()
      df['ema_20'] = ta.trend.EMAIndicator(df['Close'], window=20).ema_indicator()
      df['ema_30'] = ta.trend.EMAIndicator(df['Close'], window=30).ema_indicator()
      df['ema_50'] = ta.trend.EMAIndicator(df['Close'], window=50).ema_indicator()
      df['ema_100'] = ta.trend.EMAIndicator(df['Close'], window=100).ema_indicator()
      df['ema_200'] = ta.trend.EMAIndicator(df['Close'], window=200).ema_indicator()
      df['sma_10'] = ta.trend.SMAIndicator(df['Close'], window=10).sma_indicator()
      df['sma_20'] = ta.trend.SMAIndicator(df['Close'], window=20).sma_indicator()
      df['sma_30'] = ta.trend.SMAIndicator(df['Close'], window=30).sma_indicator()
      df['sma_50'] = ta.trend.SMAIndicator(df['Close'], window=50).sma_indicator()
      df['sma_100'] = ta.trend.SMAIndicator(df['Close'], window=100).sma_indicator()
      df['sma_200'] = ta.trend.SMAIndicator(df['Close'], window=200).sma_indicator()

      ema13 = ta.trend.EMAIndicator(close=df['Close'], window=13).ema_indicator()
      df['bull_power'] = df['High'] - ema13
      df['bear_power'] = df['Low'] - ema13

      stochrsi = ta.momentum.StochRSIIndicator(close=df['Close'])
      df['stoch_rsi'] = stochrsi.stochrsi_k()

      ichimoku = ta.trend.IchimokuIndicator(df['High'], df['Low'], window1=9, window2=26)
      df['ichimoku_base'] = ichimoku.ichimoku_base_line()

      df['vwma_20'] = (df['Close'] * df['Volume']).rolling(20).sum() / df['Volume'].rolling(20).sum()

      df['hma_9'] = HMA(df['Close'], 9)

      last = df.iloc[-1]
      close = last['Close']

      osc_signals = []
      osc_signals.append("Buy" if last['rsi'] < 30 else "Sell" if last['rsi'] > 70 else "Neutral")
      osc_signals.append("Buy" if last['stoch_k'] < 20 else "Sell" if last['stoch_k'] > 80 else "Neutral")
      osc_signals.append("Buy" if last['cci'] < -100 else "Sell" if last['cci'] > 100 else "Neutral")
      osc_signals.append("Buy" if last['adx'] > 25 else "Neutral")
      osc_signals.append("Buy" if last['ao'] > 0 else "Sell")
      osc_signals.append("Buy" if last['momentum'] > 0 else "Sell")
      osc_signals.append("Buy" if last['macd_diff'] > 0 else "Sell")
      osc_signals.append("Buy" if last['willr'] < -80 else "Sell" if last['willr'] > -20 else "Neutral")
      osc_signals.append("Buy" if last['uo'] < 30 else "Sell" if last['uo'] > 70 else "Neutral")
      osc_signals.append("Buy" if (last['bull_power'] - last['bear_power']) > 0 else "Sell")
      osc_signals.append("Buy" if last['stoch_rsi'] < 0.2 else "Sell" if last['stoch_rsi'] > 0.8 else "Neutral")


      ma_signals = []
      for ma in ['ema_10', 'ema_20', 'ema_30', 'ema_50', 'ema_100', 'ema_200', 'sma_10', 'sma_20', 'sma_30', 'sma_50', 'sma_100', 'sma_200', 'ichimoku_base', 'vwma_20', 'hma_9']:
          ma_signals.append("Buy" if close > last[ma] else "Sell")

      all_signals = osc_signals + ma_signals
      summary = pd.Series(all_signals).value_counts()
      total = len(all_signals)
      buys = summary.get("Buy", 0)
      sells = summary.get("Sell", 0)
      neutrals = summary.get("Neutral", 0)

      if (buys > sells) and (buys >= neutrals):
          recommendation = "BUY"
      elif (buys < sells) and (sells >= neutrals):
          recommendation = "SELL"
      elif buys == sells:
          recommendation = "NEUTRAL"
      elif buys / total >= 0.75:
          recommendation = "STRONG_BUY"
      elif buys / total >= 0.50:
          recommendation = "BUY"
      elif sells / total >= 0.75:
          recommendation = "STRONG_SELL"
      elif sells / total >= 0.50:
          recommendation = "SELL"
      else:
          recommendation = "NEUTRAL"

      final = {
          "BUY": buys,
          "SELL": sells,
          "NEUTRAL": summary.get("Neutral", 0),
          "RECOMMENDATION": recommendation
      }

      return final

  finalRec = get_tradingview_style_summary(symbol)
  return finalRec


def optimisation_portfolio(symbols_call, symbols_put_options):
    print(len(symbols_call), len(symbols_put_options))

    def weight_function(symbol):
        date_current = date.today().strftime("20%y-%m-%d")
        month_earlier = (date.today() - timedelta(days=31)).strftime("20%y-%m-%d")
        url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}?from={month_earlier}&apikey=HlLnwPHGLYdEUVKc6vEOY4e9SBDO9b7R"
        data_needed = get_jsonparsed_data(url)
        historical_data = data_needed.get("historical", [])
        apple_stock = pd.DataFrame(historical_data)
        apple_stock = apple_stock.iloc[::-1].reset_index(drop=True)
        apple_stock = apple_stock.rename(columns={col: col.capitalize() for col in apple_stock.columns})
        apple_stock = apple_stock.rename(
            columns={'Date': 'Date', 'Open': 'Open', 'High': 'High', 'Low': 'Low', 'Close': 'Close', 'Volume': 'Volume',
                     'Adjclose': 'Adj Close'})

        try:
            apple_stock['Price_Rise'] = (apple_stock['Adj Close'].shift(-1) > apple_stock['Adj Close']).astype(int)
        except:
            apple_stock['Price_Rise'] = (apple_stock['Close'].shift(-1) > apple_stock['Close']).astype(int)

        apple_stock = apple_stock.dropna()

        X = apple_stock[['Open', 'High', 'Low', 'Close', 'Volume']]
        y = apple_stock['Price_Rise']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        clf = MLPClassifier(hidden_layer_sizes=(50, 30, 10), max_iter=1000, random_state=42)
        clf.fit(X_train, y_train)

        predictions = clf.predict(X_test)

        accuracy = accuracy_score(y_test, predictions)

        last_day_features = pd.DataFrame({
            'Open': [apple_stock['Open'].iloc[-1]],
            'High': [apple_stock['High'].iloc[-1]],
            'Low': [apple_stock['Low'].iloc[-1]],
            'Close': [apple_stock['Close'].iloc[-1]],
            'Volume': [apple_stock['Volume'].iloc[-1]],
        })

        probability_of_rise = clf.predict_proba(last_day_features)[:, 1]

        print(f"Accuracy: {accuracy:.2%}")
        print(f"Estimated Probability of Price Rise for {symbol} Stock: {probability_of_rise[0]:.2%}")
        print(accuracy)
        print(probability_of_rise[0])
        print(accuracy*probability_of_rise[0])

        url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}?from={month_earlier}&apikey=HlLnwPHGLYdEUVKc6vEOY4e9SBDO9b7R"
        data_needed = get_jsonparsed_data(url)
        historical_data = data_needed.get("historical", [])
        apple_stock = pd.DataFrame(historical_data)
        apple_stock = apple_stock.iloc[::-1].reset_index(drop=True)
        apple_stock = apple_stock.rename(columns={col: col.capitalize() for col in apple_stock.columns})
        apple_stock = apple_stock.rename(
            columns={'Date': 'Date', 'Open': 'Open', 'High': 'High', 'Low': 'Low', 'Close': 'Close', 'Volume': 'Volume',
                     'Adjclose': 'Adj Close'})

        try:
            apple_stock['Price_Rise'] = (apple_stock['Adj Close'].shift(-1) > apple_stock['Adj Close']).astype(int)
        except:
            apple_stock['Price_Rise'] = (apple_stock['Close'].shift(-1) > apple_stock['Close']).astype(int)

        apple_stock = apple_stock.dropna()

        X = apple_stock[['Open', 'High', 'Low', 'Close', 'Volume']]
        y = apple_stock['Price_Rise']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        clf = RandomForestClassifier(n_estimators=1000, random_state=42)
        clf.fit(X_train, y_train)

        predictions = clf.predict(X_test)

        accuracy_1 = accuracy_score(y_test, predictions)

        last_day_features = pd.DataFrame({
            'Open': [apple_stock['Open'].iloc[-1]],
            'High': [apple_stock['High'].iloc[-1]],
            'Low': [apple_stock['Low'].iloc[-1]],
            'Close': [apple_stock['Close'].iloc[-1]],
            'Volume': [apple_stock['Volume'].iloc[-1]],
        })

        probability_of_rise_1 = clf.predict_proba(last_day_features)[:, 1]

        print(f"Accuracy: {accuracy_1:.2%}")
        print(f"Estimated Probability of Price Rise for {symbol} Stock: {probability_of_rise_1[0]:.2%}")
        print(accuracy_1)
        print(probability_of_rise_1[0])
        print(accuracy_1 * probability_of_rise_1[0])

        expected_prices = []
        dates = []

        actual_class = []
        expected_class = []

        #today_date = date.today().strftime("20%y-%m-%d")
        today = date.today().strftime("20%y-%m-%d")
        date_str2 = date.today() - timedelta(days=7)
        date_str2 = date_str2.strftime("20%y-%m-%d")
        url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}?from={date_str2}&apikey=HlLnwPHGLYdEUVKc6vEOY4e9SBDO9b7R"
        data_needed = get_jsonparsed_data(url)
        historical_data = data_needed.get("historical", [])
        apple_data = pd.DataFrame(historical_data)
        apple_data = apple_data.iloc[::-1].reset_index(drop=True)
        apple_data = apple_data.rename(columns={col: col.capitalize() for col in apple_data.columns})
        apple_data = apple_data.rename(
            columns={'Date': 'Date', 'Open': 'Open', 'High': 'High', 'Low': 'Low', 'Close': 'Close', 'Volume': 'Volume',
                     'Adjclose': 'Adj Close'})
        dates_list = pd.DataFrame(apple_data).dropna()['Date'].tolist()

        for i in range(len(dates_list)):
            dates_list[i] = dates_list[i]
        date_format = "%Y-%m-%d"

        today = datetime.strptime(today, date_format)
        #date1 = datetime.strptime(date_str1, date_format)
        date2 = datetime.strptime(date_str2, date_format)

        while date2 < today:
            try:
                url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}?from=1800-01-01&to={date2.strftime('20%y-%m-%d')}&apikey=HlLnwPHGLYdEUVKc6vEOY4e9SBDO9b7R"
                data_needed = get_jsonparsed_data(url)
                historical_data = data_needed.get("historical", [])
                apple_data = pd.DataFrame(historical_data)
                apple_data = apple_data.iloc[::-1].reset_index(drop=True)
                apple_data = apple_data.rename(columns={col: col.capitalize() for col in apple_data.columns})
                apple_data = apple_data.rename(
                    columns={'Date': 'Date', 'Open': 'Open', 'High': 'High', 'Low': 'Low', 'Close': 'Close',
                             'Volume': 'Volume',
                             'Adjclose': 'Adj Close'})
                daily_returns = apple_data["Adj Close"].pct_change().dropna()
                np.random.seed(42)
                num_simulations = 10000#00
                num_days = 5

                simulated_price_paths = []

                for _ in range(num_simulations):
                    daily_volatility = daily_returns.std()
                    daily_drift = daily_returns.mean()

                    price_path = [apple_data["Adj Close"].iloc[-1]]

                    for _ in range(num_days):
                        price_t = price_path[-1]
                        price_t_plus_1 = price_t * (1 + daily_drift + daily_volatility * np.random.normal())
                        price_path.append(price_t_plus_1)

                    simulated_price_paths.append(price_path)

                mean_prices = [np.mean(path) for path in simulated_price_paths]

                expected_price = np.mean(mean_prices)

                date2 = date2 + timedelta(days=1)
                print(expected_price not in expected_prices)
                dates.append(date2.strftime("20%y-%m-%d"))
                expected_prices.append(expected_price)

                continue

            except Exception as e:
                #exception = ""
                print(e)

        data = {'Date': dates, 'Expected_Price': expected_prices}

        length = len(dates)

        for i in range(length-1, -1, -1):
            element = dates[i]
            if element not in dates_list:
                dates.remove(dates[i])
                expected_prices.remove(expected_prices[i])
                length = length - 1

        for i in range(len(expected_prices)-1):
            if expected_prices[i+1] > expected_prices[i]:
                expected_class.append(1)
            else:
                expected_class.append(0)

        df = pd.DataFrame(data)

        url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}?from={date_str2}&apikey=HlLnwPHGLYdEUVKc6vEOY4e9SBDO9b7R"
        data_needed = get_jsonparsed_data(url)
        historical_data = data_needed.get("historical", [])
        apple_data = pd.DataFrame(historical_data)
        apple_data = apple_data.iloc[::-1].reset_index(drop=True)
        apple_data = apple_data.rename(columns={col: col.capitalize() for col in apple_data.columns})
        apple_data = apple_data.rename(
            columns={'Date': 'Date', 'Open': 'Open', 'High': 'High', 'Low': 'Low', 'Close': 'Close', 'Volume': 'Volume',
                     'Adjclose': 'Adj Close'})
        print(apple_data)
        print(df)

        if apple_data['Date'].iloc[0]!= df["Date"].iloc[0]:
            apple_data.drop(apple_data.index[0], inplace=True)

        for i in range(len(apple_data)-1):
            if apple_data["Close"].iloc[i+1] > apple_data["Close"].iloc[i]:
                actual_class.append(1)
            else:
                actual_class.append(0)

        mse = mean_squared_error(df["Expected_Price"], apple_data["Close"])

        rmse = np.sqrt(mse)

        rmse_percentage = (rmse / np.mean(apple_data["Close"]))
        rmse_adjusted_quotient = 1 - rmse_percentage
        rmse_upper_quotient = 1 + rmse_percentage
        print(f"RMSE as a percentage: {rmse_percentage:.2%}")
        print(expected_class)
        print(actual_class)

        count = 0

        for i in range(len(expected_class)):
            if expected_class[i] == actual_class[i]:
                count += 1

        print(count, len(expected_class))

        print(f"{(count / len(expected_class)) * 100:.2f}%")
        weighing_factor = (count / len(expected_class)) * 100
        print(weighing_factor)
        end_date = date.today().strftime("20%y-%m-%d")
        url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}?from=2000-01-01&apikey=HlLnwPHGLYdEUVKc6vEOY4e9SBDO9b7R"
        data_needed = get_jsonparsed_data(url)
        historical_data = data_needed.get("historical", [])
        apple_data = pd.DataFrame(historical_data)
        apple_data = apple_data.iloc[::-1].reset_index(drop=True)
        apple_data = apple_data.rename(columns={col: col.capitalize() for col in apple_data.columns})
        apple_data = apple_data.rename(
            columns={'Date': 'Date', 'Open': 'Open', 'High': 'High', 'Low': 'Low', 'Close': 'Close', 'Volume': 'Volume',
                     'Adjclose': 'Adj Close'})

        daily_returns = apple_data["Adj Close"].pct_change().dropna()
        np.random.seed(42)
        num_simulations = 10000#00
        num_days = 5

        simulated_price_paths = []

        for _ in range(num_simulations):
            daily_volatility = daily_returns.std()
            daily_drift = daily_returns.mean()

            price_path = [apple_data["Adj Close"].iloc[-1]]

            for _ in range(num_days):
                price_t = price_path[-1]
                price_t_plus_1 = price_t * (1 + daily_drift + daily_volatility * np.random.normal())
                price_path.append(price_t_plus_1)

            simulated_price_paths.append(price_path)


        mean_prices = [np.mean(path) for path in simulated_price_paths]
        expected_price = np.mean(mean_prices)

        print(f"Current Value of {symbol}: {apple_data['Close'].iloc[-1]:.2f}")
        print(f"Expected Fair Stock Value for {symbol}: {expected_price:.2f}")

        if (expected_price > apple_data['Close'].iloc[-1]) and (weighing_factor > 50):
            factor_used = rmse_adjusted_quotient * (weighing_factor/100)
            print(factor_used)
        elif (expected_price < apple_data['Close'].iloc[-1]) and (weighing_factor < 50):
            factor_used = rmse_adjusted_quotient * ((100-weighing_factor)/100)
            print(factor_used)
        elif (expected_price < apple_data['Close'].iloc[-1]) and (weighing_factor > 50):
            factor_used = rmse_adjusted_quotient * (weighing_factor/100) * -1
            print(factor_used)
        elif (expected_price > apple_data['Close'].iloc[-1]) and (weighing_factor < 50):
            factor_used = rmse_adjusted_quotient * ((100-weighing_factor) / 100) * -1
            print(factor_used)
        else:
            factor_used = rmse_adjusted_quotient * (weighing_factor/100)
            print(factor_used)

        url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}?from=2000-01-01&apikey=HlLnwPHGLYdEUVKc6vEOY4e9SBDO9b7R"
        data_needed = get_jsonparsed_data(url)
        historical_data = data_needed.get("historical", [])
        df_us = pd.DataFrame(historical_data)
        df_us = df_us.iloc[::-1].reset_index(drop=True)
        df_us = df_us.rename(columns={col: col.capitalize() for col in df_us.columns})
        df_us = df_us.rename(
            columns={'Date': 'Date', 'Open': 'Open', 'High': 'High', 'Low': 'Low', 'Close': 'Close', 'Volume': 'Volume',
                     'Adjclose': 'Adj Close'})
        #df_us = pd.DataFrame(yf.download(symbol, start="2000-01-01", end="2023-01-11", interval="1d"))
        last_volume = float(df_us["Volume"].iloc[-1])

        total_weight_raw = (factor_used + (probability_of_rise[0] * accuracy) + (probability_of_rise_1[0] * accuracy_1)) #* last_volume

        print(total_weight_raw)

        return total_weight_raw

    def weight_function_put(symbol):
        date_current = date.today().strftime("20%y-%m-%d")
        month_earlier = (date.today() - timedelta(days=31)).strftime("20%y-%m-%d")
        url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}?from={month_earlier}&apikey=HlLnwPHGLYdEUVKc6vEOY4e9SBDO9b7R"
        data_needed = get_jsonparsed_data(url)
        historical_data = data_needed.get("historical", [])
        apple_stock = pd.DataFrame(historical_data)
        apple_stock = apple_stock.iloc[::-1].reset_index(drop=True)
        apple_stock = apple_stock.rename(columns={col: col.capitalize() for col in apple_stock.columns})
        apple_stock = apple_stock.rename(
            columns={'Date': 'Date', 'Open': 'Open', 'High': 'High', 'Low': 'Low', 'Close': 'Close', 'Volume': 'Volume',
                     'Adjclose': 'Adj Close'})

        try:
            apple_stock['Price_Rise'] = (apple_stock['Adj Close'].shift(-1) > apple_stock['Adj Close']).astype(int)
        except:
            apple_stock['Price_Rise'] = (apple_stock['Close'].shift(-1) > apple_stock['Close']).astype(int)

        apple_stock = apple_stock.dropna()

        X = apple_stock[['Open', 'High', 'Low', 'Close', 'Volume']]
        y = apple_stock['Price_Rise']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        clf = MLPClassifier(hidden_layer_sizes=(50, 30, 10), max_iter=1000, random_state=42)
        clf.fit(X_train, y_train)

        predictions = clf.predict(X_test)

        accuracy = accuracy_score(y_test, predictions)

        last_day_features = pd.DataFrame({
            'Open': [apple_stock['Open'].iloc[-1]],
            'High': [apple_stock['High'].iloc[-1]],
            'Low': [apple_stock['Low'].iloc[-1]],
            'Close': [apple_stock['Close'].iloc[-1]],
            'Volume': [apple_stock['Volume'].iloc[-1]],
        })

        probability_of_rise = clf.predict_proba(last_day_features)[:, 1]

        print(f"Accuracy: {accuracy:.2%}")
        print(f"Estimated Probability of Price Fall for {symbol} Stock: {1 - probability_of_rise[0]:.2%}")
        print(accuracy)
        print(1 - probability_of_rise[0])
        print(accuracy * 1 - (probability_of_rise[0]))

        url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}?from={month_earlier}&apikey=HlLnwPHGLYdEUVKc6vEOY4e9SBDO9b7R"
        data_needed = get_jsonparsed_data(url)
        historical_data = data_needed.get("historical", [])
        apple_stock = pd.DataFrame(historical_data)
        apple_stock = apple_stock.iloc[::-1].reset_index(drop=True)
        apple_stock = apple_stock.rename(columns={col: col.capitalize() for col in apple_stock.columns})
        apple_stock = apple_stock.rename(
            columns={'Date': 'Date', 'Open': 'Open', 'High': 'High', 'Low': 'Low', 'Close': 'Close', 'Volume': 'Volume',
                     'Adjclose': 'Adj Close'})

        try:
            apple_stock['Price_Rise'] = (apple_stock['Adj Close'].shift(-1) > apple_stock['Adj Close']).astype(int)
        except:
            apple_stock['Price_Rise'] = (apple_stock['Close'].shift(-1) > apple_stock['Close']).astype(int)

        apple_stock = apple_stock.dropna()

        X = apple_stock[['Open', 'High', 'Low', 'Close', 'Volume']]
        y = apple_stock['Price_Rise']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        clf = RandomForestClassifier(n_estimators=1000, random_state=42)
        clf.fit(X_train, y_train)

        predictions = clf.predict(X_test)

        accuracy_1 = accuracy_score(y_test, predictions)

        last_day_features = pd.DataFrame({
            'Open': [apple_stock['Open'].iloc[-1]],
            'High': [apple_stock['High'].iloc[-1]],
            'Low': [apple_stock['Low'].iloc[-1]],
            'Close': [apple_stock['Close'].iloc[-1]],
            'Volume': [apple_stock['Volume'].iloc[-1]],
        })

        probability_of_rise_1 = clf.predict_proba(last_day_features)[:, 1]
        probability_of_fall_1 = 1 - probability_of_rise_1[0]
        probability_of_fall = 1 - probability_of_rise[0]

        print(f"Accuracy: {accuracy_1:.2%}")
        print(f"Estimated Probability of Price Fall for {symbol} Stock: {1 - probability_of_rise_1[0]:.2%}")
        print(accuracy_1)
        print(1 - probability_of_rise_1[0])
        print(accuracy_1 * (1 - probability_of_rise_1[0]))

        expected_prices = []
        dates = []

        actual_class = []
        expected_class = []

        #today_date = date.today().strftime("20%y-%m-%d")
        today = date.today().strftime("20%y-%m-%d")
        date_str2 = date.today() - timedelta(days=7)
        date_str2 = date_str2.strftime("20%y-%m-%d")
        url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}?from={date_str2}&apikey=HlLnwPHGLYdEUVKc6vEOY4e9SBDO9b7R"
        data_needed = get_jsonparsed_data(url)
        historical_data = data_needed.get("historical", [])
        apple_data = pd.DataFrame(historical_data)
        apple_data = apple_data.iloc[::-1].reset_index(drop=True)
        apple_data = apple_data.rename(columns={col: col.capitalize() for col in apple_data.columns})
        apple_data = apple_data.rename(
            columns={'Date': 'Date', 'Open': 'Open', 'High': 'High', 'Low': 'Low', 'Close': 'Close', 'Volume': 'Volume',
                     'Adjclose': 'Adj Close'})
        dates_list = pd.DataFrame(apple_data).dropna()['Date'].tolist()

        for i in range(len(dates_list)):
            dates_list[i] = dates_list[i]
        date_format = "%Y-%m-%d"

        today = datetime.strptime(today, date_format)
        #date1 = datetime.strptime(date_str1, date_format)
        date2 = datetime.strptime(date_str2, date_format)

        while date2 < today:
            try:
                url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}?from=1800-01-01&to={date2.strftime('20%y-%m-%d')}&apikey=HlLnwPHGLYdEUVKc6vEOY4e9SBDO9b7R"
                data_needed = get_jsonparsed_data(url)
                historical_data = data_needed.get("historical", [])
                apple_data = pd.DataFrame(historical_data)
                apple_data = apple_data.iloc[::-1].reset_index(drop=True)
                apple_data = apple_data.rename(columns={col: col.capitalize() for col in apple_data.columns})
                apple_data = apple_data.rename(
                    columns={'Date': 'Date', 'Open': 'Open', 'High': 'High', 'Low': 'Low', 'Close': 'Close',
                             'Volume': 'Volume',
                             'Adjclose': 'Adj Close'})
                daily_returns = apple_data["Adj Close"].pct_change().dropna()
                np.random.seed(42)
                num_simulations = 10000#00
                num_days = 5

                simulated_price_paths = []

                for _ in range(num_simulations):
                    daily_volatility = daily_returns.std()
                    daily_drift = daily_returns.mean()

                    price_path = [apple_data["Adj Close"].iloc[-1]]

                    for _ in range(num_days):
                        price_t = price_path[-1]
                        price_t_plus_1 = price_t * (1 + daily_drift + daily_volatility * np.random.normal())
                        price_path.append(price_t_plus_1)

                    simulated_price_paths.append(price_path)

                mean_prices = [np.mean(path) for path in simulated_price_paths]

                expected_price = np.mean(mean_prices)

                date2 = date2 + timedelta(days=1)
                print(expected_price not in expected_prices)
                dates.append(date2.strftime("20%y-%m-%d"))
                expected_prices.append(expected_price)

                continue

            except Exception as e:
                #exception = ""
                print(e)

        data = {'Date': dates, 'Expected_Price': expected_prices}

        length = len(dates)

        for i in range(length-1, -1, -1):
            element = dates[i]
            if element not in dates_list:
                dates.remove(dates[i])
                expected_prices.remove(expected_prices[i])
                length = length - 1

        for i in range(len(expected_prices)-1):
            if expected_prices[i+1] > expected_prices[i]:
                expected_class.append(1)
            else:
                expected_class.append(0)

        df = pd.DataFrame(data)

        url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}?from={date_str2}&apikey=HlLnwPHGLYdEUVKc6vEOY4e9SBDO9b7R"
        data_needed = get_jsonparsed_data(url)
        historical_data = data_needed.get("historical", [])
        apple_data = pd.DataFrame(historical_data)
        apple_data = apple_data.iloc[::-1].reset_index(drop=True)
        apple_data = apple_data.rename(columns={col: col.capitalize() for col in apple_data.columns})
        apple_data = apple_data.rename(
            columns={'Date': 'Date', 'Open': 'Open', 'High': 'High', 'Low': 'Low', 'Close': 'Close', 'Volume': 'Volume',
                     'Adjclose': 'Adj Close'})
        print(apple_data)
        print(df)

        if apple_data['Date'].iloc[0] != df["Date"].iloc[0]:
            apple_data.drop(apple_data.index[0], inplace=True)

        for i in range(len(apple_data)-1):
            if apple_data["Close"].iloc[i+1] > apple_data["Close"].iloc[i]:
                actual_class.append(1)
            else:
                actual_class.append(0)

        mse = mean_squared_error(df["Expected_Price"], apple_data["Close"])

        rmse = np.sqrt(mse)

        rmse_percentage = (rmse / np.mean(apple_data["Close"]))
        rmse_adjusted_quotient = 1 - rmse_percentage
        rmse_upper_quotient = 1 + rmse_percentage
        print(f"RMSE as a percentage: {rmse_percentage:.2%}")
        print(expected_class)
        print(actual_class)

        count = 0

        for i in range(len(expected_class)):
            if expected_class[i] == actual_class[i]:
                count += 1

        print(count, len(expected_class))

        print(f"{(count / len(expected_class)) * 100:.2f}%")
        weighing_factor = (count / len(expected_class)) * 100
        print(weighing_factor)
        end_date = date.today().strftime("20%y-%m-%d")
        url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}?from=2000-01-01&apikey=HlLnwPHGLYdEUVKc6vEOY4e9SBDO9b7R"
        data_needed = get_jsonparsed_data(url)
        historical_data = data_needed.get("historical", [])
        apple_data = pd.DataFrame(historical_data)
        apple_data = apple_data.iloc[::-1].reset_index(drop=True)
        apple_data = apple_data.rename(columns={col: col.capitalize() for col in apple_data.columns})
        apple_data = apple_data.rename(
            columns={'Date': 'Date', 'Open': 'Open', 'High': 'High', 'Low': 'Low', 'Close': 'Close', 'Volume': 'Volume',
                     'Adjclose': 'Adj Close'})

        daily_returns = apple_data["Adj Close"].pct_change().dropna()
        np.random.seed(42)
        num_simulations = 10000#00
        num_days = 5

        simulated_price_paths = []

        for _ in range(num_simulations):
            daily_volatility = daily_returns.std()
            daily_drift = daily_returns.mean()

            price_path = [apple_data["Adj Close"].iloc[-1]]

            for _ in range(num_days):
                price_t = price_path[-1]
                price_t_plus_1 = price_t * (1 + daily_drift + daily_volatility * np.random.normal())
                price_path.append(price_t_plus_1)

            simulated_price_paths.append(price_path)

        mean_prices = [np.mean(path) for path in simulated_price_paths]
        expected_price = np.mean(mean_prices)

        print(f"Current Value of {symbol}: {apple_data['Close'].iloc[-1]:.2f}")
        print(f"Expected Fair Stock Value for {symbol}: {expected_price:.2f}")

        if (expected_price > apple_data['Close'].iloc[-1]) and (weighing_factor > 50):
            factor_used = rmse_adjusted_quotient * (weighing_factor/100) * -1
            print(factor_used)
        elif (expected_price < apple_data['Close'].iloc[-1]) and (weighing_factor < 50):
            factor_used = rmse_adjusted_quotient * ((100-weighing_factor)/100) * -1
            print(factor_used)
        elif (expected_price < apple_data['Close'].iloc[-1]) and (weighing_factor > 50):
            factor_used = rmse_adjusted_quotient * (weighing_factor/100)
            print(factor_used)
        elif (expected_price > apple_data['Close'].iloc[-1]) and (weighing_factor < 50):
            factor_used = rmse_adjusted_quotient * ((100-weighing_factor) / 100)
            print(factor_used)
        else:
            factor_used = rmse_adjusted_quotient * (weighing_factor/100)
            print(factor_used)

        url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}?from=2000-01-01&apikey=HlLnwPHGLYdEUVKc6vEOY4e9SBDO9b7R"
        data_needed = get_jsonparsed_data(url)
        historical_data = data_needed.get("historical", [])
        df_us = pd.DataFrame(historical_data)
        df_us = df_us.iloc[::-1].reset_index(drop=True)
        df_us = df_us.rename(columns={col: col.capitalize() for col in df_us.columns})
        df_us = df_us.rename(
            columns={'Date': 'Date', 'Open': 'Open', 'High': 'High', 'Low': 'Low', 'Close': 'Close', 'Volume': 'Volume',
                     'Adjclose': 'Adj Close'})
        #df_us = pd.DataFrame(yf.download(symbol, start="2000-01-01", end="2023-11-01", interval="1d"))
        last_volume = float(df_us["Volume"].iloc[-1])

        total_weight_raw = (factor_used + (probability_of_fall * accuracy) + (probability_of_fall_1 * accuracy_1)) #* last_volume

        print(total_weight_raw)

        return total_weight_raw

    symbols = symbols_call

    pre_portfolio_optimisation = []

    for element in symbols:
        try:
            size_of_security = weight_function(element)
            pre_portfolio_optimisation.append(size_of_security)
            time.sleep(3)
            print("="*200)
        except Exception as e:
            print(e)
            traceback.print_exc()

    total = 0

    for value in pre_portfolio_optimisation:
        if value > 0:
            total += value

    portfolio_optimisation = []
    sym_call = []
    port_call = []
    sym_put = []
    port_put = []

    for i in range(len(pre_portfolio_optimisation)):
        if pre_portfolio_optimisation[i] > 0:
            standardised_score = pre_portfolio_optimisation[i]/total
            portfolio_optimisation.append(standardised_score)
    print("*"*200)
    for i in range(len(pre_portfolio_optimisation)):
        sym_call.append(symbols[i])
        if pre_portfolio_optimisation[i] > 0:
            print(f"Recommended Weight for {symbols[i]}: {pre_portfolio_optimisation[i] / total:.2%}")
            port_call.append(pre_portfolio_optimisation[i] / total)
        else:
            port_call.append(0)

    symbols_put = symbols_put_options
    pre_portfolio_optimisation_put = []

    for element in symbols_put_options:
        try:
            size_of_security_put = weight_function_put(element)
            pre_portfolio_optimisation_put.append(size_of_security_put)
            time.sleep(3)
            print("="*200)
        except Exception as e:
            print(e)
            traceback.print_exc()

    total_put = 0

    for value in pre_portfolio_optimisation_put:
        if value > 0:
            print(value)
            total_put += value

    portfolio_optimisation_put = []

    for i in range(len(pre_portfolio_optimisation_put)):
        if pre_portfolio_optimisation_put[i] > 0:
            standardised_score_put = pre_portfolio_optimisation_put[i] / total_put
            portfolio_optimisation_put.append(standardised_score_put)

    print(portfolio_optimisation_put)

    print("*" * 200)

    for i in range(len(pre_portfolio_optimisation_put)):
        sym_put.append(symbols_put[i])
        if pre_portfolio_optimisation_put[i] > 0:
            print(f"Recommended Weight for {symbols_put[i]}: {pre_portfolio_optimisation_put[i] / total_put:.2%}")  # portfolio_optimisation_put[i]:.2%}")
            port_put.append(pre_portfolio_optimisation_put[i] / total_put)
        else:
            port_put.append(0)

    print(sym_call)
    print(port_call)
    print(sym_put)
    print(port_put)

    return sym_call, sym_put, port_call, port_put


def vol():
    response = ""
    api_key = "095e35e3-f38b-4b48-98ce-5b1eee5765b3"
    ss = StockSymbol(api_key)
    symbol_only_list = ss.get_symbol_list(market="US", symbols_only=True)
    symbol_only_list_1 = ss.get_symbol_list(market="US", symbols_only=False)
    stock_list = ['AAPL', 'ABT', 'ADBE', 'ADI', 'ADP', 'ADSK', 'AEP', 'AFL', 'AJG', 'AMAT', 'AMD', 'AMGN', 'AMZN', 'ANET', 'AON', 'APD', 'APH', 'AVGO', 'AZO', 'BA', 'BAC', 'BK', 'BKNG', 'BMY', 'C', 'CARR', 'CAT', 'CDNS', 'CHTR', 'CI', 'CL', 'CMCSA', 'CME', 'CMG', 'COF', 'COP', 'COST', 'CRM', 'CSCO', 'CTAS', 'CVS', 'CVX', 'DFS', 'DHR', 'DIS', 'DLR', 'DUK', 'ECL', 'EMR', 'EOG', 'EQIX', 'FCX', 'FTNT', 'GD', 'GILD', 'GOOG', 'GOOGL', 'GS', 'GWW', 'HCA', 'HD', 'HLT', 'HON', 'IBM', 'ICE', 'INTC', 'INTU', 'JCI', 'JNJ', 'JPM', 'KLAC', 'KMI', 'KO', 'LIN', 'LLY', 'LMT', 'LOW', 'LRCX', 'MA', 'MAR', 'MCD', 'MCK', 'MDLZ', 'MDT', 'MET', 'MNST', 'MO', 'MPC', 'MRK', 'MS', 'MSI', 'NEM', 'NFLX', 'NKE', 'NOW', 'NSC', 'NVDA', 'NXPI', 'O', 'OKE', 'ORLY', 'PAYX', 'PEP', 'PG', 'PGR', 'PH', 'PLD', 'PM', 'PNC', 'PSA', 'PWR', 'PYPL', 'QCOM', 'RCL', 'ROP', 'RSG', 'SBUX', 'SNPS', 'SO', 'SPG', 'SYK', 'T', 'TFC', 'TJX', 'TMO', 'TMUS', 'TRV', 'TSLA', 'TT', 'TXN', 'UNH', 'UNP', 'UPS', 'USB', 'V', 'VRTX', 'VZ', 'WELL', 'WFC', 'ZTS']

    print(stock_list)
    momentum_list = []
    symbol_arr = []
    close_price = []
    volume = []
    market_cap = []
    sector = []

    def download_stock_data(symbol):
        url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}?from=2000-01-01&apikey=HlLnwPHGLYdEUVKc6vEOY4e9SBDO9b7R"
        data_needed = get_jsonparsed_data(url)
        historical_data = data_needed.get("historical", [])
        stock_data = pd.DataFrame(historical_data)
        stock_data = stock_data.iloc[::-1].reset_index(drop=True)
        stock_data = stock_data.rename(columns={col: col.capitalize() for col in stock_data.columns})
        stock_data = stock_data.rename(
            columns={'Date': 'Date', 'Open': 'Open', 'High': 'High', 'Low': 'Low', 'Close': 'Close',
                     'Volume': 'Volume',
                     'Adjclose': 'Adj Close'})
        return stock_data

    for symbol in stock_list:
        try:
            start_date = "2000-01-01"
            end_date = date.today()
            stock_data = download_stock_data(symbol)
            df = pd.DataFrame(stock_data)
            window_size = 50
            moving_avg = df['Volume'].rolling(window=window_size).mean()

            # Add the moving average values to the DataFrame
            df['20MA'] = moving_avg
            df = df.dropna()

            last_volume = float(df["Volume"].iloc[-1])
            change_volume = ((last_volume-(float(df["Volume"].iloc[-2])))/float(df["Volume"].iloc[-2]))*100
            last_ma = float(df["20MA"].iloc[-1])

            velocity = ((last_volume-last_ma)/last_ma)*100

            if velocity > 50:
                if change_volume > 50:
                    symbol = symbol.replace(".L", "")
                    symbol = symbol.replace(".IL", "")
                    output = TA_Handler(symbol=symbol,
                                        screener="america",
                                        exchange="NASDAQ",
                                        interval=Interval.INTERVAL_1_DAY)
                    try:
                        try:
                            bos = output.get_analysis().summary
                        except:
                            bos = recommendation_summary_technical(symbol)
                        if (bos["RECOMMENDATION"] == "BUY") or (bos["RECOMMENDATION"] == "STRONG_BUY"):
                            try:
                                indicator = output.get_analysis().indicators
                            except:
                                indicator = handlerData(symbol)
                            close = indicator["close"]
                            open_stock = indicator["open"]
                            high = indicator["high"]
                            low = indicator["low"]

                            moving_average_20 = indicator["EMA20"]
                            moving_average_50 = indicator["EMA50"]
                            moving_average_100 = indicator["EMA100"]
                            moving_average_200 = indicator["EMA200"]
                            if indicator["change"] >= 2.0 and ((close - open_stock) > 0):
                                if ((abs(moving_average_20 - low) / close) < 0.0015) and (close > moving_average_20):
                                    momentum_list.append(symbol)
                                    continue
                                elif (low < moving_average_20) and (close > moving_average_20):
                                    momentum_list.append(symbol)
                                    continue
                                elif (low < moving_average_20) and (close > moving_average_20):
                                    momentum_list.append(symbol)
                                    continue
                                elif (((close - moving_average_20) / close) > 0.0025) and (open_stock < moving_average_20):
                                    momentum_list.append(symbol)
                                    continue

                                elif ((abs(moving_average_50 - low) / close) < 0.0015) and (close > moving_average_50):
                                    momentum_list.append(symbol)
                                    continue
                                elif (low < moving_average_50) and (close > moving_average_50):
                                    momentum_list.append(symbol)
                                    continue
                                elif (low < moving_average_50) and (close > moving_average_50):
                                    momentum_list.append(symbol)
                                    continue
                                elif (((close - moving_average_50) / close) > 0.0025) and (open_stock < moving_average_50):
                                    momentum_list.append(symbol)
                                    continue

                                elif ((abs(moving_average_100 - low) / close) < 0.0015) and (close > moving_average_100):
                                    momentum_list.append(symbol)
                                    continue
                                elif (low < moving_average_100) and (close > moving_average_100):
                                    momentum_list.append(symbol)
                                    continue
                                elif (low < moving_average_100) and (close > moving_average_100):
                                    momentum_list.append(symbol)
                                    continue
                                elif (((close - moving_average_100) / close) > 0.0025) and (open_stock < moving_average_100):
                                    momentum_list.append(symbol)
                                    continue

                                elif ((abs(moving_average_200 - low) / close) < 0.0015) and (close > moving_average_200):
                                    momentum_list.append(symbol)
                                    continue
                                elif (low < moving_average_200) and (close > moving_average_200):
                                    momentum_list.append(symbol)
                                    continue
                                elif (low < moving_average_200) and (close > moving_average_200):
                                    momentum_list.append(symbol)
                                    continue
                                elif (((close - moving_average_200) / close) > 0.0025) and (open_stock < moving_average_200):
                                    momentum_list.append(symbol)
                                    continue
                                else:
                                    continue
                        else:
                            continue
                    except:
                        pass

                    try:
                        try:
                            output = TA_Handler(symbol=symbol,
                                                screener="america",
                                                exchange="NYSE",
                                                interval=Interval.INTERVAL_1_DAY)
                            bos = output.get_analysis().summary
                        except:
                            bos = recommendation_summary_technical(symbol)
                        if (bos["RECOMMENDATION"] == "BUY") or (bos["RECOMMENDATION"] == "STRONG_BUY"):
                            try:
                                indicator = output.get_analysis().indicators
                            except:
                                indicator = handlerData(symbol)
                            close = indicator["close"]
                            open_stock = indicator["open"]
                            high = indicator["high"]
                            low = indicator["low"]

                            moving_average_20 = indicator["EMA20"]
                            moving_average_50 = indicator["EMA50"]
                            moving_average_100 = indicator["EMA100"]
                            moving_average_200 = indicator["EMA200"]
                            if indicator["change"] >= 2.0 and ((close - open_stock) > 0):
                                if ((abs(moving_average_20 - low) / close) < 0.0015) and (close > moving_average_20):
                                    momentum_list.append(symbol)
                                    continue
                                elif (low < moving_average_20) and (close > moving_average_20):
                                    momentum_list.append(symbol)
                                    continue
                                elif (low < moving_average_20) and (close > moving_average_20):
                                    momentum_list.append(symbol)
                                    continue
                                elif (((close - moving_average_20) / close) > 0.0025) and (open_stock < moving_average_20):
                                    momentum_list.append(symbol)
                                    continue

                                elif ((abs(moving_average_50 - low) / close) < 0.0015) and (close > moving_average_50):
                                    momentum_list.append(symbol)
                                    continue
                                elif (low < moving_average_50) and (close > moving_average_50):
                                    momentum_list.append(symbol)
                                    continue
                                elif (low < moving_average_50) and (close > moving_average_50):
                                    momentum_list.append(symbol)
                                    continue
                                elif (((close - moving_average_50) / close) > 0.0025) and (open_stock < moving_average_50):
                                    momentum_list.append(symbol)
                                    continue

                                elif ((abs(moving_average_100 - low) / close) < 0.0015) and (close > moving_average_100):
                                    momentum_list.append(symbol)
                                    continue
                                elif (low < moving_average_100) and (close > moving_average_100):
                                    momentum_list.append(symbol)
                                    continue
                                elif (low < moving_average_100) and (close > moving_average_100):
                                    momentum_list.append(symbol)
                                    continue
                                elif (((close - moving_average_100) / close) > 0.0025) and (open_stock < moving_average_100):
                                    momentum_list.append(symbol)
                                    continue

                                elif ((abs(moving_average_200 - low) / close) < 0.0015) and (close > moving_average_200):
                                    momentum_list.append(symbol)
                                    continue
                                elif (low < moving_average_200) and (close > moving_average_200):
                                    momentum_list.append(symbol)
                                    continue
                                elif (low < moving_average_200) and (close > moving_average_200):
                                    momentum_list.append(symbol)
                                    continue
                                elif (((close - moving_average_200) / close) > 0.0025) and (open_stock < moving_average_200):
                                    momentum_list.append(symbol)
                                    continue
                                else:
                                    continue
                        else:
                            continue
                    except:
                        pass

                    try:
                        try:
                            output = TA_Handler(symbol=symbol,
                                                screener="america",
                                                exchange="AMEX",
                                                interval=Interval.INTERVAL_1_DAY)
                            bos = output.get_analysis().summary
                        except:
                            bos = recommendation_summary_technical(symbol)
                        if (bos["RECOMMENDATION"] == "BUY") or (bos["RECOMMENDATION"] == "STRONG_BUY"):
                            try:
                                indicator = output.get_analysis().indicators
                            except:
                                indicator = handlerData(symbol)
                            close = indicator["close"]
                            open_stock = indicator["open"]
                            high = indicator["high"]
                            low = indicator["low"]

                            moving_average_20 = indicator["EMA20"]
                            moving_average_50 = indicator["EMA50"]
                            moving_average_100 = indicator["EMA100"]
                            moving_average_200 = indicator["EMA200"]
                            if indicator["change"] >= 2.0 and ((close - open_stock) > 0):
                                if ((abs(moving_average_20 - low) / close) < 0.0015) and (close > moving_average_20):
                                    momentum_list.append(symbol)
                                    continue
                                elif (low < moving_average_20) and (close > moving_average_20):
                                    momentum_list.append(symbol)
                                    continue
                                elif (low < moving_average_20) and (close > moving_average_20):
                                    momentum_list.append(symbol)
                                    continue
                                elif (((close - moving_average_20) / close) > 0.0025) and (open_stock < moving_average_20):
                                    momentum_list.append(symbol)
                                    continue

                                elif ((abs(moving_average_50 - low) / close) < 0.0015) and (close > moving_average_50):
                                    momentum_list.append(symbol)
                                    continue
                                elif (low < moving_average_50) and (close > moving_average_50):
                                    momentum_list.append(symbol)
                                    continue
                                elif (low < moving_average_50) and (close > moving_average_50):
                                    momentum_list.append(symbol)
                                    continue
                                elif (((close - moving_average_50) / close) > 0.0025) and (open_stock < moving_average_50):
                                    momentum_list.append(symbol)
                                    continue

                                elif ((abs(moving_average_100 - low) / close) < 0.0015) and (close > moving_average_100):
                                    momentum_list.append(symbol)
                                    continue
                                elif (low < moving_average_100) and (close > moving_average_100):
                                    momentum_list.append(symbol)
                                    continue
                                elif (low < moving_average_100) and (close > moving_average_100):
                                    momentum_list.append(symbol)
                                    continue
                                elif (((close - moving_average_100) / close) > 0.0025) and (open_stock < moving_average_100):
                                    momentum_list.append(symbol)
                                    continue

                                elif ((abs(moving_average_200 - low) / close) < 0.0015) and (close > moving_average_200):
                                    momentum_list.append(symbol)
                                    continue
                                elif (low < moving_average_200) and (close > moving_average_200):
                                    momentum_list.append(symbol)
                                    continue
                                elif (low < moving_average_200) and (close > moving_average_200):
                                    momentum_list.append(symbol)
                                    continue
                                elif (((close - moving_average_200) / close) > 0.0025) and (open_stock < moving_average_200):
                                    momentum_list.append(symbol)
                                    continue
                                else:
                                    continue
                    except:
                        pass

                    try:
                        try:
                            output = TA_Handler(symbol=symbol,
                                                screener="america",
                                                exchange="OTC",
                                                interval=Interval.INTERVAL_1_DAY)
                            bos = output.get_analysis().summary
                        except:
                            bos = recommendation_summary_technical(symbol)
                        if (bos["RECOMMENDATION"] == "BUY") or (bos["RECOMMENDATION"] == "STRONG_BUY"):
                            try:
                                indicator = output.get_analysis().indicators
                            except:
                                indicator = handlerData(symbol)
                            close = indicator["close"]
                            open_stock = indicator["open"]
                            high = indicator["high"]
                            low = indicator["low"]

                            moving_average_20 = indicator["EMA20"]
                            moving_average_50 = indicator["EMA50"]
                            moving_average_100 = indicator["EMA100"]
                            moving_average_200 = indicator["EMA200"]
                            if indicator["change"] >= 2.0 and ((close - open_stock) > 0):
                                if ((abs(moving_average_20 - low) / close) < 0.0015) and (close > moving_average_20):
                                    momentum_list.append(symbol)
                                    continue
                                elif (low < moving_average_20) and (close > moving_average_20):
                                    momentum_list.append(symbol)
                                    continue
                                elif (low < moving_average_20) and (close > moving_average_20):
                                    momentum_list.append(symbol)
                                    continue
                                elif (((close - moving_average_20) / close) > 0.0025) and (open_stock < moving_average_20):
                                    momentum_list.append(symbol)
                                    continue

                                elif ((abs(moving_average_50 - low) / close) < 0.0015) and (close > moving_average_50):
                                    momentum_list.append(symbol)
                                    continue
                                elif (low < moving_average_50) and (close > moving_average_50):
                                    momentum_list.append(symbol)
                                    continue
                                elif (low < moving_average_50) and (close > moving_average_50):
                                    momentum_list.append(symbol)
                                    continue
                                elif (((close - moving_average_50) / close) > 0.0025) and (open_stock < moving_average_50):
                                    momentum_list.append(symbol)
                                    continue

                                elif ((abs(moving_average_100 - low) / close) < 0.0015) and (close > moving_average_100):
                                    momentum_list.append(symbol)
                                    continue
                                elif (low < moving_average_100) and (close > moving_average_100):
                                    momentum_list.append(symbol)
                                    continue
                                elif (low < moving_average_100) and (close > moving_average_100):
                                    momentum_list.append(symbol)
                                    continue
                                elif (((close - moving_average_100) / close) > 0.0025) and (open_stock < moving_average_100):
                                    momentum_list.append(symbol)
                                    continue

                                elif ((abs(moving_average_200 - low) / close) < 0.0015) and (close > moving_average_200):
                                    momentum_list.append(symbol)
                                    continue
                                elif (low < moving_average_200) and (close > moving_average_200):
                                    momentum_list.append(symbol)
                                    continue
                                elif (low < moving_average_200) and (close > moving_average_200):
                                    momentum_list.append(symbol)
                                    continue
                                elif (((close - moving_average_200) / close) > 0.0025) and (open_stock < moving_average_200):
                                    momentum_list.append(symbol)
                                    continue
                                else:
                                    continue
                    except:
                        pass
                else:
                    continue
        except Exception as e:
            print(e)
            continue

    print(momentum_list)

    for element in momentum_list:
        symbol_arr.append(element)

    return symbol_arr

from urllib.request import urlopen
import certifi
import json

app_4 = Flask(__name__)
def get_jsonparsed_data(url):
    response = urlopen(url, cafile=certifi.where())
    data = response.read().decode("utf-8")
    return json.loads(data)
@app_4.route('/')
def american_stocks():
  response = ""
  symbol_arr = []
  close_arr = []
  volume_arr = []
  market_cap = []
  target_arr = []
  stoploss_arr = []
  timeframe_arr = []
  sector = []
  type_arr = []
  weight_arr = []
  volatility_estimated = []
  tgsl_range = []
  try:
    api_key = "095e35e3-f38b-4b48-98ce-5b1eee5765b3"
    ss = StockSymbol(api_key)
    symbol_only_list = ['AAPL', 'ABT', 'ADBE', 'ADI', 'ADP', 'ADSK', 'AEP', 'AFL', 'AJG', 'AMAT', 'AMD', 'AMGN', 'AMZN', 'ANET', 'AON', 'APD', 'APH', 'AVGO', 'AZO', 'BA', 'BAC', 'BK', 'BKNG', 'BMY', 'C', 'CARR', 'CAT', 'CDNS', 'CHTR', 'CI', 'CL', 'CMCSA', 'CME', 'CMG', 'COF', 'COP', 'COST', 'CRM', 'CSCO', 'CTAS', 'CVS', 'CVX', 'DFS', 'DHR', 'DIS', 'DLR', 'DUK', 'ECL', 'EMR', 'EOG', 'EQIX', 'FCX', 'FTNT', 'GD', 'GILD', 'GOOG', 'GOOGL', 'GS', 'GWW', 'HCA', 'HD', 'HLT', 'HON', 'IBM', 'ICE', 'INTC', 'INTU', 'JCI', 'JNJ', 'JPM', 'KLAC', 'KMI', 'KO', 'LIN', 'LLY', 'LMT', 'LOW', 'LRCX', 'MA', 'MAR', 'MCD', 'MCK', 'MDLZ', 'MDT', 'MET', 'MNST', 'MO', 'MPC', 'MRK', 'MS', 'MSI', 'NEM', 'NFLX', 'NKE', 'NOW', 'NSC', 'NVDA', 'NXPI', 'O', 'OKE', 'ORLY', 'PAYX', 'PEP', 'PG', 'PGR', 'PH', 'PLD', 'PM', 'PNC', 'PSA', 'PWR', 'PYPL', 'QCOM', 'RCL', 'ROP', 'RSG', 'SBUX', 'SNPS', 'SO', 'SPG', 'SYK', 'T', 'TFC', 'TJX', 'TMO', 'TMUS', 'TRV', 'TSLA', 'TT', 'TXN', 'UNH', 'UNP', 'UPS', 'USB', 'V', 'VRTX', 'VZ', 'WELL', 'WFC', 'ZTS']
    symbol_only_list_1 = ss.get_symbol_list(market="US", symbols_only=False)

    stock_list = []
    strong_buy = []
    strong_sell = []
    strong_buy_level_2 = []
    strong_sell_level_2 = []
    strong_buy_level_3 = []
    strong_sell_level_3 = []
    strong_buy_SAR_level_3 = []
    strong_sell_SAR_level_3 = []
    stock_list_buy_4 = []
    stock_list_sell_4 = []
    stock_numbers = []

    for i in range(len(symbol_only_list)):

        stock = symbol_only_list[i]

        stock_list.append(stock)
        stock_numbers.append(i)

    print(stock_list)
    n = len(stock_list)

    for j in range(n):
        print(j)
        try:
            try:
                output = TA_Handler(symbol=stock_list[j],
                                    screener="america",
                                    exchange="NASDAQ",
                                    interval=Interval.INTERVAL_1_DAY)

                bos = output.get_analysis().summary
            except:
                bos = recommendation_summary_technical(stock_list[j])

            if (bos["RECOMMENDATION"] == "BUY") or (bos["RECOMMENDATION"] == "STRONG_BUY"):
                strong_buy.append(stock_list[j])
                continue
            elif (bos["RECOMMENDATION"] == "SELL") or (bos["RECOMMENDATION"] == "STRONG_SELL"):
                strong_sell.append(stock_list[j])
                continue
        except:
            pass

        try:
            try:
                output = TA_Handler(symbol=stock_list[j],
                                    screener="america",
                                    exchange="NYSE",
                                    interval=Interval.INTERVAL_1_DAY)

                bos = output.get_analysis().summary
                if (bos["RECOMMENDATION"] == "BUY") or (bos["RECOMMENDATION"] == "STRONG_BUY"):
                    strong_buy.append(stock_list[j])
                    continue
                elif (bos["RECOMMENDATION"] == "SELL") or (bos["RECOMMENDATION"] == "STRONG_SELL"):
                    strong_sell.append(stock_list[j])
                    continue
            except:
                bos = recommendation_summary_technical(stock_list[j])
                if (bos["RECOMMENDATION"] == "BUY") or (bos["RECOMMENDATION"] == "STRONG_BUY"):
                    strong_buy.append(stock_list[j])
                    continue
                elif (bos["RECOMMENDATION"] == "SELL") or (bos["RECOMMENDATION"] == "STRONG_SELL"):
                    strong_sell.append(stock_list[j])
                    continue
        except:
            pass

        try:
            try:
                output = TA_Handler(symbol=stock_list[j],
                                    screener="america",
                                    exchange="AMEX",
                                    interval=Interval.INTERVAL_1_DAY)

                bos = output.get_analysis().summary
                if (bos["RECOMMENDATION"] == "BUY") or (bos["RECOMMENDATION"] == "STRONG_BUY"):
                    strong_buy.append(stock_list[j])
                    continue
                elif (bos["RECOMMENDATION"] == "SELL") or (bos["RECOMMENDATION"] == "STRONG_SELL"):
                    strong_sell.append(stock_list[j])
                    continue
            except:
                bos = recommendation_summary_technical(stock_list[j])
                if (bos["RECOMMENDATION"] == "BUY") or (bos["RECOMMENDATION"] == "STRONG_BUY"):
                    strong_buy.append(stock_list[j])
                    continue
                elif (bos["RECOMMENDATION"] == "SELL") or (bos["RECOMMENDATION"] == "STRONG_SELL"):
                    strong_sell.append(stock_list[j])
                    continue
        except:
            pass

        try:
            try:
                output = TA_Handler(symbol=stock_list[j],
                                    screener="america",
                                    exchange="OTC",
                                    interval=Interval.INTERVAL_1_DAY)

                bos = output.get_analysis().summary
                if (bos["RECOMMENDATION"] == "BUY") or (bos["RECOMMENDATION"] == "STRONG_BUY"):
                    strong_buy.append(stock_list[j])
                    continue
                elif (bos["RECOMMENDATION"] == "SELL") or (bos["RECOMMENDATION"] == "STRONG_SELL"):
                    strong_sell.append(stock_list[j])
                    continue
            except:
                bos = recommendation_summary_technical(stock_list[j])
                if (bos["RECOMMENDATION"] == "BUY") or (bos["RECOMMENDATION"] == "STRONG_BUY"):
                    strong_buy.append(stock_list[j])
                    continue
                elif (bos["RECOMMENDATION"] == "SELL") or (bos["RECOMMENDATION"] == "STRONG_SELL"):
                    strong_sell.append(stock_list[j])
                    continue
        except:
            pass

    print("Buy:", strong_buy)
    print("Sell:", strong_sell)

    strong_buy = sorted(set(strong_buy))
    strong_sell = sorted(set(strong_sell))

    m = len(strong_buy)
    o = len(strong_sell)

    print(m, o)

    def level_2():
        for j in range(m):
            print(j)
            try:
                try:
                    output = TA_Handler(symbol=strong_buy[j],
                                        screener="america",
                                        exchange="NASDAQ",
                                        interval=Interval.INTERVAL_1_DAY)

                    ind = output.get_analysis().indicators
                    if ind["change"] >= 2.0:
                        strong_buy_level_2.append(strong_buy[j])
                        continue
                except:
                    ind = handlerData(strong_buy[j])
                    print(ind)
                    if ind["change"] >= 2.0:
                        strong_buy_level_2.append(strong_buy[j])
                        continue
            except:
                pass

            try:
                try:
                    output = TA_Handler(symbol=strong_buy[j],
                                        screener="america",
                                        exchange="NYSE",
                                        interval=Interval.INTERVAL_1_DAY)

                    ind = output.get_analysis().indicators
                    if ind["change"] >= 2.0:
                        strong_buy_level_2.append(strong_buy[j])
                        continue

                except:
                    ind = handlerData(strong_buy[j])
                    print(ind)
                    if ind["change"] >= 2.0:
                        strong_buy_level_2.append(strong_buy[j])
                        continue
            except:
                pass

            try:
                try:
                    output = TA_Handler(symbol=strong_buy[j],
                                        screener="america",
                                        exchange="AMEX",
                                        interval=Interval.INTERVAL_1_DAY)

                    ind = output.get_analysis().indicators
                    print(ind)
                    if ind["change"] >= 2.0:
                        strong_buy_level_2.append(strong_buy[j])
                        continue

                except:
                    ind = handlerData(strong_buy[j])
                    print(ind)
                    if ind["change"] >= 2.0:
                        strong_buy_level_2.append(strong_buy[j])
                        continue
            except:
                pass

            try:
                try:
                    output = TA_Handler(symbol=strong_buy[j],
                                        screener="america",
                                        exchange="OTC",
                                        interval=Interval.INTERVAL_1_DAY)

                    ind = output.get_analysis().indicators
                    if ind["change"] >= 2.0:
                        strong_buy_level_2.append(strong_buy[j])
                        continue

                except:
                    ind = handlerData(strong_buy[j])
                    if ind["change"] >= 2.0:
                        print(ind)
                        strong_buy_level_2.append(strong_buy[j])
                        continue
            except:
                pass

        for j in range(o):
            try:
                try:
                    output = TA_Handler(symbol=strong_sell[j],
                                        screener="america",
                                        exchange="NASDAQ",
                                        interval=Interval.INTERVAL_1_DAY)

                    ind = output.get_analysis().indicators
                    if ind["change"] <= -2.0:
                        strong_sell_level_2.append(strong_sell[j])
                        continue
                except:
                    ind = handlerData(strong_sell[j])
                    print(ind)
                    if ind["change"] <= -2.0:
                        strong_sell_level_2.append(strong_sell[j])
                        continue
            except:
                pass

            try:
                try:
                    output = TA_Handler(symbol=strong_sell[j],
                                        screener="america",
                                        exchange="NYSE",
                                        interval=Interval.INTERVAL_1_DAY)

                    ind = output.get_analysis().indicators
                    print(ind)
                    if ind["change"] <= -2.0:
                        strong_sell_level_2.append(strong_sell[j])
                        continue
                except:
                    ind = handlerData(strong_sell[j])
                    print(ind)
                    if ind["change"] <= -2.0:
                        strong_sell_level_2.append(strong_sell[j])
                        continue
            except:
                pass

            try:
                try:
                    output = TA_Handler(symbol=strong_sell[j],
                                        screener="america",
                                        exchange="AMEX",
                                        interval=Interval.INTERVAL_1_DAY)

                    ind = output.get_analysis().indicators
                    if ind["change"] <= -2.0:
                        strong_sell_level_2.append(strong_sell[j])
                        continue
                except:
                    ind = handlerData(strong_sell[j])
                    if ind["change"] <= -2.0:
                        strong_sell_level_2.append(strong_sell[j])
                        continue
            except:
                pass

            try:
                try:
                    output = TA_Handler(symbol=strong_sell[j],
                                    screener="america",
                                    exchange="OTC",
                                    interval=Interval.INTERVAL_1_DAY)

                    ind = output.get_analysis().indicators
                    if ind["change"] <= -2.0:
                        strong_sell_level_2.append(strong_sell[j])
                        continue
                except:
                    ind = handlerData(strong_sell[j])
                    if ind["change"] <= -2.0:
                        strong_sell_level_2.append(strong_sell[j])
                        continue
            except:
                pass

        print("Buy - Level 2:", strong_buy_level_2)
        print("Sell - Level 2:", strong_sell_level_2)

    level_2()

    a = len(strong_buy_level_2)
    b = len(strong_sell_level_2)

    def level_3_buy():
        for i in range(a):
            print(i)
            try:
                output = TA_Handler(symbol=strong_buy_level_2[i],
                                    screener="america",
                                    exchange="NASDAQ",
                                    interval=Interval.INTERVAL_1_DAY)
                try:
                    indicator = output.get_analysis().indicators
                except:
                    indicator = handlerData(strong_buy_level_2[i])
                close = indicator["close"]
                open_stock = indicator["open"]
                high = indicator["high"]
                low = indicator["low"]

                moving_average_20 = indicator["EMA20"]
                moving_average_50 = indicator["EMA50"]
                moving_average_100 = indicator["EMA100"]
                moving_average_200 = indicator["EMA200"]

                if ((abs(moving_average_20 - low) / close) < 0.0015) and (close > moving_average_20):
                    strong_buy_level_3.append(strong_buy_level_2[i])
                    continue
                elif (low < moving_average_20) and (close > moving_average_20):
                    strong_buy_level_3.append(strong_buy_level_2[i])
                    continue
                elif (low < moving_average_20) and (close > moving_average_20):
                    strong_buy_level_3.append(strong_buy_level_2[i])
                    continue
                elif (((close - moving_average_20) / close) > 0.0025) and (close > moving_average_20) and (
                        open_stock < moving_average_20):
                    strong_buy_level_3.append(strong_buy_level_2[i])
                    continue

                elif ((abs(moving_average_50 - low) / close) < 0.0015) and (close > moving_average_50):
                    strong_buy_level_3.append(strong_buy_level_2[i])
                    continue
                elif (low < moving_average_50) and (close > moving_average_50):
                    strong_buy_level_3.append(strong_buy_level_2[i])
                    continue
                elif (low < moving_average_50) and (close > moving_average_50):
                    strong_buy_level_3.append(strong_buy_level_2[i])
                    continue
                elif (((close - moving_average_50) / close) > 0.0025) and (close > moving_average_50) and (
                        open_stock < moving_average_50):
                    strong_buy_level_3.append(strong_buy_level_2[i])
                    continue

                elif ((abs(moving_average_100 - low) / close) < 0.0015) and (close > moving_average_100):
                    strong_buy_level_3.append(strong_buy_level_2[i])
                    continue
                elif (low < moving_average_100) and (close > moving_average_100):
                    strong_buy_level_3.append(strong_buy_level_2[i])
                    continue
                elif (low < moving_average_100) and (close > moving_average_100):
                    strong_buy_level_3.append(strong_buy_level_2[i])
                    continue
                elif (((close - moving_average_100) / close) > 0.0025) and (close > moving_average_100) and (
                        open_stock < moving_average_100):
                    strong_buy_level_3.append(strong_buy_level_2[i])
                    continue

                elif ((abs(moving_average_200 - low) / close) < 0.0015) and (close > moving_average_200):
                    strong_buy_level_3.append(strong_buy_level_2[i])
                    continue
                elif (low < moving_average_200) and (close > moving_average_200):
                    strong_buy_level_3.append(strong_buy_level_2[i])
                    continue
                elif (low < moving_average_200) and (close > moving_average_200):
                    strong_buy_level_3.append(strong_buy_level_2[i])
                    continue
                elif (((close - moving_average_200) / close) > 0.0025) and (close > moving_average_200) and (
                        open_stock < moving_average_200):
                    strong_buy_level_3.append(strong_buy_level_2[i])
                    continue

            except:
                pass

            try:
                output = TA_Handler(symbol=strong_buy_level_2[i],
                                    screener="america",
                                    exchange="OTC",
                                    interval=Interval.INTERVAL_1_DAY)
                try:
                    indicator = output.get_analysis().indicators
                except:
                    indicator = handlerData(strong_buy_level_2[i])
                close = indicator["close"]
                open_stock = indicator["open"]
                high = indicator["high"]
                low = indicator["low"]

                moving_average_20 = indicator["EMA20"]
                moving_average_50 = indicator["EMA50"]
                moving_average_100 = indicator["EMA100"]
                moving_average_200 = indicator["EMA200"]

                if ((abs(moving_average_20 - low) / close) < 0.0015) and (close > moving_average_20):
                    strong_buy_level_3.append(strong_buy_level_2[i])
                    continue
                elif (low < moving_average_20) and (close > moving_average_20):
                    strong_buy_level_3.append(strong_buy_level_2[i])
                    continue
                elif (low < moving_average_20) and (close > moving_average_20):
                    strong_buy_level_3.append(strong_buy_level_2[i])
                    continue
                elif (((close - moving_average_20) / close) > 0.0025) and (close > moving_average_20) and (
                        open_stock < moving_average_20):
                    strong_buy_level_3.append(strong_buy_level_2[i])
                    continue

                elif ((abs(moving_average_50 - low) / close) < 0.0015) and (close > moving_average_50):
                    strong_buy_level_3.append(strong_buy_level_2[i])
                    continue
                elif (low < moving_average_50) and (close > moving_average_50):
                    strong_buy_level_3.append(strong_buy_level_2[i])
                    continue
                elif (low < moving_average_50) and (close > moving_average_50):
                    strong_buy_level_3.append(strong_buy_level_2[i])
                    continue
                elif (((close - moving_average_50) / close) > 0.0025) and (close > moving_average_50) and (
                        open_stock < moving_average_50):
                    strong_buy_level_3.append(strong_buy_level_2[i])
                    continue

                elif ((abs(moving_average_100 - low) / close) < 0.0015) and (close > moving_average_100):
                    strong_buy_level_3.append(strong_buy_level_2[i])
                    continue
                elif (low < moving_average_100) and (close > moving_average_100):
                    strong_buy_level_3.append(strong_buy_level_2[i])
                    continue
                elif (low < moving_average_100) and (close > moving_average_100):
                    strong_buy_level_3.append(strong_buy_level_2[i])
                    continue
                elif (((close - moving_average_100) / close) > 0.0025) and (close > moving_average_100) and (
                        open_stock < moving_average_100):
                    strong_buy_level_3.append(strong_buy_level_2[i])
                    continue

                elif ((abs(moving_average_200 - low) / close) < 0.0015) and (close > moving_average_200):
                    strong_buy_level_3.append(strong_buy_level_2[i])
                    continue
                elif (low < moving_average_200) and (close > moving_average_200):
                    strong_buy_level_3.append(strong_buy_level_2[i])
                    continue
                elif (low < moving_average_200) and (close > moving_average_200):
                    strong_buy_level_3.append(strong_buy_level_2[i])
                    continue
                elif (((close - moving_average_200) / close) > 0.0025) and (close > moving_average_200) and (
                        open_stock < moving_average_200):
                    strong_buy_level_3.append(strong_buy_level_2[i])
                    continue

            except:
                pass

            try:
                output = TA_Handler(symbol=strong_buy_level_2[i],
                                    screener="america",
                                    exchange="NYSE",
                                    interval=Interval.INTERVAL_1_DAY)
                try:
                    indicator = output.get_analysis().indicators
                except:
                    indicator = handlerData(strong_buy_level_2[i])
                close = indicator["close"]
                open_stock = indicator["open"]
                high = indicator["high"]
                low = indicator["low"]

                moving_average_20 = indicator["EMA20"]
                moving_average_50 = indicator["EMA50"]
                moving_average_100 = indicator["EMA100"]
                moving_average_200 = indicator["EMA200"]

                if ((abs(moving_average_20 - low) / close) < 0.0015) and (close > moving_average_20):
                    strong_buy_level_3.append(strong_buy_level_2[i])
                    continue
                elif (low < moving_average_20) and (close > moving_average_20):
                    strong_buy_level_3.append(strong_buy_level_2[i])
                    continue
                elif (low < moving_average_20) and (close > moving_average_20):
                    strong_buy_level_3.append(strong_buy_level_2[i])
                    continue
                elif (((close - moving_average_20) / close) > 0.0025) and (close > moving_average_20) and (
                        open_stock < moving_average_20):
                    strong_buy_level_3.append(strong_buy_level_2[i])
                    continue

                elif ((abs(moving_average_50 - low) / close) < 0.0015) and (close > moving_average_50):
                    strong_buy_level_3.append(strong_buy_level_2[i])
                    continue
                elif (low < moving_average_50) and (close > moving_average_50):
                    strong_buy_level_3.append(strong_buy_level_2[i])
                    continue
                elif (low < moving_average_50) and (close > moving_average_50):
                    strong_buy_level_3.append(strong_buy_level_2[i])
                    continue
                elif (((close - moving_average_50) / close) > 0.0025) and (close > moving_average_50) and (
                        open_stock < moving_average_50):
                    strong_buy_level_3.append(strong_buy_level_2[i])
                    continue

                elif ((abs(moving_average_100 - low) / close) < 0.0015) and (close > moving_average_100):
                    strong_buy_level_3.append(strong_buy_level_2[i])
                    continue
                elif (low < moving_average_100) and (close > moving_average_100):
                    strong_buy_level_3.append(strong_buy_level_2[i])
                    continue
                elif (low < moving_average_100) and (close > moving_average_100):
                    strong_buy_level_3.append(strong_buy_level_2[i])
                    continue
                elif (((close - moving_average_100) / close) > 0.0025) and (close > moving_average_100) and (
                        open_stock < moving_average_100):
                    strong_buy_level_3.append(strong_buy_level_2[i])
                    continue

                elif ((abs(moving_average_200 - low) / close) < 0.0015) and (close > moving_average_200):
                    strong_buy_level_3.append(strong_buy_level_2[i])
                    continue
                elif (low < moving_average_200) and (close > moving_average_200):
                    strong_buy_level_3.append(strong_buy_level_2[i])
                    continue
                elif (low < moving_average_200) and (close > moving_average_200):
                    strong_buy_level_3.append(strong_buy_level_2[i])
                    continue
                elif (((close - moving_average_200) / close) > 0.0025) and (close > moving_average_200) and (
                        open_stock < moving_average_200):
                    strong_buy_level_3.append(strong_buy_level_2[i])
                    continue

            except:
                pass

            try:
                output = TA_Handler(symbol=strong_buy_level_2[i],
                                    screener="america",
                                    exchange="AMEX",
                                    interval=Interval.INTERVAL_1_DAY)
                try:
                    indicator = output.get_analysis().indicators
                except:
                    indicator = handlerData(strong_buy_level_2[i])
                close = indicator["close"]
                open_stock = indicator["open"]
                high = indicator["high"]
                low = indicator["low"]

                moving_average_20 = indicator["EMA20"]
                moving_average_50 = indicator["EMA50"]
                moving_average_100 = indicator["EMA100"]
                moving_average_200 = indicator["EMA200"]

                if ((abs(moving_average_20 - low) / close) < 0.0015) and (close > moving_average_20):
                    strong_buy_level_3.append(strong_buy_level_2[i])
                    continue
                elif (low < moving_average_20) and (close > moving_average_20):
                    strong_buy_level_3.append(strong_buy_level_2[i])
                    continue
                elif (low < moving_average_20) and (close > moving_average_20):
                    strong_buy_level_3.append(strong_buy_level_2[i])
                    continue
                elif (((close - moving_average_20) / close) > 0.0025) and (close > moving_average_20) and (
                        open_stock < moving_average_20):
                    strong_buy_level_3.append(strong_buy_level_2[i])
                    continue

                elif ((abs(moving_average_50 - low) / close) < 0.0015) and (close > moving_average_50):
                    strong_buy_level_3.append(strong_buy_level_2[i])
                    continue
                elif (low < moving_average_50) and (close > moving_average_50):
                    strong_buy_level_3.append(strong_buy_level_2[i])
                    continue
                elif (low < moving_average_50) and (close > moving_average_50):
                    strong_buy_level_3.append(strong_buy_level_2[i])
                    continue
                elif (((close - moving_average_50) / close) > 0.0025) and (close > moving_average_50) and (
                        open_stock < moving_average_50):
                    strong_buy_level_3.append(strong_buy_level_2[i])
                    continue

                elif ((abs(moving_average_100 - low) / close) < 0.0015) and (close > moving_average_100):
                    strong_buy_level_3.append(strong_buy_level_2[i])
                    continue
                elif (low < moving_average_100) and (close > moving_average_100):
                    strong_buy_level_3.append(strong_buy_level_2[i])
                    continue
                elif (low < moving_average_100) and (close > moving_average_100):
                    strong_buy_level_3.append(strong_buy_level_2[i])
                    continue
                elif (((close - moving_average_100) / close) > 0.0025) and (close > moving_average_100) and (
                        open_stock < moving_average_100):
                    strong_buy_level_3.append(strong_buy_level_2[i])
                    continue

                elif ((abs(moving_average_200 - low) / close) < 0.0015) and (close > moving_average_200):
                    strong_buy_level_3.append(strong_buy_level_2[i])
                    continue
                elif (low < moving_average_200) and (close > moving_average_200):
                    strong_buy_level_3.append(strong_buy_level_2[i])
                    continue
                elif (low < moving_average_200) and (close > moving_average_200):
                    strong_buy_level_3.append(strong_buy_level_2[i])
                    continue
                elif (((close - moving_average_200) / close) > 0.0025) and (close > moving_average_200) and (
                        open_stock < moving_average_200):
                    strong_buy_level_3.append(strong_buy_level_2[i])
                    continue

            except:
                continue

        print("Buy - Level 3 - EMA:", strong_buy_level_3)

    level_3_buy()

    def level_3_sell():
        for i in range(b):
            print(i)
            try:
                output = TA_Handler(symbol=strong_sell_level_2[i],
                                    screener="america",
                                    exchange="NASDAQ",
                                    interval=Interval.INTERVAL_1_DAY)
                try:
                    indicator = output.get_analysis().indicators
                except:
                    indicator = handlerData(strong_sell_level_2[i])
                close = indicator["close"]
                open_stock = indicator["open"]
                high = indicator["high"]
                low = indicator["low"]

                moving_average_20 = indicator["EMA20"]
                moving_average_50 = indicator["EMA50"]
                moving_average_100 = indicator["EMA100"]
                moving_average_200 = indicator["EMA200"]

                if ((abs(moving_average_20 - high) / close) < 0.0015) and (close < moving_average_20):
                    strong_sell_level_3.append(strong_sell_level_2[i])
                    continue
                elif (high > moving_average_20) and (close < moving_average_20):
                    strong_sell_level_3.append(strong_sell_level_2[i])
                    continue
                elif (high > moving_average_20) and (close < moving_average_20):
                    strong_sell_level_3.append(strong_sell_level_2[i])
                    continue
                elif ((abs(close - moving_average_20) / close) < 0.0025) and (close < moving_average_20) and (open_stock > moving_average_20):
                    strong_sell_level_3.append(strong_sell_level_2[i])
                    continue

                elif ((abs(moving_average_50 - high) / close) < 0.0015) and (close < moving_average_50):
                    strong_sell_level_3.append(strong_sell_level_2[i])
                    continue
                elif (high > moving_average_50) and (close < moving_average_50):
                    strong_sell_level_3.append(strong_sell_level_2[i])
                    continue
                elif (high > moving_average_50) and (close < moving_average_50):
                    strong_sell_level_3.append(strong_sell_level_2[i])
                    continue
                elif ((abs(close - moving_average_50) / close) < 0.0025) and (close < moving_average_50) and (open_stock > moving_average_50):
                    strong_sell_level_3.append(strong_sell_level_2[i])
                    continue

                elif ((abs(moving_average_100 - high) / close) < 0.0015) and (close < moving_average_100):
                    strong_sell_level_3.append(strong_sell_level_2[i])
                    continue
                elif (high > moving_average_100) and (close < moving_average_100):
                    strong_sell_level_3.append(strong_sell_level_2[i])
                    continue
                elif (high > moving_average_100) and (close < moving_average_100):
                    strong_sell_level_3.append(strong_sell_level_2[i])
                    continue
                elif ((abs(close - moving_average_100) / close) < 0.0025) and (close < moving_average_100) and (open_stock > moving_average_100):
                    strong_sell_level_3.append(strong_sell_level_2[i])
                    continue

                elif ((abs(moving_average_200 - high) / close) < 0.0015) and (close < moving_average_200):
                    strong_sell_level_3.append(strong_sell_level_2[i])
                    continue
                elif (high > moving_average_200) and (close < moving_average_200):
                    strong_sell_level_3.append(strong_sell_level_2[i])
                    continue
                elif (high > moving_average_200) and (close < moving_average_200):
                    strong_sell_level_3.append(strong_sell_level_2[i])
                    continue
                elif ((abs(close - moving_average_200) / close) < 0.0025) and (close < moving_average_200) and (open_stock > moving_average_200):
                    strong_sell_level_3.append(strong_sell_level_2[i])
                    continue

            except Exception as e:
                pass

            try:
                output = TA_Handler(symbol=strong_sell_level_2[i],
                                    screener="america",
                                    exchange="NYSE",
                                    interval=Interval.INTERVAL_1_DAY)
                try:
                    indicator = output.get_analysis().indicators
                except:
                    indicator = handlerData(strong_sell_level_2[i])
                close = indicator["close"]
                open_stock = indicator["open"]
                high = indicator["high"]
                low = indicator["low"]

                moving_average_20 = indicator["EMA20"]
                moving_average_50 = indicator["EMA50"]
                moving_average_100 = indicator["EMA100"]
                moving_average_200 = indicator["EMA200"]

                if ((abs(moving_average_20 - high) / close) < 0.0015) and (close < moving_average_20):
                    strong_sell_level_3.append(strong_sell_level_2[i])
                    continue
                elif (high > moving_average_20) and (close < moving_average_20):
                    strong_sell_level_3.append(strong_sell_level_2[i])
                    continue
                elif (high > moving_average_20) and (close < moving_average_20):
                    strong_sell_level_3.append(strong_sell_level_2[i])
                    continue
                elif ((abs(close - moving_average_20) / close) < 0.0025) and (close < moving_average_20) and (open_stock > moving_average_20):
                    strong_sell_level_3.append(strong_sell_level_2[i])
                    continue

                elif ((abs(moving_average_50 - high) / close) < 0.0015) and (close < moving_average_50):
                    strong_sell_level_3.append(strong_sell_level_2[i])
                    continue
                elif (high > moving_average_50) and (close < moving_average_50):
                    strong_sell_level_3.append(strong_sell_level_2[i])
                    continue
                elif (high > moving_average_50) and (close < moving_average_50):
                    strong_sell_level_3.append(strong_sell_level_2[i])
                    continue
                elif ((abs(close - moving_average_50) / close) < 0.0025) and (close < moving_average_50) and (open_stock > moving_average_50):
                    strong_sell_level_3.append(strong_sell_level_2[i])
                    continue

                elif ((abs(moving_average_100 - high) / close) < 0.0015) and (close < moving_average_100):
                    strong_sell_level_3.append(strong_sell_level_2[i])
                    continue
                elif (high > moving_average_100) and (close < moving_average_100):
                    strong_sell_level_3.append(strong_sell_level_2[i])
                    continue
                elif (high > moving_average_100) and (close < moving_average_100):
                    strong_sell_level_3.append(strong_sell_level_2[i])
                    continue
                elif ((abs(close - moving_average_100) / close) < 0.0025) and (close < moving_average_100) and (open_stock > moving_average_100):
                    strong_sell_level_3.append(strong_sell_level_2[i])
                    continue

                elif ((abs(moving_average_200 - high) / close) < 0.0015) and (close < moving_average_200):
                    strong_sell_level_3.append(strong_sell_level_2[i])
                    continue
                elif (high > moving_average_200) and (close < moving_average_200):
                    strong_sell_level_3.append(strong_sell_level_2[i])
                    continue
                elif (high > moving_average_200) and (close < moving_average_200):
                    strong_sell_level_3.append(strong_sell_level_2[i])
                    continue
                elif ((abs(close - moving_average_200) / close) < 0.0025) and (close < moving_average_200) and (open_stock > moving_average_200):
                    strong_sell_level_3.append(strong_sell_level_2[i])
                    continue

            except Exception as e:
                pass

            try:
                output = TA_Handler(symbol=strong_sell_level_2[i],
                                    screener="america",
                                    exchange="OTC",
                                    interval=Interval.INTERVAL_1_DAY)
                try:
                    indicator = output.get_analysis().indicators
                except:
                    indicator = handlerData(strong_sell_level_2[i])
                close = indicator["close"]
                open_stock = indicator["open"]
                high = indicator["high"]
                low = indicator["low"]

                moving_average_20 = indicator["EMA20"]
                moving_average_50 = indicator["EMA50"]
                moving_average_100 = indicator["EMA100"]
                moving_average_200 = indicator["EMA200"]

                if ((abs(moving_average_20 - high) / close) < 0.0015) and (close < moving_average_20):
                    strong_sell_level_3.append(strong_sell_level_2[i])
                    continue
                elif (high > moving_average_20) and (close < moving_average_20):
                    strong_sell_level_3.append(strong_sell_level_2[i])
                    continue
                elif (high > moving_average_20) and (close < moving_average_20):
                    strong_sell_level_3.append(strong_sell_level_2[i])
                    continue
                elif ((abs(close - moving_average_20) / close) < 0.0025) and (close < moving_average_20) and (open_stock > moving_average_20):
                    strong_sell_level_3.append(strong_sell_level_2[i])
                    continue

                elif ((abs(moving_average_50 - high) / close) < 0.0015) and (close < moving_average_50):
                    strong_sell_level_3.append(strong_sell_level_2[i])
                    continue
                elif (high > moving_average_50) and (close < moving_average_50):
                    strong_sell_level_3.append(strong_sell_level_2[i])
                    continue
                elif (high > moving_average_50) and (close < moving_average_50):
                    strong_sell_level_3.append(strong_sell_level_2[i])
                    continue
                elif ((abs(close - moving_average_50) / close) < 0.0025) and (close < moving_average_50) and (open_stock > moving_average_50):
                    strong_sell_level_3.append(strong_sell_level_2[i])
                    continue

                elif ((abs(moving_average_100 - high) / close) < 0.0015) and (close < moving_average_100):
                    strong_sell_level_3.append(strong_sell_level_2[i])
                    continue
                elif (high > moving_average_100) and (close < moving_average_100):
                    strong_sell_level_3.append(strong_sell_level_2[i])
                    continue
                elif (high > moving_average_100) and (close < moving_average_100):
                    strong_sell_level_3.append(strong_sell_level_2[i])
                    continue
                elif ((abs(close - moving_average_100) / close) < 0.0025) and (close < moving_average_100) and (open_stock > moving_average_100):
                    strong_sell_level_3.append(strong_sell_level_2[i])
                    continue

                elif ((abs(moving_average_200 - high) / close) < 0.0015) and (close < moving_average_200):
                    strong_sell_level_3.append(strong_sell_level_2[i])
                    continue
                elif (high > moving_average_200) and (close < moving_average_200):
                    strong_sell_level_3.append(strong_sell_level_2[i])
                    continue
                elif (high > moving_average_200) and (close < moving_average_200):
                    strong_sell_level_3.append(strong_sell_level_2[i])
                    continue
                elif ((abs(close - moving_average_200) / close) < 0.0025) and (close < moving_average_200) and (open_stock > moving_average_200):
                    strong_sell_level_3.append(strong_sell_level_2[i])
                    continue

            except Exception as e:
                pass

            try:
                output = TA_Handler(symbol=strong_sell_level_2[i],
                                    screener="america",
                                    exchange="AMEX",
                                    interval=Interval.INTERVAL_1_DAY)
                try:
                    indicator = output.get_analysis().indicators
                except:
                    indicator = handlerData(strong_sell_level_2[i])
                print(indicator)
                close = indicator["close"]
                open_stock = indicator["open"]
                high = indicator["high"]
                low = indicator["low"]

                moving_average_20 = indicator["EMA20"]
                moving_average_50 = indicator["EMA50"]
                moving_average_100 = indicator["EMA100"]
                moving_average_200 = indicator["EMA200"]

                if ((abs(moving_average_20 - high) / close) < 0.0015) and (close < moving_average_20):
                    strong_sell_level_3.append(strong_sell_level_2[i])
                    continue
                elif (high > moving_average_20) and (close < moving_average_20):
                    strong_sell_level_3.append(strong_sell_level_2[i])
                    continue
                elif (high > moving_average_20) and (close < moving_average_20):
                    strong_sell_level_3.append(strong_sell_level_2[i])
                    continue
                elif ((abs(close - moving_average_20) / close) < 0.0025) and (close < moving_average_20) and (open_stock > moving_average_20):
                    strong_sell_level_3.append(strong_sell_level_2[i])
                    continue

                elif ((abs(moving_average_50 - high) / close) < 0.0015) and (close < moving_average_50):
                    strong_sell_level_3.append(strong_sell_level_2[i])
                    continue
                elif (high > moving_average_50) and (close < moving_average_50):
                    strong_sell_level_3.append(strong_sell_level_2[i])
                    continue
                elif (high > moving_average_50) and (close < moving_average_50):
                    strong_sell_level_3.append(strong_sell_level_2[i])
                    continue
                elif ((abs(close - moving_average_50) / close) < 0.0025) and (close < moving_average_50) and (open_stock > moving_average_50):
                    strong_sell_level_3.append(strong_sell_level_2[i])
                    continue

                elif ((abs(moving_average_100 - high) / close) < 0.0015) and (close < moving_average_100):
                    strong_sell_level_3.append(strong_sell_level_2[i])
                    continue
                elif (high > moving_average_100) and (close < moving_average_100):
                    strong_sell_level_3.append(strong_sell_level_2[i])
                    continue
                elif (high > moving_average_100) and (close < moving_average_100):
                    strong_sell_level_3.append(strong_sell_level_2[i])
                    continue
                elif ((abs(close - moving_average_100) / close) < 0.0025) and (close < moving_average_100) and (open_stock > moving_average_100):
                    strong_sell_level_3.append(strong_sell_level_2[i])
                    continue

                elif ((abs(moving_average_200 - high) / close) < 0.0015) and (close < moving_average_200):
                    strong_sell_level_3.append(strong_sell_level_2[i])
                    continue
                elif (high > moving_average_200) and (close < moving_average_200):
                    strong_sell_level_3.append(strong_sell_level_2[i])
                    continue
                elif (high > moving_average_200) and (close < moving_average_200):
                    strong_sell_level_3.append(strong_sell_level_2[i])
                    continue
                elif ((abs(close - moving_average_200) / close) < 0.0025) and (close < moving_average_200) and (open_stock > moving_average_200):
                    strong_sell_level_3.append(strong_sell_level_2[i])
                    continue

            except Exception as e:
                pass

        print("Sell - Level 3 - EMA:", strong_sell_level_3)

    level_3_sell()

    len_buy = len(strong_buy_level_3)
    len_sell = len(strong_sell_level_3)

    def level_3_SAR_buy():
        for i in range(len_buy):
            try:
                try:
                    output = TA_Handler(symbol=strong_buy_level_3[i],
                                        screener="america",
                                        exchange="NASDAQ",
                                        interval=Interval.INTERVAL_1_DAY)
                    indicator = output.get_analysis().indicators
                    SAR = indicator["P.SAR"]
                    price = indicator["close"]
                    open_stock = indicator["open"]
                    if price > open_stock:
                        if price > SAR:
                            strong_buy_SAR_level_3.append(strong_buy_level_3[i])
                            continue
                        else:
                            pass
                except:
                    indicator = handlerData(strong_buy_level_3[i])
                    SAR = indicator["P.SAR"]
                    price = indicator["close"]
                    open_stock = indicator["open"]
                    if price > open_stock:
                        if price > SAR:
                            strong_buy_SAR_level_3.append(strong_buy_level_3[i])
                            continue
                        else:
                            pass
            except:
                pass

            try:
                try:
                    output = TA_Handler(symbol=strong_buy_level_3[i],
                                        screener="america",
                                        exchange="AMEX",
                                        interval=Interval.INTERVAL_1_DAY)
                    indicator = output.get_analysis().indicators
                    SAR = indicator["P.SAR"]
                    price = indicator["close"]
                    open_stock = indicator["open"]
                    if price > open_stock:
                        if price > SAR:
                            strong_buy_SAR_level_3.append(strong_buy_level_3[i])
                            continue
                        else:
                            pass

                except:
                    indicator = handlerData(strong_buy_level_3[i])
                    SAR = indicator["P.SAR"]
                    price = indicator["close"]
                    open_stock = indicator["open"]
                    if price > open_stock:
                        if price > SAR:
                            strong_buy_SAR_level_3.append(strong_buy_level_3[i])
                            continue
                        else:
                            pass
            except:
                pass

            try:
                try:
                    output = TA_Handler(symbol=strong_buy_level_3[i],
                                        screener="america",
                                        exchange="OTC",
                                        interval=Interval.INTERVAL_1_DAY)
                    indicator = output.get_analysis().indicators
                    SAR = indicator["P.SAR"]
                    price = indicator["close"]
                    open_stock = indicator["open"]
                    if price > open_stock:
                        if price > SAR:
                            strong_buy_SAR_level_3.append(strong_buy_level_3[i])
                            continue
                        else:
                            pass
                except:
                    indicator = handlerData(strong_buy_level_3[i])
                    SAR = indicator["P.SAR"]
                    price = indicator["close"]
                    open_stock = indicator["open"]
                    if price > open_stock:
                        if price > SAR:
                            strong_buy_SAR_level_3.append(strong_buy_level_3[i])
                            continue
                        else:
                            pass
            except:
                pass

            try:
                try:
                    output = TA_Handler(symbol=strong_buy_level_3[i],
                                        screener="america",
                                        exchange="NYSE",
                                        interval=Interval.INTERVAL_1_DAY)
                    indicator = output.get_analysis().indicators
                    SAR = indicator["P.SAR"]
                    price = indicator["close"]
                    open_stock = indicator["open"]
                    if price > open_stock:
                        if price > SAR:
                            strong_buy_SAR_level_3.append(strong_buy_level_3[i])
                            continue
                        else:
                            pass
                except:
                    indicator = handlerData(strong_buy_level_3[i])
                    SAR = indicator["P.SAR"]
                    price = indicator["close"]
                    open_stock = indicator["open"]
                    if price > open_stock:
                        if price > SAR:
                            strong_buy_SAR_level_3.append(strong_buy_level_3[i])
                            continue
                        else:
                            pass
            except:
                pass
        print("Level 3 - SAR Buy", strong_buy_SAR_level_3)

    def level_3_SAR_sell():
        for i in range(len_sell):
            try:
                try:
                    output = TA_Handler(symbol=strong_sell_level_3[i],
                                        screener="america",
                                        exchange="NASDAQ",
                                        interval=Interval.INTERVAL_1_DAY)
                    indicator = output.get_analysis().indicators
                    SAR = indicator["P.SAR"]
                    price = indicator["close"]
                    open_stock = indicator["open"]
                    if price < open_stock:
                        if price < SAR:
                            strong_sell_SAR_level_3.append(strong_sell_level_3[i])
                            continue
                        else:
                            pass
                except:
                    indicator = handlerData(strong_sell_level_3[i])
                    SAR = indicator["P.SAR"]
                    price = indicator["close"]
                    open_stock = indicator["open"]
                    if price < open_stock:
                        if price < SAR:
                            strong_sell_SAR_level_3.append(strong_sell_level_3[i])
                            continue
                        else:
                            pass
            except:
                pass

            try:
                try:
                    output = TA_Handler(symbol=strong_sell_level_3[i],
                                        screener="america",
                                        exchange="AMEX",
                                        interval=Interval.INTERVAL_1_DAY)
                    indicator = output.get_analysis().indicators
                    SAR = indicator["P.SAR"]
                    price = indicator["close"]
                    open_stock = indicator["open"]
                    if price < open_stock:
                        if price < SAR:
                            strong_sell_SAR_level_3.append(strong_sell_level_3[i])
                            continue
                        else:
                            pass
                except:
                    indicator = handlerData(strong_sell_level_3[i])
                    SAR = indicator["P.SAR"]
                    price = indicator["close"]
                    open_stock = indicator["open"]
                    if price < open_stock:
                        if price < SAR:
                            strong_sell_SAR_level_3.append(strong_sell_level_3[i])
                            continue
                        else:
                            pass
            except:
                pass

            try:
                try:
                    output = TA_Handler(symbol=strong_sell_level_3[i],
                                        screener="america",
                                        exchange="OTC",
                                        interval=Interval.INTERVAL_1_DAY)
                    indicator = output.get_analysis().indicators
                    SAR = indicator["P.SAR"]
                    price = indicator["close"]
                    open_stock = indicator["open"]
                    if price < open_stock:
                        if price < SAR:
                            strong_sell_SAR_level_3.append(strong_sell_level_3[i])
                            continue
                        else:
                            pass
                except:
                    indicator = handlerData(strong_sell_level_3[i])
                    SAR = indicator["P.SAR"]
                    price = indicator["close"]
                    open_stock = indicator["open"]
                    if price < open_stock:
                        if price < SAR:
                            strong_sell_SAR_level_3.append(strong_sell_level_3[i])
                            continue
                        else:
                            pass
            except:
                pass

            try:
                try:
                    output = TA_Handler(symbol=strong_sell_level_3[i],
                                        screener="america",
                                        exchange="NYSE",
                                        interval=Interval.INTERVAL_1_DAY)
                    indicator = output.get_analysis().indicators
                    SAR = indicator["P.SAR"]
                    price = indicator["close"]
                    open_stock = indicator["open"]
                    if price < open_stock:
                        if price < SAR:
                            strong_sell_SAR_level_3.append(strong_sell_level_3[i])
                            continue
                        else:
                            pass
                except:
                    indicator = handlerData(strong_sell_level_3[i])
                    SAR = indicator["P.SAR"]
                    price = indicator["close"]
                    open_stock = indicator["open"]
                    if price < open_stock:
                        if price < SAR:
                            strong_sell_SAR_level_3.append(strong_sell_level_3[i])
                            continue
                        else:
                            pass
            except:
                pass

        print("Level 3 - SAR Sell", strong_sell_SAR_level_3)

    level_3_SAR_buy()
    level_3_SAR_sell()

    len_buy_sar = len(strong_buy_SAR_level_3)
    len_sell_sar = len(strong_sell_SAR_level_3)

  except:
      pass

  print(strong_buy_SAR_level_3)
  symbols_vol = []#vol()
  strong_buy_SAR_level_3 = sorted(set(strong_buy_SAR_level_3 + symbols_vol))
  print(strong_buy_SAR_level_3)
  sym_call, sym_put, port_call, port_put = optimisation_portfolio(strong_buy_SAR_level_3, strong_sell_SAR_level_3)


  for i in range(len(strong_buy_SAR_level_3)):
      try:
          try:
              element = strong_buy_SAR_level_3[i]
              symbol_arr.append(element)
              element = element
              url = f"https://financialmodelingprep.com/api/v3/profile/{element}?apikey=HlLnwPHGLYdEUVKc6vEOY4e9SBDO9b7R"
              real_time_price = get_jsonparsed_data(url)[0]['price']
              ind_market_cap = get_jsonparsed_data(url)[0]['mktCap']
              ind_sector = get_jsonparsed_data(url)[0]['sector']
              t1, t2, t3, s1, s2, s3 = target_sl_buy(element)
              target_arr.append(t1)
              stoploss_arr.append(s1)
              volatility_estimated.append(f'{((t1/real_time_price) - 1) * 4:.2%}')
              url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{element}?apikey=HlLnwPHGLYdEUVKc6vEOY4e9SBDO9b7R"
              volume_ind = get_jsonparsed_data(url)['historical'][0]['volume']
              market_cap.append(ind_market_cap)
              sector.append(ind_sector)
              close_arr.append(real_time_price)
              volume_arr.append(volume_ind)
              type_arr.append("Buy")
              weight_arr.append(port_call[i])
              tgsl_range.append((t1 / real_time_price) - 1)
              timeframe_arr.append(7)

          except:
              element = strong_buy_SAR_level_3[i]
              symbol_arr.append(element)
              element = element + ".BO"
              url = f"https://financialmodelingprep.com/api/v3/profile/{element}?apikey=HlLnwPHGLYdEUVKc6vEOY4e9SBDO9b7R"
              real_time_price = get_jsonparsed_data(url)[0]['price']
              ind_market_cap = get_jsonparsed_data(url)[0]['mktCap']
              ind_sector = get_jsonparsed_data(url)[0]['sector']
              url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{element}?apikey=HlLnwPHGLYdEUVKc6vEOY4e9SBDO9b7R"
              volume_ind = get_jsonparsed_data(url)['historical'][0]['volume']
              market_cap.append(ind_market_cap)
              sector.append(ind_sector)
              close_arr.append(real_time_price)
              volume_arr.append(volume_ind)
              type_arr.append("Buy")
              weight_arr.append(port_call[i])

      except:
          len_arr = []
          len_arr.append(len(symbol_arr))
          len_arr.append(len(type_arr))
          len_arr.append(len(close_arr))
          len_arr.append(len(market_cap))
          len_arr.append(len(sector))
          len_arr.append(len(volume_arr))
          len_arr.append(len(weight_arr))
          len_arr.append(len(timeframe_arr))
          len_arr.append(len(target_arr))
          len_arr.append(len(stoploss_arr))
          len_arr.append(len(volatility_estimated))
          len_arr.append(len(tgsl_range))
          arrs = []
          arrs.append(tgsl_range)
          arrs.append(symbol_arr)
          arrs.append(type_arr)
          arrs.append(close_arr)
          arrs.append(market_cap)
          arrs.append(sector)
          arrs.append(volume_arr)
          arrs.append(weight_arr)
          arrs.append(timeframe_arr)
          arrs.append(target_arr)
          arrs.append(stoploss_arr)
          arrs.append(volatility_estimated)

          minimum = min(len_arr)

          for element_array in arrs:
              if len(element_array) > minimum:
                  element_diff = len(element_array) - minimum
                  for i in range(element_diff):
                      element_array.pop()

  for i in range(len(strong_sell_SAR_level_3)):
      try:
          try:
              element = strong_sell_SAR_level_3[i]
              symbol_arr.append(element)
              t1, t2, t3, s1, s2, s3 = target_sl_sell(element)
              target_arr.append(t1)
              stoploss_arr.append(s1)
              element = element
              url = f"https://financialmodelingprep.com/api/v3/profile/{element}?apikey=HlLnwPHGLYdEUVKc6vEOY4e9SBDO9b7R"
              real_time_price = get_jsonparsed_data(url)[0]['price']
              ind_market_cap = get_jsonparsed_data(url)[0]['mktCap']
              ind_sector = get_jsonparsed_data(url)[0]['sector']
              url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{element}?apikey=HlLnwPHGLYdEUVKc6vEOY4e9SBDO9b7R"
              volume_ind = get_jsonparsed_data(url)['historical'][0]['volume']
              market_cap.append(ind_market_cap)
              sector.append(ind_sector)
              close_arr.append(real_time_price)
              volume_arr.append(volume_ind)
              type_arr.append("Sell")
              weight_arr.append(port_put[i])
              volatility_estimated.append(f'{((t1/real_time_price) - 1) * 4:.2%}')
              tgsl_range.append((-(t1 / real_time_price)) + 1)
              timeframe_arr.append(7)
          except:
              element = strong_sell_SAR_level_3[i]
              symbol_arr.append(element)
              element = element + ".BO"
              url = f"https://financialmodelingprep.com/api/v3/profile/{element}?apikey=HlLnwPHGLYdEUVKc6vEOY4e9SBDO9b7R"
              real_time_price = get_jsonparsed_data(url)[0]['price']
              ind_market_cap = get_jsonparsed_data(url)[0]['mktCap']
              ind_sector = get_jsonparsed_data(url)[0]['sector']
              url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{element}?apikey=HlLnwPHGLYdEUVKc6vEOY4e9SBDO9b7R"
              volume_ind = get_jsonparsed_data(url)['historical'][0]['volume']
              market_cap.append(ind_market_cap)
              sector.append(ind_sector)
              close_arr.append(real_time_price)
              volume_arr.append(volume_ind)
              type_arr.append("Sell")
              weight_arr.append(port_put[i])
      except:
          len_arr = []
          len_arr.append(len(symbol_arr))
          len_arr.append(len(type_arr))
          len_arr.append(len(close_arr))
          len_arr.append(len(market_cap))
          len_arr.append(len(sector))
          len_arr.append(len(volume_arr))
          len_arr.append(len(weight_arr))
          len_arr.append(len(timeframe_arr))
          len_arr.append(len(target_arr))
          len_arr.append(len(stoploss_arr))
          len_arr.append(len(volatility_estimated))
          len_arr.append(len(tgsl_range))
          arrs = []
          arrs.append(tgsl_range)
          arrs.append(symbol_arr)
          arrs.append(type_arr)
          arrs.append(close_arr)
          arrs.append(market_cap)
          arrs.append(sector)
          arrs.append(volume_arr)
          arrs.append(weight_arr)
          arrs.append(timeframe_arr)
          arrs.append(target_arr)
          arrs.append(stoploss_arr)
          arrs.append(volatility_estimated)

          minimum = min(len_arr)

          for element_array in arrs:
              if len(element_array) > minimum:
                  element_diff = len(element_array) - minimum
                  for i in range(element_diff):
                      element_array.pop()

  print(weight_arr, tgsl_range)

  portfolio_target_return = np.dot(weight_arr, tgsl_range)/np.sum(weight_arr) * 0.45

  response += "Analysis Complete - please check your registered email address." + "\n"

  print(len(symbol_arr))
  print(len(type_arr))
  print(len(sector))
  print(len(market_cap))
  print(len(close_arr))
  print(len(volume_arr))
  print(len(weight_arr))
  print(len(timeframe_arr))
  print(len(target_arr))
  print(len(stoploss_arr))

  csv_data = {
      "Symbol": symbol_arr,
      "Execution": type_arr,
      "Sector": sector,
      "Market Capitalisation": market_cap,
      "Price": close_arr,
      "Volume": volume_arr,
      "Capital Allocation": weight_arr,
      "Timeframe": timeframe_arr,
      "Target": target_arr,
      "Stop Loss": stoploss_arr,
      "Portfolio Target Return": [f'{portfolio_target_return:.2%}'] + (['']*(len(stoploss_arr) - 1))
  }

  date_earn = (date.today() + timedelta(days=7))

  df_earnings_data = pd.DataFrame(csv_data)
  file_path = f'US_equity_{date_earn}.csv'

  df_earnings_data.to_csv(file_path, index=False)

  import smtplib
  from email.mime.multipart import MIMEMultipart
  from email.mime.text import MIMEText
  from email.mime.base import MIMEBase
  from email import encoders
  import os
  import subprocess
  import traceback
  import time

  def get_script_output(scriptpath):
      result = subprocess.run(['python', scriptpath], stdout=subprocess.PIPE, text=True)
      return result.stdout

  def send_email(sender_email, sender_password, recipient_emails, subject, body, attachment_path):
      msg = MIMEMultipart()
      msg['From'] = sender_email
      msg['To'] = ', '.join(recipient_emails)
      msg['Subject'] = subject

      msg.attach(MIMEText(body, 'plain'))

      with open(attachment_path, 'rb') as attachment:
          part = MIMEBase('application', 'octet-stream')
          part.set_payload(attachment.read())
          encoders.encode_base64(part)
          part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment_path)}')
          msg.attach(part)

      try:
          server = smtplib.SMTP('smtp.office365.com', 587)
          server.starttls()
          server.login(sender_email, sender_password)

          server.sendmail(sender_email, recipient_emails, msg.as_string())

          server.quit()

          print("Email sent successfully!")
      except smtplib.SMTPException as e:
          print(f"SMTP error occurred: {e}")
      except Exception as e:
          traceback.print_exc()
          print(f"Failed to send email. Error: {e}")

  if __name__ == "__main__":
      # Only send email if there are recommendations
      if len(df_earnings_data) > 0:
          message_mail = "Please find attached your requested report."

          sender_email = (os.getenv("SENDER_EMAIL", "signals@plutusadvisors.ai"))
          sender_password = os.getenv("SENDER_PASSWORD", "Plutus!23@advisors")
          subject = f"US Equity - Rolling Weekly Outcomes - {date_earn}"
          attachment_path = f"US_equity_{date_earn}.csv"

          # WEBAPP VERSION: Send to hardcoded email
          recipient_emails = ["param@corpgini.in"]

          try:
              server = smtplib.SMTP('smtp.office365.com', 587)
              server.starttls()
              server.login(sender_email, sender_password)

              send_email(sender_email, sender_password, recipient_emails, subject, str(message_mail), attachment_path)

              server.quit()
              print(f"Email sent successfully to {recipient_emails[0]}!")
          except smtplib.SMTPException as e:
              print(f"SMTP error occurred: {e}")
          except Exception as e:
              traceback.print_exc()
              print(f"Failed to send email. Error: {e}")
      else:
          print("No recommendations for this week - email not sent.")

      time.sleep(10)

  response = "Analysis Complete - please check your registered email address." + "\n"

  return response


american_stocks()


