from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from src.graphql.schema import schema
from src.database.session import init_db
app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await init_db()

graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")