import os
from pathlib import Path
from tests.conftest import sample_podcasts, sample_episodes
import pytest
from podcast.domainmodel.model import Author, Podcast, Category, User, PodcastSubscription, Episode, Playlist, Review
from podcast.adapters.datareader.csvdatareader import CSVDataReader

from utils import get_project_root


def test_author_initialization():
    author1 = Author(1, "Brian Denny")
    assert repr(author1) == "<Author 1: Brian Denny>"
    assert author1.name == "Brian Denny"

    with pytest.raises(ValueError):
        author2 = Author(2, "")

    with pytest.raises(ValueError):
        author3 = Author(3, 123)

    author4 = Author(4, " USA Radio   ")
    assert author4.name == "USA Radio"

    author4.name = "Jackson Mumey"
    assert repr(author4) == "<Author 4: Jackson Mumey>"


def test_author_eq():
    author1 = Author(1, "Author A")
    author2 = Author(1, "Author A")
    author3 = Author(3, "Author B")
    assert author1 == author2
    assert author1 != author3
    assert author3 != author2
    assert author3 == author3


def test_author_lt():
    author1 = Author(1, "Jackson Mumey")
    author2 = Author(2, "USA Radio")
    author3 = Author(3, "Jesmond Parish Church")
    assert author1 < author2
    assert author2 > author3
    assert author1 < author3
    author_list = [author3, author2, author1]
    assert sorted(author_list) == [author1, author3, author2]


def test_author_hash():
    authors = set()
    author1 = Author(1, "Doctor Squee")
    author2 = Author(2, "USA Radio")
    author3 = Author(3, "Jesmond Parish Church")
    authors.add(author1)
    authors.add(author2)
    authors.add(author3)
    assert len(authors) == 3
    assert repr(
        sorted(authors)) == "[<Author 1: Doctor Squee>, <Author 3: Jesmond Parish Church>, <Author 2: USA Radio>]"
    authors.discard(author1)
    assert repr(sorted(authors)) == "[<Author 3: Jesmond Parish Church>, <Author 2: USA Radio>]"


def test_author_name_setter():
    author = Author(1, "Doctor Squee")
    author.name = "   USA Radio  "
    assert repr(author) == "<Author 1: USA Radio>"

    with pytest.raises(ValueError):
        author.name = ""

    with pytest.raises(ValueError):
        author.name = 123


def test_category_initialization():
    category1 = Category(1, "Comedy")
    assert repr(category1) == "<Category 1: Comedy>"
    category2 = Category(2, " Christianity ")
    assert repr(category2) == "<Category 2: Christianity>"

    with pytest.raises(ValueError):
        category3 = Category(3, 300)

    category5 = Category(5, " Religion & Spirituality  ")
    assert category5.name == "Religion & Spirituality"

    with pytest.raises(ValueError):
        category1 = Category(4, "")


def test_category_name_setter():
    category1 = Category(6, "Category A")
    assert category1.name == "Category A"

    with pytest.raises(ValueError):
        category1 = Category(7, "")

    with pytest.raises(ValueError):
        category1 = Category(8, 123)


def test_category_eq():
    category1 = Category(9, "Action")
    category2 = Category(10, "Indie")
    category3 = Category(11, "Sports")
    assert category1 == category1
    assert category1 != category2
    assert category2 != category3
    assert category1 != "9: Adventure"
    assert category2 != 105


def test_category_hash():
    category1 = Category(9, "Action")
    category2 = Category(10, "Indie")
    category3 = Category(11, "Sports")
    category_set = set()
    category_set.add(category1)
    category_set.add(category2)
    category_set.add(category3)
    assert sorted(category_set) == [category1, category2, category3]
    category_set.discard(category2)
    category_set.discard(category1)
    assert sorted(category_set) == [category3]


def test_category_lt():
    category1 = Category(9, "Action")
    category2 = Category(10, "Indie")
    category3 = Category(11, "Sports")
    assert category1 < category2
    assert category2 < category3
    assert category3 > category1
    category_list = [category3, category2, category1]
    assert sorted(category_list) == [category1, category2, category3]


# Fixtures to reuse in multiple tests
@pytest.fixture
def my_author():
    return Author(1, "Joe Toste")


@pytest.fixture
def my_podcast(my_author):
    podcast = Podcast(100, "Joe Toste Podcast - Sales Training Expert")
    podcast.author = my_author
    return podcast


@pytest.fixture
def my_user():
    return User(1, "Shyamli", "pw12345")


@pytest.fixture
def my_subscription(my_user, my_podcast):
    return PodcastSubscription(1, my_user, my_podcast)


def test_podcast_initialization():
    author1 = Author(1, "Doctor Squee")
    podcast1 = Podcast(2, "My First Podcast")
    podcast1.author = author1
    assert podcast1.id == 2
    assert podcast1.author == author1
    assert podcast1.title == "My First Podcast"

    assert repr(podcast1) == "<Podcast 2: 'My First Podcast' by Doctor Squee>"

    with pytest.raises(ValueError):
        podcast3 = Podcast(-123, "Todd Clayton")


def test_podcast_change_title(my_podcast):
    my_podcast.title = "TourMix Podcast"
    assert my_podcast.title == "TourMix Podcast"

    with pytest.raises(ValueError):
        my_podcast.title = ""


def test_podcast_add_category(my_podcast):
    category = Category(12, "TV & Film")
    my_podcast.add_category(category)
    assert category in my_podcast.categories
    assert len(my_podcast.categories) == 1

    my_podcast.add_category(category)
    my_podcast.add_category(category)
    assert len(my_podcast.categories) == 1


def test_podcast_remove_category(my_podcast):
    category1 = Category(13, "Technology")
    my_podcast.add_category(category1)
    my_podcast.remove_category(category1)
    assert len(my_podcast.categories) == 0

    category2 = Category(14, "Science")
    my_podcast.add_category(category1)
    my_podcast.remove_category(category2)
    assert len(my_podcast.categories) == 1


def test_podcast_title_setter(my_podcast):
    my_podcast.title = "Dark Throne"
    assert my_podcast.title == 'Dark Throne'

    with pytest.raises(ValueError):
        my_podcast.title = " "

    with pytest.raises(ValueError):
        my_podcast.title = ""


def test_podcast_eq():
    author1 = Author(1, "Author A")
    author2 = Author(2, "Author C")
    author3 = Author(3, "Author B")
    podcast1 = Podcast(100, "Joe Toste Podcast - Sales Training Expert")
    podcast2 = Podcast(200, "Voices in AI")
    podcast3 = Podcast(101, "Law Talk")
    assert podcast1 == podcast1
    assert podcast1 != podcast2
    assert podcast2 != podcast3


def test_podcast_hash():
    author1 = Author(1, "Author A")
    author2 = Author(2, "Author C")
    author3 = Author(3, "Author B")
    podcast1 = Podcast(100, "Joe Toste Podcast - Sales Training Expert")
    podcast2 = Podcast(200, "Voices in AI")
    podcast3 = Podcast(100, "Law Talk")
    podcast_set = {podcast1, podcast2, podcast3}
    assert len(podcast_set) == 2  # Since podcast1 and podcast2 have the same ID


def test_podcast_lt():
    author1 = Author(1, "Author A")
    author2 = Author(2, "Author C")
    author3 = Author(3, "Author B")
    podcast1 = Podcast(100, "Joe Toste Podcast - Sales Training Expert")
    podcast2 = Podcast(200, "Voices in AI")
    podcast3 = Podcast(101, "Law Talk")
    assert podcast1 < podcast2
    assert podcast2 > podcast3
    assert podcast3 > podcast1


def test_user_initialization():
    user1 = User(1, "Shyamli", "pw12345")
    user2 = User(2, "asma", "pw67890")
    user3 = User(3, "JeNNy  ", "pw87465")
    assert repr(user1) == "<User 1: shyamli>"
    assert repr(user2) == "<User 2: asma>"
    assert repr(user3) == "<User 3: jenny>"
    assert user2.password == "pw67890"
    with pytest.raises(ValueError):
        user4 = User(4, "xyz  ", "")
    with pytest.raises(ValueError):
        user4 = User(5, "    ", "qwerty12345")


def test_user_eq():
    user1 = User(1, "Shyamli", "pw12345")
    user2 = User(2, "asma", "pw67890")
    user3 = User(3, "JeNNy  ", "pw87465")
    user4 = User(1, "Shyamli", "pw12345")
    assert user1 == user4
    assert user1 != user2
    assert user2 != user3


def test_user_hash():
    user1 = User(1, "   Shyamli", "pw12345")
    user2 = User(2, "asma", "pw67890")
    user3 = User(3, "JeNNy  ", "pw87465")
    user_set = set()
    user_set.add(user1)
    user_set.add(user2)
    user_set.add(user3)
    assert sorted(user_set) == [user1, user2, user3]
    user_set.discard(user1)
    user_set.discard(user2)
    assert list(user_set) == [user3]


def test_user_lt():
    user1 = User(1, "Shyamli", "pw12345")
    user2 = User(2, "asma", "pw67890")
    user3 = User(3, "JeNNy  ", "pw87465")
    assert user1 < user2
    assert user2 < user3
    assert user3 > user1
    user_list = [user3, user2, user1]
    assert sorted(user_list) == [user1, user2, user3]


def test_user_add_remove_favourite_podcasts(my_user, my_subscription):
    my_user.add_subscription(my_subscription)
    assert repr(my_user.subscription_list) == "[<PodcastSubscription 1: Owned by shyamli>]"
    my_user.add_subscription(my_subscription)
    assert len(my_user.subscription_list) == 1
    my_user.remove_subscription(my_subscription)
    assert repr(my_user.subscription_list) == "[]"


def test_podcast_subscription_initialization(my_subscription):
    assert my_subscription.id == 1
    assert repr(my_subscription.owner) == "<User 1: shyamli>"
    assert repr(my_subscription) == "<PodcastSubscription 1: Owned by shyamli>"
    assert repr(my_subscription.podcast) == "<Podcast 100: 'Joe Toste Podcast - Sales Training Expert' by Joe Toste>"


def test_podcast_subscription_set_owner(my_subscription):
    new_user = User(2, "asma", "pw67890")
    my_subscription.owner = new_user
    assert my_subscription.owner == new_user

    with pytest.raises(TypeError):
        my_subscription.owner = "not a user"


def test_podcast_subscription_set_podcast(my_subscription):
    author2 = Author(2, "Author C")
    new_podcast = Podcast(200, "Voices in AI")

    my_subscription.podcast = new_podcast
    assert my_subscription.podcast == new_podcast

    with pytest.raises(TypeError):
        my_subscription.podcast = "not a podcast"


def test_podcast_subscription_equality(my_user, my_podcast):
    sub1 = PodcastSubscription(1, my_user, my_podcast)
    sub2 = PodcastSubscription(1, my_user, my_podcast)
    sub3 = PodcastSubscription(2, my_user, my_podcast)
    assert sub1 == sub2
    assert sub1 != sub3


def test_podcast_subscription_hash(my_user, my_podcast):
    sub1 = PodcastSubscription(1, my_user, my_podcast)
    sub2 = PodcastSubscription(1, my_user, my_podcast)
    sub_set = {sub1, sub2}  # Should only contain one element since hash should be the same
    assert len(sub_set) == 1


# TODO : Write Unit Tests for CSVDataReader, Episode, Review, Playlist classes
@pytest.fixture
def csv_file_paths():
    # Assuming CSV files are located in `tests/data/`
    current_dir = os.path.dirname(__file__)
    podcast_csv = os.path.join(current_dir, '../data/podcasts.csv')
    episode_csv = os.path.join(current_dir, '../data/episodes.csv')
    return podcast_csv, episode_csv


# TODO : EPISODE TEST : INIT, TITLE_SETTER, AUDIO_LINK SETTER, AUDIO_LINK LENGTH, DESCRIPTION_SETTER, DATE_SETTER, EQ, LT, HASH, REPR
def test_initialisation(sample_podcasts):
    podcast = sample_podcasts[0]
    my_episode = Episode(17, podcast, "Christmas Week 1 Day 1",
                         "https://cm-media-manager.s3.amazonaws.com/ChristmasDec1.mp3?x-appid=SaddlebackChurch:DriveTimeDevotionalsPodcast",
                         234, "Day 1 : The Manger in the Mall", "2017-12-01 00:00:00+00")

    assert my_episode.id == 17
    assert my_episode.podcast == podcast
    assert my_episode.title == "Christmas Week 1 Day 1"
    assert my_episode.audio == "https://cm-media-manager.s3.amazonaws.com/ChristmasDec1.mp3?x-appid=SaddlebackChurch:DriveTimeDevotionalsPodcast"
    assert my_episode.audio_length == 234
    assert my_episode.description == "Day 1 : The Manger in the Mall"
    assert my_episode.pub_date == "2017-12-01 00:00:00+00"


def test_title_setter(sample_podcasts):
    podcast = sample_podcasts[0]
    episode1 = Episode(1, podcast, "Old Title", "www.youtube.com", 123, "descript", "2017-12-01 00:00:00+00")
    episode1.title = "New Title"
    assert episode1.title == "New Title"

    with pytest.raises(ValueError):
        episode1.title = ""


def test_audioLink_setter(sample_podcasts):
    podcast = sample_podcasts[0]

    episode1 = Episode(1, podcast, "Old Title", "www.youtube.com", 123, "descript", "2017-12-01 00:00:00+00")
    episode1.audioLink = "www.google.com"
    assert episode1.audioLink == "www.google.com"


def test_audioLength_setter(sample_podcasts):
    podcast = sample_podcasts[0]

    episode1 = Episode(1, podcast, "Old Title", "www.youtube.com", 123, "descript", "2017-12-01 00:00:00+00")
    episode1.audioLength = 321
    assert episode1.audioLength == 321


def test_description_setter(sample_podcasts):
    podcast = sample_podcasts[0]

    episode1 = Episode(1, podcast, "Old Title", "www.youtube.com", 123, "OLD descript", "2017-12-01 00:00:00+00")
    episode1.description = "NEW DESCRIPTION"
    assert episode1.description == "NEW DESCRIPTION"


def test_date_setter(sample_podcasts):
    podcast = sample_podcasts[0]

    episode1 = Episode(1, podcast, "Old Title", "www.youtube.com", 123, "OLD descript", "2017-12-01 00:00:00+00")
    episode1.date = "3111-12-11 00:00:00+00"
    assert episode1.date == "3111-12-11 00:00:00+00"


def test_episode_eq(sample_podcasts):
    podcast = sample_podcasts[0]
    podcast1 = sample_podcasts[1]
    episode1 = Episode(17, podcast, "Christmas Week 1 Day 1",
                       "https://cm-media-manager.s3.amazonaws.com/ChristmasDec1.mp3?x-appid=SaddlebackChurch:DriveTimeDevotionalsPodcast",
                       234,
                       "Day 1 : The Manger in the Mall", "2017-12-01 00:00:00+00")
    episode2 = Episode(17, podcast, "Christmas Week 1 Day 1",
                       "https://cm-media-manager.s3.amazonaws.com/ChristmasDec1.mp3?x-appid=SaddlebackChurch:DriveTimeDevotionalsPodcast",
                       234,
                       "Day 1 : The Manger in the Mall", "2017-12-01 00:00:00+00")
    episode3 = Episode(33, podcast1, "Saturday Morning Sizzling Slow Jamz",
                       "http://api.spreaker.com/download/episode/13490130/saturday_morning_sizzling_slow_jamz.mp3",
                       4870,
                       "Slow Jammin on a nice Saturday Morning", "2017-12-02 15:45:05+00")

    assert episode1 == episode2
    assert episode2 != episode3
    assert episode1 != episode3


def test_episode_lt(sample_podcasts):
    podcast = sample_podcasts[0]
    podcast1 = sample_podcasts[1]
    episode1 = Episode(17, podcast, "Christmas Week 1 Day 1",
                       "https://cm-media-manager.s3.amazonaws.com/ChristmasDec1.mp3?x-appid=SaddlebackChurch:DriveTimeDevotionalsPodcast",
                       234,
                       "Day 1 : The Manger in the Mall", "2017-12-01 00:00:00+00")
    episode2 = Episode(33, podcast1, "Saturday Morning Sizzling Slow Jamz",
                       "http://api.spreaker.com/download/episode/13490130/saturday_morning_sizzling_slow_jamz.mp3",
                       4870,
                       "Slow Jammin on a nice Saturday Morning", "2017-12-02 15:45:05+00")

    assert episode1 < episode2
    assert episode2 > episode1


def test_episode_hash(sample_podcasts):
    podcast = sample_podcasts[0]
    podcast1 = sample_podcasts[1]
    episode1 = Episode(17, podcast, "Christmas Week 1 Day 1",
                       "https://cm-media-manager.s3.amazonaws.com/ChristmasDec1.mp3?x-appid=SaddlebackChurch:DriveTimeDevotionalsPodcast",
                       234,
                       "Day 1 : The Manger in the Mall", "2017-12-01 00:00:00+00")
    episode2 = Episode(17, podcast, "Christmas Week 1 Day 1",
                       "https://cm-media-manager.s3.amazonaws.com/ChristmasDec1.mp3?x-appid=SaddlebackChurch:DriveTimeDevotionalsPodcast",
                       234,
                       "Day 1 : The Manger in the Mall", "2017-12-01 00:00:00+00")

    episode3 = Episode(71, podcast1, "Christmas Week 1 Day 1",
                       "https://cm-media-manager.s3.amazonaws.com/ChristmasDec1.mp3?x-appid=SaddlebackChurch:DriveTimeDevotionalsPodcast",
                       234,
                       "Day 1 : The Manger in the Mall", "2017-12-01 00:00:00+00")

    episode_set = set()
    episode_set.add(episode1)
    episode_set.add(episode2)
    assert len(episode_set) == 1  # Should only contain one element since hash should be the same
    episode_set.add(episode3)
    assert len(episode_set) == 2  # Should contain two element since hash should be the same


def test_episode_repr(sample_podcasts):
    podcast = sample_podcasts[0]
    podcast1 = sample_podcasts[1]
    episode1 = Episode(17, podcast, "Christmas Week 1 Day 1",
                       "https://cm-media-manager.s3.amazonaws.com/ChristmasDec1.mp3?x-appid=SaddlebackChurch:DriveTimeDevotionalsPodcast",
                       234,
                       "Day 1 : The Manger in the Mall", "2017-12-01 00:00:00+00")
    episode2 = Episode(17, podcast, "Christmas Week 1 Day 1",
                       "https://cm-media-manager.s3.amazonaws.com/ChristmasDec1.mp3?x-appid=SaddlebackChurch:DriveTimeDevotionalsPodcast",
                       234,
                       "Day 1 : The Manger in the Mall", "2017-12-01 00:00:00+00")

    episode3 = Episode(33, podcast1, "Saturday Morning Sizzling Slow Jamz",
                       "http://api.spreaker.com/download/episode/13490130/saturday_morning_sizzling_slow_jamz.mp3",
                       4870,
                       "Slow Jammin on a nice Saturday Morning", "2017-12-02 15:45:05+00")

    assert repr(episode1) == '<Episode 17 | From "<Podcast 1: \'D-Hour Radio Network\' by D Hour Radio ''Network>">'
    assert repr(episode2) == '<Episode 17 | From "<Podcast 1: \'D-Hour Radio Network\' by D Hour Radio ''Network>">'
    assert repr(episode3) == '<Episode 33 | From "<Podcast 2: \'Brian Denny Radio\' by Brian Denny>">'


# TODO : PLAYLIST TEST : EQ, LT, REPR, HASH

def test_playlist_initialisation(sample_episodes):
    episode1 = sample_episodes[0]
    episode2 = sample_episodes[1]

    user = User(12, "John Doe", password="abcdefg")
    playlist = Playlist(1, "Holiday Playlist", user, [episode1, episode2])

    assert playlist.playlist_id == 1
    assert playlist.playlist_name == "Holiday Playlist"
    assert playlist.owner == user
    assert playlist.episode_list == [episode1, episode2]

    with pytest.raises(ValueError):
        Playlist("1", "Holiday Playlist", user, [episode1])

    with pytest.raises(ValueError):
        Playlist(1, "", user, [episode1])


def test_playlist_name_setter():
    user = User(12, "John Doe", password="abcdefg")
    playlist = Playlist(1, "Holiday Playlist", user, [])
    playlist.playlist_name = "New Playlist Name"
    assert playlist.playlist_name == "New Playlist Name"

    with pytest.raises(ValueError):
        playlist.playlist_name = ""


def test_playlist_add_episode(sample_episodes):
    episode = sample_episodes[0]

    user = User(12, "John Doe", password="abcdefg")
    playlist = Playlist(1, "Holiday Playlist", user, [])

    playlist.add_episode(episode)
    assert len(playlist.episode_list) == 1
    assert playlist.episode_list[0] == episode

    with pytest.raises(TypeError):
        playlist.add_episode("Not an episode")


def test_playlist_remove_episode(sample_episodes):
    episode = sample_episodes[0]

    user = User(12, "John Doe", password="abcdefg")
    playlist = Playlist(1, "Holiday Playlist", user, [episode])

    playlist.remove_episode(episode)
    assert len(playlist.episode_list) == 0


def test_playlist_eq(sample_episodes):
    episode = sample_episodes[0]
    user = User(12, "John Doe", password="abcdefg")

    playlist1 = Playlist(1, "Holiday Playlist", user, [episode])
    playlist2 = Playlist(1, "Holiday Playlist", user, [episode])
    playlist3 = Playlist(2, "Other Playlist", user, [])

    assert playlist1 == playlist2
    assert playlist1 != playlist3


def test_playlist_lt_gt(sample_episodes):
    episode = sample_episodes[0]
    episode2 = sample_episodes[1]
    user = User(12, "John Doe", password="abcdefg")

    playlist1 = Playlist(1, "Holiday Playlist", user, [episode])
    playlist2 = Playlist(2, "Long Playlist", user, [episode, episode2])

    assert playlist1 < playlist2
    assert playlist2 > playlist1


def test_playlist_hash(sample_episodes):
    episode = sample_episodes[0]

    user = User(12, "John Doe", password="abcdefg")

    playlist1 = Playlist(1, "Holiday Playlist", user, [episode])
    playlist2 = Playlist(1, "Holiday Playlist", user, [episode])

    playlist_set = set()
    playlist_set.add(playlist1)
    playlist_set.add(playlist2)

    assert len(playlist_set) == 1  # Since playlist1 and playlist2 are equal


def test_playlist_repr(sample_episodes):
    episode = sample_episodes[0]
    user = User(12, "John Doe", password="abcdefg")

    playlist = Playlist(1, "Holiday Playlist", user, [episode])

    assert repr(playlist) == "Playlist(1, 'Holiday Playlist', Owner: john doe, Episodes: 1)"


# TODO : REVIEW TEST : EQ, LT, REPR, HASH

def test_review_initialisation(sample_podcasts, sample_episodes):
    podcast = (sample_podcasts[0])
    episode = (sample_episodes[0])
    user1 = User(1, "Dhiren", "pw12345")

    review1 = Review(1, user1, podcast, episode, 3, "Good Podcast")

    assert review1._id == 1
    assert review1._podcast == podcast
    assert review1._episode == episode
    assert review1._rating == 3
    assert review1.review_content == "Good Podcast"

    with pytest.raises(ValueError):
        review2 = Review(1, user1, podcast, episode, 7, "Good Podcast")
        review3 = Review(1, user1, podcast, episode, 3, "")


def test_review_eq(sample_podcasts, sample_episodes):
    podcast = (sample_podcasts[0])
    episode = (sample_episodes[0])
    podcast2 = (sample_podcasts[1])
    episode2 = (sample_episodes[1])
    user1 = User(1, "Dhiren", "pw12345")
    user2 = User(2, "Chris", "pw67890")

    review1 = Review(1, user1, podcast, episode, 3, "Good Podcast")
    review2 = Review(1, user1, podcast, episode, 4, "Great Podcast")
    review3 = Review(2, user2, podcast2, episode2, 5, "Amazing Podcast!")

    assert review1 == review2
    assert review1 != review3
    assert review2 != review3


def test_review_lt(sample_podcasts, sample_episodes):
    podcast = (sample_podcasts[0])
    episode = (sample_episodes[0])
    podcast2 = (sample_podcasts[1])
    episode2 = (sample_episodes[1])
    user1 = User(1, "Dhiren", "pw12345")
    user2 = User(2, "Chris", "pw67890")

    review1 = Review(1, user1, podcast, episode, 3, "Good Podcast")
    review2 = Review(1, user1, podcast, episode, 4, "Great Podcast")
    review3 = Review(2, user2, podcast2, episode2, 5, "Amazing Podcast!")

    assert review1 < review2
    assert review2 < review3
    assert review3 > review1


def test_review_repr(sample_podcasts, sample_episodes):
    podcast = (sample_podcasts[0])
    episode = (sample_episodes[0])
    podcast2 = (sample_podcasts[1])
    episode2 = (sample_episodes[1])
    user1 = User(1, "Dhiren", "pw12345")
    user2 = User(2, "Chris", "pw67890")

    review1 = Review(1, user1, podcast, episode, 3, "Good Podcast")
    review2 = Review(1, user1, podcast, episode, 4, "Great Podcast")
    review3 = Review(2, user2, podcast2, episode2, 5, "Amazing Podcast!")
    review4 = Review(3, user2, podcast2, None, 5, "Amazing Podcast!")

    assert repr(review1) == "<Review: 1, Owner: 1, Podcast: 1, Episode: 1, Rating: 3>"
    assert repr(review2) == "<Review: 1, Owner: 1, Podcast: 1, Episode: 1, Rating: 4>"
    assert repr(review3) == "<Review: 2, Owner: 2, Podcast: 2, Episode: 2, Rating: 5>"
    assert repr(review4) == "<Review: 3, Owner: 2, Podcast: 2, Episode: None, Rating: 5>"


def test_review_hash(sample_podcasts, sample_episodes):
    podcast = (sample_podcasts[0])
    episode = (sample_episodes[0])
    podcast2 = (sample_podcasts[1])
    episode2 = (sample_episodes[1])
    user1 = User(1, "Dhiren", "pw12345")
    user2 = User(2, "Chris", "pw67890")

    review1 = Review(1, user1, podcast, episode, 3, "Good Podcast")
    review2 = Review(1, user1, podcast, episode, 4, "Great Podcast")
    review3 = Review(2, user2, podcast2, episode2, 5, "Amazing Podcast!")

    review_set = set()
    review_set.add(review1)
    review_set.add(review2)
    assert len(review_set) == 1  # Should only contain one element since hash value should be the same
    review_set.add(review3)
    assert len(review_set) == 2  # Should contain two elements as hash value of review 3 differs from 1 and 2.


def test_review_set_owner(sample_podcasts, sample_episodes):
    podcast = (sample_podcasts[0])
    episode = (sample_episodes[0])
    user1 = User(1, "Dhiren", "pw12345")
    user2 = User(2, "Chris", "pw67890")

    review1 = Review(1, user1, podcast, episode, 3, "Good Podcast")

    review1.owner = user2
    assert review1.owner == user2

    with pytest.raises(TypeError):
        review1.owner = ""


def test_review_set_podcast(sample_podcasts, sample_episodes):
    podcast = (sample_podcasts[0])
    podcast2 = (sample_podcasts[1])
    episode = (sample_episodes[0])
    user1 = User(1, "Dhiren", "pw12345")
    review1 = Review(1, user1, podcast, episode, 3, "Good Podcast")

    review1.podcast = podcast2
    assert review1.podcast == podcast2

    with pytest.raises(TypeError):
        review1.podcast = ""


def test_review_set_episode(sample_podcasts, sample_episodes):
    podcast = (sample_podcasts[0])
    episode = (sample_episodes[0])
    episode2 = (sample_episodes[1])

    user1 = User(1, "Dhiren", "pw12345")

    review1 = Review(1, user1, podcast, episode, 3, "Good Podcast")

    review1.episode = episode2
    assert review1.episode == episode2

    review1.episode = None
    assert review1.episode is None


def test_review_set_rating(sample_podcasts, sample_episodes):
    podcast = (sample_podcasts[0])
    episode = (sample_episodes[0])

    user1 = User(1, "Dhiren", "pw12345")

    review1 = Review(1, user1, podcast, episode, 3, "Good Podcast")

    review1.rating = 5
    assert review1.rating == 5

    with pytest.raises(ValueError):
        review1.rating = 6
        review1.rating = -1


def test_review_set_review_content(sample_podcasts, sample_episodes):
    podcast = (sample_podcasts[0])
    episode = (sample_episodes[0])

    user1 = User(1, "Dhiren", "pw12345")
    review1 = Review(1, user1, podcast, episode, 3, "Good Podcast")

    review1.review_content = "Listening to the first epsiode right now! loving it!"
    assert review1.review_content == "Listening to the first epsiode right now! loving it!"

    review1.review_content = "   Great Podcast!    "
    assert review1.review_content == "Great Podcast!"

    with pytest.raises(ValueError):
        review1.review_content = ""


# TODO : CSV READER TEST

def test_csv_data_reader(csv_file_paths):
    podcast_filename, episode_filename = csv_file_paths
    csv_reader = CSVDataReader(podcast_filename, episode_filename)

    # Test reading podcast CSV
    csv_reader.read_podcasts_csv()
    podcasts = csv_reader.dataset_of_podcasts
    assert len(csv_reader.dataset_of_podcasts) == 3  # Assuming there are 3 podcasts in the file
    assert podcasts[0].title == "D-Hour Radio Network"

    # Assuming 'name' is the correct attribute for the author in the Author class
    assert podcasts[1].author.name == "Brian Denny"

    assert len(podcasts[0].categories) == 2  # Society & Culture, Personal Journals

    # Test reading episodes CSV
    csv_reader.read_episodes_csv()
    episodes = csv_reader.dataset_of_episodes
    assert len(episodes) == 3  # Assuming 3 episodes in the file
    assert episodes[0].title == "The Mandarian Orange Show Episode 74- Bad Hammer Time"
    assert episodes[0].audio_length == 100
    assert episodes[1].title == "Finding yourself in the character by justifying your actions"
