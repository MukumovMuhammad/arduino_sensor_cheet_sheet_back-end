from fastapi import FastAPI
from ArduinoSensorITem import Sensor
import db

app = FastAPI()



@app.get("/")
def read_root():
    return True


@app.get("/get_all_sensors")
def get_all_sensors():
    items = db.get_all_sensors()
    return {"items" : items}