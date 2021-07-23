from pathlib import Path
from typing import List, Union

import click
import questionary

from create_github_project.resource_manager import ResourceManager

PRODUCTION_BRANCHES = ['master', 'main']
SUPPORTED_COMMIT_TYPES = ResourceManager.get_commit_types()
SUPPORTED_LANGUAGES = ResourceManager.get_supported_language()


@click.group()
def cmd() -> None:
    """CLI のエントリーポイント。
    """
    pass


@cmd.command(help="Initialize local Git repository.")
@click.argument('repo_dir', type=click.Path(exists=False, path_type=Path))
@click.option('--repo-name', type=str, default='',
              help='GitHub repository name. Default is directory name of `repo_dir`.')
@click.option('--production', type=click.Choice(PRODUCTION_BRANCHES), help='Production branch name.')
@click.option('--commit-types', type=str, help='Comma separated commit types to be included in CHANGELOG.md.')
@click.option('--lang', type=str, help='Comma separated programming languages to be used in repository.')
def init(repo_dir: Path, repo_name: str, production: str, lang: str, commit_types: str) -> None:
    """ローカルリポジトリを初期化するコマンド。

    Args:
        repo_dir (Path): リポジトリ作成先
        repo_name (str): リポジトリ名
        production (str): 本番用ブランチの名前
        lang (str): カンマ区切りのプログラミング言語
        commit_types (str): カンマ区切りの commit type
    """
    # リポジトリ作成先にフォルダ/ファイルが存在しないこと
    if repo_dir.exists():
        raise click.BadParameter(f'Directory {repo_dir.as_posix()} already exists.')

    # commit type
    types = to_choices('commit type', commit_types, SUPPORTED_COMMIT_TYPES)
    # 言語
    languages = to_choices('language', lang, SUPPORTED_LANGUAGES)
    # リポジトリ名が未指定の場合は、リポジトリ作成先から推定する。
    repo_name = repo_name or repo_dir.name

    # 本番用ブランチ
    production = production or questionary.select('Production branch name?', choices=['master', 'main']).ask()
    # commit type
    if types is None:
        choices = [
            questionary.Choice(type_, checked=type_ in ['feat', 'fix', 'docs', 'perf'])
            for type_ in SUPPORTED_COMMIT_TYPES
        ]
        types = questionary.checkbox('Commit types to be included CHANGELOG?', choices=choices).ask()
    # 言語
    if languages is None:
        languages = questionary.checkbox('Programming languages to be used?', choices=SUPPORTED_LANGUAGES).ask()

    # リポジトリ初期化
    rm = ResourceManager(repo_dir, repo_name, production, types, languages)
    rm.initialize()


def to_choices(name: str, choices_str: Union[str, None], allowed: List[str]) -> Union[List[str], None]:
    """カンマ区切りのリストをパースする。

    Args:
        name (str): 項目名
        choices_str (Union[str, None]): カンマ区切りのリスト
        allowed (List[str]): 許容される値

    Raises:
        click.BadParameter: 許容されない値が指定された場合

    Returns:
        Union[List[str], None]: パース結果
    """
    if choices_str is None:
        return None

    choices = list(set(choices_str.split(',')))
    unsupported = set(choices) - set(allowed)
    if unsupported:
        raise click.BadParameter(f'Unsupported {name} designated: {",".join(unsupported)}')
    return choices
