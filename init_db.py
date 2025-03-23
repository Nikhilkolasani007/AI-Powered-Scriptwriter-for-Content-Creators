import sqlite3

# Connect to database (creates database.db if not exists)
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create a users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

# Commit and close connection
conn.commit()
conn.close()

print("Database setup completed successfully.")
