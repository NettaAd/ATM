# ATM System API

## Overview

This project is a simple server-side ATM system built with **FastAPI** in Python.  
It allows users to:
- Retrieve account balance
- Deposit money
- Withdraw money
- (Enrichment) Create and delete accounts
- (Enrichment) View transaction history with timestamps

All data is stored in-memory.

**Live Demo:**  
- Root URL: [https://netta-atm.azurewebsites.net](https://netta-atm.azurewebsites.net)
- API Docs: [https://netta-atm.azurewebsites.net/docs](https://netta-atm.azurewebsites.net/docs)  

**How to Use the Docs:**
The `/docs` endpoint provides an interactive UI (powered by **Swagger UI**) where you can explore and test the API directly from your browser.

1. **Navigate to `/docs`**  
   Open [https://netta-atm.azurewebsites.net/docs](https://netta-atm.azurewebsites.net/docs)

2. **Expand any endpoint**  
   Click on a method like `POST /accounts/{account_number}/deposit` to view required input and example schemas.

3. **Try it out**  
   Click the "Try it out" button, fill in parameters (like `account_number` and request body), then click **Execute**.

4. **View the response**  
   You’ll see the full HTTP response including the response code, headers, and JSON body.

**Deployment:**  
This project is deployed using **Azure App Service for Linux**, which allows you to host web apps using a fully managed platform-as-a-service (PaaS) model.

- Deployment is done directly via Git using Azure's deployment center.
- The service runs a Linux container that supports Python and FastAPI.
- Logs and startup messages can be viewed via Kudu or the Azure Portal.

**Why Azure App Service?**

- **Free Tier Available:** Ideal for small projects and demos like this.
- **Easy Git Integration:** Push code to a branch and it auto-deploys.
- **Built-in Monitoring & Logs:** Easy debugging with streaming logs and SSH access.
- **Supports FastAPI out of the box:** Python apps run seamlessly on the Linux-based App Service.

---

## Why FastAPI and Python?

- **Python** is widely used for backend development, is easy to read, and has a rich ecosystem for web APIs and testing.
- **FastAPI** is a modern, high-performance web framework for building APIs with Python 3.7+ based on standard Python type hints.  
  - It provides automatic interactive documentation (`/docs`).
  - It is asynchronous and very fast, making it suitable for both learning and production.
  - It has excellent support for data validation and error handling via Pydantic models.

---

## How to Run Locally (PowerShell)

1. **Clone the repository**
   ```
    git clone https://github.com/NettaAd/ATM.git
    cd ATM
   ```

2. **Create and activate a virtual environment (optional but recommended)**  
    ```
    python -m venv venv
    .\venv\Scripts\Activate.ps1
    ```

3. **Install dependencies**
    ```
    pip install fastapi uvicorn pydantic httpx pytest
     ```

4. **Start the server locally**
   ```
   uvicorn main:app --reload
   ```

5. **API Documentation**  
   Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for interactive API docs.

6. **Run tests**
   ```
   pytest test_main.py
   ```

---

## Example Requests & Responses

### Get Balance

**Request:**  
`GET /accounts/123/balance`

**Response:**
```json
{
  "account_number": "123",
  "balance": 1000.0
}
```

---

### Deposit Money

**Request:**  
`POST /accounts/123/deposit`  
**Body:**
```json
{
  "amount": 100
}
```

**Response:**
```json
{
  "account_number": "123",
  "balance": 1100.0
}
```

---

### Withdraw Money

**Request:**  
`POST /accounts/123/withdraw`  
**Body:**
```json
{
  "amount": 50
}
```

**Response:**
```json
{
  "account_number": "123",
  "balance": 1050.0
}
```

---

### (Enrichment) Create Account

**Request:**  
`POST /accounts/`  
**Body:**
```json
{
  "account_number": "789",
  "initial_balance": 200
}
```

**Response:**
```json
{
  "message": "Account created",
  "account_number": "789"
}
```

---

### (Enrichment) Delete Account

**Request:**  
`DELETE /accounts/789`

**Response:**
```json
{
  "message": "Account deleted",
  "account_number": "789"
}
```

---

### (Enrichment) Transaction History

**Request:**  
`GET /accounts/123/history`

**Response:**
```json
{
  "account_number": "123",
  "history": [
    {
      "type": "deposit",
      "amount": 100,
      "timestamp": "2025-06-17T12:34:56.789012+00:00"
    },
    {
      "type": "withdraw",
      "amount": 50,
      "timestamp": "2025-06-17T12:35:10.123456+00:00"
    }
  ]
}
```

---

## Approach, Design Decisions, and Challenges

### Approach

- The project uses **FastAPI** for building a RESTful API, chosen for its speed, simplicity, and automatic documentation.
- Account data is stored in a Python dictionary in-memory, mapping account numbers to balances and transaction histories.
- The API is structured with clear endpoints for balance retrieval, deposit, withdrawal, account creation/deletion, and transaction history.

### Design Decisions

- **In-Memory Storage:**  
  For simplicity and to meet assignment requirements, all account data is stored in-memory. This makes the API stateless and easy to reset, but not suitable for production or multi-user environments.
- **Validation and Error Handling:**  
  The API checks for valid account numbers, positive transaction amounts, and sufficient funds for withdrawals. Errors return appropriate HTTP status codes and messages.
- **Testing:**  
  Automated tests are provided using FastAPI’s `TestClient` and `pytest` to ensure all endpoints work as expected and handle edge cases.
- **Documentation:**  
  FastAPI’s built-in `/docs` endpoint provides interactive API documentation for easy testing and exploration.

### Challenges

- **Testing State Changes:**  
  Since the account balances are stored in-memory, running tests in sequence can affect the state. This was managed by careful test design and could be improved by resetting state between tests.
- **Deployment Platform Requirements:**  
  Some cloud platforms (like Render.com) now require a credit card for free-tier deployment, which may be a barrier for some users. Alternatives were considered for truly free hosting.
- **API Security:**  
  For this assignment, no authentication is implemented. In a real-world scenario, security would be essential to protect user accounts.

---

## Unit Tests

Unit tests are provided in `test_main.py` using `pytest` and FastAPI’s `TestClient`.  
Each test function is documented and covers:

- Account creation and duplicate prevention
- Account deletion and error on missing account
- Balance retrieval and error on missing account
- Deposit and withdraw (including invalid cases)
- Transaction history with type and timestamp

To run the tests:
```
pytest test_main.py
```

Example test function:
```python
def test_deposit():
    """
    Test depositing a valid amount and handling invalid (negative) deposit amounts.
    """
    response = client.post("/accounts/123/deposit", json={"amount": 100})
    assert response.status_code == 200
    response = client.post("/accounts/123/deposit", json={"amount": -50})
    assert response.status_code == 400
```

---

## Notes

- If you try to access a non-existent account, you will get a 404 error.
- Withdrawals that exceed the balance or negative amounts will return a 400 error.

---

## Author

- Netta Adani
