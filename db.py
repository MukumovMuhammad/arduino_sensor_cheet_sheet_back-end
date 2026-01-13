import sqlite3 
from typing import List
from ArduinoSensorITem import Sensor 

DATABASE_PATH = "database.db"



def get_db() -> sqlite3.Connection:
    """Creates a new database connection for each request."""
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    try:
        yield conn
    finally:

        conn.close()

# --- Database Initialization ---

def create_sensor_table():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sensors (
        id INTEGER PRIMARY KEY,
        title text,
        context text,
        code text,
        title_img text,
        scheme_image text
    )
    ''')
    conn.commit()
    conn.close()

create_sensor_table()



def add_new_arduino_sensor(item: Sensor, db_connection: sqlite3.Connection):
    """Inserts a new sensor record using the provided connection."""
    cursor = db_connection.cursor()

    cursor.execute("INSERT INTO sensors (title, context, code,title_img, scheme_image ) VALUES (?, ?,?,?,?)", 
                   item.get_values())
    db_connection.commit()

    

def fetch_all_sensors(db_connection: sqlite3.Connection) -> List[Sensor]:
    items = []
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM sensors")
    all_sensors = cursor.fetchall()    

    for item in all_sensors:
        items.append(Sensor(item[1],item[2],item[3],item[4], item[5], item[0]))
    return items


def delete_sensor(sensor_id: int, db_connection: sqlite3.Connection):
    cursor = db_connection.cursor()

    cursor.execute(
        "DELETE FROM sensors WHERE id = ?",
        (sensor_id,)
    )

    db_connection.commit()

    return cursor.rowcount
