from sqlite3 import connect

DB_PATH = "app/request.db"

def init_db():
    connection = None
    try:
        connection = connect(DB_PATH)
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

def insert_software_incident(incident_data: dict) -> int:
    connection = None
    try:
        connection = connect(DB_PATH)
        connection.execute("PRAGMA foreign_keys = ON")
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO requests (request_type, requester_id, status, assigned_team) VALUES 
            (?, ?, ?, ?)""", (incident_data["request_type"], incident_data["requester_id"],
            incident_data["status"], incident_data["assigned_team"])
        )
        new_id = cursor.lastrowid
        cursor.execute(
            """
            INSERT INTO software_incidents (request_id, resource, description, impact, urgency, 
            priority) VALUES (?, ?, ?, ?, ?, ?)""", (new_id, incident_data["resource"],
            incident_data["description"], incident_data["impact"], incident_data["urgency"], incident_data["priority"])
        )
        connection.commit()
        return new_id
    except Exception:
        if connection:
            connection.rollback()
        raise
    finally:
        if connection:
            connection.close()