from pathlib import Path
from typing import Optional
import typer
from PIL import Image
from utils import print_exception, get_output_name, get_output_path

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
            typer.echo(f"Image mode: {typer.secho(im.mode, fg="green")}")

    except Exception as e:
        print_exception(e)


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
            resized_image = im.resize(size=(width, height))

            output_name = get_output_name(output_name, path)
            output_path = get_output_path(path, output_name)

            resized_image.save(output_path)
            typer.echo(
                f"Resized image saved to: {typer.style(str(output_path), fg=typer.colors.GREEN)}"
            )

    except Exception as e:
        print_exception(e)


@app.command()
def optimize_image(
    path: Path = typer.Argument(..., help="Path to image", exists=True),
    width: Optional[int] = typer.Option(None, "--width", "-w", help="Width of image"),
    height: Optional[int] = typer.Option(
        None, "--height", "-H", help="Height of image"
    ),
    output_name: Optional[str] = typer.Option(
        None, "--name", "-n", help="Output name of image"
    ),
    output_dir: Optional[Path] = typer.Option(
        None, "--dir", "-d", help="Path to save optimized image"
    ),
):
    try:
        with Image.open(path) as im:
            output_name = get_output_name(output_name, path)
            output_path = get_output_path(output_dir, output_name)

            if (width or height) is not None:
                width = width if width is not None else im.width
                height = height if height is not None else im.height
                im = im.resize(size=(width, height))

            im.save(output_path, optimize=True, quality=95)
    except Exception as e:
        print_exception(e)


if __name__ == "__main__":
    app()
