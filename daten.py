import json
from datetime import datetime

def speichern(name, ECTS, dozent, leistungsnachweis, semester, note, gewichtung, vertiefungsrichtung, bewertung):
    datei = "einträge.json"
    try:
        with open(datei) as open_file:
            datei_inhalt = json.load(open_file)
    except FileNotFoundError:
        datei_inhalt = {}

    datei_inhalt[str(datetime.now())] = {"Name": name,
                                         "ECTS": ECTS,
                                         "Dozent": dozent,
                                         "Leistungsnachweis": leistungsnachweis,
                                         "Semester": semester,
                                         "Note": note,
                                         "Gewichtung": gewichtung,
                                         "Vertiefungsrichtung": vertiefungsrichtung,
                                         "Bewertung": bewertung
                                         }
    with open(datei, "w") as open_file:
        json.dump(datei_inhalt, open_file, indent="4")


def noten_laden():
    datei_name = "einträge.json"

    try:
        with open(datei_name) as open_file:
            datei_inhalt = json.load(open_file)
    except FileNotFoundError:
        datei_inhalt = {}

    return datei_inhalt
