import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models.user import User
from models.post import Post
from repositories.user_repository import UserRepository
from repositories.post_repository import PostRepository


def test_create_post_success():
    user_repo = UserRepository()
    user = User(username="testuser", email="test@example.com", password="hashedpassword")
    user_id = user_repo.create(user)

    post_repo = PostRepository()
    post = Post(title="Test Post", text="This is a test post.", author_id=user_id)
    
    post_id = post_repo.create(post)

    assert post_id is not None
    created_post = post_repo.get_by_id(post_id)
    assert created_post.title == "Test Post"
    assert created_post.text == "This is a test post."
    assert created_post.author_id == user_id


def test_get_post_by_id_success():
    user_repo = UserRepository()
    user = User(username="testuser", email="test@example.com", password="hashedpassword")
    user_id = user_repo.create(user)

    post_repo = PostRepository()
    post = Post(title="Test Post", text="This is a test post.", author_id=user_id)
    post_id = post_repo.create(post)

    retrieved_post = post_repo.get_by_id(post_id)
    assert retrieved_post is not None
    assert retrieved_post.title == "Test Post"
    assert retrieved_post.text == "This is a test post."


def test_get_post_by_id_not_found():
    post_repo = PostRepository()
    retrieved_post = post_repo.get_by_id(999)
    assert retrieved_post is None


def test_get_by_author():
    user_repo = UserRepository()
    user1 = User(username="user1", email="user1@example.com", password="hashedpassword")
    user2 = User(username="user2", email="user2@example.com", password="hashedpassword")
    user1_id = user_repo.create(user1)
    user2_id = user_repo.create(user2)

    post_repo = PostRepository()
    post1 = Post(title="Post 1", text="This is post 1.", author_id=user1_id)
    post2 = Post(title="Post 2", text="This is post 2.", author_id=user1_id)
    post_repo.create(post1)
    post_repo.create(post2)

    posts_by_user1 = post_repo.get_by_author(user1_id)
    assert len(posts_by_user1) == 2

    posts_by_user2 = post_repo.get_by_author(user2_id)
    assert len(posts_by_user2) == 0


def test_update_post_success():
    user_repo = UserRepository()
    user = User(username="testuser", email="test@example.com", password="hashedpassword")
    user_id = user_repo.create(user)

    post_repo = PostRepository()
    post = Post(title="Original Title", text="This is a post.", author_id=user_id)
    post_id = post_repo.create(post)

    updates = {
        "title": "Updated Title",
        "text": "This is an updated post."
    }
    updated_post = post_repo.update(post_id, updates)

    assert updated_post is not None
    assert updated_post.title == "Updated Title"
    assert updated_post.text == "This is an updated post."


def test_update_post_not_found():
    post_repo = PostRepository()
    updates = {
        "title": "Updated Title"
    }
    updated_post = post_repo.update(999, updates)
    assert updated_post is None


def test_delete_post_success():
    user_repo = UserRepository()
    user = User(username="testuser", email="test@example.com", password="hashedpassword")
    user_id = user_repo.create(user)

    post_repo = PostRepository()
    post = Post(title="Test Post", text="This is a test post.", author_id=user_id)
    post_id = post_repo.create(post)

    deleted = post_repo.delete(post_id)
    assert deleted is True
    assert post_repo.get_by_id(post_id) is None


def test_delete_post_not_found():
    post_repo = PostRepository()
    deleted = post_repo.delete(999)
    assert deleted is False
