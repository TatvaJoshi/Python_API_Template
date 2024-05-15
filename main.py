from typing import Any
from fastapi import Depends, FastAPI
from loguru import logger
from sentence_transformers import SentenceTransformer
import uvicorn
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
# from Helpers.config_logger import setup_console_logger
from BAL.Dependencies.logger_dependencies import ConsoleLoggerDependency, FileLoggerDependency
from Helpers.config_logger import LoggerFactory
from Helpers.time_measure import TimerContextManager
from Helpers.globals import get_file_console_logger, set_file_console_logger, set_model,set_model_fast,set_reranker_model,set_rerank_tokenizer
from DAL.Database.db_connection_reranker import init_pool_re,close_pool_re
from transformers import AutoTokenizer, pipeline, AutoModelForSequenceClassification
from optimum.onnxruntime import ORTModelForFeatureExtraction
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
# from Middlewares.process_time_middleware import add_process_time_header
from Controllers.v1 import vector_search,hybrid_search,keyword_search,feedback_collection
from DAL.Database.db_connection import init_pool,close_pool
from Middlewares.process_time_middleware import AddProcessTimeHeader

model = None
model_fast=None
ranking_model=None

def load_resources():
    global model
    global model_fast
    global ranking_model
    if model is None and model_fast is None and ranking_model is None:
        model = SentenceTransformer(model_name_or_path='DAL\ML_models\gte-base')
        model_fast = ORTModelForFeatureExtraction.from_pretrained("DAL\ML_models\gte-base\onnx") # ONNX checkpoint
        tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name_or_path='DAL\ML_models\gte-base\onnx')
        embedder = pipeline("feature-extraction",model=model_fast,tokenizer=tokenizer)
        rank_tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name_or_path='DAL\ML_models\ms-marco-MiniLM-L-12-v2')
        rank_model = AutoModelForSequenceClassification.from_pretrained(pretrained_model_name_or_path='DAL\ML_models\ms-marco-MiniLM-L-12-v2')
        set_model(model)
        set_model_fast(embedder)
        set_reranker_model(rank_model)
        set_rerank_tokenizer(rank_tokenizer)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    with TimerContextManager("Load resources"):
        load_resources()
    await init_pool()
    await init_pool_re()
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    set_file_console_logger(LoggerFactory().setup_file_console_logger())
    yield
    await close_pool()
    await close_pool_re()

app = FastAPI(lifespan=lifespan,disable_logger=True)  
app.middleware("http")(AddProcessTimeHeader)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(vector_search.router, prefix="/api/v1")
app.include_router(hybrid_search.router, prefix="/api/v1")
app.include_router(keyword_search.router, prefix="/api/v1")
app.include_router(feedback_collection.router, prefix="/api/v1")

@app.get("/", tags=["Root"], description="Get root endpoint", summary="Root endpoint to check service status")
async def root():#email_handler: NotificationHandler = Depends(get_email_handler("tatvajoshi0@gmail.com", "tjj972024", "tatva.joshi@albertahealthservices.ca")),
    """
    This endpoint is used to check the status of the service.

    Responses:
        200: Successful request. Returns a dictionary with a single key-value pair,
        where the key is "message" and the value is a string indicating the service status.
    """
    get_file_console_logger().info("testing global")
    return {"message": "Hello From AHS Semantic Search Search!"}

# TODO: Fix this error in red
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8099)#! host and port values does not work,fix it 
