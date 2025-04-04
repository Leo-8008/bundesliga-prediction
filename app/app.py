from flask import Flask, render_template, request
import pandas as pd
import pickle
import numpy as np
import os
from azure.storage.blob import BlobServiceClient

app = Flask(__name__)


AZURE_STORAGE_KEY = os.getenv("AZURE_STORAGE_KEY")
STORAGE_ACCOUNT_NAME = "bundesligaml4305190470"
CONTAINER_NAME = "models"

def get_latest_version():
    try:
        blob_service = BlobServiceClient(
            f"https://{STORAGE_ACCOUNT_NAME}.blob.core.windows.net",
            credential=AZURE_STORAGE_KEY
        )
        container_client = blob_service.get_container_client(CONTAINER_NAME)
        versions = set(blob.name.split("/")[0] for blob in container_client.list_blobs())
        return sorted(versions)[-1] if versions else "Unbekannt"
    except Exception as e:
        print("Fehler beim Ermitteln der Modellversion:", e)
        return "Unbekannt"

model_version = get_latest_version()

base_path = os.path.dirname(os.path.dirname(__file__))
model_path = os.path.join(base_path, "models", model_version)

with open(os.path.join(model_path, "model_home.pkl"), "rb") as f:
    model_home = pickle.load(f)
with open(os.path.join(model_path, "model_away.pkl"), "rb") as f:
    model_away = pickle.load(f)
feature_names = pd.read_csv(os.path.join(model_path, "feature_names.csv"))["feature"].tolist()

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
                           selected_home=home_team, selected_away=away_team,
                           model_version=model_version)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
