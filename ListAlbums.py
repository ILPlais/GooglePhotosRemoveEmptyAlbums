#!/bin/python3
import os
import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import requests

# Define the scopes required to access the Google Photos API
SCOPES = ['https://www.googleapis.com/auth/photoslibrary.readonly']

def authenticate():
	"""
	Authenticates the user and returns the credentials.
	"""
	creds = None

	# Check if a token already exists
	if os.path.exists('token.json'):
		creds = Credentials.from_authorized_user_file('token.json', SCOPES)

	# If credentials are not valid or do not exist
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			# Refresh the token if necessary
			creds.refresh(Request())
		else:
			# Run the OAuth 2.0 flow to get new credentials
			flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
			creds = flow.run_local_server(port=0)

		# Save the credentials for future use
		with open('token.json', 'w') as token:
			token.write(creds.to_json())

	return creds

def list_albums():
	"""
	Lists photo albums with their names and the number of photos they contain.
	"""
	creds = authenticate()
	headers = {
		'Authorization': f'Bearer {creds.token}'
	}

	# URL for the Google Photos API
	url = 'https://photoslibrary.googleapis.com/v1/albums'
	next_page_token = None

	# Loop on the API's responses
	while True:
		# Increase page size to retrieve more albums at once
		params = {'pageSize': 50}

		if next_page_token:
			params['pageToken'] = next_page_token

		# Send a GET request to the Google Photos API to retrieve albums
		response = requests.get(url, headers = headers, params = params)
		if response.status_code == 200:
			data = response.json()
			albums = data.get('albums', [])

			# Iterate through each album and print its name and number of photos
			for album in albums:
				album_id = album['id']
				album_title = album['title']
				media_items_count = album.get('mediaItemsCount', '0')
				print(f"Album: {album_title}")
				print(f"\tID: {album_id}")
				print(f"\tNumber of photos: {media_items_count}")

			next_page_token = data.get('nextPageToken')

			# Exit the loop if we have reach the last page
			if not next_page_token:
				break
		else:
			print(f"Failed to retrieve albums: {response.status_code}")

if __name__ == '__main__':
	# Call the function to list albums
	list_albums()