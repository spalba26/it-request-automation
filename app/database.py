from sqlite3 import connect

def init_db():
    connection = None
    try:
        connection = connect("app/request.db")
        connection.execute("PRAGMA foreign_keys = ON")
        cursor = connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                request_type TEXT NOT NULL,
                requester_id TEXT NOT NULL,
                status TEXT NOT NULL,
                assigned_team TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS software_incidents (
                request_id INTEGER PRIMARY KEY,
                resource TEXT NOT NULL,
                description TEXT NOT NULL,
                impact TEXT NOT NULL,
                urgency TEXT NOT NULL,
                priority TEXT NOT NULL,
                FOREIGN KEY (request_id) REFERENCES requests (id)
            )
            """
        )
        connection.commit()
    finally:
        if connection:
            connection.close()
