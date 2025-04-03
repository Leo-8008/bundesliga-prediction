import json
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pickle

# JSON laden
with open("bundesliga_results.json", "r", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(data)

# Tore extrahieren
df[["home_goals", "away_goals"]] = df["score"].str.extract(r'(\d+):(\d+)').astype(int)

# Fehlende Werte auffüllen (z. B. falls Form oder Rank noch fehlt)
df["home_team_rank"] = df.get("home_team_rank", pd.Series([None]*len(df))).fillna(10)
df["away_team_rank"] = df.get("away_team_rank", pd.Series([None]*len(df))).fillna(10)
df["home_form"] = df.get("home_form", pd.Series([None]*len(df))).fillna(1.5)
df["away_form"] = df.get("away_form", pd.Series([None]*len(df))).fillna(1.5)

# Features vorbereiten (One-Hot-Encoding + numerische Features)
features = pd.concat([
    pd.get_dummies(df[["home_team", "away_team"]]),
    df[["home_team_rank", "away_team_rank", "home_form", "away_form"]]
], axis=1)

# Zielvariablen
y_home = df["home_goals"]
y_away = df["away_goals"]

# Train/Test-Split
X_train, X_test, y_home_train, y_home_test = train_test_split(features, y_home, test_size=0.2, random_state=42)
_, _, y_away_train, y_away_test = train_test_split(features, y_away, test_size=0.2, random_state=42)

# Modelle trainieren
model_home = LinearRegression()
model_away = LinearRegression()

model_home.fit(X_train, y_home_train)
model_away.fit(X_train, y_away_train)

# Modelle speichern
with open("model_home.pkl", "wb") as f:
    pickle.dump(model_home, f)

with open("model_away.pkl", "wb") as f:
    pickle.dump(model_away, f)

# Feature-Namen speichern
features.columns.to_series().to_frame(name="feature").to_csv("feature_names.csv", index=False)

print("Modelle erfolgreich trainiert und gespeichert – mit erweiterten Features!")
