import time

from config import config
from dav_functions.webdav import *


def test_webdav_get_static_file():
    """Tests if a static file (that exists already) is present and can be read."""
    content = get_webdav_file_content(
        config.webdav_url + "/" + config.textfile_name,
        config.username,
        config.password)
    assert content is not None
    assert str(content).__contains__(config.textfile_contains)


def test_webdav_write_test_file():
    """Uploads a file via webdav"""
    # Write
    assert upload_file_to_webdav(
        config.webdav_url,
        config.username,
        config.password,
        "test_data/" + config.testfile_name,
        config.testfile_name)
    
    time.sleep(1)  # wait 1 second so Nextcloud can process the upload
    
    
def test_webdav_read_test_file():
    """Reads previously uploaded file via webdav"""
    # Read
    content = get_webdav_file_content(
        config.webdav_url + "/" + config.testfile_name,
        config.username,
        config.password)
    assert content is not None
    assert str(content).__contains__(config.testfile_contains)
    

def test_webdav_delete_test_file():
    """Deletes previously uploaded file via webdav"""
    # Delete
    assert delete_webdav_file(
        config.webdav_url + "/" + config.testfile_name,
        config.username,
        config.password)

    content = get_webdav_file_content(
        config.webdav_url + "/" + config.testfile_name,
        config.username,
        config.password)
    
    print(content)

