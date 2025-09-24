import sqlite3
import os

def init_database():
    """Initialize SQLite database with tables"""
    db_path = os.path.join(os.path.dirname(__file__), 'app.db')

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(80) UNIQUE NOT NULL,
            email VARCHAR(120) UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create posts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title VARCHAR(200) NOT NULL,
            content TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    # Create comments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            post_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (post_id) REFERENCES posts (id),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    conn.commit()
    return conn, cursor

def create_indexes(cursor):
    """Create indexes for better performance"""
    indexes = [
        "CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)",
        "CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)",
        "CREATE INDEX IF NOT EXISTS idx_posts_user_id ON posts(user_id)",
        "CREATE INDEX IF NOT EXISTS idx_posts_created_at ON posts(created_at)",
        "CREATE INDEX IF NOT EXISTS idx_comments_post_id ON comments(post_id)",
        "CREATE INDEX IF NOT EXISTS idx_comments_user_id ON comments(user_id)"
    ]

    for index in indexes:
        cursor.execute(index)

def insert_sample_data(cursor):
    """Insert sample data into tables"""
    # Sample users
    users = [
        ('john_doe', 'john@example.com'),
        ('jane_smith', 'jane@example.com'),
        ('bob_wilson', 'bob@example.com')
    ]

    cursor.executemany(
        "INSERT OR IGNORE INTO users (username, email) VALUES (?, ?)",
        users
    )

    # Sample posts
    posts = [
        ('First Post', 'This is the content of the first post', 1),
        ('Second Post', 'Another interesting post here', 2),
        ('Third Post', 'More content for the third post', 1),
        ('Fourth Post', 'Final post content', 3)
    ]

    cursor.executemany(
        "INSERT OR IGNORE INTO posts (title, content, user_id) VALUES (?, ?, ?)",
        posts
    )

    # Sample comments
    comments = [
        ('Great post!', 1, 2),
        ('Thanks for sharing', 1, 3),
        ('Interesting perspective', 2, 1),
        ('I agree with this', 3, 2),
        ('Nice work', 4, 1)
    ]

    cursor.executemany(
        "INSERT OR IGNORE INTO comments (content, post_id, user_id) VALUES (?, ?, ?)",
        comments
    )

if __name__ == '__main__':
    conn, cursor = init_database()
    create_indexes(cursor)
    insert_sample_data(cursor)
    conn.commit()
    conn.close()
    print("Database initialized successfully!")