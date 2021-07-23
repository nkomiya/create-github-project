from pathlib import Path

import click

from create_github_project.resource_manager import ResourceManager


@click.group()
def cmd() -> None:
    """CLI のエントリーポイント。
    """
    pass


@cmd.command(help="ローカルリポジトリを初期化する。")
@click.argument('repo_dir', type=click.Path(exists=False, path_type=Path))
@click.option('--production', type=str, default='master',
              help='Production branch name.')
def init(repo_dir: Path, production: str) -> None:
    """ローカルリポジトリを初期化用のコマンド。

    Args:
        repo_dir (str): リポジトリ作成先
        production (str): 本番用ブランチの名前
    """
    if repo_dir.exists():
        raise click.BadParameter(f'Directory {repo_dir.as_posix()} already exists.')
    rm = ResourceManager(repo_dir, production)
    rm.initialize()
