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
    ("Manteca", "Lácteos", 900, 6, 2),
    ("Café", "Bebidas", 2500, 3, 1),
    ("Té", "Bebidas", 400, 14, 3),
    ("Harina", "Comida", 550, 9, 2),
    ("Sal", "Comida", 150, 25, 5),
    ("Chocolate", "Snacks", 1800, 7, 2),
    ("Cereal", "Snacks", 2200, 5, 1),
    ("Agua", "Bebidas", 250, 30, 10),
    ("Refresco", "Bebidas", 900, 12, 3),
    ("Dulce de leche", "Comida", 1300, 6, 2),
]

for nombre, categoria, precio, cantidad, stock_minimo in productos:

    # 🔍 verificar si ya existe
    cursor.execute("""
        SELECT id FROM productos
        WHERE nombre = ? AND categoria = ? AND precio_unitario = ?
    """, (nombre, categoria, precio))

    existe = cursor.fetchone()

    if not existe:
        cursor.execute("""
            INSERT INTO productos (nombre, categoria, precio_unitario, cantidad, stock_minimo)
            VALUES (?, ?, ?, ?, ?)
        """, (nombre, categoria, precio, cantidad, stock_minimo))

conn.commit()
conn.close()

print("Seed ejecutado sin duplicar productos")