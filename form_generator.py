from flask import Flask, render_template, request, redirect
import json
import os
import pyodbc

app = Flask(__name__)

def get_db_connection():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=LAPTOP-STEFAN20;'
        'DATABASE=NUME_BAZA_DATE;'
        # 'UID=utilizator;'
        # 'PWD=parola'
    )
    return conn

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
        return raspuns()

    return render_template("formular.html", formular=template)

@app.route("/formular_trimis", methods=["GET", "POST"])
def raspuns():
    return render_template("formular_trimis.html")

if __name__ == '__main__':
    app.run(debug=True)
