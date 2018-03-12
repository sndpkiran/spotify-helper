#!/usr/bin/env python

import requests
import urllib
import urlparse
import webbrowser
import base64
from creds import *

scopes = "user-read-private user-read-email"

def main():
	authorize_url = "https://accounts.spotify.com/authorize?response_type=code"
	token_url = "https://accounts.spotift.com/api/token"
	
	params = { "client_id": client_id,
	 	   "scope": scopes,
		   "redirect_uri": redirect_uri }
	
	# params_string = urllib.urlencode(params)
	# webbrowser.open(authorize_url + "&" + params_string)

	response_url = raw_input("Please copy and paste the redirected url here: ")
	url_info = urlparse.parse_qs(urlparse.urlsplit(response_url).query)
	
	code = str(url_info['code'][0])

	token_params = {"grant_type": "authorization_code",
			"code": code,
			"redirect_uri": redirect_uri}

	auth = base64.b64encode(client_id + ":" + client_secret)
	headers = {"Authorization": "Basic " + auth}

if __name__ == "__main__":
	main()
