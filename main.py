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


@app.route("/meine_noten", methods=['GET', 'POST'])
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

    total_ects = {}
    for key, values in eingabe.items():
        ects = values['ECTS']

        if not total_ects.get(ects):
            total_ects[ects] = float(values['ECTS'])
        else:
            total_ects[ects] = float(total_ects[ects]) + float(values['ECTS'])

    for key, value in total_ects.items():
        total = value

    durchschnitt_noten = {}
    for key, values in eingabe.items():
        note = str(values['ECTS'])

        if not durchschnitt_noten.get(note):
            durchschnitt_noten[note] = float(values['Note'])
        else:
            durchschnitt_noten[note] = float(durchschnitt_noten[note]) + float(values['Note'])

    for key, value in durchschnitt_noten.items():
        durchschnitt = float(value) / float(total) #Das funktioniert so noch nicht, ich rechne hier die Noten gesamt durch die ECTS gesamt
        #Man muss aber die Noten gesammt durch die Anzahl Einträge rechnen.


    return render_template("Meine_Noten.html", neuedaten=eingabe, user=filter_liste, ver=gefiltert, total_ects=total_ects, durchschnitt=durchschnitt)


# Da habe ich keine Ahnung was schreiben und muss ich morgen selbst nochmal anschauen
# Sollte jetzt soweit gehen aber idk

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


@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
