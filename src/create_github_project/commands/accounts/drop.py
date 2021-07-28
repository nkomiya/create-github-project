import click

from create_github_project.accounts import Accounts


@click.command(help='Drop GitHub account under managements.')
@click.argument('account_id', type=str)
def drop(account_id: str) -> None:
    """ツール管理下にある GitHub アカウントを管理から外す。

    Args:
        account_id (str): GitHub アカウント ID
    """
    accounts = Accounts()
    if not accounts.exists(account_id):
        raise click.BadParameter(f"Account '{account_id}' is not under management.")
    accounts.drop(account_id)
