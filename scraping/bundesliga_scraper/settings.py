BOT_NAME = "bundesliga_scraper"

SPIDER_MODULES = ["bundesliga_scraper.spiders"]
NEWSPIDER_MODULE = "bundesliga_scraper.spiders"

# Respektiere robots.txt (kann auf False gesetzt werden, falls notwendig)
ROBOTSTXT_OBEY = True

# User-Agent (um nicht von der Website geblockt zu werden)
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

# Item Pipelines (für spätere Datenverarbeitung)
ITEM_PIPELINES = {
    "bundesliga_scraper.pipelines.BundesligaScraperPipeline": 300,
}
