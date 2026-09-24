from uuid import UUID
from dataclasses import dataclass
from app.domain.enums.order_status import OrderStatus
from decimal import Decimal
from datetime import datetime

@dataclass 
class Order():
    id: UUID
    user_id: UUID
    status: OrderStatus
    total_amount: Decimal
    created_at: datetime
    updated_at: datetime


