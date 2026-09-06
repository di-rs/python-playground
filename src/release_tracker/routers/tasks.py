from typing import Annotated

from fastapi import APIRouter, Query, status

from .. import crud
from ..dependencies import ProjectDep, SessionDep, TaskDep
from ..models import TaskCreate, TaskPriority, TaskRead, TaskStatus, TaskUpdate

router = APIRouter(tags=["tasks"])


@router.get("/tasks", response_model=list[TaskRead])
def list_tasks(
    session: SessionDep,
    project_id: int | None = None,
    project_slug: str | None = None,
    task_status: Annotated[TaskStatus | None, Query(alias="status")] = None,
    task_priority: Annotated[
        TaskPriority | None, Query(alias="priority")
    ] = None,
    overdue_only: bool = False,
):
    return crud.list_tasks(
        session,
        project_id=project_id,
        project_slug=project_slug,
        task_status=task_status,
        task_priority=task_priority,
        overdue_only=overdue_only,
    )


@router.post(
    "/projects/{project_id}/tasks",
    status_code=status.HTTP_201_CREATED,
    response_model=TaskRead,
)
def create_task(project: ProjectDep, payload: TaskCreate, session: SessionDep):
    return crud.create_task(session, project.id, payload)


@router.get(
    "/tasks/{task_id}", status_code=status.HTTP_200_OK, response_model=TaskRead
)
def get_task(task: TaskDep):
    return task


@router.patch(
    "/tasks/{task_id}", status_code=status.HTTP_200_OK, response_model=TaskRead
)
def update_task(task: TaskDep, session: SessionDep, payload: TaskUpdate):
    return crud.update_task(session, task, payload)


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task: TaskDep, session: SessionDep):
    crud.delete_task(session, task)
