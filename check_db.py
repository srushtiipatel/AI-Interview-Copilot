import sqlite3

# 1️⃣ Connect to your database file
conn = sqlite3.connect("interviews.db")  # Make sure the path is correct
cursor = conn.cursor()

# 2️⃣ Show all tables in the database
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables in database:", tables)

# 3️⃣ Fetch all saved interviews
cursor.execute("SELECT * FROM interviews;")
rows = cursor.fetchall()

print("\nAll saved interviews:")
for row in rows:
    print("ID:", row[0])
    print("Resume Name:", row[1])
    print("Questions:", row[2])
    print("Answer:", row[3])
    print("Technical Score:", row[4])
    print("Communication Score:", row[5])
    print("Confidence:", row[6])
    print("Timestamp:", row[7])
    print("-" * 50)

# 4️⃣ Close the connection
conn.close()