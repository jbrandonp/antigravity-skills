#!/usr/bin/env python3
"""
Kate MySQL Sync Engine
Two-way sync between Hermes memory and MySQL kate_sync database.
Run: python3 kate_mysql_sync.py [--pull | --push | --full]
"""

import mysql.connector
import json
import sys
from datetime import datetime

MYSQL_CONFIG = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': '2108',
    'database': 'kate_sync'
}

def get_mysql_connection():
    return mysql.connector.connect(**MYSQL_CONFIG)

def pull_memories():
    """Pull memories from MySQL and format for Hermes memory injection."""
    conn = get_mysql_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT id, target, content, created_at FROM memory_store ORDER BY id")
    rows = cursor.fetchall()
    
    cursor.execute("SELECT key_name, value_text, category FROM user_profile ORDER BY category, priority DESC")
    profile = cursor.fetchall()
    
    cursor.execute("SELECT name, description, status FROM projects WHERE status='active'")
    projects = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    output = {
        'memories': rows,
        'profile': profile,
        'projects': projects,
        'synced_at': datetime.now().isoformat(),
        'stats': {
            'memories': len(rows),
            'profile_entries': len(profile),
            'projects': len(projects)
        }
    }
    
    return output

def push_to_mysql(memory_entries, profile_entries=None, project_entries=None):
    """Push new entries to MySQL."""
    conn = get_mysql_connection()
    cursor = conn.cursor()
    inserted = {'memory': 0, 'profile': 0, 'projects': 0}
    
    for target, content in memory_entries:
        # Check for duplicate
        cursor.execute("SELECT id FROM memory_store WHERE target=%s AND content=%s", (target, content))
        if not cursor.fetchone():
            cursor.execute("INSERT INTO memory_store (target, content) VALUES (%s, %s)", (target, content))
            inserted['memory'] += 1
    
    if profile_entries:
        for key, value, cat, prio in profile_entries:
            cursor.execute(
                """INSERT INTO user_profile (key_name, value_text, category, priority) 
                   VALUES (%s, %s, %s, %s) 
                   ON DUPLICATE KEY UPDATE value_text=VALUES(value_text), priority=VALUES(priority)""",
                (key, value, cat, prio)
            )
            inserted['profile'] += 1
    
    if project_entries:
        for name, desc, status in project_entries:
            cursor.execute(
                "INSERT IGNORE INTO projects (name, description, status) VALUES (%s, %s, %s)",
                (name, desc, status)
            )
            inserted['projects'] += 1
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return inserted

def get_stats():
    """Get sync statistics."""
    conn = get_mysql_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            (SELECT COUNT(*) FROM memory_store) as memories,
            (SELECT COUNT(*) FROM user_profile) as profile_entries,
            (SELECT COUNT(*) FROM projects) as projects,
            (SELECT COUNT(*) FROM sessions_log) as sessions,
            (SELECT COUNT(*) FROM lessons) as lessons
    """)
    stats = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return {
        'memories': stats[0],
        'profile_entries': stats[1],
        'projects': stats[2],
        'sessions': stats[3],
        'lessons': stats[4]
    }

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Kate MySQL Sync Engine')
    parser.add_argument('--pull', action='store_true', help='Pull data from MySQL')
    parser.add_argument('--push', action='store_true', help='Push data to MySQL (placeholder)')
    parser.add_argument('--full', action='store_true', help='Full two-way sync')
    parser.add_argument('--stats', action='store_true', help='Show sync stats')
    args = parser.parse_args()
    
    if args.pull:
        data = pull_memories()
        print(json.dumps(data, indent=2, default=str))
    elif args.push:
        print("Push mode: use from within Hermes context")
    elif args.full:
        data = pull_memories()
        print(f"Synced: {data['stats']}")
    elif args.stats:
        print(json.dumps(get_stats(), indent=2))
    else:
        print(json.dumps(get_stats(), indent=2))
