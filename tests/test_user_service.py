import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from unittest.mock import MagicMock
from services.user_service import UserService
from models.user import User
from repositories.user_repository import UserRepository
from fastapi import HTTPException


@pytest.fixture
def user_repository_mock():
    return MagicMock(spec=UserRepository)


@pytest.fixture
def user_service(user_repository_mock):
    return UserService(user_repository=user_repository_mock)


def test_create_user_success(user_service, user_repository_mock):
    user_repository_mock.create.return_value = 1 

    user_id = user_service.create_user("testuser", "test@example.com", "hashedpassword")
    
    assert user_id == 1
    user_repository_mock.create.assert_called_once()


def test_create_user_duplicate_email(user_service, user_repository_mock):
    user_repository_mock.create.side_effect = HTTPException(status_code=400, detail="Email already registered.")
    
    with pytest.raises(HTTPException) as exc_info:
        user_service.create_user("testuser", "duplicate@example.com", "hashedpassword")
    
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Email already registered."


def test_login_success(user_service, user_repository_mock):
    user = User(username="testuser", email="test@example.com", password="hashedpassword")
    user_repository_mock.get_by_email.return_value = user
    user_service.pwd_context.verify = lambda password, hashed: password == "hashedpassword" 

    token = user_service.login("test@example.com", "hashedpassword")
    
    assert token["access_token"] is not None
    assert token["token_type"] == "bearer"


def test_login_user_not_found(user_service, user_repository_mock):
    user_repository_mock.get_by_email.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        user_service.login("nonexistent@example.com", "password")
    
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "User not found."


def test_login_user_banned(user_service, user_repository_mock):
    user = User(username="testuser", email="test@example.com", password="hashedpassword", is_banned=True)
    user_repository_mock.get_by_email.return_value = user
    user_service.pwd_context.verify = lambda password, hashed: password == "hashedpassword"

    with pytest.raises(HTTPException) as exc_info:
        user_service.login("test@example.com", "hashedpassword")
    
    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "User is banned."


def test_get_by_id_success(user_service, user_repository_mock):
    user = User(username="testuser", email="test@example.com", password="hashedpassword")
    user_repository_mock.get_by_id.return_value = user

    retrieved_user = user_service.get_by_id(1)

    assert retrieved_user == user
    user_repository_mock.get_by_id.assert_called_once_with(1)


def test_update_user_success(user_service, user_repository_mock):
    user = User(username="testuser", email="test@example.com", password="hashedpassword")
    user_repository_mock.get_by_id.return_value = user
    updates = {"username": "updateduser"}

    user_repository_mock.update.return_value = User(username="updateduser", email="test@example.com", password="hashedpassword")

    updated_user = user_service.update_user(1, updates)

    assert updated_user.username == "updateduser"
    user_repository_mock.update.assert_called_once_with(1, updates)



def test_delete_user_success(user_service, user_repository_mock):
    user_repository_mock.delete.return_value = True

    deleted = user_service.delete_user(1)

    assert deleted is True
    user_repository_mock.delete.assert_called_once_with(1)


def test_ban_user_success(user_service, user_repository_mock):
    user_repository_mock.update.return_value = User(is_banned=True)

    banned_user = user_service.ban_user(1)

    assert banned_user.is_banned is True
    user_repository_mock.update.assert_called_once_with(1, {'is_banned': True})
