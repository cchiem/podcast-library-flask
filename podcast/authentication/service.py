from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import User
from werkzeug.security import generate_password_hash, check_password_hash


class NameNotUniqueException(Exception):
    pass


class UnknownUserException(Exception):
    pass


class AuthenticationException(Exception):
    pass


def add_user(repo: AbstractRepository, user_name: str, password: str):
    user = repo.get_user(user_name)
    if user is not None:
        raise NameNotUniqueException
    password_hash = generate_password_hash(password)
    user = User(repo.get_new_user_id(), user_name, password_hash)
    repo.add_user(user)


def get_user(repo: AbstractRepository, user_name: str):
    user = repo.get_user(user_name)
    if user is None:
        raise UnknownUserException

    return user_to_dict(user)


def authenticate_user(user_name: str, password: str, repo: AbstractRepository):
    authenticated = False

    user = repo.get_user(user_name)
    if user is not None:
        authenticated = check_password_hash(user.password, password)
    if not authenticated:
        raise AuthenticationException


def user_to_dict(user: User):
    return {
        'username': user.username,
        'password': user.password
    }
