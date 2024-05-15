from Helpers.globals import get_model, get_model_fast, get_rerank_model, get_rerank_tokenizer
from Helpers.old_utility.logger import get_console_logger, get_file_logger
from fastapi import HTTPException


# TODO: Adding classes here instead using raw functions to improve structure of the code.
async def get_model_dependency():
    try:
        model = get_model()
        return model
    except Exception as e:
        get_console_logger.critical(e)
        get_file_logger.critical(e)
        raise HTTPException(status_code=500, detail=str(e))

async def get_model_fast_dependency():
    try:
        model_fast = get_model_fast()
        return model_fast
    except Exception as e:
        get_console_logger.critical(e)
        get_file_logger.critical(e)
        raise HTTPException(status_code=500, detail=str(e))

async def get_rerank_tokenizer_dependency():
    try:
        rerank_tokenizer = get_rerank_tokenizer()
        return rerank_tokenizer
    except Exception as e:
        get_console_logger().critical(e)
        get_file_logger().critical(e)
        raise HTTPException(status_code=500, detail=str(e))


async def get_reranker_model_dependency():
    try:
        reranker = get_rerank_model()
        return reranker
    except Exception as e:
        get_console_logger().critical(e)
        get_file_logger().critical(e)
        raise HTTPException(status_code=500, detail=str(e))

