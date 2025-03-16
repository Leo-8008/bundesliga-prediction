import scrapy


class BundesligaScraperItem(scrapy.Item):
    rank = scrapy.Field()
    team = scrapy.Field()
    games = scrapy.Field()
    wins = scrapy.Field()
    draws = scrapy.Field()
    losses = scrapy.Field()
    goals = scrapy.Field()
    goal_diff = scrapy.Field()
    points = scrapy.Field()
