from uuid import UUID
from dataclasses import dataclass

@dataclass
class User():
    id: UUID
    name: str
    email: str
    password: str
