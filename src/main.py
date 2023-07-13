import uvicorn
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware

import db.tables
from config import config, is_dev
from schema import graphql_app
import core.file.upload as upload_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", config["CLIENT_URL"], config["ADMIN_URL"]],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(graphql_app, prefix="/graphql")
app.include_router(upload_router.router, prefix="/file")

if __name__ == "__main__":
    host = str(config["HOST"])
    port = int(str(config["PORT"]))

    uvicorn.run(app="main:app", host=host, port=port, reload=is_dev())
