from flask import Flask
from flask import render_template
from flask import url_for
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
    if request.method == "POST":
        name = request.form["name"]
        ECTS = request.form["ECTS"]
        dozent = request.form["dozent"]
        leistungsnachweis = request.form["leistungsnachweis"]
        semester = request.form["semester"]
        note = request.form["note"]
        gewichtung = request.form["gewichtung"]
        vertiefungsrichtung = request.form["vertiefungsrichtung"]
        bewertung = request.form["bewertung"]
        daten.speichern(name, ECTS, dozent, leistungsnachweis, semester, note, gewichtung, vertiefungsrichtung, bewertung)

        eintrag_gespeichert = "Dein Eintrag wurde erfasst. Bei Bedarf kann nun ein weiterer Eintrag erfolgen."

        return render_template('input.html', eintrag=eintrag_gespeichert)

    return render_template('input.html')

@app.route("/form", methods=["get", "post"])
def form():
    if request.method.lower() == "get":
        return render_template("formular.html")
    if request.method.lower() == "post":
        name = request.form["vorname"]
        return name

@app.route("/list")
def auflistung():
    elemente = ["bla", "blubber", "döner"]
    return render_template("list.html", html_elemente=elemente)

@app.route("/table")
def tabelle():
    biere = [
        {
            "name": "Glatsch",
            "herkunft": "Chur",
            "vol": "4.8",
            "brauerei": "Calanda",
            "preis": 0.90
        },
        {
            "name": "Retro",
            "herkunft": "Luzern",
            "vol": "4.8",
            "brauerei": "Eichhof",
            "preis": 2.00
        },
        {
            "name": "Quöllfrisch",
            "herkunft": "Appenzell",
            "vol": "4.8",
            "brauerei": "Locher",
            "preis": 1.80
        }
    ]
    for bier in biere:
        preis = bier["preis"]
        tax = berechnen(preis)
        bier["steuern"] = tax
    table_header = ["name", "herkunft", "vol", "brauberei", "preis", "steuern"]
    return render_template("beer.html", beers=biere, header=table_header)

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

@app.route("/meine_noten")
def meine_noten():
    return render_template("Meine_Noten.html")

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
