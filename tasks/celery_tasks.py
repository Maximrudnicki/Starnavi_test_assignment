from sqlalchemy.orm import configure_mappers
from models import Comment, Post, User

configure_mappers()

from celery import Celery

from repositories.comment_repository import CommentRepository
from repositories.post_repository import PostRepository


celery = Celery("tasks", broker="redis://redis:6379/0", backend="redis://redis:6379/0")


@celery.task
def auto_reply(post_id, reply_text=None):
    comment_repo = CommentRepository()
    post_repo = PostRepository()

    post = post_repo.get_by_id(post_id)
    reply = Comment(post_id=post.id, user_id=post.author_id, text=reply_text)
    comment_repo.create(reply)
