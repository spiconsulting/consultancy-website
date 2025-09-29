import json
import click
from flask.cli import with_appcontext
from app import db
from app.models import User, Post, Job

# This decorator registers a new command 'export-all-data' with Flask
@click.command('export-all-data')
@with_appcontext
def export_all_data_command():
    """Exports all major data from the database to a single JSON file."""
    
    # --- Export Users (excluding sensitive password hash) ---
    users = User.query.all()
    users_data = []
    for user in users:
        users_data.append({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'is_admin': user.is_admin
        })
        
    # --- Export Posts ---
    posts = Post.query.all()
    posts_data = []
    for post in posts:
        posts_data.append({
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'timestamp': post.timestamp.isoformat(),
            'author_username': post.author.username,
            'slug': post.slug,
            'image_file': post.image_file
        })

    # --- Export Jobs ---
    jobs = Job.query.all()
    jobs_data = []
    for job in jobs:
        jobs_data.append({
            'id': job.id,
            'title': job.title,
            'location': job.location,
            'job_type': job.job_type,
            'description': job.description
        })
        
    # --- Combine all data into a single dictionary ---
    full_export = {
        'users': users_data,
        'posts': posts_data,
        'jobs': jobs_data
    }
    
    # Write the combined data to a JSON file
    with open('full_database_export.json', 'w') as f:
        json.dump(full_export, f, indent=4)
        
    click.echo('Successfully exported all data to full_database_export.json')

