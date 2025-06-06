"""
SQLite Database Management for AI Red Team Toolkit
Provides database operations for storing and managing system prompts.
"""

import sqlite3
import os
import logging
from datetime import datetime
from typing import List, Dict, Optional

logger = logging.getLogger('app.database')

class Database:
    """Database connection and management class"""
    
    def __init__(self, db_path: str = "redteam_toolkit.db"):
        """Initialize database connection"""
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database tables"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Create system_prompts table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS system_prompts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL UNIQUE,
                        content TEXT NOT NULL,
                        category TEXT DEFAULT 'general',
                        description TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        usage_count INTEGER DEFAULT 0,
                        tags TEXT DEFAULT '',
                        is_active BOOLEAN DEFAULT 1
                    )
                ''')
                
                # Create usage_logs table for tracking prompt usage
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS usage_logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        prompt_id INTEGER,
                        tool_used TEXT,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (prompt_id) REFERENCES system_prompts (id)
                    )
                ''')
                
                # Create trigger to update updated_at timestamp
                cursor.execute('''
                    CREATE TRIGGER IF NOT EXISTS update_system_prompts_timestamp 
                    AFTER UPDATE ON system_prompts
                    BEGIN
                        UPDATE system_prompts SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
                    END
                ''')
                
                conn.commit()
                logger.info("Database initialized successfully")
                
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            raise

class SystemPromptModel:
    """Model class for system prompts database operations"""
    
    def __init__(self, db_path: str = "redteam_toolkit.db"):
        self.db = Database(db_path)
    
    def create_prompt(self, name: str, content: str, category: str = 'general', 
                     description: str = '', tags: str = '') -> int:
        """Create a new system prompt"""
        try:
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO system_prompts (name, content, category, description, tags)
                    VALUES (?, ?, ?, ?, ?)
                ''', (name, content, category, description, tags))
                
                prompt_id = cursor.lastrowid
                conn.commit()
                
                logger.info(f"Created new system prompt: {name} (ID: {prompt_id})")
                return prompt_id
                
        except sqlite3.IntegrityError as e:
            logger.error(f"Prompt name already exists: {name}")
            raise ValueError(f"A prompt with the name '{name}' already exists")
        except Exception as e:
            logger.error(f"Error creating prompt: {e}")
            raise
    
    def get_all_prompts(self, active_only: bool = True) -> List[Dict]:
        """Get all system prompts"""
        try:
            with sqlite3.connect(self.db.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                query = 'SELECT * FROM system_prompts'
                if active_only:
                    query += ' WHERE is_active = 1'
                query += ' ORDER BY name'
                
                cursor.execute(query)
                results = cursor.fetchall()
                
                return [dict(row) for row in results]
                
        except Exception as e:
            logger.error(f"Error getting all prompts: {e}")
            raise
    
    def get_prompt_by_id(self, prompt_id: int) -> Optional[Dict]:
        """Get a specific prompt by ID"""
        try:
            with sqlite3.connect(self.db.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM system_prompts WHERE id = ?', (prompt_id,))
                
                result = cursor.fetchone()
                return dict(result) if result else None
                
        except Exception as e:
            logger.error(f"Error getting prompt by ID {prompt_id}: {e}")
            raise
    
    def get_prompt_by_name(self, name: str) -> Optional[Dict]:
        """Get a specific prompt by name"""
        try:
            with sqlite3.connect(self.db.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM system_prompts WHERE name = ?', (name,))
                
                result = cursor.fetchone()
                return dict(result) if result else None
                
        except Exception as e:
            logger.error(f"Error getting prompt by name {name}: {e}")
            raise
    
    def update_prompt(self, prompt_id: int, name: str = None, content: str = None, 
                     category: str = None, description: str = None, tags: str = None) -> bool:
        """Update an existing prompt"""
        try:
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.cursor()
                
                # Build dynamic update query
                update_fields = []
                values = []
                
                if name is not None:
                    update_fields.append('name = ?')
                    values.append(name)
                if content is not None:
                    update_fields.append('content = ?')
                    values.append(content)
                if category is not None:
                    update_fields.append('category = ?')
                    values.append(category)
                if description is not None:
                    update_fields.append('description = ?')
                    values.append(description)
                if tags is not None:
                    update_fields.append('tags = ?')
                    values.append(tags)
                
                if not update_fields:
                    return True  # Nothing to update
                
                values.append(prompt_id)
                query = f"UPDATE system_prompts SET {', '.join(update_fields)} WHERE id = ?"
                
                cursor.execute(query, values)
                success = cursor.rowcount > 0
                conn.commit()
                
                if success:
                    logger.info(f"Updated prompt ID {prompt_id}")
                else:
                    logger.warning(f"No prompt found with ID {prompt_id}")
                
                return success
                
        except sqlite3.IntegrityError as e:
            logger.error(f"Update failed - name already exists: {name}")
            raise ValueError(f"A prompt with the name '{name}' already exists")
        except Exception as e:
            logger.error(f"Error updating prompt {prompt_id}: {e}")
            raise
    
    def delete_prompt(self, prompt_id: int, soft_delete: bool = True) -> bool:
        """Delete a prompt (soft delete by default)"""
        try:
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.cursor()
                
                if soft_delete:
                    # Soft delete - mark as inactive
                    cursor.execute('UPDATE system_prompts SET is_active = 0 WHERE id = ?', (prompt_id,))
                else:
                    # Hard delete - actually remove from database
                    cursor.execute('DELETE FROM system_prompts WHERE id = ?', (prompt_id,))
                
                success = cursor.rowcount > 0
                conn.commit()
                
                if success:
                    delete_type = "soft deleted" if soft_delete else "deleted"
                    logger.info(f"Prompt ID {prompt_id} {delete_type}")
                else:
                    logger.warning(f"No prompt found with ID {prompt_id}")
                
                return success
                
        except Exception as e:
            logger.error(f"Error deleting prompt {prompt_id}: {e}")
            raise
    
    def search_prompts(self, query: str, category: str = None) -> List[Dict]:
        """Search prompts by name, content, or tags"""
        try:
            with sqlite3.connect(self.db.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                search_query = '''
                    SELECT * FROM system_prompts 
                    WHERE is_active = 1 
                    AND (name LIKE ? OR content LIKE ? OR tags LIKE ? OR description LIKE ?)
                '''
                values = [f'%{query}%'] * 4
                
                if category:
                    search_query += ' AND category = ?'
                    values.append(category)
                
                search_query += ' ORDER BY name'
                
                cursor.execute(search_query, values)
                results = cursor.fetchall()
                
                return [dict(row) for row in results]
                
        except Exception as e:
            logger.error(f"Error searching prompts: {e}")
            raise
    
    def get_categories(self) -> List[str]:
        """Get all unique categories"""
        try:
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT DISTINCT category FROM system_prompts WHERE is_active = 1 ORDER BY category')
                
                results = cursor.fetchall()
                return [row[0] for row in results]
                
        except Exception as e:
            logger.error(f"Error getting categories: {e}")
            raise
    
    def log_usage(self, prompt_id: int, tool_used: str):
        """Log prompt usage for analytics"""
        try:
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.cursor()
                
                # Insert usage log
                cursor.execute('''
                    INSERT INTO usage_logs (prompt_id, tool_used)
                    VALUES (?, ?)
                ''', (prompt_id, tool_used))
                
                # Update usage count
                cursor.execute('''
                    UPDATE system_prompts 
                    SET usage_count = usage_count + 1 
                    WHERE id = ?
                ''', (prompt_id,))
                
                conn.commit()
                logger.info(f"Logged usage for prompt ID {prompt_id} with tool {tool_used}")
                
        except Exception as e:
            logger.error(f"Error logging usage: {e}")
            raise
    
    def get_usage_stats(self, days: int = 30) -> Dict:
        """Get usage statistics for the last N days"""
        try:
            with sqlite3.connect(self.db.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                # Most used prompts
                cursor.execute('''
                    SELECT sp.name, sp.usage_count, COUNT(ul.id) as recent_usage
                    FROM system_prompts sp
                    LEFT JOIN usage_logs ul ON sp.id = ul.prompt_id 
                        AND ul.timestamp >= datetime('now', '-{} days')
                    WHERE sp.is_active = 1
                    GROUP BY sp.id, sp.name, sp.usage_count
                    ORDER BY recent_usage DESC, sp.usage_count DESC
                    LIMIT 10
                '''.format(days))
                
                most_used = [dict(row) for row in cursor.fetchall()]
                
                # Tool usage stats
                cursor.execute('''
                    SELECT tool_used, COUNT(*) as usage_count
                    FROM usage_logs
                    WHERE timestamp >= datetime('now', '-{} days')
                    GROUP BY tool_used
                    ORDER BY usage_count DESC
                '''.format(days))
                
                tool_stats = [dict(row) for row in cursor.fetchall()]
                
                # Total stats
                cursor.execute('SELECT COUNT(*) FROM system_prompts WHERE is_active = 1')
                total_prompts = cursor.fetchone()[0]
                
                cursor.execute('''
                    SELECT COUNT(*) FROM usage_logs 
                    WHERE timestamp >= datetime('now', '-{} days')
                '''.format(days))
                total_usage = cursor.fetchone()[0]
                
                return {
                    'total_prompts': total_prompts,
                    'total_usage_last_{}days'.format(days): total_usage,
                    'most_used_prompts': most_used,
                    'tool_usage_stats': tool_stats
                }
                
        except Exception as e:
            logger.error(f"Error getting usage stats: {e}")
            raise
    
    def import_from_file(self, file_content: str, source_name: str, category: str = 'imported'):
        """Import prompts from text file content"""
        try:
            imported_count = 0
            
            # Split content by sections (assuming they're separated by dashes)
            sections = file_content.split('----------------------------.')
            
            for i, section in enumerate(sections):
                section = section.strip()
                if not section:
                    continue
                
                # Extract name from first line or use a default
                lines = section.split('\n')
                if lines:
                    name = lines[0].strip()
                    if not name or name.startswith('System') or len(name) > 100:
                        name = f"{source_name} - Section {i + 1}"
                    
                    # Use the full section as content
                    content = section
                    
                    # Try to create the prompt (skip if duplicate)
                    try:
                        self.create_prompt(
                            name=name,
                            content=content,
                            category=category,
                            description=f"Imported from {source_name}",
                            tags=f"imported,{source_name.lower().replace(' ', '_')}"
                        )
                        imported_count += 1
                    except ValueError as e:
                        if "already exists" in str(e):
                            logger.info(f"Skipping duplicate prompt: {name}")
                        else:
                            raise
            
            logger.info(f"Imported {imported_count} prompts from {source_name}")
            return imported_count
            
        except Exception as e:
            logger.error(f"Error importing prompts from file: {e}")
            raise
