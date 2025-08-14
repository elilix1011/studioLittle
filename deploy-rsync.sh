#!/bin/bash

# デプロイ設定
REMOTE_HOST="your-domain.com"
REMOTE_USER="your-username"
REMOTE_DIR="/public_html"

# アップロードするファイル/ディレクトリ
UPLOAD_FILES=(
    "contact/"
    "lesson/"
    "teachers/"
    "event/"
    "diet-yoga/"
    "onlineyoga/"
    "yoga-instructor/"
    "module/"
    "images/"
    "index.html"
)

echo "🚀 rsyncでデプロイを開始します..."

# 各ファイル/ディレクトリを同期
for file in "${UPLOAD_FILES[@]}"; do
    if [ -e "$file" ]; then
        echo "📁 同期中: $file"
        rsync -avz --delete "$file" "$REMOTE_USER@$REMOTE_HOST:$REMOTE_DIR/"
    else
        echo "⚠️  ファイルが見つかりません: $file"
    fi
done

echo "✅ rsyncデプロイが完了しました！"

