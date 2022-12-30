# posted_articles_qiita

これまで投稿してきた記事の総閲覧数の確認

1. tmp_config.ini のファイル名をconfig.ini に変更する
1. 自身のアクセストークンをconfig.iniに記入
1. 以下のコードを実行し、環境構築

```
python -m venv venv
.\venv\Scripts\activate

pip install requests
```

## Run
```
python qiita_my_articles.py
```