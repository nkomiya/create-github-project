from typing import List, Tuple, Union

import questionary

from .base import BaseParameter


class Select(BaseParameter):
    """選択肢形式のパラメータ。

    Args:
        value (Union[str, None]): 初期値
        title (str): 質問文
        choices (List[str]): 選択肢
    """

    def __init__(self, value: str, title: str, choices: List[str]) -> None:
        super().__init__(value)
        self._title = title
        self._choices = choices

    @property
    def question(self) -> questionary.Question:
        return questionary.select(self._title, choices=self._choices)

    def validate_value(self, value: str) -> Tuple[bool, Union[str, None]]:
        # 許容されない値が指定された場合
        if value not in self._choices:
            msg = f"'{value}' is not one of " + ', '.join(map(lambda x: f"'{x}'", self._choices))
            return False, msg

        return True, None

    def finalize_value(self, value: str) -> str:
        return value
