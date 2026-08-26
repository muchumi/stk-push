from api.models.stk_transaction import STKTransaction

def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()=={
        "message": "Hello world, welcome to STK push API"
    }


# Testing stk push endpoint
def test_stk_push(client, monkeypatch):
    def mock_initiate_stk_push(phoneNumber, amount):
        return {
            "MerchantRequestID": "TEST-MERCHANT-123",
            "CheckoutRequestID": "TEST-CHECKOUT-123",
            "ResponseCode": "0",
            "ResponseDescription": "Success",
            "CustomerMessage": "Success. Request accepted for processing"
        }

    monkeypatch.setattr(
        "api.routers.stk_routes.initiate_stk_push",
        mock_initiate_stk_push
    )

    response = client.post(
        "/stk/push",
        json={
            "phoneNumber": "254719271870",
            "amount": 100,
            "accountReference": "TEST001",
            "transactionDescription": "Test payment"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["phoneNumber"] == "254719271870"
    assert data["amount"] == 100
    assert data["merchant_request_id"] == "TEST-MERCHANT-123"
    assert data["checkout_request_id"] == "TEST-CHECKOUT-123"
    assert data["status"] == "pending"


# Testing successful STK callback
def test_stk_callback_success(client, db):
    # Create a transaction first
    transaction = STKTransaction(
        phoneNumber="254719271870",
        amount=100,
        merchant_request_id="TEST-MERCHANT-123",
        checkout_request_id="TEST-CHECKOUT-123",
        status="pending"
    )

    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    callback_payload = {
        "Body": {
            "stkCallback": {
                "MerchantRequestID": "TEST-MERCHANT-123",
                "CheckoutRequestID": "TEST-CHECKOUT-123",
                "ResultCode": 0,
                "ResultDesc": "The service request is processed successfully.",
                "CallbackMetadata": {
                    "Item": [
                        {
                            "Name": "Amount",
                            "Value": 100
                        },
                        {
                            "Name": "MpesaReceiptNumber",
                            "Value": "TEST123ABC"
                        },
                        {
                            "Name": "TransactionDate",
                            "Value": 20260824123045
                        },
                        {
                            "Name": "PhoneNumber",
                            "Value": 254719271870
                        }
                    ]
                }
            }
        }
    }

    response = client.post(
        "/stk/callback",
        json=callback_payload
    )

    assert response.status_code == 200

    data = response.json()

    assert data["ResultCode"] == 0
    assert data["ResultDesc"] == "Accepted"
    assert data["message"] == "Callback received and processed successfully."

    # Verify transaction was updated
    db.refresh(transaction)

    assert transaction.status == "success"
    assert transaction.phoneNumber == "254719271870"
    assert transaction.mpesa_receipt_number == "TEST123ABC"
    assert transaction.transaction_date == 20260824123045


# Testing failed STK callback
def test_stk_callback_failed(client, db):
    # Create a pending transaction
    transaction = STKTransaction(
        phoneNumber="254719271870",
        amount=100,
        merchant_request_id="TEST-MERCHANT-456",
        checkout_request_id="TEST-CHECKOUT-456",
        status="pending"
    )

    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    callback_payload = {
        "Body": {
            "stkCallback": {
                "MerchantRequestID": "TEST-MERCHANT-456",
                "CheckoutRequestID": "TEST-CHECKOUT-456",
                "ResultCode": 1032,
                "ResultDesc": "Request cancelled by user."
            }
        }
    }

    response = client.post(
        "/stk/callback",
        json=callback_payload
    )

    assert response.status_code == 200

    data = response.json()

    assert data["ResultCode"] == 0
    assert data["ResultDesc"] == "Accepted"

    # Verify transaction was marked as failed
    db.refresh(transaction)

    assert transaction.status == "failed"


# Testing callback for an unknown transaction
def test_stk_callback_unknown_transaction(client):
    callback_payload = {
        "Body": {
            "stkCallback": {
                "MerchantRequestID": "UNKNOWN-MERCHANT",
                "CheckoutRequestID": "UNKNOWN-CHECKOUT",
                "ResultCode": 0,
                "ResultDesc": "The service request is processed successfully.",
                "CallbackMetadata": {
                    "Item": [
                        {
                            "Name": "Amount",
                            "Value": 100
                        },
                        {
                            "Name": "MpesaReceiptNumber",
                            "Value": "UNKNOWN123"
                        },
                        {
                            "Name": "TransactionDate",
                            "Value": 20260824123045
                        },
                        {
                            "Name": "PhoneNumber",
                            "Value": 254719271870
                        }
                    ]
                }
            }
        }
    }

    response = client.post(
        "/stk/callback",
        json=callback_payload
    )

    assert response.status_code == 200

    data = response.json()

    assert data["ResultCode"] == 0
    assert data["ResultDesc"] == "Accepted"
    assert data["message"] == "Callback received and processed successfully."

# Testing get all transactions
def test_get_all_transactions(client, db):

    transaction1 = STKTransaction(
        phoneNumber="254719271870",
        amount=100,
        merchant_request_id="MERCHANT-001",
        checkout_request_id="CHECKOUT-001",
        status="success"
    )

    transaction2 = STKTransaction(
        phoneNumber="254712345678",
        amount=200,
        merchant_request_id="MERCHANT-002",
        checkout_request_id="CHECKOUT-002",
        status="pending"
    )

    db.add_all([transaction1, transaction2])
    db.commit()

    response = client.get("/stk/transactions")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["phoneNumber"] == "254719271870"
    assert data[1]["phoneNumber"] == "254712345678"


# Testing get single transaction
def test_get_single_transaction(client, db):

    transaction = STKTransaction(
        phoneNumber="254719271870",
        amount=100,
        merchant_request_id="MERCHANT-003",
        checkout_request_id="CHECKOUT-003",
        status="pending"
    )

    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    response = client.get(
        f"/stk/transactions/{transaction.id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == transaction.id
    assert data["phoneNumber"] == "254719271870"
    assert data["amount"] == 100
    assert data["checkout_request_id"] == "CHECKOUT-003"
    assert data["status"] == "pending"


# Testing single transaction not found
def test_get_single_transaction_not_found(client):

    response = client.get("/stk/transactions/99999")

    assert response.status_code == 404

    data = response.json()

    assert data["detail"] == "Transaction resource not found"

# Testing transaction search with phone number
def test_search_transactions_by_phone_number(client, db):
    transaction_one=STKTransaction(
        phoneNumber="254719271870",
        amount=100,
        merchant_request_id="MERCHANT-001",
        checkout_request_id="CHECKOUT-001",
        status="success"
    )
    transaction_two=STKTransaction(
        phoneNumber="254712345678",
        amount=200,
        merchant_request_id="MERCHANT-002",
        checkout_request_id="CHECKOUT-002",
        status="pending"
    )
    db.add_all([transaction_one, transaction_two])
    db.commit()

    response=client.get("/stk/transactions/search?phoneNumber=254719271870")
    assert response.status_code==200
    data=response.json()

    assert len(data)==1
    assert data[0]["phoneNumber"]=="254719271870"
    assert data[0]["amount"]==100