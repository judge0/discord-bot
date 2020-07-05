import asyncio
import asyncpg

from datetime import datetime
import json

from typing import List
from os import environ

CREATE_TABLE_USERS = """
    CREATE TABLE IF NOT EXISTS users (
                discord_id BIGINT NOT NULL,
                PRIMARY KEY (discord_id)
            )
"""

CREATE_TABLE_EXECUTIONS = """
    CREATE TABLE IF NOT EXISTS executions (
                token TEXT NOT NULL,
                user_id BIGINT NOT NULL,
                created_at TIMESTAMP,
                lines_of_code INT,
                PRIMARY KEY (token),
                FOREIGN KEY (user_id) REFERENCES users(discord_id)
            )
"""

CREATE_TABLE_TASKS = """
    CREATE TABLE IF NOT EXISTS tasks (
                task_id TEXT,
                author_id SERIAL,
                created_at TIMESTAMP,
                task JSON,
                PRIMARY KEY (task_id),
                FOREIGN KEY (author_id) REFERENCES authors(author_id)
            )
"""

CREATE_TABLE_SOLUTIONS = """
    CREATE TABLE IF NOT EXISTS solutions (
                solution_id SERIAL,
                user_id BIGINT,
                task_id TEXT,
                test_cases_passed BOOL[], 
                created_at TIMESTAMP,
                lines_of_code INT,
                PRIMARY KEY (solution_id),
                FOREIGN KEY (user_id) REFERENCES users(discord_id),
                FOREIGN KEY (task_id) REFERENCES tasks(task_id)
            )
"""

CREATE_TABLE_AUTHORS = """
    CREATE TABLE IF NOT EXISTS authors (
                author_id SERIAL,
                nickname TEXT NOT NULL UNIQUE,
                icon_url TEXT,
                PRIMARY KEY (author_id)
            )
"""

INSERT_DISCORD_USER = """
    INSERT INTO users (discord_id)
    SELECT $1
    WHERE NOT EXISTS
    (
        SELECT discord_id
        FROM users
        WHERE discord_id = $1
    )
"""

INSERT_AUTHOR = """
    INSERT INTO authors (nickname, icon_url)
    VALUES ($1, $2)
"""  # asyncpg.exceptions.UniqueViolationError:


INSERT_EXECUTION = """
    INSERT INTO executions (user_id, token, created_at, lines_of_code)
    SELECT $1, $2, $3, $4
    WHERE NOT EXISTS
    (
        SELECT token
        FROM executions
        WHERE token = $2
    )
"""

INSERT_TASK = """
    INSERT INTO tasks (task_id, author_id, created_at, task)
    VALUES ($1, $2, $3, $4)
"""

INSERT_SOLUTION = """
    INSERT INTO solutions (user_id, task_id, test_cases_passed, created_at, lines_of_code)
    VALUES ($1, $2, $3, $4, $5)
"""

UPDATE_AUTHOR_NICKNAME = """
    UPDATE authors
    SET nickname = $2
    WHERE nickname = $1
"""

UPDATE_AUTHOR_ICON_URL = """
    UPDATE authors
    SET icon_url = $2
    WHERE icon_url = $1
"""

GET_AUTHOR_ID = """
   SELECT author_id
   FROM authors
   WHERE nickname = $1
   LIMIT 1
""" 

GET_LAST_TASK_ID = """
   SELECT created_at, task_id
   FROM tasks 
   ORDER BY created_at DESC
   LIMIT 1
"""
# GET_LAST_TASK_ID = """
#    SELECT *
#    FROM authors 
# """
def asyncinit(cls):
    """Decorator for an async instantiation of a class."""
    __new__ = cls.__new__

    async def init(obj, *arg, **kwarg):
        await obj.__init__(*arg, **kwarg)
        return obj

    def new(cls, *arg, **kwarg):
        obj = __new__(cls, *arg, **kwarg)
        coro = init(obj, *arg, **kwarg)
        return coro

    cls.__new__ = new
    return cls


@asyncinit
class BotDataBase:
    """
    Represents a interface to the PostgreSQL database.
    """
    async def __init__(self):
        self.conn = await asyncpg.connect(
            user=environ["DB_USER"],
            password=environ["DB_PASS"].strip('"'),
            database=environ["DB_NAME"],
            host="localhost",
        )
        await self.__create_tables()

    async def __create_tables(self) -> None:
        """Initalize the tables of the database if they don't exist."""
        tables_queries = [
            CREATE_TABLE_USERS,
            CREATE_TABLE_AUTHORS,
            CREATE_TABLE_EXECUTIONS,
            CREATE_TABLE_TASKS,
            CREATE_TABLE_SOLUTIONS,
        ]

        for query in tables_queries:
            await self.conn.execute(query)

    async def insert_user(self, discord_id: int) -> None:
        """Inserts a user with discord user id into the database."""
        await self.conn.execute(INSERT_DISCORD_USER, *locals().values())

    async def insert_author(self, nickname: str, icon_url=None) -> None:
        """Inserts an author of task into the database."""
        await self.conn.execute(INSERT_AUTHOR, *locals().values())

    async def insert_execution(
        self, user_id: int, token: str, created_at: datetime, lines_of_code: int
    ) -> None:
        """Insert executed info of passed source code into the database."""
        await self.conn.execute(INSERT_EXECUTION, *locals().values())

    async def insert_solution(
        self,
        user_id: int,
        task_id: str,
        test_cases_passed: List[bool],
        created_at: datetime,
        lines_of_code: int
    ) -> None:
        """Inserts a solution from user to a task into the database."""
        await self.conn.execute(INSERT_SOLUTION, *locals().values())

    async def insert_task(
        self, author_nickname: str, created_at: datetime, task_dict: dict
    ):
        author_id = await self.__get_author_id(author_nickname)
        task_id = await self.__get_last_task_id()
        task = json.dumbs(task)

        # (task_id, author_id, created_at, task)
        args = [task_id, author_id, created_at, task]
        await self.conn.execute(INSERT_EXECUTION, *args)

    async def get_author_id(self, nickname: str) -> int:
        records = await self.conn.fetch(GET_AUTHOR_ID, nickname)
        return records[0].get('author_id')

    async def get_last_task_id(self) -> str:
        records = await self.conn.fetch(GET_LAST_TASK_ID)
        return records[0].get('task_id')

t = r"""
    {
    "title": "Sum two numbers",
    "difficulty": 0,
    "description": "Create a program which takes two numbers as an input and prints their sum.",
    "example": "```Input:\n2\n3\nOutput:\n5```",
    "test_cases": [
      {
        "inputs": [
          "4",
          "5"
        ],
        "output": "9",
        "hidden": false
      },
      {
        "inputs": [
          "1",
          "1"
        ],
        "output": "2",
        "hidden": false
      },
      {
        "inputs": [
          "5",
          "6"
        ],
        "output": "11",
        "hidden": true
      },
      {
        "inputs": [
          "30",
          "20"
        ],
        "output": "50",
        "hidden": true
      },
      {
        "inputs": [
          "0",
          "-5"
        ],
        "output": "-5",
        "hidden": true
      }
    ]
  }"""


async def run():
    db = await BotDataBase()
    ta = await db.get_author_id('otherone')
    print("This", ta)

    # # Insert a record into the created table.
    # await conn.execute('''
    # INSERT INTO users (discord_id)
    # SELECT $1
    # WHERE NOT EXISTS
    # (
    #     SELECT discord_id
    #     FROM users
    #     WHERE discord_id = $1
    # )
    # ''', 365859941292048386)

    # await conn.execute(CREATE_TABLE_SOLUTIONS)
    # await conn.execute(INSERT_SOLUTION, 365859941292048384, '0001', [False, False, False, True, False, True, True], datetime.now(), 159)
    # # await conn.execute(INSERT_EXECUTION,
    # #                    365859941292053646,
    # #                    'd85cd024-1548-4165-0000-7bc88673f142',
    # #                    datetime.now(),
    # #                    123)
    # # # Select a row from the table.
    # row = await conn.fetch(
    #     'SELECT * FROM solutions')
    # # *row* now contains
    # # asyncpg.Record(id=1, name='Bob', dob=datetime.date(1984, 3, 1))
    # # print(row)
    # # row = await conn.fetch(
    # #     'SELECT * FROM tasks')
    # # # *row* now contains
    # # # asyncpg.Record(id=1, name='Bob', dob=datetime.date(1984, 3, 1))
    # print(row)

    # # Close the connection.
    # await conn.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(run())
