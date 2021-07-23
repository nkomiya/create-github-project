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
        # repository root directory
        root = Path(self.repo_dir)
        # checkout
        repo = git.Repo.init(self.repo_dir)
        repo.git.checkout(b=self.production)
        # package.json
        package_json = None

        # core files
        for path in self.RESOURCES.glob('core/**/*'):
            if os.path.isdir(path):
                continue
            dest = root.joinpath(path.relative_to(self.RESOURCES / 'core'))

            # read data with rendering if necessary
            with open(path, 'r') as f:
                data = f.read()
            if path.suffix == '.jinja':
                data = Template(data).render(repo_name=self._repo_name,
                                             production_branch=self.production,
                                             languages=self._languages)
                dest = dest.parent.joinpath(dest.stem)
            if path.name == '.versionrc.json':
                data = self.build_versionrc(data)

            # write file and add to index
            os.makedirs(dest.parent, exist_ok=True)
            with open(dest, 'w') as f:
                f.write(data)
            repo.index.add([dest.relative_to(self.repo_dir).as_posix()])

            # save path to package.json
            if dest.name == 'package.json':
                package_json = dest

        # language specific files
        for lang in self._languages:
            for path in map(lambda x: self.RESOURCES.joinpath('lang').joinpath(x), self.LANG[lang]):
                dest = root.joinpath(path.relative_to(self.RESOURCES / 'lang'))
                dest = dest.parent.joinpath('docs/setup').joinpath(dest.name)
                # copy
                os.makedirs(dest.parent, exist_ok=True)
                shutil.copy(path, dest)
                repo.index.add([dest.relative_to(self.repo_dir).as_posix()])

        # create yarn.lock
        pwd = os.getcwd()
        os.chdir(package_json.parent)
        subprocess.run(['yarn', 'install'])
        shutil.rmtree('node_modules')
        repo.index.add([package_json.parent.joinpath('yarn.lock').relative_to(self.repo_dir).as_posix()])
        os.chdir(pwd)

        # commit to production branch
        repo.index.commit(self._COMMIT_MESSAGE)

        # create develop branch
        repo.git.checkout(self.production, b=self.develop)

    def build_versionrc(self, template: str) -> str:
        """.versionrc.json を構築する。

        Args:
            template (str): .versionrc.json のテンプレート

        Returns:
            str: .versionrc.json の中身
        """
        data_as_json = json.loads(template)
        types = []
        for type_ in data_as_json['types']:
            tmp = type_.copy()
            if type_['type'] not in self._commit_types:
                tmp['hidden'] = True
            types.append(tmp)
        data_as_json['types'] = types
        return json.dumps(data_as_json, indent=4)
