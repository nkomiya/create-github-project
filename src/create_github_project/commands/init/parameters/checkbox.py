from typing import List, Tuple, Union

import questionary

from .base import BaseParameter


class CheckBox(BaseParameter):
    """チェックボックス形式のパラメータ。

    Args:
        value (Union[str, None]): 初期値
        title (str): prompt に利用する質問文
        choices (List[str]): 選択肢一覧
        default (List[str]): prompt でデフォルト有効にする値
    """

    def __init__(self, value: Union[str, None], title: str, choices: List[str], default: List[str]) -> None:
        super().__init__(value)
        self._title = title
        self._choices = choices
        self._default = default

    @property
    def question(self) -> questionary.Question:
        choices = [
            questionary.Choice(type_, checked=type_ in self._default) for type_ in self._choices
        ]
        return questionary.checkbox(self._title, choices=choices)

    def validate_value(self, value: str) -> Tuple[bool, Union[str, None]]:
        # 空文字指定の場合
        if value == '':
            return True, None

        # 空文字でない値が指定されている場合
        arr = list(set(value.split(',')))
        unsupported = set(arr) - set(self._choices)
        if unsupported:
            return False, 'Unsupported value designated: ' + ', '.join(map(lambda x: f"'{x}'", unsupported))

        return True, None

    def finalize_value(self, value: str):
        if value == '':
            return []
        return list(set(value.split(',')))
