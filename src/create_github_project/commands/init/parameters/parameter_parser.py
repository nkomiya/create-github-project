from typing import Dict, List, Union

from .checkbox import CheckBox
from .enums import ParameterType
from .reviewers import Reviewers
from .select import Select
from create_github_project.utils import get_commit_types, get_languages

# プロダクションブランチ名 一覧
PRODUCTION_BRANCHES = ['master', 'main']
# コミット型 一覧
SUPPORTED_COMMIT_TYPES = get_commit_types()
# 言語一覧
SUPPORTED_LANGUAGES = get_languages()


class ParameterParser:
    """コマンド経由で指定されたパラメータのパースを行うクラス。

    Args:
        production (Union[str, None]): 本番用ブランチ
        commit_types (Union[str, None]): CHANGELOG に含める commit 型
        reviewers (Union[str, None]): リリース時のレビュアー
        config (List[Dict[str, object]]): テーマ固有のパラメータ構成
        params (Dict[str, object]): テーマ固有のパラメータ値
    """

    def __init__(self,
                 production: Union[str, None],
                 commit_types: Union[str, None],
                 reviewers: Union[str, None],
                 config: List[Dict[str, object]],
                 params: Dict[str, object]):
        self._production = Select(production, 'Production branch name?', PRODUCTION_BRANCHES)
        self._commit_types = CheckBox(commit_types,
                                      'Commit types to be included CHANGELOG?',
                                      SUPPORTED_COMMIT_TYPES,
                                      ['feat', 'fix', 'docs', 'perf'])
        self._reviewers = Reviewers(reviewers, 'Who should review on release?')

        # その他パラメータ
        self._names = [c['name'] for c in config]
        self._params = {}
        for ci in config:
            name = ci['name']
            type_ = ci['type']
            config = ci['config']
            p = ParameterType.find(type_)
            self._params[name] = p.value(params.get(name), **config)

    def parse(self):
        """パラメータのパースを行う。

        Returns:
            Tuple[Tuple[str, List[str], List[str], Dict[str, object], Union[str, None]]:

                パース結果を表す下記のタプル。

                    * パース後の値を格納する下記のタプル。エラーの場合は None を返す。

                        * 本番用ブランチ名
                        * CHANGELOG に含める commit 型
                        * リリース時のレビュアー
                        * テーマ固有のパラメータ

                    * エラー内容。パースに成功した場合は None。
        """
        # コマンド経由の入力値を検証
        ok, err = self._validate()
        if not ok:
            return None, err

        # 必須オプション
        production = self._production.finalize()
        commit_types = self._commit_types.finalize()
        reviewers = self._reviewers.finalize()

        # テーマ固有のオプション
        params = {}
        for k, v in self._params.items():
            params[k] = v.finalize()

        # 返却
        return (production, commit_types, reviewers, params), None

    def _validate(self):
        """コマンド経由で指定されたパラメータ値のバリデーションを行う。

        Returns:
            Tuple[bool, Union[str, None]]: バリデーション結果を表す下記のタプル。

                * バリデーションの成否
                * 不正内容。バリデーションに通過する場合は None。
        """
        ok, err = self._production.validate()
        if not ok:
            return False, f'Invalid production branch: {err}'

        ok, err = self._commit_types.validate()
        if not ok:
            return False, f'Invalid commit type(s): {err}'

        ok, err = self._reviewers.validate()
        if not ok:
            return False, f'Invalid reviewer(s): {err}'

        # テーマ固有オプションのバリデーション
        for name in self._names:
            ok, err = self._params[name].validate()
            if not ok:
                return None, f"Invalid value for parameter '{name}': {err}"

        return True, None
