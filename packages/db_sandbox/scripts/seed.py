from pathlib import Path

from db_sandbox.database import get_pg_pool

from packages.db_sandbox.scripts.embed import generate_comments_embeddings


def seed() -> None:
    with get_pg_pool().connection() as conn:
        sample_data = Path("samples/sample-pg.sql").read_bytes()

        conn.execute(sample_data)
        conn.commit()

        print("Loaded sample data.")

        generate_comments_embeddings()

        print("Generated embeddings.")


if __name__ == "__main__":
    seed()
