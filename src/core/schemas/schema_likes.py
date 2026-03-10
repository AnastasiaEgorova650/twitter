from pydantic import BaseModel, ConfigDict, Field, model_validator


class LikeSchema(BaseModel):


    id: int = Field(alias="user_id")
    username: str = Field(alias="name")

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )

    @model_validator(mode="before")
    def extract_user(cls, data_like):

        user = data_like.user
        return user
