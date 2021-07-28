from click import Group

from .init import init
from .accounts import build as build_accounts_cmd
from .versions import build as build_versions_cmd


def build(cmd: Group) -> None:
    """親のコマンドグループにサブコマンドを追加する。

    Args:
        cmd (Group): 親コマンドのグループ
    """
    cmd.add_command(init)
    # コマンドグループ
    build_accounts_cmd(cmd)
    build_versions_cmd(cmd)
