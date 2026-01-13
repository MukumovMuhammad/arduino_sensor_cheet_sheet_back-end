from typing import Annotated
from fastapi import Depends, Form, UploadFile, HTTPException, FastAPI
from ArduinoSensorITem import Sensor
from fastapi.staticfiles import StaticFiles
from db import *
import shutil
import os


scheme_imgs_dir = "scheme_imgs"
title_imgs_dir = "title_imgs"
os.makedirs(scheme_imgs_dir, exist_ok=True)
os.makedirs(title_imgs_dir, exist_ok=True)

app = FastAPI()

app.mount(f"/{scheme_imgs_dir}", StaticFiles(directory=scheme_imgs_dir), name=scheme_imgs_dir)
app.mount(f"/{title_imgs_dir}", StaticFiles(directory=title_imgs_dir), name=title_imgs_dir)


@app.get("/")
def read_root():
    return True


@app.post("/add_new_sensor")
async def add_new_sensor(
    title: Annotated[str, Form()], 
    context: Annotated[str, Form()], 
    code: Annotated[str, Form()], 
    title_img: UploadFile, 
    scheme_img: UploadFile,
    db_conn: sqlite3.Connection = Depends(get_db)
    ):

    title_ext = os.path.splitext(title_img.filename)[1]
    scheme_ext = os.path.splitext(scheme_img.filename)[1]
    if title_ext.lower() not in ['.jpg', '.jpeg', '.png', '.gif']:
        raise HTTPException(status_code=400, detail="Invalid image format")
    #Yes yes I am just making a copy and same check! I am too lazy to make it all in one condition!
    # This works fine! So leave it!
    if scheme_ext.lower() not in ['.jpg', '.jpeg', '.png', '.gif']:
        raise HTTPException(status_code=400, detail="Invalid image format")
    
    title_loc = os.path.join(title_imgs_dir, title_img.filename)
    scheme_loc = os.path.join(scheme_imgs_dir, scheme_img.filename)
    try:
        with open(title_loc, "wb") as buffer:
            shutil.copyfileobj(title_img.file, buffer) 
        
        with open(scheme_loc, "wb") as buffer:
            shutil.copyfileobj(scheme_img.file, buffer) 
    finally:

        await title_img.close() 
        await scheme_img.close() 

    item = Sensor(title, context, code, title_loc, scheme_loc) 
    add_new_arduino_sensor(item, db_conn)
    return {
        "status": True, 
        "message": "New Item is added!"
    }

@app.get("/get_all_sensors")
def get_all_sensors(db_conn: sqlite3.Connection = Depends(get_db)):
    items = fetch_all_sensors(db_conn)
    return {"status": True, "message": "Data has been fetched" , "items" : items}

