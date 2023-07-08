from fastapi import Depends
from strawberry import Schema
from strawberry.fastapi import GraphQLRouter

from db.session import Session
from .query import Query
from .mutation import Mutation


async def get_db_session():
    session = Session()
    try:
        yield session
    finally:
        session.close


async def get_context(db=Depends(get_db_session)):
    return {"db": db}


schema = Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema, context_getter=get_context)
