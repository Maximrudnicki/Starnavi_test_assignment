from sqlalchemy.orm import Mapped, mapped_column, relationship

from config.db import Base
from models.post import Post


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[str]
    banned: Mapped[bool] = mapped_column(default=False)
    auto_reply_enabled: Mapped[bool] = mapped_column(default=True)
    auto_reply_delay: Mapped[int] = mapped_column(default=3600)

    posts: Mapped[list["Post"]] = relationship("Post", back_populates="user")
