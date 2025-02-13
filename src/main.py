from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from contextlib import asynccontextmanager
from src.graphql.schema import schema
from src.database.session import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manejo correcto del ciclo de vida de la app"""
    await init_db()
    yield
    print("App shutting down...")

app = FastAPI(lifespan=lifespan)

graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")
