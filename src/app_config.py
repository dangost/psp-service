import os
from uuid import uuid4
from dotenv import load_dotenv

from src.sql_config import SqlConfig


class AppConfig:
    def __init__(self):
        load_dotenv()
        connection: str = os.getenv('CONNECTION_STRING', default='sqlite:///../test.db')
        self.jwt_secret = os.getenv('JWT_SECRET', default=str(uuid4()).replace('-', ''))
        self.ip = os.getenv('IP', default="127.0.0.1")
        self.port = os.getenv('PORT', default=5000)
        self.sql_config = SqlConfig(connection)

