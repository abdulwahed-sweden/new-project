# Database Management Application

A complete SQLite database setup with Flask web interface and Bootstrap styling.

## Features

- SQLite database with Users, Posts, and Comments tables
- Optimized indexes for better performance
- Sample data pre-loaded
- Bootstrap-styled web interface
- RESTful API endpoints
- Add new users and posts functionality

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Initialize the database:
```bash
python database/init_db.py
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to `http://localhost:5000`

## Database Schema

### Users Table
- id (PRIMARY KEY)
- username (UNIQUE)
- email (UNIQUE)
- created_at

### Posts Table
- id (PRIMARY KEY)
- title
- content
- user_id (FOREIGN KEY)
- created_at

### Comments Table
- id (PRIMARY KEY)
- content
- post_id (FOREIGN KEY)
- user_id (FOREIGN KEY)
- created_at

## API Endpoints

- `GET /api/users` - Get all users
- `GET /api/posts` - Get all posts with user information
- `GET /api/comments/<post_id>` - Get comments for specific post

## Web Interface

- `/` - Dashboard with statistics
- `/users` - View and add users
- `/posts` - View and add posts