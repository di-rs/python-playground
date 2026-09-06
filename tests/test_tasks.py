from fastapi.testclient import TestClient

from release_tracker.models import TaskStatus


def test_create_task(client: TestClient, sample_project_id: int):
    response = client.post(
        f"/projects/{sample_project_id}/tasks",
        json={
            "title": "Add settings page",
            "priority": "high",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Add settings page"
    assert data["status"] == "planned"
    assert data["priority"] == "high"
    assert data["project_id"] == sample_project_id
    assert data["project_name"] == "Release Platform"
    assert data["project_slug"] == "release-platform"


def test_get_task(client: TestClient, sample_task_id: int):
    response = client.get(f"/tasks/{sample_task_id}")
    assert response.status_code == 200
    assert response.json()["id"] == sample_task_id


def test_get_task_not_found(client: TestClient):
    response = client.get("/tasks/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}


def test_list_tasks_filter_by_status(
    client: TestClient, sample_project_id: int
):
    client.post(
        f"/projects/{sample_project_id}/tasks",
        json={
            "title": "Done task",
            "status": TaskStatus.done,
        },
    )
    client.post(
        f"/projects/{sample_project_id}/tasks",
        json={
            "title": "Planned task",
            "status": TaskStatus.planned,
        },
    )

    response = client.get(
        "/tasks",
        params={
            "status": TaskStatus.done,
        },
    )
    assert response.status_code == 200

    titles = [task["title"] for task in response.json()]
    assert titles == ["Done task"]


def test_list_tasks_filter_by_project_slug(
    client: TestClient, sample_project_id: int
):
    response = client.post(
        "/projects",
        json={
            "name": "Second Project",
            "description": "A test project",
        },
    )
    assert response.status_code == 201
    second_project = response.json()

    client.post(
        f"/projects/{sample_project_id}/tasks",
        json={
            "title": "First project task",
        },
    )
    client.post(
        f"/projects/{second_project['id']}/tasks",
        json={
            "title": "Second project task",
        },
    )

    response = client.get(
        "/tasks",
        params={
            "project_slug": second_project["slug"],
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == second_project["id"]

    titles = [task["title"] for task in response.json()]
    assert titles == ["Second project task"]
