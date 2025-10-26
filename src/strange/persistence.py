"""
Persistence layer for the strange tool using SQLite.

This module provides database connection management and schema creation.
"""

import sqlite3
from pathlib import Path
from typing import Optional
from contextlib import contextmanager


class Database:
    """
    SQLite database manager for the strange tool.
    
    Handles connection management, schema creation, and transaction handling.
    """
    
    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize the database connection.
        
        Args:
            db_path: Path to the SQLite database file. If None, uses default location.
        """
        if db_path is None:
            # Use default path in user's home directory
            home = Path.home()
            db_dir = home / '.strange'
            db_dir.mkdir(exist_ok=True)
            db_path = str(db_dir / 'decisions.db')
        
        self.db_path = db_path
        self._connection: Optional[sqlite3.Connection] = None
        self._init_schema()
    
    def _get_connection(self) -> sqlite3.Connection:
        """Get or create a database connection."""
        if self._connection is None:
            self._connection = sqlite3.connect(self.db_path)
            self._connection.row_factory = sqlite3.Row
            # Enable foreign key constraints
            self._connection.execute("PRAGMA foreign_keys = ON")
        return self._connection
    
    @contextmanager
    def get_cursor(self):
        """
        Context manager for database cursor with automatic commit/rollback.
        
        Yields:
            sqlite3.Cursor: Database cursor for executing queries
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            yield cursor
            conn.commit()
        except Exception:
            conn.rollback()
            raise
    
    def _init_schema(self):
        """Initialize the database schema."""
        with self.get_cursor() as cursor:
            # Create decisions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS decisions (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)
            
            # Create options table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS options (
                    id TEXT PRIMARY KEY,
                    decision_id TEXT NOT NULL,
                    name TEXT NOT NULL,
                    description TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    FOREIGN KEY (decision_id) REFERENCES decisions(id) ON DELETE CASCADE
                )
            """)
            
            # Create criteria table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS criteria (
                    id TEXT PRIMARY KEY,
                    decision_id TEXT NOT NULL,
                    name TEXT NOT NULL,
                    description TEXT,
                    weight REAL NOT NULL DEFAULT 1.0,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    FOREIGN KEY (decision_id) REFERENCES decisions(id) ON DELETE CASCADE
                )
            """)
            
            # Create scores table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS scores (
                    id TEXT PRIMARY KEY,
                    option_id TEXT NOT NULL,
                    criteria_id TEXT NOT NULL,
                    value REAL NOT NULL,
                    notes TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    FOREIGN KEY (option_id) REFERENCES options(id) ON DELETE CASCADE,
                    FOREIGN KEY (criteria_id) REFERENCES criteria(id) ON DELETE CASCADE,
                    UNIQUE(option_id, criteria_id)
                )
            """)
            
            # Create indexes for better query performance
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_options_decision_id 
                ON options(decision_id)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_criteria_decision_id 
                ON criteria(decision_id)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_scores_option_id 
                ON scores(option_id)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_scores_criteria_id 
                ON scores(criteria_id)
            """)
    
    def close(self):
        """Close the database connection."""
        if self._connection:
            self._connection.close()
            self._connection = None
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit with automatic cleanup."""
        self.close()

