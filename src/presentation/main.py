import asyncio

import uvloop
import uvicorn
from bindme import container
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utilities import add_timer_middleware

from src.presentation.api import setup_rest_controllers
from src.presentation.di import setup_ioc


def build_app() -> FastAPI:
    asyncio.set_event_loop_policy(
        policy=uvloop.EventLoopPolicy()
    )

    setup_ioc(container=container)

    app = FastAPI()
    app.add_middleware(
        middleware_class=CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    setup_rest_controllers(app=app)

    add_timer_middleware(app=app, show_avg=True)

    return app


if __name__ == '__main__':
    uvicorn.run(
        app='src.presentation.main:build_app',
        host='0.0.0.0',
        port=8000,
        factory=True,
        reload=True
    )
