from fastapi.testclient import TestClient
from main import app, accounts

client = TestClient(app)

def test_get_balance():
    response = client.get("/accounts/123/balance")
    assert response.status_code == 200
    assert response.json() == {"account_number": "123", "balance": accounts["123"]}
    response = client.get("/accounts/999/balance")
    assert response.status_code == 404

def test_deposit():
    response = client.post("/accounts/123/deposit", json={"amount": 100})
    assert response.status_code == 200
    assert response.json()["balance"] == accounts["123"]
    response = client.post("/accounts/123/deposit", json={"amount": -50})
    assert response.status_code == 400

def test_withdraw():
    response = client.post("/accounts/456/withdraw", json={"amount": 100})
    assert response.status_code == 200
    assert response.json()["balance"] == accounts["456"]
    response = client.post("/accounts/456/withdraw", json={"amount": 10000})
    assert response.status_code == 400
    response = client.post("/accounts/456/withdraw", json={"amount": -10})
    assert response.status_code == 400

    
# Run tests if this file is executed directly
if __name__ == "__main__":
    test_get_balance()
    test_deposit()
    test_withdraw()
    print("All tests passed.")