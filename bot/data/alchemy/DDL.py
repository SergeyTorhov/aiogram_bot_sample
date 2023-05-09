from sqlalchemy import String, Integer, DateTime, Column
from datetime import datetime
from typing import Optional

from bot.data.db_main import Database


class User(Database.BASE):
    """
    Класс реализующий таблицу user
    """
    __tablename__ = "user_table"

    user_id: int = Column(Integer, primary_key=True)
    last_call: datetime = Column(DateTime)
    user_name: str = Column(String, nullable=True)
    first_name: str = Column(String, nullable=True)
    last_name: str = Column(String, nullable=True)

    def __init__(self, user_id: int, last_call: datetime, user_name: str,
                 first_name: str, last_name: str):
        self.user_id = user_id
        self.last_call = last_call
        self.user_name = user_name
        self.first_name = first_name
        self.last_name = last_name


def create_all_db_structure(db_user_name: Optional[str], db_user_password: Optional[str],
                            db_address: Optional[str], db_name: Optional[str]):
    Database(db_user_name=db_user_name, db_user_password=db_user_password,
             db_address=db_address, db_name=db_name).BASE.metadata. \
        create_all(Database(db_user_name=db_user_name, db_user_password=db_user_password,
                            db_address=db_address, db_name=db_name).engine)
