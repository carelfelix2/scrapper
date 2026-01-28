from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.core.security import verify_token
from app.schemas.schemas import (
    ScrapingTaskInput, ScrapingTaskResponse, ScrapingTaskDetailResponse,
    SuccessResponse, PaginatedResponse
)
from app.services.scraping_service import ScrapingTaskService

router = APIRouter(prefix="/api/v1/tasks", tags=["Scraping Tasks"])

def get_current_user_id(authorization: Optional[str] = None) -> int:
    """Dependency to extract user ID from token"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    token = authorization.split(" ")[1]
    return verify_token(token)

@router.post("", response_model=SuccessResponse)
async def create_scraping_task(
    task_input: ScrapingTaskInput,
    db: Session = Depends(get_db),
    authorization: Optional[str] = None
):
    """Create a new scraping task"""
    user_id = get_current_user_id(authorization)
    
    try:
        task = ScrapingTaskService.create_task(db, user_id, task_input)
        return SuccessResponse(
            success=True,
            message="Scraping task created successfully",
            data=ScrapingTaskResponse.model_validate(task)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating task: {str(e)}"
        )

@router.get("/{task_id}", response_model=SuccessResponse)
async def get_scraping_task(
    task_id: int,
    db: Session = Depends(get_db),
    authorization: Optional[str] = None
):
    """Get a specific scraping task"""
    user_id = get_current_user_id(authorization)
    
    task = ScrapingTaskService.get_task_by_id(db, task_id, user_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    return SuccessResponse(
        success=True,
        message="Task retrieved successfully",
        data=ScrapingTaskDetailResponse.model_validate(task)
    )

@router.get("", response_model=SuccessResponse)
async def list_scraping_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    authorization: Optional[str] = None
):
    """List all scraping tasks for the current user"""
    user_id = get_current_user_id(authorization)
    
    tasks = ScrapingTaskService.get_user_tasks(db, user_id, skip, limit)
    total = ScrapingTaskService.get_tasks_count(db, user_id)
    
    return SuccessResponse(
        success=True,
        message="Tasks retrieved successfully",
        data=PaginatedResponse(
            total=total,
            page=skip // limit + 1,
            page_size=limit,
            items=[ScrapingTaskResponse.model_validate(task) for task in tasks]
        )
    )
