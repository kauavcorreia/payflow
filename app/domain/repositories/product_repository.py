from abc import ABC, abstractmethod
from app.domain.entities.product import Product
from uuid import UUID

class ProductRepository(ABC):
    @abstractmethod
    def get_product_by_id(self, product_id: UUID) -> Product | None:
        pass

    @abstractmethod
    def create_product(self, product: Product) -> Product:
        pass

    @abstractmethod
    def list_products(self) -> list[Product]:
        pass

