import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class OMDbHandler:
    """
    Handles interactions with the OMDb API to fetch movie metadata.
    """
    def __init__(self):
        self.api_key = os.getenv('OMDB_API_KEY')
        self.base_url = "http://www.omdbapi.com/"

    def get_movie_details(self, title):
        """
        Fetches movie details by title.
        
        Args:
            title (str): The title of the movie.
            
        Returns:
            dict: Movie data if found, else None.
        """
        if not self.api_key:
            raise ValueError("API Key not found. Please set OMDB_API_KEY in .env file.")

        params = {
            'apikey': self.api_key,
            't': title
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status() # Raises error for 4xx/5xx
            data = response.json()
            
            if data.get('Response') == 'True':
                return {
                    'name': data['Title'],
                    'year': int(data['Year']) if data['Year'].isdigit() else 0,
                    'rating': float(data.get('imdbRating', 0)) if data.get('imdbRating') != 'N/A' else 0.0,
                    'poster': data.get('Poster'),
                    'director': data.get('Director')
                }
            return None
        except requests.RequestException as e:
            print(f"API Request Error: {e}")
            return None