import os
from pathlib import Path
from typing import Optional
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


@app.command()
def resize_image(
    height: int,
    width: int,
    image_name: str,
    directory: Optional[Path] = None,
    path: Path = typer.Argument(..., help="Path to image", exists=True),
):
    try:
        with Image.open(path) as im:
            size = (height, width)
            resized_image = im.resize(size)

            if directory:
                resized_image.save(f"{directory}/{image_name}")
                typer.echo(
                    f"Resized image saved \nin {typer.style(directory,fg="green")} directory with {typer.style(image_name,fg="blue")} name"
                )
            else:
                resized_image.save(image_name)
                typer.echo(
                    f"Resized image saved in {typer.style("current", fg="magenta")} directory"
                )

    except Exception as e:
        typer.secho(e, err=True, fg="red")
        typer.Exit(1)


if __name__ == "__main__":
    app()
