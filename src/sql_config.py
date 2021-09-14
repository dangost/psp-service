from sqlalchemy import MetaData
from sqlalchemy.future import create_engine


class SqlConfig:
    def __init__(self, connection: str):
        self.engine = create_engine(connection)
        self.metadata = MetaData(self.engine)
