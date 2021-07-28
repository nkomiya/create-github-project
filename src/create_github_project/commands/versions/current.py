import click

from create_github_project import __version__ as VERSION


@click.command(help='Desplay version.')
def current() -> None:
    """パッケージのバージョンを表示する。
    """
    print(f'create-github-project version: {VERSION}')
