from pathlib import Path
import typer
from PIL import Image

app = typer.Typer()


@app.command()
def info(path: Path = typer.Argument(..., help="Path to image", exists=True)):
    "Show image information"

    try:
        with Image.open(path) as im:
            height, width = im.size
            typer.echo(f"Image name: {typer.style(im.filename, fg="green")}")
            typer.echo(f"Image format: {typer.style(im.format, fg="green")}")
            typer.echo(f"Image size: {typer.style(f"{height}x{width}", fg="green")}")

    except Exception as e:
        typer.secho(e, err=True, fg="red")
        typer.Exit(1)


if __name__ == "__main__":
    app()
