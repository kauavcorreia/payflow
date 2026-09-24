from uuid import UUID
from dataclasses import dataclass
from decimal import Decimal

@dataclass
class Product():
    id: UUID | None
    name: str
    current_price: Decimal

