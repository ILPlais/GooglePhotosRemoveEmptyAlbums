#!/bin/python3
import argparse
import pathlib
import os
import platform
from GoogleAuthenticate import authenticate
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
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
	# Create the driver for the browser
	options = Options()
	if args.location:
		options.binary_location = str(args.location)
	options.headless = True
	options.add_argument(f"--user-data-dir={args.profile}")
	driver = webdriver.Chrome(options = options)
	driver.set_window_size(800, 600)

	# Open the album page
	driver.get(album_productUrl)

	# Wait for the page to load
	driver.implicitly_wait(10)

	# Click on the top right button
	ActionChains(driver).move_by_offset(760, 25).click().perform()

	# Click on the "Delete the album" menu item
	ActionChains(driver).move_by_offset(700 - 760, 90 - 25).click().perform()

	# Click on the "Delete" button
	ActionChains(driver).move_by_offset(620 - 760 - 700, 360 - 25 - 90).click().perform()

	# Wait for the page to load
	driver.implicitly_wait(10)

	# Close the browser
	driver.quit()

	return True

if __name__ == '__main__':
	# Command line options
	parser = argparse.ArgumentParser(description = "Delete empty albums from Google Photos.")
	parser.add_argument("-l", "--location",
		required = False,
		type = pathlib.Path,
		help = "Path to the browser location to use.")
	parser.add_argument("-p", "--profile",
		required = False,
		type = pathlib.Path,
		help = "Path to the Chrome profile to use.")
	args = parser.parse_args()

	# Check if the location is provided
	if args.location:
		# Check if the location path uses local variables
		if "%" in str(args.location):
			args.location = pathlib.Path(os.path.expandvars(args.location))

		# Check if the location exists
		if not args.location.exists():
			raise ValueError(f"⚠️ Location not found: {args.location}")
		else:
			print(f"🕸️ Using the provided browser location: {args.location}")

	# If the profile is not provided, use the default profile
	if not args.profile:
		case = platform.system()
		if case == "Windows":
			args.profile = pathlib.Path(os.environ.get("LOCALAPPDATA")) / "Google" / "Chrome" / "User Data"
		elif case == "Darwin":
			args.profile = pathlib.Path(os.environ.get("HOME")) / "Library" / "Application Support" / "Google" / "Chrome" / "Profile"
		elif case == "Linux":
			args.profile = pathlib.Path(os.environ.get("HOME")) / ".config" / "google-chrome" / "Profile"
		else:
			raise ValueError(f"⚠️ Unsupported system: {case}")

	# Check if the profile path uses local variables
	if "%" in str(args.profile):
		args.profile = pathlib.Path(os.path.expandvars(args.profile))

	# Check if the profile exists
	if not args.profile.exists():
		raise ValueError(f"⚠️ Profile not found: {args.profile}")
	else:
		print(f"👤 Using the profile located at: {args.profile}")

	delete_empty_albums()