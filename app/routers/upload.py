from fastapi import APIRouter, UploadFile, File, Form, HTTPException
import pandas as pd
from sqlalchemy.exc import IntegrityError
from app.models import tables_metadata
from app.crud import validate_and_convert_dataframe, insert_objects_in_db

router = APIRouter()

@router.post("/upload")
async def upload_file(type_: str = Form(...), file: UploadFile = File(...), has_header: bool = Form(True)):

    print("upload.py --> upload_file --> type_: " + str(type_) + "; file: " + str(file) + "; has_header: " + str(has_header))
    
    print("upload.py --> upload_file --> list(tables_metadata.keys()): " + str(list(tables_metadata.keys())))

    if type_ not in list(tables_metadata.keys()):
        raise HTTPException(status_code=400, detail=f"Tabla no reconocida. Usar uno de: {list(tables_metadata.keys())}")

    try:
        df = pd.read_csv(file.file, header=0 if has_header else None)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error leyendo CSV: {str(e)}")
        
    print("upload.py --> upload_file --> df = pd.read_csv(file.file, header=0 if has_header else None)")

    try:
        objects = validate_and_convert_dataframe(df, type_, has_header)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
        
    print("upload.py --> upload_file --> objects = validate_and_convert_dataframe(df, type_, has_header)")

    try:
        insert_objects_in_db(objects)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Error: claves duplicadas o violacion de integridad.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
        
    print("upload.py --> upload_file --> insert_objects_in_db(objects)")

    return {"message": f"{len(objects)} registros insertados en {type} exitosamente."}