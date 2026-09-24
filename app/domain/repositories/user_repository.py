from abc import ABC, abstractmethod
from app.domain.entities.user import User
from uuid import UUID

class UserRepository(ABC):

    @abstractmethod
    def get_user_by_id(self, user_id: UUID) -> User | None:
        pass

    @abstractmethod
    def create_user(self, user: User) -> User:
        pass
