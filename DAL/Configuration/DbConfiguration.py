# from typing import AsyncGenerator
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# from sqlalchemy.orm import sessionmaker
# from Settings.Settings import LoadConfig

# config = LoadConfig()
# dbHost, dbPort, dbUser, dbPass, dbName = config

# DATABASE_URL = f"postgresql+asyncpg://{dbUser}:{dbPass}@{dbHost}:{dbPort}/{dbName}"

# engine = create_async_engine(DATABASE_URL,echo=True,future=True)
# async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# async def get_session() -> AsyncGenerator[AsyncSession, None]:
#     async with async_session() as session:
#         yield session