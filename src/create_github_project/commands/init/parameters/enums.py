from enum import Enum

from .checkbox import CheckBox
from .reviewers import Reviewers
from .select import Select


class ParameterType(Enum):
    """パラメータとして許容する型を管理する列挙体。
    """

    #: チェックボックス形式
    CHECKBOX = CheckBox
    #: GitHub レビュアー用 チェックボックス形式
    REVIEWERS = Reviewers
    #: 選択肢形式
    SELECT = Select

    @classmethod
    def find(cls, name: str) -> 'ParameterType':
        """name に合致する列挙子を返す。

        Returns:
            ParameterType: 列挙子

        Raises:
            NotImplementedError: 不正なパラメータ型が指定された場合
        """
        for e in cls:
            if e.name.lower() == name:
                return e

        # NOTE: 現状 template は完全に package 管理下にあるため、不正な parameter 型の検証は不要
        raise NotImplementedError(f'Parameter type `{name}` is not supported.')
