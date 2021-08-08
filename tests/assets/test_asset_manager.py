from pathlib import Path
from py._path.local import LocalPath
from typing import Dict, List

import git
import pytest

from create_github_project.assets import AssetManager
from create_github_project.assets.asset import Asset
from create_github_project.manifest import ManifestParser


def to_reviewers(account_id: str) -> Dict[str, Dict[str, str]]:
    dummy_id = account_id + 'X' * 50
    return {
        dummy_id: {
            'display_name': account_id,
            'homepage': f'https://github.com/{dummy_id}'
        }
    }


class TestManifestParser:

    TEST_DATA_ROOT = Path(__file__).parent.joinpath('cases')
    PRODUCTION = 'master'
    COMMIT_TYPES = ['feat', 'fix']

    @pytest.fixture(autouse=True)
    def keep_theme_path(self) -> None:
        # 上書き対象
        themes = ManifestParser.THEMES
        yield
        # 復元
        ManifestParser.THEMES = themes

    @pytest.fixture
    def git_root(self, tmpdir: LocalPath) -> Path:
        yield Path(tmpdir.strpath)

    @pytest.mark.parametrize(
        ['case_name', 'assets', 'production', 'urls', 'reviewers', 'parameters', 'outputs'],
        [
            # case 1
            [
                'no_param',
                [
                    {'src': 'dir1', 'dest': '/'},
                    {'src': 'dir2', 'dest': '/'}
                ],
                'main',
                {}, [], {},
                ['file1.txt', 'subdir/file2.txt'],
            ],
            # case 2
            [
                'no_param',
                [
                    {'src': 'dir1', 'dest': 'subdir'},
                ],
                'master',
                {}, [], {},
                ['subdir/file1.txt'],
            ],
            # case 3
            [
                'with_param',
                [
                    {'src': 'files', 'dest': '/'},
                ],
                'main',
                {}, [], {},
                ['file1.txt', 'file2.txt'],
            ],
        ]
    )
    def test_initialize(self, git_root: Path,
                        case_name: str, assets: List[Dict[str, str]],
                        production: str,
                        urls: Dict[str, str],
                        reviewers: Dict[str, Dict[str, str]],
                        parameters: Dict[str, object],
                        outputs: List[str]) -> None:

        src = self.TEST_DATA_ROOT.joinpath(case_name)

        assets = [Asset(src.joinpath(d['src']), d['dest']) for d in assets]
        am = AssetManager(git_root, urls, case_name, production, self.COMMIT_TYPES, reviewers, parameters)

        am.initialize(assets)

        for name in outputs:
            assert git_root.joinpath(name).exists()

        repo = git.Repo(git_root)
        assert {b.name for b in repo.branches} == {production, 'develop'}
