"""
Example Flask app showing how to use the fixed templates.
This is a reference implementation for testing purposes.
"""

from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)

# Sample data for demonstration
sample_users = [
    {
        'id': 1,
        'username': 'john_doe',
        'email': 'john@example.com',
        'created_at': '2025-09-24 10:30:00'
    },
    {
        'id': 2,
        'username': 'jane_smith',
        'email': 'jane@example.com',
        'created_at': '2025-09-24 12:15:00'
    }
]

sample_posts = [
    {
        'id': 1,
        'title': 'Welcome to Smarty v5',
        'content': 'This is a sample post to demonstrate the new template system with relative timestamps and modern design.',
        'username': 'john_doe',
        'created_at': '2025-09-24 14:00:00',
        'comment_count': 5
    },
    {
        'id': 2,
        'title': 'Template System Update',
        'content': 'All templates have been updated to use the Smarty v5 theme with proper navigation and responsive design.',
        'username': 'jane_smith',
        'created_at': '2025-09-24 15:30:00',
        'comment_count': 3
    }
]

@app.route('/')
def index():
    """Dashboard page"""
    stats = {
        'users': len(sample_users),
        'posts': len(sample_posts),
        'comments': 12  # Number of available settings/configuration options
    }
    return render_template('index.html', stats=stats)

@app.route('/users')
def users():
    """Users page"""
    return render_template('users.html', users=sample_users)

@app.route('/posts')
def posts():
    """Posts page"""
    return render_template('posts.html', posts=sample_posts, available_users=sample_users)


@app.route('/add_user', methods=['POST'])
def add_user():
    """Add user endpoint (placeholder)"""
    # In a real app, this would handle form data
    return "User add functionality would be implemented here"

@app.route('/add_post', methods=['POST'])
def add_post():
    """Add post endpoint (placeholder)"""
    # In a real app, this would handle form data
    return "Post add functionality would be implemented here"

@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return render_template('404.html', title="Page Not Found"), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)