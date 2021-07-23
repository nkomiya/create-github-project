import os
from pathlib import Path
import shutil

import git


class ResourceManager:
    """Git リポジトリへのファイル配置を管理するクラス。

    Args:
        repo_dir (str): リポジトリ作成先のパス
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

    def __init__(self, repo_dir: str, production: str) -> None:
        self._repo_dir = repo_dir
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
        # destination
        dest = Path(self.repo_dir)
        # checkout
        repo = git.Repo.init(self.repo_dir)
        repo.git.checkout(b=self.production)

        # core files
        for path in self.RESOURCES.glob('core/**/*'):
            if os.path.isdir(path):
                continue
            dest = dest.joinpath(path.relative_to(self.RESOURCES / 'core'))
            shutil.copyfile(path, dest)
            # add to index
            repo.index.add([dest.relative_to(self.repo_dir).as_posix()])

        # commit to production branch
        repo.index.commit(self._COMMIT_MESSAGE)

        # create develop branch
        repo.git.checkout(self.production, b=self.develop)
