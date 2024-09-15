import requests
import json
import time

API_URL = "http://127.0.0.1:5000"

def test_post_data():
    data = {
        "Roll": 0.93,
        "Pitch": -0.04,
        "Yaw": 0.18,
        "Accel/Time": [1, 2, 2323, 443, 212, 2323, 0, 0, 0],
        "Roll/Time": [9, 2, 22, 222, 121, 213],
        "Punch": 1,
        "Fastest Punch": 112,
        "Average punch / min": 8.2
    }
    
    response = requests.post(f"{API_URL}/sensor_data", json=data)
    print("POST Response:", response.status_code, response.json())
    assert response.status_code == 201, f"Expected status code 201, but got {response.status_code}"

def test_get_data():
    response = requests.get(f"{API_URL}/sensor_data")
    print("GET Response:", response.status_code, response.json())
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    
    data = response.json()
    assert "Roll" in data, "Roll data is missing"
    assert "Pitch" in data, "Pitch data is missing"
    assert "Yaw" in data, "Yaw data is missing"
    assert "Accel/Time" in data, "Accel/Time data is missing"
    assert "Roll/Time" in data, "Roll/Time data is missing"
    assert "Punch" in data, "Punch data is missing"
    assert "Fastest Punch" in data, "Fastest Punch data is missing"
    assert "Average punch / min" in data, "Average punch / min data is missing"

if __name__ == "__main__":
    print("Testing POST request...")
    test_post_data()
    
    print("\nWaiting 2 seconds...")
    time.sleep(2)
    
    print("\nTesting GET request...")
    test_get_data()
    
    print("\nAll tests passed successfully!")