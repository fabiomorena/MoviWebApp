MoviWeb App
A Flask-based web application for managing personal movie lists with OMDb API integration.

🎬 Description
MoviWeb App is a complete web application that allows users to create and manage their personal movie lists. The application integrates with the OMDb API to automatically fetch detailed movie information including title, director, release year, rating, and movie posters.

🚀 Features
User Management: Create and manage user accounts
Movie Lists: Each user can create their personal movie list
OMDb API Integration: Automatic fetching of movie data
Responsive Design: Works on desktop and mobile
Error Handling: Robust error handling and user feedback
Database: SQLite-based storage with SQLAlchemy ORM
🛠️ Technologies
Backend: Python, Flask
Database: SQLite with SQLAlchemy ORM
Frontend: HTML, CSS, Jinja2 Templates
API: OMDb API for movie information
Styling: Custom CSS framework (no external libraries)
📋 Prerequisites
Python 3.7 or higher
pip (Python Package Manager)

📦 Installation
Clone the repository:
git clone https://github.com/fabiomorena/MoviWebApp.git
cd MoviWebApp

Create virtual environment:
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

Install dependencies:
pip install flask flask-sqlalchemy requests python-dotenv

Get OMDb API Key (optional but recommended):
Visit OMDb API
Register for a free API key
Create a .env file in the project directory:
OMDB_API_KEY=your-api-key-here

Running the Application
python app.py

The application will be available at http://localhost:5000

📁 Project Structure
MoviWebApp/
├── app.py                 # Main application file
├── models.py             # Database models
├── data_manager.py       # Data management class
├── .env                  # Environment variables (optional)
├── templates/            # HTML Templates
│   ├── base.html         # Base template
│   ├── index.html        # User list
│   ├── user_movies.html  # User movies
│   ├── 404.html          # Error page
│   └── 500.html          # Server error
├── static/               # Static files
│   ├── style.css         # CSS stylesheet
│   └── images/           # Images (movie posters)
└── venv/                 # Virtual environment

🎯 Usage
Create User: Create a new user on the homepage
Add Movies: Add movies by title on the user page
Manage Movies: Delete movies from personal list
View Data: See all movies with details like director, year, and rating
🔧 Development
Database Model
The application uses two main tables:

Users: Stores user information
Movies: Stores movie information with user association
DataManager
The DataManager class encapsulates all database operations:

create_user(): Create new user
get_users(): Retrieve all users
add_movie(): Add movie to user
get_movies(): Retrieve user's movies
delete_movie(): Delete movie
API Integration
The application integrates with OMDb API with fallback mechanism:

Attempts to fetch movie data via OMDb API
Falls back to default data on API failures or invalid key
Known movies have predefined data
🐛 Error Handling
The application implements comprehensive error handling:

HTTP Errors: 404 and 500 error pages
Database Errors: Graceful degradation on database issues
API Errors: Fallback on API failures
User Input: Validation and error messages
🎨 Design Features
Responsive Design: Works on all devices
Modern Color Palette: Gradient-based design
Card-based Display: Movies in attractive cards
Hover Effects: Interactive user interface
Emoji Integration: Visually appealing icons
Consistent Typography: Readable font sizes and spacing
🤝 Contributing
Fork the repository
Create your feature branch (git checkout -b feature/AmazingFeature)
Commit your changes (git commit -m 'Add some AmazingFeature')
Push to the branch (git push origin feature/AmazingFeature)
Open a pull request
📝 License
This project is licensed under the MIT License - see the LICENSE file for details.

📧 Contact
Fabio Morena - @fabiomorena

Project Link: https://github.com/fabiomorena/MoviWebApp

🙏 Acknowledgments
OMDb API for movie data
Flask for the web framework
SQLAlchemy for the ORM
Inspired by modern media management web applications
🚀 Future Improvements
User authentication with password hashing
Movie search functionality
Movie rating system
Export/Import movie lists
Advanced filtering and sorting
User profile management
Movie recommendations
Multi-language support
