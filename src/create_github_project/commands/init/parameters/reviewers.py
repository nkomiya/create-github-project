from .checkbox import CheckBox
from create_github_project.utils import Accounts


class Reviewers(CheckBox):
    """GitHub レビュアー用 パラメータ。

    Args:
        value (Union[str, None]): 初期値
        title (str): prompt の質問文
    """

    def __init__(self, value: str, title: str) -> None:
        self._accounts = Accounts()
        super().__init__(value, title, self._accounts.list(), [])

    def finalize(self):
        # CheckBox クラスの finalize メソッドを override し、
        # GitHub アカウント ID に付帯情報を付与した辞書に変換する。
        arr = super().finalize()
        return {i: self._accounts.get_account_info(i) for i in arr}
