#!/bin/python3
import argparse
import pathlib
import os
import time
import platform
from GoogleAuthenticate import authenticate
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from tqdm import tqdm
from colorama import Fore

# Define the scopes required to access the Google Photos API
SCOPES = ['https://www.googleapis.com/auth/photoslibrary.readonly']

# URLs for the Google Photos API
GOOGLE_PHOTOS_API = 'https://photoslibrary.googleapis.com/v1/albums'

# Class for the album
class Album:
	"""
	Class for the album.
	"""
	def __init__(self, id, title, productUrl, mediaItemsCount):
		self.id = id
		self.title = title
		self.productUrl = productUrl
		self.mediaItemsCount = mediaItemsCount

# Class for the album list
class AlbumList:
	"""
	Class for the album list.
	"""
	def __init__(self):
		self.albums = []

def delete_empty_albums():
	"""
	Delete the albums with no items in them.
	"""
	# Get the empty albums
	albums = list_empty_albums()

	# Loop on the empty albums
	for album in tqdm(albums.albums, desc = "Deleting empty albums", unit = "album"):
		album_id = album['id']
		album_title = album['title']
		album_productUrl = album['productUrl']
		album_media_items_count = int(album.get('mediaItemsCount', '0'))

		# If the album has no items, remove it
		if album_media_items_count == 0:
			# Remove the empty album
			try:
				print(f"""{Fore.YELLOW}🚮 Remove the empty album: "{album_title}"…{Fore.RESET}""")
				print(f"\tURL: {album_productUrl}")

				# Use the browser to remove the album
				if delete_album(album_productUrl):
					print(f"{Fore.GREEN}🗑️ Successfully removed empty album: {album_title}.{Fore.RESET}")
					print(f"\tID: {album_id}")
				else:
					print(f"{Fore.RED}⚠️ Failed to remove album: {album_title}.{Fore.RESET}")
					print(f"\tID: {album_id}")
					print(f"\tURL: {album_productUrl}")
			except Exception as e:
				print(f"{Fore.RED}⚠️ Failed to remove album: {album_title}.{Fore.RESET}")
				print(f"\tError: {e}")
				print(f"\tID: {album_id}")
				print(f"\tURL: {album_productUrl}")

def list_empty_albums() -> AlbumList:
	"""
	List all the empty albums.
	"""
	creds = authenticate(SCOPES)
	headers = {
		'Authorization': f'Bearer {creds.token}',
		'Content-type': 'application/json'
	}

	# Initialize the album list
	album_list = AlbumList()

	# Initialize the token for the pages
	next_page_token = None
	num_pages = 0

	print(f"{Fore.YELLOW}🔍 Retrieving empty albums…{Fore.RESET}")

	# Loop on the API's responses
	while True:
		params = {'pageSize': 50}
		if next_page_token:
			params['pageToken'] = next_page_token

		# Sent a GET request to the Google Photos API to get the albums
		response = requests.get(GOOGLE_PHOTOS_API, headers=headers, params=params)
		if response.status_code == 200:
			data = response.json()
			albums = data.get('albums', [])

			# Add the empty albums to the album list
			for album in albums:
				album_id = album['id']
				album_title = album['title']
				album_productUrl = album['productUrl']
				album_media_items_count = int(album.get('mediaItemsCount', '0'))

				# Add the empty album to the album list
				if album_media_items_count == 0:
					album_list.albums.append(Album(album_id, album_title, album_productUrl, album_media_items_count))

			# Get the next page token
			next_page_token = data.get('nextPageToken')
			num_pages += 1			

			# Print the number of pages and albums
			print(f"{Fore.YELLOW}🔍 Retrieved {num_pages:,} {'pages' if num_pages > 1 else 'page'} ({len(album_list.albums):,} {'albums' if len(album_list.albums) > 1 else 'album'}).{Fore.RESET}")
	
			# If there is no next page token, break the loop
			if not next_page_token:
				break
		else:
			print(f"{Fore.RED}⚠️ Failed to retrieve albums: {response.status_code}.{Fore.RESET}")
			break

	return album_list

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

	try:
		# Open the album page
		driver.get(album_productUrl)

		# Wait for the page to load
		driver.implicitly_wait(10)

		# Click on the top right button
		ActionChains(driver).move_by_offset(750, 30).click().perform()
		time.sleep(0.2)

		# Click on the "Delete the album" menu item
		ActionChains(driver).move_by_offset(0, 60).click().perform()
		time.sleep(0.2)

		# Click on the "Delete" button
		ActionChains(driver).move_by_offset(-150, 200).click().perform()
		time.sleep(1)

		# Wait for the page to load
		driver.implicitly_wait(10)

		return True
	finally:
		# Close the browser
		driver.quit()

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
			raise ValueError(f"{Fore.RED}⚠️ Location not found: {args.location}!{Fore.RESET}")
		else:
			print(f"{Fore.YELLOW}🕸️ Using the provided browser location: {args.location}.{Fore.RESET}")

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
			raise ValueError(f"{Fore.RED}⚠️ Unsupported system: {case}!{Fore.RESET}")

	# Check if the profile path uses local variables
	if "%" in str(args.profile):
		args.profile = pathlib.Path(os.path.expandvars(args.profile))

	# Check if the profile exists
	if not args.profile.exists():
		raise ValueError(f"{Fore.RED}⚠️ Profile not found: {args.profile}!{Fore.RESET}")
	else:
		print(f"{Fore.YELLOW}👤 Using the profile located at: {args.profile}.{Fore.RESET}")

	delete_empty_albums()