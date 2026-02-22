import os

import pytest

from lab import enable_logging

TEST_DIR = os.path.dirname(__file__)
TMP_DIR = os.path.join(TEST_DIR, "tmp")
FILE_DIR = os.path.join(TEST_DIR, "files")


def pytest_sessionstart(session):
    r"""Called after the Session object has been created and
    before performing collection and entering the run test loop.
    """
    os.makedirs(TMP_DIR, exist_ok=True)


@pytest.fixture
def test_dir():
    return os.path.abspath(TEST_DIR)


@pytest.fixture
def tmp_dir():
    return os.path.abspath(TMP_DIR)


@pytest.fixture
def file_dir():
    return os.path.abspath(FILE_DIR)


@pytest.fixture(scope="session", autouse=True)
def turn_on_logging():
    enable_logging(10)
