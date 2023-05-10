from typing import Final
from typing import Optional
from os import path

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from utils.singleton import SingletonMeta


class Database(metaclass=SingletonMeta):
    """
    A class that implements work with the database. The only instance in the application.
    """
    BASE: Final = declarative_base()

    # USE FOR SQLITE
    # __db_name = "bot_sqlite_db"
    # __db_path = path.abspath(path.join("", __db_name))

    def __init__(self, db_user_name: Optional[str], db_user_password: Optional[str],
                 db_address: Optional[str], db_name: Optional[str]):
        # USE FOR POSTGRESQL
        self.__db_engine = "postgresql+psycopg2://{}:{}@{}/{}".format(db_user_name,
                                                                      db_user_password,
                                                                      db_address,
                                                                      db_name)

        # USE FOR SQLITE
        # self.__db_engine = 'sqlite:///{}'.format(Database.__db_path)

        self.__engine = create_engine(self.__db_engine, echo=True)
        session = sessionmaker(bind=self.__engine)
        self.__session = session()

    @property
    def session(self):
        """
        Getter for getting the current session.
        :return:
        """
        return self.__session

    @property
    def engine(self):
        """
        Getter for getting the current engine.
        :return:
        """
        return self.__engine
