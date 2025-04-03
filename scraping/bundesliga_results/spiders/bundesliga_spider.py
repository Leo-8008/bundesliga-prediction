import scrapy
import json
import os

class BundesligaResultsSpider(scrapy.Spider):
    name = "bundesliga_results"
    allowed_domains = ["transfermarkt.de"]
    start_urls = [
        f"https://www.transfermarkt.de/bundesliga/spieltag/wettbewerb/L1?saison_id={year}&spieltag={i}"
        for year in [2019, 2024] for i in range(1, 35)
    ]

    all_matches = []

    def parse(self, response):
        season = response.url.split("saison_id=")[1].split("&")[0]
        matchday = response.url.split("spieltag=")[-1]

        rows = response.xpath("//tr[contains(@class, 'table-grosse-schrift')]")
        matches = []

        for game in rows:
            team_home = game.xpath(".//td[contains(@class, 'rechts hauptlink') and contains(@class, 'spieltagsansicht-vereinsname')][1]/a[last()]/text()").get()
            team_away = game.xpath(".//td[contains(@class, 'hauptlink') and contains(@class, 'spieltagsansicht-vereinsname') and contains(@class, 'no-border-links')][1]/a[1]/text()").get()
            score = game.xpath(".//span[@class='matchresult finished']/text()").get()
            date_row = game.xpath("following-sibling::tr[1]")
            date = date_row.xpath(".//a/text()").get()
            rank_home = game.xpath(".//td[contains(@class, 'rechts')]/span[@class='tabellenplatz']/text()").get()
            rank_away = game.xpath(".//td[contains(@class, 'no-border-links')]/span[@class='tabellenplatz']/text()").get()

            rank_home = int(rank_home.strip("().")) if rank_home else None
            rank_away = int(rank_away.strip("().")) if rank_away else None

            if team_home and team_away and score:
                matches.append({
                    "season": season,
                    "matchday": matchday,
                    "home_team": team_home.strip(),
                    "away_team": team_away.strip(),
                    "score": score.strip(),
                    "date": date.strip() if date else None,
                    "home_team_rank": rank_home,
                    "away_team_rank": rank_away,
                })

        self.all_matches.extend(matches)
        self.log(f" {len(matches)} Spiele gesammelt für Saison {season}, Spieltag {matchday}")

    def closed(self, reason):
        
        # Datei im Hauptordner speichern
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        filename = os.path.join(project_root, "bundesliga_results.json")
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.all_matches, f, ensure_ascii=False, indent=4)
        self.log(f" Gesamtergebnis gespeichert ({len(self.all_matches)} Spiele) → {filename}")
