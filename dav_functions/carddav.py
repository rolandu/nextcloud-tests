import requests
import vobject
import uuid
from xml.etree import ElementTree as ET


# relevant docs:
# https://eventable.github.io/vobject/
# https://sabre.io/xml/

def create_carddav_contact(carddav_url, username, password, contact_info):
    """
    Creates a new contact in the CardDAV server.

    :param carddav_url: URL to the CardDAV server address book
    :param username: Username for authentication
    :param password: Password for authentication
    :param contact_info: Dictionary with contact information (e.g., name, email)
    :return: True if contact is created successfully, False otherwise
    """
    # Create a vCard
    card = vobject.vCard()
    card.add('fn').value = contact_info.get('fullname', 'Unknown')
    card.add('email').value = contact_info.get('email', '')
    
    contact_filename = f"{uuid.uuid4()}.vcf"

    # Serialize to string
    card_string = card.serialize()
    print("Serialized vCard:", card_string)  # Debug print
    
    try:
        response = requests.put(
            f"{carddav_url}/{contact_filename}",
            data=card_string,
            auth=(username, password),
            headers={
                'content-type': 'text/vcard'
            }
        )
        response.raise_for_status()
        return True
    except requests.HTTPError as e:
        print(f"HTTP Error: {e}")
        print("Response content:", response.content.decode())
        return False
    except Exception as e:
        print(f"Error creating contact: {e}")
        return False


def update_carddav_contact(
        carddav_url: str,
        username: str,
        password: str,
        card: vobject,
        href: str):
    """
    Updates a contact in the CardDAV server.

    :param carddav_url: URL to the CardDAV server address book
    :param username: Username for authentication
    :param password: Password for authentication
    :param card: a vobject.vCard containing updated information
    :param href: the current path or only the filename including extension, e.g. <uuid>.vcf
    :return: True if contact is created successfully, False otherwise
    """
    contact_filename = href.split("/")[-1]
    
    # Serialize to string
    card_string = card.serialize()
    print("Serialized vCard:", card_string)  # Debug print
    
    try:
        response = requests.put(
            f"{carddav_url}/{contact_filename}",
            data=card_string,
            auth=(username, password),
            headers={
                'content-type': 'text/vcard'
            }
        )
        response.raise_for_status()
        return True
    except requests.HTTPError as e:
        print(f"HTTP Error: {e}")
        print("Response content:", response.content.decode())
        return False
    except Exception as e:
        print(f"Error creating contact: {e}")
        return False


def fetch_carddav_contacts(carddav_url, username, password):
    """
    Fetches contacts from the CardDAV server using PROPFIND.

    :param carddav_url: URL to the CardDAV server address book
    :param username: Username for authentication
    :param password: Password for authentication
    :return: list of dictionary of {fn, href, vcard}
    """
    # Define the headers
    headers = {
        "content-type": "application/xml",
        "depth": "1"
    }

    # Define the body for the PROPFIND request
    report_request_body = """
    <card:addressbook-query xmlns:d="DAV:" xmlns:card="urn:ietf:params:xml:ns:carddav">
        <d:prop>
            <d:getetag />
            <d:displayname />
            <card:address-data />
        </d:prop>
    </card:addressbook-query>
    """

    try:
        response = requests.request(
            method="REPORT",
            url=carddav_url + "/",
            auth=(username, password),
            data=report_request_body,
            headers=headers
        )
        response.raise_for_status()

        # Parse the XML response if needed
        tree = ET.fromstring(response.content)
        contacts = []
        for response_element in tree.findall('.//{DAV:}response'):
            href = response_element.find('{DAV:}href').text
            address_data_element = response_element.find('.//{urn:ietf:params:xml:ns:carddav}address-data')
            if address_data_element is not None:
                vcard = vobject.readOne(address_data_element.text)
                fn = vcard.fn.value if hasattr(vcard, 'fn') else "Unknown"
                contacts.append({
                    "fn": fn,
                    "href": href,
                    "vcard": vcard})
        return contacts

    except Exception as e:
        print(f"Error fetching contacts: {e}")
        return None


def fetch_carddav_contact(
        carddav_url: str,
        username: str,
        password: str,
        fn: str):
    """
    Fetches a single contact from the CardDAV server using PROPFIND.

    :param carddav_url: URL to the CardDAV server address book
    :param username: Username for authentication
    :param password: Password for authentication
    :param fn: full name of the contact
    :return: dictionary of {fn, href, vcard}
    """
    # Fetch contacts
    contacts = fetch_carddav_contacts(
        carddav_url,
        username,
        password)
    if contacts is None:
        raise Exception("No contacts found")
    
    retrieved_contact = ""
    for contact in contacts:
        if contact["fn"] == fn:
            retrieved_contact = contact
    
    if retrieved_contact == "":
        raise Exception("Contact not found")
    
    return retrieved_contact


def delete_carddav_contact(
        carddav_url: str,
        username: str,
        password: str,
        href: str):
    """
    Deletes a contact from the CardDAV server.

    :param carddav_url: URL to the CardDAV server address book
    :param username: Username for authentication
    :param password: Password for authentication
    :param href: the current path or only the filename including extension, e.g. <uuid>.vcf
    :return: True if contact is deleted successfully, False otherwise
    """
    contact_filename = href.split("/")[-1]

    try:
        response = requests.delete(
            f"{carddav_url}/{contact_filename}",
            auth=(username, password)
        )
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"Error deleting contact: {e}")
        return False

