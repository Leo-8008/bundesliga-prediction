import os
import json
import pandas as pd

base_path = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(base_path, "bundesliga_results.json")

with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(data)


df[["home_goals", "away_goals"]] = df["score"].str.extract(r"(\d+):(\d+)").astype(float)

df["date"] = pd.to_datetime(df["date"], format="%d.%m.%Y", errors="coerce")


df["home_form"] = 0.0
df["away_form"] = 0.0


for idx, row in df.iterrows():
    date = row["date"]
    home_team = row["home_team"]
    away_team = row["away_team"]

    prev_home_games = df[
        (df["home_team"] == home_team) &
        (df["date"] < date)
    ].sort_values("date", ascending=False).head(3)

    prev_away_games = df[
        (df["away_team"] == away_team) &
        (df["date"] < date)
    ].sort_values("date", ascending=False).head(3)


    def calc_form(games, team_col, goals_for, goals_against):
        form = 0
        for _, g in games.iterrows():
            gf = g[goals_for]
            ga = g[goals_against]
            if gf > ga:
                form += 3
            elif gf == ga:
                form += 1
        return form

    df.at[idx, "home_form"] = calc_form(prev_home_games, "home_team", "home_goals", "away_goals")
    df.at[idx, "away_form"] = calc_form(prev_away_games, "away_team", "away_goals", "home_goals")

# Datum wieder zu String machen für JSON-Speicherung
df["date"] = df["date"].dt.strftime("%d.%m.%Y")

# Zurückspeichern
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(df.to_dict(orient="records"), f, ensure_ascii=False, indent=4)

print("Form-Features erfolgreich ergänzt!")
