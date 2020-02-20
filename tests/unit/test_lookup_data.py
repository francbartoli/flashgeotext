import pytest
from pydantic import ValidationError

from flashgeotext.lookup import load_data_from_file
from flashgeotext.lookup import LookupData
from flashgeotext.settings import DEMODATA_CITIES
from flashgeotext.settings import DEMODATA_COUNTRIES


def test_lookup_data(test_data_cities):
    lookup = LookupData(name="cities", data=test_data_cities)

    assert lookup.name == "cities"
    assert isinstance(lookup.data, dict)


@pytest.mark.parametrize(
    "id, name, data, expectation",
    [
        (1, "cities", ["Berlin", "Hamburg"], pytest.raises(ValidationError)),
        (2, "cities", ("Berlin", "Hamburg"), pytest.raises(ValidationError)),
        (3, "cities", "Berlin", pytest.raises(ValidationError)),
        (4, "cities", 1337, pytest.raises(ValidationError)),
        (5, 1337, {"Berlin": ["Berlin"]}, pytest.raises(ValidationError)),
        (6, [13, 37], {"Berlin": ["Berlin"]}, pytest.raises(ValidationError)),
        (7, (13, 37), {"Berlin": ["Berlin"]}, pytest.raises(ValidationError)),
        (8, {"13": 37}, {"Berlin": ["Berlin"]}, pytest.raises(ValidationError)),
    ],
)
def test_lookup_data_raises(id, name, data, expectation):

    with expectation:
        lookup = LookupData(name=name, data=data)

        assert isinstance(lookup, LookupData)


@pytest.mark.parametrize(
    "id, name, data, error_count",
    [
        (1, "cities", {"Berlin": "Berlin"}, 1),
        (2, "cities", {"Berlin": ["Dickes B"]}, 1),
        (2, "cities", {"Berlin": "Hamburg"}, 2),
    ],
)
def test_lookup_data_validate(id, name, data, error_count):
    lookup = LookupData(name=name, data=data)

    validation = lookup.validate()

    assert validation.error_count == error_count


@pytest.mark.parametrize(
    "id, name, demodata",
    [(1, "cities", DEMODATA_CITIES), (2, "countries", DEMODATA_COUNTRIES)],
)
def test_lookup_data_demo_data(id, name, demodata):
    lookup = LookupData(name=name, data=load_data_from_file(demodata))

    validation = lookup.validate()

    assert validation.error_count == 0
