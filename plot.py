import pandas as pd
import plotly.graph_objects as go

# Define column names based on your data
column_names = ['Date', 'Time', 'Open', 'High', 'Low', 'Close']

# Load the data from the CSV file, specifying the column names
df = pd.read_csv('ohlc_data.csv', names=column_names)

# Combine the Date and Time columns into a single DateTime column
df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])

# Create the candlestick chart
fig = go.Figure(data=[go.Candlestick(x=df['DateTime'],
                                     open=df['Open'],
                                     high=df['High'],
                                     low=df['Low'],
                                     close=df['Close'])])

# Update layout
fig.update_layout(title='Candlestick Chart',
                  xaxis_title='DateTime',
                  yaxis_title='Price',
                  xaxis_rangeslider_visible=False)

# Show the figure
fig.show()
