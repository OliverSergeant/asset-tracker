import sqlite3

def init_db():
    conn = sqlite3.connect('asset_tracker.db')
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        username TEXT NOT NULL,
                        password TEXT NOT NULL
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS assets (
                        id INTEGER PRIMARY KEY,
                        user_id INTEGER,
                        asset_name TEXT NOT NULL,
                        asset_value REAL,
                        FOREIGN KEY(user_id) REFERENCES users(id)
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                        id INTEGER PRIMARY KEY,
                        asset_id INTEGER,
                        transaction_date TEXT,
                        transaction_type TEXT,
                        FOREIGN KEY(asset_id) REFERENCES assets(id)
                    )''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()