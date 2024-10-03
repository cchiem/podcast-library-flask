from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import Podcast, User

def get_podcasts(repo: AbstractRepository):
    return repo.get_podcasts()

def get_user(repo: AbstractRepository, username: str):
    return repo.get_user(username)

def get_podcast_by_id(repo: AbstractRepository, podcast_id: int):
    return repo.get_podcast_by_id(podcast_id)

def add_to_user_playlist(repo: AbstractRepository, user: User, podcast: Podcast):
    return repo.add_to_user_playlist(user, podcast)