"""Run Chronem's packaged PostgreSQL migrations."""

import argparse

from chronem.persistence.postgres.migration import upgrade_postgres_database


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Upgrade a PostgreSQL database to Chronem's migration head."
    )
    parser.add_argument(
        "--database-url",
        required=True,
        help="SQLAlchemy PostgreSQL URL, normally read from CHRONEM_DATABASE_URL",
    )
    args = parser.parse_args()
    upgrade_postgres_database(args.database_url)


if __name__ == "__main__":
    main()
