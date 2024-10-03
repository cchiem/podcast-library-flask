from __future__ import annotations
import datetime
from datetime import datetime
from bisect import insort_left


def validate_non_negative_int(value):
    if not isinstance(value, int) or value < 0:
        raise ValueError("ID must be a non-negative integer.")

def validate_non_empty_string(value, field_name="value"):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


class Author:

    def __init__(self, author_id: int, name: str):
        if author_id is not None:
            validate_non_negative_int(author_id)
        validate_non_empty_string(name, "Author name")
        self._id = author_id
        self._name = name.strip()
        self.podcast_list = []

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str):
        validate_non_empty_string(new_name, "New name")
        self._name = new_name.strip()

    def add_podcast(self, podcast: Podcast):
        if not isinstance(podcast, Podcast):
            raise TypeError("Expected a Podcast instance.")
        if podcast not in self.podcast_list:
            self.podcast_list.append(podcast)

    def remove_podcast(self, podcast: Podcast):
        if podcast in self.podcast_list:
            self.podcast_list.remove(podcast)

    def __repr__(self) -> str:
        return f"<Author {self._id}: {self._name}>"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Author):
            return False
        return self.name == other.name

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Author):
            return False
        return self.name < other.name

    def __hash__(self) -> int:
        return hash(self.name)


class Podcast:
    # def __init__(self, podcast_id: int, author: Author, title: str = "Untitled", image: str = None,
    #              description: str = "", website: str = "", itunes_id: int = None, language: str = "Unspecified"):
    def __init__(self, podcast_id: int, podcast_title: str):
        validate_non_negative_int(podcast_id)
        self._id = podcast_id

        validate_non_empty_string(podcast_title, "Podcast title")
        self._title = podcast_title.strip()

        self._author = None
        self._image = None
        self._description = None
        self._language = None
        self._website = None
        self._itunes_id = None
        self._categories = []
        self._episodes = []
        self._reviews = []

    @property
    def id(self) -> int:
        return self._id

    @property
    def author(self) -> Author:
        return self._author

    @property
    def episodes(self) -> list:  # Return the list of episodes
        return self._episodes

    @author.setter
    def author(self, author: Author):
        if isinstance(author, Author):
            self._author = author
        else:
            self._author = None

    @property
    def itunes_id(self) -> int:
        return self._itunes_id

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, new_title: str):
        validate_non_empty_string(new_title, "Podcast title")
        self._title = new_title.strip()

    @property
    def image(self) -> str:
        return self._image

    @image.setter
    def image(self, new_image: str):
        if new_image is not None and not isinstance(new_image, str):
            raise TypeError("Podcast image must be a string or None.")
        self._image = new_image

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, new_description: str):
        if not isinstance(new_description, str):
            validate_non_empty_string(new_description, "Podcast description")
        self._description = new_description

    @property
    def language(self) -> str:
        return self._language

    @language.setter
    def language(self, new_language: str):
        if not isinstance(new_language, str):
            raise TypeError("Podcast language must be a string.")
        self._language = new_language

    @property
    def website(self) -> str:
        return self._website

    @website.setter
    def website(self, new_website: str):
        validate_non_empty_string(new_website, "Podcast website")
        self._website = new_website

    @itunes_id.setter
    def itunes_id(self, value):
        self._itunes_id = value

    @property
    def categories(self) -> list:
        return self._categories

    @property
    def reviews(self) -> list:
        return self._reviews

    def add_category(self, category: Category):
        if not isinstance(category, Category):
            raise TypeError("Expected a Category instance.")
        if category not in self._categories:
            self._categories.append(category)

    def remove_category(self, category: Category):
        if category in self._categories:
            self._categories.remove(category)

    def add_episode(self, episode: Episode):
        if not isinstance(episode, Episode):
            raise TypeError("Expected an Episode instance.")
        if episode not in self._episodes:
            insort_left(self._episodes,episode)

    def remove_episode(self, episode: Episode):
        if episode in self._episodes:
            self._episodes.remove(episode)

    def add_review(self, review: Review):
        if not isinstance(review, Review):
            raise TypeError("Expected a Review instance.")
        self.reviews.append(review)

    def remove_review(self, review: Review):
        if review in self.reviews:
            self.reviews.remove(review)

    def get_podcast_average_rating(self):
        if len(self.reviews) == 0:
            return 0
        rating_total = 0
        ratings = 0
        for review in self.reviews:
            rating_total += review.rating
            ratings += 1
        return round(rating_total / ratings, 1)

    def __repr__(self):
        return f"<Podcast {self.id}: '{self.title}' by {self.author.name}>"

    def __eq__(self, other):
        if not isinstance(other, Podcast):
            return False
        return self.id == other.id

    def __lt__(self, other):
        if not isinstance(other, Podcast):
            return False
        return self.title < other.title

    def __hash__(self):
        return hash(self.id)


class Category:
    def __init__(self, category_id: int, name: str):
        validate_non_negative_int(category_id)
        validate_non_empty_string(name, "Category name")
        self._id = category_id
        self._name = name.strip()

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str):
        validate_non_empty_string(new_name, "New name")
        self._name = new_name.strip()

    def __repr__(self) -> str:
        return f"<Category {self._id}: {self._name}>"

    def __eq__(self, other):
        if not isinstance(other, Category):
            return False
        return self.id == other.id

    def __lt__(self, other):
        if not isinstance(other, Category):
            return False
        return self._name < other.name

    def __hash__(self):
        return hash(self._id)


class User:
    def __init__(self, user_id: int, username: str, password: str):
        validate_non_negative_int(user_id)
        validate_non_empty_string(username, "Username")
        validate_non_empty_string(password, "Password")
        self._id = user_id
        self._username = username.lower().strip()
        self._password = password
        self._subscription_list = []
        self._playlist = Playlist(1, ("Playlist: " + username), self, [])

    @property
    def playlist(self) -> list:
        return self._playlist
    @property
    def id(self) -> int:
        return self._id

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password

    @property
    def subscription_list(self):
        return self._subscription_list

    def add_subscription(self, subscription: PodcastSubscription):
        if not isinstance(subscription, PodcastSubscription):
            raise TypeError("Subscription must be a PodcastSubscription object.")
        if subscription not in self._subscription_list:
            self._subscription_list.append(subscription)

    def remove_subscription(self, subscription: PodcastSubscription):
        if subscription in self._subscription_list:
            self._subscription_list.remove(subscription)

    def __repr__(self):
        return f"<User {self.id}: {self.username}>"

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return self.id == other.id

    def __lt__(self, other):
        if not isinstance(other, User):
            return False
        return self.id < other.id

    def __hash__(self):
        return hash(self.id)


class PodcastSubscription:
    def __init__(self, sub_id: int, owner: User, podcast: Podcast):
        validate_non_negative_int(sub_id)
        if not isinstance(owner, User):
            raise TypeError("Owner must be a User object.")
        if not isinstance(podcast, Podcast):
            raise TypeError("Podcast must be a Podcast object.")
        self._id = sub_id
        self._owner = owner
        self._podcast = podcast

    @property
    def id(self) -> int:
        return self._id

    @property
    def owner(self) -> User:
        return self._owner

    @owner.setter
    def owner(self, new_owner: User):
        if not isinstance(new_owner, User):
            raise TypeError("Owner must be a User object.")
        self._owner = new_owner

    @property
    def podcast(self) -> Podcast:
        return self._podcast

    @podcast.setter
    def podcast(self, new_podcast: Podcast):
        if not isinstance(new_podcast, Podcast):
            raise TypeError("Podcast must be a Podcast object.")
        self._podcast = new_podcast

    def __repr__(self):
        return f"<PodcastSubscription {self.id}: Owned by {self.owner.username}>"

    def __eq__(self, other):
        if not isinstance(other, PodcastSubscription):
            return False
        return self.id == other.id and self.owner == other.owner and self.podcast == other.podcast

    def __lt__(self, other):
        if not isinstance(other, PodcastSubscription):
            return False
        return self.id < other.id

    def __hash__(self):
        return hash((self.id, self.owner, self.podcast))


class Episode:
    def __init__(self, id: int, podcast: Podcast, title: str = "Untitled", audio: str = "", audio_length: int = 0,
                 description: str = "", pub_date: datetime = None):
        validate_non_negative_int(id)
        validate_non_empty_string(title)
        self.__id = id
        self.__podcast = podcast
        self.__title = title
        self.__audio = audio
        self.__audio_length = audio_length
        self.__description = description
        self.__pub_date = pub_date if pub_date else datetime.now()

    @property
    def id(self) -> int:
        return self.__id

    @id.setter
    def id(self, new_id: int):
        if not isinstance(new_id, int):
            raise TypeError("Episode.id must be an int type!")
        if new_id < 0:
            raise ValueError("To avoid confusion, Episode.id cannot be a negative integer.")
        self.__id = new_id

    @property
    def podcast(self) -> Podcast:
        return self.__podcast

    @podcast.setter
    def podcast(self, new_podcast: Podcast):
        if not isinstance(new_podcast, Podcast):
            raise TypeError("Episode.podcast must be a Podcast type!")
        self.__podcast = new_podcast

    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, new_title: str):
        if not isinstance(new_title, str):
            raise TypeError("Episode.title must be a str type!")
        if len(new_title) == 0:
            raise ValueError("Episode.title must not be an empty string.")
        self.__title = new_title

    @property
    def audio(self) -> str:
        return self.__audio

    @audio.setter
    def audio(self, new_audio: str):
        if not isinstance(new_audio, str):
            raise TypeError("Episode.audio must be a str type!")
        self.__audio = new_audio

    @property
    def audio_length(self) -> int:
        return self.__audio_length

    @audio_length.setter
    def audio_length(self, new_length: int):
        if not isinstance(new_length, int):
            raise TypeError("Episode.audio_length must be an int type!")
        if new_length < 0:
            raise ValueError("Episode.audio_length must not be less than 0.")
        self.__audio_length = new_length

    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, new_desc: str):
        if not isinstance(new_desc, str):
            raise TypeError("Episode.description must be a str type!")
        self.__description = new_desc

    @property
    def pub_date(self) -> str:
        return self.__pub_date

    @pub_date.setter
    def pub_date(self, new_date: str):
        if not isinstance(new_date, str):
            raise TypeError("Episode.pub_date must be a str type!")
        try:
            datetime.strptime(new_date, "%Y-%m-%d %H:%M:%S+00")
        except ValueError:
            raise ValueError("Episode.pub_date must be in the following format: YY-MM-DD HH:MM:SS+00!")

    def __repr__(self):
        return f"<Episode {self.id} | From \"{self.podcast}\">"

    def __eq__(self, other: 'Episode'):
        if not isinstance(other, Episode):
            return False
        # Episodes are considered equal if both podcast id and episode id are the same
        return self.podcast.id == other.podcast.id and self.id == other.id

    def __lt__(self, other: 'Episode'):
        if not isinstance(other, Episode):
            return False
        # First compare by podcast id, then by episode id within the same podcast
        if self.podcast.id == other.podcast.id:
            return self.title < other.title
        return self.podcast.id < other.podcast.id

    def __hash__(self):
        return hash((self.id, self.podcast.id))


class Review:
    # TODO: Complete the implementation of the Review class.
    def __init__(self, new_review_id: int, owner: User, podcast: Podcast, episode: (Episode or None), rating: int,
                 review_content: str):

        validate_non_negative_int(new_review_id)
        if not isinstance(owner, User):
            raise TypeError("Owner must be a User object.")
        if not isinstance(podcast, Podcast):
            raise TypeError("Podcast must be a Podcast object.")
        if not isinstance(episode, Episode) and not (episode is None):
            raise TypeError("Episode must be a Episode object or None.")
        validate_non_negative_int(rating)
        if rating > 5:
            raise ValueError("Rating must be less than 5.")
        # check what range is needed and if range must be checked for.
        validate_non_empty_string(review_content)
        self._id = new_review_id
        self._owner = owner
        self._podcast = podcast
        self._episode = episode
        self._rating = rating
        self._review_content = review_content
        self._date = datetime.now()

    @property
    def id(self) -> int:
        return self._id

    @property
    def owner(self) -> User:
        return self._owner

    @property
    def podcast(self) -> Podcast:
        return self._podcast

    @property
    def episode(self) -> Episode:
        return self._episode

    @property
    def rating(self) -> int:
        return self._rating

    @property
    def review_content(self) -> str:
        return self._review_content

    # insert methods here

    @owner.setter
    def owner(self, new_owner: User):
        if not isinstance(new_owner, User):
            raise TypeError("Owner must be a User object.")
        self._owner = new_owner

    @podcast.setter
    def podcast(self, new_podcast: Podcast):
        if not isinstance(new_podcast, Podcast):
            raise TypeError("Podcast must be a Podcast object.")
        self._podcast = new_podcast

    @episode.setter
    def episode(self, new_episode: Episode):
        if not isinstance(new_episode, Episode) and not (new_episode is None):
            raise TypeError("Episode must be a Episode object or None.")
        self._episode = new_episode

    @rating.setter
    def rating(self, new_rating: int):
        validate_non_negative_int(new_rating)
        if new_rating > 5:
            raise ValueError("Rating must be less than 5.")
        self._rating = new_rating

    @review_content.setter
    def review_content(self, new_review_content: str):
        validate_non_empty_string(new_review_content)
        self._review_content = new_review_content.strip()

    @property
    def date(self) -> str:
        return self._date.strftime("%d/%m/%y, %H:%M")

    @date.setter
    def date(self, new_date: str):
        if not isinstance(new_date, str):
            raise TypeError("Episode.pub_date must be a str type!")
        try:
            datetime.strptime(new_date, "%Y-%m-%d %H:%M:%S+00")
        except ValueError:
            raise ValueError("Episode.pub_date must be in the following format: YY-MM-DD HH:MM:SS+00!")

    def __repr__(self):
        return (f"<Review: {self._id}, Owner: {self._owner.id}, Podcast: {self._podcast.id}, Episode: {self._episode.id if self._episode else None}, "
                f"Rating: {self._rating}>")

    def __eq__(self, other):
        # equality determined by id, owner and podcast
        if isinstance(other, Review):
            if self._id == other._id and self._owner == other._owner and self._podcast == other._podcast:
                return True
        return False

    def __lt__(self, other):
        if not isinstance(other, Review):
            return False
        return self._rating < other._rating

    def __hash__(self):
        return hash((self._id, self._owner, self._podcast))


class Playlist:
    def __init__(self, playlist_id: int, playlist_name: str, owner: User, episodes_list: list):
        validate_non_negative_int(playlist_id)
        validate_non_empty_string(owner.username)
        validate_non_empty_string(playlist_name)

        self._playlist_id = playlist_id
        self._playlist_name = playlist_name
        self._owner = owner
        self._episodes_list = episodes_list

    @property
    def playlist_id(self) -> int:
        return self._playlist_id

    @property
    def playlist_name(self) -> str:
        return self._playlist_name

    @property
    def owner(self) -> User:
        return self._owner

    @property
    def episode_list(self) -> list:
        return self._episodes_list

    @property
    def playlist(self) -> list:
        return self._episodes_list

    @property
    def playlist_length(self) -> int:
        return len(self._episodes_list)

    @playlist_id.setter
    def playlist_id(self, new_playlist_id: int):
        validate_non_negative_int(new_playlist_id)
        self._playlist_id = new_playlist_id

    @playlist_name.setter
    def playlist_name(self, new_playlist_name: str):
        validate_non_empty_string(new_playlist_name, "New playlist name")
        self._playlist_name = new_playlist_name

    @owner.setter
    def owner(self, new_owner: User):
        validate_non_empty_string(new_owner.username, "New owner name")
        self._owner = new_owner
        # assuming that owners being added will check the name to make sure its not null
    
    def add_episode(self, episode: Episode):
        if not isinstance(episode, Episode):
            raise TypeError("Expected an Episode instance.")
        if episode not in self._episodes_list:
            self._episodes_list.append(episode)

    def remove_episode(self, episode: Episode):
        if not isinstance(episode, Episode):
            raise TypeError("Expected an Episode instance.")
        if episode in self._episodes_list:
            self._episodes_list.remove(episode)
    def remove_episode_by_id(self, episode_id: int):
        for ep in self._episodes_list:
            if ep.id == episode_id:
                self._episodes_list.remove(ep)

    def __lt__(self, other):
        if not isinstance(other, Playlist):
            return NotImplemented
        return len(self._episodes_list) < len(other._episodes_list)

    def __eq__(self, other):
        if not isinstance(other, Playlist):
            return NotImplemented
        return (self.playlist_id == other.playlist_id and
                self.playlist_name == other.playlist_name and
                self.owner == other.owner and
                self.playlist == other.playlist)

    def __repr__(self):
        return (f"Playlist({self.playlist_id}, '{self.playlist_name}', "
                f"Owner: {self.owner.username}, Episodes: {len(self.playlist)})")

    def __hash__(self):
        return hash((self.playlist_id, self.playlist_name, self.owner.username))

