from typing import Annotated
from fastapi import Depends, Form, UploadFile, HTTPException, FastAPI
from ArduinoSensorITem import Sensor
from db import *
import shutil
import os

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
    picture: UploadFile, # This parameter accepts the file
    db_conn: sqlite3.Connection = Depends(get_db)
):
    
    file_extension = os.path.splitext(picture.filename)[1]
    if file_extension.lower() not in ['.jpg', '.jpeg', '.png', '.gif']:
        raise HTTPException(status_code=400, detail="Invalid image format")

    file_location = os.path.join(UPLOAD_DIR, picture.filename)
    try:
        with open(file_location, "wb") as buffer:

            shutil.copyfileobj(picture.file, buffer) 
    finally:

        await picture.close() 
    item = Sensor(title, context, code, image_path=file_location) 
    add_new_arduino_sensor(item, db_conn)
    return {
        "status": True, 
        "message": "New Item is added!", 
        "image_path_saved": file_location
    }

@app.get("/get_all_sensors")
def get_all_sensors(db_conn: sqlite3.Connection = Depends(get_db)):
    items = fetch_all_sensors(db_conn)
    return {"status": True, "message": "Data has been fetched" , "items" : items}
