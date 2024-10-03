import os
import random
from abc import ABC
from bisect import insort_left
from typing import List

from podcast.domainmodel.model import Podcast, User, Review, Playlist
from podcast.domainmodel.model import Episode
from podcast.adapters.datareader.csvdatareader import CSVDataReader
from podcast.adapters.repository import AbstractRepository


class MemoryRepository(AbstractRepository, ABC):
    def __init__(self):
        self.podcasts = []
        self.episodes = []
        self.users = []
        self.current_user_id = 0
        self.current_review_id = 0

    def add_podcast(self, podcast: Podcast):
        if isinstance(podcast, Podcast):
            insort_left(self.podcasts, podcast)

    def get_podcasts(self) -> List[Podcast]:
        return self.podcasts

    def remove_podcast(self, podcast_id: int):
        for podcast in self.podcasts:
            if podcast.id == podcast_id:
                self.podcasts.remove(podcast)

    def add_episode(self, episode: Episode):
        if isinstance(episode, Episode):
            insort_left(self.episodes, episode)

    def get_episodes_for_podcast(self, podcast_id: int) -> list:
        podcast_lookup = {p.id: p for p in self.podcasts}
        podcast = podcast_lookup.get(podcast_id)
        if podcast:
            return podcast.episodes
        return []

    def get_podcast_by_id(self, podcast_id: int) -> Podcast:
        for pod in self.podcasts:
            if pod.id == podcast_id:    
                return pod

    def add_user(self, user: User):
        if isinstance(user, User):
            insort_left(self.users, user)

    def get_user(self, username: str) -> User:
        for user in self.users:
            if user.username == username:
                return user

    def get_new_user_id(self) -> int:
        user_id = self.current_user_id
        self.current_user_id += 1
        return user_id

    def get_new_review_id(self) -> int:
        review_id = self.current_review_id
        self.current_review_id += 1
        return review_id

    def add_review_to_podcast(self, review: Review, podcast_to_add_to: Podcast):
        for podcast in self.podcasts:
            if podcast == podcast_to_add_to:
                for podcast_reviews in podcast.reviews:
                    if podcast_reviews.owner == review.owner:
                        return False
                podcast.add_review(review)
                [print(item) for item in podcast.reviews]
        return True

    def get_random_podcasts(self) -> list:
        filtered_podcasts = [podcast for podcast in self.podcasts if len(podcast.title.split(' ')) < 7]
        randomPodcasts = random.sample(filtered_podcasts, min(9, len(filtered_podcasts)))
        return randomPodcasts

    def get_saved_episodes_for_user(self, username:str) -> list:
        for user in self.users:
            if user.username == username:
                return user.playlist.playlist
    
    def remove_episode_from_user_playlist(self, user: User, episode_id: int):
        user_playlist = user.playlist
        user_playlist.remove_episode_by_id(episode_id)

    def add_to_user_playlist(self, user: User, podcast: Podcast):
        user_playlist = user.playlist
        for ep in podcast.episodes:
            user_playlist.add_episode(ep)

    def get_episode_by_id(self, episode_id: int):
        for ep in self.episodes:
            if ep.id == episode_id:
                return ep



















def populate(repo: AbstractRepository, debug: bool):
    current_dir = os.path.dirname(os.path.abspath(__file__))

    if debug:
        tests_data_dir = os.path.abspath(os.path.join(current_dir, '..', '..', 'tests', 'data'))
        episodes_file_name = os.path.join(tests_data_dir, 'episodes.csv')
        podcasts_file_name = os.path.join(tests_data_dir, 'podcasts.csv')
    else:
        # When not in debug, use the actual data path in 'adapters/data'
        episodes_file_name = os.path.join(current_dir, "data", "episodes.csv")
        podcasts_file_name = os.path.join(current_dir, "data", "podcasts.csv")

    reader = CSVDataReader(podcasts_file_name, episodes_file_name)

    reader.read_podcasts_csv()
    reader.read_episodes_csv()

    authors = reader.dataset_of_authors
    podcasts = reader.dataset_of_podcasts
    categories = reader.dataset_of_categories
    episodes = reader.dataset_of_episodes

    for podcast in podcasts:
        repo.add_podcast(podcast)

    for episode in episodes:
        repo.add_episode(episode)
