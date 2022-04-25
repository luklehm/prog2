from flask import Flask
from flask import render_template
from flask import request
import daten


from rechnen.steuern import berechnen
from rechnen.steuern import abgaben

from datetime import datetime

app = Flask("Notenrechner")


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        return render_template("input.html")
    return render_template("index.html")


@app.route("/input", methods=["GET", "POST"])
def input():
    if request.method == 'POST':
        name = request.form['name']
        ects = request.form['ects']
        dozent = request.form['dozent']
        semester = request.form['semester']
        note = request.form['note']
        vertiefungsrichtung = request.form['vertiefungsrichtung']
        bewertung = request.form['bewertung']
        daten.speichern(name, ects, dozent, semester, note, vertiefungsrichtung, bewertung)

        eintrag_gespeichert = "Deine Note wurde erfasst. Bei Bedarf kann eine weitere Note hinzugefügt werden."

        return render_template('input.html', eintrag=eintrag_gespeichert)

    return render_template('input.html')


@app.route("/meine_noten", methods=["GET", "POST"])

def meine_noten():
    eingabe = daten.noten_laden()
    filter_liste = []
    filter_value = ""
    filter_key = ""
    gefiltert = False

    if request.method == 'POST':
        gefiltert = True
        vertiefung = request.form['vertiefungsrichtung']

        if vertiefung != "":
            filter_value = vertiefung
            filter_key = "Vertiefungsrichtung"

        for key, eintrag in eingabe.items():
            if eintrag[filter_key] == filter_value:
                filter_liste.append(eintrag)

    return render_template("Meine_Noten.html", neuedaten=eingabe, user=filter_liste, ver=gefiltert)


@app.route("/demo_chf", methods=["get", "post"])
def anderes():
    if request.method.lower() == "get":
        return render_template("preis.html")
    if request.method.lower() == "post":
        preis = request.form["Preis"]
        preis = float(preis)
        abgaben_betrag = abgaben(preis)

        now = datetime.now()
        with open("jail_free_card.txt", "a", encoding="utf8") as offene_datei:
            offene_datei.write(f"{now},{preis},{abgaben_betrag}\n")
        return render_template("preis.html", abgabe=abgaben_betrag)

@app.route("/demo_euro")
def egal_was_2():
    abgaben_betrag = abgaben(400)
    return f"{abgaben_betrag} €"

@app.route("/datum")
def datum_anzeige():
    with open("jail_free_card.txt", encoding="utf8") as open_file:
        inhalt = open_file.read()
    return inhalt.replace("\n", "<br>")



@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
