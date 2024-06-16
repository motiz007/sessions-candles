import yfinance as yf
import pandas as pd
from datetime import datetime, time

# Function to fetch historical data
def fetch_data(ticker, start_date, end_date, interval='60m'):
    data = yf.download(ticker, start=start_date, end=end_date, interval=interval)
    return data

# Function to segment data into specific time zones and overlaps
def segment_data(data):
    data = data.reset_index()
    data['Datetime'] = pd.to_datetime(data['Datetime'])
    data.set_index('Datetime', inplace=True)

    time_segments = {
        'sydney_only': ((time(6, 0), time(8, 0)), 'Australia/Sydney'),
        'sydney_tokyo_overlap': ((time(8, 0), time(10, 0)), 'Australia/Sydney'),
        'tokyo_only': ((time(10, 0), time(13, 0)), 'Asia/Tokyo'),
        'tokyo_london_overlap': ((time(13, 0), time(16, 0)), 'Asia/Tokyo'),
        'london_only': ((time(16, 0), time(18, 0)), 'Europe/London'),
        'london_newyork_overlap': ((time(18, 0), time(21, 0)), 'Europe/London'),
        'newyork_only': ((time(21, 0), time(23, 59)), 'America/New_York'),
        'newyork_sydney_overlap': ((time(0, 0), time(6, 0)), 'America/New_York'),
    }

    segmented_data = {}

    for segment, ((start_time, end_time), tz) in time_segments.items():
        segment_df = data.between_time(start_time, end_time)
        segment_df = segment_df.tz_localize('UTC').tz_convert(tz)
        segmented_data[segment] = segment_df

    return segmented_data

# Function to create candlesticks
def create_candles(segmented_data):
    candles = {}
    for segment, data in segmented_data.items():
        if data.empty:
            continue
        ohlc = data.resample('1H').ohlc()
        candles[segment] = ohlc
    return candles

# Main function
def main():
    ticker = 'EURUSD=X'
    start_date = '2023-06-10'
    end_date = '2023-06-14'
    data = fetch_data(ticker, start_date, end_date)
    segmented_data = segment_data(data)
    candles = create_candles(segmented_data)
    
    for segment, candle_data in candles.items():
        print(f"{segment}:\n{candle_data}\n")

if __name__ == "__main__":
    main()
