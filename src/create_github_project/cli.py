from pathlib import Path

import click
import questionary

from create_github_project.resource_manager import ResourceManager

PRODUCTION_BRANCHES = ['master', 'main']


@click.group()
def cmd() -> None:
    """CLI のエントリーポイント。
    """
    pass


@cmd.command(help="Initialize local Git repository.")
@click.argument('repo_dir', type=click.Path(exists=False, path_type=Path))
@click.option('--repo-name', type=str, default='',
              help='GitHub repository name. Default is directory name of `repo_dir`.')
@click.option('--production', type=click.Choice(PRODUCTION_BRANCHES), help='Production branch name.')
def init(repo_dir: Path, repo_name: str, production: str) -> None:
    """ローカルリポジトリを初期化するコマンド。

    Args:
        repo_dir (Path): リポジトリ作成先
        repo_name (str): リポジトリ名
        production (str): 本番用ブランチの名前
    """
    # リポジトリ作成先にフォルダ/ファイルが存在しないこと
    if repo_dir.exists():
        raise click.BadParameter(f'Directory {repo_dir.as_posix()} already exists.')

    # リポジトリ名が未指定の場合は、リポジトリ作成先から推定する。
    repo_name = repo_name or repo_dir.name

    # ブランチ名が未入力の場合
    production = production or questionary.select('Production branch name?', choices=['master', 'main']).ask()

    rm = ResourceManager(repo_dir, repo_name, production)
    rm.initialize()
