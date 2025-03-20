import pandas as pd
from datetime import datetime
import sqlite3

# File paths
csv_file = "gpu_listings.csv"  # Your current CSV file
database_file = "gpu_listings.db"  # SQLite database file

# Read the CSV file into a Pandas DataFrame
try:
    df = pd.read_csv(csv_file)
    print(f"Loaded {len(df)} rows from '{csv_file}'.")
except FileNotFoundError:
    print(f"Error: File '{csv_file}' not found.")
    exit()

# Convert 'time' and 'date_added' columns to proper datetime format
try:
    df['time'] = pd.to_datetime(df['time'], errors='coerce')  # Handle invalid dates with NaT
    df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')  # Handle invalid dates with NaT
    print("Converted 'time' and 'date_added' columns to datetime format.")
except KeyError as e:
    print(f"Error: Missing column in CSV: {e}")
    exit()

# Connect to SQLite database
conn = sqlite3.connect(database_file)
cursor = conn.cursor()

# Create the table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS gpu_listings (
    id INTEGER PRIMARY KEY,
    name TEXT,
    ti BOOLEAN,
    price REAL,
    time DATETIME,
    iced BOOLEAN,
    link TEXT,
    date_added DATETIME,
    archived BOOLEAN
)
''')
print("Database table 'gpu_listings' ensured.")

# Insert new rows and update existing ones
new_rows_count = 0
updated_rows_count = 0

for _, row in df.iterrows():
    try:
        # Check if the row already exists in the database by ID
        cursor.execute("SELECT COUNT(*) FROM gpu_listings WHERE id = ?", (row['id'],))
        exists = cursor.fetchone()[0]

        # Format datetime values
        time_value = row['time'].strftime('%Y-%m-%d %H:%M:%S') if not pd.isna(row['time']) else None
        date_added_value = row['date_added'].strftime('%Y-%m-%d %H:%M:%S') if not pd.isna(row['date_added']) else None

        if not exists:  # If the row does not exist, insert it
            cursor.execute('''
            INSERT INTO gpu_listings (id, name, ti, price, time, iced, link, date_added, archived)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                row['id'],
                row['name'],
                row['ti'],
                row['price'],
                time_value,
                row['iced'],
                row['link'],
                date_added_value,
                row['archived']
            ))
            new_rows_count += 1
        else:  # If the row exists, update it
            cursor.execute('''
            UPDATE gpu_listings 
            SET name = ?, ti = ?, price = ?, time = ?, iced = ?, link = ?, date_added = ?, archived = ?
            WHERE id = ?
            ''', (
                row['name'],
                row['ti'],
                row['price'],
                time_value,
                row['iced'],
                row['link'],
                date_added_value,
                row['archived'],
                row['id']
            ))
            updated_rows_count += 1
    except sqlite3.Error as e:
        print(f"Error processing row with ID {row['id']}: {e}")

# Commit changes and close the connection
conn.commit()
conn.close()

print(f"{new_rows_count} new rows were inserted into the database.")
print(f"{updated_rows_count} existing rows were updated in the database.")