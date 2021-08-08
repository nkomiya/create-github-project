from typing import Dict, List


class InputsSection:
    """manifest file の inputs セクションを管理するクラス。

    inputs セクションでは、下記形式の yaml を想定する。

    .. code-block: yaml

        assets:
        - name: "<パラメータの名前>"
          type: "<パラメータの型>"
          # その他 type 固有のパラメータ
          param1: ...
          param2: ...

    Args:
        config (List[Dict[str, object]]): inputs セクションを表す辞書
    """

    NAME = 'name'
    TYPE = 'type'

    def __init__(self, config: List[Dict[str, object]]) -> None:
        self._config = config

    @property
    def names(self) -> List[str]:
        """List[str]: inputs 内 パラメータ名の一覧"""
        return [item[self.NAME] for item in self._config]

    def get_type(self, name: str) -> str:
        """パラメータの型を返す。

        Args:
            name (str): パラメータ名

        Returns:
            str: 型

        Raises:
            ValueError: パラメータ名が不正の場合
        """
        for item in self._config:
            if item[self.NAME] == name:
                return item[self.TYPE]
        raise ValueError(f'Unexpected name: {name}')

    def get_config(self, name: str) -> Dict[str, object]:
        """パラメータの構成を返す。

        Args:
            name (str): パラメータ名

        Returns:
            Dict[str, object]: パラメータの構成

        Raises:
            ValueError: パラメータ名が不正の場合
        """
        exclude = [self.NAME, self.TYPE]

        for item in self._config:
            if item[self.NAME] == name:
                return {k: v for k, v in item.items() if k not in exclude}
        raise ValueError(f'Unexpected name: {name}')
