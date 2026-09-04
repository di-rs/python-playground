from dataclasses import dataclass
from datetime import date, timedelta
from enum import StrEnum, auto


@dataclass
class Project:
    name: str
    slug: str
    archived: bool = False

    def archive(self) -> None:
        self.archived = True


def slugify(name: str, sep="-") -> str:
    cleaned = name.strip().lower()
    return cleaned.replace(" ", sep)


def add_tag(name: str, tags: list[str] | None = None):
    if tags is None:
        tags = []
    tags.append(name)
    return tags


def add_tag_global(name, tags=[]):
    tags.append(name)
    return tags


def archive_project(name: str, *, notify=False, force=False):
    if force:
        print(f"Force archive {name}")
    if notify:
        print(f"Sent notification to {name}")


class TaskStatus(StrEnum):
    planned = "planned"
    in_progress = auto()
    blocked = auto()
    done = auto()

    def next_status(self) -> TaskStatus:
        match self:
            case TaskStatus.planned:
                return TaskStatus.in_progress
            case TaskStatus.in_progress:
                return TaskStatus.done
            case TaskStatus.blocked | TaskStatus.done:
                return self


def is_overdue(due_date: date | None, status: TaskStatus) -> bool:
    if not due_date or status == TaskStatus.done:
        return False

    return due_date < date.today()


def next_status(current: TaskStatus) -> TaskStatus:
    match current:
        case TaskStatus.planned:
            return TaskStatus.in_progress
        case TaskStatus.in_progress:
            return TaskStatus.done
        case TaskStatus.blocked | TaskStatus.done:
            return current


def main():
    print("Hello from learn-python!")
    name = f"   SDDSS {None}"
    print(name.strip().lower(), True, None)
    name = name * 2
    print(name, date.today())
    print(slugify(name, sep="_"))
    print(
        add_tag("foo"),
        add_tag("bar"),
        add_tag("baz"),
    )
    print(
        add_tag_global("foo"),
        add_tag_global("bar"),
        add_tag_global("baz"),
    )
    print(archive_project("name-dpsd", force=True, notify=True))
    print(Project("name", slug="ds-ds"))

    yesterday = date.today() - timedelta(days=1)

    print(is_overdue(None, TaskStatus.planned))  # False
    print(is_overdue(yesterday, TaskStatus.done))  # False
    print(is_overdue(yesterday, TaskStatus.in_progress))  # True

    print(next_status(TaskStatus.planned))  # TaskStatus.in_progress
    print(next_status(TaskStatus.in_progress))  # TaskStatus.done
    print(next_status(TaskStatus.done))  # TaskStatus.done
    print(next_status(TaskStatus.blocked))  # TaskStatus.blocked


if __name__ == "__main__":
    main()
