import asyncio
import asyncpg

from datetime import datetime
import json

from os import environ

class BotDataBase:
    def __init__(self):
        pass 

    def create(self):
        pass

    def insert(self):
        pass

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
""" # asyncpg.exceptions.UniqueViolationError:


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
async def run():
    conn = await asyncpg.connect(user=environ['DB_USER'], password=environ['DB_PASS'].strip('"'),
                                 database=environ['DB_NAME'], host='localhost')

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

    await conn.execute(CREATE_TABLE_SOLUTIONS)
    await conn.execute(INSERT_SOLUTION, 365859941292048384, '0001', [False, False, False, True, False, True, True], datetime.now(), 159)
    # await conn.execute(INSERT_EXECUTION, 
    #                    365859941292053646, 
    #                    'd85cd024-1548-4165-0000-7bc88673f142',
    #                    datetime.now(),
    #                    123)
    # # Select a row from the table.
    row = await conn.fetch(
        'SELECT * FROM solutions')
    # *row* now contains
    # asyncpg.Record(id=1, name='Bob', dob=datetime.date(1984, 3, 1))
    # print(row)
    # row = await conn.fetch(
    #     'SELECT * FROM tasks')
    # # *row* now contains
    # # asyncpg.Record(id=1, name='Bob', dob=datetime.date(1984, 3, 1))
    print(row)

    # Close the connection. 
    await conn.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(run())