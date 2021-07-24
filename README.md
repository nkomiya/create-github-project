# GitHub プロジェクト 雛形作成ツール

## 前提条件

- Python 3.7 以降がインストールされていること

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
    ${INSTALL_DIR}/bin/python -m pip install -U git+https://github.com/nkomiya/create-github-project@v0.2.0
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

### Git リポジトリの雛形作成

下記コマンドの実行により、ローカル PC に Git リポジトリの雛形が作成される。

```bash
create-github-project init sample-project
```

#### リポジトリ作成時のオプションの表示

リポジトリ作成時のオプション項目は、指定が無い場合は CLI により指定が促される。
上記挙動が煩わしい場合は、CLI のオプションによるオプション項目の指定が利用可能。

```bash
create-github-project init --help
```

### レビュアーの管理

本ツールにて作成される Git リポジトリには、リリースの PR を作成する GitHub Actions が含まれる。
この PR へレビュアーを自動割当されるようにするには、レビュアーに指定したい GitHub アカウントをリポジトリ作成前に事前登録する必要がある。

- 追加

    ```bash
    create-github-project account add nkomiya --display-name 古宮
    ```

- 一覧表示

    ```bash
    create-github-project account list
    ```

- 削除

    ```bash
    create-github-project account drop nkomiya
    ```

### ツールのバージョン管理

#### バージョンのアップデート

最新版のリリースが GitHub 上に存在する場合、下記コマンドによりアップデートが可能。

```bash
create-github-project update
```

#### 現行のバージョン確認

```bash
create-github-project version
```
