from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from api.utils import AppException, app_exception_manager, default_exception_manager
from api.v1 import v1_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    pass


app = FastAPI(debug=False, lifespan=lifespan)

app.add_exception_handler(AppException, app_exception_manager)
app.add_exception_handler(Exception, default_exception_manager)

app.include_router(v1_router)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8014,
    )
