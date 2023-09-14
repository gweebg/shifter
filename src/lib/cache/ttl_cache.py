"""
Code adapted from https://github.com/colingrady/LiteCache/blob/main/litecache.py
"""

import pickle
import sqlite3
import time
from typing import Any, Optional

import src.lib.cache.sql_commands as queries

DAY_AS_SECONDS: int = 24 * 60 * 60
DEFAULT_TTL = DAY_AS_SECONDS * 7  # Two week time to live.


class NotSet:
    """
    This class is used to represent a cache miss.
    """
    __slots__ = ()


class Cache:

    """
    This class represent an in-disk ttl caching system using SQLite3.

    :param cache_db: Name of the file to store the database, use :memory: to store database in memory.
    :type cache_db: str
    :param ttl: Default time to live value for each cache entry. Defaults to DEFAULT_TTL.
    :type ttl: int
    :param save_on_exit: Enable of disable on exit saving (committing). True by default.
    :type save_on_exit: bool
    """

    # Limiting the set of attributes of this class (better performance).
    __slots__ = (
        '_conn',
        'db',
        'ttl',
        'save_on_exit'
    )

    def __init__(self, cache_db: Optional[str] = None,
                 ttl: Optional[int] = DEFAULT_TTL, save_on_exit: Optional[bool] = True):
        """
        Class constructor.
        """

        # Get the cache file
        cache_db: str = cache_db or ':memory:'

        # Save the details
        self._conn: Optional[sqlite3.Connection] = None
        self.db: str = cache_db
        self.ttl = ttl
        self.save_on_exit = save_on_exit

    def __repr__(self) -> str:
        """
        :return: String representation of the Cache class.
        :rtype: str
        """
        return (f'Cache(db={self.db}, ttl={self.ttl}, '
                f'save_on_exit={self.save_on_exit})')

    def __del__(self):
        """
        Closes the database connection cleanly, saving before deleting if desired.
        """

        if self._conn:

            if self.save_on_exit:
                self.save()

            self._conn.close()

    def __contains__(self, key: str) -> bool:
        """
        Default contains method inherited from object.
        Checks whether the key is present or not on the database.
        :param key: Key to be checked.
        :type key: str
        :return: True if contains the key, False otherwise.
        :rtype: bool
        """
        return self.has(key)

    def __getitem__(self, key: str) -> Any:
        """
        Get the value to which its primary key is key.
        :param key: Key to be retrieved.
        :type key: str
        :return: The value obtained from the provided key.
        :rtype: Any
        """
        return self.get(key)

    def __setitem__(self, key: str, value: Any) -> None:
        """
        Set a new entry on the database.
        :param key: Key from the (key, value) pair.
        :type key: str
        :param value: Value from the (key, value) pair.
        :type value: Any
        """
        self.set(key, value)

    @staticmethod
    def _now() -> int:
        """
        :return: The current epoch time.
        :rtype: int
        """
        return int(time.time())

    def _since(self, ttl: Optional[int] = None) -> int:
        """
        Calculates the earliest last_seen time for an entry to be returned.
        :param ttl: Optional ttl value to overwrite the original set at the instantiation of the class.
        :type ttl: int, optional
        :return: Earliest last_seen time for an entry to be returned.
        :rtype: int
        """

        ttl: int = ttl or self.ttl  # Allow ttl to be overriden.
        return 0 if ttl == 0 else self._now() - ttl

    @property
    def _connection(self) -> sqlite3.Connection:
        """
        Property that represents the sqlite3 connection.
        :return: The SQLite3 connection object.
        :rtype: sqlite3.Connection
        """

        if not self._conn:  # If the connection is not yet set up.

            # Open the connection
            self._conn = sqlite3.connect(database=self.db, timeout=30)

            # Creating tables and indexes for the database.
            self._conn.execute(queries.SQL_TABLE_CREATE)
            self._conn.execute(queries.SQL_INDEX_CREATE)

            self.save()  # Saving the changes.

        return self._conn

    def save(self) -> None:
        """
        Commit incoming changes to the database.
        """
        self._connection.commit()

    def rollback(self) -> None:
        """
        Rollback any changes made to the database since the last save or open.
        """
        self._connection.rollback()

    def has(self, key: str, ttl: Optional[int] = None) -> bool:
        """
        Checks whether a key exists on the database, has in account the ttl of the row.
        :param key: Value in which to look for.
        :type key: str
        :param ttl: Optional overwrite ttl value.
        :type ttl: int, optional
        :return: True if the key exists, False otherwise.
        :rtype: bool
        """

        # Query the database.
        cursor: sqlite3.Cursor = self._connection.execute(queries.SQL_GET_KEY_SINCE, (key, self._since(ttl)))
        return cursor.fetchone() is not None

    def get(self, key: str, default: Optional[Any] = NotSet, ttl: Optional[int] = None) -> Any:
        """
        Retrieves the corresponding value to the specified key from the database.
        :param key: The primary key value.
        :type key: str
        :param default: Default value for the result, can be used as a sentinel.
        :type default: Any
        :param ttl: Optional overwrite ttl value.
        :type ttl: int
        :return: The value stored on the database.
        :rtype: Any
        """

        # Start with the default
        result: Any = default

        # Querying the database for the data.
        cursor: sqlite3.Cursor = self._connection.execute(queries.SQL_GET_KEY_SINCE, (key, self._since(ttl)))
        row = cursor.fetchone()

        if row is not None:  # If there were results, deserialize them using pickle.
            result = pickle.loads(row[0])

        if result is NotSet:  # If result is still NotSet then we have no matches and raise a key (not found) error.
            raise KeyError(key)

        return result

    def set(self, key: str, value: Any, last_seen: Optional[int] = None) -> None:
        """
        Inserting a new value into the cache.
        :param key: The primary key to the key pair value.
        :type key: str
        :param value: The value corresponding to the key.
        :type value: Any
        :param last_seen: Value used for ttl checking.
        :type last_seen: int, optional
        """

        # Get the last_seen time.
        last_seen: Optional[int] = last_seen or self._now()

        # Serialize the data using pickle.
        data: bytes = pickle.dumps(value)

        # Insert the data to the database.
        self._connection.execute(queries.SQL_ADD_UPDATE_KEY, (key, memoryview(data), last_seen))

    def expire(self, key: str) -> None:
        """
        Expire a key belonging to the database.
        :param key: Key that corresponds to the row to expire.
        """

        # Expiring the row by setting the last_seen value to one before now().
        last_seen = self._now() - 1
        self._connection.execute(queries.SQL_UPDATE_KEY_LAST_SEEN, (last_seen, key))

    def delete(self, key: str) -> None:
        """
        Delete the row which has the key specified.
        :param key: Value which row will be deleted.
        """
        self._connection.execute(queries.SQL_DELETE_KEY, (key,))

    def clear(self) -> None:
        """
        Clear the database.
        """
        self._connection.execute(queries.SQL_CLEAR)
