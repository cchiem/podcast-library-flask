
from flask import Blueprint, render_template, request, session
import random
import podcast.adapters.repository as repo
import podcast.home.service as services

home_blueprint = Blueprint('home_bp', __name__)

@home_blueprint.route('/', methods=['GET', 'POST'])
def home():
    randomPodcasts = services.get_random_podcasts(repo.repo_instance)
    if 'username' in session:
        username = session['username']
    else:
        username = None
    return render_template(
        'home.html',
        podcastList=randomPodcasts,
        username=username
    )

