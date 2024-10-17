from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from router.router import all_routers
from config.config import ALLOWED_ORIGINS


app = FastAPI(title="Test assigment for Starnavi")

for router in all_routers:
    app.include_router(
        router,
        prefix="/api/v1",
    )

origins = [ALLOWED_ORIGINS]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)
