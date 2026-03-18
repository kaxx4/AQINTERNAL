#!/usr/bin/env python3
"""
MCP Memory Server - Persistent memory for AI agents
Provides remember, recall, rollback, and search tools for cross-session context
"""

import json
import os
import time
from pathlib import Path
from typing import Any
import sqlite3
from datetime import datetime

# MCP Server implementation
class MemoryServer:
    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = os.path.expanduser("~/.claude/agent-memory.db")

        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.init_db()

    def init_db(self):
        """Initialize SQLite database for memory storage"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    agent_name TEXT,
                    tags TEXT,
                    content TEXT NOT NULL,
                    context TEXT
                )
            """)
            conn.commit()

    def remember(self, content: str, agent_name: str = None, tags: list = None, context: str = None) -> dict:
        """Store a decision, deliverable, or context snapshot"""
        tags_str = json.dumps(tags or [])

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                INSERT INTO memories (content, agent_name, tags, context)
                VALUES (?, ?, ?, ?)
            """, (content, agent_name, tags_str, context))
            conn.commit()
            memory_id = cursor.lastrowid

        return {
            "status": "stored",
            "memory_id": memory_id,
            "timestamp": datetime.now().isoformat(),
            "tags": tags or []
        }

    def recall(self, search_term: str = None, agent_name: str = None, tags: list = None) -> dict:
        """Search and retrieve relevant memories"""
        with sqlite3.connect(self.db_path) as conn:
            query = "SELECT id, timestamp, agent_name, tags, content FROM memories WHERE 1=1"
            params = []

            if agent_name:
                query += " AND agent_name = ?"
                params.append(agent_name)

            if search_term:
                query += " AND content LIKE ?"
                params.append(f"%{search_term}%")

            query += " ORDER BY timestamp DESC LIMIT 10"

            cursor = conn.execute(query, params)
            memories = cursor.fetchall()

        results = [
            {
                "id": m[0],
                "timestamp": m[1],
                "agent": m[2],
                "tags": json.loads(m[3]) if m[3] else [],
                "content": m[4]
            }
            for m in memories
        ]

        return {
            "status": "retrieved",
            "count": len(results),
            "memories": results
        }

    def search(self, query: str) -> dict:
        """Find memories across all sessions and agents"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT id, timestamp, agent_name, tags, content
                FROM memories
                WHERE content LIKE ? OR tags LIKE ?
                ORDER BY timestamp DESC LIMIT 20
            """, (f"%{query}%", f"%{query}%"))
            memories = cursor.fetchall()

        results = [
            {
                "id": m[0],
                "timestamp": m[1],
                "agent": m[2],
                "tags": json.loads(m[3]) if m[3] else [],
                "content": m[4]
            }
            for m in memories
        ]

        return {
            "status": "search_complete",
            "query": query,
            "count": len(results),
            "memories": results
        }

    def rollback(self, memory_id: int = None) -> dict:
        """Restore to a previous known-good state"""
        with sqlite3.connect(self.db_path) as conn:
            if memory_id:
                cursor = conn.execute(
                    "SELECT * FROM memories WHERE id = ?",
                    (memory_id,)
                )
                memory = cursor.fetchone()
                if memory:
                    return {
                        "status": "restored",
                        "memory_id": memory_id,
                        "content": memory[4],
                        "context": memory[5]
                    }

        return {"status": "error", "message": "Memory not found"}

    def list_agents(self) -> dict:
        """List all agents with memories"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT DISTINCT agent_name, COUNT(*) as memory_count
                FROM memories
                WHERE agent_name IS NOT NULL
                GROUP BY agent_name
                ORDER BY memory_count DESC
            """)
            agents = cursor.fetchall()

        return {
            "status": "listed",
            "agents": [
                {"name": a[0], "memories": a[1]} for a in agents
            ]
        }


# MCP Protocol handlers
if __name__ == "__main__":
    import sys

    server = MemoryServer()

    # Read MCP requests from stdin
    for line in sys.stdin:
        try:
            request = json.loads(line)
            tool = request.get("tool")
            params = request.get("params", {})

            result = None
            if tool == "remember":
                result = server.remember(
                    content=params.get("content"),
                    agent_name=params.get("agent_name"),
                    tags=params.get("tags"),
                    context=params.get("context")
                )
            elif tool == "recall":
                result = server.recall(
                    search_term=params.get("search_term"),
                    agent_name=params.get("agent_name"),
                    tags=params.get("tags")
                )
            elif tool == "search":
                result = server.search(params.get("query"))
            elif tool == "rollback":
                result = server.rollback(params.get("memory_id"))
            elif tool == "list_agents":
                result = server.list_agents()

            if result:
                print(json.dumps(result))

        except Exception as e:
            print(json.dumps({"error": str(e)}))
