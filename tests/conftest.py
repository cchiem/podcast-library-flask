import os

import pytest

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
def sample_podcasts(csv_file_paths):
    podcast_filename, episode_filename = csv_file_paths
    csv_reader = CSVDataReader(podcast_filename, episode_filename)

    csv_reader.read_podcasts_csv()
    podcasts = csv_reader.dataset_of_podcasts

    return podcasts

@pytest.fixture
def sample_episodes(csv_file_paths):
    podcast_filename, episode_filename = csv_file_paths
    csv_reader = CSVDataReader(podcast_filename, episode_filename)
    #must have a podcast to have an episode
    csv_reader.read_podcasts_csv()

    csv_reader.read_episodes_csv()
    episodes = csv_reader.dataset_of_episodes
    return episodes


@pytest.fixture
def sample_author():
    return Author(1, "test_author")


@pytest.fixture
def sample_user():
    return User(1, 'test_user', generate_password_hash('password123'))


@pytest.fixture
def sample_podcast(sample_author):
    sample_pod = Podcast(1, 'Sample Podcast')
    sample_pod.author = sample_author
    sample_pod.add_episode(Episode(1, sample_pod, 'Sample Episode', "audio_url", 45, "Sample description", datetime.now()))
    return sample_pod


@pytest.fixture
def sample_episode(sample_podcast):
    return Episode(1, sample_podcast, 'Sample Episode', "audio_url", 45, "Sample description", datetime.now())


@pytest.fixture
def sample_review(sample_user, sample_podcast, sample_episode):
    return Review(1, sample_user, sample_podcast, None, 1, 'This is a review')

@pytest.fixture
def csv_file_paths():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Assuming CSV files are located in `tests/data/`
    tests_data_dir = os.path.abspath(os.path.join(current_dir, '..', '..', 'tests', 'data'))
    episodes_file_name = os.path.join(tests_data_dir, 'episodes.csv')
    podcasts_file_name = os.path.join(tests_data_dir, 'podcasts.csv')
    return podcasts_file_name, episodes_file_name

