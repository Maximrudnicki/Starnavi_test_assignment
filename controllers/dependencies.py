from services.user_service import UserService
from services.post_service import PostService
from services.comment_service import CommentService

from repositories.user_repository import UserRepository
from repositories.post_repository import PostRepository
from repositories.comment_repository import CommentRepository


def get_user_service():
    user_repository = UserRepository()
    return UserService(user_repository)


def get_post_service():
    post_repository = PostRepository()
    return PostService(post_repository)


def get_comment_service():
    comment_repository = CommentRepository()
    return CommentService(comment_repository)
