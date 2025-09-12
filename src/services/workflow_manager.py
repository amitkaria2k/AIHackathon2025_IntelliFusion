"""
Workflow Manager Service for handling approval processes
"""
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from ..config import Config
from ..database import get_session_local, Workflow, WorkflowTask, Document as DocumentModel

class WorkflowManagerService:
    """Service for managing document approval workflows"""
    
    def __init__(self):
        """Initialize the workflow manager service"""
        self.default_approvers = Config.DEFAULT_APPROVERS
    
    def create_approval_workflow(self, 
                               project_id: str, 
                               document_id: str,
                               workflow_name: str,
                               approvers: Optional[List[str]] = None) -> str:
        """
        Create a new approval workflow for a document
        
        Args:
            project_id: ID of the project
            document_id: ID of the document
            workflow_name: Name of the workflow
            approvers: List of approver names (uses default if not provided)
            
        Returns:
            Workflow ID
        """
        
        SessionLocal = get_session_local()
        db = SessionLocal()
        try:
            # Use default approvers if none provided
            if not approvers:
                approvers = self.default_approvers
            
            # Create workflow
            workflow = Workflow(
                project_id=project_id,
                name=workflow_name,
                description=f"Approval workflow for document review",
                status="Active"
            )
            
            db.add(workflow)
            db.commit()
            
            # Create workflow tasks for each approver
            for i, approver in enumerate(approvers):
                due_date = datetime.now() + timedelta(days=3 * (i + 1))  # Staggered due dates
                
                task = WorkflowTask(
                    workflow_id=workflow.id,
                    document_id=document_id,
                    task_name=f"Review and approve document",
                    assignee=approver.strip(),
                    status="Pending",
                    priority="Medium",
                    due_date=due_date,
                    comments=""
                )
                
                db.add(task)
            
            db.commit()
            return workflow.id
            
        except Exception as e:
            db.rollback()
            raise Exception(f"Error creating workflow: {str(e)}")
        finally:
            db.close()
    
    def get_pending_tasks(self, assignee: Optional[str] = None) -> List[Dict]:
        """
        Get pending workflow tasks
        
        Args:
            assignee: Filter by assignee (optional)
            
        Returns:
            List of pending tasks
        """
        
        db = SessionLocal()
        try:
            query = db.query(WorkflowTask).filter(WorkflowTask.status == "Pending")
            
            if assignee:
                query = query.filter(WorkflowTask.assignee == assignee)
            
            tasks = query.all()
            
            result = []
            for task in tasks:
                # Get document info
                document = db.query(DocumentModel).filter(DocumentModel.id == task.document_id).first()
                
                result.append({
                    "task_id": task.id,
                    "workflow_id": task.workflow_id,
                    "document_id": task.document_id,
                    "document_name": document.name if document else "Unknown",
                    "document_type": document.document_type if document else "Unknown",
                    "task_name": task.task_name,
                    "assignee": task.assignee,
                    "priority": task.priority,
                    "due_date": task.due_date.isoformat() if task.due_date else None,
                    "created_at": task.created_at.isoformat(),
                    "comments": task.comments
                })
            
            return result
            
        except Exception as e:
            raise Exception(f"Error retrieving pending tasks: {str(e)}")
        finally:
            db.close()
    
    def complete_task(self, 
                     task_id: str, 
                     status: str, 
                     comments: Optional[str] = None) -> bool:
        """
        Complete a workflow task
        
        Args:
            task_id: ID of the task
            status: New status (Approved/Rejected)
            comments: Optional comments
            
        Returns:
            True if successful
        """
        
        db = SessionLocal()
        try:
            task = db.query(WorkflowTask).filter(WorkflowTask.id == task_id).first()
            
            if not task:
                raise Exception("Task not found")
            
            # Update task
            task.status = status
            task.completed_at = datetime.now()
            task.comments = comments or ""
            
            db.commit()
            
            # Check if workflow is complete
            self._check_workflow_completion(db, task.workflow_id)
            
            return True
            
        except Exception as e:
            db.rollback()
            raise Exception(f"Error completing task: {str(e)}")
        finally:
            db.close()
    
    def _check_workflow_completion(self, db: Session, workflow_id: str):
        """Check if workflow is complete and update document status"""
        
        # Get all tasks for this workflow
        tasks = db.query(WorkflowTask).filter(WorkflowTask.workflow_id == workflow_id).all()
        
        if not tasks:
            return
        
        # Check if all tasks are complete
        pending_tasks = [t for t in tasks if t.status == "Pending"]
        rejected_tasks = [t for t in tasks if t.status == "Rejected"]
        
        if not pending_tasks:  # All tasks completed
            workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
            
            if rejected_tasks:
                # If any task was rejected, mark workflow as cancelled
                workflow.status = "Cancelled"
                # Update document status
                if tasks[0].document_id:
                    document = db.query(DocumentModel).filter(DocumentModel.id == tasks[0].document_id).first()
                    if document:
                        document.status = "Rejected"
            else:
                # All approved, mark workflow as completed
                workflow.status = "Completed"
                # Update document status
                if tasks[0].document_id:
                    document = db.query(DocumentModel).filter(DocumentModel.id == tasks[0].document_id).first()
                    if document:
                        document.status = "Approved"
            
            db.commit()
    
    def get_workflow_status(self, workflow_id: str) -> Dict:
        """
        Get workflow status and progress
        
        Args:
            workflow_id: ID of the workflow
            
        Returns:
            Workflow status information
        """
        
        db = SessionLocal()
        try:
            workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
            
            if not workflow:
                raise Exception("Workflow not found")
            
            tasks = db.query(WorkflowTask).filter(WorkflowTask.workflow_id == workflow_id).all()
            
            # Calculate progress
            total_tasks = len(tasks)
            completed_tasks = len([t for t in tasks if t.status in ["Approved", "Rejected"]])
            pending_tasks = len([t for t in tasks if t.status == "Pending"])
            approved_tasks = len([t for t in tasks if t.status == "Approved"])
            rejected_tasks = len([t for t in tasks if t.status == "Rejected"])
            
            progress_percentage = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
            
            return {
                "workflow_id": workflow.id,
                "name": workflow.name,
                "status": workflow.status,
                "progress_percentage": round(progress_percentage, 2),
                "total_tasks": total_tasks,
                "completed_tasks": completed_tasks,
                "pending_tasks": pending_tasks,
                "approved_tasks": approved_tasks,
                "rejected_tasks": rejected_tasks,
                "created_at": workflow.created_at.isoformat(),
                "tasks": [
                    {
                        "task_id": task.id,
                        "assignee": task.assignee,
                        "status": task.status,
                        "due_date": task.due_date.isoformat() if task.due_date else None,
                        "completed_at": task.completed_at.isoformat() if task.completed_at else None,
                        "comments": task.comments
                    } for task in tasks
                ]
            }
            
        except Exception as e:
            raise Exception(f"Error retrieving workflow status: {str(e)}")
        finally:
            db.close()
    
    def get_project_workflows(self, project_id: str) -> List[Dict]:
        """Get all workflows for a project"""
        
        db = SessionLocal()
        try:
            workflows = db.query(Workflow).filter(Workflow.project_id == project_id).all()
            
            result = []
            for workflow in workflows:
                tasks = db.query(WorkflowTask).filter(WorkflowTask.workflow_id == workflow.id).all()
                
                total_tasks = len(tasks)
                completed_tasks = len([t for t in tasks if t.status in ["Approved", "Rejected"]])
                progress = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
                
                result.append({
                    "workflow_id": workflow.id,
                    "name": workflow.name,
                    "status": workflow.status,
                    "progress_percentage": round(progress, 2),
                    "total_tasks": total_tasks,
                    "completed_tasks": completed_tasks,
                    "created_at": workflow.created_at.isoformat()
                })
            
            return result
            
        except Exception as e:
            raise Exception(f"Error retrieving project workflows: {str(e)}")
        finally:
            db.close()
