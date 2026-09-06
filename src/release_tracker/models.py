from datetime import UTC, date, datetime
from enum import StrEnum, auto
from typing import Annotated, Literal

from pydantic import EmailStr, StringConstraints
from sqlalchemy import Column, DateTime
from sqlmodel import Field, Relationship, SQLModel


class TaskStatus(StrEnum):
    planned = auto()
    in_progress = auto()
    blocked = auto()
    done = auto()


class TaskPriority(StrEnum):
    low = auto()
    medium = auto()
    high = auto()
    urgent = auto()


def utc_now() -> datetime:
    return datetime.now(UTC)


ProjectName = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=2),
]

TaskTitle = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=2),
]


class ProjectBase(SQLModel):
    name: ProjectName = Field(unique=True)
    description: str | None = None


class Project(ProjectBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    slug: str = Field(unique=True)

    tasks: list[Task] = Relationship(back_populates="project")

    created_at: datetime = Field(
        default_factory=utc_now,
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(SQLModel):
    name: ProjectName | None = None
    description: str | None = None


class ProjectRead(ProjectBase):
    id: int
    slug: str
    created_at: datetime


class TaskBase(SQLModel):
    title: TaskTitle
    details: str | None = None
    status: TaskStatus = TaskStatus.planned
    priority: TaskPriority = TaskPriority.medium
    due_date: date | None = None


class Task(TaskBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="project.id", index=True)

    project: Project = Relationship(back_populates="tasks")

    @property
    def project_name(self) -> str:
        return self.project.name

    @property
    def project_slug(self) -> str:
        return self.project.slug

    created_at: datetime = Field(
        default_factory=utc_now,
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )


class TaskCreate(TaskBase):
    pass


class TaskUpdate(SQLModel):
    title: TaskTitle | None = None
    details: str | None = None
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    due_date: date | None = None


class TaskRead(TaskBase):
    id: int
    project_id: int
    project_name: str
    project_slug: str
    created_at: datetime


class UserBase(SQLModel):
    email: EmailStr = Field(unique=True)
    is_active: bool = True


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str


class UserCreate(SQLModel):
    email: EmailStr
    password: str


class UserRead(UserBase):
    id: int


class AccessToken(SQLModel):
    access_token: str
    token_type: Literal["bearer"] = "bearer"
