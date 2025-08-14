# Studio Little Website

ロリポップサーバーで運用されているStudio LittleのWebサイトプロジェクトです。

## プロジェクト構成

```
studioLittle/
├── contact/          # お問い合わせページ
├── lesson/           # レッスン情報
├── teachers/         # 講師紹介
├── blog/             # WordPressブログ
├── event/            # イベント情報
├── diet-yoga/        # ダイエットヨガ
├── onlineyoga/       # オンラインヨガ
├── yoga-instructor/  # ヨガインストラクター
├── cgi/              # CGIスクリプト
├── mail_v3/          # メールフォーム
├── module/           # 共通モジュール
└── docker/           # Docker設定
```

## 開発環境のセットアップ

### 前提条件
- Docker
- Docker Compose
- Git

### セットアップ手順

1. リポジトリをクローン
```bash
git clone <repository-url>
cd studioLittle
```

2. Dockerコンテナを起動
```bash
docker-compose up -d
```

3. ブラウザでアクセス
- メインサイト: http://localhost:8080
- 開発用PHP環境: http://localhost:8081

## 開発ワークフロー

1. ローカルでファイルを編集
2. `git add` で変更をステージング
3. `git commit` で変更をコミット
4. 必要に応じてFTPでロリポップサーバーにアップロード

## ファイル管理

### Git管理対象
- HTML/CSS/JavaScriptファイル
- 画像ファイル
- PHPファイル
- Docker設定ファイル

### Git管理除外
- バックアップファイル (*.bak, *.202*, *.old)
- ログファイル (*.log)
- 一時ファイル (*.tmp, *.temp)
- システムファイル (.DS_Store)
- WordPress設定ファイル (wp-config.php)

## 技術スタック

- **Webサーバー**: Nginx
- **PHP**: 8.1
- **フレームワーク**: WordPress (blog/)
- **CGI**: Perl
- **フロントエンド**: HTML5, CSS3, JavaScript

## 注意事項

- 本番環境の設定ファイルは含まれていません
- データベース接続情報は環境変数で管理してください
- セキュリティ上重要なファイルは.gitignoreで除外されています

## ライセンス

このプロジェクトはStudio Littleの所有物です。
