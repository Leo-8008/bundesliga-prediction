import scrapy


class BundesligaSpider(scrapy.Spider):
    name = "bundesliga"
    allowed_domains = ["transfermarkt.de"]
    start_urls = [
        "https://www.transfermarkt.de/bundesliga/tabelle/wettbewerb/L1/saison_id/2023"
    ]

    def parse(self, response):
        rows = response.xpath("//table[contains(@class, 'items')]/tbody/tr")

        for row in rows:
            yield {
                "rank": row.xpath(".//td[contains(@class, 'rechts hauptlink')]/text()").get(default="").strip(),
                "team": row.xpath(".//td[contains(@class, 'hauptlink')][2]/a/text()").get(default="").strip(),
                "games": row.xpath(".//td[@class='zentriert'][1]/text()").get(default="").strip(),
                "wins": row.xpath(".//td[@class='zentriert'][2]/text()").get(default="").strip(),
                "draws": row.xpath(".//td[@class='zentriert'][3]/text()").get(default="").strip(),
                "losses": row.xpath(".//td[@class='zentriert'][4]/text()").get(default="").strip(),
                "goals": row.xpath(".//td[@class='zentriert'][5]/text()").get(default="").strip(),
                "goal_diff": row.xpath(".//td[@class='zentriert'][6]/text()").get(default="").strip(),
                "points": row.xpath(".//td[@class='zentriert'][7]/text()").get(default="").strip(),
            }
