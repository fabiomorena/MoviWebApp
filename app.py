from flask import Flask, render_template, request, redirect, url_for, flash
import requests
import os
from data_manager import DataManager
from models import db
import logging
import secrets

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///moviwebapp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = secrets.token_hex(16)  # Generate random secret key

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize database with app
db.init_app(app)

# Initialize DataManager
data_manager = DataManager()

# Hardcoded movie data for common movies (fallback when OMDb fails)
MOVIE_DATABASE = {
    'jaws': {
        'title': 'Jaws',
        'director': 'Steven Spielberg',
        'year': 1975,
        'rating': 8.0,
        'poster_url': 'https://m.media-amazon.com/images/M/MV5BNjQwNDI3MzYtZGQxMC00NGIwLWIyZjAtY2FmZTg3ZmU4ODA5XkEyXkFqcGdeQXVyNTAyODk3OTY@._V1_SX300.jpg'
    },
    'the godfather': {
        'title': 'The Godfather',
        'director': 'Francis Ford Coppola',
        'year': 1972,
        'rating': 9.2,
        'poster_url': 'https://m.media-amazon.com/images/M/MV5BM2MyNjYxNmUtYTAwNi00MTYxLWJmNWYtYzZlODY3ZTk3OTFlXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_SX300.jpg'
    },
    'star wars': {
        'title': 'Star Wars',
        'director': 'George Lucas',
        'year': 1977,
        'rating': 8.6,
        'poster_url': 'https://m.media-amazon.com/images/M/MV5BNzVlY2MwMjktM2E4OS00Y2Y3LWE3ZjctYzhkZGM3YzA1ZWM2XkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_SX300.jpg'
    },
    'pulp fiction': {
        'title': 'Pulp Fiction',
        'director': 'Quentin Tarantino',
        'year': 1994,
        'rating': 8.9,
        'poster_url': 'https://m.media-amazon.com/images/M/MV5BNGNhMDIzZTUtNTBlZi00MTRlLWFjM2ItYzViMjE3YzI5MjljXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_SX300.jpg'
    }
}


def fetch_movie_from_omdb(title):
    """Fetch movie information from OMDb API with fallback to hardcoded data"""
    try:
        # First, try to find in our hardcoded database
        normalized_title = title.lower().strip()
        if normalized_title in MOVIE_DATABASE:
            logger.info(f"Using hardcoded data for '{title}'")
            return MOVIE_DATABASE[normalized_title]

        # Try OMDb API
        api_key = 'db7f2332'  # Your API key
        if api_key:
            url = f"http://www.omdbapi.com/?t={title}&apikey={api_key}"
            response = requests.get(url, timeout=5)

            if response.status_code == 200:
                data = response.json()
                if data.get('Response') == 'True':
                    return {
                        'title': data.get('Title', title),
                        'director': data.get('Director', 'N/A'),
                        'year': int(data.get('Year', 0)) if data.get('Year', '0').isdigit() else 0,
                        'rating': float(data.get('imdbRating', 0)) if data.get('imdbRating', '0') != 'N/A' else 0.0,
                        'poster_url': data.get('Poster', '')
                    }
                else:
                    logger.warning(f"OMDb API error for '{title}': {data.get('Error', 'Unknown error')}")

        # Fallback: return basic data with default poster
        logger.info(f"Using fallback data for '{title}'")
        return {
            'title': title.title(),
            'director': 'Unknown Director',
            'year': 2020,
            'rating': 7.0,
            'poster_url': 'https://m.media-amazon.com/images/M/MV5BNjQwNDI3MzYtZGQxMC00NGIwLWIyZjAtY2FmZTg3ZmU4ODA5XkEyXkFqcGdeQXVyNTAyODk3OTY@._V1_SX300.jpg'
            # Jaws poster as default
        }

    except Exception as e:
        logger.error(f"Error fetching movie data for '{title}': {str(e)}")
        # Return fallback data
        return {
            'title': title.title(),
            'director': 'Unknown Director',
            'year': 2020,
            'rating': 7.0,
            'poster_url': 'https://m.media-amazon.com/images/M/MV5BNjQwNDI3MzYtZGQxMC00NGIwLWIyZjAtY2FmZTg3ZmU4ODA5XkEyXkFqcGdeQXVyNTAyODk3OTY@._V1_SX300.jpg'
        }


# Home route - redirects to users list
@app.route('/')
def home():
    return redirect(url_for('list_users'))


# List all users
@app.route('/users')
def list_users():
    try:
        users = data_manager.get_users()
        return render_template('index.html', users=users)
    except Exception as e:
        logger.error(f"Error fetching users: {str(e)}")
        flash("Unable to load users at this time.", "error")
        return render_template('index.html', users=[])


# Get movies for a specific user
@app.route('/users/<int:user_id>')
def get_user_movies(user_id):
    try:
        user = data_manager.get_user(user_id)
        if not user:
            flash("User not found.", "error")
            return render_template('404.html'), 404

        movies = data_manager.get_movies(user_id)
        return render_template('user_movies.html', user=user, movies=movies)
    except Exception as e:
        logger.error(f"Error fetching movies for user {user_id}: {str(e)}")
        flash("Unable to load movies at this time.", "error")
        return render_template('user_movies.html', user=user or {}, movies=[])


# Create a new user
@app.route('/users/new', methods=['POST'])
def create_user():
    try:
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        # Validate input
        if not name or not email or not password:
            flash("All fields are required.", "error")
            return redirect(url_for('list_users'))

        if len(password) < 6:
            flash("Password must be at least 6 characters long.", "error")
            return redirect(url_for('list_users'))

        data_manager.create_user(name, email, password)
        flash(f"User '{name}' created successfully!", "success")
        return redirect(url_for('list_users'))

    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        flash("Unable to create user. Please try again.", "error")
        return redirect(url_for('list_users'))


# Add a movie to a user's collection
@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie(user_id):
    try:
        # Validate user exists
        user = data_manager.get_user(user_id)
        if not user:
            flash("User not found.", "error")
            return redirect(url_for('list_users'))

        title = request.form.get('title', '').strip()
        if not title:
            flash("Movie title is required.", "error")
            return redirect(url_for('get_user_movies', user_id=user_id))

        # Fetch movie information (with fallback)
        movie_data = fetch_movie_from_omdb(title)

        # Add the movie to the user's collection
        data_manager.add_movie(movie_data, user_id)
        flash(f"Movie '{movie_data['title']}' added successfully!", "success")
        return redirect(url_for('get_user_movies', user_id=user_id))

    except Exception as e:
        logger.error(f"Error adding movie for user {user_id}: {str(e)}")
        flash("Unable to add movie. Please try again.", "error")
        return redirect(url_for('get_user_movies', user_id=user_id))


# Delete a movie
@app.route('/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(movie_id):
    try:
        # Get the movie first to know which user it belongs to
        movie = data_manager.get_movie(movie_id)
        if not movie:
            flash("Movie not found.", "error")
            return redirect(url_for('list_users'))

        user_id = movie.user_id
        if data_manager.delete_movie(movie_id):
            flash("Movie deleted successfully!", "success")
        else:
            flash("Unable to delete movie.", "error")

        return redirect(url_for('get_user_movies', user_id=user_id))

    except Exception as e:
        logger.error(f"Error deleting movie {movie_id}: {str(e)}")
        flash("Unable to delete movie. Please try again.", "error")
        return redirect(url_for('list_users'))


# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    try:
        # Create tables if they don't exist
        with app.app_context():
            db.create_all()

        # Run the Flask application
        app.run(debug=True)

    except Exception as e:
        logger.critical(f"Failed to start application: {str(e)}")
        print(f"Application failed to start: {str(e)}")
