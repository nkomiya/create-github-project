import os
from pathlib import Path
import shutil
import subprocess

import git
from jinja2 import Template


class ResourceManager:
    """Git リポジトリへのファイル配置を管理するクラス。

    Args:
        repo_dir (str): リポジトリ作成先のパス
        repo_name (str): リポジトリ名
        production (str): 本番用ブランチの名前

    Attributes:
        repo_dir (str): ローカルリポジトリのパス
        production (str): 本番用ブランチの名前
        develop (str): 開発用ブランチの名前
    """

    #: 開発用ブランチの名前
    _DEVELOP = 'develop'
    #: リポジトリ初期化時のコミットメッセージ
    _COMMIT_MESSAGE = 'chore: initialize repository'
    #: リポジトリに格納するテンプレートファイルの格納先
    RESOURCES = Path(__file__).parent.joinpath('resources')

    def __init__(self, repo_dir: str, repo_name: str, production: str) -> None:
        self._repo_dir = repo_dir
        self._repo_name = repo_name
        self._production = production

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
                                             production_branch=self.production)
                dest = dest.parent.joinpath(dest.stem)

            # write file and add to index
            os.makedirs(dest.parent, exist_ok=True)
            with open(dest, 'w') as f:
                f.write(data)
            repo.index.add([dest.relative_to(self.repo_dir).as_posix()])

            # save path to package.json
            if dest.name == 'package.json':
                package_json = dest

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
