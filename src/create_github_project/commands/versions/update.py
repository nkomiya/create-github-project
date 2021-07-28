import pip

import click
from github import Github

from .const import REPOSITORY
from create_github_project import __version__ as VERSION


@click.command(help='Update version if available newer versions exist.')
def update() -> None:
    """新規リリースがある場合に package の更新を行う。
    """
    repo = Github().get_repo(REPOSITORY)
    latest = list(repo.get_releases())[0]
    if latest.tag_name.endswith(VERSION):
        print('Up to date.')
        return
    pip.main(['install', f'git+https://github.com/{REPOSITORY}@{latest.tag_name}'])
