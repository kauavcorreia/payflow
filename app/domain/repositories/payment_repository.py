from abc import ABC, abstractmethod
from app.domain.entities.payment import Payment
from uuid import UUID

class PaymentRepository(ABC):

    @abstractmethod
    def create_payment(self, payment: Payment) -> Payment:
        pass

    @abstractmethod
    def get_payment_by_id(self, payment_id: UUID) -> Payment | None:
        pass

    @abstractmethod
    def get_payments_by_order_id(self, order_id: UUID) -> list[Payment]:
        pass

    @abstractmethod
    def get_payments_by_external_id(self, external_id: str) -> list[Payment]:
        pass

    @abstractmethod
    def update_payment(self, payment: Payment) -> Payment:
        pass

