

# Base config
base_url = "https://my.server:port/nextcloud-path/"
username = "username"
password = "password"

# name of a calendar the user already has
calendar_name = "Personal"

# a file that already exists on the server in the base directory of this user, including some text
textfile_name = "test-textfile.txt"
textfile_contains = "This is a textfile."

# a file that will be created and deleted during the tests, make sure the file is not there before the tests
testfile_name = "test_upload.txt"
testfile_contains = "I am also a test."

# Advanced variables, these should not change as long as the test is used on Nextcloud (or nextcloud changes something)
webdav_url = base_url + "remote.php/dav/files/" + username
caldav_url = base_url + "remote.php/dav/calendars/" + username
carddav_url = base_url + "remote.php/dav/addressbooks/users/" + username + "/contacts"
