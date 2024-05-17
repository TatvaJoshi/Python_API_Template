from fastapi import HTTPException
from Helpers.Globals import GetModel, GetModelFast, GetRerankModel, GetRerankTokenizer
from Helpers.ConfigLogger import LoggerFactory

# TODO: Adding classes here instead using raw functions to improve structure of the code.
async def GetModelDependency():
    try:
        model = GetModel()
        return model
    except Exception as e:
        LoggerFactory().SetupFileConsoleLogger().critical(e)
        raise HTTPException(status_code=500, detail=str(e))

async def GetModelFastDependency():
    try:
        modelFast = GetModelFast()
        return modelFast
    except Exception as e:
        LoggerFactory().SetupFileConsoleLogger().critical(e)
        raise HTTPException(status_code=500, detail=str(e))

async def GetRerankTokenizerDependency():
    try:
        rerankTokenizer = GetRerankTokenizer()
        return rerankTokenizer
    except Exception as e:
        LoggerFactory().SetupFileConsoleLogger().critical(e)
        raise HTTPException(status_code=500, detail=str(e))


async def GetRerankerModelDependency():
    try:
        reranker = GetRerankModel()
        return reranker
    except Exception as e:
        LoggerFactory().SetupFileConsoleLogger().critical(e)
        raise HTTPException(status_code=500, detail=str(e))

