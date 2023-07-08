from fastapi import Depends
from strawberry import Schema, extensions
from strawberry.fastapi import GraphQLRouter
from strawberry.extensions import AddValidationRules
from graphql.validation import NoSchemaIntrospectionCustomRule

from db.session import Session
from config import config, is_dev
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


extensions = []
if not is_dev():
    extensions = [
        AddValidationRules([NoSchemaIntrospectionCustomRule])
    ]


schema = Schema(
    query=Query,
    mutation=Mutation,
    extensions=extensions
)


graphql_app = GraphQLRouter(
    schema,
    context_getter=get_context,
    graphiql=is_dev()
)
