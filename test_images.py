import pathlib

import pytest

import utils


IMAGES = (
    pathlib.Path("test_data/IMAGE_1.png"),
    pathlib.Path("test_data/IMAGE_2.png"),
)


@pytest.mark.parametrize("path", IMAGES)
def test_open_preview(path):
    utils.open_preview(path)
