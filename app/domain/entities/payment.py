from uuid import UUID
from dataclasses import dataclass
from app.domain.enums.payment_status import PaymentStatus
from decimal import Decimal
from datetime import datetime

@dataclass
class Payment():
    id: UUID
    order_id: UUID
    status: PaymentStatus
    amount: Decimal
    external_payment_id: str
    created_at: datetime
    updated_at: datetime
