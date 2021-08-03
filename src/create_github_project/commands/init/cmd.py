from pathlib import Path
from typing import Tuple

import click

from .parameters import ParameterParser, PRODUCTION_BRANCHES
from create_github_project.assets import AssetManager
from create_github_project.manifest import ManifestParser
from create_github_project.utils import click_callbacks, utility_fn


@click.command(help="Initialize local Git repository.")
@click.argument('repo_dir', type=click.Path(exists=False, path_type=Path))
@click.option('--repo-name', type=str, default='',
              help='GitHub repository name. Default is directory name of `REPO_DIR`.')
@click.option('--production', type=click.Choice(PRODUCTION_BRANCHES), help='Production branch name.')
@click.option('--commit-types', type=str, help='Comma separated commit types to be included in CHANGELOG.md.')
@click.option('--reviewers', type=str, help='Comma separated GitHub account ID for release reviewers.')
@click.option('--parameter', '-p', 'parameters', type=str, multiple=True,
              callback=click_callbacks.to_multi_parameter,
              help='Theme specific parameters.')
@click.option('--remote-type', 'remote_type', type=click.Choice(['github', 'gsr']), default='github',
              help='Remote repository type. Link format in CHANGELOG is changed depending on the value.')
@click.option('--remote-repo-name', 'remote_repo_name', type=str,
              help=' '.join([
                  'Remote repository name for changelog. Format is',
                  '`REPO_OWNER`/`REPO_NAME` for GitHub, ',
                  '`PROJECT_ID`/`REPO_NAME` for GSR'
              ]))
def init(repo_dir: Path,
         repo_name: str,
         production: str,
         commit_types: str,
         reviewers: str,
         parameters: Tuple[str],
         remote_type: str,
         remote_repo_name: str) -> None:
    """ローカルリポジトリを初期化するコマンド。

    Args:
        repo_dir (Path): リポジトリ作成先
        repo_name (str): リポジトリ名
        production (str): 本番用ブランチの名前
        commit_types (str): カンマ区切りの commit type
        reviewers (str): カンマ区切り リリースレビュー担当者 GitHub アカウント ID
        parameters (Tuple[str]): テーマ固有のパラメータ
    """
    # リポジトリ作成先にフォルダ/ファイルが存在しないこと
    if repo_dir.exists():
        raise click.BadParameter(f'Directory {repo_dir.as_posix()} already exists.')
    # リポジトリ名が未指定の場合は、リポジトリ作成先から推定する。
    repo_name = repo_name or repo_dir.name

    # CHANGELOG に埋め込む URL 郡を作成する。
    ok, remote_url, urls = utility_fn.to_remote_urls(remote_type, remote_repo_name)
    if not ok:
        raise click.BadParameter(
            f'Invalid remote repository name `{remote_repo_name}`', param_hint='--remote-repo-name')

    # マニフェストファイル
    mp = ManifestParser('default')
    mp.get_input_config()
    unknown = set(parameters.keys()) - set(mp.get_parameter_names())
    if unknown:
        raise click.BadParameter('Unknown parameter detected: ' + ', '.join(map(lambda x: f"'{x}'", unknown)),
                                 param_hint="'--param'")

    # インプットパラメータ
    pp = ParameterParser(production, commit_types, reviewers, mp.get_input_config(), parameters)
    result, err = pp.parse()
    if err is not None:
        raise click.ClickException(err)
    production, commit_types, reviewers, parameters = result

    # 格納対象リソース
    assets = mp.get_assets(production, commit_types, list(reviewers.keys()), parameters)

    # リポジトリ初期化
    am = AssetManager(repo_dir, urls, repo_name, production, commit_types, reviewers, parameters)
    am.initialize(assets)

    # メッセージ
    note = '  (known after push)' if remote_url.endswith('${GITHUB_REPOSITORY}') else ''
    print('\n'.join([
        '',
        'Repository successfully configured:\n',
        f'  Local repository : {repo_dir}',
        f'  Remote repository: {remote_url}{note}\n',
        'Suggested actions:\n',
        '  - Initialize remote branches\n',
        '    git remote add origin <Remote repository URL>',
        '    git push origin develop',
        '    git push origin --all\n',
        '  - Activate GitHub workflows by visiting Actions tab.\n',
        mp.get_follow_up(2, production, commit_types, reviewers, parameters)
    ]).rstrip())
