import src.db.tables

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import config
from .schema import graphql_app


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", config["CLIENT_URL"], config["ADMIN_URL"]],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(graphql_app, prefix="/graphql")
