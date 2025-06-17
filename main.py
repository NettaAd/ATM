"""
ATM System API

This FastAPI application simulates a simple ATM system with in-memory storage.
It supports creating and deleting accounts, retrieving balances, depositing and withdrawing money,
and viewing transaction history with timestamps.

Assignment-required endpoints are listed first, followed by enrichment (optional) endpoints.
"""
from typing import Dict
from datetime import datetime, UTC
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# In-memory account storage: keys are account numbers, values are dicts with balance and history
accounts: Dict[str, Dict] = {
    "123": {"balance": 1000.0, "history": []},
    "456": {"balance": 500.0, "history": []}
}

class Transaction(BaseModel):
    """
    Represents a transaction request for deposit or withdrawal.
    """
    amount: float

class AccountCreate(BaseModel):
    """
    Represents a request to create a new account.
    """
    account_number: str
    initial_balance: float = 0.0

# ============================
# Assignment-Required Methods
# ============================

@app.get("/accounts/{account_number}/balance")
def get_balance(account_number: str):
    """
    Retrieve the current balance for a given account number.
    """
    if account_number not in accounts:
        raise HTTPException(status_code=404, detail="Account not found")
    
    return {"account_number": account_number, "balance": accounts[account_number]["balance"]}

@app.post("/accounts/{account_number}/withdraw")
def withdraw(account_number: str, transaction: Transaction):
    """
    Withdraw a specified amount from the account if sufficient funds exist.
    """
    if account_number not in accounts:
        raise HTTPException(status_code=404, detail="Account not found")

    if transaction.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")

    if accounts[account_number]["balance"] < transaction.amount:
        raise HTTPException(status_code=400, detail=(
                f"Insufficient funds: current balance is {accounts[account_number]['balance']}, "
                f"attempted to withdraw {transaction.amount}"
            )
        )

    accounts[account_number]["balance"] -= transaction.amount
    accounts[account_number]["history"].append({
        "type": "withdraw",
        "amount": transaction.amount,
        "timestamp": datetime.now(UTC).isoformat()
    })
    return {"account_number": account_number, "balance": accounts[account_number]["balance"]}

@app.post("/accounts/{account_number}/deposit")
def deposit(account_number: str, transaction: Transaction):
    """
    Deposit a specified amount into the account.
    """
    if account_number not in accounts:
        raise HTTPException(status_code=404, detail="Account not found")

    if transaction.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")

    accounts[account_number]["balance"] += transaction.amount
    accounts[account_number]["history"].append({
        "type": "deposit",
        "amount": transaction.amount,
        "timestamp": datetime.now(UTC).isoformat()
    })
    return {"account_number": account_number, "balance": accounts[account_number]["balance"]}

# ============================
#       Enrichment Methods
# ============================

@app.post("/accounts/")
def create_account(account: AccountCreate):
    """
    (Enrichment) Create a new account with a unique account number and optional initial balance.
    """
    if account.account_number in accounts:
        raise HTTPException(status_code=400, detail="Account already exists")

    accounts[account.account_number] = {
        "balance": account.initial_balance,
        "history": [{
            "type": "create",
            "amount": account.initial_balance,
            "timestamp": datetime.now(UTC).isoformat()
        }]
    }
    return {"message": "Account created", "account_number": account.account_number}

@app.delete("/accounts/{account_number}")
def delete_account(account_number: str):
    """
    (Enrichment) Delete an account by account number.
    """
    if account_number not in accounts:
        raise HTTPException(status_code=404, detail="Account not found")

    del accounts[account_number]
    return {"message": "Account deleted", "account_number": account_number}

@app.get("/accounts/{account_number}/history")
def get_history(account_number: str):
    """
    (Enrichment) Get the transaction history for an account.
    """
    if account_number not in accounts:
        raise HTTPException(status_code=404, detail="Account not found")

    return {
        "account_number": account_number,
        "history": accounts[account_number]["history"]
    }

@app.get("/")
def root():
    """
    Root endpoint providing a friendly message and link to API documentation.
    """
    return {"message": "ATM API is running. Visit /docs for API documentation."}
