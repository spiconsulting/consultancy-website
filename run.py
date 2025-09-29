# Import the application factory function from our 'app' package.
from app import create_app, db
# Import the User and Post models so Flask-Migrate can see them.
from app.models import User, Post
# --- UPDATED: Import the new exporter command ---
from exporter import export_all_data_command
# Load environment variables from the .env file. This is crucial for security.
from dotenv import load_dotenv
load_dotenv()

# Create the Flask application instance using our factory.
app = create_app()

# --- UPDATED: Register the new command with the app ---
# You can remove the old app.cli.add_command if you want
app.cli.add_command(export_all_data_command)

# This context processor makes the 'db', 'User', and 'Post' variables
# available in the 'flask shell' for easy testing and debugging.
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Job': Job}

# The following block ensures that the server is only started when
# this script is executed directly (not when imported).
if __name__ == '__main__':
    # Run the application with debugging enabled.
    # Debug mode provides helpful error messages and automatically reloads the server on code changes.
    app.run(debug=True)