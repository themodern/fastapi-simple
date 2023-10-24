from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import Optional

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

@app.get("/index")
def index():
    return {"message": "Hello World"}


def connect_to_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class my_Research_Models(BaseModel):
    asset_name:     str = Field(min_length=1)
    model_name:     str = Field(min_length=1, max_length=100)
    market:         str = Field(min_length=1, max_length=100)
    currency:       str = Field(min_length=1, max_length=100)

class Update_my_Research_Models(BaseModel):
    asset_name:     Optional[str] = None
    model_name:     Optional[str] = None
    market:         Optional[str] = None
    currency:       Optional[str] = None





@app.get("/model/get_all_models")
def read_all_models_api(db: Session = Depends(connect_to_db)):
    return db.query(models.Research_Model).all()

# lookup the asset in target market
@app.get("/model/get_models/{model_market}")
def get_models_api(model_market:str, db: Session = Depends(connect_to_db)):
    my_Models = db.query(models.Research_Model).filter(models.Research_Model.market == model_market).all()

    if not my_Models:
        raise HTTPException(status_code=404, detail="No models found for the specified market")

    return my_Models

# lookup the asset in target market
@app.get("/model/get_model_asset_name/{asset_name}")
def get_models_api(asset_name:str, db: Session = Depends(connect_to_db)):
    my_Models = db.query(models.Research_Model).filter(models.Research_Model.asset_name == asset_name).all()

    if not my_Models:
        raise HTTPException(status_code=404, detail="No models found for the specified market")

    return my_Models

# lookup the asset in target market
@app.get("/model/get_models_model_name/{model_name}")
def get_models_api(model_name:str, db: Session = Depends(connect_to_db)):
    my_Models = db.query(models.Research_Model).filter(models.Research_Model.model_name == model_name).all()

    if not my_Models:
        raise HTTPException(status_code=404, detail="No models found for the specified model name")

    return my_Models

#################################################


#add new model function
@app.post("/model/post_new_model")
def create_new_model_api(myModel: my_Research_Models, db: Session = Depends(connect_to_db)):

    new_model = models.Research_Model()
    new_model.asset_name = myModel.asset_name
    new_model.model_name = myModel.model_name
    new_model.market = myModel.market
    new_model.currency = myModel.currency

    db.add(new_model)
    db.commit()

    return myModel


# update function 
@app.put("/model/update_model/{model_id}")
def update_model_api(model_id: int, update_Model: Update_my_Research_Models, db: Session = Depends(connect_to_db)):

    my_Model = db.query(models.Research_Model).filter(models.Research_Model.id == model_id).first()

    if my_Model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {model_id} : Does not exist"
        )

    if update_Model.asset_name != None:
        my_Model.asset_name = update_Model.asset_name
    if update_Model.model_name != None:
        my_Model.model_name = update_Model.model_name
    if update_Model.market != None:
        my_Model.market = update_Model.market
    if update_Model.currency is not None:
        my_Model.currency = update_Model.currency

    db.add(my_Model)
    db.commit()
    return {"message": "Book updated successfully"}


@app.delete("/model/delete_model/{model_id}")
def delete_model_api(model_id: int, db: Session = Depends(connect_to_db)):

    my_Model = db.query(models.Research_Model).filter(models.Research_Model.id == model_id).first()

    if my_Model is None:
        raise HTTPException(
            status_code=404,
            detail=f"Model ID {model_id} : Does not exist"
        )

    db.query(models.Research_Model).filter(models.Research_Model.id == model_id).delete()
    db.commit()
    return {"message": f"Model ID: {model_id} is deleted successfully"}




from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import pandas as pd
from io import BytesIO
import os


# Define the folder where you want to save the DataFrame as CSV
save_folder = "data/"  # Replace with your desired folder path

# Ensure the folder exists; create it if not
os.makedirs(save_folder, exist_ok=True)

@app.post("/upload-dataframe/")
async def upload_dataframe(file: UploadFile):
    try:
        if file.filename.endswith(".csv"):
            # Read the file contents as bytes
            file_contents = await file.read()
            
            # Convert bytes data to a file-like object (BytesIO)
            file_bytes = BytesIO(file_contents)
            
            # Read the DataFrame from the BytesIO object
            df = pd.read_csv(file_bytes)
            
            # Save the DataFrame as a CSV file
            csv_filename = os.path.join(save_folder, file.filename)
            df.to_csv(csv_filename, index=False)
            
            return JSONResponse(content={"message": "DataFrame uploaded and saved."})
        else:
            return JSONResponse(content={"error": "Only CSV files are allowed."})
    except Exception as e:
        return JSONResponse(content={"error": str(e)})


@app.get("/get-dataframe/")
async def get_dataframe(filename: str):
    # Specify the directory where your CSV files are located.
    data_folder = "data"

    # Check if the requested file exists in the data folder
    file_path = os.path.join(data_folder, filename)

    if os.path.exists(file_path) and filename.endswith(".csv"):
        # Read the CSV file into a DataFrame
        df = pd.read_csv(file_path)

        # Convert the DataFrame to a list of dictionaries (JSON-like format)
        dataframe_dict = df.to_dict(orient="records")

        return JSONResponse(content={"dataframe": dataframe_dict})
    else:
        return JSONResponse(content={"error": "File not found or not a valid CSV file."})
