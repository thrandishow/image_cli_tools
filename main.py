from functools import partial
from pathlib import Path
from typing import Optional
import typer
from PIL import Image
import utils
import multiprocessing

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
        utils.print_exception(e)


@app.command()
def resize_image(
    path: Path = typer.Argument(..., help="Path to image", exists=True),
    width: int = typer.Argument(..., help="Width of image"),
    height: int = typer.Argument(..., help="Height of image"),
    output_name: Optional[str] = typer.Option(
        None, "--name", "-n", help="Resized image name with format (png, jpg, etc...)"
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

            output_name = utils.get_output_name(output_name, path)
            output_path = utils.get_output_path(output_dir, output_name)

            resized_image.save(output_path)
            typer.echo(
                f"Resized image saved to: {typer.style(str(output_path), fg=typer.colors.GREEN)}"
            )

    except Exception as e:
        utils.print_exception(e)


@app.command()
def optimize_image(
    path: Path = typer.Argument(..., help="Path to image", exists=True),
    width: Optional[int] = typer.Option(None, "--width", help="Width of image"),
    height: Optional[int] = typer.Option(None, "--height", help="Height of image"),
    output_name: Optional[str] = typer.Option(
        None, "--name", "-n", help="Output name of image"
    ),
    output_dir: Optional[Path] = typer.Option(
        None, "--dir", "-d", help="Path to save optimized image"
    ),
):
    """Optimizes image, format of image is jpg

    Args:
        path (Path, optional): Path to image. Defaults to typer.Argument(..., help="Path to image", exists=True).
        width (Optional[int], optional): Width of image. Defaults to typer.Option(None, "--width", "-w", help="Width of image").
        height (Optional[int], optional): Height of image. Defaults to typer.Option( None, "--height", "-H", help="Height of image" ).
        output_name (Optional[str], optional): Output name of optimized image (without suffix!). Defaults to typer.Option( None, "--name", "-n", help="Output name of image" ).
        output_dir (Optional[Path], optional): Output path to optimized image. Defaults to typer.Option( None, "--dir", "-d", help="Path to save optimized image" ).
    """
    try:
        with Image.open(path) as im:
            primal_size: float = round(path.stat().st_size / 1024**2, 2)
            output_name = utils.get_output_name(output_name, path)
            output_path = utils.get_output_path(output_dir, output_name).with_suffix(
                ".jpg"
            )

            if im.mode == "P" and "transparency" in im.info:
                im = im.convert("RGBA")

            if (width or height) is not None:
                width = width if width is not None else im.width
                height = height if height is not None else im.height
                im.thumbnail((width, height), Image.Resampling.LANCZOS)

            if im.mode == "RGBA":
                im = im.convert("RGB")

            im.save(output_path, "JPEG", quality=50)

            end_size: float = round(output_path.stat().st_size / 1024**2, 2)
            size_benefit_percents = utils.calculate_benefit(primal_size, end_size)
            typer.echo(
                f"Optimized image saved to: {typer.style(str(output_path), fg="green")} {typer.style(f"{size_benefit_percents}% ⬆️",fg="magenta")}"
            )

    except Exception as e:
        utils.print_exception(e)


@app.command()
def optimize_bulk(
    folder_input_path: Path = typer.Argument(..., help="Path to folder with images"),
    width: Optional[int] = typer.Option(None, "--width"),
    height: Optional[int] = typer.Option(None, "--height"),
    quality: Optional[int] = typer.Option(85, "--quality", "-q"),
    folder_output_path: Optional[Path] = typer.Option(
        None, "--folder", "-f", help="Folder, where images will be saved"
    ),
):
    """Optimizes folder of images

    Args:
        folder_input_path (Path, optional): Folder with images. Defaults to typer.Argument(..., help="Path to folder with images").
        width (Optional[int], optional): Width of optimized images. Defaults to typer.Option(None, "--width").
        height (Optional[int], optional): Height of optimized images. Defaults to typer.Option(None, "--height").
        quality (Optional[int], optional): Quality of optimized images. Defaults to typer.Option(85, "--quality", "-q").
        folder_output_path (Optional[Path], optional): Folder where optimized images will be saved. Defaults to typer.Option( None, "--folder", "-f", help="Folder, where images will be saved" ).
    """
    extensions = ("*.jpg", "*.jpeg", "*.png", "*.webp")
    files = []
    for ext in extensions:
        files.extend(list(folder_input_path.glob(ext)))

    if not files:
        typer.secho("Files are not found", fg="yellow")
        return

    typer.echo(
        f"Found files: {typer.style(len(files),fg="green")}. Running processing on all cores..."
    )

    worker_func = partial(
        utils.process_single_image,
        width=width,
        height=height,
        output_dir=folder_output_path,
        quality=quality,
    )

    with multiprocessing.Pool() as pool:
        pool.map(worker_func, files)


if __name__ == "__main__":
    app()
