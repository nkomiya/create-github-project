import json
from pathlib import Path
from typing import List

from click.testing import CliRunner, Result
from github import Github
import pytest
from pytest_mock.plugin import MockerFixture

from create_github_project import __version__ as VERSION
from create_github_project.__main__ import cli
from create_github_project.commands import build


class TestVersions:

    @staticmethod
    def run(cmd: str) -> Result:
        build(cli)
        runner = CliRunner()
        return runner.invoke(cli, ['versions', cmd])

    @property
    def version(self) -> str:
        with open(Path(__file__).parent.joinpath('../../release/package.json'), 'r') as f:
            return json.load(f)['version']

    def test_current(self) -> None:
        result = self.run('current')
        assert result.exit_code == 0
        assert self.version in result.output

    @pytest.mark.parametrize(
        ['diff', 'update'],
        [
            # latest
            [[0, 0, 0], False],
            # patch
            [[0, 0, 1], True],
            # minor
            [[0, 1, 0], True],
            # major
            [[1, 0, 0], True],
            # mix
            [[1, 1, 1], True],
        ])
    def test_update(self, mocker: MockerFixture, diff: List[int], update: bool) -> None:
        version = '.'.join(
            (
                f"{x+y}" for x, y in zip(map(int, VERSION.split('.')), diff)
            )
        )

        # github
        latest = mocker.Mock()
        latest.tag_name = f'v{version}'
        repo = mocker.Mock()
        repo.get_releases.return_value = [latest]
        mocker.patch.object(Github, 'get_repo', return_value=repo)
        # pip
        pip = mocker.patch('pip.main')

        # execute
        result = self.run('update')

        # assert
        assert result.exit_code == 0
        assert pip.call_count == int(update)
