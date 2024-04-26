import requests
import pytest

# Test health endpoint
def test_health_endpoint():
    # Assuming the health endpoint URL of your Streamlit app
    health_endpoint_url = "http://streamlit:8501/health"  # Update with your actual health endpoint URL
    
    # Make a request to the health endpoint
    response = requests.get(health_endpoint_url)
    
    # Assert that the response status code is 200
    assert response.status_code == 200
