from flask import Flask
from flask import render_template
from flask import url_for
from flask import request

from rechnen.steuern import berechnen

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("index.html", name="Lukas")

    about_link = url_for("about")
    return render_template("index")


@app.route("/about")
def about():
    return "about"


@app.route("/form" , methods=["get", "post"])
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


if __name__ == "__main__":
    app.run(debug=True, port=5000)
