"""Pydantic schemas for calculation validation and serialization."""

from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, model_validator


class CalculationType(str, Enum):
    """Supported arithmetic calculation types."""

    ADD = "Add"
    SUB = "Sub"
    MULTIPLY = "Multiply"
    DIVIDE = "Divide"


class CalculationCreate(BaseModel):
    """Validate data used to create a calculation."""

    a: float
    b: float
    type: CalculationType

    @model_validator(mode="after")
    def validate_operands(self) -> "CalculationCreate":
        """Reject division when the second operand is zero."""

        if (
            self.type == CalculationType.DIVIDE
            and self.b == 0
        ):
            raise ValueError("Cannot divide by zero.")

        return self


class CalculationRead(BaseModel):
    """Serialize a saved calculation."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    a: float
    b: float
    type: CalculationType
    result: float