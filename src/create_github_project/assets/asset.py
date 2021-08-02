from pathlib import Path


class Asset:
    """Git リポジトリへの配置対象リソースを管理する。

    Args:
        src (Path): 元となるテンプレートを格納するディレクトリ
        destination (Path): Git のルートディレクトリから見たリソースの配置先
    """

    def __init__(self,
                 src: Path,
                 destination: str):
        self._src = src
        self._destination = destination

    @property
    def source(self) -> Path:
        """Path: テンプレート格納先"""
        return self._src

    @property
    def destination(self) -> str:
        """str: Git リポジトリへのリソース格納先"""
        return self._destination
