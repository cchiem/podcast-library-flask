from random import sample
import os
from datetime import datetime
import pytest
from podcast.adapters.repository import AbstractRepository

from podcast import CSVDataReader
from podcast.description.description import description
from podcast.home import service as home_services
from podcast.playlist import service as playlist_services
from podcast.description import service as description_services
from podcast.catalogue import service as catalogue_services
from podcast.authentication import service as authentication_services
from podcast.playlist.playlist import playlist
from tests.conftest import sample_podcasts
from tests.conftest import *
from podcast.domainmodel.model import *
from podcast.playlist import playlist
from werkzeug.security import generate_password_hash, check_password_hash

from tests.conftest import in_memory_repo, sample_podcasts, sample_episodes
from podcast.domainmodel.model import *



@pytest.fixture
def csv_file_paths():
    # Assuming CSV files are located in `tests/data/`
    current_dir = os.path.dirname(__file__)
    podcast_csv = os.path.join(current_dir, '../data/podcasts.csv')
    episode_csv = os.path.join(current_dir, '../data/episodes.csv')
    return podcast_csv, episode_csv

# Test retrieving podcasts from the home service layer
def test_can_get_all_podcasts(in_memory_repo, sample_podcasts):
    podcasts_from_service_layer = home_services.get_podcasts(in_memory_repo)
    assert podcasts_from_service_layer[0] == sample_podcasts[1]


# Test removing an episode from a user's playlist
def test_remove_episode_from_user_playlist(in_memory_repo, sample_user, sample_episode, sample_podcast):
    episode_id = sample_episode.id
    episode = description_services.get_episode_by_id(in_memory_repo, episode_id)
    user_playlist = sample_user.playlist
    user_playlist.add_episode(episode)
    assert episode in sample_user.playlist.episode_list
    playlist_services.remove_episode_from_user_playlist(in_memory_repo, sample_user, episode)
    assert [episode] not in sample_user.playlist.episode_list


# Test retrieving a user by username
def test_get_user(in_memory_repo, sample_user):
    username = sample_user.username
    user = playlist_services.get_user(in_memory_repo, username)
    assert sample_user.username == username


# Test getting random podcasts for a user
def test_get_random_podcasts(in_memory_repo):
    random_podcasts = home_services.get_random_podcasts(in_memory_repo)
    assert len(random_podcasts) > 0


# Test retrieving a podcast by its ID
def test_get_podcast_by_id(in_memory_repo, sample_podcast):
    podcast_id = sample_podcast.id
    podcast = description_services.get_podcast_by_id(in_memory_repo, podcast_id)
    assert podcast.id == podcast_id


# Test getting all episodes for a specific podcast
def test_get_episodes_for_podcast(in_memory_repo, sample_podcast):
    podcast_id = sample_podcast.id
    episodes = description_services.get_episodes_for_podcast(in_memory_repo, podcast_id)
    assert len(episodes) > 0
    for episode in episodes:
        assert episode.podcast.id == podcast_id


# Test adding a review for a podcast
def test_add_review(in_memory_repo, sample_podcast, sample_user, sample_review):
    in_memory_repo.add_user(sample_user)
    in_memory_repo.add_podcast(sample_podcast)
    podcast_id = sample_podcast.id
    review_text = sample_review.review_content
    rating = sample_review.rating
    username = sample_user.username
    print(sample_user)
    description_services.add_review(in_memory_repo, podcast_id, review_text, rating, username)

    # Verify that the review is added
    podcast = in_memory_repo.get_podcast_by_id(podcast_id)
    assert len(podcast.reviews) > 0
    review = podcast.reviews[-1]
    assert review.review_content == review_text
    assert review.rating == rating

# Test retrieving an episode by its ID
def test_get_episode_by_id(in_memory_repo, sample_episode):
    episode_id = sample_episode.id
    episode = description_services.get_episode_by_id(in_memory_repo, episode_id)
    assert episode.id == episode_id


# Test retrieving saved episodes for a user
def test_get_saved_episodes_for_user(in_memory_repo, sample_user):
    username = sample_user.username
    saved_episodes = description_services.get_saved_episodes_for_user(in_memory_repo, username)
    assert saved_episodes is None


# Test authenticating a user
def test_authenticate_user(in_memory_repo, sample_user):
    in_memory_repo.add_user(sample_user)
    username = sample_user.username
    password = sample_user.password
    authentication = authentication_services.authenticate_user(username, 'password123', in_memory_repo)
    assert authentication != False

def test_user_to_dict(sample_user):
    user_dict = authentication_services.user_to_dict(sample_user)
    assert user_dict['username'] == sample_user.username
    assert user_dict['password'] == sample_user.password

# Test adding a podcast to a user's playlist
def test_add_to_user_playlist(in_memory_repo, sample_user, sample_podcast, sample_episode):
    catalogue_services.add_to_user_playlist(in_memory_repo, sample_user, sample_podcast)
    assert sample_episode in [episode for episode in sample_user.playlist.playlist]
