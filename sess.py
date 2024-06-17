import yfinance as yf
import pandas as pd
from datetime import datetime, time
import json

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

    for date in pd.date_range(start=data.index.min().date(), end=data.index.max().date()):
        daily_data = data.loc[date.strftime('%Y-%m-%d')]
        for segment, ((start_time, end_time), tz) in time_segments.items():
            segment_df = daily_data.tz_convert(tz)
            segment_df = segment_df.between_time(start_time, end_time)
            if not segment_df.empty:
                open_price = segment_df.iloc[0]['Open']
                high_price = segment_df['High'].max()
                low_price = segment_df['Low'].min()
                close_price = segment_df.iloc[-1]['Close']
                start_datetime = datetime.combine(date, start_time)
                segmented_data.append({
                    'time': int(start_datetime.timestamp()),
                    'session': segment,
                    'open': open_price,
                    'high': high_price,
                    'low': low_price,
                    'close': close_price
                })

    return pd.DataFrame(segmented_data)

# Main function
def main():
    ticker = 'EURUSD=X'
    start_date = '2023-04-03'
    end_date = '2023-06-17'
    data = fetch_data(ticker, start_date, end_date)
    segmented_data = segment_data(data)
    
    # Save the data to a JSON file
    json_data = segmented_data.to_json(orient='records')
    with open('segmented_data.json', 'w') as f:
        f.write(json_data)

if __name__ == "__main__":
    main()
