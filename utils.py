import pathlib
import subprocess


def open_preview(path: pathlib.Path):
    """Opens given file in Preview."""
    subprocess.Popen(["open", "-a", "Preview", path])
