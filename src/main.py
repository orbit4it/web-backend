import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

import db.tables # pyright: ignore
from config import config, is_dev
from schema import graphql_app

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", config["CLIENT_URL"], config["ADMIN_URL"]],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(graphql_app, prefix="/graphql")

if __name__ == "__main__":
    host = str(config["HOST"])
    port = int(str(config["PORT"]))
    workers = int(str(config["WORKERS"]))

    uvicorn.run(
        app="main:app",
        host=host,
        port=port,
        workers=workers,
        reload=is_dev(),
        log_config="log.ini",
        ssl_certfile=config.get("SSL_CERTFILE"),
        ssl_keyfile=config.get("SSL_KEYFILE"),
    )
