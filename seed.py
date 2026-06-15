import sqlite3

conn = sqlite3.connect("inventario.db")
cursor = conn.cursor()

productos = [
    ("Arroz", "Comida", 500, 10, 2),
    ("Fideos", "Comida", 300, 15, 3),
    ("Leche", "Lácteos", 800, 8, 2),
    ("Azúcar", "Comida", 450, 12, 2),
    ("Yerba", "Bebidas", 1200, 5, 1),
    ("Pan", "Comida", 200, 20, 5),
    ("Aceite", "Comida", 1500, 7, 2),
    ("Galletitas", "Snacks", 600, 18, 4),
    ("Jugo", "Bebidas", 700, 10, 3),
    ("Queso", "Lácteos", 2000, 4, 1),
]

cursor.executemany("""
INSERT INTO productos (nombre, categoria, precio_unitario, cantidad, stock_minimo)
VALUES (?, ?, ?, ?, ?)
""", productos)

conn.commit()
conn.close()

print("10 productos insertados correctamente")