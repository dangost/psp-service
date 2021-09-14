from hashlib import sha512
from uuid import uuid4
from datetime import datetime, timezone

import jwt
from jwt import DecodeError

from src.common.exceptions import UnauthorizedException
from src.sql_config import SqlConfig
from src.users.exceptions import IncorrectPasswordException, UserNotFoundException, LoginAlreadyExists, \
    EmailAlreadyExists

from src.users.models import UserLoginDetails, UserRegistrationDetails, User
from src.users.repository import UsersRepository


class UsersService:
    def __init__(self, sql_config: SqlConfig, jwt_secret: str):
        self.users_repo = UsersRepository(sql_config)
        self._jwt_secret = jwt_secret

    def create(self, users_registration: UserRegistrationDetails) -> User:
        self.exists(users_registration.login, users_registration.email)
        user = User(
            id=str(uuid4()),
            login=users_registration.login,
            email=users_registration.email,
            create_time=datetime.now(tz=timezone.utc)
        )
        password_hash = self._sha(users_registration.password)
        self.users_repo.insert(user, password_hash)
        return user

    def login(self, users_login: UserLoginDetails) -> str:
        real_password_hash = self.users_repo.get_password_hash(users_login.login)
        password_hash = self._sha(users_login.password)

        if real_password_hash != password_hash:
            raise IncorrectPasswordException()

        return self._create_jwt(users_login.login)

    def get_by_id(self, user_id: str) -> User:
        """
        ::raises UserNotFoundException
        """
        user = self.users_repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundException(user_id)
        return user

    def get_by_login(self, login: str) -> User:
        """
        ::raises UserNotFoundException
        """
        user = self.users_repo.get_by_login(login)
        if not user:
            raise UserNotFoundException(login)
        return user

    def exists(self, login: str, email: str) -> None:
        """
        ::raise LoginAlreadyExists
        ::raise EmailAlreadyExists
        """
        if self.users_repo.get_by_login(login):
            raise LoginAlreadyExists(login)

        if self.users_repo.get_by_email(email):
            raise EmailAlreadyExists(email)

    def auth(self, headers: dict) -> User:
        try:
            token = headers['Authorization']
            payload = jwt.decode(token, self._jwt_secret, algorithms=["HS256"])
            login = payload["login"]
        except (DecodeError, KeyError):
            raise UnauthorizedException()
        return self.get_by_login(login)

    def _create_jwt(self, user_login: str) -> str:
        payload = {"login": user_login, "authTime": str(datetime.now(tz=timezone.utc))}
        token = jwt.encode(payload, self._jwt_secret, algorithm="HS256")
        return token

    @staticmethod
    def _sha(_input: str) -> str:
        return sha512(f"{_input}".encode("utf-8")).hexdigest()
