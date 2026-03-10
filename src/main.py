from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api import routes_medias, routes_tweets, routes_users
from src.api.crud.insert_data_in_tables import create_tables
from src.core.models.db_helper import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Чтобы база данных не создавалась заново нужно закомментировать эту строчку
    await create_tables()
    yield
    await db_helper.dispose()


main_app = FastAPI(lifespan=lifespan)
main_app.include_router(routes_users.users_route)
main_app.include_router(routes_tweets.tweets_route)
main_app.include_router(routes_medias.medias_route)
