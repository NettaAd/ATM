from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.testclient import TestClient

app = FastAPI()

# In-memory account storage: keys are account numbers, values are balances
accounts = {
    "123": 1000.0,
    "456": 500.0
}

class Transaction(BaseModel):
    amount: float

@app.get("/accounts/{account_number}/balance")
def get_balance(account_number: str):
    """
    Retrieve the current balance for a given account number.
    """
    if account_number not in accounts:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"account_number": account_number, "balance": accounts[account_number]}

@app.post("/accounts/{account_number}/withdraw")
def withdraw(account_number: str, transaction: Transaction):
    """
    Withdraw a specified amount from the account if sufficient funds exist.
    """
    if account_number not in accounts:
        raise HTTPException(status_code=404, detail="Account not found")
    if transaction.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
    if accounts[account_number] < transaction.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")
    accounts[account_number] -= transaction.amount
    return {"account_number": account_number, "balance": accounts[account_number]}

@app.post("/accounts/{account_number}/deposit")
def deposit(account_number: str, transaction: Transaction):
    """
    Deposit a specified amount into the account.
    """
    if account_number not in accounts:
        raise HTTPException(status_code=404, detail="Account not found")
    if transaction.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
    accounts[account_number] += transaction.amount
    return {"account_number": account_number, "balance": accounts[account_number]}

@app.get("/")
def root():
    return {"message": "ATM API is running. Visit /docs for API documentation."}
