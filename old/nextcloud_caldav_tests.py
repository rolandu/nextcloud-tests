import configparser
import caldav

# Read the configuration
config = configparser.ConfigParser()
config.read('config.py')

# Get CalDAV details from the config
base_url = config.get('nextcloud', 'base_url')
username = config.get('nextcloud', 'username')
password = config.get('nextcloud', 'password')

# Advanced variables
caldav_url = base_url + "remote.php/dav/calendars/" + username + "/me/"

# Connect to the CalDAV server
client = caldav.DAVClient(url=caldav_url, username=username, password=password)
principal = client.principal()

try:
    # Fetch and list all calendars
    calendars = principal.calendars()
    if calendars:
        print("Calendars found:")
        for calendar in calendars:
            print(calendar)
    else:
        print("No calendars found.")

except Exception as e:
    print(f"An error occurred: {e}")
