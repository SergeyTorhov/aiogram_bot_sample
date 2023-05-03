import sqlite3
from typing import List, Tuple


class BotDBFunction:
    def __init__(self, dbname: str):
        self.__db_name = dbname
        self.create_user_table()

    def create_user_table(self) -> None:
        """
        Создает таблицу с заданным именем и столбцами в базе данных SQLite
        :return: ничего не возвращает
        """
        with sqlite3.connect(self.__db_name) as db:
            cursor = db.cursor()

            cursor.execute("""
                        CREATE TABLE IF NOT EXISTS users(
                        user_id INTEGER UNIQUE PRIMARY KEY NOT NULL,
                        first_call DATETIME  NOT NULL,
                        user_name TEXT,
                        first_name TEXT,
                        last_name TEXT
                        )""")

            db.commit()

    def insert_into_table(self, table_name: str, values: List[Tuple[int, str, str, str, str]]):
        """Вставляет значения в таблицу с заданным именем и структурой.

        Args:
            table_name (str): Имя таблицы.
            values (List[Tuple[int, str, str, int]]): Список кортежей, содержащих значения для вставки в таблицу.
        """
        with sqlite3.connect(self.__db_name) as conn:
            cur = conn.cursor()

            placeholders = ','.join(['?'] * len(values[0]))
            query = f"INSERT INTO {table_name} VALUES ({placeholders})"

            cur.executemany(query, values)
            conn.commit()

    def find_user_by_id(self, table_name: str, user_id: int) -> tuple:
        """
        Searches for a user by user_id in the 'users' table.

        Args:
            user_id (int): The user ID to search for.

        Returns:
            tuple: A tuple representing the user row in the 'users' table.
            :param user_id:
            :param table_name:
        """
        with sqlite3.connect(self.__db_name) as conn:
            cursor = conn.cursor()

            cursor.execute(f"SELECT * FROM {table_name} WHERE user_id=?", (user_id,))
            user_data = cursor.fetchone()

        return user_data

    def update_user_by_id(self, table_name: str, user_id: int, user_name: str, first_name: str, last_name: str) -> None:
        """
        Updates a user's record in the 'users' table with the specified user_id.

        Args:
            user_id (int): The user ID to update.
            first_call (str): The new first call value for the user.


        Returns:
            None
            :param last_name:
            :param first_name:
            :param user_name:
            :param user_id:
            :param table_name:
        """
        with sqlite3.connect(self.__db_name) as conn:
            cursor = conn.cursor()

            cursor.execute(f"UPDATE {table_name} SET user_name=?, first_name=?, last_name=? WHERE user_id=?",
                           (user_name, first_name, last_name, user_id))

            conn.commit()
