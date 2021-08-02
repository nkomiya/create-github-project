import click

from create_github_project.utils import Accounts


@click.command(help='Add GitHub account under managements.')
@click.argument('account_id', type=str)
@click.option('--display-name', type=str, help='Display name for this user.', required=True)
def add(account_id: str, display_name: str) -> None:
    """GitHub アカウントをツールの管理下に登録する。

    Args:
        account_id (str): GitHub アカウント ID
        display_name (str): 表示名

    Raises:
        click.BadParameter: 対象アカウントが存在しない場合
    """
    accounts = Accounts()

    # 対象アカウントが管理下にある場合は何もしない。
    if accounts.exists(account_id):
        print(f"GitHub Account '{account_id}' already under management.")
        return

    homepage = accounts.add(account_id, display_name)
    if homepage is None:
        raise click.BadParameter(f"Account '{account_id}' not exist.")

    # メッセージ
    print('\n'.join([
        'Following GitHub account added under management.\n',
        f'  - account ID   : {account_id}',
        f'  - Display name : {display_name}',
        f'  - homepage     : {homepage}'
    ]))
