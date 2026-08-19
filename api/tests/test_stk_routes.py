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