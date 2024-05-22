from fastapi import Depends, FastAPI
from sentence_transformers import SentenceTransformer
import uvicorn
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from DAL.Database.DbConnection import ClosePool, InitPool
from DAL.Database.DbConnectionReranker import ClosePoolRe, InitPoolRe
from Helpers.ConfigLogger import LoggerFactory
from Helpers.TimeMeasure import TimerContextManager
from transformers import AutoTokenizer, pipeline, AutoModelForSequenceClassification
from optimum.onnxruntime import ORTModelForFeatureExtraction
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from Controllers.v1 import FeedbackCollectionController, HybridSearchController, KeywordSearchController, VectorSearchController
from Helpers.Globals import GetFileConsoleLogger, SetFileConsoleLogger, SetModel, SetModelFast, SetRerankModel, SetRerankTokenizer

model = None
modelFast = None
rankingModel = None

def LoadResources():
   global model
   global modelFast
   global rankingModel
   if model is None and modelFast is None and rankingModel is None:
       model = SentenceTransformer(model_name_or_path='DAL\ML_models\gte-base')
       modelFast = ORTModelForFeatureExtraction.from_pretrained("DAL\ML_models\gte-base\onnx")
       tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name_or_path='DAL\ML_models\gte-base\onnx')
       embedder = pipeline("feature-extraction", model=modelFast, tokenizer=tokenizer)
       rankTokenizer = AutoTokenizer.from_pretrained(pretrained_model_name_or_path='DAL\ML_models\ms-marco-MiniLM-L-12-v2')
       rankModel = AutoModelForSequenceClassification.from_pretrained(pretrained_model_name_or_path='DAL\ML_models\ms-marco-MiniLM-L-12-v2')
       SetModel(model)
       SetModelFast(embedder)
       SetRerankModel(rankModel)
       SetRerankTokenizer(rankTokenizer)

@asynccontextmanager
async def lifespan(app: FastAPI):
   with TimerContextManager("Load resources"):
       LoadResources()
   await InitPool()
   await InitPoolRe()
   redis = aioredis.from_url("redis://localhost")
   FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
   SetFileConsoleLogger(LoggerFactory().SetupFileConsoleLogger())
   yield
   await ClosePool()
   await ClosePoolRe()

app = FastAPI(lifespan=lifespan,disable_logger=True)  
# app.middleware("http")(AddProcessTimeHeader)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(VectorSearchController.router, prefix="/api/v1")
app.include_router(HybridSearchController.router, prefix="/api/v1")
app.include_router(KeywordSearchController.router, prefix="/api/v1")
app.include_router(FeedbackCollectionController.router, prefix="/api/v1")

@app.get("/", tags=["Root"], description="Get root endpoint", summary="Root endpoint to check service status")
async def root():
   """
   This endpoint is used to check the status of the service.

   Responses:
       200: Successful request. Returns a dictionary with a single key-value pair,
       where the key is "message" and the value is a string indicating the service status.
   """
   GetFileConsoleLogger().info("testing global")
   return {"message": "Hello From AHS Semantic Search Search!"}

# TODO: Fix this error in red
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8099)#! host and port values does not work,fix it 
