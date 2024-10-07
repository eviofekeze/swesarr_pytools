import datetime

import pytest
from resources import expected_data
from swesarr_pytools.access_swesarr import AccessSAR


@pytest.fixture
def access_swesarr():
    return AccessSAR()


def test_retrieve_meta(access_swesarr):
    assert access_swesarr.data_meta == expected_data.EXPECTED_META
    assert access_swesarr.flight_names == expected_data.EXPECTED_FOLDER_NAMES
    assert access_swesarr.flight_dates == expected_data.EXPECTED_FOLDER_DATES


def test_validate_date(access_swesarr):
    expected_date = datetime.date(year=1995, month=10, day=5)
    assert access_swesarr.validate_date(some_date="10/5/95", date_name="This Date") == expected_date
    assert access_swesarr.validate_date(some_date="10/5/1995", date_name="This Date") == expected_date
    assert access_swesarr.validate_date(
        some_date=datetime.date(year=1995, month=10, day=5), date_name="This Date") == expected_date


def test_available_date_within_range(access_swesarr):
    retrieved_dates = access_swesarr.available_date_within_range(start_date=datetime.date(year=2019, month=1, day=1),
                                                                 end_date=datetime.date(year=2019, month=12, day=31))
    assert retrieved_dates == expected_data.EXPECTED_DATES_RANGE

    retrieved_empty_dates = access_swesarr.available_date_within_range(
        start_date=datetime.date(year=2018, month=1, day=1),
        end_date=datetime.date(year=2018, month=12, day=31)
    )
    assert retrieved_empty_dates is None
