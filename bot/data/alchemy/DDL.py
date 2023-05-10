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


class TextString(Database.BASE):
    """
    Класс реализующий таблицу text_string
    """
    __tablename__ = "text_string"

    string_id: int = Column(Integer, primary_key=True)
    string_name: str = Column(String, nullable=True, unique=True)
    string_text: str = Column(String, nullable=True)
    string_language: str = Column(String, nullable=True)
    string_type: str = Column(String, nullable=True)

    def __init__(self, string_name: str, string_text: str,
                 string_language: str, string_type: str):
        self.string_name = string_name
        self.string_text = string_text
        self.string_language = string_language
        self.string_type = string_type


def create_all_db_structure(db_user_name: Optional[str], db_user_password: Optional[str],
                            db_address: Optional[str], db_name: Optional[str]):
    """
    The function of creating tables in the database.
    :param db_user_name:
    :param db_user_password:
    :param db_address:
    :param db_name:
    :return:
    """
    Database(db_user_name=db_user_name, db_user_password=db_user_password,
             db_address=db_address, db_name=db_name).BASE.metadata. \
        create_all(Database(db_user_name=db_user_name, db_user_password=db_user_password,
                            db_address=db_address, db_name=db_name).engine)


