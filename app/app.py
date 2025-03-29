from flask import Flask, render_template, request
import pandas as pd
import pickle
import numpy as np
import os

app = Flask(__name__)

# Basisverzeichnis definieren (eine Ebene über dem app-Verzeichnis)
base_path = os.path.dirname(os.path.dirname(__file__))

# Modelle und Feature-Namen laden
with open(os.path.join(base_path, "model_home.pkl"), "rb") as f:
    model_home = pickle.load(f)

with open(os.path.join(base_path, "model_away.pkl"), "rb") as f:
    model_away = pickle.load(f)

feature_names = pd.read_csv(os.path.join(base_path, "feature_names.csv"))["feature"].tolist()

# Alle Teams aus den Feature-Namen extrahieren
teams = sorted(set(name.replace("home_team_", "").replace("away_team_", "")
                   for name in feature_names))

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    if request.method == "POST":
        home_team = request.form.get("home_team")
        away_team = request.form.get("away_team")

        # Feature-Vektor vorbereiten
        x = pd.DataFrame([0]*len(feature_names), index=feature_names).T
        if f"home_team_{home_team}" in x.columns:
            x[f"home_team_{home_team}"] = 1
        if f"away_team_{away_team}" in x.columns:
            x[f"away_team_{away_team}"] = 1

        # Vorhersage
        home_goals = model_home.predict(x)[0]
        away_goals = model_away.predict(x)[0]

        # Runden auf ganze Tore
        prediction = f"Tipp: {int(round(home_goals))}:{int(round(away_goals))}"

    return render_template("index.html", teams=teams, prediction=prediction)

if __name__ == "__main__":
    app.run(debug=True)
