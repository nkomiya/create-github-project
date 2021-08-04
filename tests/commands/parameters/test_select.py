from typing import List
from unittest.mock import MagicMock

import pytest
from pytest_mock import MockFixture
from questionary import Question

from create_github_project.commands.init.parameters.select import Select


class TestSelect:

    @pytest.fixture(autouse=True)
    def question(self, mocker: MockFixture) -> MagicMock:
        q = mocker.Mock(spec=Question)
        mocker.patch('questionary.select', return_value=q)
        yield q

    @pytest.mark.parametrize(
        ['value', 'choices', 'has_call'],
        [
            [
                'val1',
                ['val1', 'val2'],
                False,
            ],
            [
                None,
                ['val1', 'val2'],
                True,
            ],
        ]
    )
    def test_finalize(self, question: MagicMock,
                      value: str, choices: List[str], has_call: bool) -> None:
        s = Select(value, "prompt", choices)

        ok, _ = s.validate()
        assert ok

        s.finalize()
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
        s = Select(value, "prompt", choices)
        ok, _ = s.validate()
        assert not ok
