import abc
from typing import List
from podcast.domainmodel.model import Podcast, Episode, User, Review

repo_instance = None


class RepositoryException(Exception):
    def __int__(self, message=None):
        print(f"RepositoryException: {message}")


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_podcast(self, podcast: Podcast):
        # adds a podcast to the repository list of podcast
        raise NotImplementedError

    @abc.abstractmethod
    def get_podcasts(self) -> List[Podcast]:
        # Returns the list of catalogue
        raise NotImplementedError

    @abc.abstractmethod
    def remove_podcast(self, podcast_id: int):
        # remove podcast
        raise NotImplementedError

    @abc.abstractmethod
    def add_episode(self, episode: Episode):
        # adds a episode to the repository list of podcast
        raise NotImplementedError

    @abc.abstractmethod
    def get_episodes_for_podcast(self, podcast_id: int):
        # get episodes
        raise NotImplementedError

    @abc.abstractmethod
    def get_podcast_by_id(self, podcast_id: int):
        raise NotImplementedError

    @abc.abstractmethod
    def add_user(self, user: User):
        # adds a user to the repository list of Users.
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, user_name: str):
        # adds a user with matching username, else None
        raise NotImplementedError
        
    @abc.abstractmethod
    def get_new_user_id(self):
        # get the next integer user id available.
        raise NotImplementedError

    @abc.abstractmethod
    def get_random_podcasts(self):
        # get 9 random podcasts
        raise NotImplementedError

    @abc.abstractmethod
    def get_saved_episodes_for_user(self, username: str):
        # get podcasts saved for user
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_new_review_id(self):
        # get the next integer review id available.
        raise NotImplementedError

    @abc.abstractmethod
    def add_review_to_podcast(self, review: Review, podcast: Podcast):
        # add review object to a podcast object
        raise NotImplementedError

    @abc.abstractmethod
    def add_to_user_playlist(self, user: User, podcast: Podcast):
        # add to user's playlist
        raise NotImplementedError
    
    @abc.abstractmethod
    def remove_episode_from_user_playlist(self, user: User, episode_id: int):
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_episode_by_id(self, episode_id: int):
        raise NotImplementedError