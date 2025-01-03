#!/bin/python3
from GoogleAuthenticate import authenticate
import requests

# Define the scopes required to access the Google Photos API
SCOPES = ['https://www.googleapis.com/auth/photoslibrary.readonly']

# URLs for the Google Photos API
GOOGLE_PHOTOS_API = 'https://photoslibrary.googleapis.com/v1/albums'

def list_albums():
	"""
	Lists photo albums with their names and the number of photos they contain.
	"""
	creds = authenticate(SCOPES)
	headers = {
		'Authorization': f'Bearer {creds.token}'
	}

	# Initialize the token for the pages
	next_page_token = None

	# Loop on the API's responses
	while True:
		# Increase page size to retrieve more albums at once
		params = {'pageSize': 50}

		if next_page_token:
			params['pageToken'] = next_page_token

		# Send a GET request to the Google Photos API to retrieve albums
		response = requests.get(GOOGLE_PHOTOS_API, headers = headers, params = params)
		if response.status_code == 200:
			data = response.json()
			albums = data.get('albums', [])

			# Iterate through each album and print its name and number of photos
			for album in albums:
				album_id = album['id']
				album_title = album['title']
				album_productUrl = album['productUrl']
				album_media_items_count = album.get('mediaItemsCount', '0')
				print(f"🖼️ Album: {album_title}")
				print(f"\tID: {album_id}")
				print(f"\tURL: {album_productUrl}")
				print(f"\tNumber of photos: {album_media_items_count}")

			next_page_token = data.get('nextPageToken')

			# Exit the loop if we have reach the last page
			if not next_page_token:
				break
		else:
			print(f"⚠️ Failed to retrieve albums: {response.status_code}")

if __name__ == '__main__':
	# Call the function to list albums
	list_albums()