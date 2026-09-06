from fastapi import APIRouter, status

from .. import crud
from ..dependencies import CurrentUserDep, ProjectDep, SessionDep
from ..models import ProjectCreate, ProjectRead, ProjectUpdate

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("", response_model=list[ProjectRead])
def list_projects(session: SessionDep):
    return crud.list_projects(session)


@router.post(
    "", response_model=ProjectRead, status_code=status.HTTP_201_CREATED
)
def create_project(
    payload: ProjectCreate, session: SessionDep, current_user: CurrentUserDep
):
    return crud.create_project(payload=payload, session=session)


@router.get("/{project_id}", response_model=ProjectRead)
def get_project(project: ProjectDep):
    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project: ProjectDep, session: SessionDep):
    crud.delete_project(session, project)


@router.patch("/{project_id}", response_model=ProjectRead)
def update_project(
    project: ProjectDep, payload: ProjectUpdate, session: SessionDep
):
    return crud.update_project(session, project, payload=payload)
