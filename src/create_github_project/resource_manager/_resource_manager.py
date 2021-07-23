import json
import os
from pathlib import Path
import shutil
import subprocess
from typing import List

import git
from jinja2 import Template


class ResourceManager:
    """Git リポジトリへのファイル配置を管理するクラス。

    Args:
        repo_dir (str): リポジトリ作成先のパス
        repo_name (str): リポジトリ名
        production (str): 本番用ブランチの名前
        commit_types (List[str]): changelog に含める commit type

    Attributes:
        repo_dir (str): ローカルリポジトリのパス
        production (str): 本番用ブランチの名前
        develop (str): 開発用ブランチの名前
        languages (List[str]): 利用言語
    """

    #: 開発用ブランチの名前
    _DEVELOP = 'develop'
    #: リポジトリ初期化時のコミットメッセージ
    _COMMIT_MESSAGE = 'chore: initialize repository'
    #: リポジトリに格納するテンプレートファイルの格納先
    RESOURCES = Path(__file__).parent.joinpath('resources')
    #: versionrc のテンプレートへのパス
    VERSIONRC = RESOURCES.joinpath('core/release/.versionrc.json')
    #: 常に複製するファイル郡
    CORE = {
        '*': {},
        'release/*': {},
        '.github/*': {},
        '.github/issue_template/*': {}
    }
    #: 言語ごとの環境設定手順
    LANG = {
        'python': [
            'python.md'
        ],
        'java': [
            'java.md',
            'schema.xml'
        ]
    }

    def __init__(self, repo_dir: str, repo_name: str, production: str,
                 commit_types: List[str], languages: List[str]) -> None:
        self._repo_dir = repo_dir
        self._repo_name = repo_name
        self._production = production
        self._commit_types = commit_types
        self._languages = languages

    @classmethod
    def get_commit_types(cls) -> List[str]:
        """コミット型の一覧を返す。

        Returns:
            List[str]: コミット型
        """
        with open(cls.VERSIONRC, 'r') as f:
            return [t['type'] for t in json.load(f)['types']]

    @classmethod
    def get_supported_language(cls) -> List[str]:
        """設定手順が存在する言語の一覧を返す。

        Returns:
            List[str]: 言語
        """
        return list(cls.LANG.keys())

    @property
    def repo_dir(self) -> str:
        """str: ローカルリポジトリのパス"""
        return self._repo_dir

    @property
    def production(self) -> str:
        """str: 本番用ブランチの名前"""
        return self._production

    @property
    def develop(self) -> str:
        """str: 開発用ブランチの名前"""
        return self._DEVELOP

    def initialize(self) -> None:
        """ローカルリポジトリを初期化する。
        """
        # checkout
        repo = git.Repo.init(self.repo_dir)
        repo.git.checkout(b=self.production)

        # core files
        src_root = Path(self.RESOURCES.joinpath('core'))
        for key, _ in self.CORE.items():
            targets = list(src_root.glob(key))
            self.add_to_index(repo, src_root, targets)

        # language specific files
        src_root = Path(self.RESOURCES.joinpath('lang'))
        for lang in self._languages:
            targets = map(src_root.joinpath, self.LANG[lang])
            self.add_to_index(repo, src_root, targets, 'docs/setup')

        # overwrite versionrc
        self.overwrite_versionrc(repo)
        # create yarn.lock
        self.create_yarn_lock(repo)

        # commit to production branch
        repo.index.commit(self._COMMIT_MESSAGE)
        # create develop branch
        repo.git.checkout(self.production, b=self.develop)

    def add_to_index(self, repo: git.Repo, src_root, targets, dest_prefix: str = '') -> None:
        root = Path(self.repo_dir)

        for path in targets:
            if path.is_dir():
                continue
            dest = root.joinpath(path.relative_to(src_root))
            if dest_prefix:
                dest = dest.parent.joinpath(dest_prefix).joinpath(dest.name)

            # read data with rendering if necessary
            with open(path, 'r') as f:
                data = f.read()
            if path.suffix == '.jinja':
                data = Template(data).render(repo_name=self._repo_name,
                                             production_branch=self.production,
                                             languages=self._languages)
                dest = dest.parent.joinpath(dest.stem)

            # write file and add to index
            os.makedirs(dest.parent, exist_ok=True)
            with open(dest, 'w') as f:
                f.write(data)
            repo.index.add([dest.relative_to(self.repo_dir).as_posix()])

    def overwrite_versionrc(self, repo: git.Repo) -> None:
        """.versionrc.json を書き換える。

        Args:
            repo (git.Repo): git repository
        """
        git_root = Path(repo.git_dir).parent
        for path in map(git_root.joinpath, repo.git.ls_files().split('\n')):
            if Path(path).name != '.versionrc.json':
                continue

            with open(path, 'r') as f:
                versionrc = json.load(f)

            types = []
            for type_ in versionrc['types']:
                tmp = type_.copy()
                if type_['type'] not in self._commit_types:
                    tmp['hidden'] = True
                types.append(tmp)
            versionrc['types'] = types

            with open(path, 'w') as f:
                f.write(json.dumps(versionrc, indent=4))

            # add to staging
            repo.index.add([path.relative_to(git_root).as_posix()])

    def create_yarn_lock(self, repo: git.Repo) -> None:
        """yarn.lock を作成する。

        Args:
            repo (git.Repo): git repository
        """
        git_root = Path(repo.git_dir).parent
        for path in map(git_root.joinpath, repo.git.ls_files().split('\n')):
            if Path(path).name != 'package.json':
                continue

            pwd = os.getcwd()
            os.chdir(path.parent)
            subprocess.run(['yarn', 'install'])
            shutil.rmtree('node_modules')
            repo.index.add([path.parent.joinpath('yarn.lock').relative_to(git_root).as_posix()])
            os.chdir(pwd)
