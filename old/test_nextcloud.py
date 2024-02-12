import caldav
import time

import pytest

import config
from dav_functions.caldav import *
from dav_functions.carddav import *
from dav_functions.webdav import *


def test_get_static_file():
    content = get_webdav_file_content(
        config.webdav_url + "/" + config.textfile_name,
        config.username,
        config.password)
    assert content is not None
    assert str(content).__contains__(config.textfile_contains)


def test_write_read_delete_a_file():
    # Write
    assert upload_file_to_webdav(
        config.webdav_url,
        config.username,
        config.password,
        config.testfile_name,
        config.testfile_name)
    
    time.sleep(1)  # wait 1 second
    
    # Read
    content = get_webdav_file_content(
        config.webdav_url + "/" + config.testfile_name,
        config.username,
        config.password)
    assert content is not None
    assert str(content).__contains__(config.testfile_contains)
    
    # Delete
    assert delete_webdav_file(
        config.webdav_url + "/" + config.testfile_name,
        config.username,
        config.password)


def test_caldav():
    # Connect to the CalDAV server
    client = caldav.DAVClient(
        url=config.caldav_url,
        username=config.username,
        password=config.password
    )
    principal = client.principal()
    
    # Get the proper calendar
    calendars = principal.calendars()
    if not calendars:
        pytest.fail("No calendars found on the CalDAV server.")
    calendar = get_calendar_by_name(principal, config.calendar_name)
    if not calendar:
        pytest.fail("Calendar " + config.calendar_name + " not found")

    # Example test_event
    test_event_summary = "Meeting with Bob (Test Event)"

    event_data = create_event_data(
        test_event_summary,
        datetime(2023, 11, 15, 14, 0, 0),
        datetime(2023, 11, 15, 15, 0, 0),
        "Discuss project updates"
    )

    # we also need to give a range when we search for it
    search_range_start = datetime(2023,11,10)
    search_range_end = datetime(2023,11,20)

    # Create an event
    create_caldav_event(calendar, event_data)
    
    # Read events to verify creation
    retrieved_event = get_calendar_event_by_name_range(
        calendar,
        test_event_summary,
        search_range_start,
        search_range_end
    )
    assert retrieved_event is not None, "Event was not created successfully."

    # Delete the test_event
    retrieved_event_uid = retrieved_event.instance.vevent.uid.value
    assert delete_caldav_event(
        calendar,
        retrieved_event_uid,
        search_range_start,
        search_range_end
    ), "Event deletion failed."


# @pytest.mark.skip(reason="bug in Nextcloud, needs to be resolved first")
def test_carddav():
    contact_info = {
        "fullname": "John Doe",
        "email": "johndoe@example.com"
    }

    # Create a contact
    assert create_carddav_contact(
        config.carddav_url,
        config.username,
        config.password,
        contact_info), "Failed to create contact"

    # Fetch contacts
    contacts = fetch_carddav_contacts(
        config.carddav_url,
        config.username,
        config.password)
    assert contacts is not None
    
    to_be_deleted = ""
    for contact in contacts:
        if contact["fn"] == "John Doe":
            to_be_deleted = contact["href"].rpartition('/')[-1]
    
    assert to_be_deleted is not None, "Contact not found after creation"
    assert to_be_deleted != ""

    # Delete the contact
    assert delete_carddav_contact(
        config.carddav_url,
        config.username,
        config.password,
        to_be_deleted), "Failed to delete contact"
