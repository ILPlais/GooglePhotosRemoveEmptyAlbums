#!/bin/python3
from GoogleAuthenticate import authenticate
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains

# Define the scopes required to access the Google Photos API
SCOPES = ['https://www.googleapis.com/auth/photoslibrary.readonly']

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
				album_productUrl = album['productUrl']
				album_media_items_count = int(album.get('mediaItemsCount', '0'))
				
				if album_media_items_count == 0:
					# Remove the empty album
					try:
						if delete_album(album_productUrl):
							print(f"🗑️ Successfully removed empty album: {album_title}.")
							print(f"\tID: {album_id}")
						else:
							print(f"⚠️ Failed to remove album: {album_title}.")
							print(f"\tID: {album_id}")
					except Exception as e:
						print(f"⚠️ Failed to remove album: {album_title}.")
						print(f"\tError: {e}")
						print(f"\tID: {album_id}")
				elif album_media_items_count > 0:
					print(f"🖼️ Album {album_title} has {album_media_items_count} item{'s' if album_media_items_count > 1 else ''}. Skipping removal.")

			next_page_token = data.get('nextPageToken')
			if not next_page_token:
				break
		else:
			print(f"⚠️ Failed to retrieve albums: {response.status_code}")
			break

def delete_album(album_productUrl):
	"""
	Delete the album with the given product URL.
	"""
	# Create the driver for the browser Firefox
	options = Options()
	options.headless = True
	driver = webdriver.Firefox(options = options)
	driver.set_window_size(800, 600)

	# Open the album page
	driver.get(album_productUrl)

	# Wait for the page to load
	driver.implicitly_wait(10)

	# Click on the top right button
	ActionChains(driver).move_by_offset(760, 25).click().perform()

	# Click on the "Delete the album" menu item
	ActionChains(driver).move_by_offset(700, 90).click().perform()

	# Click on the "Delete" button
	#ActionChains(driver).move_by_offset(620, 360).click().perform()
	ActionChains(driver).move_by_offset(475, 360).click().perform()

	# Wait for the page to load
	driver.implicitly_wait(10)

	# Close the browser
	driver.quit()

	return True

if __name__ == '__main__':
	delete_empty_albums()