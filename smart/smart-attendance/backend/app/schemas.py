from pydantic import BaseModel
from typing import Optional


class EnrollIn(BaseModel):
    reg_no: str
    name: str
    phone_number: Optional[str] = None
