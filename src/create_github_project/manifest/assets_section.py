from typing import Dict, List

from jinja2 import Template


class AssetsSection:
    """manifest file の assets セクションを管理するクラス。

    Args:
        config (List[Dict[str, object]]): assets セクションを表す辞書
    """

    NAME = 'name'
    TO = 'to'
    IF = 'if'

    def __init__(self, config: List[Dict[str, object]]):
        self._params = {
            item[self.NAME]: {
                self.TO: item[self.TO],
                self.IF: item.get(self.IF, 'True')
            }
            for item in config
        }

    def get_assets(self, **params: Dict[str, object]) -> List[Dict[str, str]]:
        """assets セクションで指定されているリソースの一覧を返す。

        このメソッドでは、assets セクション内のキー `if` の template 置換を行い、
        置換結果が True であれば、Git リポジトリへの配置対象とみなす。

        Args:
            **param (Dict[str, object]): template 置換に利用するパラメータ

        Returns:
            List[Dict[str, str]]: リソース一覧
        """
        assets = []
        for k, v in self._params.items():
            if Template(v[self.IF]).render(**params) == 'True':
                assets.append({
                    'source': f'{k}',
                    'destination': v[self.TO]
                })

        return assets
