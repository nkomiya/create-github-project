import click

from .current import current
from .update import update


__all__ = [
    'build'
]


@click.group(help='Manage tool versions.')
def versions() -> None:
    pass


def build(cmd: click.Group) -> None:
    """親コマンドにサブコマンドを追加する。

    Args:
        cmd (click.Group): 親コマンド
    """
    versions.add_command(current)
    versions.add_command(update)

    cmd.add_command(versions)
