import urllib.request
import json
import urllib.error

BASE_URL = "http://localhost:8000/api"

def print_result(name, success, info=""):
    status = "PASS" if success else "FAIL"
    print(f"[{status}] {name} {info}")

def run_tests():
    print("=== Snacko API Automation Test Suite ===\n")
    
    # 1. Login Customer
    token = None
    try:
        req = urllib.request.Request(
            f"{BASE_URL}/auth/login",
            data=json.dumps({"identifier": "ishantmishra050@gmail.com", "password": "password123"}).encode(),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req) as res:
            data = json.loads(res.read().decode())
            token = data.get("access_token")
            print_result("Customer Login", True)
    except Exception as e:
        print_result("Customer Login", False, str(e))
        return

    auth_headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    # 2. Get Profile
    user_id = None
    try:
        req = urllib.request.Request(f"{BASE_URL}/auth/me", headers=auth_headers)
        with urllib.request.urlopen(req) as res:
            data = json.loads(res.read().decode())
            user_id = data.get("id")
            print_result("Get Profile (/me)", True, f"Found User: {data.get('email')}")
    except Exception as e:
        print_result("Get Profile (/me)", False, str(e))

    # 3. Add Address
    address_id = None
    try:
        addr_data = {
            "full_name": "Test Tester", "mobile": "9998887776", "pincode": "400001",
            "flat_building": "100", "area_street": "Test Street", "city": "Mumbai", "state": "Maharashtra"
        }
        req = urllib.request.Request(f"{BASE_URL}/users/me/addresses", data=json.dumps(addr_data).encode(), headers=auth_headers)
        with urllib.request.urlopen(req) as res:
            data = json.loads(res.read().decode())
            address_id = data.get("id")
            print_result("Create Address", True, f"Address ID: {address_id}")
    except Exception as e:
        print_result("Create Address", False, str(e))

    # 4. Fetch Stores
    store_id = None
    try:
        req = urllib.request.Request(f"{BASE_URL}/stores/", headers=auth_headers)
        with urllib.request.urlopen(req) as res:
            data = json.loads(res.read().decode())
            if len(data) > 0:
                store_id = data[0].get("id")
                print_result("Fetch Stores", True, f"Found {len(data)} stores. Selected Store ID: {store_id}")
            else:
                print_result("Fetch Stores", False, "No stores configured in DB.")
    except Exception as e:
        print_result("Fetch Stores", False, str(e))

    # 5. Fetch Store Products
    store_product_id = None
    if store_id:
        try:
            req = urllib.request.Request(f"{BASE_URL}/products/store/{store_id}", headers=auth_headers)
            with urllib.request.urlopen(req) as res:
                data = json.loads(res.read().decode())
                if len(data) > 0:
                    store_product_id = data[0].get("id")
                    print_result("Fetch Store Products", True, f"Found {len(data)} products. Selected Product ID: {store_product_id}")
                else:
                    print_result("Fetch Store Products", False, "No products for store.")
        except Exception as e:
            print_result("Fetch Store Products", False, str(e))

    # 6. Place Order
    order_id = None
    if store_id and store_product_id and address_id:
        try:
            order_data = {
                "store_id": store_id,
                "address_id": address_id,
                "payment_method": "cod",
                "items": [{"store_product_id": store_product_id, "quantity": 2}]
            }
            req = urllib.request.Request(f"{BASE_URL}/orders/", data=json.dumps(order_data).encode(), headers=auth_headers)
            with urllib.request.urlopen(req) as res:
                data = json.loads(res.read().decode())
                order_id = data.get("id")
                print_result("Create Order", True, f"Order ID: {order_id}, Total: {data.get('total_amount')}")
        except urllib.error.HTTPError as e:
            print_result("Create Order", False, f"HTTP {e.code}: {e.read().decode()}")
        except Exception as e:
            print_result("Create Order", False, str(e))

    # 7. View Orders
    try:
        req = urllib.request.Request(f"{BASE_URL}/orders/", headers=auth_headers)
        with urllib.request.urlopen(req) as res:
            data = json.loads(res.read().decode())
            print_result("Fetch My Orders", True, f"Found {len(data)} orders.")
    except Exception as e:
        print_result("Fetch My Orders", False, str(e))

    print("\n=== Testing Store Owner (Chitale) ===\n")
    store_token = None
    try:
        req = urllib.request.Request(
            f"{BASE_URL}/auth/login",
            data=json.dumps({"identifier": "chitale@example.com", "password": "store123"}).encode(),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req) as res:
            data = json.loads(res.read().decode())
            store_token = data.get("access_token")
            print_result("Store Owner Login", True)
    except urllib.error.HTTPError as e:
        print_result("Store Owner Login", False, f"HTTP {e.code}: {e.read().decode()}")
    
    if store_token:
        store_headers = {"Authorization": f"Bearer {store_token}", "Content-Type": "application/json"}
        try:
            req = urllib.request.Request(f"{BASE_URL}/orders/admin/all", headers=store_headers)
            with urllib.request.urlopen(req) as res:
                data = json.loads(res.read().decode())
                print_result("Fetch Store Orders (Admin)", True, f"Found {len(data)} orders to fulfill.")
        except urllib.error.HTTPError as e:
            print_result("Fetch Store Orders", False, f"HTTP {e.code}: {e.read().decode()}")

    print("\n🏁 Full API Automation Check Complete.")

if __name__ == "__main__":
    run_tests()
