import logging
import os

import sqlalchemy as sa
from sqlalchemy.engine.url import make_url
from sqlalchemy.exc import OperationalError, ProgrammingError
from pymongo import MongoClient
from pymongo import errors as MongoErrors
from motor.motor_asyncio import AsyncIOMotorClient


from madmigration.utils.helpers import generate_database_details
from madmigration.errors import UnsupportedDatabase
from .database_enum import DatabaseTypes

def _get_scalar_result(engine, sql_text):
    with engine.connect() as conn:
        return conn.scalar(sql_text)

def run_database_exist_check(url: str, sql_text: str):
    try:
        engine = sa.create_engine(url)
        return bool(_get_scalar_result(engine, sql_text))
    except (ProgrammingError, OperationalError):
        return False
    finally:
        if engine:
            engine.dispose()

def confirm_psql_database(url: str):
    def inner(database: str):
        sql_text = "SELECT 1 FROM pg_database WHERE datname='%s'" % database
        return run_database_exist_check(url, sql_text)
    return inner

def confirm_mysql_database(url: str):
    def inner(database: str):
        sql_text = ("SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA "
                        "WHERE SCHEMA_NAME = '%s'" % database)
        return run_database_exist_check(url, sql_text)
    return inner

def generic_confirm_database(url):
    def inner(database):
        logging.info(database)

        sql_text = 'SELECT 1'
        return run_database_exist_check(url, sql_text)
    return inner

def confirm_sqlite_database(url):
    def inner(database):
        logging.info(url)
        if not os.path.isfile(database) or os.path.getsize(database) < 100:
            return False

        with open(database, 'rb') as f:
            header = f.read(100)
        return header[:16] == b'SQLite format 3\x00'
    return inner

def confirm_mongo_database(url):
    def inner(database):
        logging.info(f'checking database {database}')
        try:
            client = MongoClient(url)
            client.server_info()
            return True
        except MongoErrors.ServerSelectionTimeoutError:
            return False
        except MongoErrors.ConnectionFailure:
            return False
    return inner

def confirm_database_strategy(url):
    details = generate_database_details(url)
    database = details.database

    strategies = {
        DatabaseTypes.POSTGRES: confirm_psql_database(url),
        DatabaseTypes.MYSQL: confirm_mysql_database(url),
        DatabaseTypes.MSSQL: generic_confirm_database(url),
        DatabaseTypes.MONGODB: confirm_mongo_database(url),
        DatabaseTypes.SQLITE: generic_confirm_database(url)
    }

    strategy = strategies.get(details.dialect_name, None)
    if strategy is None:
        raise UnsupportedDatabase('Migration database provided is currently unsupported in mad migration')
    return strategy(database)
    

async def _async_get_scalar_result(engine, sql_text):
    async with engine.connect() as conn:
        return await conn.scalar(sql_text)

async def async_run_database_exist_check(url: str, sql_text: str):
    try:
        engine = sa.create_engine(url)
        return bool(await _async_get_scalar_result(engine, sql_text))
    except (ProgrammingError, OperationalError):
        return False
    finally:
        if engine:
            engine.dispose()

def async_confirm_psql_database(url: str):
    async def inner(database: str):
        sql_text = "SELECT 1 FROM pg_database WHERE datname='%s'" % database
        return await async_run_database_exist_check(url, sql_text)
    return inner

def async_confirm_mysql_database(url: str):
    async def inner(database: str):
        sql_text = ("SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA "
                        "WHERE SCHEMA_NAME = '%s'" % database)
        return await async_run_database_exist_check(url, sql_text)
    return inner

def async_generic_confirm_database(url):
    async def inner(database):
        logging.info(database)

        sql_text = 'SELECT 1'
        return await async_run_database_exist_check(url, sql_text)
    return inner

def async_confirm_sqlite_database(url):
    async def inner(database):
        logging.info(url)
        if not os.path.isfile(database) or os.path.getsize(database) < 100:
            return False

        with open(database, 'rb') as f:
            header = f.read(100)
        return header[:16] == b'SQLite format 3\x00'
    return inner

def async_confirm_mongo_database(url):
    async def inner(database):
        logging.info(f'checking database {database}')
        try:
            client = AsyncIOMotorClient(url)
            await client.server_info()
            return True
        except Exception:
            return False
    return inner

async def async_confirm_database_strategy(url):
    details = generate_database_details(url)
    database = details.database

    strategies = {
        DatabaseTypes.POSTGRES: async_confirm_psql_database(url),
        DatabaseTypes.MYSQL: async_confirm_mysql_database(url),
        DatabaseTypes.MSSQL: async_generic_confirm_database(url),
        DatabaseTypes.MONGODB: async_confirm_mongo_database(url),
        DatabaseTypes.SQLITE: async_generic_confirm_database(url)
    }

    strategy = strategies.get(details.dialect_name, None)
    if strategy is None:
        raise UnsupportedDatabase('Migration database provided is currently unsupported in mad migration')
    return await strategy(database)