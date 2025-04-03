import pickle
import pandas as pd

# Beispiel-Teams + zusätzliche Feature-Werte
home_team = "FC Bayern München"
away_team = "Bor. Dortmund"
home_team_rank = 1           # Tabellenplatz Heimteam
away_team_rank = 2           # Tabellenplatz Auswärtsteam
home_form = 2.6              # z. B. Ø Punkte aus letzten 5 Heimspielen
away_form = 1.4              # z. B. Ø Punkte aus letzten 5 Auswärtsspielen

# Feature-Namen laden
feature_names = pd.read_csv("feature_names.csv")["feature"].tolist()

# Eingabefeatures erzeugen
input_data = pd.DataFrame(columns=feature_names)
input_data.loc[0] = 0  # alle Features initialisieren

# One-Hot-Encoding der Teams
if f"home_team_{home_team}" in input_data.columns:
    input_data.loc[0, f"home_team_{home_team}"] = 1
if f"away_team_{away_team}" in input_data.columns:
    input_data.loc[0, f"away_team_{away_team}"] = 1

# Neue numerische Features setzen
if "home_team_rank" in input_data.columns:
    input_data.loc[0, "home_team_rank"] = home_team_rank
if "away_team_rank" in input_data.columns:
    input_data.loc[0, "away_team_rank"] = away_team_rank
if "home_form" in input_data.columns:
    input_data.loc[0, "home_form"] = home_form
if "away_form" in input_data.columns:
    input_data.loc[0, "away_form"] = away_form

# Modelle laden
with open("model_home.pkl", "rb") as f:
    model_home = pickle.load(f)

with open("model_away.pkl", "rb") as f:
    model_away = pickle.load(f)

# Vorhersage
pred_home_goals = round(model_home.predict(input_data)[0])
pred_away_goals = round(model_away.predict(input_data)[0])

print(f"Vorhergesagtes Ergebnis für {home_team} vs. {away_team}: {pred_home_goals}:{pred_away_goals}")
