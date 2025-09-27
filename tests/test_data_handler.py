import pytest
import pandas as pd
from app import data_handler
import uuid

# Fixture to mock the customer DataFrame
@pytest.fixture
def mock_customer_df(monkeypatch):
    """Fixture to mock the global customer_df in data_handler."""
    # 1. Create a controlled test data
    num_users = 3  # Number of mock users
    test_data = {
        'id': [str(uuid.uuid4()) for _ in range(num_users)],  # Generate unique UUIDs
        'name': ['Alice Smith', 'Bob Johnson', 'Charlie Brown'],
        'email': ['alice@test.com', 'bob@test.com', 'charlie@test.com'],
        'createddate': pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03']),
        'isactive': [True, False, True],
        'countrycode': ['US', 'DE', 'CA']
    }
    mock_df = pd.DataFrame(test_data)
    
    # 2. Use monkeypatch to replace the real df with our mock df
    monkeypatch.setattr(data_handler, 'customer_df', mock_df)
    return mock_df

# --- Tests for get_all_countries ---

def test_get_all_countries(mock_customer_df):
    """
    GIVEN a mocked DataFrame with three unique countries
    WHEN the get_all_countries function is called
    THEN it should return a sorted list of those unique country codes.
    """
    result = data_handler.get_all_countries()
    assert result == ['CA', 'DE', 'US']

# --- Tests for get_customers ---

def test_get_customers_no_filters(mock_customer_df):
    """
    GIVEN mocked data
    WHEN get_customers is called with no filters (just pagination)
    THEN it should return the correct paginated response.
    """
    response = data_handler.get_customers(page=1, page_size=2)
    assert response.total_count == 3
    assert len(response.customers) == 2
    assert response.customers[0].name == 'Alice Smith'

def test_get_customers_search_filter(mock_customer_df):
    """Test searching by name."""
    response = data_handler.get_customers(page=1, page_size=10, search='Bob')
    assert response.total_count == 1
    assert len(response.customers) == 1
    assert response.customers[0].name == 'Bob Johnson'

def test_get_customers_is_active_filter(mock_customer_df):
    """Test filtering by inactive status."""
    response = data_handler.get_customers(page=1, page_size=10, is_active=False)
    assert response.total_count == 1
    assert response.customers[0].name == 'Bob Johnson'

def test_get_customers_country_filter(mock_customer_df):
    """Test filtering by country code."""
    response = data_handler.get_customers(page=1, page_size=10, country_code='CA')
    assert response.total_count == 1
    assert response.customers[0].name == 'Charlie Brown'

def test_get_customers_sorting(mock_customer_df):
    """Test sorting by name in descending order."""
    response = data_handler.get_customers(page=1, page_size=10, sort_by='name', sort_direction='desc')
    assert response.total_count == 3
    assert response.customers[0].name == 'Charlie Brown'

def test_get_customers_pagination(mock_customer_df):
    """Test fetching the second page."""
    response = data_handler.get_customers(page=2, page_size=2)
    assert response.total_count == 3
    assert len(response.customers) == 1
    assert response.customers[0].name == 'Charlie Brown'