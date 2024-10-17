from sqlalchemy.orm import Mapped, mapped_column

from config.db import Base


class Post(Base):
    __tablename__ = 'posts'