from fastapi import FastAPI, Depends
from ArduinoSensorITem import Sensor
from db import *

app = FastAPI()



@app.get("/")
def read_root():
    return True


@app.post("/add_new_sensor")
def add_new_sensor(title: str, context: str, code: str, db_conn: sqlite3.Connection = Depends(get_db)):
    item = Sensor(title, context, code)
    add_new_arduino_sensor(item, db_conn)
    return {"status": True, "message": "New Item is added!"}

@app.get("/get_all_sensors")
def get_all_sensors(db_conn: sqlite3.Connection = Depends(get_db)):
    items = fetch_all_sensors(db_conn)
    return {"status": True, "message": "Data has been fetched" , "items" : items}