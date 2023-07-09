import os
from typing import Callable

import pytest


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
