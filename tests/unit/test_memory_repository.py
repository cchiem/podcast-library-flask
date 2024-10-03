from random import sample

import pytest
from podcast.domainmodel.model import Podcast, Episode, Category, Author
from podcast.adapters.repository import AbstractRepository
from tests.conftest import *

from tests.conftest import in_memory_repo

@pytest.fixture
def csv_file_paths():
    # Assuming CSV files are located in `tests/data/`
    current_dir = os.path.dirname(__file__)
    podcast_csv = os.path.join(current_dir, '../data/podcasts.csv')
    episode_csv = os.path.join(current_dir, '../data/episodes.csv')
    return podcast_csv, episode_csv

def test_add_podcasts(in_memory_repo):
    line1 = [6,
             "test",
             "image source",
             "description test",
             "English",
             "category1 | category2",
             "www.website.com",
             "author name",
             12312415]

    category_list = line1[5].split(" | ")
    author_name = line1[7]
    # Handle the author
    author = Author(3, author_name)
    # Create the podcast instance
    podcast = Podcast(
        podcast_id=int(line1[0]),
        podcast_title=str(line1[1]))

    # Handle categories
    for category_name in category_list:
        cate = Category(1, category_name)
        podcast.add_category(cate)
    # Handle author
    author.add_podcast(podcast)

    in_memory_repo.add_podcast(podcast)
    assert (in_memory_repo.get_podcasts()[3]) is podcast  # new foruth element is added and is a podcast!


def test_get_podcasts(in_memory_repo):
    podcastTest = Podcast(3,
                          "Radio Popolare")
    podcastTest.add_category(Category(1, "Society & Culture"))

    assert in_memory_repo.get_podcasts()[2] == podcastTest


def test_remove_podcast(in_memory_repo):
    assert len(in_memory_repo.podcasts) == 3
    in_memory_repo.remove_podcast(2)  # removing by id
    assert len(in_memory_repo.podcasts) == 2


def test_get_episodes_for_podcast(in_memory_repo):
    assert len(in_memory_repo.get_episodes_for_podcast(1)) == 1


def test_get_podcast_by_id(in_memory_repo):
    assert type(in_memory_repo.get_podcast_by_id(1)) == Podcast


def test_add_user(in_memory_repo, sample_user):
    in_memory_repo.add_user(sample_user)
    assert len(in_memory_repo.users) == 1


def test_get_user(in_memory_repo, sample_user):
    sample_username = sample_user.username
    in_memory_repo.add_user(sample_user)

    memory_username = in_memory_repo.get_user(sample_username)
    assert memory_username == sample_user


def test_get_new_user_id(in_memory_repo, sample_user):
    in_memory_repo.add_user(sample_user)

    assert in_memory_repo.current_user_id == 0


def test_add_review_to_podcast(in_memory_repo, sample_review, sample_podcast):
    in_memory_repo.add_review_to_podcast(sample_review, sample_podcast)
    podcast = in_memory_repo.get_podcast_by_id(1)

    assert sample_review in podcast.reviews


def test_get_random_podcasts(in_memory_repo):
    randomPodcasts = in_memory_repo.get_random_podcasts()
    assert len(randomPodcasts) == 3

def test_get_saved_episodes_for_user(in_memory_repo, sample_user):
    username = sample_user.username
    in_memory_repo.add_user(sample_user)

    episodes = in_memory_repo.get_saved_episodes_for_user(username)
    assert episodes == []

def test_get_episode_by_id(in_memory_repo, sample_episode):
    memory_episode = in_memory_repo.get_episode_by_id(1)
    assert sample_episode == memory_episode