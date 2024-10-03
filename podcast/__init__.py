"""Initialize Flask app."""
from pathlib import Path

from flask import Flask, render_template, request
import podcast.adapters.repository as repo
from podcast.adapters.datareader.csvdatareader import CSVDataReader
from podcast.adapters.memory_repository import MemoryRepository, populate

# TODO: Access to the podcast should be implemented via the repository pattern and using blueprints, so this can not
#  stay here!
from podcast.domainmodel.model import Podcast, Author, Episode


def create_app(test_config=None):
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)

    # Configure the app from configuration-file settings.
    app.config.from_object('config.Config')
    data_path = Path('podcast') / 'adapters' / 'data'

    if test_config is not None:
        # Load test configuration, and override any configuration settings.
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']

    # Create the MemoryRepository implementation for a memory-based repository.
    repo.repo_instance = MemoryRepository()
    # fill the content of the repository from the provided csv files, false because its not debuging
    populate(repo.repo_instance, False)
        
    with app.app_context():
        from .home import home
        app.register_blueprint(home.home_blueprint)

    with app.app_context():
        from .description import description
        app.register_blueprint(description.description_blueprint)

    with app.app_context():
        from .catalogue import catalogue
        app.register_blueprint(catalogue.catalogue_blueprint)

    with app.app_context():
        from podcast.playlist.playlist import playlist_blueprint
        app.register_blueprint(playlist_blueprint, url_prefix='/playlist')

    with app.app_context():
        from .authentication import authentication
        app.register_blueprint(authentication.authentication_blueprint)

    return app


