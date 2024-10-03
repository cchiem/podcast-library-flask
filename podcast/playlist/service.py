from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import User,Podcast


def get_podcasts(repo: AbstractRepository):
    return repo.get_podcasts()

def get_user(repo: AbstractRepository, username: str):
    return repo.get_user(username)

def remove_episode_from_user_playlist(repo: AbstractRepository, user: User, episode_id: int):
    return repo.remove_episode_from_user_playlist(user, episode_id)