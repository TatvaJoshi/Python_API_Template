from contextlib import asynccontextmanager
import asyncpg

from DAL.Models.settings import load_config
# @asynccontextmanager
# async def get_db():
#     try:
#         db_type,db_host,db_port,db_user,db_pass,db_name = load_config()
#     except KeyError as e:
#         raise Exception(f"Missing configuration value: {e}")

#     try:
#         conn = await asyncpg.connect(user=db_user, password=db_pass,
#                                       port=db_port, host=db_host,
#                                       database=db_name)
#     except asyncpg.PostgresError as e:
#         raise Exception(f"Error connecting to the database: {e}")

#     try:
#         yield conn
#     finally:
#         await conn.close()

config = load_config()
db_host,db_port,db_user,db_pass,db_name = config

pool = None

async def init_pool():
    global pool
    pool = await asyncpg.create_pool(
        user=db_user,
        password=db_pass,
        host=db_host,
        port=db_port,
        database=db_name,
        min_size=5,
        max_size=20
    )

async def close_pool():
    global pool
    await pool.close()

@asynccontextmanager
async def get_db():
    async with pool.acquire() as conn:
        try:
            yield conn
        finally:
            pass