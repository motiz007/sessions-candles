import yfinance as yf
import pandas as pd
from datetime import datetime, time

# Function to fetch historical data
def fetch_data(ticker, start_date, end_date, interval='1h'):
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

    segmented_data = []

    # Iterate through each date in the data
    for date in pd.date_range(start=data.index.min().date(), end=data.index.max().date()):
        daily_data = data.loc[date.strftime('%Y-%m-%d')]
        day_segments = {}
        for segment, ((start_time, end_time), tz) in time_segments.items():
            segment_df = daily_data.tz_convert(tz)
            segment_df = segment_df.between_time(start_time, end_time)
            if not segment_df.empty:
                open_price = segment_df.iloc[0]['Open']
                high_price = segment_df['High'].max()
                low_price = segment_df['Low'].min()
                close_price = segment_df.iloc[-1]['Close']
                day_segments[segment] = {
                    'Open': open_price,
                    'High': high_price,
                    'Low': low_price,
                    'Close': close_price
                }
        if day_segments:
            segmented_data.append((date.strftime('%Y-%m-%d'), day_segments))

    return segmented_data

# Function to create candlesticks (OHLC data only)
def create_candles(segmented_data):
    candles = {}
    for date, segments in segmented_data:
        for segment, data in segments.items():
            if data['Open'] is not None:  # Check if the segment has any data
                if segment not in candles:
                    candles[segment] = pd.DataFrame(columns=['Date', 'Open', 'High', 'Low', 'Close'])
                new_row = pd.DataFrame({
                    'Date': [date],
                    'Open': [data['Open']],
                    'High': [data['High']],
                    'Low': [data['Low']],
                    'Close': [data['Close']]
                })
                # Ensure new_row is not empty or all-NA
                if not new_row.empty and not new_row.isna().all().all():
                    candles[segment] = pd.concat([candles[segment], new_row], ignore_index=True)
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
