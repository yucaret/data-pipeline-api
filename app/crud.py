import pandas as pd
from app.database import SessionLocal
from app.models import dynamic_models, tables_metadata
from typing import List

def validate_and_convert_dataframe(df: pd.DataFrame, type_: str, has_header: bool = True) -> List[object]:

    print("crud.py --> validate_and_convert_dataframe --> df: " + str(df) + "; type_: " + str(type_) + "; has_header: " + str(has_header))
    
    if type_ not in list(tables_metadata.keys()):
        raise ValueError(f"Tabla no reconocida: {type_}")
    
    # Obtener metadata de la tabla
    table_meta = []
    for sublist in tables_metadata.values():
        for row in sublist:
            if row['table'] == type_:
                table_meta.append(row) # Si coincide a table_meta
    
    if not table_meta:
        raise ValueError(f"No se encontro metadata para la tabla: {type_}")

    expected_columns = [col['columns'] for col in table_meta]

    # Validación de columnas
    if has_header:
        if list(df.columns) != expected_columns:
            raise ValueError(f"Se esperaban columnas en orden: {expected_columns}, se recibio: {list(df.columns)}")
    else:
        df.columns = expected_columns  # Asignar columnas desde metadata

    # Validación de tipos
    for col_meta in table_meta:
        col_name = col_meta['columns']
        dtype = col_meta['datatype'].lower()
        allow_null = col_meta['allownull'].lower() == "yes"
        
        if col_name not in df.columns:
            raise ValueError(f"La columna '{col_name}' no esta en el archivo cargado.")

        if not allow_null and df[col_name].isnull().any():
            raise ValueError(f"La columna '{col_name}' no permite valores nulos.")

        if dtype == "integer":
            try:
                df[col_name] = pd.to_numeric(df[col_name], errors="coerce").astype("Int64")
            except Exception:
                raise ValueError(f"La columna '{col_name}' es de enteros.")
                
        elif dtype == "string":
            max_len = col_meta.get("large")
            df[col_name] = df[col_name].astype(str)
            # Convertir los valores nulos a None
            df[col_name] = df[col_name].replace({"nan": None})
            #df[col_name] = df[col_name].fillna("").astype(str)
            
            if max_len and max_len.isdigit():
                if df[col_name].map(len).max() > int(max_len):
                    raise ValueError(f"Valores en columna '{col_name}' superan longitud maxima de {max_len}.")
        
        elif dtype == "datetime":
            try:
                df[col_name] = pd.to_datetime(df[col_name], errors='coerce')
                df[col_name] = df[col_name].where(~df[col_name].isna(), None)
                #df[col_name] = df[col_name].where(df[col_name].notna(), None)
                
            except Exception:
                raise ValueError(f"No se pudo convertir '{col_name}' a datetime.")

    # Validación de claves primarias duplicadas
    pk_cols = [c["columns"] for c in table_meta if c["keytype"].upper() == "PK"]
    
    if pk_cols and df.duplicated(subset=pk_cols).any():
        raise ValueError(f"Valores duplicados en clave primaria: {pk_cols}")
    
    # Forzamos a sacar NAN NAT
    df = df.replace({pd.NA: None})
    df = df.where(pd.notnull(df), None)
    df = df.astype(object)

    # Crear objetos de la clase dinámica
    ModelClass = dynamic_models[type_]
    objects = [ModelClass(**dict(zip(df.columns, row))) for row in df.itertuples(index=False, name=None)]

    return objects

def insert_objects_in_db(objects: List[object]):
    db = SessionLocal()
    
    try:
        db.bulk_save_objects(objects)
        db.commit()
    finally:
        db.close()