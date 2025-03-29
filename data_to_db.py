import csv
import sqlite3
import os
from datetime import datetime


def migrate_data_to_sqlite():
    """
    Migrates data from gpu_listings.csv to gpu_listings.db
    Treats the CSV as the source of truth and syncs the database accordingly
    """
    print("Starting data migration from CSV to SQLite...")

    # Define file paths
    csv_file_path = "gpu_listings.csv"
    db_file_path = "gpu_listings.db"

    # Check if CSV file exists
    if not os.path.exists(csv_file_path):
        print(f"Error: CSV file {csv_file_path} not found!")
        return

    # Connect to SQLite database (creates it if it doesn't exist)
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()

    # Check if table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='gpu_listings'")
    table_exists = cursor.fetchone() is not None

    if not table_exists:
        # Create table with the correct structure
        cursor.execute('''
            CREATE TABLE gpu_listings (
                id TEXT PRIMARY KEY,
                name TEXT,
                ti TEXT,
                price INTEGER,
                time TEXT,
                iced TEXT,
                link TEXT,
                date_added TEXT,
                archived TEXT
            )
        ''')
        conn.commit()
        print("Created new gpu_listings table")

    # Read CSV data
    csv_data = []
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as f:
            # Check CSV headers
            first_line = f.readline().strip()
            f.seek(0)  # Reset to beginning of file

            # Use fieldnames that match your CSV
            fieldnames = ['id', 'name', 'ti', 'price', 'time', 'iced', 'link', 'date_added', 'archived']
            csv_reader = csv.DictReader(f, fieldnames=fieldnames)

            # Skip header row if it exists
            if first_line.startswith('id,name,ti,price'):
                next(csv_reader)

            for row in csv_reader:
                try:
                    price = int(row.get('price', 0))
                except (ValueError, TypeError):
                    price = 0

                standardized_row = {
                    'id': row.get('id', ''),
                    'name': row.get('name', ''),
                    'ti': row.get('ti', 'False'),
                    'price': price,
                    'time': row.get('time', ''),
                    'iced': row.get('iced', 'False'),
                    'link': row.get('link', ''),
                    'date_added': row.get('date_added', ''),
                    'archived': row.get('archived', 'False')
                }
                csv_data.append(standardized_row)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    print(f"Read {len(csv_data)} listings from CSV file")

    # Get existing entries from the database with all their data
    cursor.execute("SELECT id, name, ti, price, time, iced, link, date_added, archived FROM gpu_listings")
    existing_data = {
        row[0]: dict(zip(['id', 'name', 'ti', 'price', 'time', 'iced', 'link', 'date_added', 'archived'], row)) for row
        in cursor.fetchall()}

    # Count operations
    new_entries = 0
    updated_entries = 0

    # Process each CSV row
    for item in csv_data:
        try:
            if item['id'] in existing_data:
                # Check if data has actually changed
                existing_item = existing_data[item['id']]
                if (str(existing_item['name']) != item['name'] or
                        str(existing_item['ti']) != item['ti'] or
                        existing_item['price'] != item['price'] or
                        str(existing_item['time']) != item['time'] or
                        str(existing_item['iced']) != item['iced'] or
                        str(existing_item['link']) != item['link'] or
                        str(existing_item['date_added']) != item['date_added'] or
                        str(existing_item['archived']) != item['archived']):
                    # Data has changed, update it
                    cursor.execute('''
                        UPDATE gpu_listings SET 
                        name = ?, ti = ?, price = ?, time = ?, 
                        iced = ?, link = ?, date_added = ?, archived = ?
                        WHERE id = ?
                    ''', (
                        item['name'], item['ti'], item['price'], item['time'],
                        item['iced'], item['link'], item['date_added'], item['archived'],
                        item['id']
                    ))
                    updated_entries += 1
            else:
                # New entry
                cursor.execute('''
                    INSERT INTO gpu_listings
                    (id, name, ti, price, time, iced, link, date_added, archived)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    item['id'], item['name'], item['ti'], item['price'],
                    item['time'], item['iced'], item['link'],
                    item['date_added'], item['archived']
                ))
                new_entries += 1

        except sqlite3.Error as e:
            print(f"Error processing item {item['id']}: {e}")

    # Commit changes
    conn.commit()

    # Count total entries in database
    cursor.execute("SELECT COUNT(*) FROM gpu_listings")
    total_entries = cursor.fetchone()[0]

    print(f"Migration complete: {new_entries} new entries added, {updated_entries} entries updated")
    print(f"Total entries in database: {total_entries}")

    conn.close()

if __name__ == "__main__":
    migrate_data_to_sqlite()