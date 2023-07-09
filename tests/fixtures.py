import os
from typing import Callable

import pytest

from labeler.domain.objects import Dimension, MediaDefinition


@pytest.fixture
def current_dir(request) -> str:
    return os.path.dirname(request.module.__file__)


@pytest.fixture
def get_test_image(current_dir) -> Callable[[str], bytes]:
    def f(name):
        return open(os.path.join(current_dir, "test_images", name), "rb").read()

    return f


@pytest.fixture
def save_test_image(current_dir) -> Callable[[str, bytes], None]:
    def f(name: str, data: bytes):
        open(os.path.join(current_dir, "test_images", name), "wb").write(data)

    return f


@pytest.fixture
def create_test_media() -> Callable[[int, int, int, int, int], MediaDefinition]:
    def f(
        width: int,
        height: int,
        dpi: int = 600,
        margin_horizontal: int = 0,
        margin_vertical: int = 0,
    ):
        return MediaDefinition(
            width=Dimension(mm=width),
            length=Dimension(mm=height),
            minimal_margin_horizontal=Dimension(mm=margin_horizontal),
            minimal_margin_vertical=Dimension(mm=margin_vertical),
            dpi=dpi,
            description=f"test media {width}mm x{height}mm @ {dpi}dpi",
        )

    return f
