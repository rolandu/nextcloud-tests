import caldav
import pytest

from config import config
from dav_functions.caldav import *

# defining constants

# Example test event summary (name)
test_event_summary = "Meeting with Bob (Test Event)"
test_event_start = datetime(2023, 11, 15, 14, 0, 0)
test_event_end = datetime(2023, 11, 15, 15, 0, 0)
test_event_description = "Discuss project updates"
test_event_description_new = "Updated description"

# we need to give a range when we search for it
search_range_start = datetime(2023, 11, 10)
search_range_end = datetime(2023, 11, 20)


def get_current_state_of_test_event(caldav_calendar):
    return get_calendar_event_by_name_range(
        caldav_calendar,
        test_event_summary,
        search_range_start,
        search_range_end
    )


@pytest.fixture(scope="module")
def caldav_principal():
    # Connect to the CalDAV server
    client = caldav.DAVClient(
        url=config.caldav_url,
        username=config.username,
        password=config.password
    )
    principal = client.principal()
    
    yield principal


@pytest.fixture(scope="module")
def caldav_calendar(caldav_principal):
    # Get the proper calendar
    calendars = caldav_principal.calendars()
    if not calendars:
        pytest.fail("No calendars found on the CalDAV server.")
    calendar = get_calendar_by_name(caldav_principal, config.calendar_name)
    if not calendar:
        pytest.fail("Calendar " + config.calendar_name + " not found")
    
    yield calendar


def test_caldav_create_and_read(caldav_calendar):
    # Check that the event does not already exist
    retrieved_event = get_current_state_of_test_event(caldav_calendar)
    assert retrieved_event is None, "Calendar is not clean prior to first test."
    
    # Create an event
    event_data = create_event_data(
        test_event_summary,
        test_event_start,
        test_event_end,
        test_event_description
    )
    create_caldav_event(caldav_calendar, event_data)
    
    # Read events to verify creation
    retrieved_event = get_current_state_of_test_event(caldav_calendar)
    assert retrieved_event is not None, "Event was not created successfully."


def test_caldav_update(caldav_calendar):
    # Get event
    retrieved_event = get_current_state_of_test_event(caldav_calendar)
    assert retrieved_event is not None, "Event does not exist."
    ical_event = retrieved_event.icalendar_instance
    vevent = ical_event.walk('VEVENT')[0]
    assert vevent['DESCRIPTION'] == test_event_description
    
    # Update the description
    vevent['DESCRIPTION'] = test_event_description_new
    
    retrieved_event.data = ical_event.to_ical()
    retrieved_event.save()
    
    # Get event
    retrieved_event = get_current_state_of_test_event(caldav_calendar)
    ical_event = retrieved_event.icalendar_instance
    vevent = ical_event.walk('VEVENT')[0]
    assert vevent['DESCRIPTION'] == test_event_description_new
    

def test_caldav_delete(caldav_calendar):
    # Get event
    retrieved_event = get_current_state_of_test_event(caldav_calendar)
    assert retrieved_event is not None, "Event was not created successfully."
    retrieved_event_uid = retrieved_event.instance.vevent.uid.value
    
    # Delete the test_event
    assert delete_caldav_event(
        caldav_calendar,
        retrieved_event_uid,
        search_range_start,
        search_range_end
    ), "Event deletion failed."
    
    # Getting the event should fail now
    retrieved_event = get_current_state_of_test_event(caldav_calendar)
    assert retrieved_event is None
