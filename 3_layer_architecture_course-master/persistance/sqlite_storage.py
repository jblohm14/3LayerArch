import sqlite3
from business.model.user import User

from persistance.storage import UserStorage


class SqliteStorage(UserStorage):

    DB_FILE = ":memory:"
    CREATE_TABLE_STATEMENT = "CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, user_name TEXT, first_name TEXT, last_name TEXT, role INTEGER)"

    GET_USER_STATEMENT = "SELECT * FROM users WHERE user_id = ?"

    GET_ALL_USERS_STATEMENT = "SELECT * FROM users"

    ADD_USER_STATEMENT = (
        "INSERT INTO users (user_name, first_name, last_name, role) VALUES (?, ?, ?, ?)"
    )

    FIND_USER_STATEMENT = "SELECT * FROM users WHERE user_name = ?"

    DELETE_USER_STATEMENT = "DELETE FROM users WHERE user_id = ?"

    UPDATE_USER_STATEMENT = "UPDATE users SET user_name = ?, first_name = ?, last_name = ?, role = ? WHERE user_id = ?"

    def __init__(self):
        self._connection = sqlite3.connect(self.DB_FILE, check_same_thread=False)
        cursor = self._connection.cursor()
        cursor.execute(self.CREATE_TABLE_STATEMENT)
        cursor.close()
        self._connection.commit()

    def get(self, user_id):
        cursor = self._connection.cursor()
        cursor.execute(self.GET_USER_STATEMENT, (user_id,))
        row = cursor.fetchone()
        cursor.close()
        self._connection.commit()
        if row is None:
            return None
        return self._row_to_user(row)

    def get_all(self):
        cursor = self._connection.cursor()
        cursor.execute(self.GET_ALL_USERS_STATEMENT)
        rows = cursor.fetchall()
        cursor.close()
        self._connection.commit()

        return [self._row_to_user(row) for row in rows]

    def add(self, user):
        cursor = self._connection.cursor()
        cursor.execute(
            self.ADD_USER_STATEMENT,
            (user.user_name, user.first_name, user.last_name, user.role),
        )
        user_id = cursor.lastrowid
        cursor.close()
        self._connection.commit()
        user.user_id = user_id
        return user_id

    def find_by_user_name(self, user_name: str) -> User:
        cursor = self._connection.cursor()
        cursor.execute(self.FIND_USER_STATEMENT, (user_name,))
        row = cursor.fetchone()
        cursor.close()
        self._connection.commit()
        if row is None:
            return None
        return self._row_to_user(row)

    def delete(self, user_id):
        cursor = self._connection.cursor()
        cursor.execute(self.DELETE_USER_STATEMENT, (user_id,))
        cursor.close()
        self._connection.commit()

    def update(self, user):
        cursor = self._connection.cursor()
        cursor.execute(
            self.UPDATE_USER_STATEMENT,
            (user.user_name, user.first_name, user.last_name, user.role, user.user_id),
        )
        cursor.close()
        self._connection.commit()

    def _row_to_user(self, row):
        user = User(row[1], row[2], row[3])
        user.user_id = row[0]
        user.role = row[4]
        return user
