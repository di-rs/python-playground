project_names = ["Payments API", "Developer Portal", "Ops Console"]

slugs = [name.lower().replace(" ", "-") for name in project_names]

tasks = [
    {"title": "ship docs", "done": False},
    {"title": "cut release", "done": True},
    {"title": "announce launch", "done": False},
]

open_titles = [task["title"] for task in tasks if not task["done"]]


def validate_project_name(name: str) -> str:
    stripped = name.strip()
    if len(stripped) == 0:
        raise ValueError("Project name cannot be blank.")
    return stripped
