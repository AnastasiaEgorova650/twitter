import json
from http import HTTPStatus

from httpx import AsyncClient

from tests.good_responses import create_tweet, get_result, get_tweets

API_KEY = "api-key"
CONTENT_TYPE = "Content-Type"
APP_JSON = "application/json"


async def test_tweets(ac: AsyncClient):
    response = await ac.get("/api/tweets", headers={API_KEY: "test_1"})
    tweets_data = response.json()
    assert response.status_code == HTTPStatus.OK
    assert tweets_data == get_tweets


async def test_add_new_tweet(ac: AsyncClient):
    response = await ac.post(
        "/api/tweets",
        content=json.dumps(
            {"tweet_data": "Tweet for test", "tweet_media_ids": []}
        ),
        headers={CONTENT_TYPE: APP_JSON, API_KEY: "test_1"},
    )
    new_tweet_data = response.json()
    assert response.status_code == HTTPStatus.CREATED
    assert new_tweet_data == create_tweet


async def test_delete_tweet(ac: AsyncClient):
    response = await ac.delete(
        "/api/tweets/2",
        headers={CONTENT_TYPE: APP_JSON, API_KEY: "test_2"},
    )
    delete_tweet_data = response.json()
    assert response.status_code == HTTPStatus.OK
    assert delete_tweet_data == get_result


async def test_add_tweet_like(ac: AsyncClient):
    response = await ac.post(
        "/api/tweets/1/likes",
        headers={CONTENT_TYPE: APP_JSON, API_KEY: "test_2"},
    )
    like_add_data = response.json()
    assert response.status_code == HTTPStatus.CREATED
    assert like_add_data == get_result


async def test_delete_tweet_like(ac: AsyncClient):
    response = await ac.delete(
        "/api/tweets/1/likes",
        headers={CONTENT_TYPE: APP_JSON, API_KEY: "test_2"},
    )
    like_delete_data = response.json()
    assert response.status_code == HTTPStatus.OK
    assert like_delete_data == get_result
