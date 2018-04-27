import requests
import json
import csv
import argparse
from pandas import DataFrame

class League():

	def getPlayerHistory(self, playerName, history_url, playerscores):
		r = requests.get(history_url)
		json = r.json()
		history = json['history']
		for gw in history:
			if gw['event'] == '0':
				playerscores[playerName][int(gw['event']) - 1] = gw['points']
			else:
				playerscores[playerName][int(gw['event']) - 1] = gw['points'] + playerscores[playerName][int(gw['event']) - 2]
		return playerscores

	def main(self, leagueId, gw, playerlimit):
		FPL_URL = "https://fantasy.premierleague.com/drf/"
		LEAGUE_CLASSIC_URL = "leagues-classic-standings/"

		league_url = FPL_URL + LEAGUE_CLASSIC_URL + leagueId + '?phase=1'
		playerscores = {}

		# Get all players
		#try:
		r = requests.get(league_url)
		json = r.json()
		leaguename = json['league']['name']
		playernames, playerids = [x['entry_name'] for x in json['standings']['results']], [x['entry'] for x in json['standings']['results']]
		if len(playernames) > playerlimit:
			playernames = playernames[:playerlimit]
			playerids = playerids[:playerlimit]

		values = [[0 for _ in range(gw + 1)] for _ in range(len(playernames))]
		playerscores = dict(zip(playernames, values))
		nameToId = dict(zip(playernames, playerids))

		# Get point history for every player
		for player in playernames:
			playerHistoryUrl = FPL_URL + "entry/" + str(nameToId[player]) + "/history"
			playerscores = self.getPlayerHistory(player, playerHistoryUrl, playerscores)

		df = DataFrame.from_dict(playerscores, orient='index')
		return leaguename, df
		#except:
		#	return None, "Error, could not find league with ID " + str(leagueId)


"""
parser = argparse.ArgumentParser(description="Get league statistics over time")
parser.add_argument('-l', '--league', dest='league', required=True)
parser.add_argument('-gw', '--gameweek', dest='gw', type=int, required=True)
args = parser.parse_args()
"""