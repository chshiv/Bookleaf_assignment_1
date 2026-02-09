from pydantic import BaseModel, Field, PositiveInt, field_validator, validator
from fastapi import HTTPException

class WithdrawalRequest(BaseModel):
    author_id: PositiveInt = Field(..., description="ID of the author")
    amount: PositiveInt = Field(..., description="Amount to withdraw")

    class Config:
        extra = "forbid"

    # Pydantic v2 style field validator
    @field_validator("amount")
    @classmethod
    def check_minimum_withdrawal(cls, v):
        if v < 500:
            raise HTTPException(status_code=400, detail="Minimum withdrawal amount is ₹500")
        return v