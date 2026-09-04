import sqlite3
from config import DATABASE_PATH


def get_connection():
    return sqlite3.connect(DATABASE_PATH)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            text TEXT,
            tags TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        );
    ''')
    conn.commit()
    conn.close()


def add_user(user_id, username, first_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT OR IGNORE INTO users (user_id, username, first_name) VALUES (?, ?, ?)',
        (user_id, username, first_name)
    )
    conn.commit()
    conn.close()


def save_memory(user_id, text, tags=''):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO memories (user_id, text, tags) VALUES (?, ?, ?)',
        (user_id, text, tags)
    )
    conn.commit()
    conn.close()


def get_random_memory(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT id, text, created_at FROM memories WHERE user_id = ? ORDER BY RANDOM() LIMIT 1',
        (user_id,)
    )
    row = cursor.fetchone()
    conn.close()
    return row


def get_all_memories(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT id, text, created_at FROM memories WHERE user_id = ? ORDER BY created_at DESC',
        (user_id,)
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


def delete_memory(user_id, memory_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        'DELETE FROM memories WHERE id = ? AND user_id = ?',
        (memory_id, user_id)
    )
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    return affected > 0
