import json
from datetime import datetime


def speichern(name, ects, dozent, semester, note, vertiefungsrichtung, bewertung):
    datei = "eintrage.json"
    try:
        with open(datei) as open_file:
            datei_inhalt = json.load(open_file)
    except FileNotFoundError:
        datei_inhalt = {}

    datei_inhalt[str(datetime.now())] = {'Name': name,
                                         'ECTS': ects,
                                         'Dozent': dozent,
                                         'Semester': semester,
                                         'Note': note,
                                         'Vertiefungsrichtung': vertiefungsrichtung,
                                         'Bewertung': bewertung}

    with open(datei, "w") as open_file:
        json.dump(datei_inhalt, open_file, indent=4)


def noten_laden():
    datei_name = "eintrage.json"

    try:
        with open(datei_name) as open_file:
            datei_inhalt = json.load(open_file)
    except FileNotFoundError:
        datei_inhalt = {}

    return datei_inhalt
