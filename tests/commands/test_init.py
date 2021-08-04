from pathlib import Path
from typing import List
from unittest.mock import MagicMock

from click.testing import CliRunner, Result
import pytest
from pytest_mock.plugin import MockerFixture

from create_github_project.__main__ import cli
from create_github_project.assets import AssetManager
from create_github_project.commands import build
from create_github_project.commands.init.parameters import ParameterParser
from create_github_project.manifest import ManifestParser


class TestInit:

    @staticmethod
    def run(args: List[str], mocker: MockerFixture, exists: bool = False) -> Result:
        _ = mocker.patch.object(Path, 'exists', return_value=exists)
        build(cli)
        runner = CliRunner()
        return runner.invoke(cli, ['init', 'repo_dir'] + args)

    @pytest.fixture(autouse=True)
    def initialize(self, mocker: MockerFixture) -> MagicMock:
        yield mocker.patch.object(AssetManager, 'initialize')

    def test_dir_exist(self, mocker: MockerFixture, initialize: MagicMock) -> None:
        result = self.run([], mocker, True)
        assert result.exit_code != 0
        initialize.assert_not_called()

    def test_invalid_remote_repo_name(self, mocker: MockerFixture, initialize: MagicMock) -> None:
        _ = mocker.patch('create_github_project.utils.utility_fn.to_remote_urls',
                         return_value=[None, None, 'error'])
        result = self.run([], mocker)
        assert result.exit_code != 0
        initialize.assert_not_called()

    @pytest.mark.parametrize(
        ['designated', 'defined'],
        [
            # unknown
            [
                ['x=1', 'y=2,3'],
                ['x']
            ],
            # case
            [
                ['X=1', 'y=2,3'],
                ['x', 'y']
            ],
        ]
    )
    def test_invalid_parameter_names(self, mocker: MockerFixture, initialize: MagicMock,
                                     designated: List[str], defined: List[str]) -> None:
        _ = mocker.patch.object(ManifestParser, 'get_parameter_names', return_value=defined)
        args = list(map(lambda x: f'--parameter={x}', designated))
        result = self.run(args, mocker)
        assert result.exit_code != 0
        initialize.assert_not_called()

    def test_invalid_parameter_values(self, mocker: MockerFixture, initialize: MagicMock) -> None:
        _ = mocker.patch.object(ParameterParser, 'parse', return_value=[None, "error"])
        result = self.run([], mocker)
        assert result.exit_code != 0
        initialize.assert_not_called()

    def test_ok(self, mocker: MockerFixture, initialize: MagicMock) -> None:
        _ = mocker.patch.object(ParameterParser, 'parse',
                                return_value=[
                                    [
                                        'master',
                                        ['feat', 'fix'],
                                        # reviewers
                                        {},
                                        # custom parameters
                                        {
                                            'languages': []
                                        }
                                    ],
                                    None
                                ])

        # execute
        result = self.run([], mocker)

        # examine
        assert result.exit_code == 0
        initialize.assert_called_once()
