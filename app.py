from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

DATABASE_PATH = os.path.join('database', 'app.db')

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_stats():
    """Get database statistics"""
    conn = get_db_connection()

    users_count = conn.execute('SELECT COUNT(*) FROM users').fetchone()[0]
    posts_count = conn.execute('SELECT COUNT(*) FROM posts').fetchone()[0]
    comments_count = conn.execute('SELECT COUNT(*) FROM comments').fetchone()[0]

    conn.close()

    return {
        'users': users_count,
        'posts': posts_count,
        'comments': comments_count
    }

@app.route('/')
def index():
    """Home page with statistics"""
    stats = get_stats()
    return render_template('index.html', stats=stats)

@app.route('/users')
def users():
    """Users page"""
    conn = get_db_connection()
    users = conn.execute('''
        SELECT id, username, email, created_at
        FROM users
        ORDER BY created_at DESC
    ''').fetchall()
    conn.close()
    return render_template('users.html', users=users)

@app.route('/posts')
def posts():
    """Posts page"""
    conn = get_db_connection()

    # Get posts with user information and comment counts
    posts = conn.execute('''
        SELECT p.id, p.title, p.content, p.created_at, u.username,
               COUNT(c.id) as comment_count
        FROM posts p
        JOIN users u ON p.user_id = u.id
        LEFT JOIN comments c ON p.id = c.post_id
        GROUP BY p.id, p.title, p.content, p.created_at, u.username
        ORDER BY p.created_at DESC
    ''').fetchall()

    # Get all users for the add post form
    available_users = conn.execute('''
        SELECT id, username FROM users ORDER BY username
    ''').fetchall()

    conn.close()
    return render_template('posts.html', posts=posts, available_users=available_users)

@app.route('/add_user', methods=['POST'])
def add_user():
    """Add a new user"""
    username = request.form['username']
    email = request.form['email']

    try:
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO users (username, email) VALUES (?, ?)
        ''', (username, email))
        conn.commit()
        conn.close()
        flash('User added successfully!', 'success')
    except sqlite3.IntegrityError as e:
        flash('Error: Username or email already exists!', 'error')
    except Exception as e:
        flash(f'Error adding user: {str(e)}', 'error')

    return redirect(url_for('users'))

@app.route('/add_post', methods=['POST'])
def add_post():
    """Add a new post"""
    title = request.form['title']
    content = request.form['content']
    user_id = request.form['user_id']

    try:
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO posts (title, content, user_id) VALUES (?, ?, ?)
        ''', (title, content, user_id))
        conn.commit()
        conn.close()
        flash('Post added successfully!', 'success')
    except Exception as e:
        flash(f'Error adding post: {str(e)}', 'error')

    return redirect(url_for('posts'))

@app.route('/api/users')
def api_users():
    """API endpoint to get all users"""
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users ORDER BY created_at DESC').fetchall()
    conn.close()

    return {
        'users': [dict(user) for user in users]
    }

@app.route('/api/posts')
def api_posts():
    """API endpoint to get all posts with user information"""
    conn = get_db_connection()
    posts = conn.execute('''
        SELECT p.*, u.username
        FROM posts p
        JOIN users u ON p.user_id = u.id
        ORDER BY p.created_at DESC
    ''').fetchall()
    conn.close()

    return {
        'posts': [dict(post) for post in posts]
    }

@app.route('/api/comments/<int:post_id>')
def api_comments(post_id):
    """API endpoint to get comments for a specific post"""
    conn = get_db_connection()
    comments = conn.execute('''
        SELECT c.*, u.username
        FROM comments c
        JOIN users u ON c.user_id = u.id
        WHERE c.post_id = ?
        ORDER BY c.created_at DESC
    ''', (post_id,)).fetchall()
    conn.close()

    return {
        'comments': [dict(comment) for comment in comments]
    }

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)