import argparse
import sqlite3
import sys
import time

import requests

parser = argparse.ArgumentParser(description='Scrapes GBFS Station status to sqlite.')
parser.add_argument('--gbfsurl', dest='gbfs_url', help='GBFS root URL')
parser.add_argument('--sqlitefile', dest='sqlite_file', help='filepath to sqlite file, where information are saved')
parser.add_argument('--interval', dest='interval', type=int, default=90, help='interval of requests in seconds (default 90)')
args = parser.parse_args()

if not args.gbfs_url:
	sys.exit("--gbfsurl missing")
if not args.sqlite_file:
	sys.exit("--sqlitefile missing")

connection = sqlite3.connect(args.sqlite_file)
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS station_status(timestamp INTEGER, station_id TEXT, num_bikes_available INTEGER, station_name TEXT, lat REAL, lon REAL) ")
connection.commit()
r = requests.get(args.gbfs_url)
gbfs = r.json()

gbfs_lang = list(gbfs['data'])[0]
gbfs_feeds = gbfs['data'][gbfs_lang]['feeds']
station_status_url = list(filter(lambda feed: feed['name'] == "station_status", gbfs_feeds))[0]['url']
station_information_url = list(filter(lambda feed: feed['name'] == "station_information", gbfs_feeds))[0]['url']



while True:
	try:
		station_information_request = requests.get(station_information_url)
		station_information = station_information_request.json()
		station_status_request = requests.get(station_status_url)
		station_status = station_status_request.json()

		for station in station_status['data']['stations']:
			cur_station_information = list(filter(lambda si_station: si_station['station_id'] == station['station_id'], station_information['data']['stations']))[0]
			cursor.execute("INSERT INTO station_status (timestamp, station_id, num_bikes_available, station_name, lat, lon) VALUES(:timestamp, :station_id, :num_bikes_available, :station_name, :lat, :lon)", {
					"timestamp": station_status['last_updated'],
					"station_id": station['station_id'],
					"num_bikes_available": station['num_bikes_available'],
					"station_name": cur_station_information['name'],
					"lat": cur_station_information['lat'],
					"lon": cur_station_information['lon']
				})
		connection.commit()
	except Exception as e:
		print(e)
	
	time.sleep(args.interval)