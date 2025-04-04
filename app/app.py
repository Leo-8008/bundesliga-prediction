from flask import Flask, render_template, request
import pandas as pd
import pickle
import numpy as np
import os
import re
from azure.storage.blob import BlobServiceClient

app = Flask(__name__)

# Azure Blob Konfiguration
AZURE_STORAGE_KEY = os.getenv("AZURE_STORAGE_KEY")
STORAGE_ACCOUNT_NAME = "bundesligaml4305190470"
CONTAINER_NAME = "models"
DOWNLOAD_DIR = os.path.dirname(os.path.dirname(__file__))

def download_latest_model():
    if not AZURE_STORAGE_KEY:
        print("Azure Storage Key nicht gesetzt!")
        return

    blob_service = BlobServiceClient(
        f"https://{STORAGE_ACCOUNT_NAME}.blob.core.windows.net",
        credential=AZURE_STORAGE_KEY
    )
    container = blob_service.get_container_client(CONTAINER_NAME)

    version_folders = set()
    for blob in container.list_blobs():
        match = re.match(r"(v\d{8}_\d{4})/", blob.name)
        if match:
            version_folders.add(match.group(1))

    if not version_folders:
        print("Keine Modellversionen gefunden.")
        return

    latest_version = sorted(version_folders)[-1]
    print(f"Lade neuestes Modell: {latest_version}")

    for filename in ["model_home.pkl", "model_away.pkl", "feature_names.csv"]:
        blob_path = f"{latest_version}/{filename}"
        blob = container.get_blob_client(blob_path)
        with open(os.path.join(DOWNLOAD_DIR, filename), "wb") as f:
            f.write(blob.download_blob().readall())
            print(f"Heruntergeladen: {filename}")

# ⬇Neueste Modelle laden
download_latest_model()

# Modelle und Features einladen
with open(os.path.join(DOWNLOAD_DIR, "model_home.pkl"), "rb") as f:
    model_home = pickle.load(f)
with open(os.path.join(DOWNLOAD_DIR, "model_away.pkl"), "rb") as f:
    model_away = pickle.load(f)

feature_names = pd.read_csv(os.path.join(DOWNLOAD_DIR, "feature_names.csv"))["feature"].tolist()

# Teamauswahl vorbereiten (nur Teamnamen)
teams = sorted(set(
    name.replace("home_team_", "").replace("away_team_", "")
    for name in feature_names
    if name.startswith("home_team_") or name.startswith("away_team_")
))

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    home_team = None
    away_team = None

    if request.method == "POST":
        home_team = request.form.get("home_team")
        away_team = request.form.get("away_team")

        x = pd.DataFrame([0]*len(feature_names), index=feature_names).T
        if f"home_team_{home_team}" in x.columns:
            x[f"home_team_{home_team}"] = 1
        if f"away_team_{away_team}" in x.columns:
            x[f"away_team_{away_team}"] = 1

        home_goals = model_home.predict(x)[0]
        away_goals = model_away.predict(x)[0]

        prediction = f"{home_team} vs. {away_team} – Tipp: {int(round(home_goals))}:{int(round(away_goals))}"

    return render_template("index.html", teams=teams, prediction=prediction,
                           selected_home=home_team, selected_away=away_team)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
