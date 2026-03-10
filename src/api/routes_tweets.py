from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.crud.crud_tweets import (
    add_like_to_tweet,
    create_tweet,
    delete_like_by_tweet,
    delete_tweet_from_db,
    get_all_tweets,
)
from src.api.crud.crud_users import get_current_user
from src.core.config import API_KEY_DEFAULT, MODEL
from src.core.models.db_helper import db_helper
from src.core.models.model_users import User
from src.core.schemas.schema_base import (
    ErrorResponseSchema,
    LockedResponseSchema,
    ResponseSchema,
    UnauthorizedResponseSchema,
    ValidationResponseSchema,
)
from src.core.schemas.schema_tweets import (
    TweetInSchema,
    TweetListSchema,
    TweetResponseSchema,
)

tweets_route = APIRouter(prefix="/api/tweets", tags=["Работа с твитами"])


@tweets_route.get(
    "",
    status_code=HTTPStatus.OK,
    response_model=TweetListSchema,
    responses={401: {MODEL: UnauthorizedResponseSchema}},
)
async def get_tweets_follow_user(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    current_user: Annotated[User, Depends(get_current_user)],
    api_key: Annotated[str | None, Header()] = API_KEY_DEFAULT,
):
    tweets = await get_all_tweets(session=session, current_user=current_user)
    return {"tweets": tweets}


@tweets_route.post(
    "",
    status_code=HTTPStatus.CREATED,
    response_model=TweetResponseSchema,
    responses={
        401: {MODEL: UnauthorizedResponseSchema},
        422: {MODEL: ValidationResponseSchema},
    },
)
async def create_new_tweet(
    tweet: TweetInSchema,
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    current_user: Annotated[User, Depends(get_current_user)],
    api_key: Annotated[str | None, Header()] = API_KEY_DEFAULT,
):
    new_tweet = await create_tweet(
        tweet=tweet, current_user=current_user, session=session
    )
    return {"tweet_id": new_tweet.id}


@tweets_route.delete(
    "/{tweet_id}",
    status_code=HTTPStatus.OK,
    response_model=ResponseSchema,
    responses={
        401: {MODEL: UnauthorizedResponseSchema},
        404: {MODEL: ErrorResponseSchema},
        422: {MODEL: ValidationResponseSchema},
        423: {MODEL: LockedResponseSchema},
    },
)
async def delete_tweet(
    tweet_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    current_user: Annotated[User, Depends(get_current_user)],
    api_key: Annotated[str | None, Header()] = API_KEY_DEFAULT,
):
    await delete_tweet_from_db(tweet_id, session, current_user)
    return {"result": True}


@tweets_route.post(
    "/{tweet_id}/likes",
    status_code=HTTPStatus.CREATED,
    response_model=ResponseSchema,
    responses={
        401: {MODEL: UnauthorizedResponseSchema},
        404: {MODEL: ErrorResponseSchema},
        422: {MODEL: ValidationResponseSchema},
        423: {MODEL: LockedResponseSchema},
    },
)
async def add_like(
    tweet_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    current_user: Annotated[User, Depends(get_current_user)],
    api_key: Annotated[str | None, Header()] = API_KEY_DEFAULT,
):
    await add_like_to_tweet(
        user=current_user, tweet_id=tweet_id, session=session
    )
    return {"result": True}


@tweets_route.delete(
    "/{tweet_id}/likes",
    response_model=ResponseSchema,
    responses={
        401: {MODEL: UnauthorizedResponseSchema},
        404: {MODEL: ErrorResponseSchema},
        422: {MODEL: ValidationResponseSchema},
        423: {MODEL: LockedResponseSchema},
    },
)
async def delete_like(
    tweet_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    current_user: Annotated[User, Depends(get_current_user)],
    api_key: Annotated[str | None, Header()] = API_KEY_DEFAULT,
):
    await delete_like_by_tweet(
        user=current_user, tweet_id=tweet_id, session=session
    )
    return {"result": True}
