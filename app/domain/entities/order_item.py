from uuid import UUID
from dataclasses import dataclass 
from decimal import Decimal

@dataclass
class OrderItem():
    id: UUID
    order_id: UUID
    product: UUID
    quantity: int
    unit_price: Decimal
    subtotal: Decimal



