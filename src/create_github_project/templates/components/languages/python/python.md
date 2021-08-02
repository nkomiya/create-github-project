# Python 開発環境 構築手順

## 拡張機能のインストール

- インストール対象
    - [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
    - [Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance)

- インストールコマンド

    ```bash
    code --install-extension ms-python.python
    code --install-extension ms-python.vscode-pylance
    ```

## 拡張機能のセットアップ

### 仮想環境作成

下記コマンドにより、Git のルートディレクトリに Python の仮想環境を作成する。

```bash
# Gitのルートディレクトリへ移動
cd $(git rev-parse --show-toplevel)

# Python 仮想環境の作成
python -m venv ./venv

# コード整形/静的解析用にライブラリを追加
. venv/bin/activate && pip install autopep8 flake8
```

### VS Code の設定

**Settings** にて下記操作を行い、追加した拡張機能のセットアップを行う。

#### VS Code における Python 仮想環境の有効化

1. Command palette を開き「Python: Select Interpreter」を選択

    ![select](https://user-images.githubusercontent.com/49669363/126274449-079a08ac-b815-4a23-ad53-6b8536c87a7b.png)

1. 「Enter interpreter path...」を選択

    ![enter](https://user-images.githubusercontent.com/49669363/126274579-f8b83d90-1b5c-4423-8b24-bd6142e5ea82.png)

1. 表示される入力窓に「./venv/bin/python」を入力
1. Window の下部にて仮想環境が選択されたことを確認

    ![check](https://user-images.githubusercontent.com/49669363/126275017-f0f8320d-a369-4734-9bc7-4a3ddc1d747e.png)

#### Autopep8 の設定

1. 単一行の文字数の最大値を120文字に設定

    ![autopep](https://user-images.githubusercontent.com/49669363/117638923-52716d80-b1be-11eb-985a-cf19027a077d.png)

#### Flake8 の設定

1. Flake8 の有効化、単一行の文字数の最大値を120文字に設定

    ![flake](https://user-images.githubusercontent.com/49669363/117638929-543b3100-b1be-11eb-8676-27db39cdf810.png)

### 補足

- Autopep8により、[PEP8](https://www.python.org/dev/peps/pep-0008/) 準拠のコーディングスタイルに統一できる
- Flake8 により、コードの静的解析(構文チェック等)が行われ、構文の誤り等がハイライトされる。

    - Flake8 によるハイライト例

        ![example](https://user-images.githubusercontent.com/49669363/126272558-32b32777-d5d6-4e48-a151-cd6eb46f6cbe.png)
- 注意
    - Flake8 による静的解析は VS Code 上でアクティブな (=開いている) ファイルのみが対象となる。
