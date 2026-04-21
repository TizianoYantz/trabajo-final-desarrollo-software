from flask import Flask, render_template, request

app = Flask(__name__)

# Usuario de prueba
USUARIO = "admin"
PASSWORD = "1234"

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        password = request.form["password"]

        if usuario == USUARIO and password == PASSWORD:
            return "Login correcto ✅"
        else:
            return "Datos incorrectos ❌"

    return render_template("login.html")

app.run(debug=True)
