import sqlite3
# Connect to the SQLite database
conn = sqlite3.connect("faces_log.db")
cursor = conn.cursor()

# Drop the old table (if it exists)
cursor.execute("DROP TABLE IF EXISTS face_logs")

# Create the new table with the image column
cursor.execute("""
CREATE TABLE face_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    image BLOB NOT NULL
)
""")

# Commit the changes
conn.commit()

# Close the connection
conn.close()