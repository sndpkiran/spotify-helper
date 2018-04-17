#!/usr/bin/env python

import requests
import urllib
import urlparse
import webbrowser
import base64
import json
from creds import *

scopes = "user-read-private user-read-email playlist-modify-public"
authorize_url = "https://accounts.spotify.com/authorize?response_type=code"
token_url = "https://accounts.spotify.com/api/token"
api_url = "https://api.spotify.com/v1/me"
playlist_url = "https://api.spotify.com/v1/users/"

def get_playlists(user, headers):
	user_id = user.json()['id']
	playlists = requests.get(playlist_url + user_id + "/playlists", headers=headers)

	playlist_id = playlists.json()['items'][1]['id']

	tracks  = json.loads(requests.get(playlist_url + user_id + "/playlists/" + playlist_id + "/tracks",  headers=headers).content)
	count = len(tracks['items'])

	headers['Content-type'] = "application/json"
	payload = '{"range_start": 0, "insert_before": 4}'
	response = requests.put(playlist_url + user_id + "/playlists/" + playlist_id + "/tracks", data=payload, headers=headers)

	print response.content


	for i in range(6):
		name = tracks['items'][i]['track']['name']
		album = tracks['items'][i]['track']['album']['name']
		print name + " - " + album


def main():

	params = { "client_id": client_id,
	 	   "scope": scopes,
		   "redirect_uri": redirect_uri }

	params_string = urllib.urlencode(params)
	webbrowser.open(authorize_url + "&" + params_string)

	response_url = raw_input("Please copy and paste the redirected url here: ")
	url_info = urlparse.parse_qs(urlparse.urlsplit(response_url).query)

	code = str(url_info['code'][0])

	token_params = {"grant_type": "authorization_code",
			"code": code,
			"redirect_uri": redirect_uri,
			"client_id": client_id,
			"client_secret": client_secret}

	# TODO: Fix encoding issue in python 2
	# auth = base64.b64encode(client_id + ":" + client_secret)
	# headers = {"Authorization": "Basic " + auth}

	# body = {"client_id": client_id,
		# "client_secret": client_secret}

	token_response = requests.post(token_url, data=token_params)
	access_token = token_response.json()['access_token']

	headers = {"Authorization": "Bearer " + access_token}
	user = requests.get(api_url, headers=headers)

	# print user.content
	get_playlists(user, headers)

if __name__ == "__main__":
	main()
