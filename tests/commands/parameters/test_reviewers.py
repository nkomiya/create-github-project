from typing import Dict, List
from unittest.mock import MagicMock

import pytest
from pytest_mock import MockFixture
from questionary import Question

from create_github_project.commands.init.parameters.reviewers import Reviewers
from create_github_project.utils import Accounts


class TestReviewers:

    @pytest.fixture(autouse=True)
    def question(self, mocker: MockFixture) -> MagicMock:
        q = mocker.Mock(spec=Question)
        mocker.patch('questionary.checkbox', return_value=q)
        yield q

    @staticmethod
    def get_account_list(account: str) -> Dict[str, str]:
        return {'display_name': account, 'homepage': 'https://github.com/test'}

    @pytest.mark.parametrize(
        ['value', 'accounts', 'has_call'],
        [
            [
                '',
                ['user1', 'user2', 'user3'],
                False,
            ],
            [
                'user1',
                ['user1', 'user2', 'user3'],
                False,
            ],
            [
                'user1,user2',
                ['user1', 'user2', 'user3'],
                False,
            ],
            [
                None,
                ['user1', 'user2', 'user3'],
                True,
            ],
        ]
    )
    def test_finalize(self, mocker: MockFixture, question: MagicMock,
                      value: str, accounts: List[str], has_call: bool) -> None:

        question.unsafe_ask.return_value = [] if value is None else value.split()
        mocker.patch.object(Accounts, 'list', return_value=accounts)
        mocker.patch.object(Accounts, 'get_account_info', side_effect=self.get_account_list)

        r = Reviewers(value, "prompt")

        ok, _ = r.validate()
        assert ok

        r.finalize()
        assert question.unsafe_ask.call_count == int(has_call)

    @pytest.mark.parametrize(
        ['value', 'choices'],
        [
            [
                'val3',
                ['val1', 'val2'],
            ],
            [
                'Val1',
                ['val1', 'val2'],
            ],
        ]
    )
    def test_validate_fail(self, value: str, choices: List[str]) -> None:
        r = Reviewers(value, "prompt")
        ok, _ = r.validate()
        assert not ok
