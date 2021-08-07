from io import StringIO
import json
from pathlib import Path
from py._path.local import LocalPath
from typing import Dict, List, Union

import pytest
from pytest import CaptureFixture
import yaml

from create_github_project.utils import Accounts


class TestAccountsClass:

    USER1 = 'user1-' + 'a' * 50
    USER2 = 'user2-' + 'a' * 50

    @pytest.fixture(autouse=True)
    def filepath(self, tmpdir: LocalPath):
        old_path = Accounts.FILE_PATH
        Accounts.FILE_PATH = Path(tmpdir.strpath).joinpath('accounts.json')
        yield
        Accounts.FILE_PATH = old_path

    @staticmethod
    def create_config_file(data: Dict[str, Dict[str, str]]) -> None:
        with open(Accounts.FILE_PATH, 'w') as f:
            f.write(json.dumps(data))

    @pytest.mark.parametrize(
        ['touch'],
        [
            [True],
            [False]
        ]
    )
    def test_initialized(self, touch: bool) -> None:
        if touch:
            self.create_config_file({})
        assert Accounts().initialized() == touch

    @pytest.mark.parametrize(
        ['accounts', 'account_id', 'result'],
        [
            [
                {},
                'github', False
            ],
            [
                {
                    'github': {
                        'display_name': 'GitHub',
                        'homepage': 'https://github.com/github'
                    },
                },
                'github', True
            ],
        ]
    )
    def test_exists(self, accounts: Dict[str, Dict[str, str]], account_id: str, result: bool) -> None:
        self.create_config_file(accounts)
        assert Accounts().exists(account_id) == result

    @pytest.mark.parametrize(
        ['accounts', 'users'],
        [
            [
                {
                    USER1: {
                        'display_name': 'USER1',
                        'homepage': 'https://github.com/' + USER1
                    },
                    USER2: {
                        'display_name': 'USER2',
                        'homepage': 'https://github.com/' + USER2
                    },
                },
                [USER1, USER2]
            ],
            [
                {},
                []
            ]
        ]
    )
    def test_list(self, accounts: Dict[str, Dict[str, str]], users: List[str]) -> None:
        self.create_config_file(accounts)
        assert set(Accounts().list()) == set(users)

    @pytest.mark.parametrize(
        ['accounts'],
        [
            [
                {
                    USER1: {
                        'display_name': 'USER1',
                        'homepage': 'https://github.com/' + USER1
                    },
                    USER2: {
                        'display_name': 'USER2',
                        'homepage': 'https://github.com/' + USER2
                    },
                },
            ],
            [
                {},
            ]
        ]
    )
    def test_dump_list(self, capfd: CaptureFixture, accounts: Dict[str, Dict[str, str]]) -> None:
        self.create_config_file(accounts)

        Accounts().dump_list()
        stdout, _ = capfd.readouterr()
        with StringIO(stdout) as sio:
            sio.seek(0)
            output = sio.read()

        if accounts:
            for a in yaml.safe_load(output):
                aid = a['account_id']
                assert aid in accounts.keys()
                assert a['display_name'] == accounts[aid]['display_name']
                assert a['homepage'] == accounts[aid]['homepage']
        else:
            assert output == ""

    @pytest.mark.parametrize(
        ['accounts', 'account_id', 'display_name', 'expect_homepage'],
        [
            [
                {},
                'github', 'GitHub', 'https://github.com/github'
            ],
            [
                {
                    'github': {
                        'display_name': 'GitHub',
                        'homepage': 'https://github.com/github'
                    },
                },
                'github', 'GitHub', None,
            ],
            # user が存在しない場合 (GitHub のユーザ名は39文字が上限)
            [
                {},
                'a'*50, 'User Not Exist', None
            ],
        ]
    )
    def test_add(self, accounts: Dict[str, Dict[str, str]], account_id: str, display_name: str,
                 expect_homepage: Union[str, None]) -> None:
        self.create_config_file(accounts)
        homepage = Accounts().add(account_id, display_name)
        assert expect_homepage == homepage

    def test_drop_ok(self) -> None:
        self.create_config_file({
            'github': {
                'display_name': 'GitHub',
                'homepage': 'https://github.com/github'
            }
        })
        Accounts().drop('github')

    def test_drop_fail(self) -> None:
        self.create_config_file({})
        with pytest.raises(ValueError):
            Accounts().drop('github')

    def test_get_account_info(self) -> None:
        info = {
            'display_name': 'GitHub',
            'homepage': 'https://github.com/github'
        }
        self.create_config_file({
            'github': info
        })

        result = Accounts().get_account_info('github')
        assert info == result
