#!/bin/python3
from GoogleAuthenticate import authenticate
import requests
import json

# Define the scopes required to access the Google Photos API
SCOPES = ['https://www.googleapis.com/auth/photoslibrary']

def delete_empty_albums():
	"""
	Delete the albums with no items in them.
	"""
	creds = authenticate(SCOPES)
	headers = {
		'Authorization': f'Bearer {creds.token}',
		'Content-type': 'application/json'
	}

	# URLs for the Google Photos API
	albums_url = 'https://photoslibrary.googleapis.com/v1/albums'
	remove_album_url = 'https://photoslibrary.googleapis.com/v1/albums:remove'
	next_page_token = None

	# Loop on the API's responses
	while True:
		params = {'pageSize': 50}
		if next_page_token:
			params['pageToken'] = next_page_token

		response = requests.get(albums_url, headers=headers, params=params)
		if response.status_code == 200:
			data = response.json()
			albums = data.get('albums', [])

			for album in albums:
				album_id = album['id']
				album_title = album['title']
				media_items_count = int(album.get('mediaItemsCount', '0'))
				
				if media_items_count == 0:
					# Remove the empty album
					payload = json.dumps({"albumId": album_id})
					remove_response = requests.post(remove_album_url, headers = headers, data = payload)

					if remove_response.status_code == 200:
						print(f"❌ Successfully removed empty album: {album_title}.")
						print(f"\tID: {album_id}")
					else:
						print(f"⚠️ Failed to remove album: {album_title}.")
						print(f"\tError: {remove_response.status_code}")
						print(f"\tID: {album_id}")
				elif media_items_count > 0:
					print(f"🖼️ Album {album_title} has {media_items_count} item{'s' if media_items_count > 1 else ''}. Skipping removal.")

			next_page_token = data.get('nextPageToken')
			if not next_page_token:
				break
		else:
			print(f"⚠️ Failed to retrieve albums: {response.status_code}")
			print(f"\tResponse: {response.text}")
			break

if __name__ == '__main__':
	delete_empty_albums()