import sqlite3

conn = sqlite3.connect("inventario.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    categoria TEXT NOT NULL,
    precio_unitario REAL NOT NULL,
    cantidad INTEGER NOT NULL,
    stock_minimo INTEGER NOT NULL
)
""")

conn.commit()
conn.close()

print("Base de datos creada correctamente")