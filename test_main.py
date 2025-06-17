"""
This module contains tests for the FastAPI application defined in main.py.
"""
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_balance():
    """
    Test retrieving the balance for an existing account and handling a non-existent account.
    """
    response = client.get("/accounts/123/balance")
    assert response.status_code == 200
    assert "balance" in response.json()

    response = client.get("/accounts/999/balance")
    assert response.status_code == 404

def test_deposit():
    """
    Test depositing a valid amount and handling invalid (negative) deposit amounts.
    """
    response = client.post("/accounts/123/deposit", json={"amount": 100})
    assert response.status_code == 200

    response = client.post("/accounts/123/deposit", json={"amount": -50})
    assert response.status_code == 400

def test_withdraw():
    """
    Test withdrawing a valid amount, overdraw attempts, and invalid (negative) withdrawal amounts.
    """
    response = client.post("/accounts/456/withdraw", json={"amount": 100})
    assert response.status_code == 200

    response = client.post("/accounts/456/withdraw", json={"amount": 10000})
    assert response.status_code == 400

    response = client.post("/accounts/456/withdraw", json={"amount": -10})
    assert response.status_code == 400


def test_create_account():
    """
    Test creating a new account and handling duplicate account creation.
    """
    # Create a new account
    response = client.post("/accounts/", json={"account_number": "789", "initial_balance": 200})
    assert response.status_code == 200
    assert response.json()["message"] == "Account created"

    # Try to create the same account again
    response = client.post("/accounts/", json={"account_number": "789", "initial_balance": 100})
    assert response.status_code == 400

def test_delete_account():
    """
    Test deleting an existing account and handling deletion of a non-existent account.
    """
    # Delete an existing account
    response = client.delete("/accounts/789")
    assert response.status_code == 200
    assert response.json()["message"] == "Account deleted"

    # Try to delete again
    response = client.delete("/accounts/789")
    assert response.status_code == 404

def test_history():
    """
    Test that transaction history is recorded and includes deposit and withdrawal entries.
    """
    # Deposit and withdraw to generate history
    client.post("/accounts/123/deposit", json={"amount": 10})
    client.post("/accounts/123/withdraw", json={"amount": 5})
    response = client.get("/accounts/123/history")
    assert response.status_code == 200

    history = response.json()["history"]
    assert isinstance(history, list)
    assert any(item["type"] == "deposit" for item in history)
    assert any(item["type"] == "withdraw" for item in history)
