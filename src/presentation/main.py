import asyncio

import uvloop
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def build_app() -> FastAPI:
    asyncio.set_event_loop_policy(
        policy=uvloop.EventLoopPolicy()
    )

    app = FastAPI()
    app.add_middleware(
        middleware_class=CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    return app


if __name__ == '__main__':
    uvicorn.run(
        app='src.presentation.main:build_app',
        host='0.0.0.0',
        port=8000,
        factory=True,
        reload=True
    )
