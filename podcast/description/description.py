#CAHTa[soifgdh

from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import TextAreaField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange
import podcast.adapters.repository as repo
import podcast.description.service as services
from podcast.authentication.authentication import login_required

description_blueprint = Blueprint('description_bp', __name__)

class ReviewForm(FlaskForm):
    review_text = TextAreaField('Review', validators=[DataRequired(),
                                                   Length(min=4, message='Review must be at least 4 characters')])
    rating = IntegerField('Rating (1-5)', validators=[DataRequired(), NumberRange(min=1, max=5, message='Rating must be a whole number between 1 and 5.')])
    submit = SubmitField('Submit')

@description_blueprint.route('/description/<int:podcast_id>', methods=['GET'])
def description(podcast_id):
    if 'username' in session:
        username = session['username']
        saved_episodes = services.get_saved_episodes_for_user(repo.repo_instance, username)
        saved_episodes_by_id = [episode.id for episode in saved_episodes]
    else:
        username = None
        saved_episodes_by_id = None
    podcast = services.get_podcast_by_id(repo.repo_instance, podcast_id)
    episodes = services.get_episodes_for_podcast(repo.repo_instance, podcast_id)
    form = ReviewForm()

    return render_template(
        'podcastDescription.html',
        podcast=podcast,
        episodes=episodes,
        username=username,
        form=form,
        saved_episodes_by_id=saved_episodes_by_id
    )

@description_blueprint.route('/description/<int:podcast_id>/review', methods=['POST'])
@login_required
def leave_review_on_podcast(podcast_id):
    username = session['username']
    print(username)
    form = ReviewForm()

    if form.validate_on_submit():
        try:
            review_text = form.review_text.data
            rating = int(form.rating.data)
            services.add_review(repo.repo_instance, podcast_id, review_text, rating, username)
            flash("Review successfully added!", 'success')
            #print repo.repo_instance.get_podcast_by_id(podcast_id)

            # Redirect back to the description page after submitting the review
        except services.UserReviewAddedException:
            print("Exception occurred")
            flash("You have already added a review for this podcast.", 'error')
    return redirect(url_for('description_bp.description', podcast_id=podcast_id))



    # If the form is not valid, render the description page again with the form and errors
    podcast = services.get_podcast_by_id(repo.repo_instance, podcast_id)
    episodes = services.get_episodes_for_podcast(repo.repo_instance, podcast_id)
    saved_episodes = services.get_saved_episodes_for_user(repo.repo_instance, username)
    saved_episodes_by_id = [episode.id for episode in saved_episodes]

    return render_template(
        'podcastDescription.html',
        podcast=podcast,
        episodes=episodes,
        username=username,
        form=form,
        message="There was an error submitting your review.",
        saved_episodes_by_id=saved_episodes_by_id
    )

@description_blueprint.route('/description/<int:podcast_id>/<int:episode_id>', methods=['POST'])
@login_required
def add_to_playlist(podcast_id, episode_id):
    if 'username' not in session:
        flash('You need to be logged in to add podcasts to your playlist.', 'error')
        return redirect(url_for('catalogue_bp.catalogue'))

    username = session['username']
    user = services.get_user(repo.repo_instance, username)  # Fetch the user

    # Fetch the episode to add to the user's playlist
    episode = services.get_episode_by_id(repo.repo_instance, episode_id)

    if episode is None:
        flash('Episode not found.', 'error')
        return redirect(url_for('description_bp.description', podcast_id=podcast_id))

    # Add the episode to the user's playlist
    user_playlist = user.playlist
    user_playlist.add_episode(episode)
    flash('Episode added to your playlist!', 'success')

    # Redirect back to the podcast description page
    return redirect(url_for('description_bp.description', podcast_id=podcast_id))


@description_blueprint.route('/description/remove/<int:podcast_id>/<int:review_id>', methods=['POST'])
@login_required
def remove_review(podcast_id, review_id):
    # Check if the user is logged in
    if 'username' not in session:
        return redirect(url_for('authentication_bp.login'))

    username = session['username']
    user = services.get_user(repo.repo_instance, username)

    # Call a service function to remove the podcast from the user's playlist
    services.remove_review(repo.repo_instance, user, podcast_id, review_id)
    flash("Review removed")
    return redirect(url_for('description_bp.description', podcast_id=podcast_id))
