from sqlalchemy.exc import NoResultFound
from sqlalchemy import update, Row
from sqlalchemy import select

from bot.data.db_main import Database
from bot.data.alchemy.DDL import User, TextString

from datetime import datetime
from typing import Optional
import logging


async def insert_text_string(string_name: str, string_text: str, string_type: str, string_language: str) -> None:
    """
    Writing text variables to the database.
    :param string_name:
    :param string_text:
    :param string_type:
    :param string_language:
    :return:
    """
    try:
        async with Database().session as session:
            async with session.begin():
                session.add(TextString(string_name=string_name,
                                       string_text=string_text,
                                       string_type=string_type,
                                       string_language=string_language))
                await session.commit()

    except Exception as exc:
        logging.debug(exc)
        await session.rollback()


async def find_text_string(string_name: str) -> str:
    """
    Finding the value of a text variable.
    :param string_name: string_name
    :return:
    """
    try:

        async with Database().session as session:
            stmt = select(TextString.string_text, TextString.string_language).where(
                TextString.string_name == string_name)
            result = await session.execute(stmt)

        return result.one()[0]
    except NoResultFound:
        logging.exception(msg="TEXT NOT FOUND")
        return "STRING {} NOT FOUND".format(string_name)


async def create_new_user(user_id: int, last_call: datetime, user_name: str,
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
        async with Database().session as session:
            async with session.begin():
                session.add(User(user_id=user_id,
                                 last_call=last_call,
                                 user_name=user_name,
                                 first_name=first_name,
                                 last_name=last_name))
                # await session.commit()
    except Exception as exc:
        logging.exception(exc)
        await session.rollback()


async def update_user_data(user_id, last_call, user_name, first_name, last_name) -> None:
    """
    Updating user data in the database.
    :param user_id:
    :param last_call:
    :param user_name:
    :param first_name:
    :param last_name:
    :return:
    """
    try:
        async with Database().session as session:

            stmt = update(User).where(User.user_id == user_id).values(last_call=last_call, user_name=user_name,
                                                                      first_name=first_name, last_name=last_name)
            await session.execute(stmt)
            await session.commit()
    except Exception as exc:
        logging.info(exc)
        await session.rollback()


async def find_userdata_by_id(user_id: int) -> Optional[tuple[int, datetime]]:
    """
    Search for user data in the database.
    :param user_id:
    :return:
    """
    try:
        async with Database().session as session:
            stmt = select(User.user_id, User.last_call).where(User.user_id == user_id)
            result = await session.execute(stmt)
        return result.one()

    except NoResultFound:
        logging.info("NO USER DATA IN DB")
        return None
