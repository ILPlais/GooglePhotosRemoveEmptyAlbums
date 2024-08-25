# Google Photos remove empty albums
Remove all empty albums from a Google Photos account

# How-to use

To retrive the Google libraries needed to use the Google Photos REST API, follow this steps:

## Install libraries

You will need the Google Auth libraries. You can install them using **pip**:

```
pip install google-auth google-auth-oauthlib google-auth-httplib2
```

## Configure the OAuth 2.0 indetification informations

1. Go to the [Google Cloud console](https://console.cloud.google.com/).
2. Create a new project or select an existing one.
3. Activate the Google Photos Library API for your project.
4. Configure the OAuth 2.0 consent screen.
5. Create OAuth 2.0 credentials and download the `credentials.json` file.