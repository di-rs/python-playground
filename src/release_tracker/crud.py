from sqlmodel import Session, select

from .models import Project, ProjectCreate, ProjectUpdate


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