from datetime import datetime

from ninja import Schema

class CustomerSchemaIn(Schema):
    name: str
    phone: str

class CustomerSchemaOut(Schema):
    id: int
    name: str
    phone: str
    is_connected: bool
    is_lead: bool
    created_at: datetime