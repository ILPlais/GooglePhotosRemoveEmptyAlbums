#!/bin/python3
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

def authenticate(scopes):
	"""
	Authenticates the user and returns the credentials.
	"""
	creds = None

	# Check if a token already exists
	if os.path.exists('token.json'):
		creds = Credentials.from_authorized_user_file('token.json', scopes)

	# If credentials are not valid or do not exist
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			# Refresh the token if necessary
			creds.refresh(Request())
		else:
			# Run the OAuth 2.0 flow to get new credentials
			flow = InstalledAppFlow.from_client_secrets_file('credentials.json', scopes)
			creds = flow.run_local_server(port=0)

		# Save the credentials for future use
		with open('token.json', 'w') as token:
			token.write(creds.to_json())

	return creds