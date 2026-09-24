from abc import ABC, abstractmethod
from app.domain.entities.order import Order
from uuid import UUID

class OrderRepository(ABC):
    @abstractmethod
    def get_order_by_id(self, order_id: UUID) -> Order | None:
        pass

    @abstractmethod
    def create_order(self, order: Order) -> Order:
        pass

    @abstractmethod
    def update_order(self, order: Order) -> Order:
        pass

 