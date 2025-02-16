import sqlite3

# Database file
database_file = "../../gpu_listings.db"

# Connect to SQLite (creates the database file if it doesn't exist)
conn = sqlite3.connect(database_file)
cursor = conn.cursor()

# Create a table with appropriate data types
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

print("Database and table created successfully!")

# Commit and close the connection
conn.commit()
conn.close()
