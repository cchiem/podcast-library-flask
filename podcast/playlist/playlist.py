from flask import Blueprint, render_template, session, redirect, url_for, request, flash
import podcast.playlist.service as services
import podcast.adapters.repository as repo
from podcast.domainmodel.model import User
from podcast.authentication.authentication import login_required

playlist_blueprint = Blueprint('playlist_bp', __name__)

@playlist_blueprint.route('/', methods=['GET', 'POST'])
@login_required
def playlist():
    # Check if the user is logged in
    if 'username' not in session:
        return redirect(url_for('authentication_bp.login'))

    else:
        username = session['username']
        user = services.get_user(repo.repo_instance, username)
        playlist = user.playlist
        episodes = playlist.playlist  # Access the episodes

        # Pagination logic
        page = request.args.get('page', 1, type=int)
        per_page = 10
        start = (page - 1) * per_page
        end = start + per_page
        total_pages = (playlist.playlist_length + per_page - 1) // per_page
        items_on_page = episodes[start:end]

        # Render the playlist template
        return render_template(
            'playlist.html',
            username=username,
            playlist=playlist,
            items_on_page=items_on_page,
            total_pages=total_pages,
            page=page
        )


@playlist_blueprint.route('/remove_episode_from_user_playlist/<int:episode_id>', methods=['POST'])
@login_required
def remove_episode_from_user_playlist(episode_id):
    # Check if the user is logged in
    if 'username' not in session:
        return redirect(url_for('authentication_bp.login'))
    
    username = session['username']
    user = services.get_user(repo.repo_instance, username)

    # Call a service function to remove the podcast from the user's playlist
    services.remove_episode_from_user_playlist(repo.repo_instance, user, episode_id)
    flash("Episode removed")
    return redirect(url_for('playlist_bp.playlist'))
