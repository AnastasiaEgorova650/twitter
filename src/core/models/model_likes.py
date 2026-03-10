from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.core.models.model_base import Base


class Like(Base):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )
    tweet_id: Mapped[int] = mapped_column(
        ForeignKey("tweets.id", ondelete="CASCADE")
    )

    def __repr__(self):
        return (
            f"Like(id={self.id}, user_id={self.user_id}, "
            f"tweet_id={self.tweet_id})"
        )

    __mapper_args__ = {"confirm_deleted_rows": False}
