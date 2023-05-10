from sqlalchemy.exc import NoResultFound
from sqlalchemy import update

from bot.data.db_main import Database
from bot.data.alchemy.DDL import User, TextString

from datetime import datetime
from typing import Optional


def find_text_string(string_name: str) -> Optional[str]:
    """
    Finding the value of a text variable.
    :param string_name: string_name
    :return:
    """
    try:
        return Database().session.query(TextString.string_text).filter(TextString.string_name == string_name).one()[0]
    except NoResultFound:
        return None


def create_new_user(user_id: int, last_call: datetime, user_name: str,
                    first_name: str, last_name: str) -> None:
    """
    Writing user data to the database.
    :param user_id:
    :param last_call:
    :param user_name:
    :param first_name:
    :param last_name:
    :return:
    """
    try:
        Database().session.add(User(user_id=user_id,
                                    last_call=last_call,
                                    user_name=user_name,
                                    first_name=first_name,
                                    last_name=last_name))
        Database().session.commit()
    except Exception as exc:
        print(exc)
        Database().session.rollback()


def update_user_data(user_id, last_call, user_name, first_name, last_name) -> None:
    """
    Updating user data in the database.
    :param user_id:
    :param last_call:
    :param user_name:
    :param first_name:
    :param last_name:
    :return:
    """
    stmt = (update(User).
            filter(User.user_id == user_id).
            values(last_call=last_call, user_name=user_name, first_name=first_name, last_name=last_name)
            )
    Database().session.execute(stmt)
    Database().session.commit()


def find_userdata_by_id(user_id: int) -> Optional[tuple[int, datetime]]:
    """
    Search for user data in the database.
    :param user_id:
    :return:
    """
    try:
        return Database().session.query(User.user_id, User.last_call).filter(User.user_id == user_id).one()
    except NoResultFound:
        return None


def insert_text_string(string_name: str, string_text: str, string_type: str, string_language: str) -> None:
    """
    Writing text variables to the database.
    :param string_name:
    :param string_text:
    :param string_type:
    :param string_language:
    :return:
    """
    try:
        Database().session.add(TextString(string_name=string_name,
                                          string_text=string_text,
                                          string_type=string_type,
                                          string_language=string_language))
        Database().session.commit()
    except Exception as exc:
        print(exc)
        Database().session.rollback()
