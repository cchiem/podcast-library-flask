from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import Podcast, Review


class UserReviewAddedException(Exception):
    pass

def get_podcast_by_id(repo: AbstractRepository, podcast_id: int):
    return repo.get_podcast_by_id(podcast_id)

def get_episodes_for_podcast(repo: AbstractRepository, podcast_id: int):
    return repo.get_episodes_for_podcast(podcast_id)

def add_review(repo: AbstractRepository, podcast_id: int, review_text: str, rating: int, username: str):
    #new_review_id: int, owner: User, podcast: Podcast, episode: (Episode or None), rating: int,review_content: str):
    user = repo.get_user(username)
    review = Review(repo.get_new_review_id(), repo.get_user(username), repo.get_podcast_by_id(podcast_id), None, rating, review_text)
    review_added = repo.add_review_to_podcast(review, repo.get_podcast_by_id(podcast_id))
    if not review_added:
        raise UserReviewAddedException
    #return repo.add_review(context needed)

def get_episode_by_id(repo: AbstractRepository, episode_id: int):
    return repo.get_episode_by_id(episode_id)

def get_user(repo: AbstractRepository, username: str):
    return repo.get_user(username)

def get_saved_episodes_for_user(repo: AbstractRepository, username: str):
    return repo.get_saved_episodes_for_user(username)
