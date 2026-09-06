from datetime import UTC, datetime

from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

from release_tracker.dependencies import SessionDep

from .models import (
    Project,
    ProjectCreate,
    ProjectUpdate,
    Task,
    TaskCreate,
    TaskPriority,
    TaskStatus,
    TaskUpdate,
)


def slugify(value: str) -> str:
    cleaned = "".join(c for c in value.lower() if c.isalnum() or c == " ")
    return "-".join(cleaned.split()) or "project"


def list_projects(session: Session) -> list[Project]:
    statement = select(Project).order_by(Project.name)
    projects = session.exec(statement).all()
    return list(projects)


def get_project(session: Session, project_id: int) -> Project | None:
    project = session.get(Project, project_id)
    return project


def create_project(session: Session, payload: ProjectCreate) -> Project:
    project = Project.model_validate(
        payload, update={"slug": slugify(payload.name)}
    )
    session.add(project)
    session.commit()
    session.refresh(project)
    return project


def update_project(
    session: Session, project: Project, payload: ProjectUpdate
) -> Project:
    updated_fields = payload.model_dump(exclude_unset=True)
    project.sqlmodel_update(updated_fields)

    if "name" in updated_fields and updated_fields["name"] is not None:
        project.slug = slugify(updated_fields["name"])

    session.add(project)
    session.commit()
    session.refresh(project)
    return project


def delete_project(session: Session, project: Project) -> None:
    session.delete(project)
    session.commit()


def list_tasks(
    session: Session,
    *,
    project_id: int | None = None,
    project_slug: str | None = None,
    task_status: TaskStatus | None = None,
    task_priority: TaskPriority | None = None,
    overdue_only: bool = False,
) -> list[Task]:
    statement = select(Task).options(selectinload(Task.project))  # type: ignore[arg-type]

    if project_id is not None:
        statement = statement.where(Task.project_id == project_id)
    if project_slug is not None:
        statement = statement.join(Project).where(Project.slug == project_slug)
    if task_status is not None:
        statement = statement.where(Task.status == task_status)
    if task_priority is not None:
        statement = statement.where(Task.priority == task_priority)
    if overdue_only:
        statement = statement.where(
            Task.due_date != None,  # noqa: E711
            Task.due_date < datetime.now(tz=UTC).date(),  # type: ignore[operator]
            Task.status is not TaskStatus.done,
        )

    tasks = session.exec(statement).all()
    return list(tasks)


def get_task(session: SessionDep, task_id: int) -> Task | None:
    statement = (
        select(Task)
        .options(selectinload(Task.project))  # type: ignore[arg-type]
        .where(Task.id == task_id)
    )
    return session.exec(statement).first()


def create_task(
    session: Session, project_id: int | None, payload: TaskCreate
) -> Task:
    task = Task.model_validate(payload, update={"project_id": project_id})
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def update_task(session: Session, task: Task, payload: TaskUpdate) -> Task:
    task.sqlmodel_update(payload.model_dump(exclude_unset=True))
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def delete_task(session: Session, task: Task) -> None:
    session.delete(task)
    session.commit()
