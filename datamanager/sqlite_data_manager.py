from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float, ForeignKey
from sqlalchemy.exc import SQLAlchemyError
from datamanager.data_manager_interface import DataManagerInterface

# 1. Database Setup (SQLAlchemy Boilerplate)
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# 2. Table Definitions (Models)
class User(db.Model):
    """
    Represents a user in the database.
    """
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)


class Movie(db.Model):
    """
    Represents a movie in the database, linked to a user.
    """
    __tablename__ = 'movies'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    director: Mapped[str] = mapped_column(String, nullable=True)
    year: Mapped[int] = mapped_column(Integer, nullable=True)
    rating: Mapped[float] = mapped_column(Float, nullable=True)
    poster: Mapped[str] = mapped_column(String, nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

# 3. The Data Manager Implementation
class SQLiteDataManager(DataManagerInterface):
    """
    Data Manager implementation using SQLite and SQLAlchemy.
    """
    def __init__(self, app):
        """
        Initializes the database with the Flask app context.
        """
        db.init_app(app)
        self.db = db
        
        # Create tables if they do not exist yet
        with app.app_context():
            db.create_all()

    def get_all_users(self):
        """
        Fetches all users from the database.
        
        Returns:
            list: A list of User objects.
        """
        return User.query.all()

    def get_user_movies(self, user_id):
        """
        Fetches all movies belonging to a specific user.
        
        Args:
            user_id (int): The ID of the user.
            
        Returns:
            list: A list of Movie objects.
        """
        return Movie.query.filter_by(user_id=user_id).all()

    def add_user(self, user_name):
        """
        Adds a new user to the database with error handling.
        
        Args:
            user_name (str): The name of the new user.
            
        Returns:
            bool: True if successful, False otherwise.
        """
        new_user = User(name=user_name)
        try:
            self.db.session.add(new_user)
            self.db.session.commit()
            return True
        except SQLAlchemyError as e:
            self.db.session.rollback()
            print(f"Database Error (add_user): {e}")
            return False

    def add_movie(self, user_id, movie_data):
        """
        Adds a new movie to the database for a specific user.
        Includes error handling for database transactions.
        
        Args:
            user_id (int): The ID of the user.
            movie_data (dict): Dictionary containing movie details.
            
        Returns:
            bool: True if successful, False otherwise.
        """
        new_movie = Movie(
            name=movie_data['name'],
            director=movie_data.get('director', 'Unknown'),
            year=movie_data['year'],
            rating=movie_data['rating'],
            poster=movie_data.get('poster'),
            user_id=user_id
        )
        try:
            self.db.session.add(new_movie)
            self.db.session.commit()
            return True
        except SQLAlchemyError as e:
            self.db.session.rollback() # Undo changes on error
            print(f"Database Error (add_movie): {e}")
            return False

    def update_movie(self, movie_id, movie_data):
        """
        Updates an existing movie's details with error handling.
        
        Args:
            movie_id (int): The ID of the movie to update.
            movie_data (dict): Dictionary containing updated fields.
            
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            movie = Movie.query.get(movie_id)
            if movie:
                movie.name = movie_data.get('name', movie.name)
                movie.director = movie_data.get('director', movie.director)
                movie.year = movie_data.get('year', movie.year)
                movie.rating = movie_data.get('rating', movie.rating)
                self.db.session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            self.db.session.rollback()
            print(f"Database Error (update_movie): {e}")
            return False

    def delete_movie(self, movie_id):
        """
        Deletes a movie by ID with error handling.
        
        Args:
            movie_id (int): The ID of the movie to delete.
            
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            movie = Movie.query.get(movie_id)
            if movie:
                self.db.session.delete(movie)
                self.db.session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            self.db.session.rollback()
            print(f"Error deleting movie: {e}")
            return False

    def get_movie(self, movie_id):
        """
        Fetches a single movie object by ID.
        """
        return Movie.query.get(movie_id)
    
    def get_user(self, user_id):
        """
        Fetches a specific user by their ID.
        """
        return User.query.get(user_id)