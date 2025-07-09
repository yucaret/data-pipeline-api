# data-pipeline-api

**Descripción general**  
Este proyecto implementa una solución de procesamiento y análisis de datos a través de una API construida con FastAPI y PostgreSQL. Permite la carga, validación, almacenamiento y consulta analítica de datos de empleados, departamentos y puestos de trabajo. Forma parte de mi portafolio profesional como proyecto de ingeniería de datos.

---

## Objetivo del Proyecto

- Automatizar la ingesta de archivos CSV mediante una API REST.
- Validar los datos recibidos según una metadata dinámica definida en un archivo CSV.
- Insertar los datos limpios en una base de datos PostgreSQL.
- Exponer endpoints analíticos que permitan responder preguntas de negocio relevantes, como contrataciones por trimestre o departamentos con contrataciones por encima del promedio.

---

## Arquitectura del Sistema

```
Client (CSV Upload via /upload)

FastAPI Backend
 ├── Validación de datos (con pandas)
 ├── Conversión dinámica según metadata
 ├── Inserción en PostgreSQL (SQLAlchemy)
 └── Endpoints de análisis (/analytics/...)

 PostgreSQL (3 tablas: employees, departments, jobs)
```

---

## Componentes Principales

| Componente     | Descripción                                          |
|----------------|------------------------------------------------------|
| FastAPI        | Framework para construir APIs rápidas y eficientes. |
| SQLAlchemy     | ORM para interactuar con PostgreSQL.                |
| pandas         | Validación y procesamiento de archivos CSV.         |
| PostgreSQL     | Base de datos relacional.                           |
| Uvicorn        | Servidor ASGI para correr FastAPI.                  |

---

## Funcionalidades

### 1. Carga de archivos
**Endpoint:** `POST /upload`  
- Acepta archivos CSV (empleados, departamentos o puestos).
- Determina la estructura según el parámetro `type_` (valores posibles a usar employees, jobs o departments).
- Permite el ingreso de archivos con o sin cabecera con el parámetro `has_header` (True o False).
- Valida los datos contra el archivo `metadata/metadatatables.csv`.
- Convierte dinámicamente los tipos de datos.
- Inserta los datos válidos en la base de datos.

![image](https://github.com/user-attachments/assets/2e603493-4cd6-410f-91c8-ef9bc17edf00)

### 2. Consultas Analíticas
**Endpoint:** `GET /analytics/hires_by_quarter`  
- Devuelve contrataciones por trimestre agrupadas por departamento y puesto.

![image](https://github.com/user-attachments/assets/4f54fbc5-b781-47fe-b08a-ff5356721073)

**Endpoint:** `GET /analytics/departments_above_mean`  
- Devuelve los departamentos con contrataciones por encima del promedio en 2021.

![image](https://github.com/user-attachments/assets/2469d9f1-526d-4660-869d-b2bf7e01c33f)

---

## Estructura del Repositorio

```
.
├── app/
│   ├── crud.py              # Validación y conversión de datos
│   ├── database.py          # Configuración de la conexión con PostgreSQL
│   ├── models.py            # Definición de tablas ORM
│   ├── routers/
│   │   ├── upload.py        # Endpoint de carga
│   │   └── queries.py       # Endpoints analíticos
├── metadata/
│   ├── types_config.py      # Tipo de dato según motor de base de datos
│   └── metadatatables.csv   # Estructura de las tablas
├── main.py                  # Punto de entrada de la aplicación
└── requirements.txt         # Dependencias
```
---

## Diseño

```
![image](https://github.com/user-attachments/assets/5dc3f355-fd22-4fa9-b82a-288dffbbf147)
```
---

## Cómo ejecutar localmente

```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # o venv\Scripts\activate en Windows

# Instalar dependencias
pip install -r requirements.txt

# Iniciar servidor
uvicorn main:app --reload
```

---

## Despliegue

La aplicación puede desplegarse en plataformas como Railway o Render. Asegúrate de configurar las variables de entorno para conectar a la base de datos.

Esta solución fue desplegada en railway, una plataforma comoda e intuitiva para configurar, conecta a github y se añade comoponentes como es el caso de posgresql, redis, etc.
![image](https://github.com/user-attachments/assets/46976786-14e2-48a0-8b8b-62af63f1bf2e)

Para probar el api ingresas la link: https://data-pipeline-api-production.up.railway.app/docs#/

![image](https://github.com/user-attachments/assets/96b9f4d2-6aee-4559-9e30-b1d90d40b2a9)

---

## Consideraciones Técnicas

- Se maneja correctamente la carga de valores nulos (NaN, NaT) transformándolos a `None` para la compatibilidad con PostgreSQL.
- El sistema soporta definición dinámica de modelos desde el archivo metadata, lo que permite una extensión futura sin modificar código.

---

## Autor

Jorge Eduardo Vicente Hernández
