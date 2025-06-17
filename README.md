# ATM System API

## Overview

This project is a simple server-side ATM system built with FastAPI.  
It allows users to:
- Retrieve account balance
- Deposit money
- Withdraw money

All data is stored in-memory for demonstration purposes.

---

## How to Run

1. **Install dependencies**  
   (Make sure you are in your virtual environment)
   ```
   pip install fastapi uvicorn pydantic httpx pytest
   ```

2. **Start the server**
   ```
   uvicorn main:app --reload
   ```

3. **API Documentation**  
   Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for interactive API docs.

4. **Run tests**
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

## Notes

- If you try to access a non-existent account, you will get a 404 error.
- Withdrawals that exceed the balance or negative amounts will return a 400 error.

---

## Author

- Your Name Here
