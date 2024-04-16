import pytest
from garden_database import find_garden, search_for_garden_name, sort_garden
from class_Garden import Garden

@pytest.fixture
def sample_garden_data():
    return [
        {"garden_id": "1", "name": "Rose Garden", "date" : "2022-01-01", "garden": ["00001","00002","00003"],},
        {"garden_id": "2", "name": "Vegetable Garden", "date" : "2022-03-15", "garden": ["00001","00002"],},
        {"garden_id": "3", "name": "Herb Garden", "date": "2022-02-10", "garden": ["00001","00002"],}
    ]

def test_find_garden_found(sample_garden_data):
    garden_id = "1"
    garden = find_garden(sample_garden_data, garden_id)
    assert isinstance(garden, Garden)
    assert garden.name == "Rose Garden"

def test_find_garden_not_found(sample_garden_data):
    garden_id = "4"
    garden = find_garden(sample_garden_data, garden_id)
    assert garden is None
    
def test_search_for_garden_name_found(sample_garden_data):
    name = "rose"
    gardens = search_for_garden_name(sample_garden_data, name)
    assert isinstance(gardens, list)
    assert len(gardens) == 1
    assert gardens[0]["name"] == "Rose Garden"

def test_search_for_garden_name_not_found(sample_garden_data):
    name = "orchid"
    gardens = search_for_garden_name(sample_garden_data, name)
    assert gardens is False
    
def test_sort_garden_by_date(sample_garden_data):
    sorted_gardens = sort_garden(sample_garden_data, "date")
    assert len(sorted_gardens) == 3
    assert sorted_gardens[0]["name"] == "Rose Garden"
    assert sorted_gardens[1]["name"] == "Herb Garden"
    assert sorted_gardens[2]["name"] == "Vegetable Garden"

def test_sort_garden_by_name(sample_garden_data):
    sorted_gardens = sort_garden(sample_garden_data, "name")
    assert len(sorted_gardens) == 3
    assert sorted_gardens[0]["name"] == "Herb Garden"
    assert sorted_gardens[1]["name"] == "Rose Garden"
    assert sorted_gardens[2]["name"] == "Vegetable Garden"
    