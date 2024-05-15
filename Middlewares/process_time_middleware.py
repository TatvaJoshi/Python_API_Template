import time
from typing import Any
from fastapi import Depends, Request
from fastapi.responses import JSONResponse
from BAL.Dependencies.logger_dependencies import FileConsoleLoggerDependency
from DAL.Database.db_connection import get_db
from datetime import datetime
from fastapi.concurrency import iterate_in_threadpool

async def AddProcessTimeHeader(request: Request, call_next):
    if request.scope["path"] == "/":
        response = await call_next(request)
        return response
    
    if request.method != "POST":
        try:
            start_time = time.time()
            response = await call_next(request)
            process_time = time.time() - start_time
            # file_console_logger().critical("a testing error in middleware occured:",e)
            
            return response
        except Exception as e:
            # Handle exceptions here
            # file_console_logger().critical("an error in middleware occured:",e)
            return JSONResponse(status_code=500, content={"message": "Internal Server Error"})
        finally:
            if response.status_code == 200:
                response_body = [chunk async for chunk in response.body_iterator]
                response.body_iterator = iterate_in_threadpool(iter(response_body))
                async with get_db() as conn:
                    await conn.execute("""
                            INSERT INTO user_requests (query_params, timestamp, client_host, path, results, status_code, response_time)
                            VALUES ($1, $2, $3, $4, $5, $6, $7)
                        """, str(dict(request.query_params)), datetime.now(), request.client.host,request.url.path, (b''.join(response_body)).decode("utf-8"), response.status_code, process_time)

    else:
        response = await call_next(request)
        return response
