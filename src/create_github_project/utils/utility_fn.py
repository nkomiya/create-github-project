import json
import os
from pathlib import Path
from typing import Dict, List, Tuple, Union

from jinja2 import Template
import questionary

VERSIONRC = Path(__file__).parent.joinpath('../templates/components/core/release/.versionrc.json.jinja')
LANGUAGES = Path(__file__).parent.joinpath('../templates/components/languages')


def get_commit_types() -> List[str]:
    """コミット型の一覧を返す。

    Returns:
        List[str]: コミット型
    """
    with open(VERSIONRC, 'r') as f:
        data = Template(f.read()).render(commit_types=[])
    return [t['type'] for t in json.loads(data)['types']]


def get_languages() -> List[str]:
    """プログラミング言語の一覧を返す。

    Returns:
        List[str]: プログラミング言語
    """
    lang = []
    for name in os.listdir(LANGUAGES):
        if not os.path.isdir(os.path.join(LANGUAGES, name)):
            continue  # pragma: no cover
        lang.append(name)
    return lang


def to_remote_urls(type_: str, name: Union[str, None]) -> Tuple[Union[str, None],
                                                                Union[Dict[str, str], None],
                                                                Union[None, str]]:
    """リモートリポジトリの URL 郡を作成する。

    リポジトリ名が与えられていない場合、リポジトリの種別が GitHub でない場合は、
    インタラクティブにリポジトリ名の入力を促す。

    Args:
        type_ (str): リポジトリの種別 (github, または gsr)
        name (Union[str, None]): リモートリポジトリの名前

    Returns:
        Tuple[Union[str, None], Union[Dict[str, str], None], Union[None, str]]: 下記 URL 郡

            * リモートリポジトリ トップページへの URL, リポジトリ名が不正な場合は None
            * CHANGELOG に埋め込む URL, リポジトリ名が不正な場合は None
            * URL 作成時に発生したエラー, 正常時は None

    Raises:
        ValueError: リポジトリ種別が不正な場合
    """
    if type_ not in ('github', 'gsr'):
        raise ValueError(f'Unsupported repository type `{type_}`.')

    # fill branch name
    if name is None:
        if type_ == 'github':
            name = '${GITHUB_REPOSITORY}'
        elif type_ in ('gsr'):
            name = questionary.text('Remote repository name?').unsafe_ask()
        else:
            raise NotImplementedError(f'Unsupported repository type `{type_}`.')  # pragma: no cover

    # validate branch name
    if name != '${GITHUB_REPOSITORY}':
        tmp = name.split('/')
        if len(tmp) != 2:
            return None, None, f'Invalid repository name `{name}`'

    # generate links
    if type_ == 'github':
        base = f'https://github.com/{name}'
        return base, {
            'commitUrlFormat': base + '/commit/{{hash}}',
            'compareUrlFormat': base + '/compare/{{previousTag}}...{{currentTag}}'
        }, None
    elif type_ == 'gsr':
        base = f'https://source.cloud.google.com/{name}'
        return base, {
            'commitUrlFormat': base + '/+/{{hash}}',
            'compareUrlFormat': base + '/+/refs/tags/{{currentTag}}...refs/tags/{{previousTag}}'
        }, None
    else:
        raise NotImplementedError(f'Unsupported repository type `{type_}`.')  # pragma: no cover
