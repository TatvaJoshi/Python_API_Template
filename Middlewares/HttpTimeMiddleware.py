import time
from typing import Any
from fastapi import Depends, Request
from fastapi.responses import JSONResponse
from DAL.Database.DbConnection import GetDb
from datetime import datetime
from fastapi.concurrency import IterateInThreadpool

async def AddProcessTimeHeader(request: Request, callNext):
   if request.scope["path"] == "/":
       response = await callNext(request)
       return response

   if request.method != "POST":
       try:
           startTime = time.time()
           response = await callNext(request)
           processTime = time.time() - startTime
           # fileConsoleLogger().critical("a testing error in middleware occured:",e)
           return response
       except Exception as e:
           # Handle exceptions here
           # fileConsoleLogger().critical("an error in middleware occured:",e)
           return JSONResponse(status_code=500, content={"message": "Internal Server Error"})
       finally:
           if response.statusCode == 200:
               responseBody = [chunk async for chunk in response.bodyIterator]
               response.bodyIterator = IterateInThreadpool(iter(responseBody))
               async with GetDb() as conn:
                   await conn.execute(""" INSERT INTO user_requests (query_params, timestamp, client_host, path, results, status_code, response_time) VALUES ($1, $2, $3, $4, $5, $6, $7) """, str(dict(request.queryParams)), datetime.now(), request.client.host, request.url.path, (b''.join(responseBody)).decode("utf-8"), response.statusCode, processTime)
           else:
               response = await callNext(request)
               return response