from uuid import UUID
from dataclasses import dataclass
from app.domain.enums.webhook_event_type import WebhookEventType
from datetime import datetime

@dataclass
class WebhookEvent():
    id: UUID
    event_id: str
    payment_id: UUID
    event_type: WebhookEventType
    received_at: datetime   
    processed_at: datetime
    
