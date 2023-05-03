from sqlalchemy import create_engine
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from typing import Optional


class AllDDL:
    """
    Класс реализующий работу со структурой БД
    """
    def __init__(self, db_name: str):
        self.db_name = db_name

    class Base(DeclarativeBase):
        """
        Базовый класс
        """
        pass

    class User(Base):
        """
        Класс реализующий таблицу user
        """
        __tablename__ = "user"

        user_id: Mapped[int] = mapped_column(primary_key=True)
        last_call: Mapped[str] = mapped_column(String(64))
        user_name: Mapped[Optional[str]]
        first_name: Mapped[Optional[str]]
        last_name: Mapped[Optional[str]]

        def __init__(self, user_id: Mapped[int], last_call: Mapped[str], user_name: Mapped[Optional[str]],
                     first_name: Mapped[Optional[str]], last_name: Mapped[Optional[str]]):
            self.user_id = user_id
            self.last_call = last_call
            self.user_name = user_name
            self.first_name = first_name
            self.last_name = last_name

    def create_all_table(self) -> None:
        """
        Функция создания структуры БД
        :return:
        """
        engine = create_engine('sqlite:///{}'.format(self.db_name), echo=True)
        self.Base.metadata.create_all(engine)
        engine.dispose()
