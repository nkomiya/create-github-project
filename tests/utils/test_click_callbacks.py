from typing import Dict, List

import pytest

from create_github_project.utils.click_callbacks import to_multi_parameter


@pytest.mark.parametrize(
    ['cli_input', 'expected'],
    [
        [
            ['x=1', 'y=z=2'],
            {
                'x': '1',
                'y': 'z=2'
            }
        ],
    ]
)
def test_to_multi_parameter(cli_input: List[str], expected: Dict[str, str]):
    actual = to_multi_parameter(None, None, cli_input)
    assert expected == actual
