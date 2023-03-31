import logging 
from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from .api.routers import holistic_search_api


# instantiate the extensions
def create_app():

    # instantiate the app
    app = FastAPI()

    @app.get("/")
    async def root():
        return {"message": "Hi!"}

    #exception handler 
    @app.exception_handler(StarletteHTTPException)
    async def validation_exception_handler(request: Request, exc: StarletteHTTPException):
        logging.error(f"{exc.detail}")
        return PlainTextResponse(str(exc.detail), status_code=exc.status_code)
    
    app.include_router(holistic_search_api.router) # url = /api/v1/holistic-search
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000", 
            "http://localhost:3001",
            "http://127.0.0.1:8000",
        ],
        # allow_origins=["*"], # allow all origins
        allow_credentials=True, # allow cookies
        allow_methods=["*"], # allow all methods
        allow_headers=["*"], # allow all headers
    )

    return app