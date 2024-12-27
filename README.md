
# Google Photos remove empty albums
Remove all empty albums from a Google Photos account

# How-to use

To retrieve the Google libraries needed to use the Google Photos REST API, follow these steps:

## Create your virtual environment

You can create your virtual environment with Python:

**Under Linux or macOD:**

```bash
python3 -m venv .venv
```

**Under Windows:**

```powershell
python -m venv .venv
```

## Switch on your new virtual environment

**Under Linux or macOS:**

```bash
source .venv/bin/activate
```

**Under Windows:**

 - In **PowerShell**:
	```powershell
	.\.venv\Scripts\Activate.ps1
	```

 - In **Command Prompt**:
	```batch
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

## Using the script

The script use the [Selenium WebDriver](https://www.selenium.dev/documentation/webdriver/) to control your browser.

It only works with [Google Chrome](https://www.google.fr/chrome/browser/) and [Chromium](https://www.chromium.org/Home/) browsers.

**First, you need to be connected to your Google Account in the browser you will use.**

### Command line

```
usage: DeleteEmptyAlbums.py [-h] [-l LOCATION] [-p PROFILE]

Delete empty albums from Google Photos.

options:
  -h, --help            show this help message and exit
  -l LOCATION, --location LOCATION
                        Path to the browser location to use. Work only with Google Chrome or Chromium.
  -p PROFILE, --profile PROFILE
                        Path to the user profile to use.
```

### Examples

With **Google Chrome** and the **default user** profile:
```
python3 DeleteEmptyAlbums.py
```
  - The default user profile paths are:
    - Under **Windows**:
		```batch
		%LOCALAPPDATA%\Google\Chrome\User Data\
		```
    - Under **macOS**:
		```bash
		$HOME/Library/Application Support/Google/Chrome/Profile/
		```
    - Under **Linux**:
		```bash
		$HOME/.config/google-chrome/Profile/
		```

With **Chromium** and the **default user** profile under **Windows PowerShell**, if only Chromium is installed:
```powershell
python .\DeleteEmptyAlbums.py --profile "$ENV:LOCALAPPDATA\Chromium\User Data"
```

With **Chromium** under **Windows PowerShell** with the specific path to Chromium:
```powershell
python .\DeleteEmptyAlbums.py --location "$ENV:ProgramFiles\Chromium\Application\chrome.exe" --profile "$ENV:LOCALAPPDATA\Chromium\User Data"
```

With **Chromium** under the **Windows Command Prompt**:
```batch
python DeleteEmptyAlbums.py --location "%ProgramFiles%\Chromium\Application\chrome.exe" --profile "%LOCALAPPDATA%\Chromium\User Data"
```
