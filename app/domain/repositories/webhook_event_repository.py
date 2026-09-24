from abc import ABC, abstractmethod
from app.domain.entities.webhook_event import WebhookEvent
from uuid import UUID

class WebhookEventRepository(ABC):

    @abstractmethod
    def exist_event_by_id(self, event_id: UUID) ->bool:
        pass

    @abstractmethod
    def create_event(event_type: WebhookEvent) -> WebhookEvent:
        pass
