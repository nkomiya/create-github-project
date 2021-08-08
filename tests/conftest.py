import sys
from unittest.mock import MagicMock

from github import Github
import pytest
from pytest_mock import MockFixture

sys.path.insert(0, '../src')


@pytest.fixture(autouse=True)
def github_get_user(mocker: MockFixture) -> MagicMock:
    m = mocker.patch.object(Github, 'get_user')
    yield m
