import scrapers

#ixture = scrapers.scraper_fixture_fiba_basketball("https://www.fiba.basketball/es/basketballworldcup/2023/games")
#
#rint(scrapers.scraper_actions_fiba_basketball(fixture))

print(scrapers.boxscore_four_factors(["/es/basketballworldcup/2023/game/2608/South-Sudan-Puerto-Rico","/es/basketballworldcup/2023/game/2808/Puerto-Rico-Serbia", "/es/basketballworldcup/2023/game/3008/China-Puerto-Rico", "/es/basketballworldcup/2023/game/2508/Dominican-Republic-Philippines", "/es/basketballworldcup/2023/game/2708/Italy-Dominican-Republic", "/es/basketballworldcup/2023/game/2908/Angola-Dominican-Republic"]))