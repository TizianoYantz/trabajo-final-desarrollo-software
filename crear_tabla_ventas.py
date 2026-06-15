import sqlite3

conn = sqlite3.connect("inventario.db")
cursor = conn.cursor()

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
