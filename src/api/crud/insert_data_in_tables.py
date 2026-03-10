import datetime

from sqlalchemy import insert

from src.core.models.db_helper import db_helper
from src.core.models.model_base import Base
from src.core.models.model_images import Image
from src.core.models.model_likes import Like
from src.core.models.model_tweets import Tweet
from src.core.models.model_users import User, followers_tbl

# -----------------------------------------------------------------
NAMES = (
    "Анастасия Егорова",
    "Ксения Коновалова",
    "Богдан Павлов",
    "Сара Бурова",
    "Дмитрий Матвеев",
)
API_KEYS = ("test", "konovalova", "pavlov", "burova", "matveev")
USER_DATA = zip(NAMES, API_KEYS)
USER_DATA_TPL = tuple(
    {"name": user[0], "api_key": user[1]} for user in USER_DATA
)

# -----------------------------------------------------------------
TWEET_TEXTS = (
    "Лучше сейчас, чем потом.",
    "Будь в моменте, не в будущем.",
    "Жизнь слишком коротка, чтобы откладывать счастье.",
    "Отпускай, что мешает двигаться дальше.",
    "Кот — это маленький философ, который учит нас наслаждаться настоящим моментом.",
)
USER_IDS = (1, 2, 3, 4, 5)
TWEET_DATA_ZIP = zip(TWEET_TEXTS, USER_IDS)
TWEET_DATA = tuple(
    {
        "tweet_text": tweet[0],
        "user_id": tweet[1],
        "created_at": datetime.datetime.now(),
    }
    for tweet in TWEET_DATA_ZIP
)

# -----------------------------------------------------------------
LIKE_USER_IDS = (1, 2, 3, 1, 2, 1, 1, 2, 3, 4, 5)
LIKE_TWEET_IDS = (2, 2, 2, 3, 3, 4, 5, 5, 5, 5, 5)
LIKE_DATA_ZIP = zip(LIKE_USER_IDS, LIKE_TWEET_IDS)
LIKE_DATA = tuple(
    {"user_id": like[0], "tweet_id": like[1]} for like in LIKE_DATA_ZIP
)

# -----------------------------------------------------------------
FOLLOWED_DATA = (
    {"follower_id": 1, "followed_id": 2},
    {"follower_id": 1, "followed_id": 3},
    {"follower_id": 1, "followed_id": 5},
)

# -----------------------------------------------------------------
IMAGE_DATA = ({"tweet_id": 5, "path_media": "images/112.jpg"},)


async def create_tables():
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        await insert_data(conn)


async def insert_data(conn):
    await conn.execute(insert(User), USER_DATA_TPL)
    await conn.execute(insert(Tweet), TWEET_DATA)
    await conn.execute(insert(Like), LIKE_DATA)
    await conn.execute(insert(followers_tbl), FOLLOWED_DATA)
    await conn.execute(insert(Image), IMAGE_DATA)








