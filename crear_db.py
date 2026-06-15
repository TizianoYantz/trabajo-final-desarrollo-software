import sqlite3

conn = sqlite3.connect("inventario.db")
cursor = conn.cursor()

# =========================
# PRODUCTOS
# =========================
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

# =========================
# MOVIMIENTOS
# =========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS movimientos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    descripcion TEXT NOT NULL,
    fecha TEXT DEFAULT CURRENT_TIMESTAMP
)
""")

# =========================
# VENTAS
# =========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS ventas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    producto_id INTEGER NOT NULL,
    cantidad INTEGER NOT NULL,
    fecha TEXT DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()

print("Base de datos creada correctamente")