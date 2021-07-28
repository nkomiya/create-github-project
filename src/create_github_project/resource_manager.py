import json
import os
from pathlib import Path
from typing import Dict, List

import git
from jinja2 import Environment, FileSystemLoader


class ResourceManager:
    """Git リポジトリへのファイル配置を管理するクラス。

    Args:
        repo_dir (str): リポジトリ作成先のパス
        repo_name (str): リポジトリ名
        production (str): 本番用ブランチの名前
        commit_types (List[str]): changelog に含める commit type
        languages (List[str]): 利用するプログラミング言語
        code_review (Dict[str, Dict[str, str]]): ソースコード レビュアー
        release_review (Dict[str, Dict[str, str]]): リリース レビュアー

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
    #: テンプレート
    TEMPLATE_ROOT = Path(__file__).parent.joinpath('templates')
    TEMPLATE_LOADER = Environment(loader=FileSystemLoader(TEMPLATE_ROOT.as_posix()))
    #: versionrc のテンプレートへのパス
    VERSIONRC = '_core/release/.versionrc.json.jinja'
    #: 言語ごとの環境設定手順
    LANGUAGES = ['python', 'java']

    def __init__(self,
                 repo_dir: str,
                 repo_name: str,
                 production: str,
                 commit_types: List[str],
                 languages: List[str],
                 code_review: Dict[str, Dict[str, str]],
                 release_review: Dict[str, Dict[str, str]]) -> None:
        self._theme = 'default'
        self._repo_dir = repo_dir
        self._repo_name = repo_name
        self._production = production
        self._commit_types = commit_types
        self._languages = languages
        self._code_review = code_review
        self._release_review = release_review

    @classmethod
    def get_commit_types(cls) -> List[str]:
        """コミット型の一覧を返す。

        Returns:
            List[str]: コミット型
        """
        data = cls.TEMPLATE_LOADER.get_template(cls.VERSIONRC).render(commit_types=[])
        return [t['type'] for t in json.loads(data)['types']]

    @classmethod
    def get_supported_language(cls) -> List[str]:
        """サポート対象のプログラミング言語の一覧を返す。

        Returns:
            List[str]: 言語
        """
        return cls.LANGUAGES

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
        src_root = self.TEMPLATE_ROOT.joinpath('_core')
        self.add_to_index(repo, src_root)

        # extensions
        extensions = self._languages
        ext_root = self.TEMPLATE_ROOT.joinpath('_extension')
        for ext in extensions:
            src_root = ext_root.joinpath(ext)
            self.add_to_index(repo, src_root)

        # theme files
        src_root = self.TEMPLATE_ROOT.joinpath(self._theme)
        self.add_to_index(repo, src_root)

        # commit to production branch
        repo.index.commit(self._COMMIT_MESSAGE)
        # create develop branch
        repo.git.checkout(self.production, b=self.develop)

    def add_to_index(self, repo: git.Repo, src_root: str) -> None:
        """テンプレートファイルを index に登録する。

        本メソッドでは、src_root で指定されるディレクトリ配下に存在するファイルを、
        ディレクトリ構造を保ったまま、ローカルリポジトリに配置する。

        配置するファイルの拡張子が .jinja である場合はテンプレートの置換処理を行い、
        ファイル名が EXCLUDE で始まるファイルはリポジトリに配置しない。

        Args:
            repo (git.Repo): git repository
            src_root (str): テンプレートファイル格納元の起点
        """
        root = Path(self.repo_dir)
        targets = [key for key in src_root.glob('**/*') if not key.name.startswith('EXCLUDE')]

        for path in targets:
            if path.is_dir():
                continue
            dest = root.joinpath(path.relative_to(src_root))

            # read data with rendering if necessary
            data = None
            if path.suffix != '.jinja':
                with open(path, 'r') as f:
                    data = f.read()
            else:
                template_path = path.relative_to(self.TEMPLATE_ROOT).as_posix()
                template = self.TEMPLATE_LOADER.get_template(template_path)
                data = template.render(repo_name=self._repo_name,
                                       production_branch=self.production,
                                       commit_types=self._commit_types,
                                       languages=self._languages,
                                       code_review=self._code_review,
                                       release_review=self._release_review)
                dest = dest.parent.joinpath(dest.stem)

            # write file and add to index
            os.makedirs(dest.parent, exist_ok=True)
            with open(dest, 'w') as f:
                f.write(data)
            repo.index.add([dest.relative_to(self.repo_dir).as_posix()])
