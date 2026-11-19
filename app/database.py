from sqlite3 import connect

def init_db():
    connection = None
    try:
        connection = connect("app/request.db")
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
        connection.commit()
    finally:
        if connection:
            connection.close()
