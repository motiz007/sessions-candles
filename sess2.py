import pandas as pd
import re

# Step 1: Read the file and remove trailing commas
with open('eurusd_data.csv', 'r') as file:
    lines = file.readlines()

# Step 2: Write cleaned content to a new file
with open('cleaned_temp_eurusd_data.csv', 'w') as cleaned_file:
    for line in lines[2:]:  # Skip the first two lines
        cleaned_line = re.sub(r',\s*$', '', line) + '\n'  # Remove trailing commas, keep newline
        cleaned_file.write(cleaned_line)

# Step 3: Read the cleaned file into a pandas DataFrame
df = pd.read_csv('cleaned_temp_eurusd_data.csv')

# Step 4: Save the cleaned DataFrame to a new CSV file
df.to_csv('cleaned_eurusd_data.csv', index=False)

print("Data cleaning complete. Cleaned data saved to 'cleaned_eurusd_data.csv'.")
