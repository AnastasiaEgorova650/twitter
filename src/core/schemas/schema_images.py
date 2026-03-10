from pydantic import BaseModel, ConfigDict, Field

from src.core.schemas.schema_base import ResponseSchema


class ImageResponseSchema(ResponseSchema):


    id: int = Field(alias="media_id")

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )


class ImagePathSchema(BaseModel):


    path_media: str

    model_config = ConfigDict(from_attributes=True)
