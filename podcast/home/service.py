from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import Podcast

def get_podcasts(repo: AbstractRepository):
    return repo.get_podcasts()

def get_random_podcasts(repo: AbstractRepository):
    return repo.get_random_podcasts()