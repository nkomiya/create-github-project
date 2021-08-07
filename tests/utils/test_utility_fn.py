from typing import Union

import pytest
from pytest_mock import MockFixture
from questionary import Question

from create_github_project.utils import get_commit_types, get_languages, to_remote_urls


def test_get_commit_types() -> None:
    assert set(get_commit_types()) == {
        'feat',
        'fix',
        'perf',
        'docs',
        'test',
        'refactor',
        'style',
        'chore',
    }


def test_get_languages() -> None:
    assert set(get_languages()) == {
        'java',
        'python'
    }


class TestToRemoteUrl:

    DEFAULT_REPO_NAME = 'owner/repo-name'

    @pytest.mark.parametrize(
        ['type_', 'name', 'repo_asked', 'repo_url', 'commit_url_format', 'compare_url_format'],
        [
            # github
            [
                'github', 'owner/repo-name', False,
                'https://github.com/owner/repo-name',
                'https://github.com/owner/repo-name/commit/{{hash}}',
                'https://github.com/owner/repo-name/compare/{{previousTag}}...{{currentTag}}',
            ],
            [
                'github', None, False,
                'https://github.com/${GITHUB_REPOSITORY}',
                'https://github.com/${GITHUB_REPOSITORY}/commit/{{hash}}',
                'https://github.com/${GITHUB_REPOSITORY}/compare/{{previousTag}}...{{currentTag}}',
            ],
            # gsr
            [
                'gsr', 'project-id/repo-name', False,
                'https://source.cloud.google.com/project-id/repo-name',
                'https://source.cloud.google.com/project-id/repo-name/+/{{hash}}',
                'https://source.cloud.google.com/project-id/repo-name/+/refs/tags/{{currentTag}}...refs/tags/{{previousTag}}',
            ],
            [
                'gsr', None, True,
                f'https://source.cloud.google.com/{DEFAULT_REPO_NAME}',
                (
                    f'https://source.cloud.google.com/{DEFAULT_REPO_NAME}' +
                    '/+/{{hash}}'
                ),
                (
                    f'https://source.cloud.google.com/{DEFAULT_REPO_NAME}' +
                    '/+/refs/tags/{{currentTag}}...refs/tags/{{previousTag}}'
                ),
            ],
        ]
    )
    def test_ok(self, mocker: MockFixture, type_: str, name: Union[str, None],
                repo_asked: bool, repo_url: str, commit_url_format: str, compare_url_format: str) -> None:
        q = mocker.Mock(spec=Question)
        mocker.patch('questionary.text', return_value=q)
        q.unsafe_ask.return_value = self.DEFAULT_REPO_NAME

        actual_repo_url, changelog_urls, err = to_remote_urls(type_, name)
        assert repo_url == actual_repo_url
        assert isinstance(changelog_urls, dict) and (
            commit_url_format == changelog_urls['commitUrlFormat']
            and
            compare_url_format == changelog_urls['compareUrlFormat']
        )
        assert err is None
        if repo_asked:
            q.unsafe_ask.assert_called_once()
        else:
            q.unsafe_ask.assert_not_called()

    @pytest.mark.parametrize(
        ['type_', 'name'],
        [
            # github
            [
                'github', 'ERROR',
            ],
            [
                'github', 'owner/repo-name/ERROR',
            ],
            # gsr
            [
                'gsr', 'ERROR',
            ],
            [
                'gsr', 'project/repo-name/ERROR',
            ],
        ]
    )
    def test_fail(self, mocker: MockFixture, type_: str, name: str) -> None:
        actual_repo_url, changelog_urls, err = to_remote_urls(type_, name)
        assert actual_repo_url is None
        assert changelog_urls is None
        assert err is not None

    @pytest.mark.parametrize(
        ['type_', 'name'],
        [
            [
                'UNKNOWN', None,
            ],
            [
                'UNKNOWN', 'owner/repo-name',
            ],
            [
                'UNKNOWN', 'ERROR',
            ],
        ]
    )
    def test_crush(self, type_: str, name: str) -> None:
        with pytest.raises(ValueError):
            to_remote_urls(type_, name)
