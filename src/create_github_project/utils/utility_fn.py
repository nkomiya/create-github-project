import json
import os
from pathlib import Path
from typing import List

from jinja2 import Template

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
