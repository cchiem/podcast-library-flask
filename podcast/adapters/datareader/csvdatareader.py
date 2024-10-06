import os
import csv
from pathlib import Path

from podcast.domainmodel.model import Podcast, Episode, Author, Category


class CSVDataReader:
    def __init__(self, podcast_filename, episode_filename):
        # dir_name = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '.'))
        self.__podcast_filename = podcast_filename
        self.__episode_filename = episode_filename
        self.__dataset_of_podcasts = []
        self.__dataset_of_episodes = []
        self.__dataset_of_authors = set()
        self.__dataset_of_categories = set()

    @property
    def dataset_of_podcasts(self) -> list:
        return self.__dataset_of_podcasts

    @property
    def dataset_of_episodes(self) -> list:
        return self.__dataset_of_episodes

    @property
    def dataset_of_authors(self) -> set:
        return self.__dataset_of_authors

    @property
    def dataset_of_categories(self) -> set:
        return self.__dataset_of_categories

    def read_podcasts_csv(self):
        if not os.path.exists(self.__podcast_filename):
            print(f"path {self.__podcast_filename} does not exist!")
            return
        with open(self.__podcast_filename, "r", encoding='utf-8-sig') as podcast_file:
            podcasts_rows = csv.DictReader(podcast_file)
            author_count = 1
            category_count = 1
            for row in podcasts_rows:
                try:
                    podcast_id = int(row["id"])
                    podcast_title = row["title"]
                    podcast = Podcast(podcast_id, podcast_title)

                    author = Author(author_count, row["author"])
                    if author not in self.__dataset_of_authors:
                        author_count += 1
                        self.__dataset_of_authors.add(author)
                    else:
                        # Retrieve the existing author from the set to associate with the podcast
                        for existing_author in self.__dataset_of_authors:
                            if existing_author == author:
                                author = existing_author
                                break
                    podcast.author = author

                    podcast.description = row["description"]
                    podcast.image = "/static/images/"+ author.name + ".jpg"
                    podcast.language = row["language"]
                    podcast.website = row["website"]
                    podcast.itunes_id = row["itunes_id"]

                    category_names = row["categories"].split("|")
                    for category_name in category_names:
                        category = Category(category_count, category_name.strip())
                        if category not in self.__dataset_of_categories:
                            self.__dataset_of_categories.add(category)
                            category_count += 1
                        else:
                            # Retrieve the existing category from the set to associate with the podcast
                            for existing_category in self.__dataset_of_categories:
                                if existing_category == category:
                                    category = existing_category
                                    break
                        podcast.add_category(category)

                    self.__dataset_of_podcasts.append(podcast)

                except ValueError as e:
                    # print(f"Skipping row due to invalid data: {e}")
                    pass
                except KeyError as e:
                    # print(f"Skipping row due to missing key: {e}")
                    pass

    def read_episodes_csv(self):
        # Create a dictionary for quick lookup of podcasts by their id
        podcast_lookup = {p.id: p for p in self.__dataset_of_podcasts}

        with open(self.__episode_filename, "r", encoding='utf-8-sig') as episode_file:
            # id,podcast_id,title,audio,audio_length,description,pub_date
            episodes_rows = csv.DictReader(episode_file)

            # Iterate through all rows in the CSV
            for row in episodes_rows:
                episode_id = int(row["id"])
                podcast_id = int(row["podcast_id"])  # Podcast ID for the current episode

                # Efficient lookup for the podcast using the dictionary
                podcast = podcast_lookup.get(podcast_id)

                # Ensure the podcast was found
                if podcast is not None:
                    title = row["title"]
                    audio = row["audio"]
                    audio_length = int(row["audio_length"])
                    description = row["description"]
                    pub_date = row["pub_date"]


                    # Create episode object
                    episode = Episode(episode_id, podcast, title, audio, audio_length, description, pub_date)

                    # Add the episode to the podcast and repository
                    podcast.add_episode(episode)
                    self.__dataset_of_episodes.append(episode)
