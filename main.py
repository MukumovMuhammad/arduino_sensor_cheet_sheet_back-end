from typing import Annotated
from fastapi import Depends, Form, UploadFile, HTTPException, FastAPI
from ArduinoSensorITem import Sensor
from fastapi.staticfiles import StaticFiles
from db import *
import shutil
import os
import glob
import base64

UPLOAD_DIR = "images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI()

app.mount(f"/{UPLOAD_DIR}", StaticFiles(directory=UPLOAD_DIR), name=UPLOAD_DIR)

@app.get("/")
def read_root():
    return True


@app.post("/add_new_sensor")
async def add_new_sensor(
    title: Annotated[str, Form()], 
    context: Annotated[str, Form()], 
    code: Annotated[str, Form()], 
    picture: UploadFile, 
    db_conn: sqlite3.Connection = Depends(get_db)
):
    

    file_extension = os.path.splitext(picture.filename)[1]
    if file_extension.lower() not in ['.jpg', '.jpeg', '.png', '.gif']:
        raise HTTPException(status_code=400, detail="Invalid image format")
        return {
        "status": False, 
        "message": "this extension cannot be stored!",
        }

    file_location = os.path.join(UPLOAD_DIR, picture.filename)
    try:
        with open(file_location, "wb") as buffer:

            shutil.copyfileobj(picture.file, buffer) 
    finally:

        await picture.close() 

    item = Sensor(title, context, code, file_location) 
    add_new_arduino_sensor(item, db_conn)
    return {
        "status": True, 
        "message": "New Item is added!"
    }

@app.get("/get_all_sensors")
def get_all_sensors(db_conn: sqlite3.Connection = Depends(get_db)):
    items = fetch_all_sensors(db_conn)
    return {"status": True, "message": "Data has been fetched" , "items" : items}


@app.get("/get_sensor_image")
def get_sensor_image(image_id: int):
    files = glob.glob(f"{UPLOAD_DIR}/{image_id}.*")

    if not files:
        return {"error": "Image not found"}

    image_path = files[0]  # take first match

    with open(image_path, "rb") as img:
        encoded = base64.b64encode(img.read()).decode("utf-8")

    extension = image_path.split(".")[-1]

    return {
        "image_base64": encoded,
        "extension": extension
    }