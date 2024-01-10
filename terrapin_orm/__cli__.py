import asyncio

import typer

from terrapin_orm.migrations import generate_migration_script

app = typer.Typer(name="terrapin")


@app.command()
def get_migrations():
    asyncio.run(generate_migration_script())


@app.callback()
def main():
    ...


if __name__ == "__main__":
    app()
