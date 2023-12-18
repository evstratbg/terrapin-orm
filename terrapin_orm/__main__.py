import typer

app = typer.Typer(
    name="terrapin",
    add_completion=False,
)


@app.command()
def make_migrations():
    ...


@app.callback()
def main():
    ...


if __name__ == "__main__":
    app()
