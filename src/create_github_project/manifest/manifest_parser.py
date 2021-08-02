from pathlib import Path
from typing import Dict, List

from jinja2 import Template
import yaml

from .inputs_section import InputsSection
from .assets_section import AssetsSection
from create_github_project.assets.asset import Asset


class ManifestParser:
    """manifest file のパーサ。

    Args:
        theme (str): テーマ名
    """

    _ROOT = Path(__file__).parent.joinpath('../templates')
    THEMES = _ROOT.joinpath('themes')
    COMPONENTS = _ROOT.joinpath('components')

    def __init__(self, theme: str):

        with open(self.THEMES.joinpath(theme).joinpath('manifest.yaml'), 'r') as f:
            manifest = yaml.safe_load(f)

        self._theme = self.THEMES.joinpath(theme)
        self._inputs = InputsSection(manifest['inputs'])
        self._assets = AssetsSection(manifest['assets'])
        self._follow_ups = manifest['followUps']

    def get_parameter_names(self) -> List[str]:
        """manifest file で定義された、インプットパラメータ名の一覧を返す。

        Returns:
            List[str]: パラメータ名の一覧
        """
        return list(self._inputs.names)

    def get_input_config(self) -> List[Dict[str, object]]:
        """manifest file で定義された、インプットパラメータの構成を返す。

        Returns:
            List[Dict[str, object]]: パラメータの構成
        """
        return [
            {
                'name': name,
                'type': self._inputs.get_type(name),
                'config': self._inputs.get_config(name)
            }
            for name in self._inputs.names
        ]

    def get_assets(self,
                   production: str,
                   commit_types: List[str],
                   reviewers: List[str],
                   inputs: Dict[str, object]) -> List[Asset]:
        """manifest file で定義から、Git リポジトリに配置するリソースの一覧を取得する。

        Args:
            production (str): 本番ブランチ
            commit_types (List[str]): CHANGELOG に含める commit 型
            reviewers (List[str]): リリースのレビュアー
            inputs (Dict[str, object]): テーマ固有 パラメータ

        Returns:
            List[Asset]: リソース一覧
        """
        # parse manifest file
        arr = self._assets.get_assets(production=production,
                                      commit_types=commit_types,
                                      reviewers=reviewers,
                                      inputs=inputs)

        # map to asset instance
        assets = []
        for a in arr:
            src_raw = a['source']
            dest = a['destination']
            if src_raw.startswith('@'):
                assets.append(Asset(self.COMPONENTS.joinpath(src_raw[1:]), dest))
            else:
                assets.append(Asset(self._theme.joinpath(src_raw), dest))

        return assets

    def get_follow_up(self,
                      indent: int,
                      production: str,
                      commit_types: List[str],
                      reviewers: List[str],
                      inputs: Dict[str, object]) -> str:
        """リポジトリ作成後に表示すべき、追加のメッセージを返す。

        Args:
            indent (int): インデント幅
            production (str): 本番ブランチ
            commit_types (List[str]): CHANGELOG に含める commit 型
            reviewers (List[str]): リリースのレビュアー
            inputs (Dict[str, object]): テーマ固有 パラメータ

        Returns:
            str: 追加のメッセージ
        """
        params = {
            "production": production,
            "commit_types": commit_types,
            "reviewers": reviewers,
            "inputs": inputs
        }

        msg = []
        for f in self._follow_ups:
            if Template(f['if']).render(**params) == 'True':
                content = '\n'.join(' ' * indent + line for line in f['content'].split('\n'))
                msg.append(content)

        return '\n'.join(msg)
