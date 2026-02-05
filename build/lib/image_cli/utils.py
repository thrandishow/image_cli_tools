import typer
from pathlib import Path
from PIL import Image


def print_exception(e: Exception) -> None:
    """Prints exception and exits the program"""
    typer.secho(e, err=True, fg="red")
    raise typer.Exit(1)


def get_output_name(output_name: None | str, path: Path) -> str:
    """Gets output name for the image"""
    if output_name is None:
        output_name = f"{path.stem}_changed{path.suffix}"
    return output_name


def get_output_path(output_dir: Path | None, output_name: str) -> Path:
    """Gets output path for the image"""
    if output_dir is not None:
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = Path(output_dir / output_name)

    else:
        output_path = Path(output_name)
    return output_path


def calculate_benefit(primal_size: float, end_size: float) -> float:
    """Calculates the benefit of the optimization"""
    if primal_size == 0:
        return 0.0
    return round(100 - (end_size * 100 / primal_size), 2)


def process_single_image(
    image_path: Path,
    width: int | None,
    height: int | None,
    output_dir: Path | None,
    quality: int | None,
) -> None:
    """Processes a single image"""
    try:
        with Image.open(image_path) as im:
            primal_size: float = round(image_path.stat().st_size / 1024**2, 2)
            if im.mode == "P" and "transparency" in im.info:
                im = im.convert("RGBA")

            if width or height:
                w = width or im.width
                h = height or im.height
                im.thumbnail((w, h), Image.Resampling.LANCZOS)

            out_name = image_path.stem + "_opt.jpg"
            out_path = get_output_path(output_dir, out_name)

            if im.mode == "RGBA":
                im = im.convert("RGB")

            im.save(out_path, "JPEG", quality=quality)
            end_size = round(out_path.stat().st_size / 1024**2, 2)
            size_benefit_percents = calculate_benefit(primal_size, end_size)

            typer.echo(
                f"{typer.style("Done",fg="green")}: {image_path.name} {typer.style(f'{size_benefit_percents}% ⬆️',fg="magenta")}"
            )

    except Exception as e:
        typer.secho(f"Error {image_path.name}: {e}", fg="red")
