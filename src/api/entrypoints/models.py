from enum import StrEnum
from pydantic import BaseModel,EmailStr
from typing import List


class CrmType(StrEnum):
    capsule = "capsule"
    pipedrive = "pipedrive"

class Contact(BaseModel):
    name: str
    first_name: str
    last_name: str
    crm: CrmType
    address: List[str]|None = None
    phone: List[str]|None = None
    email: List[EmailStr]|None = None
    company: str|None = None
    