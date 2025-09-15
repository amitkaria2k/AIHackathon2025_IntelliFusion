# Database configuration for persistent storage
import sqlite3
import json
from typing import Dict, List, Any
from datetime import datetime
import os

class DatabaseManager:
    """Simple database manager for project data persistence"""
    
    def __init__(self, db_path: str = "bosch_projects.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Projects table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                description TEXT,
                functional_reqs TEXT,
                non_functional_reqs TEXT,
                conditions TEXT,
                recommended_docs TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Documents table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                content TEXT,
                status TEXT DEFAULT 'Draft',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (project_id) REFERENCES projects (id)
            )
        ''')
        
        # Project data files table for RAG
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS project_data_files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER,
                filename TEXT NOT NULL,
                file_path TEXT,
                file_type TEXT,
                file_size INTEGER,
                content TEXT,
                content_hash TEXT,
                is_template BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (project_id) REFERENCES projects (id)
            )
        ''')
        
        # Vector embeddings table for RAG
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vector_embeddings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER,
                file_id INTEGER,
                chunk_index INTEGER,
                chunk_text TEXT,
                embedding_vector TEXT,
                metadata TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (project_id) REFERENCES projects (id),
                FOREIGN KEY (file_id) REFERENCES project_data_files (id)
            )
        ''')
        
        # Workflows table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS workflows (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER,
                document_id INTEGER,
                name TEXT NOT NULL,
                status TEXT DEFAULT 'Active',
                approvers TEXT,
                current_step INTEGER DEFAULT 0,
                comments TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (project_id) REFERENCES projects (id),
                FOREIGN KEY (document_id) REFERENCES documents (id)
            )
        ''')
        
        # Workflow comments table for detailed comment history
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS workflow_comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                workflow_id INTEGER,
                approver TEXT NOT NULL,
                action TEXT NOT NULL,
                comment TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (workflow_id) REFERENCES workflows (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_project(self, project: Dict[str, Any]) -> int:
        """Save project to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO projects (name, type, description, functional_reqs, 
                                non_functional_reqs, conditions, recommended_docs)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            project['name'],
            project['type'],
            project['description'],
            json.dumps(project.get('functional_reqs', [])),
            json.dumps(project.get('non_functional_reqs', [])),
            json.dumps(project.get('conditions', [])),
            json.dumps(project.get('recommended_docs', []))
        ))
        
        project_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return project_id
    
    def get_projects(self) -> List[Dict[str, Any]]:
        """Get all projects from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM projects ORDER BY created_at DESC')
        rows = cursor.fetchall()
        
        projects = []
        for row in rows:
            project = {
                'id': row[0],
                'name': row[1],
                'type': row[2],
                'description': row[3],
                'functional_reqs': json.loads(row[4]) if row[4] else [],
                'non_functional_reqs': json.loads(row[5]) if row[5] else [],
                'conditions': json.loads(row[6]) if row[6] else [],
                'recommended_docs': json.loads(row[7]) if row[7] else [],
                'created_at': row[8],
                'updated_at': row[9]
            }
            projects.append(project)
        
        conn.close()
        return projects
    
    def save_document(self, document: Dict[str, Any]) -> int:
        """Save document to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO documents (project_id, name, type, content, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            document['project_id'],
            document['name'],
            document['type'],
            document['content'],
            document.get('status', 'Draft')
        ))
        
        document_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return document_id
    
    def get_documents(self, project_id: int = None) -> List[Dict[str, Any]]:
        """Get documents from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if project_id:
            cursor.execute('SELECT * FROM documents WHERE project_id = ? ORDER BY created_at DESC', (project_id,))
        else:
            cursor.execute('SELECT * FROM documents ORDER BY created_at DESC')
        
        rows = cursor.fetchall()
        
        documents = []
        for row in rows:
            document = {
                'id': row[0],
                'project_id': row[1],
                'name': row[2],
                'type': row[3],
                'content': row[4],
                'status': row[5],
                'created_at': row[6],
                'updated_at': row[7]
            }
            documents.append(document)
        
        conn.close()
        return documents
    
    def save_workflow(self, workflow: Dict[str, Any]) -> int:
        """Save workflow to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO workflows (project_id, document_id, name, status, approvers, current_step)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            workflow['project_id'],
            workflow.get('document_id'),
            workflow['name'],
            workflow.get('status', 'Active'),
            json.dumps(workflow.get('approvers', [])),
            workflow.get('current_step', 0)
        ))
        
        workflow_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return workflow_id
    
    def get_workflows(self, project_id: int = None) -> List[Dict[str, Any]]:
        """Get workflows from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if project_id:
            cursor.execute('SELECT * FROM workflows WHERE project_id = ? ORDER BY created_at DESC', (project_id,))
        else:
            cursor.execute('SELECT * FROM workflows ORDER BY created_at DESC')
        
        rows = cursor.fetchall()
        
        workflows = []
        for row in rows:
            workflow = {
                'id': row[0],
                'project_id': row[1],
                'document_id': row[2],
                'name': row[3],
                'status': row[4],
                'approvers': json.loads(row[5]) if row[5] else [],
                'current_step': row[6],
                'created_at': row[7],
                'updated_at': row[8]
            }
            workflows.append(workflow)
        
        conn.close()
        return workflows
    
    def update_workflow(self, workflow_id: int, updates: Dict[str, Any]):
        """Update workflow in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        set_clause = ', '.join([f"{key} = ?" for key in updates.keys()])
        values = list(updates.values())
        values.append(workflow_id)
        
        cursor.execute(f'''
            UPDATE workflows 
            SET {set_clause}, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', values)
        
        conn.commit()
        conn.close()
    
    def update_document(self, document_id: int, updates: Dict[str, Any]):
        """Update document in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        set_clause = ', '.join([f"{key} = ?" for key in updates.keys()])
        values = list(updates.values())
        values.append(document_id)
        
        cursor.execute(f'''
            UPDATE documents 
            SET {set_clause}, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', values)
        
        conn.commit()
        conn.close()
    
    def update_project(self, project_id: int, updates: Dict[str, Any]):
        """Update project in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Handle list fields
        processed_updates = {}
        for key, value in updates.items():
            if key in ['functional_reqs', 'non_functional_reqs', 'conditions', 'recommended_docs'] and isinstance(value, list):
                processed_updates[key] = json.dumps(value)
            else:
                processed_updates[key] = value
        
        set_clause = ', '.join([f"{key} = ?" for key in processed_updates.keys()])
        values = list(processed_updates.values())
        values.append(project_id)
        
        cursor.execute(f'''
            UPDATE projects 
            SET {set_clause}, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', values)
        
        conn.commit()
        conn.close()
    
    def delete_project(self, project_id: int):
        """Delete project and all related data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Delete related workflow comments first
        cursor.execute('''
            DELETE FROM workflow_comments 
            WHERE workflow_id IN (
                SELECT id FROM workflows WHERE project_id = ?
            )
        ''', (project_id,))
        
        # Delete related workflows
        cursor.execute('DELETE FROM workflows WHERE project_id = ?', (project_id,))
        
        # Delete related documents
        cursor.execute('DELETE FROM documents WHERE project_id = ?', (project_id,))
        
        # Delete project data files and embeddings
        cursor.execute('DELETE FROM vector_embeddings WHERE project_id = ?', (project_id,))
        cursor.execute('DELETE FROM project_data_files WHERE project_id = ?', (project_id,))
        
        # Delete project
        cursor.execute('DELETE FROM projects WHERE id = ?', (project_id,))
        
        conn.commit()
        conn.close()
    
    def delete_multiple_projects(self, project_ids: List[int]):
        """Delete multiple projects and all related data"""
        for project_id in project_ids:
            self.delete_project(project_id)
    
    # Project Data Files Management
    def save_project_data_file(self, project_id: int, filename: str, file_path: str, file_type: str, 
                               file_size: int, content: str, content_hash: str, is_template: bool = False) -> int:
        """Save project data file information"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO project_data_files 
            (project_id, filename, file_path, file_type, file_size, content, content_hash, is_template)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (project_id, filename, file_path, file_type, file_size, content, content_hash, is_template))
        
        file_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return file_id
    
    def get_project_data_files(self, project_id: int, include_templates: bool = True) -> List[Dict]:
        """Get all data files for a project"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if include_templates:
            cursor.execute('''
                SELECT * FROM project_data_files WHERE project_id = ?
                ORDER BY created_at DESC
            ''', (project_id,))
        else:
            cursor.execute('''
                SELECT * FROM project_data_files WHERE project_id = ? AND is_template = FALSE
                ORDER BY created_at DESC
            ''', (project_id,))
        
        columns = [col[0] for col in cursor.description]
        files = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        conn.close()
        return files
    
    def delete_project_data_file(self, file_id: int):
        """Delete a project data file and its embeddings"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Delete associated embeddings
        cursor.execute('DELETE FROM vector_embeddings WHERE file_id = ?', (file_id,))
        
        # Delete file record
        cursor.execute('DELETE FROM project_data_files WHERE id = ?', (file_id,))
        
        conn.commit()
        conn.close()
    
    # Vector Embeddings Management
    def save_vector_embedding(self, project_id: int, file_id: int, chunk_index: int, 
                              chunk_text: str, embedding_vector: List[float], metadata: Dict = None):
        """Save vector embedding for text chunk"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Convert embedding to JSON string
        embedding_json = json.dumps(embedding_vector)
        metadata_json = json.dumps(metadata or {})
        
        cursor.execute('''
            INSERT INTO vector_embeddings 
            (project_id, file_id, chunk_index, chunk_text, embedding_vector, metadata)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (project_id, file_id, chunk_index, chunk_text, embedding_json, metadata_json))
        
        conn.commit()
        conn.close()
    
    def get_vector_embeddings(self, project_id: int) -> List[Dict]:
        """Get all vector embeddings for a project"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT ve.*, pdf.filename 
            FROM vector_embeddings ve
            JOIN project_data_files pdf ON ve.file_id = pdf.id
            WHERE ve.project_id = ?
            ORDER BY ve.file_id, ve.chunk_index
        ''', (project_id,))
        
        columns = [col[0] for col in cursor.description]
        embeddings = []
        
        for row in cursor.fetchall():
            embedding_dict = dict(zip(columns, row))
            # Parse JSON fields
            embedding_dict['embedding_vector'] = json.loads(embedding_dict['embedding_vector'])
            embedding_dict['metadata'] = json.loads(embedding_dict['metadata'])
            embeddings.append(embedding_dict)
        
        conn.close()
        return embeddings
    
    def add_workflow_comment(self, workflow_id: int, approver: str, action: str, comment: str = ""):
        """Add comment to workflow"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO workflow_comments (workflow_id, approver, action, comment)
            VALUES (?, ?, ?, ?)
        ''', (workflow_id, approver, action, comment))
        
        conn.commit()
        conn.close()
    
    def get_workflow_comments(self, workflow_id: int) -> List[Dict[str, Any]]:
        """Get all comments for a workflow"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM workflow_comments 
            WHERE workflow_id = ? 
            ORDER BY created_at ASC
        ''', (workflow_id,))
        
        rows = cursor.fetchall()
        
        comments = []
        for row in rows:
            comment = {
                'id': row[0],
                'workflow_id': row[1],
                'approver': row[2],
                'action': row[3],
                'comment': row[4],
                'created_at': row[5]
            }
            comments.append(comment)
        
        conn.close()
        return comments
