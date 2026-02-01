import os
from pathlib import Path
from typing import Optional
import typer
from PIL import Image

app = typer.Typer(add_completion=False)


@app.command()
def info(path: Path = typer.Argument(..., help="Path to image", exists=True)):
    """Shows information about the image

    Args:
        path (Path, required): Path to image. Defaults to typer.Argument(..., help="Path to image", exists=True).

    Raises:
        typer.Exit:  Exit the program
    """
    try:
        with Image.open(path) as im:
            width, height = im.size
            typer.echo(f"Image name: {typer.style(im.filename, fg="green")}")
            typer.echo(f"Image format: {typer.style(im.format, fg="green")}")
            typer.echo(f"Image size: {typer.style(f"{width}x{height}", fg="green")}")

    except Exception as e:
        typer.secho(e, err=True, fg="red")
        raise typer.Exit(1)


@app.command()
def resize_image(
    path: Path = typer.Argument(..., help="Path to image", exists=True),
    width: int = typer.Argument(..., help="Width of image"),
    height: int = typer.Argument(..., help="Height of image"),
    output_name: Optional[str] = typer.Option(
        None, "--name", "-n", help="Resized image name"
    ),
    output_dir: Optional[Path] = typer.Option(
        None, "--dir", "-d", help="Path to save resized image"
    ),
):
    """Resizes image

    Args:
        path (Path, required): Path to image. Defaults to typer.Argument(..., help="Path to image", exists=True).
        width (int, required): Width of image. Defaults to typer.Argument(..., help="Width of image").
        height (int, required): Height of image. Defaults to typer.Argument(..., help="Height of image").
        output_name (Optional[str], optional): Output name of resized image. Defaults to typer.Option( None, "--name", "-n", help="Resized image name" ).
        output_dir (Optional[Path], optional): Output dir of resized image. Defaults to typer.Option( None, "--dir", "-d", help="Path to save resized image" ).

    Raises:
        typer.Exit: Exit the program
    """

    try:
        with Image.open(path) as im:
            size = (width, height)
            resized_image = im.resize(size)

            if output_name is None:
                output_name = f"{path.stem}_resized{path.suffix}"

            if output_dir:
                output_dir.mkdir(parents=True, exist_ok=True)
                output_path = output_dir / output_name

            else:
                output_path = Path(output_name)

            resized_image.save(output_path)
            typer.echo(
                f"Resized image saved to: {typer.style(str(output_path), fg=typer.colors.GREEN)}"
            )

    except Exception as e:
        typer.secho(e, err=True, fg="red")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
