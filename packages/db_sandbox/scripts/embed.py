import sys
from sys import argv

from db_sandbox.config import get_settings
from db_sandbox.database import get_pg_pool
from pgvector.psycopg import register_vector
from requests import request

BATCH_SIZE = 50


ollama = {
    "dimensions": 768,
    "model": "nomic-embed-text",
    "url": get_settings().ollama_host_url,
}


def ollama_embed(texts: list[str]) -> list[list[float]]:
    res = request(
        method="POST",
        url=f"{ollama['url']}/api/embed",
        headers={"Content-Type": "application/json"},
        json={"model": ollama["model"], "input": texts},
    )
    if not res.ok:
        raise RuntimeError(f"Ollama API error: ${res.status_code} ${res.text}")

    return res.json()["embeddings"]


def get_embeddings(text: str) -> None:
    embedding = ollama_embed([text])
    print(",".join(str(v) for v in embedding[0]))


def generate_comments_embeddings() -> None:
    with get_pg_pool().connection() as conn:
        conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
        register_vector(conn)

        print(
            f"Using ollama "
            f"({ollama['model']}, {ollama['dimensions']} dimensions)"
        )

        conn.execute("""
            ALTER TABLE comments
            DROP COLUMN IF EXISTS embedding
        """)
        conn.execute(
            t"""ALTER TABLE comments
            ADD COLUMN embedding vector({ollama["dimensions"]:l})
            """
        )

        rows = conn.execute(
            "SELECT comment_id, comment FROM comments ORDER BY comment_id"
        ).fetchall()
        rows_len = len(rows)
        print(f"Found {rows_len} comments to embed")

        with conn.cursor() as cur:
            for i in range(0, rows_len, BATCH_SIZE):
                batch = rows[i : i + BATCH_SIZE]
                texts = [row["comment"] for row in batch]

                embeddings = ollama_embed(texts)

                cur.executemany(
                    """
                    UPDATE comments
                    SET embedding = %s
                    WHERE comment_id = %s
                    """,
                    [
                        (embedding, row["comment_id"])
                        for row, embedding in zip(
                            batch, embeddings, strict=True
                        )
                    ],
                )
                print(f"Embedded {min(i + BATCH_SIZE, rows_len)}/{rows_len}")

        print("Done!")


def usage() -> None:
    print("Usage:")
    print("  uv run python scripts/embed.py generate     Embed all comments")
    print(
        "  uv run python scripts/embed.py get <TEXT>   Get a single embedding"
    )


if __name__ == "__main__":
    if len(argv) < 2:
        usage()
        sys.exit(1)

    mode = argv[1]
    if mode == "generate":
        generate_comments_embeddings()
    elif mode == "get":
        text = " ".join(argv[2:]).strip()

        if not text:
            usage()
            sys.exit(1)

        get_embeddings(text)
    else:
        usage()
        sys.exit(1)
