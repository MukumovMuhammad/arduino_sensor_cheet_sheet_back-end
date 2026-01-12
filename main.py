from typing import Annotated
from fastapi import Depends, Form, UploadFile, HTTPException, FastAPI
from ArduinoSensorITem import Sensor
from db import *
import shutil
import os
import glob
import base64

UPLOAD_DIR = "uploaded_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI()



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
    item = Sensor(title, context, code) 
    item_id = add_new_arduino_sensor(item, db_conn)

    file_extension = os.path.splitext(picture.filename)[1]
    if file_extension.lower() not in ['.jpg', '.jpeg', '.png', '.gif']:
        raise HTTPException(status_code=400, detail="Invalid image format")
        delete_sensor(item_id, db_conn)
        return {
        "status": False, 
        "message": "this extension cannot be stored!",
        "item_id": item_id
        }

    file_location = os.path.join(UPLOAD_DIR, str(item_id) + file_extension)
    try:
        with open(file_location, "wb") as buffer:

            shutil.copyfileobj(picture.file, buffer) 
    except:
        delete_sensor(item_id, db_conn)
    finally:

        await picture.close() 
    
    return {
        "status": True, 
        "message": "New Item is added!",
        "item_id": item_id
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