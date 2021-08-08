from pathlib import Path
from py._path.local import LocalPath
from typing import Dict, List

import pytest
import yaml

from create_github_project.manifest import ManifestParser


class TestManifestParser:

    THEME_NAME = 'test'

    @pytest.fixture(autouse=True)
    def pathes(self, tmpdir: LocalPath) -> str:
        # 上書き対象
        themes = ManifestParser.THEMES
        components = ManifestParser.COMPONENTS

        # 上書き
        root = Path(tmpdir.strpath)
        ManifestParser.THEMES = root.joinpath('themes')
        ManifestParser.THEMES.mkdir(exist_ok=True)
        ManifestParser.COMPONENTS = root.joinpath('components')
        ManifestParser.COMPONENTS.mkdir(exist_ok=True)
        yield

        # 復元
        ManifestParser.THEMES = themes
        ManifestParser.COMPONENTS = components

    @classmethod
    def create_theme_file(cls,
                          inputs: List[Dict[str, object]],
                          assets,
                          follow_ups) -> None:
        theme_dir = ManifestParser.THEMES.joinpath(cls.THEME_NAME)
        theme_dir.mkdir(exist_ok=True)
        with open(theme_dir.joinpath('manifest.yaml'), 'w') as f:
            yaml.dump({
                'inputs': inputs,
                'assets': assets,
                'followUps': follow_ups
            }, f)

    @pytest.mark.parametrize(
        ['inputs', 'expect_names', 'expect_config'],
        [
            # case1
            [
                [
                    {'name': 'param1', 'type': 'select', 'opt1-1': '1', 'opt1-2': '2'},
                    {'name': 'param2', 'type': 'checkbox', 'opt2-1': '3', 'opt2-2': '4'},
                    {'name': 'param3', 'type': 'reviewers', 'opt3-1': '5', 'opt3-2': '6'},
                ],
                ['param1', 'param2', 'param3'],
                [
                    {'name': 'param1', 'type': 'select', 'config': {'opt1-1': '1', 'opt1-2': '2'}},
                    {'name': 'param2', 'type': 'checkbox', 'config': {'opt2-1': '3', 'opt2-2': '4'}},
                    {'name': 'param3', 'type': 'reviewers', 'config': {'opt3-1': '5', 'opt3-2': '6'}},
                ]
            ]
        ]
    )
    def test_inputs_section(self, inputs: List[Dict[str, str]],
                            expect_names: List[str], expect_config: List[Dict[str, object]]) -> None:
        self.create_theme_file(inputs, [], [])
        mp = ManifestParser(self.THEME_NAME)

        assert mp.get_parameter_names() == expect_names
        assert mp.get_input_config() == expect_config

    @pytest.mark.parametrize(
        ['inputs', 'assets', 'expect'],
        [
            # case1
            [
                [],
                [
                    {'name': 'asset1', 'to': '/'},
                    {'name': '@asset2', 'to': '/'}
                ],
                [
                    {'dir': 'theme', 'source': 'asset1', 'destination': '/'},
                    {'dir': 'component', 'source': 'asset2', 'destination': '/'}
                ],
            ]
        ]
    )
    def test_assets_section(self, inputs: List[Dict[str, str]], assets: List[Dict[str, str]],
                            expect: List[str]) -> None:
        self.create_theme_file(inputs, assets, [])
        mp = ManifestParser(self.THEME_NAME)

        actual = mp.get_assets('master', ['feat', 'fix'], [], inputs)
        assert len(expect) == len(actual)
        for e, a in zip(expect, actual):
            if e['dir'] == 'theme':
                formatter = ManifestParser.THEMES.joinpath(self.THEME_NAME).joinpath
            else:
                formatter = ManifestParser.COMPONENTS.joinpath
            assert formatter(e['source']) == a.source
            assert e['destination'] == a.destination

    @pytest.mark.parametrize(
        ['inputs', 'input_params', 'follow_ups', 'expect'],
        [
            # case1
            [
                [],
                {},
                [
                    {'content': 'content1'},
                    {'content': 'content2'}
                ],
                '\n'.join([
                    '  content1',
                    '',
                    '  content2'
                ])
            ],
            # case2
            [
                [
                    {'name': 'param1', 'type': 'select'},
                    {'name': 'param2', 'type': 'select'},
                ],
                {
                    'param1': 'yes',
                    'param2': 'yes'
                },
                [
                    {'content': 'content1', 'if': '{{ inputs.param1 == "yes" }}'},
                    {'content': 'content2', 'if': '{{ inputs.param2 == "yes" }}'},
                ],
                '\n'.join([
                    '  content1',
                    '',
                    '  content2'
                ])
            ],
            # case3
            [
                [
                    {'name': 'param1', 'type': 'select'},
                    {'name': 'param2', 'type': 'select'},
                ],
                {
                    'param1': 'yes',
                    'param2': 'no',
                },
                [
                    {'content': 'content1', 'if': '{{ inputs.param1 == "yes" }}'},
                    {'content': 'content2', 'if': '{{ inputs.param2 == "yes" }}'},
                ],
                '  content1'
            ],
            # case4
            [
                [
                    {'name': 'param1', 'type': 'select'},
                    {'name': 'param2', 'type': 'select'},
                ],
                {
                    'param1': 'no',
                    'param2': 'yes',
                },
                [
                    {'content': 'content1', 'if': '{{ inputs.param1 == "yes" }}'},
                    {'content': 'content2', 'if': '{{ inputs.param2 == "yes" }}'},
                ],
                '  content2'
            ],
            # case5
            [
                [
                    {'name': 'param1', 'type': 'select'},
                    {'name': 'param2', 'type': 'select'},
                ],
                {
                    'param1': 'no',
                    'param2': 'no',
                },
                [
                    {'content': 'content1', 'if': '{{ inputs.param1 == "yes" }}'},
                    {'content': 'content2', 'if': '{{ inputs.param2 == "yes" }}'},
                ],
                ''
            ],
        ]
    )
    def test_follow_ups_section(self, inputs: List[Dict[str, str]], input_params: Dict[str, object],
                                follow_ups: List[Dict[str, str]],
                                expect: str) -> None:
        self.create_theme_file(inputs, [], follow_ups)
        mp = ManifestParser(self.THEME_NAME)

        actual = mp.get_follow_up(2, 'master', ['feat', 'fix'], [], input_params)
        assert expect == actual
