from pathlib import Path
from typing import Union

import click
import questionary

from create_github_project.resource_manager import ResourceManager

_DEFAULT_PRODUCTION_BRANCH = 'master'


@click.group()
def cmd() -> None:
    """CLI のエントリーポイント。
    """
    pass


@cmd.command(help="Initialize local Git repository.")
@click.argument('repo_dir', type=click.Path(exists=False, path_type=Path))
@click.option('--production', type=str, default=None,
              help='Production branch name.')
def init(repo_dir: Path, production: Union[str, None]) -> None:
    """ローカルリポジトリを初期化するコマンド。

    Args:
        repo_dir (str): リポジトリ作成先
        production (Union[str, None]): 本番用ブランチの名前
    """
    # リポジトリ作成先にフォルダ/ファイルが存在しないこと
    if repo_dir.exists():
        raise click.BadParameter(f'Directory {repo_dir.as_posix()} already exists.')

    # ブランチ名が未入力の場合
    if production is None:
        production = questionary.text(f'Production branch name [{_DEFAULT_PRODUCTION_BRANCH}]?').ask()
        production = production or _DEFAULT_PRODUCTION_BRANCH

    # ブランチ名のチェック
    if not ResourceManager.validate_branch(production):
        raise click.BadParameter(f"Branch name '{production}' is not allowed for production branch.")

    rm = ResourceManager(repo_dir, production)
    rm.initialize()
