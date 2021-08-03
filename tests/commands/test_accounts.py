from typing import List

from click.testing import CliRunner, Result
import pytest
from pytest_mock.plugin import MockerFixture

from create_github_project.__main__ import cli
from create_github_project.commands import build
from create_github_project.utils import Accounts


class TestAccounts:

    @staticmethod
    def run(cmd: str, args: List[str]) -> Result:
        build(cli)
        runner = CliRunner()
        return runner.invoke(cli, ['accounts', cmd] + args)

    def test_list(self, mocker: MockerFixture) -> None:
        dump_list = mocker.patch.object(Accounts, 'dump_list')
        result = self.run('list', [])
        assert result.exit_code == 0
        dump_list.assert_called_once_with()

    @pytest.mark.parametrize(
        ['mock_results', 'ok', 'add_calls'],
        [
            # add account finished successfully
            [[False, 'https://...'], True, True],
            # try add account, but account not exist on GitHub
            [[False, None], False, True],
            # account already under control
            [[True, None], True, False],
        ]
    )
    def test_add(self, mocker: MockerFixture, mock_results: List[object], ok: bool, add_calls: bool) -> None:
        _ = mocker.patch.object(Accounts, 'exists', return_value=mock_results[0])
        add = mocker.patch.object(Accounts, 'add', return_value=mock_results[1])

        # execute
        result = self.run('add', ['dummy', '--display-name', 'dummy name'])

        # examine
        if ok:
            assert result.exit_code == 0
        else:
            assert result.exit_code != 0

        if add_calls:
            add.assert_called_once_with('dummy', 'dummy name')
        else:
            add.assert_not_called()

    @pytest.mark.parametrize(
        ['exists', 'ok', 'drop_calls'],
        [
            # drop account successfully
            [True, True, True],
            # account not under control
            [False, False, False],
        ]
    )
    def test_drop(self, mocker: MockerFixture, exists: bool, ok: bool, drop_calls: bool) -> None:
        _ = mocker.patch.object(Accounts, 'exists', return_value=exists)
        drop = mocker.patch.object(Accounts, 'drop')

        # execute
        result = self.run('drop', ['dummy'])

        # examine
        if ok:
            assert result.exit_code == 0
        else:
            assert result.exit_code != 0

        if drop_calls:
            drop.assert_called_once_with('dummy')
        else:
            drop.assert_not_called()
