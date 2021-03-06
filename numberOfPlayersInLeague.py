import requests
import json
import csv

FPL_URL = "https://fantasy.premierleague.com/drf/"
USER_SUMMARY_SUBURL = "element-summary/"
LEAGUE_STANDING_SUBURL = "leagues-classic-standings/"
TEAM_ENTRY_SUBURL = "entry/"
GW_NUMBER = 1
EVENT_SUBURL = "event/" + str(GW_NUMBER) + "/picks"
USER_SUMMARY_URL = FPL_URL + USER_SUMMARY_SUBURL
LEAGUE_STANDING_URL = FPL_URL + LEAGUE_STANDING_SUBURL
ID_TEST = 1

yala_on_scasse_league_id = 336217
reddit_pl_url = 1459
test_entry_id = 2677936

# player data: https://fantasy.premierleague.com/drf/bootstrap-static   (download it in a local file!)

# https://fantasy.premierleague.com/drf/leagues-classic-standings/336217?phase=1&le-page=1&ls-page=5
def getUserEntryIds(league_id, ls_page):
	league_url = LEAGUE_STANDING_URL + str(league_id) + "?phase=1&le-page=1&ls-page=" + str(ls_page)
	r = requests.get(league_url)
	jsonResponse = r.json()
	standings = jsonResponse["standings"]["results"]
	if not standings:
		print("no more standings found!")
		return None

	entries = []

	for player in standings:
		entries.append(player["entry"])

	return entries

# team pick example https://fantasy.premierleague.com/drf/entry/2677936/event/1/picks with 2677936 being entry_id of the player
def getplayersPickedForEntryId(entry_id):
	playerTeamUrlForSpecificGW = FPL_URL + TEAM_ENTRY_SUBURL + str(entry_id) + "/" + EVENT_SUBURL
	r = requests.get(playerTeamUrlForSpecificGW)
	jsonResponse = r.json()
	picks = jsonResponse["picks"]
	elements = []

	for pick in picks:
		elements.append(pick["element"])

	return elements

def getAllPlayersDetailedJson():
	with open('allPlayersInfo.json') as json_data:
		d = json.load(json_data)
		return d


playerElementIdToNameMap = {}
allPlayers = getAllPlayersDetailedJson()
for element in allPlayers["elements"]:
	playerElementIdToNameMap[element["id"]] = element["web_name"].encode('ascii','ignore')


countOfplayersPicked = {}
totalNumberOfPlayersCount = 0
pageCount = 1
while(True):
	try:
		entries = getUserEntryIds(reddit_pl_url, pageCount)
		totalNumberOfPlayersCount += len(entries)
		pageCount += 1
		print(totalNumberOfPlayersCount)
	except:
		pass

#print sorted(countOfplayersPicked.items(), key=lambda x: x[1])
# print countOfplayersPicked