# Ensemble-BE

## 始め方

`sudo service neo4j start`で neo4j を起動
cypherGUI をインストールした人はそのディレクトリで`npm start`で起動
`python -m venv .venv`で仮想環境を構築（初回のみ）
`source .venv/bin/activate`で仮想環境に入る
`pip install -r requirements.txt`で必要なパッケージをインストール（時々）
`uvicorn api:app --reload`で起動
`deactivate`で仮想環境から退出
`sudo service neo4j stop`で neo4j を停止
