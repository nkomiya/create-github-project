import click

from ._list import _list
from .add import add
from .drop import drop

__all__ = [
    'build'
]


@click.group(help='Manage GitHub account to set reviewers.')
def accounts() -> None:
    pass


def build(cmd: click.Group) -> None:
    """親コマンドにサブコマンドを追加する。

    Args:
        cmd (click.Group): 親コマンド
    """
    accounts.add_command(_list)
    accounts.add_command(add)
    accounts.add_command(drop)

    cmd.add_command(accounts)
