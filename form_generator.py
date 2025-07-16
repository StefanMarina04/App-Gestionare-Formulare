from flask import Flask, render_template, request, redirect, session
import json
import os
import pyodbc

app = Flask(__name__)
app.secret_key = "cheie_secreta"  # cheia pentru sesiuni
import uuid
id_completare = str(uuid.uuid4())

# === Conexiune DB ===
def get_db_connection():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=LAPTOP-STEFAN20;'
        'DATABASE=App-Gestionare-Formulare;'
        'Trusted_Connection=yes;'
    )
    return conn

# === LOGIN ===
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

# === INREGISTRARE ===
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

            # Verificăm dacă utilizatorul există deja
            cursor.execute("SELECT * FROM Utilizatori WHERE Email = ?", email)
            if cursor.fetchone():
                return "Emailul există deja!", 400

            # Inserăm utilizatorul nou
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

# === DECONETARE ===
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# === MENIU ===
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

# === FORMULAR ===
@app.route("/formular/<nume>", methods=["GET", "POST"])
def formular(nume):
    try:
        with open(f"formulare/{nume}.json", "r", encoding="utf-8") as f:
            template = json.load(f)
    except FileNotFoundError:
        return "Formularul nu există!", 404

    if request.method == "POST":
        date_primite = request.form.to_dict(flat=False)
        print("Date primite:", date_primite)

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            id_utilizator = session.get("id_utilizator", 1)

            # 🔒 dacă există deja ID_Completare pt formularul acesta, nu-l înlocuim
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
            print("Eroare la salvare în baza de date:", e)
            return "A apărut o eroare la salvarea datelor.", 500

        return redirect("/formular_trimis")

    return render_template("formular.html", formular=template)

# === CONFIRMARE ===
@app.route("/formular_trimis")
def raspuns():
    return render_template("formular_trimis.html")

# === RUN APP ===
if __name__ == '__main__':
    app.run(debug=True)
