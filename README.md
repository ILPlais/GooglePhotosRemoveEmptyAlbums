# Google Photos remove empty albums
Remove all empty albums from a Google Photos account

# How-to use

To retrieve the Google libraries needed to use the Google Photos REST API, follow these steps:

## Create your virtual environment

You can create your virtual environment with Python:

**Under Linux:**

```
python3 -m venv .venv
```

**Under Windows:**

```
python -m venv .venv
```

## Switch on your new virtual environment

**Under Linux:**

```
source .venv/bin/activate
```

**Under Windows:**

 - In PowerShell:
	```
	.\.venv\Scripts\Activate.ps1
	```

 - In Command Line:
	```
	.venv\Scripts\activate.bat
	```
## Install libraries

You will need the Google Auth libraries. You can install them using **pip**:

```
pip install --requirement requirements.txt
```

## Configure the OAuth 2.0 identification information

1. Go to the [Google Cloud console](https://console.cloud.google.com/).
2. Create a new project or select an existing one.
3. Activate the Google Photos Library API for your project.
4. Configure the OAuth 2.0 consent screen.
5. Create OAuth 2.0 credentials and download the `credentials.json` file.
