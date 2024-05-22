from sqlalchemy import Column, Integer, String, Text, TSVECTOR, TIMESTAMP, JSON
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import VECTOR

Base = declarative_base()

class AhsCaDocuments(Base):
    __tablename__ = "ahs_ca_documents"

    id = Column(Integer, primary_key=True)
    pageid = Column(String)
    reference = Column(String)
    title = Column(String)
    description = Column(String)
    keywords = Column(String)
    ahs_searchtitle = Column(String)
    ahs_searchkeywords = Column(String)
    ahs_owner = Column(String)
    referrer = Column(String)
    created = Column(String)
    modified = Column(String)
    published = Column(String)
    content = Column(Text)
    document_with_idx_mutli_column = Column(TSVECTOR)
    last_modified = Column(TIMESTAMP)
    elapsed_days = Column(Integer)

class AhsCaTokenizedEmbeddingsGte(Base):
    __tablename__ = "ahs_ca_tokenized_embeddings_gte"

    id = Column(Integer, primary_key=True)
    ahs_ca_documents = Column(Integer)
    segment_number = Column(Integer)
    chunk = Column(Text)
    embedding = Column(VECTOR(768))
    document_with_idx = Column(TSVECTOR)

class UserFeedback(Base):
    __tablename__ = "user_feedback"

    id = Column(Integer, primary_key=True)
    user_query = Column(Text)
    results = Column(JSON)
    search_type = Column(String)
    result_found = Column(String)
    feedback = Column(String)
    comment = Column(String)
    timestamp = Column(TIMESTAMP)

class UserRequests(Base):
    __tablename__ = "user_requests"

    id = Column(Integer, primary_key=True)
    query_params = Column(Text)
    timestamp = Column(TIMESTAMP)
    client_host = Column(String)
    path = Column(String)
    results = Column(Text)
    status_code = Column(Integer)
    response_time = Column(Integer)