from pydantic import BaseModel, ConfigDict

"""
    STK Transaction Response Model.
    It is used to validate the response data from the database and ensure that it conforms to the expected structure.
"""
class STKTransactionResponse(BaseModel):
    id: int
    phoneNumber: str
    amount: float
    merchant_request_id: str | None
    checkout_request_id: str | None
    mpesa_receipt_number: str | None
    status: str
    result_desc: str | None

    model_config = ConfigDict(from_attributes=True)

