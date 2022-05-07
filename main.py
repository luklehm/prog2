from flask import Flask
from flask import render_template
from flask import request
import daten
import plotly.express as px
from plotly.offline import plot
import pandas as pd




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

# Da habe ich keine Ahnung was schreiben und muss ich morgen selbst nochmal anschauen

@app.route("/analyse", methods=['GET', 'POST'])
def analyse():
    analyse = daten.noten_laden()
    ects = {}

    for key, values in analyse.items():
        vertiefung_ = values['Vertiefungsrichtung']

        if not ects.get(vertiefung_):
            ects[vertiefung_] = float(values['ECTS'])
        else:
            ects[vertiefung_] = float(ects[vertiefung_]) + float(values['ECTS'])


    x = list(ects.keys())
    y = list(ects.values())

    fig = px.bar(x=x, y=y, labels={"x": "Vertiefungsrichtung",
                                   "y": "ECTS"},
                 title="Anzahl ECTS pro Vertiefungsrichtung")

    div = plot(fig, output_type="div")
    return render_template("analyse.html", div=div)


"""
    return x


    fig = px.bar(x=x, y=y, labels={"x": "Monate",
                                   "y": "Betrag in CHF"},
                 title="Ausgaben über die Monate hinweg")



    fig = px.bar(x=x, y=y, )
    div = plot()

    
    analyse = daten.noten_laden()
    vertiefung = {}

    for key, value in analyse.items():
        if not vertiefung.get():
            vertiefung = float("Vertiefungsrichtung")
        else:
            vertiefung = vertiefung + float("Vertiefungsrichtung")

    fig = px.bar(x=x, y=y, labels={"x": "Vertiefungsrichtung",
                                   "y": "ECTS"},
                 title="Anzahl ECTS pro Vertiefungsrichtung")

    div = plot(fig, output_type="div")

    summe_ects = list(vertiefung.values())
    summe = 0
    for einzel in summe_ects:
        summe += float(einzel)

    ECTS = 0
    if request.method == 'POST':

    # gehört ins rendertemplate für die attribute, viz_div=div, vertiefung=vertiefung, total=summe

    return render_template("analyse.html")
    """

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
