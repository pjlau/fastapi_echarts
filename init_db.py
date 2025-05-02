import sqlite3

# Connect to SQLite database (creates file if it doesn't exist)
conn = sqlite3.connect("data/sales.db")
cursor = conn.cursor()

# Create sales table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT NOT NULL,
        value INTEGER NOT NULL
    )
""")

# Insert sample data
sample_data = [
    ("Apples", 30),
    ("Bananas", 50),
    ("Oranges", 20),
    ("Grapes", 40),
    ("Pears", 25),
    ("Mangoes", 35)
]
cursor.executemany("INSERT OR REPLACE INTO sales (category, value) VALUES (?, ?)", sample_data)

# Commit and close
conn.commit()
conn.close()

print("Database initialized with sample data.")