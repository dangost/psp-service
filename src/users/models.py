from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class User:
    id: str
    login: str
    email: str
    create_time: datetime


@dataclass(frozen=True)
class UserLoginDetails:
    login: str
    password: str


@dataclass(frozen=True)
class UserRegistrationDetails:
    login: str
    email: str
    password: str
