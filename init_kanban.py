#!/usr/bin/env python3
"""Initialize Kanban board for TRIBEv2 Evaluation project."""
import sqlite3, os

db = '/opt/data/kanban/boards/tribev2-evaluation/kanban.db'
os.makedirs(os.path.dirname(db), exist_ok=True)

conn = sqlite3.connect(db)
conn.execute('''
CREATE TABLE IF NOT EXISTS board (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP
)''')
conn.execute('''
CREATE TABLE IF NOT EXISTS lists (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  board_id INTEGER REFERENCES board(id),
  title TEXT NOT NULL,
  position INTEGER DEFAULT 0,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP
)''')
conn.execute('''
CREATE TABLE IF NOT EXISTS cards (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  list_id INTEGER REFERENCES lists(id),
  title TEXT NOT NULL,
  description TEXT DEFAULT '',
  position INTEGER DEFAULT 0,
  labels TEXT DEFAULT '',
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT DEFAULT CURRENT_TIMESTAMP
)''')

conn.execute("INSERT OR IGNORE INTO board (id, name) VALUES (1, 'TRIBEv2 Evaluation')")
# Default lists: Backlog, In Progress, Done, Blocked
lists = [('Backlog', 0), ('In Progress', 1), ('Done', 2), ('Blocked', 3)]
for title, pos in lists:
    conn.execute('INSERT OR IGNORE INTO lists (board_id, title, position) VALUES (1, ?, ?)', (title, pos))
conn.commit()
print(f'Kanban board created at {db}')
conn.close()
