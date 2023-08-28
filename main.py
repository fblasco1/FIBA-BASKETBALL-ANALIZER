import scrapers

fixture = scrapers.scraper_fixture_fiba_basketball("https://www.fiba.basketball/es/basketballworldcup/2023/games")

print(scrapers.scraper_actions_fiba_basketball(fixture))