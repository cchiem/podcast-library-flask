from flask import Blueprint, render_template, request, session, redirect, url_for, flash
import podcast.adapters.repository as repo
import podcast.catalogue.service as services

catalogue_blueprint = Blueprint('catalogue_bp', __name__)

@catalogue_blueprint.route('/catalogue', methods=['GET', 'POST'])
def catalogue():
    if 'username' in session:
        username = session['username']
        user = services.get_user(repo.repo_instance, username)  # Fetch the user
    else:
        username = None
        user = None
        
    # Capture the search query and filter criteria from the request
    search_query = request.args.get('q', '')
    filter_by = request.args.get('filter_by', 'title')

    # Get the full list of podcasts
    podcastList = services.get_podcasts(repo.repo_instance)

    # Apply filtering based on the selected criteria
    if search_query:
        search_query_lower = search_query.lower()

        if filter_by == 'title':
            podcastList = [podcast for podcast in podcastList if search_query_lower in podcast.title.lower()]
        elif filter_by == 'category':
            podcastList = [podcast for podcast in podcastList if any(search_query_lower in category.name.lower() for category in podcast.categories)]
        elif filter_by == 'author':
            podcastList = [podcast for podcast in podcastList if search_query_lower in podcast.author.name.lower()]

    # Pagination logic
    page = request.args.get('page', 1, type=int)
    per_page = 20
    start = (page - 1) * per_page
    end = start + per_page
    total_pages = (len(podcastList) + per_page - 1) // per_page
    items_on_page = podcastList[start:end]

    return render_template(
        'catalogue.html',
        items_on_page=items_on_page,
        total_pages=total_pages,
        page=page,
        search_query=search_query,  # Pass the search query to the template
        filter_by=filter_by,  # Pass the selected filter to the template for persistence
        username=username,
        user=user
    )

@catalogue_blueprint.route('/add_to_playlist/<int:podcast_id>', methods=['POST'])
def add_to_playlist(podcast_id):
    if 'username' not in session:
        flash('You need to be logged in to add podcasts to your playlist.', 'error')
        return redirect(url_for('catalogue_bp.catalogue'))

    username = session['username']
    user = services.get_user(repo.repo_instance, username)  # Fetch the user
    podcast = services.get_podcast_by_id(repo.repo_instance, podcast_id)  # Fetch the podcast object by its ID

    if podcast is None:
        flash('Podcast not found.', 'error')
        return redirect(url_for('catalogue_bp.catalogue'))

    # Add the podcast to the user's playlist
    services.add_to_user_playlist(repo.repo_instance, user, podcast)
    flash('Podcast added to your playlist!', 'success')

    # Redirect back to the catalogue page
    search_query = request.args.get('q', '')
    filter_by = request.args.get('filter_by', 'title')
    page = request.args.get('page', 1)

    return redirect(url_for('catalogue_bp.catalogue', q=search_query, filter_by=filter_by, page=page))
