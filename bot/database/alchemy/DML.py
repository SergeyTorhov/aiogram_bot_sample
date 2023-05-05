from sqlalchemy.exc import NoResultFound
from sqlalchemy import update

from bot.database.db_main import Database
from bot.database.alchemy.DDL import User


def create_new_user(user_id, last_call, user_name, first_name, last_name):
    try:
        Database().session.query(User.user_id).filter(User.user_id == user_id).one()
    except NoResultFound:
        Database().session.add(User(user_id=user_id,
                                    last_call=last_call,
                                    user_name=user_name,
                                    first_name=first_name,
                                    last_name=last_name))
        Database().session.commit()


def update_user_data(user_id, last_call, user_name, first_name, last_name):
    stmt = (update(User).
            where(User.user_id.in_([user_id])).
            values(last_call=last_call, user_name=user_name, first_name=first_name, last_name=last_name)
            )
    Database().session.execute(stmt)
    Database().session.commit()


def find_userdata_by_id(user_id):
    try:
        return Database().session.query(User.user_id, User.last_call).filter(User.user_id == user_id).one()
    except NoResultFound:
        return None
