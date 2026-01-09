import sqlite3 
from ArduinoSensorITem import Sensor
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS sensors (
    id INTEGER PRIMARY KEY,
    title text,
    context text,
    code text
)
''')
conn.commit()


def add_new_arduino_sensor(item: Sensor):
    cursor.execute("INSERT INTO sensors VALUES (?,?,?)", item.title, item.context, item.code)
    conn.commit()

def get_all_sensors():
    items = []
    cursor.execute("SELECT * FROM sensors")
    all_sensors = cursor.fetchall()

    for i in all_sensors:
        items.append(Sensor(id=i[0], title=i[1], context=i[2], code=i[3]))
    
    return items
    
