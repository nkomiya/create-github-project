from typing import List
from unittest.mock import MagicMock

import pytest
from pytest_mock import MockFixture
from questionary import Question

from create_github_project.commands.init.parameters.checkbox import CheckBox


class TestCheckBox:

    @pytest.fixture(autouse=True)
    def question(self, mocker: MockFixture) -> MagicMock:
        q = mocker.Mock(spec=Question)
        mocker.patch('questionary.checkbox', return_value=q)
        yield q

    @pytest.mark.parametrize(
        ['value', 'choices', 'default', 'has_call'],
        [
            [
                'val1',
                ['val1', 'val2'],
                [],
                False,
            ],
            [
                None,
                ['val1', 'val2'],
                [],
                True,
            ],
        ]
    )
    def test_finalize(self, question: MagicMock,
                      value: str, choices: List[str], default: List[str], has_call: bool) -> None:
        c = CheckBox(value, "prompt", choices, default)

        ok, _ = c.validate()
        assert ok

        c.finalize()
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
        c = CheckBox(value, "prompt", choices, [])
        ok, _ = c.validate()
        assert not ok
