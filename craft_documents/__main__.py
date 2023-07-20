import typer

app = typer.Typer()


# TODO: Remove
@app.command()
def main():
    print("Hello, world!")


if __name__ == "__main__":
    app()
