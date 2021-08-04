from typing import Dict, List
from unittest.mock import MagicMock

import pytest
from pytest_mock import MockFixture

from create_github_project.commands.init.parameters.checkbox import CheckBox
from create_github_project.commands.init.parameters.select import Select
from create_github_project.commands.init.parameters.reviewers import Reviewers
from create_github_project.commands.init.parameters import ParameterParser
from create_github_project.utils import Accounts

CHECKBOX = {
    'name': 'x',
    'type': 'checkbox',
    'config': {
        'title': 'prompt',
        'choices': ['c1', 'c2'],
        'default': []
    }
}

REVIEWERS = {
    'name': 'x',
    'type': 'reviewers',
    'config': {
        'title': 'prompt'
    }
}

SELECT = {
    'name': 'x',
    'type': 'select',
    'config': {
        'title': 'prompt',
        'choices': ['c1', 'c2']
    }
}


class TestParameterParser:

    @pytest.fixture(autouse=True)
    def q_checkbox(self, mocker: MockFixture) -> MagicMock:
        yield mocker.patch.object(CheckBox, 'question')

    @pytest.fixture(autouse=True)
    def q_reviewers(self, mocker: MockFixture) -> MagicMock:
        yield mocker.patch.object(Reviewers, 'question')

    @pytest.fixture(autouse=True)
    def q_select(self, mocker: MockFixture) -> MagicMock:
        yield mocker.patch.object(Select, 'question')

    @pytest.mark.parametrize(
        ['production', 'commit_types', 'reviewers', 'config', 'params', 'calls'],
        [
            [
                'master',
                'feat,fix',
                'user1,user2',
                {},
                {},
                [0, 0, 0]
            ],
            [
                None,
                'feat',
                'user1',
                {},
                {},
                [0, 0, 1]
            ],
            [
                'main',
                None,
                'user1',
                {},
                {},
                [1, 0, 0]
            ],
            [
                'main',
                'feat',
                None,
                {},
                {},
                [0, 1, 0]
            ],
            [
                'master',
                'feat,fix',
                'user1,user2',
                [CHECKBOX],
                {
                    'x': 'c1'
                },
                [0, 0, 0]
            ],
            [
                'master',
                'feat,fix',
                'user1,user2',
                [REVIEWERS],
                {
                    'x': 'user1,user2'
                },
                [0, 0, 0]
            ],
            [
                'master',
                'feat,fix',
                'user1,user2',
                [SELECT],
                {
                    'x': 'c1'
                },
                [0, 0, 0]
            ],
            [
                'master',
                'feat,fix',
                'user1,user2',
                [CHECKBOX],
                {},
                [1, 0, 0]
            ],
            [
                'master',
                'feat,fix',
                'user1,user2',
                [REVIEWERS],
                {},
                [0, 1, 0]
            ],
            [
                'master',
                'feat,fix',
                'user1,user2',
                [SELECT],
                {},
                [0, 0, 1]
            ]
        ]
    )
    def test_finalize(self, mocker: MockFixture,
                      q_checkbox: MagicMock, q_reviewers: MagicMock, q_select: MagicMock,
                      production: str, commit_types: str, reviewers: str,
                      config: Dict[str, str], params: Dict[str, str], calls: List[int]) -> None:

        q_checkbox.unsafe_ask.return_value = []
        q_reviewers.unsafe_ask.return_value = []
        q_select.unsafe_ask.return_value = 'value'
        mocker.patch.object(Accounts, 'list', return_value=['user1', 'user2'])
        mocker.patch.object(Accounts, 'get_account_info', return_value={})

        pp = ParameterParser(production, commit_types, reviewers, config, params)

        result, err = pp.parse()

        assert result is not None
        assert err is None

        actual_calls = list(map(lambda x: x.unsafe_ask.call_count, [q_checkbox, q_reviewers, q_select]))
        assert actual_calls == calls

    @pytest.mark.parametrize(
        ['production', 'commit_types', 'reviewers', 'config', 'params'],
        [
            [
                'ERROR',
                'feat,fix',
                'user1,user2',
                {},
                {},
            ],
            [
                'master',
                'ERROR',
                'user1',
                {},
                {},
            ],
            [
                'main',
                'feat',
                'ERROR',
                {},
                {},
            ],
            [
                'master',
                'feat,fix',
                'user1,user2',
                [CHECKBOX],
                {
                    'x': 'ERROR'
                },
            ],
            [
                'master',
                'feat,fix',
                'user1,user2',
                [REVIEWERS],
                {
                    'x': 'ERROR'
                },
            ],
            [
                'master',
                'feat,fix',
                'user1,user2',
                [SELECT],
                {
                    'x': 'ERROR'
                },
            ],
        ]
    )
    def test_validate_fail(self, mocker: MockFixture,
                           production: str, commit_types: str, reviewers: str,
                           config: Dict[str, str], params: Dict[str, str]) -> None:

        mocker.patch.object(Accounts, 'list', return_value=['user1', 'user2'])
        mocker.patch.object(Accounts, 'get_account_info', return_value={})

        pp = ParameterParser(production, commit_types, reviewers, config, params)
        result, err = pp.parse()
        assert result is None
        assert err is not None
