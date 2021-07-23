from pathlib import Path

import git

REPO_DIR = 'template'
PRODUCTION_BRANCH = 'master'
DEVELOP_BRANCH = 'develop'
COMMIT_MESSAGE = 'chore: initialize repository'


def main():
    # リポジトリ作成
    repo = git.Repo.init(REPO_DIR)
    repo.git.checkout(b=PRODUCTION_BRANCH)

    # TODO: 適切なファイルパスに変更する
    root = Path(REPO_DIR)
    readme = root.joinpath('README.md')
    readme.touch()

    # commit
    repo.index.add([readme.relative_to(REPO_DIR).as_posix()])
    repo.index.commit(COMMIT_MESSAGE)

    # develop ブランチの作成
    repo.git.checkout(PRODUCTION_BRANCH, b=DEVELOP_BRANCH)
