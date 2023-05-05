from typing import Final
from os import path

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from utils.singleton import SingletonMeta


class Database(metaclass=SingletonMeta):
    BASE: Final = declarative_base()
    __db_name = "bot_sqlite_db"
    __db_path = path.abspath(path.join("", __db_name))
    __db_engine = 'sqlite:///{}'.format(__db_path)

    def __init__(self):
        self.__engine = create_engine(Database.__db_engine, echo=True)
        session = sessionmaker(bind=self.__engine)
        self.__session = session()

    @property
    def session(self):
        return self.__session

    @property
    def engine(self):
        return self.__engine
