import pandas as pd
from datetime import datetime
import sqlite3

# File paths
csv_file = "../../gpu_listings.csv"  # Your current CSV file
database_file = "../../gpu_listings.db"  # SQLite database file

# Read the CSV file into a Pandas DataFrame
df = pd.read_csv(csv_file)

# Convert 'time' and 'date_added' columns to proper datetime format
df['time'] = pd.to_datetime(df['time'], errors='coerce')  # Handle invalid dates with NaT
df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')  # Handle invalid dates with NaT

# Connect to SQLite database
conn = sqlite3.connect(database_file)

# Insert data into the database
df.to_sql("gpu_listings", conn, if_exists="replace", index=False)

print("Data migrated successfully from CSV to SQLite!")

# Close the connection
conn.close()
