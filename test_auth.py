import urllib.request
import json
import urllib.error

BASE_URL = "http://localhost:8000"

def test_auth():
    print("Testing Registration...")
    reg_data = {
        "name": "Test User",
        "email": "testauth@example.com",
        "password": "Password123!",
        "phone": "9998887776",
        "country": "India"
    }
    
    req1 = urllib.request.Request(
        f"{BASE_URL}/api/auth/register",
        data=json.dumps(reg_data).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req1) as response:
            print(f"Register Status: {response.status}")
            print(f"Register Response: {response.read().decode('utf-8')}")
    except urllib.error.HTTPError as e:
        print(f"Register Failed with Status: {e.code}")
        print(f"Register Error Response: {e.read().decode('utf-8')}")


    print("\nTesting Login...")
    login_data = {
        "identifier": "testauth@example.com",
        "password": "Password123!"
    }
    
    req2 = urllib.request.Request(
        f"{BASE_URL}/api/auth/login",
        data=json.dumps(login_data).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req2) as response:
            print(f"Login Status: {response.status}")
            print(f"Login Response: {response.read().decode('utf-8')}")
    except urllib.error.HTTPError as e:
        print(f"Login Failed with Status: {e.code}")
        print(f"Login Error Response: {e.read().decode('utf-8')}")

if __name__ == "__main__":
    test_auth()
