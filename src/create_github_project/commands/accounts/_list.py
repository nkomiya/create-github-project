import click

from create_github_project.utils import Accounts


@click.command(name='list', help='List GitHub account under managements.')
def _list() -> None:
    """管理下にある GitHub アカウントの一覧を出力する。
    """
    Accounts().dump_list()
