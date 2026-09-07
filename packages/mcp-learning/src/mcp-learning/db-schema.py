import os
import sqlite3

from fastmcp import FastMCP

dirname = os.path.dirname(__file__)

mcp = FastMCP(name="issue-server", version="1.0.0")


@mcp.resource(
    uri="schema://database",
    mime_type="text/plain",
    name="database-schema",
    title="Database Schema",
    description="A schema of the database",
)
def database_schema() -> str:
    db_path = os.path.join(dirname, "..", "database.sqlite")

    conn = sqlite3.connect(db_path + "?mode=ro", uri=True)
    cursor = conn.cursor()
    cursor.execute(
        """SELECT sql FROM sqlite_master WHERE type='table'
        AND sql IS NOT NULL ORDER BY name
        """
    )
    tables = cursor.fetchall()

    conn.close()

    tables_sql = [row[0] for row in tables]
    return ";\n".join(tables_sql) + ";" if tables_sql else ""


if __name__ == "__main__":
    mcp.run()
