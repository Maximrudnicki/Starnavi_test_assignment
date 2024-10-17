import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models.user import User
from models.post import Post
from models.comment import Comment
from repositories.user_repository import UserRepository
from repositories.post_repository import PostRepository
from repositories.comment_repository import CommentRepository


def test_create_comment_success():
    user_repo = UserRepository()
    user = User(
        username="testuser", email="test@example.com", password="hashedpassword"
    )
    user_id = user_repo.create(user)

    post_repo = PostRepository()
    post = Post(title="Test Post", text="This is a test post.", author_id=user_id)
    post_id = post_repo.create(post)

    comment_repo = CommentRepository()
    comment = Comment(post_id=post_id, user_id=user_id, text="This is a test comment.")
    comment_id = comment_repo.create(comment)

    assert comment_id is not None
    created_comment = comment_repo.get_by_id(comment_id)
    assert created_comment.text == "This is a test comment."
    assert created_comment.post_id == post_id
    assert created_comment.user_id == user_id


def test_get_comment_by_id_success():
    user_repo = UserRepository()
    user = User(
        username="testuser", email="test@example.com", password="hashedpassword"
    )
    user_id = user_repo.create(user)

    post_repo = PostRepository()
    post = Post(title="Test Post", text="This is a test post.", author_id=user_id)
    post_id = post_repo.create(post)

    comment_repo = CommentRepository()
    comment = Comment(post_id=post_id, user_id=user_id, text="This is a test comment.")
    comment_id = comment_repo.create(comment)

    retrieved_comment = comment_repo.get_by_id(comment_id)
    assert retrieved_comment is not None
    assert retrieved_comment.text == "This is a test comment."


def test_get_comment_by_id_not_found():
    comment_repo = CommentRepository()
    retrieved_comment = comment_repo.get_by_id(999)
    assert retrieved_comment is None


def test_get_comments_by_post_success():
    user_repo = UserRepository()
    user = User(
        username="testuser", email="test@example.com", password="hashedpassword"
    )
    user_id = user_repo.create(user)

    post_repo = PostRepository()
    post = Post(title="Test Post", text="This is a test post.", author_id=user_id)
    post_id = post_repo.create(post)

    comment_repo = CommentRepository()
    comment1 = Comment(
        post_id=post_id, user_id=user_id, text="This is a test comment 1."
    )
    comment2 = Comment(
        post_id=post_id, user_id=user_id, text="This is a test comment 2."
    )
    comment_repo.create(comment1)
    comment_repo.create(comment2)

    comments_by_post = comment_repo.get_by_post(post_id)
    assert len(comments_by_post) == 2


def test_update_comment_success():
    user_repo = UserRepository()
    user = User(
        username="testuser", email="test@example.com", password="hashedpassword"
    )
    user_id = user_repo.create(user)

    post_repo = PostRepository()
    post = Post(title="Test Post", text="This is a test post.", author_id=user_id)
    post_id = post_repo.create(post)

    comment_repo = CommentRepository()
    comment = Comment(post_id=post_id, user_id=user_id, text="Original comment text.")
    comment_id = comment_repo.create(comment)

    updates = {"text": "Updated comment text."}
    updated_comment = comment_repo.update(comment_id, updates)

    assert updated_comment is not None
    assert updated_comment.text == "Updated comment text."


def test_update_comment_not_found():
    comment_repo = CommentRepository()
    updates = {"text": "This won't work."}
    updated_comment = comment_repo.update(999, updates)
    assert updated_comment is None


def test_delete_comment_success():
    user_repo = UserRepository()
    user = User(
        username="testuser", email="test@example.com", password="hashedpassword"
    )
    user_id = user_repo.create(user)

    post_repo = PostRepository()
    post = Post(title="Test Post", text="This is a test post.", author_id=user_id)
    post_id = post_repo.create(post)

    comment_repo = CommentRepository()
    comment = Comment(
        post_id=post_id, user_id=user_id, text="This comment will be deleted."
    )
    comment_id = comment_repo.create(comment)

    deleted = comment_repo.delete(comment_id)
    assert deleted is True
    assert comment_repo.get_by_id(comment_id) is None


def test_delete_comment_not_found():
    comment_repo = CommentRepository()
    deleted = comment_repo.delete(999)
    assert deleted is False
