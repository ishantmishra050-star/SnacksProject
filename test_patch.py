import urllib.request
import json
import urllib.error

BASE_URL = "http://localhost:8000/api"

def test():
    # Login as Chitale
    req = urllib.request.Request(
        f"{BASE_URL}/auth/login",
        data=json.dumps({"identifier": "chitale@example.com", "password": "store123"}).encode(),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as res:
        token = json.loads(res.read().decode())["access_token"]
    
    # Try updating order status
    try:
        req = urllib.request.Request(
            f"{BASE_URL}/admin/orders/1/status",
            data=json.dumps({"status": "confirmed"}).encode(),
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"},
            method="PATCH"
        )
        with urllib.request.urlopen(req) as res:
            print("Status:", res.status)
            print("Response:", res.read().decode())
    except urllib.error.HTTPError as e:
        print("HTTP Error:", e.code)
        print("Response:", e.read().decode())
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    test()
