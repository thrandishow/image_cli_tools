import typer
from pathlib import Path


def print_exception(e: Exception):
    typer.secho(e, err=True, fg="red")
    raise typer.Exit(1)


def get_output_name(output_name: None | str, path: Path):
    if output_name is None:
        output_name = f"{path.stem}_resized{path.suffix}"
    return output_name


def get_output_path(output_dir: Path | None, output_name: str) -> Path:
    if output_dir is not None:
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = Path(output_dir / output_name)

    else:
        output_path = Path(output_name)
    return output_path


def calculate_benefit(primal_size: float, end_size: float) -> float:
    return round(100 - (end_size * 100 / primal_size), 2)
