from flask import Flask, render_template, request, redirect, url_for
from datamanager.sqlite_data_manager import SQLiteDataManager
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///moviwebapp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

data_manager = SQLiteDataManager(app)

@app.route('/')
def home():
    return render_template('users.html', users=data_manager.get_all_users())

@app.route('/users')
def list_users():
    # Fetch all users from the DB and pass them to the template
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    # If the form is submitted (POST)
    if request.method == 'POST':
        user_name = request.form['name']
        data_manager.add_user(user_name)
        return redirect(url_for('list_users'))

    # If the page is just loaded (GET)
    return render_template('add_user.html')

@app.route('/users/<int:user_id>')
def user_movies(user_id):
    # 1. Fetch movies for this user
    movies = data_manager.get_user_movies(user_id)
    
    # 2. Display template
    return render_template('user_movies.html', movies=movies, user_id=user_id)

@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_movie_to_user(user_id):
    if request.method == 'POST':
        movie_name = request.form['movie_name']
        
        # --- API FETCHING ---
        API_KEY = "fc1880cd" # In production, use os.getenv('API_KEY')
        api_url = f"http://www.omdbapi.com/?apikey={API_KEY}&t={movie_name}"
        
        try:
            response = requests.get(api_url)

            data = response.json()
            
            if data.get('Response') == 'True':
                # Build dictionary for DataManager
                movie_data = {
                    'name': data['Title'],
                    'year': int(data['Year']),
                    'rating': float(data.get('imdbRating', 0)), # Default to 0 if N/A
                    'poster': data.get('Poster'),
                    'director': data.get('Director')
                }
                
                # Save in DB
                data_manager.add_movie(user_id, movie_data)
                
                # Redirect to user's movie list
                return redirect(url_for('user_movies', user_id=user_id))
            else:
                return f"<h1>Movie '{movie_name}' not found in API!</h1><a href='/users/{user_id}/add_movie'>Try again</a>"
                
        except Exception as e:
            return f"<h1>Error fetching data: {e}</h1>"

    # GET request: Show form
    return render_template('add_movie.html', user_id=user_id)

@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>')
def delete_movie(user_id, movie_id):
    data_manager.delete_movie(movie_id)
    return redirect(url_for('user_movies', user_id=user_id))

@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    # 1. POST: Save updated data
    if request.method == 'POST':
        updated_data = {
            'name': request.form['name'],
            'director': request.form['director'],
            'year': int(request.form['year']),
            'rating': float(request.form['rating'])
        }
        data_manager.update_movie(movie_id, updated_data)
        return redirect(url_for('user_movies', user_id=user_id))

    # 2. GET: Show form with existing data
    movie = data_manager.get_movie(movie_id)
    return render_template('update_movie.html', movie=movie, user_id=user_id)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)