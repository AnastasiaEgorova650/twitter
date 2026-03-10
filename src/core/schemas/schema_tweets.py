from http import HTTPStatus
from typing import List, Optional

import loguru
from pydantic import BaseModel, ConfigDict, Field, field_validator
from starlette.exceptions import HTTPException

from src.core.config import LENGTH_TWEET
from src.core.schemas.schema_base import ResponseSchema
from src.core.schemas.schema_images import ImagePathSchema
from src.core.schemas.schema_likes import LikeSchema
from src.core.schemas.schema_users import BaseUserSchema


class TweetOutSchema(BaseModel):


    id: int
    tweet_text: str = Field(
        alias="content",
        default="Белеет мой парус такой одинокий на фоне стальных кораблей.",
    )
    user: BaseUserSchema = Field(alias="author")
    likes: List[LikeSchema]
    images: List[str] = Field(alias="attachments")

    @field_validator("images", mode="before")
    def serialize_images(cls, img_values: List[ImagePathSchema]):
        """
        Возвращаем список строк, ссылкой на изображение
        """
        if isinstance(img_values, list):
            return [img_value.path_media for img_value in img_values]
        loguru.logger.debug(
            f"Путь к картинке ----------------------------> {img_values}"
        )
        return img_values

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )


class TweetInSchema(BaseModel):


    tweet_data: str = Field()
    tweet_media_ids: Optional[list[int]]

    @field_validator("tweet_data", mode="before")
    def check_len_tweet_data(cls, tweet_message: str) -> str | None:

        if len(tweet_message) > LENGTH_TWEET:
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,  # 422
                detail=f"Сообщение не может быть длиннее 280 символов."
                f"Длина сообщения: {len(tweet_message)} символов.",
            )

        return tweet_message

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )


class TweetListSchema(BaseModel):


    tweets: List[TweetOutSchema]


class TweetResponseSchema(ResponseSchema):


    id: int = Field(alias="tweet_id")
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )
