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
        if os.path.isdir(os.path.join(LANGUAGES, name)):
            lang.append(name)
    return lang


def to_remote_urls(type_: str, name: Union[str, None]) -> Tuple[bool, Union[str, None], Union[Dict[str, str], None]]:
    """リモートリポジトリの URL 郡を作成する。

    リポジトリ名が与えられていない場合、リポジトリの種別が GitHub でない場合は、
    インタラクティブにリポジトリ名の入力を促す。

    Args:
        type_ (str): リポジトリの種別 (github, または gsr)
        name (Union[str, None]): リモートリポジトリの名前

    Returns:
        Tuple[Union[str, None], Union[Dict[str, str], None]]: 下記 URL 郡

            * URL 作成処理の可否
            * リモートリポジトリ トップページへの URL, リポジトリ名が不正な場合は None
            * CHANGELOG に埋め込む URL, リポジトリ名が不正な場合は None

    Raises:
        ValueError: リポジトリ種別が不正な場合
    """
    if name is None:
        if type_ == 'github':
            name = '${GITHUB_REPOSITORY}'
        else:
            name = questionary.text('Remote repository name?').unsafe_ask()
    else:
        tmp = name.split('/')
        if len(tmp) != 2:
            return False, None, None

    if type_ == 'github':
        base = f'https://github.com/{name}'
        return True, base, {
            'commitUrlFormat': base + '/commit/{{hash}}',
            'compareUrlFormat': base + '/compare/{{previousTag}}...{{currentTag}}'
        }
    elif type_ == 'gsr':
        base = f'https://source.cloud.google.com/{name}'
        return True, base, {
            'commitUrlFormat': base + '/+/{{hash}}',
            'compareUrlFormat': base + '/+/refs/tags/{{previousTag}}...{{currentTag}}'
        }

    raise ValueError(f'Unsupported repository type `{type_}`.')
