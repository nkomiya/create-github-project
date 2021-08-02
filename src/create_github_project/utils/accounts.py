import json
from operator import itemgetter
import os
from pathlib import Path
from typing import Dict, List, Union

from github import Github


class Accounts:

    #: アカウント一覧を管理するファイル
    FILE_PATH = Path(os.path.expanduser('~')).joinpath('.create-github-project/accounts.json')

    def __init__(self):
        # アカウント一覧を取得しておく。
        self._accounts = {}
        if self.initialized():
            with open(self.FILE_PATH, 'r') as f:
                self._accounts = json.load(f)

    def initialized(self) -> bool:
        """アカウントファイルが存在するかどうかを返す。

        Returns:
            bool: アカウントファイルが存在するかどうか
        """
        return self.FILE_PATH.exists()

    def exists(self, account_id: str) -> bool:
        """対象アカウントが既に管理下にあるかどうかを返す。

        Args:
            account_id (str): GitHub アカウント ID

        Returns:
            bool: 管理下にあるかどうか
        """
        return account_id in self._accounts.keys()

    def list(self) -> List[str]:
        """管理下にある GitHub アカウント ID の一覧を返す。

        Returns:
            List[str]: 管理下にある GitHub アカウント ID
        """
        return list(self._accounts.keys())

    def dump_list(self) -> None:
        """管理下にある GitHub アカウントを標準出力に表示する。
        """
        for account_id, info in sorted(self._accounts.items(), key=itemgetter(0)):
            print(f'- account_id   : {account_id}')
            print(f'  display_name : {info["display_name"]}')
            print(f'  homepage     : {info["homepage"]}')

    def add(self, account_id: str, display_name: str) -> Union[str, None]:
        """GitHub アカウントをツール管理下に登録する。

        Args:
            account_id (str): GitHub アカウント ID
            display_name (str): 表示名

        Returns:
            Union[str, None]: 対象アカウントの URL, アカウント取得に失敗した場合 None
        """
        # 既に登録されている場合
        if account_id in self._accounts.keys():
            return None

        # アカウント存在確認
        try:
            user = Github().get_user(account_id)
        except Exception:
            return None

        # 情報更新
        self._accounts.update({
            account_id: dict(
                display_name=display_name,
                homepage=user.html_url
            )
        })
        self._update_file()

        return user.html_url

    def drop(self, account_id: str) -> None:
        """GitHub アカウントを管理から外す。

        Args:
            account_id (str): GitHub アカウント ID
        """
        if account_id not in self._accounts.keys():
            raise ValueError(f"Account '{account_id}' is not under management.")

        # 情報更新
        _ = self._accounts.pop(account_id)
        self._update_file()

    def get_account_info(self, account_id: str) -> Dict[str, str]:
        """GitHub アカウント情報を返す。

        Args:
            account_id (str): GitHub アカウント ID

        Returns:
            Dict[str, str]: アカウント情報
        """
        return self._accounts[account_id]

    def _update_file(self):
        """アカウント一覧のファイルを更新する。
        """
        os.makedirs(self.FILE_PATH.parent, exist_ok=True)
        with open(self.FILE_PATH, 'w') as f:
            json.dump(self._accounts, f, indent=4)
