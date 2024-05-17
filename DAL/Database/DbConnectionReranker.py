from contextlib import asynccontextmanager
import asyncpg
from Settings.Settings import LoadConfig

config = LoadConfig()
dbHost, dbPort, dbUser, dbPass, dbName = config
pool = None

async def InitPoolRe():
   global pool
   pool = await asyncpg.create_pool(
       user=dbUser, password=dbPass, host=dbHost, port=dbPort, database=dbName, min_size=5, max_size=20
   )

async def ClosePoolRe():
   global pool
   await pool.close()

@asynccontextmanager
async def GetDbRerank():
   async with pool.acquire() as conn:
       try:
           yield conn
       finally:
           pass