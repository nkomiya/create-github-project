from typing import Dict, List

import pytest

from create_github_project.manifest.assets_section import AssetsSection


@pytest.mark.parametrize(
    ['config', 'params', 'expect'],
    [
        # case1
        [
            [
                {'name': 'asset1', 'to': '/'},
            ],
            {},
            [
                {'source': 'asset1', 'destination': '/'},
            ]
        ],
        # case2
        [
            [
                {'name': 'asset1', 'to': '/'},
                {'name': 'asset2', 'to': '/'},
            ],
            {},
            [
                {'source': 'asset1', 'destination': '/'},
                {'source': 'asset2', 'destination': '/'},
            ]
        ],
        # case3
        [
            [
                {'name': 'asset1', 'to': '/', 'if': '{{ inputs.var1 == "yes" }}'},
                {'name': 'asset2', 'to': '/', 'if': '{{ inputs.var2 == "yes" }}'},
            ],
            {
                'inputs': {
                    'var1': 'yes',
                    'var2': 'no',
                }
            },
            [
                {'source': 'asset1', 'destination': '/'},
            ]
        ],
    ]
)
def test_get_assets(config: List[Dict[str, str]], params: Dict[str, object], expect: List[Dict[str, str]]) -> None:
    assets = AssetsSection(config)
    actual = assets.get_assets(**params)
    assert len(actual) == len(expect)
    for a in actual:
        assert a in expect
