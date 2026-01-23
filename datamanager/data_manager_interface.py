from abc import ABC, abstractmethod

class DataManagerInterface(ABC):
    """
    Interface defining the contract for data management.
    
    This abstract base class ensures that any data manager implementation 
    (e.g., SQLite, JSON, CSV) provides the necessary methods to handle 
    users and movies consistently.
    """

    @abstractmethod
    def get_all_users(self):
        """
        Retrieves all users from the data storage.

        Returns:
            list: A list of User objects (or dictionaries, depending on implementation).
        """
        pass

    @abstractmethod
    def get_user_movies(self, user_id):
        """
        Retrieves all movies associated with a specific user.

        Args:
            user_id (int): The ID of the user whose movies to retrieve.

        Returns:
            list: A list of Movie objects (or dictionaries) belonging to the user.
        """
        pass

    @abstractmethod
    def add_user(self, user):
        """
        Adds a new user to the data storage.

        Args:
            user (str): The name of the user to be added.
        """
        pass

    @abstractmethod
    def add_movie(self, user_id, movie):
        """
        Adds a new movie to a specific user's list.

        Args:
            user_id (int): The ID of the user who owns the movie.
            movie (dict): A dictionary containing movie details (name, year, rating, etc.).
        """
        pass

    @abstractmethod
    def update_movie(self, movie_id, movie_data):
        """
        Updates the details of an existing movie.

        Args:
            movie_id (int): The ID of the movie to update.
            movie_data (dict): A dictionary containing the updated movie details.
        """
        pass

    @abstractmethod
    def delete_movie(self, movie_id):
        """
        Deletes a specific movie from the data storage.

        Args:
            movie_id (int): The ID of the movie to delete.
        """
        pass