from sqlalchemy.orm import Mapped, mapped_column

from config.db import Base


class Comment(Base):
    __tablename__ = 'comments'