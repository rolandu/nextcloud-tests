import requests


def get_webdav_file_content(webdav_url, username, password):
    """
    Retrieves the content of a file from a WebDAV server.

    :param webdav_url: URL of the file on the WebDAV server
    :param username: WebDAV server username
    :param password: WebDAV server password
    :return: Content of the file or None if an error occurs
    """
    try:
        response = requests.get(webdav_url, auth=(username, password))
        response.raise_for_status()  # This will raise an HTTPError if the HTTP request returned an unsuccessful status code
        return response.content
    except requests.RequestException as e:
        print(f"Error retrieving the file: {e}")
        return None


# Example Usage
# webdav_url = "https://your-webdav-server.com/path/to/file"
# username = "your_username"
# password = "your_password"
# content = get_webdav_file_content(webdav_url, username, password)
# if content is not None:
#     print(content)


def upload_file_to_webdav(webdav_url, username, password, local_file_path, remote_file_name):
    """
    Uploads a file to a WebDAV server.

    :param webdav_url: URL of the WebDAV server (directory where the file will be stored)
    :param username: WebDAV server username
    :param password: WebDAV server password
    :param local_file_path: Path to the local file to be uploaded
    :param remote_file_name: The name of the file on the server after upload
    :return: True if upload was successful, False otherwise
    """
    try:
        # Open the file in binary mode
        with open(local_file_path, 'rb') as file:
            # Construct the full URL (directory URL + file name)
            full_url = f'{webdav_url.rstrip("/")}/{remote_file_name}'
            
            # Perform the PUT request to upload the file
            response = requests.put(full_url, data=file, auth=(username, password))
            response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
            
            return True
    except requests.RequestException as e:
        print(f"Error uploading the file: {e}")
        return False


# Example Usage
# webdav_url = "https://your-webdav-server.com/path/to/directory"
# username = "your_username"
# password = "your_password"
# local_file_path = "/path/to/your/local/file"
# remote_file_name = "uploaded_file.txt"
# success = upload_file_to_webdav(webdav_url, username, password, local_file_path, remote_file_name)
# if success:
#     print("File uploaded successfully.")
# else:
#     print("Failed to upload the file.")


def delete_webdav_file(webdav_url, username, password):
    """
    Deletes a file from a WebDAV server.

    :param webdav_url: The full URL to the file on the WebDAV server
    :param username: The username for WebDAV server authentication
    :param password: The password for WebDAV server authentication
    :return: True if deletion was successful, False otherwise
    """
    try:
        response = requests.delete(webdav_url, auth=(username, password))
        response.raise_for_status()  # This will raise an HTTPError if the HTTP request returned an unsuccessful status code
        return True
    except requests.RequestException as e:
        print(f"Error occurred: {e}")
        return False

# Example usage:
# success = delete_webdav_file("https://webdav.server.com/path/to/file", "username", "password")
# if success:
#     print("File deleted successfully.")
# else:
#     print("Failed to delete the file.")
