from flask import Flask, render_template, request, redirect, session, send_file
import json
import os
import pyodbc

from reportlab.pdfgen import canvas
import io
from datetime import datetime

from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

pdfmetrics.registerFont(TTFont("Arial", "static/fonts/ARIAL.TTF"))
pdfmetrics.registerFont(TTFont("ArialBD", "static/fonts/ARIALBD.TTF"))

app = Flask(__name__)
app.secret_key = "cheie_secreta"
import uuid
id_completare = str(uuid.uuid4())

def get_db_connection():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=LAPTOP-STEFAN20;'
        #'SERVER=STEFAN2023\SQLEXPRESS;'
        'DATABASE=App-Gestionare-Formulare;'
        'Trusted_Connection=yes;'
    )
    return conn

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("EmailInput")
        parola = request.form.get("ParolaInput")

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT ID_Utilizator FROM Utilizatori WHERE Email = ? AND Parola = ?
            """, email, parola)

            row = cursor.fetchone()
            if row:
                session["id_utilizator"] = row[0]
                return redirect("/meniu")
            else:
                 return render_template("login.html", eroare="Email sau parolă greșită!")

        except Exception as e:
                return render_template("login.html", eroare="Eroare la autentificare! (Posibilă problemă la server)")
        
    return render_template("login.html")

@app.route("/inregistrare", methods=["GET", "POST"])
def inregistrare():
    if request.method == "POST":
        email = request.form.get("EmailInput")
        parola = request.form.get("ParolaInput")
        nume_complet = request.form.get("NumeInput")
        confirmare = request.form.get("ConfirmareParola")
        if parola != confirmare:
            return render_template("inregistrare.html", eroare="Parolele nu coincid")
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM Utilizatori WHERE Email = ?", email)
            if cursor.fetchone():
                return "Emailul există deja!", 400

            cursor.execute("""
                INSERT INTO Utilizatori (Email, Parola, Nume_Complet) VALUES (?, ?, ?)
            """, email, parola, nume_complet)
            conn.commit()
            cursor.close()
            conn.close()

            print("User registered:", email)
            return redirect("/")
        except Exception as e:
            print("Eroare înregistrare:", e)
            return "Eroare la înregistrare", 500

    return render_template("inregistrare.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/meniu")
def meniu():
    id_completare = str(uuid.uuid4())  
    formulare = []
    for f in os.listdir("formulare"):
        if f.endswith(".json"):
            with open(os.path.join("formulare", f), encoding="utf-8") as file:
                continut = json.load(file)
                formulare.append({
                    "nume": continut.get("titlu", f.split(".")[0]),
                    "id": f.split(".")[0],
                    "anonim": continut.get("anonim", False)
                })
    return render_template("meniu.html", formulare=formulare)

@app.route("/formular/<nume>", methods=["GET", "POST"])
def formular(nume):
    try:
        with open(f"formulare/{nume}.json", "r", encoding="utf-8") as f:
            template = json.load(f)
    except FileNotFoundError:
        return "Formularul nu există!", 404
    user_data = {}
    id_utilizator = session.get("id_utilizator", 1)

    if id_utilizator != 1:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT Email, Nume_Complet FROM Utilizatori WHERE ID_Utilizator = ?", id_utilizator)
        row = cursor.fetchone()
        if row:
            user_data["email"] = row.Email
            user_data["nume complet"] = row.Nume_Complet
            user_data["nume"] = row.Nume_Complet
            user_data["nume_complet"] = row.Nume_Complet
            user_data["numeinput"] = row.Nume_Complet
        cursor.close()
        conn.close()


    if request.method == "POST":
        date_primite = request.form.to_dict(flat=False)
        print("Date primite:", date_primite)

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            id_utilizator = session.get("id_utilizator", 1)

            if f"id_completare_{nume}" not in session:
                session[f"id_completare_{nume}"] = str(uuid.uuid4())

            id_completare = session[f"id_completare_{nume}"]

            for camp, valoare in date_primite.items():
                if isinstance(valoare, list):
                    for val in valoare:
                        cursor.execute("""
                            INSERT INTO Raspunsuri (ID_Utilizator, Formular, Camp, Valoare, ID_Completare)
                            VALUES (?, ?, ?, ?, ?)
                        """, id_utilizator, nume, camp, val, id_completare)
                else:
                    cursor.execute("""
                        INSERT INTO Raspunsuri (ID_Utilizator, Formular, Camp, Valoare, ID_Completare)
                        VALUES (?, ?, ?, ?, ?)
                    """, id_utilizator, nume, camp, valoare, id_completare)

            conn.commit()
            cursor.close()
            conn.close()

        except Exception as e:
            print("Eroare la salvarea în baza de date:", e)
            return "A apărut o eroare în timpul salvării datelor.", 500

        return redirect("/formular_trimis")

    return render_template("formular.html", formular=template, user_data=user_data)

@app.route("/formular_trimis")
def raspuns():
    return render_template("formular_trimis.html")

@app.route("/export_pdf")
def export_pdf():
    id_utilizator = session.get("id_utilizator", 1)

    id_completare = None
    for key in session:
        if key.startswith("id_completare_"):
            id_completare = session[key]
            break

    if not id_completare:
        return "Nu există un formular completat recent!", 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT Formular, Camp, Valoare FROM Raspunsuri
            WHERE ID_Completare = ?
        """, id_completare)

        raspunsuri = cursor.fetchall()
        cursor.close()
        conn.close()

        if not raspunsuri:
            return "Nu s-au găsit date pentru export.", 404

        buffer = io.BytesIO()
        pdf = canvas.Canvas(buffer)
        pdf.setTitle("Formular completat")

        nume_formular = raspunsuri[0].Formular.replace(" ", "_")  
        data = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{nume_formular}_{data}.pdf"
        
        y = 800
        pdf.setFont("ArialBD", 14)
        pdf.drawString(50, y, f"Formular completat: {raspunsuri[0].Formular}")
        y -= 25
        pdf.setFont("Arial", 11)
        pdf.drawString(50, y, f"Completat la data de: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
        y -= 40
        pdf.setFont("Arial", 11)
        pdf.drawString(50, y, f"Răspunsuri:")
        y -= 20

        for rand in raspunsuri:
            if y < 50:
                pdf.showPage()
                y = 800
            pdf.drawString(50, y, f"{rand.Camp}: {rand.Valoare}")
            y -= 20

        pdf.save()
        buffer.seek(0)

        return send_file(buffer, as_attachment=True, download_name=filename, mimetype='application/pdf')

    except Exception as e:
        print("Eroare PDF:", e)
        return "Eroare la generarea PDF-ului.", 500

if __name__ == '__main__':
    app.run(debug=True)
