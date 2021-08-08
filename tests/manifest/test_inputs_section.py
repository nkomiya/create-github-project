from typing import Dict, List

import pytest

from create_github_project.manifest.inputs_section import InputsSection


class TestInputsSection:

    @pytest.mark.parametrize(
        ['config', 'expect'],
        [
            # case1
            [
                [
                    {'name': 'param1', 'type': 'select'},
                ],
                ['param1']
            ],
            # case2
            [
                [
                    {'name': 'param1', 'type': 'select'},
                    {'name': 'param2', 'type': 'checkbox'},
                    {'name': 'param3', 'type': 'reviewers'},
                ],
                ['param1', 'param2', 'param3']
            ],
            # case3
            [
                [
                    {'name': 'param1', 'type': 'select', 'additional_param': 'test'},
                ],
                ['param1']
            ],
        ]
    )
    def test_names(self, config: List[Dict[str, str]], expect: List[str]) -> None:
        inputs = InputsSection(config)
        assert set(inputs.names) == set(expect)

    @pytest.mark.parametrize(
        ['config', 'key', 'expect_type', 'expect_config'],
        [
            # case1
            [
                [
                    {'name': 'param1', 'type': 'select', 'additional_param': 'p1'},
                ],
                'param1', 'select', {'additional_param': 'p1'}
            ],
            # case2
            [
                [
                    {'name': 'param1', 'type': 'select', 'additional_param': 'p1'},
                    {'name': 'param2', 'type': 'checkbox', 'additional_param': 'p2'},
                    {'name': 'param3', 'type': 'reviewers', 'additional_param': 'p3'},
                ],
                'param2', 'checkbox', {'additional_param': 'p2'}
            ],
            # case3
            [
                [
                    {
                        'name': 'param1', 'type': 'select',
                        'additional_param1': 'p1',
                        'additional_param2': 'p2'
                    },
                ],
                'param1', 'select', {
                    'additional_param1': 'p1',
                    'additional_param2': 'p2'
                }
            ],
        ]
    )
    def test_getters_ok(self, config: List[Dict[str, str]], key: str,
                        expect_type: str, expect_config: Dict[str, object]) -> None:
        inputs = InputsSection(config)
        assert inputs.get_type(key) == expect_type
        assert inputs.get_config(key) == expect_config

    @pytest.mark.parametrize(
        ['config', 'key'],
        [
            # case1
            [
                [
                    {'name': 'param1', 'type': 'select', 'additional_param': 'p1'},
                ],
                'param2'
            ],
            # case2
            [
                [
                    {'name': 'param1', 'type': 'select', 'additional_param': 'p1'},
                ],
                'Param1'
            ],
        ]
    )
    def test_getters_fail(self, config: List[Dict[str, str]], key: str) -> None:
        inputs = InputsSection(config)

        with pytest.raises(ValueError):
            inputs.get_type(key)

        with pytest.raises(ValueError):
            inputs.get_config(key)
