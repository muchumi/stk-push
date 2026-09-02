from pydantic import BaseModel, Field, field_validator


class STKPushRequest(BaseModel):
    phoneNumber: str = Field(
        ...,
        description="Customer number in international format",
        json_schema_extra={"example": "+254719271870"}
    )

    amount: float = Field(
        ...,
        gt=0,
        description="Amount to be charged",
        json_schema_extra={"example": 100.00}
    )

    accountReference: str = Field(
        ...,
        min_length=1,
        max_length=20,
        description="Reference for the transaction",
        json_schema_extra={"example": "INV001"}
    )

    transactionDescription: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Description of the transaction",
        json_schema_extra={"example": "Payment For Goods"}
    )

    @field_validator("phoneNumber")
    @classmethod
    def validate_phone_number(cls, value):
        if not value.startswith("+254") or len(value) != 13:
            raise ValueError("Invalid Kenyan phone number")

        if not value[1:].isdigit():
            raise ValueError("Invalid Kenyan phone number")

        return value