import os
from pathlib import Path
import pip
from typing import Dict, List, Union

import click
from github import Github
import questionary

from create_github_project import __version__ as VERSION
from create_github_project.resource_manager import ResourceManager
from create_github_project.accounts import Accounts

# GitHub リポジトリに関する情報
REPOSITORY = 'nkomiya/create-github-project'


PRODUCTION_BRANCHES = ['master', 'main']
SUPPORTED_COMMIT_TYPES = ResourceManager.get_commit_types()
SUPPORTED_LANGUAGES = ResourceManager.get_supported_language()


@click.group(help='Command line tool to create templated Git project.')
def cmd() -> None:
    """CLI のエントリーポイント。
    """
    pass


@cmd.command(help="Initialize local Git repository.")
@click.argument('repo_dir', type=click.Path(exists=False, path_type=Path))
@click.option('--repo-name', type=str, default='',
              help='GitHub repository name. Default is directory name of `REPO_DIR`.')
@click.option('--production', type=click.Choice(PRODUCTION_BRANCHES), help='Production branch name.')
@click.option('--commit-types', type=str, help='Comma separated commit types to be included in CHANGELOG.md.')
@click.option('--lang', type=str, help='Comma separated programming languages to be used in repository.')
@click.option('--code-review', type=str, help='Comma separated GitHub account ID for code reviewers.')
@click.option('--release-review', type=str, help='Comma separated GitHub account ID for release reviewers.')
def init(repo_dir: Path, repo_name: str, production: str, lang: str, commit_types: str,
         code_review: str, release_review: str) -> None:
    """ローカルリポジトリを初期化するコマンド。

    Args:
        repo_dir (Path): リポジトリ作成先
        repo_name (str): リポジトリ名
        production (str): 本番用ブランチの名前
        lang (str): カンマ区切りのプログラミング言語
        commit_types (str): カンマ区切りの commit type
        code_review (str): カンマ区切り コードレビュー担当者の GitHub アカウント ID
        release_review (str): カンマ区切り リリースレビュー担当者 GitHub アカウント ID
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
    production = production or questionary.select('Production branch name?', choices=['master', 'main']).unsafe_ask()
    # commit type
    if types is None:
        choices = [
            questionary.Choice(type_, checked=type_ in ['feat', 'fix', 'docs', 'perf'])
            for type_ in SUPPORTED_COMMIT_TYPES
        ]
        types = questionary.checkbox('Commit types to be included CHANGELOG?', choices=choices).unsafe_ask()
    # 言語
    if languages is None:
        languages = questionary.checkbox('Programming languages to be used?', choices=SUPPORTED_LANGUAGES).unsafe_ask()

    # レビュアー
    code_review = parse_reviewer(code_review, 'code-review', 'Who should review code changes?')
    release_review = parse_reviewer(release_review, 'release-review', 'Who should review on release?')

    # リポジトリ初期化
    rm = ResourceManager(repo_dir, repo_name, production, types, languages, code_review, release_review)
    rm.initialize()

    # メッセージ
    print('\n'.join([
        'Repository created to the following path:\n',
        f'  {os.path.abspath(repo_dir)}\n',
        'Suggested actions:',
        '  - Initialize remote branches\n',
        '    git remote add origin <Remote repository URL>',
        '    git push origin develop',
        '    git push origin --all\n',
        '  - Activate GitHub workflows by visiting Actions tab.\n',
    ]))


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

    if choices_str == '':
        return []

    choices = list(set(choices_str.split(',')))
    unsupported = set(choices) - set(allowed)
    if unsupported:
        raise click.BadParameter(f'Unsupported {name} designated: {",".join(unsupported)}')
    return choices


def parse_reviewer(reviewers: str, key: str, question: str) -> Dict[str, Dict[str, str]]:
    """カンマ区切りで指定されたレビュアーを辞書形式に変換する。

    Args:
        reviewers (str): レビュアー
        key (str): レビュー項目
        question (str): プロンプトに表示する質問

    Returns:
        Dict[str, Dict[str, str]]: レビュアー
    """
    accounts = Accounts()
    availabe_account = accounts.list()

    account_ids = to_choices(key, reviewers, availabe_account)
    # レビュアーが未指定の場合
    if account_ids is None:
        # 選択可能なアカウントが存在する場合にのみ、prompt で確認を促す。
        account_ids = questionary.checkbox(question, choices=availabe_account).unsafe_ask() if availabe_account else []

    # 付帯情報を付与した辞書として返す
    return {aid: accounts.get_account_info(aid) for aid in account_ids}


@cmd.group(help='Manage GitHub account to set reviewers.')
def account() -> None:
    pass


@account.command(name='list', help='List GitHub account under managements.')
def _list() -> None:
    """管理下にある GitHub アカウントの一覧を出力する。
    """
    Accounts().dump_list()


@account.command(help='Add GitHub account under managements.')
@click.argument('account_id', type=str)
@click.option('--display-name', type=str, help='Display name for this user.', required=True)
def add(account_id: str, display_name: str) -> None:
    """GitHub アカウントをツールの管理下に登録する。

    Args:
        account_id (str): GitHub アカウント ID
        display_name (str): 表示名

    Raises:
        click.BadParameter: 対象アカウントが存在しない場合
    """
    accounts = Accounts()

    # 対象アカウントが管理下にある場合は何もしない。
    if accounts.exists(account_id):
        print(f"GitHub Account '{account_id}' already under management.")
        return

    homepage = accounts.add(account_id, display_name)
    if homepage is None:
        raise click.BadParameter(f"Account '{account_id}' not exist.")

    # メッセージ
    print('\n'.join([
        'Following GitHub account added under management.\n',
        f'  - account ID   : {account_id}',
        f'  - Display name : {display_name}',
        f'  - homepage     : {homepage}'
    ]))


@account.command(help='Drop GitHub account under managements.')
@click.argument('account_id', type=str)
def drop(account_id: str) -> None:
    """ツール管理下にある GitHub アカウントを管理から外す。

    Args:
        account_id (str): GitHub アカウント ID
    """
    accounts = Accounts()
    if not accounts.exists(account_id):
        raise click.BadParameter(f"Account '{account_id}' is not under management.")
    accounts.drop(account_id)


@cmd.command(help='Update version if available newer versions exist.')
def update() -> None:
    """新規リリースがある場合に package の更新を行う。
    """
    repo = Github().get_repo(REPOSITORY)
    latest = list(repo.get_releases())[0]
    if latest.tag_name.endswith(VERSION):
        print('Up to date.')
        return
    pip.main(['install', f'git+https://github.com/{REPOSITORY}@{latest.tag_name}'])


@cmd.command(help='Desplay version.')
def version() -> None:
    """パッケージのバージョンを表示する。
    """
    print(f'create-github-project version: {VERSION}')
