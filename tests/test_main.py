from fastapi.testclient import TestClient
from app.main import app
from app import data_handler
import pandas as pd
import pytest
import uuid

# Instantiate the TestClient with the FastAPI app
client = TestClient(app)

@pytest.fixture
def mock_customer_df(monkeypatch):
    """Fixture to mock the global customer_df for endpoint tests."""
    num_users = 3  # Number of mock users
    test_data = {
        'id': [str(uuid.uuid4()) for _ in range(num_users)],  # Generate unique UUIDs
        'name': ['Alice', 'Bob', 'Charlie'],
        'email': ['a@test.com', 'b@test.com', 'c@test.com'],
        'createddate': pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03']),
        'isactive': [True, False, True], 'countrycode': ['US', 'DE', 'CA']
    }
    mock_df = pd.DataFrame(test_data)
    monkeypatch.setattr(data_handler, 'customer_df', mock_df)
    return mock_df

# --- Tests for the /api/countries endpoint ---

def test_read_countries_endpoint(mock_customer_df):
    """Test the GET /api/countries endpoint."""
    response = client.get("/api/countries")
    assert response.status_code == 200
    assert response.json() == ['CA', 'DE', 'US']

# --- Tests for the /api/customers endpoint ---

def test_read_customers_endpoint_no_params(mock_customer_df):
    """Test the GET /api/customers endpoint with default parameters."""
    response = client.get("/api/customers")
    assert response.status_code == 200
    data = response.json()
    assert data['total_count'] == 3
    assert len(data['customers']) == 3 # Default sort is by date desc
    assert data['customers'][0]['name'] == 'Charlie'

def test_read_customers_endpoint_with_query_params(mock_customer_df):
    """Test the GET /api/customers endpoint with a filter."""
    response = client.get("/api/customers?isActive=false")
    assert response.status_code == 200
    data = response.json()
    assert data['total_count'] == 1
    assert data['customers'][0]['name'] == 'Bob'

def test_read_customers_endpoint_invalid_param(mock_customer_df):
    """Test that FastAPI's validation catches invalid parameters."""
    # `page` must be greater than or equal to 1.
    response = client.get("/api/customers?page=0")
    # 422 Unprocessable Entity is the correct response for validation errors.
    assert response.status_code == 422