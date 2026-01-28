# MoviWeb App 🎬

A robust Flask web application to manage favorite movies.
Users can create accounts, add movies to their personal collection, and rate them. Movie metadata (Poster, Rating, Year) is fetched automatically via the OMDb API.

## Features
* 👤 **User Management**: Create and view user profiles.
* 🔍 **Smart Fetching**: Auto-fetch movie details via OMDb API.
* 💾 **Persistent Storage**: Data is stored securely using SQLite & SQLAlchemy.
* 🛡️ **Robust Error Handling**: Prevents crashes on invalid inputs or database errors.
* 🔒 **Security**: API Keys are managed via environment variables (not hardcoded).
* 🎨 **UI/UX**: Responsive Dark Mode design with glassmorphism effects.

## Project Structure
* `app.py`: Main Flask application controller.
* `datamanager/`: Handles database logic (SQLite) and API communication.
* `templates/`: HTML files using Jinja2 inheritance.
* `static/`: CSS styling and assets.

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/RafMo2024/moviweb-app.git](https://github.com/RafMo2024/moviweb-app.git)
   cd moviweb-app