from flask import Flask
from flask import render_template
from flask import request
import daten
import plotly.express as px
from plotly.offline import plot

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

    lenght = str(len(eingabe))

    # Zum Berechnen der Anzahl absolvierten ECTS
    total_ects = {}
    for EE, FF in eingabe.items():
        ects = FF['ECTS']

        if not total_ects.get(ects):
            total_ects[ects] = float(FF['ECTS'])
        else:
            total_ects[ects] = float(total_ects[ects]) + float(FF['ECTS'])

    # Zum Berechnen des Durchschnitts der Noten
    durchschnitt_noten = {}
    for XX, YY in eingabe.items():
        note = str(YY['ECTS'])

        if not durchschnitt_noten.get(note):
            durchschnitt_noten[note] = float(YY['Note'])
        else:
            durchschnitt_noten[note] = float(durchschnitt_noten[note]) + float(YY['Note'])

    for TT, xy in durchschnitt_noten.items():
        durchschnitt = float(xy) / float(lenght)

    # Zum Berechnen des Durchschnitts der Bewertungen
    durchschnitt_bewertung = {}
    for OO, PP in eingabe.items():
        bewertung = str(PP['ECTS'])

        if not durchschnitt_bewertung.get(bewertung):
            durchschnitt_bewertung[bewertung] = float(PP['Bewertung'])
        else:
            durchschnitt_bewertung[bewertung] = float(durchschnitt_bewertung[bewertung]) + float(PP['Bewertung'])

        for QQ, bew, in durchschnitt_bewertung.items():
            dur_bew = float(bew) / float(lenght)

    return render_template("Meine_Noten.html", neuedaten=eingabe, user=filter_liste, ver=gefiltert, total_ects=total_ects, durchschnitt=durchschnitt, bewertung=dur_bew)


# Da habe ich keine Ahnung was schreiben und muss ich morgen selbst nochmal anschauen
# Sollte jetzt soweit gehen aber idk

@app.route("/analyse", methods=['GET', 'POST'])
def analyse():
    analyse = daten.noten_laden()
    #Diagramm für die Summe ECTS pro Modulgruppe
    ects = {"Digital Innovation": 0.0,
            "Information Technology": 0.0,
            "Sozial- und Methodenkompetenz": 0.0,
            "User Experience": 0.0}

    for key, values in analyse.items():
        vertiefung_ = values['Vertiefungsrichtung']

        if not ects.get(vertiefung_):
            ects[vertiefung_] = float(values['ECTS'])
        else:
            ects[vertiefung_] = float(ects[vertiefung_]) + float(values['ECTS'])

    x = list(ects.keys())
    y = list(ects.values())

    fig = px.line(x=x, y=[8, 8, 8, 8], color=px.Constant("Ziel ECTS"),
                  labels=dict(x="Vertiefungsrichtung", y="ECTS", color="Legende"))
    fig.add_bar(x=x, y=y, name="Ist ECTS")

    div = plot(fig, output_type="div")

    #Diagramm für die Bewertungen pro Modulgruppe
    bewertung = {"Digital Innovation": 0.0,
                "Information Technology": 0.0,
                "Sozial- und Methodenkompetenz": 0.0,
                "User Experience": 0.0}

    for key, values in analyse.items():
        bewer = values['Vertiefungsrichtung']

        if not ects.get(bewer):
            bewertung[bewer] = float(values['Bewertung'])
        else:
            bewertung[bewer] = float(ects[bewer]) + float(values['Bewertung'])

    x = list(bewertung.keys())
    y = list(bewertung.values())

    fig = px.bar(x=x, y=y, labels=dict(x="Vertiefungsrichtung", y="Bewertungen"))

    div2 = plot(fig, output_type="div")

    return render_template("analyse.html", div=div, div2=div2)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
