# GitHub プロジェクト 自動作成ツール

## 前提条件

- Python 3.7 以降がインストールされていること
- yarn が global インストールされていること

## セットアップ手順

### 1. 仮想環境作成

本ツールは Python を利用したコマンドラインツールであるため、Python の仮想環境を作成する。

```bash
INSTALL_DIR=<仮想環境作成先の絶対パス>

python -m venv ${INSTALL_DIR}
```

### 2. インストールと設定

- install

    ```bash
    ${INSTALL_DIR}/bin/python -m pip install -U pip
    ${INSTALL_DIR}/bin/python -m pip install -U git+https://github.com/nkomiya/create-github-project
    ```

- エイリアスと補完

    ```bash
    alias create-github-project="${INSTALL_DIR}/bin/create-github-project"

    # 補完 (bash shell)
    eval "$(
        LC_ALL='en_US.UTF8' _CREATE_GITHUB_PROJECT_COMPLETE=bash_source create-github-project |
        sed -e "s|\$1|${INSTALL_DIR}/bin/create-github-project|"
    )"
    ```

## 使用方法

### GitHub リポジトリのテンプレートを作成する

```bash
create-github-project init sample-project
```
