import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect("inventario.db")
cursor = conn.cursor()

usuario = "admin"
password = generate_password_hash("admin123")

cursor.execute("""
INSERT OR IGNORE INTO usuarios (usuario, password)
VALUES (?, ?)
""", (usuario, password))

conn.commit()
conn.close()

print("Administrador creado correctamente")
print("Usuario: admin")
print("Contraseña: admin123")