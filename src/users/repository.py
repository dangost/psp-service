from sqlalchemy import Table, MetaData, Column, String, TIMESTAMP

from src.sql_config import SqlConfig
from src.users.models import User

USERS: Table


def describe_table(metadata: MetaData):
    return Table(
        "users",
        metadata,
        Column("id", String, primary_key=True, nullable=False),
        Column("login", String, nullable=False, unique=True),
        Column("email", String, nullable=False, unique=True),
        Column("password_hash", String, nullable=False),
        Column("create_time", TIMESTAMP, nullable=False)
    )


class UsersRepository:
    def __init__(self, sql_config: SqlConfig):
        global USERS
        USERS = describe_table(sql_config.metadata)
        self.engine = sql_config.engine

    def insert(self, user: User, password_hash: str) -> None:
        statement = USERS.insert().values(
            id=user.id,
            login=user.login,
            email=user.email,
            password_hash=password_hash,
            create_time=user.create_time
        )

        with self.engine.begin() as connection:
            connection.execute(statement)

    def get_by_login(self, login: str) -> User:
        statement = USERS.select().where(USERS.c.login == login)

        with self.engine.begin() as connection:
            row = connection.execute(statement).one_or_none()

        return self._row_to_user(row)

    def get_by_id(self, _id: str) -> User:
        statement = USERS.select().where(USERS.c.id == _id)

        with self.engine.begin() as connection:
            row = connection.execute(statement).one_or_none()

        return self._row_to_user(row)

    def get_by_email(self, email: str) -> User:
        statement = USERS.select().where(USERS.c.email == email)

        with self.engine.begin() as connection:
            row = connection.execute(statement).one_or_none()

        return self._row_to_user(row)

    def get_password_hash(self, login: str):
        statement = USERS.select().where(USERS.c.login == login)

        with self.engine.begin() as connection:
            row = connection.execute(statement).one_or_none()

        return row.password_hash

    @staticmethod
    def _row_to_user(row) -> User:
        return User(
            id=row.id,
            login=row.login,
            email=row.email,
            create_time=row.create_time
        ) if row else None

