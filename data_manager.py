from models import db, User, Movie


class DataManager:
    def __init__(self):
        pass

    def create_user(self, name, email, password):
        """Add a new user to the database"""
        new_user = User(username=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    def get_users(self):
        """Return a list of all users in the database"""
        return User.query.all()

    def get_user(self, user_id):
        """Return a specific user by ID"""
        return User.query.get(user_id)

    def get_movies(self, user_id):
        """Return a list of all movies of a specific user"""
        return Movie.query.filter_by(user_id=user_id).all()

    def add_movie(self, movie_data, user_id):
        """Add a new movie to a user's collection"""
        new_movie = Movie(
            title=movie_data.get('title'),
            director=movie_data.get('director'),
            year=movie_data.get('year'),
            rating=movie_data.get('rating'),
            poster_url=movie_data.get('poster_url'),
            user_id=user_id
        )
        db.session.add(new_movie)
        db.session.commit()
        return new_movie

    def update_movie(self, movie_id, updated_data):
        """Update the details of a specific movie in the database"""
        movie = Movie.query.get(movie_id)
        if movie:
            movie.title = updated_data.get('title', movie.title)
            movie.director = updated_data.get('director', movie.director)
            movie.year = updated_data.get('year', movie.year)
            movie.rating = updated_data.get('rating', movie.rating)
            movie.poster_url = updated_data.get('poster_url', movie.poster_url)
            db.session.commit()
            return movie
        return None

    def delete_movie(self, movie_id):
        """Delete the movie from the user's list of favorites"""
        movie = Movie.query.get(movie_id)
        if movie:
            db.session.delete(movie)
            db.session.commit()
            return True
        return False

    def get_movie(self, movie_id):
        """Get a specific movie by ID"""
        return Movie.query.get(movie_id)
