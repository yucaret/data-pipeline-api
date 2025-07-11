import fastapi
import sqlalchemy
import pandas
import pydantic
import psycopg2
import dotenv
import uvicorn
from fastapi import FastAPI
from app.routers import upload, batch, queries
from app.database import engine, Base
from app import models

def print_versions():
    print("Librerias instaladas:")
    print(f"- fastapi: {fastapi.__version__}")
    print(f"- sqlalchemy: {sqlalchemy.__version__}")
    print(f"- pandas: {pandas.__version__}")
    print(f"- pydantic: {pydantic.__version__}")
    print(f"- psycopg2: {psycopg2.__version__}")
    #print(f"- python-dotenv: {dotenv.__version__}")
    print(f"- uvicorn: {uvicorn.__version__}")

print_versions()

#Borrar Todo
#Base.metadata.drop_all(bind=engine)

#Creamos en base a metadata
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(upload.router)
app.include_router(batch.router)
app.include_router(queries.router)
