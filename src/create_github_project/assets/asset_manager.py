import os
from pathlib import Path
from typing import Dict, List

import git
from jinja2 import Environment, FileSystemLoader

from .asset import Asset


class AssetManager:
    """Git リポジトリへのリソース配置を管理するクラス。

    Args:
        repo_dir (Path): リポジトリ作成先のパス
        repo_name (str): リポジトリ名
        production (str): 本番用ブランチの名前
        commit_types (List[str]): changelog に含める commit type
        reviewers (Dict[str, Dict[str, str]]): リリース時のレビュアー
        parameters (Dict[str, object]): その他 template 用パラメータ
    """

    #: 開発用ブランチ
    DEVELOP = 'develop'
    #: リポジトリ初期化時のコミットメッセージ
    COMMIT_MESSAGE = 'chore: initialize repository'

    def __init__(self,
                 repo_dir: Path,
                 repo_name: str,
                 production: str,
                 commit_types: List[str],
                 reviewers: Dict[str, Dict[str, str]],
                 parameters: Dict[str, object]) -> None:
        # リポジトリ情報
        self._repo_dir = repo_dir
        self._production = production
        # テンプレートのパラメータ
        self._template_parameter = {
            'repo_name': repo_name,
            'production_branch': production,
            'commit_types': commit_types,
            'reviewers': reviewers,
            'inputs': parameters
        }

    def initialize(self, assets: List[Asset]) -> None:
        """Git リポジトリを初期化する。

        Args:
            assets (List[Asset]): 配置対象のリソース
        """
        # checkout
        repo = git.Repo.init(self._repo_dir)
        repo.git.checkout(b=self._production)

        for a in assets:
            src_root = a.source
            dest = Path(self._repo_dir.as_posix() + '/' + a.destination)

            self.deploy_files(repo, src_root, dest)

        # commit to production branch
        repo.index.commit(self.COMMIT_MESSAGE)
        # create develop branch
        repo.git.checkout(self._production, b=self.DEVELOP)

    def deploy_files(self, repo: git.Repo, src_root: Path, dest: Path):
        """Git リポジトリにファイルを配置し index に登録する。

        このメソッドでは、src_root 以下のファイルを再帰的に探索し、Git リポジトリに配置していく。
        なお、ファイル名に応じて、下記の処理を行う。

        1. 拡張子が .jinja である場合       : テンプレートの置換処理
        1. ファイル名が EXCLUDE で始まる場合 : リポジトリへの配置を skip

        Args:
            repo (git.Repo): git repository
            src_root (Path):
            dest (Path): ファイル配置先
        """
        env = Environment(loader=FileSystemLoader(src_root.as_posix()))

        for src in src_root.glob('**/*'):
            if src.is_dir():
                continue
            if src.name.startswith('EXCLUDE'):
                continue

            # output file path
            output = dest.joinpath(src.relative_to(src_root))

            # read data with rendering if necessary
            data = None
            if src.suffix != '.jinja':
                with open(src, 'r') as f:
                    data = f.read()
            else:
                template_path = src.relative_to(src_root).as_posix()
                template = env.get_template(template_path)
                data = template.render(**self._template_parameter)
                # drop extension .jinja
                output = output.parent.joinpath(output.stem)

            # write file and add to index
            os.makedirs(output.parent, exist_ok=True)
            with open(output, 'w') as f:
                f.write(data.rstrip() + '\n')

            # add to index
            repo.index.add([output.relative_to(self._repo_dir).as_posix()])
