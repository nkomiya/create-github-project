# GitHub プロジェクト 雛形作成ツール

## 前提条件

- Python 3.7 以降がインストールされていること
- 補完を有効にする場合
    - Bash shell を利用する場合は、Bash のバージョンが 4.4 以降であること

## セットアップ手順

### 1. 仮想環境作成

本ツールは Python を利用したコマンドラインツールであるため、Python の仮想環境を作成する。

```bash
INSTALL_DIR=<仮想環境作成先の絶対パス>

python -m venv ${INSTALL_DIR}
```

### 2. インストールと設定

#### インストール

```bash
${INSTALL_DIR}/bin/python -m pip install -U pip
${INSTALL_DIR}/bin/python -m pip install -U git+https://github.com/nkomiya/create-github-project@v0.3.1
```

#### コマンドの設定

1. 環境変数 PATH に含まれるディレクトリに Symbolic link を作成

    ```bash
    ln -s ${INSTALL_DIR}/bin/create-github-project <Symbolic link 作成先>
    ```

1. 補完の有効化

    - **bash** : ~/.bashrc に下記を追記

        ```bash
        eval "$(LC_MESSAGES='en_US.UTF-8' _CREATE_GITHUB_PROJECT_COMPLETE=bash_source create-github-project)"
        ```

    - **zsh** : ~/.zshrc に下記を追記

        ```shell
        # 「command not found: compdef」のエラーが出る場合は、下記の設定も必要
        # autoload -Uz compinit
        # compinit

        eval "$(_CREATE_GITHUB_PROJECT_COMPLETE=zsh_source create-github-project)"
        ```

    - **fish** : ~/.config/fish/completions/create-github-project.fish に下記を追記

        ```shell
        eval (env _CREATE_GITHUB_PROJECT_COMPLETE=fish_source create-github-project)
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
    create-github-project account add nkomiya --display-name nkomiya
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
