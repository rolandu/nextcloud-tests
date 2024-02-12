import pytest

from config import config
from dav_functions.carddav import *


# constants
test_contact_name = "John Doe"
test_contact_name_that_does_not_exist = "ASDFASDFSADFASDFASDFASDFASDFASDF"
test_contact_email = "johndoe@example.com"
test_contact_updated_note = "Updated vcard with .new email."
test_contact_updated_email = "johndoe@example.net"
contact_info = {
    "fullname": test_contact_name,
    "email": test_contact_email
}


def get_test_contact():
    return fetch_carddav_contact(
        config.carddav_url,
        config.username,
        config.password,
        test_contact_name)


def test_carddav_create_and_read():
    # Create a contact
    assert create_carddav_contact(
        config.carddav_url,
        config.username,
        config.password,
        contact_info), "Failed to create contact"
    
    # Confirm contact can now be found
    retrieved_contact = get_test_contact()
    
    assert retrieved_contact is not None, "Contact not found after creation"
    assert retrieved_contact != ""


def test_carddav_read():
    # Fetch contact
    retrieved_contact = get_test_contact()
    
    assert retrieved_contact is not None, "Contact not found after creation"
    assert retrieved_contact != ""
    
    print("Retrieved contact:" + str(retrieved_contact))
    print("Serialized vcard: " + str(retrieved_contact['vcard'].serialize()))
    
    # Negative test, this should throw an error
    with pytest.raises(Exception) as excinfo:
        fetch_carddav_contact(
            config.carddav_url,
            config.username,
            config.password,
            test_contact_name_that_does_not_exist)
    assert excinfo.value.args[0] == "Contact not found"
    

def test_carddav_update():
    # Fetch contact
    to_be_updated = get_test_contact()
    assert to_be_updated is not None, "Contact not found"
    assert to_be_updated != ""
    
    vcard = vobject.readOne(to_be_updated['vcard'].serialize())
    
    # updating the card
    vcard.add('note')
    vcard.note.value = test_contact_updated_note
    vcard.email.value = test_contact_updated_email
    
    assert update_carddav_contact(
        config.carddav_url,
        config.username,
        config.password,
        vcard,
        to_be_updated['href']
    )


def test_carddav_delete():
    # Fetch contact
    to_be_deleted = get_test_contact()
    
    assert to_be_deleted is not None, "Contact not found"
    assert to_be_deleted != ""

    # Delete the contact
    assert delete_carddav_contact(
        config.carddav_url,
        config.username,
        config.password,
        to_be_deleted['href']), "Failed to delete contact"

    # Confirm the contact is not there anymore
    with pytest.raises(Exception) as excinfo:
        get_test_contact()
    assert excinfo.value.args[0] == "Contact not found"
