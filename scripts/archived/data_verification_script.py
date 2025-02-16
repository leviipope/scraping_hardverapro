import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("../../gpu_listings.db")
cursor = conn.cursor()

# Query data from the table
cursor.execute("SELECT * FROM gpu_listings")
rows = cursor.fetchall()

for row in rows:
    print(row)

# Close connection
conn.close()
