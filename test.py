import asyncio
from typing import AsyncGenerator, List, Tuple
from fastapi import Depends, FastAPI
import sqlalchemy
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import TIMESTAMP, MetaData, Table, Column, Integer, String, Text, create_engine, func, select
from pgvector.sqlalchemy import Vector
from sentence_transformers import SentenceTransformer
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.dialects.postgresql import TSVECTOR
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import uvicorn
from sentence_transformers import SentenceTransformer

# async def get_db_connection():
#     engine = create_async_engine("postgresql+asyncpg://postgres:postgres@localhost:5433/testing_index_vector")
#     metadata = MetaData(bind=engine)
#     my_table = Table('ahs_ca_documents', metadata, autoload = True)

#     my_session = Session(engine)


# class Base(DeclarativeBase):
#     pass
# class AhsCaDocuments(Base):
#     __tablename__ = "ahs_ca_documents"

#     id = Column(Integer, primary_key=True)
#     pageid = Column(String)
#     reference = Column(String)
#     title = Column(String)
#     description = Column(String)
#     keywords = Column(String)
#     ahs_searchtitle = Column(String)
#     ahs_searchkeywords = Column(String)
#     ahs_owner = Column(String)
#     referrer = Column(String)
#     created = Column(String)
#     modified = Column(String)
#     published = Column(String)
#     content = Column(Text)
#     document_with_idx_mutli_column = Column(Vector)
#     last_modified = Column(TIMESTAMP)
#     elapsed_days = Column(Integer)

# class AhsCaTokenizedEmbeddingsGte(Base):
#     __tablename__ = "ahs_ca_tokenized_embeddings_gte"

#     id = Column(Integer, primary_key=True)
#     ahs_ca_documents = Column(Integer)
#     segment_number = Column(Integer)
#     chunk = Column(Text)
#     embedding = Column(Vector(768))
#     document_with_idx = Column(TSVECTOR)


# engine = create_async_engine("postgresql+asyncpg://postgres:postgres@localhost:5433/testing_index_vector")
# async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
# async def get_session() -> AsyncGenerator[AsyncSession, None]:
#     async with async_session() as session:
#         yield session

# app = FastAPI()

# @app.get("/documents")
# async def get_documents(session: AsyncSession = Depends(get_session)):
#     query = select(AhsCaDocuments).limit(1)
#     result = await session.execute(query)
#     return result

# if __name__ == "__main__":
#     uvicorn.run(app, host="localhost", port=8099)#! host and port values does not work,fix it 




engine = create_engine("postgresql://postgres:postgres@localhost:5433/testing_index_vector")
# metadata = MetaData()
# metadata.reflect(engine)
# # Get the reflected table objects
# docs_table = metadata.tables['ahs_ca_documents']
# embs_table = metadata.tables['ahs_ca_tokenized_embeddings_gte']
# Create the session
class Base(DeclarativeBase):
    pass

class EmbeddingsTable(Base):
    __tablename__ = 'ahs_ca_tokenized_embeddings_gte'

    id = Column(Integer, primary_key=True)
    ahs_ca_documents = Column(Integer)
    segment_number = Column(Integer)
    chunk = Column(Text)
    embedding = Column(Vector(768))
    document_with_idx = Column(TSVECTOR)
    
Session = sessionmaker(bind=engine)
session = Session()
# Perform a left join and retrieve the first record
# result = session.query(docs_table, embs_table) \
#                  .outerjoin(embs_table, docs_table.c.id == embs_table.c.ahs_ca_documents) \
#                  .first()
model = SentenceTransformer(model_name_or_path='DAL\ML_models\gte-base')
embedding=model.encode("cancer care alberta")
# results=session.scalars(select([embs_table.c.id,embs_table.c.ahs_ca_documents,embs_table.c.chunk,embs_table.c]).order_by(embs_table.c.embedding.cosine_distance(embedding.tolist())).limit(2)).all()
import time

start_time = time.time()

results=session.scalars(select(EmbeddingsTable).order_by(EmbeddingsTable.embedding.cosine_distance(embedding.tolist())).limit(50)).all()
print("Execution time: %s seconds" % (time.time() - start_time))
for i in results:
    print(i)
