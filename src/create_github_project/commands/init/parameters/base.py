from abc import ABCMeta, abstractmethod, abstractproperty
from typing import Tuple, Union

import questionary


class BaseParameter(metaclass=ABCMeta):
    """CLI 経由で指定されたパラメータを管理する基底クラス。

    Args:
        value (Union[str, None]): パラメータの値
    """

    def __init__(self, value: Union[str, None]) -> None:
        self._raw_value = value

    @abstractproperty
    def question(self) -> questionary.Question:
        """パラメータ未指定時に利用する prompt を返す。

        Returns:
            questionary.Question: prompt
        """
        pass

    def validate(self) -> Tuple[bool, Union[str, None]]:
        """パラメータ値のバリデーションを行う。

        値が None (コマンド経由で指定されていない) 場合は、バリデーションを skip する。

        Returns:
            Tuple[bool, Union[str, None]]: バリデーション結果を表す、下記形式の辞書。

                1. バリデーション成否
                2. 不正が検知された場合、不正理由
        """
        if self._raw_value is None:
            return True, None
        return self.validate_value(self._raw_value)

    @abstractmethod
    def validate_value(self, value: str) -> Tuple[bool, Union[str, None]]:
        """パラメータ値のバリデーションを行う。

        Args:
            value (str): パラメータ値

        Returns:
            Tuple[bool, Union[str, None]]: バリデーション結果を表す、下記形式の辞書。

                1. バリデーション成否
                2. 不正が検知された場合、不正理由
        """
        pass

    def finalize(self) -> object:
        """パラメータ値を確定化する。

        Returns:
            object: パラメータ値
        """
        if self._raw_value is None:
            return self.question.unsafe_ask()
        return self.finalize_value(self._raw_value)

    @abstractmethod
    def finalize_value(self, value: str) -> object:
        """パラメータ値を整形し、確定化する。

        ここでは click 経由での入力値の整形を行い、questionary で得られる値に型を揃える。

        Args:
            value (Tuple[str, None]): パラメータ値

        Returns:
            object: パラメータ値
        """
        pass
