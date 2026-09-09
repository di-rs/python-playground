from pathlib import Path

from neo4j import Driver
from neo5j.database import get_neo4j_db


def seed(client: Driver):
    source = Path("samples/sample-neo4j.cql").read_text()
    statements = [
        statement.strip()
        for statement in source.split(";")
        if statement.strip()
    ]

    for statement in statements:
        client.execute_query(statement)  # pyright: ignore[reportCallIssue, reportArgumentType]

    print("Done")


if __name__ == "__main__":
    with get_neo4j_db() as client:
        seed(client)
