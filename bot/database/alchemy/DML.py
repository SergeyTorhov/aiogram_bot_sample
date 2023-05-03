from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import select

from typing import Optional

from bot.database.alchemy.DDL import AllDDL


class AllDML:
    """
    Класс реализующий работу данными в БД
    """

    def __init__(self, db_name: str):
        self.db_name = db_name
        self.engine = create_engine('sqlite:///{}'.format(self.db_name), echo=True)

    def update_user_data(self, user_id, last_call, user_name, first_name, last_name):
        with Session(self.engine) as session:
            stmt = select(AllDDL.User).where(AllDDL.User.user_id.in_([user_id, ]))
            my_user = session.scalars(stmt).one()
            my_user.last_name = last_name
            my_user.user_name = user_name
            my_user.first_name = first_name
            my_user.last_call = last_call
            session.commit()

    def find_user_by_id(self, user_id):
        with Session(self.engine) as session:
            stmt = select(AllDDL.User).where(AllDDL.User.user_id.in_([user_id, ]))
            return session.scalars(stmt).first()

    def insert_user_data(self, user_id, last_call, user_name, first_name, last_name):
        with Session(self.engine) as session:
            my_user_data = AllDDL.User(
                user_id=user_id,
                last_call=last_call,
                user_name=user_name,
                first_name=first_name,
                last_name=last_name
            )
            session.add_all([my_user_data])
            session.commit()
