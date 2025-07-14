from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/inregistrare", methods=["GET", "POST"])
def inregistrare():
    if request.method == "POST":
        email = request.form.get("email")
        parola = request.form.get("parola")
        print("User registered:", email)
        return redirect("/")  

    return render_template("inregistrare.html")

@app.route("/meniu", methods=["GET", "POST"])
def meniu():
    formulare = [f.split(".")[0] for f in os.listdir("formulare") if f.endswith(".json")]
    return render_template("meniu.html", formulare=formulare)

@app.route("/formular/<nume>", methods=["GET", "POST"])
def formular(nume):
    try:
        with open(f"formulare/{nume}.json", "r", encoding="utf-8") as f:
            template = json.load(f)
    except FileNotFoundError:
        return "Formularul nu exista!", 404

    if request.method == "POST":
        date_primite = request.form.to_dict()
        print("Date primite:", date_primite) 
        return "Formular trimis cu succes!"

    return render_template("formular.html", formular=template)

if __name__ == '__main__':
    app.run(debug=True)
