import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pytest

from models.user import User
from repositories.user_repository import UserRepository

def test_create_user_success():
    user_repo = UserRepository()
    user = User(username="testuser", email="test@example.com", password="hashedpassword")
    
    user_id = user_repo.create(user)
    
    assert user_id is not None


def test_create_user_duplicate_email():
    user_repo = UserRepository()
    user1 = User(username="testuser1", email="duplicate@example.com", password="hashedpassword")
    user_repo.create(user1)

    user2 = User(username="testuser2", email="duplicate@example.com", password="hashedpassword")
    
    with pytest.raises(Exception):
        user_repo.create(user2)


def test_get_by_id_success():
    user_repo = UserRepository()
    user = User(username="testuser", email="test@example.com", password="hashedpassword")
    user_id = user_repo.create(user)

    retrieved_user = user_repo.get_by_id(user_id)
    assert retrieved_user is not None
    assert retrieved_user.username == "testuser"

def test_get_by_id_not_found():
    user_repo = UserRepository()
    retrieved_user = user_repo.get_by_id(999)
    assert retrieved_user is None


def test_get_all_users():
    user_repo = UserRepository()
    user1 = User(username="user1", email="user1@example.com", password="hashedpassword")
    user2 = User(username="user2", email="user2@example.com", password="hashedpassword")
    user_repo.create(user1)
    user_repo.create(user2)

    users = user_repo.get_all()
    assert len(users) == 2


def test_update_user_success():
    user_repo = UserRepository()
    user = User(username="testuser", email="test@example.com", password="hashedpassword")
    user_id = user_repo.create(user)

    updates = {
        "username": "updateduser",
        "email": "updated@example.com"
    }
    updated_user = user_repo.update(user_id, updates)

    assert updated_user is not None
    assert updated_user.username == "updateduser"
    assert updated_user.email == "updated@example.com"


def test_update_user_not_found():
    user_repo = UserRepository()
    updates = {
        "username": "updateduser"
    }
    updated_user = user_repo.update(999, updates)
    assert updated_user is None


def test_delete_user_success():
    user_repo = UserRepository()
    user = User(username="testuser", email="test@example.com", password="hashedpassword")
    user_id = user_repo.create(user)

    deleted = user_repo.delete(user_id)
    assert deleted is True
    assert user_repo.get_by_id(user_id) is None


def test_delete_user_not_found():
    user_repo = UserRepository()
    deleted = user_repo.delete(999)
    assert deleted is False

