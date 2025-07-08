from sqlalchemy import Integer, String, DateTime, Float, Boolean, Text, Date, Time, Numeric, JSON

TYPES_BY_DB = {
    "postgresql": {
        "Integer": Integer,
        "String": String,
        "DateTime": DateTime,
        "Float": Float,
        "Boolean": Boolean,
        "Text": Text,
        "Date": Date,
        "Time": Time,
        "Numeric": Numeric,
        "JSON": JSON,
    },
    "mysql": {
        "Integer": Integer,
        "String": String,
        "DateTime": DateTime,
        "Float": Float,
        "Boolean": Boolean,
        "Text": Text,
        "Date": Date,
        "Time": Time,
        "Numeric": Numeric,
        # JSON y ARRAY no son soportados igual en MySQL
    },
    # Puedes agregar SQLite, Oracle, etc.
}
