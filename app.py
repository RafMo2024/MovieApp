from flask import Flask, render_template, request, redirect, url_for
from datamanager.sqlite_data_manager import SQLiteDataManager
from datamanager.api_handler import OMDbHandler

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///moviwebapp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Managers
data_manager = SQLiteDataManager(app)
api_handler = OMDbHandler()

@app.route('/')
def home():
    """
    Renders the home page, which displays the list of all users.
    
    Returns:
        Rendered HTML template 'users.html'.
    """
    return render_template('index.html')

@app.route('/users')
def list_users():
    """
    Retrieves all users from the database and displays them.
    
    Returns:
        Rendered HTML template 'users.html' with a list of users.
    """
    # Fetch all users from the DB and pass them to the template
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    """
    Handles the creation of a new user.
    
    Methods:
        GET: Displays the form to add a user.
        POST: Processes the form data and adds the user to the database.
        
    Returns:
        GET: Rendered 'add_user.html' template.
        POST: Redirect to 'list_users' route.
    """
    # If the form is submitted (POST)
    if request.method == 'POST':
        user_name = request.form['name']
        data_manager.add_user(user_name)
        return redirect(url_for('list_users'))

    # If the page is just loaded (GET)
    return render_template('add_user.html')

@app.route('/users/<int:user_id>')
def user_movies(user_id):
    """
    Displays the list of favorite movies for a specific user.
    
    Args:
        user_id (int): The unique ID of the user.
        
    Returns:
        Rendered 'user_movies.html' template with the user's movies.
    """
    # 1. Fetch movies for this user
    movies = data_manager.get_user_movies(user_id)

    # 2. Fetch the user's name (NEW STEP)
    user = data_manager.get_user(user_id)
    
    # 3. Display template
    return render_template('user_movies.html', movies=movies, user=user)

@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_movie_to_user(user_id):
    """
    Route to add a movie to a specific user's list.
    Uses the OMDbHandler to fetch movie metadata automatically.
    
    POST: Searches API, gets data, and saves to DB.
    GET: Displays the search form.
    """
    if request.method == 'POST':
        movie_name = request.form['movie_name']
        
        # 1. Fetch data using the separated API module
        movie_data = api_handler.get_movie_details(movie_name)
        
        if movie_data:
            # 2. Save to database using the Data Manager
            success = data_manager.add_movie(user_id, movie_data)
            
            if success:
                return redirect(url_for('user_movies', user_id=user_id))
            else:
                return "<h1>Database Error: Could not save movie.</h1>"
        else:
            # API returned nothing or failed
            return f"<h1>Movie '{movie_name}' not found!</h1><p><a href='/users/{user_id}/add_movie'>Try again</a></p>"

    user = data_manager.get_user(user_id)
    return render_template('add_movie.html', user=user)

@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>')
def delete_movie(user_id, movie_id):
    """
    Deletes a specific movie from a user's list.
    
    Args:
        user_id (int): The ID of the user.
        movie_id (int): The ID of the movie to delete.
        
    Returns:
        Redirects back to the user's movie list.
    """
    data_manager.delete_movie(movie_id)
    return redirect(url_for('user_movies', user_id=user_id))

@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    """
    Handles updating the details of an existing movie.
    
    Methods:
        GET: Displays the form pre-filled with existing movie data.
        POST: Updates the movie in the database with new form data.
        
    Args:
        user_id (int): The ID of the user.
        movie_id (int): The ID of the movie to update.
        
    Returns:
        GET: Rendered 'update_movie.html'.
        POST: Redirect to 'user_movies'.
    """
    # 1. POST: Save updated data
    if request.method == 'POST':
        try:
            # Versuche, die Zahlen umzuwandeln
            year = int(request.form['year'])
            rating = float(request.form['rating'])
        except ValueError:
            # Falls der User Text statt Zahlen eingegeben hat
            return "<h1>Error: Year must be an integer and Rating a number.</h1><a href='javascript:history.back()'>Go Back</a>", 400

        updated_data = {
            'name': request.form['name'],
            'director': request.form['director'],
            'year': year,
            'rating': rating
        }
        data_manager.update_movie(movie_id, updated_data)
        return redirect(url_for('user_movies', user_id=user_id))

    # 2. GET: Show form with existing data
    movie = data_manager.get_movie(movie_id)
    return render_template('update_movie.html', movie=movie, user_id=user_id)

@app.errorhandler(404)
def page_not_found(e):
    """
    Custom error handler for 404 (Page Not Found) errors.
    
    Args:
        e: The exception object.
        
    Returns:
        Rendered '404.html' template and 404 status code.
    """
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True, port=5001)