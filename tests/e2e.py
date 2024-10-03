import os
import pytest
from podcast import create_app
from podcast.adapters.memory_repository import MemoryRepository, populate
from utils import get_project_root
from podcast import CSVDataReader
from podcast.domainmodel.model import Episode
from podcast.adapters.memory_repository import MemoryRepository, populate
from utils import get_project_root
from podcast.domainmodel.model import *
from werkzeug.security import generate_password_hash, check_password_hash

# Path to test data
TEST_DATA_PATH = get_project_root() / "tests" / "data"

@pytest.fixture
def in_memory_repo():
    repo = MemoryRepository()
    populate(repo, True)
    return repo

@pytest.fixture
def client():
    my_app = create_app({
        'TESTING': True,
        'TEST_DATA_PATH': TEST_DATA_PATH,
        'WTF_CSRF_ENABLED': False,
        'REPOSITORY': 'memory'
    })
    return my_app.test_client()

@pytest.fixture
def auth(client):
    return AuthenticationManager(client)

class AuthenticationManager:
    def __init__(self, client):
        self.__client = client

    def login(self, user_name="Username", password="Password"):
        return self.__client.post(
            "/authentication/login",
            data={"user_name": user_name, "password": password}
        )

    def logout(self):
        return self.__client.get("/authentication/logout")

def test_register(client):
    response = client.get("/authentication/register")
    assert response.status_code == 400

    response = client.post(
        "/authentication/register",
        data={"user_name": "newuser", "password": "Password123"}
    )
    assert response.headers["Location"] == "/authentication/login"



def test_login_required_get_to_playlist(client):
    response = client.post('/playlist')
    assert response.headers['Location'] == 'http://localhost/playlist/'
    
def test_reviews_with_invalid_input(client):
    # Register and login
    client.post("/authentication/register",
                data={"user_name": "username", "password": "Password123"})
    client.post('/authentication/login',
                data={"user_name": "username", "password": "Password123"})

    response = client.post('description/7/review',
                           data={'review_text': 'Good Podcast', 'rating': 6})
    message = b'Redirecting.'

    assert message in response.data

def test_podcast_with_reviews(client):
    # Register and login
    client.post("/authentication/register",
                data={"user_name": "username", "password": "Password123"})
    client.post('/authentication/login',
                data={"user_name": "username", "password": "Password123"})

    # Leave a review

    client.post('/description/7/review',
                data={'review_text': 'Great Podcast', 'rating': 3})

    response = client.get("/description/7")
    assert response.status_code == 200
    assert b'Great Podcast' in response.data
