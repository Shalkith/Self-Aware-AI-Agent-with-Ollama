import sqlite3
import json
import os
from datetime import datetime
from typing import List, Dict, Any

# Import config
from config import config

class MemoryManager:
    def __init__(self, db_path: str = None):
        self.db_path = db_path or config.MEMORY_DB_PATH
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.init_db()

    def init_db(self):
        """Initialize the database with required tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create memories table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                memory_type TEXT NOT NULL,
                content TEXT NOT NULL,
                metadata TEXT
            )
        ''')

        # Create experiences table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS experiences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                experience TEXT NOT NULL,
                outcome TEXT,
                metadata TEXT
            )
        ''')

        conn.commit()
        conn.close()

    def store_memory(self, memory_type: str, content: str, metadata: Dict = None):
        """Store a memory with type and content."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO memories (timestamp, memory_type, content, metadata)
            VALUES (?, ?, ?, ?)
        ''', (
            datetime.now().isoformat(),
            memory_type,
            content,
            json.dumps(metadata) if metadata else None
        ))

        conn.commit()
        conn.close()

    def store_experience(self, experience: str, outcome: str = None, metadata: Dict = None):
        """Store an experience with optional outcome."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO experiences (timestamp, experience, outcome, metadata)
            VALUES (?, ?, ?, ?)
        ''', (
            datetime.now().isoformat(),
            experience,
            outcome,
            json.dumps(metadata) if metadata else None
        ))

        conn.commit()
        conn.close()

    def get_memories(self, memory_type: str = None, limit: int = None) -> List[Dict]:
        """Retrieve memories, optionally filtered by type."""
        if limit is None:
            limit = config.MEMORY_MAX_LONG_TERM_MEMORIES
        """Retrieve memories, optionally filtered by type."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if memory_type:
            cursor.execute('''
                SELECT id, timestamp, memory_type, content, metadata
                FROM memories
                WHERE memory_type = ?
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (memory_type, limit))
        else:
            cursor.execute('''
                SELECT id, timestamp, memory_type, content, metadata
                FROM memories
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (limit,))

        rows = cursor.fetchall()
        conn.close()

        return [
            {
                'id': row[0],
                'timestamp': row[1],
                'memory_type': row[2],
                'content': row[3],
                'metadata': json.loads(row[4]) if row[4] else None
            }
            for row in rows
        ]

    def get_recent_experiences(self, limit: int = None) -> List[Dict]:
        """Retrieve recent experiences."""
        if limit is None:
            limit = config.MEMORY_MAX_RECENT_EXPERIENCES
        """Retrieve recent experiences."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id, timestamp, experience, outcome, metadata
            FROM experiences
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (limit,))

        rows = cursor.fetchall()
        conn.close()

        return [
            {
                'id': row[0],
                'timestamp': row[1],
                'experience': row[2],
                'outcome': row[3],
                'metadata': json.loads(row[4]) if row[4] else None
            }
            for row in rows
        ]

    def search_memories(self, query: str) -> List[Dict]:
        """Search memories by content."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id, timestamp, memory_type, content, metadata
            FROM memories
            WHERE content LIKE ?
            ORDER BY timestamp DESC
        ''', (f'%{query}%',))

        rows = cursor.fetchall()
        conn.close()

        return [
            {
                'id': row[0],
                'timestamp': row[1],
                'memory_type': row[2],
                'content': row[3],
                'metadata': json.loads(row[4]) if row[4] else None
            }
            for row in rows
        ]

    def clear_memories(self):
        """Clear all memories and experiences."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('DELETE FROM memories')
        cursor.execute('DELETE FROM experiences')

        conn.commit()
        conn.close()

    def get_memory_stats(self) -> Dict[str, int]:
        """Get statistics about stored memories."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT COUNT(*) FROM memories')
        memory_count = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM experiences')
        experience_count = cursor.fetchone()[0]

        conn.close()

        return {
            'memory_count': memory_count,
            'experience_count': experience_count
        }