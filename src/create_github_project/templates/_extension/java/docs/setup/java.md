# Java 開発環境 構築手順

## IntelliJ のインストール

[リンク](https://www.jetbrains.com/ja-jp/idea/download/) より IntelliJ をインストールする。

## IDE の初期設定

### コードスタイルの定義

1. **Preferences** を開き、Editor > Code Style > Java へ遷移。

    ![pref](https://user-images.githubusercontent.com/49669363/126277501-29201553-1a3e-4f16-82f3-fe683a093ed3.png)

1. 「Schema」にて「project」を選択

    ![schema](https://user-images.githubusercontent.com/49669363/126277631-87771b07-30a4-469a-ac2a-054fcf5549af.png)

1. 歯車マークから、import Schema > IntelliJ IDEA code style XML を選択

    ![xml](https://user-images.githubusercontent.com/49669363/126277878-7a160270-eb61-48e5-b96d-d7298c129c24.png)

1. 本リポジトリ内の [schema.xml](./schema.xml) を選択した後、「Current Schema」を選択の上「OK」をクリック

    ![import](https://user-images.githubusercontent.com/49669363/126278504-52b5e6e3-536f-4407-9ee6-d4f897388c14.png)

### 自動整形の有効化

[リンク先](https://qiita.com/sisidovski/items/bde2d844c3c73457923c#%E3%83%9E%E3%82%AF%E3%83%AD%E3%82%92%E7%99%BB%E9%8C%B2%E3%81%99%E3%82%8B) の手順を参照。
