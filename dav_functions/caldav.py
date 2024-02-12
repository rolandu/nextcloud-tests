from datetime import datetime
import uuid


def get_calendar_by_name(principal, calendar_name):
    """ Get a calendar by its name. """
    calendars = principal.calendars()
    for calendar in calendars:
        if calendar.name == calendar_name:
            return calendar
    return None


def create_event_data(summary, start, end, description=""):
    """ Creates event data in iCalendar format. """
    event = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "BEGIN:VEVENT",
        f"SUMMARY:{summary}",
        f"DTSTART:{start.strftime('%Y%m%dT%H%M%SZ')}",
        f"DTEND:{end.strftime('%Y%m%dT%H%M%SZ')}",
        f"DTSTAMP:{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}",
        f"UID:{uuid.uuid4()}",
        f"DESCRIPTION:{description}",
        "END:VEVENT",
        "END:VCALENDAR"
    ]
    return "\n".join(event)


def read_caldav_events(calendar):
    """
    This is problematic without a date range, will not get all the results!
    :param calendar:
    :return:
    """
    try:
        events = calendar.events()
        return events
    except Exception as e:
        print(f"Error reading events: {e}")


def read_caldav_events_range(calendar, start_date, end_date):
    """
    Reads events from a specific calendar within the given date range.

    :param calendar: The CalDAV calendar object
    :param start_date: The start date for fetching events
    :param end_date: The end date for fetching events
    :return: A list of CalDAV event objects
    """
    try:
        return calendar.date_search(start=start_date, end=end_date)
    except Exception as e:
        print(f"Error reading events: {e}")
        return []


def get_calendar_event_by_name(calendar, event_name):
    """
    Retrieves a calendar event by its name (summary) without limiting the date range.
    
    This is problematic without a date range, will not get all the results!

    :param calendar: The CalDAV calendar object
    :param event_name: The name (summary) of the event to retrieve
    :return: The first matching CalDAV event object or None if not found
    """
    try:
        # Fetch all events from the calendar
        events = read_caldav_events(calendar)
        for event in events:
            if event.instance.vevent.summary.value == event_name:
                return event
        return None  # Event not found
    except Exception as e:
        print(f"Error occurred while searching for the event: {e}")
        return None


def get_calendar_event_by_name_range(calendar, event_name, start_date, end_date):
    """
    Retrieves a calendar event by its name (summary) within the given date range.

    :param calendar: The CalDAV calendar object
    :param event_name: The name (summary) of the event to retrieve
    :param start_date: The start date for fetching events
    :param end_date: The end date for fetching events
    :return: The first matching CalDAV event object or None if not found
    """
    try:
        events = read_caldav_events_range(calendar, start_date, end_date)
        for event in events:
            if event.instance.vevent.summary.value == event_name:
                return event
        return None  # Event not found
    except Exception as e:
        print(f"Error occurred while searching for the event: {e}")
        return None


def create_caldav_event(calendar, event_data):
    try:
        calendar.save_event(event_data)
    except Exception as e:
        print(f"Error creating event: {e}")


def delete_caldav_event(calendar, event_uid, start_date, end_date):
    """
    Deletes an event from a CalDAV calendar based on its UID.

    :param calendar: The calendar from which to delete the event
    :param event_uid: The unique identifier of the event to be deleted
    :return: True if the event was deleted successfully, False otherwise
    """
    try:
        events = read_caldav_events_range(calendar, start_date, end_date)
        for event in events:
            if event.instance.vevent.uid.value == event_uid:
                event.delete()
                return True
        return False  # Event not found
    except Exception as e:
        print(f"Error deleting the event: {e}")
        return False


