"""
Initialize the SQLite database with required schema.
Run this once to set up the database.
"""
import sqlite3
from pathlib import Path

DATABASE_PATH = "database.db"

def init_database():
    """Create all required tables if they don't exist."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Enable foreign keys
    cursor.execute("PRAGMA foreign_keys = ON")
    
    # Create asset_types table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS asset_types (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    """)
    
    # Create locations table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS locations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            location_type TEXT CHECK(location_type IN ('Warehouse', 'Store')),
            is_active INTEGER DEFAULT 1
        )
    """)
    
    # Create statuses table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS statuses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    """)
    
    # Create assets table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS assets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            asset_type_id INTEGER NOT NULL,
            serial_number TEXT UNIQUE NOT NULL,
            current_location_id INTEGER NOT NULL,
            status_id INTEGER NOT NULL,
            deployment_date TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY (asset_type_id) REFERENCES asset_types(id),
            FOREIGN KEY (current_location_id) REFERENCES locations(id),
            FOREIGN KEY (status_id) REFERENCES statuses(id)
        )
    """)
    
    # Create asset_movements table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS asset_movements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            asset_id INTEGER NOT NULL,
            from_location_id INTEGER,
            to_location_id INTEGER NOT NULL,
            movement_ts TEXT NOT NULL,
            note TEXT,
            FOREIGN KEY (asset_id) REFERENCES assets(id),
            FOREIGN KEY (from_location_id) REFERENCES locations(id),
            FOREIGN KEY (to_location_id) REFERENCES locations(id)
        )
    """)
    
    # Insert default statuses if they don't exist
    statuses = ["In Stock", "Deployed", "In Repair", "Retired"]
    for status in statuses:
        cursor.execute(
            "INSERT OR IGNORE INTO statuses (name) VALUES (?)",
            (status,)
        )
    
    conn.commit()
    conn.close()
    print(f"Database initialized at {DATABASE_PATH}")

if __name__ == "__main__":
    init_database()