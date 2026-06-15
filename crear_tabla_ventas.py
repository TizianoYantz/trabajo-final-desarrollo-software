import sqlite3

conn = sqlite3.connect("inventario.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    categoria TEXT,
    precio_unitario REAL,
    cantidad INTEGER,
    stock_minimo INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS movimientos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    descripcion TEXT,
    fecha TEXT DEFAULT CURRENT_TIMESTAMP
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS ventas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    producto_id INTEGER,
    cantidad INTEGER,
    fecha TEXT DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()