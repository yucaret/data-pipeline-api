import csv
import os
#from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy import Column, ForeignKey
from app.database import Base
from app.metadata.types_config import TYPES_BY_DB

# Motor de Base de datos, en rail esta como una variable, en local jala de .env
CURRENT_DB = os.getenv("DATABASE_ENGINE", "postgresql")

# Ruta del CSV
METADATA_CSV_PATH = os.path.join(os.path.dirname(__file__), "metadata", "metadatatables.csv")

# Tipos de dato validos
#SQLALCHEMY_TYPES = {
#    "Integer": Integer,
#    "String": String,
#    "DateTime": DateTime
#}
SQLALCHEMY_TYPES = TYPES_BY_DB[CURRENT_DB]

# Agrupar columnas por tabla
tables_metadata = {}

with open(METADATA_CSV_PATH, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        table_name = row["table"]
        
        if table_name not in tables_metadata:
            tables_metadata[table_name] = []
        
        tables_metadata[table_name].append(row)
        
dynamic_models = {}

# Creamos clases
for table_name, columns in tables_metadata.items():
    # Nombre de columna
    attrs = {"__tablename__": table_name}

    for col in columns:
        col_name = col["columns"]
        col_type_str = col["datatype"]
        col_kwargs = {}

        # Validamos tipo de dato
        if col_type_str not in SQLALCHEMY_TYPES:
            raise ValueError(f"Tipo de dato no reconocido: '{col_type_str}' en la columna '{col_name}' de la tabla '{table_name}'")

        base_type = SQLALCHEMY_TYPES[col_type_str]

        # Si es String, considerar tamanho
        if col_type_str == "String" and col["large"]:
            col_type = base_type(int(col["large"]))
        else:
            col_type = base_type

        # Es Nulo
        col_kwargs["nullable"] = (col["allownull"].lower() == "yes")

        # Es Primary key
        if col["keytype"].upper() == "PK":
            col_kwargs["primary_key"] = True

        # Es foreign Key
        if col["keytype"].upper() == "FK":
            ref_table = col["foreingtable"]
            if not ref_table:
                raise ValueError(f"La columna '{col_name}' de la tabla '{table_name}' es FK pero no tiene 'foreingtable' definido")
            col_type = ForeignKey(f"{ref_table}.id")

        # Definir la columna SQLAlchemy
        attrs[col_name] = Column(col_type, **col_kwargs)

    # Creamos clase
    cls = type(table_name.capitalize(), (Base,), attrs)

    # Registramos la clase en el modulo, para que cuando al import se lean
    globals()[cls.__name__] = cls
    
    # Agregar al diccionario dinámico, para usarlo en upload
    dynamic_models[table_name] = cls