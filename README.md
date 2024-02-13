# nextcloud-tests

This is a simple Python script to test webdav, caldav and carddav on Nextcloud (might also work with out dav servers).

The tests typically upload, read and delete data, not leaving behind any traces in the end. 
The tests are not independent of one another (cannot read something if it hasn't been uploaded). 
That's not best practice for testing in general, but makes sense in this situation.

## Purpose

For me and many others, Nextcloud is a central part of our daily workflow and we need it to work properly.

Several times in the past, I had sync issues after upgrading Nextcloud to a new version. 
I started to operate a second instance of Nextcloud for testing purposes. 
I would first try to upgrade the test instance before upgrading my main instance.
(Basically that's best practice in any case.)

However, after upgrading the test instance, how do I verify if everything works properly? 
I used to try all functions manually, which was a lot of work and not always free of errors.

So I decided to create a small collection of tests to verify my Nextcloud instance's sync functions work properly.

## Limitations

This only tests the sync functions via webdav/caldav/carddav. 
It does not test the web-based user interface or other functionalities.
You will need to test other things manually or using other scripts.

## Prerequisites

### Required software

- Nextcloud (Version >20)
- Python 3.8.5 (or compatible)
- Python packages according to requirements.txt
- pyenv + virtualenv (optional, recommended)

### pyenv + virtualenv (optional)

You only need to do these steps if you wish to use pyenv + virtualenv and have those packages installed.

Navigate to the directory of the tool and run:

```commandline
pyenv install
pyenv virtualenv nextcloud-tests
pyenv activate 
```

Then continue with installing requirements.

### Install python requirements

```commandline
pip install -r requirements.txt
```

### Upload testfile to your Nextcloud

The tests also include testing a static test file that is supposed to already be there before the tests start. Please 
manually upload `test_data/test-textfile.txt` to your Nextcloud test user's base directory.

*Why does this test exist? I had some trouble with the encryption module at some point which made files unreadable after
an upgrade, so I wanted to verify if existing data remained readable after an upgrade. 
This file is supposed to always stay in the test user's directory so we can check if it remains readable after the upgrade.*

### Configuration

Copy the `config/config.sample.py` to `config/config.py`:

```commandline
cp config/config.sample.py config/config.py
```

and fill out the `config.py` according to your environment (i.e. Nextcloud path / username / password).

## Usage

### Run all tests

Just run pytest in console to run all tests and get a report:

`pytest`

By default, this will only show you failed tests. The `-v` option gives more verbose output:

`pytest -v` 

### Run only certain tests

```
pytest test_webdav.py  # runs certain tests by file (recommended)

pytest -k <test name>  # runs a certain test by function name; warning: some tests depend on one another
pytest -k "test_webdav_get_static_file"  # example
```

## Alternative way to run: Docker

If you don't want to deal with Python/Pyenv/Packages and/or are more familiar with Docker, you can use the included 
Docker specs to run the tests.

```commandline
docker-compose up --build   # build the package, install all dependencies and run the tests
```

In the `docker-compose.yml` you can modify the `pytest` command to be executed if needed.

You will still need to create and fill out the `config/config.py` as described above.

## Nextcloud bugs

### Carddav

In approximately Version 20 of Nextcloud (I am not sure exactly), 
I was not able to get all Carddav functions to work properly. 
The issue was resolved by Version 24 (maybe earlier).

This was not an issue in production, as Thunderbird's sync features worked well, 
but looking at their carddav implementation theirs was much more complex than what I am using here.

I read that bugs existed in those functions and ignored these tests for a while.

In conclusion, if you get carddav errors in NC20, you can *maybe* ignore those.

### Exclude some tests permanently

In case there are known bugs, you can exclude some tests by putting this in front of the respective function:

`@pytest.mark.skip(reason="bug in Nextcloud, needs to be resolved first")
`
