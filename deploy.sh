#!/bin/bash

# デプロイ設定
FTP_HOST="your-domain.com"
FTP_USER="your-username"
FTP_PASS="your-password"
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

echo "🚀 デプロイを開始します..."

# FTPコマンドの作成
cat > ftp_commands.txt << EOF
open $FTP_HOST
user $FTP_USER $FTP_PASS
binary
cd $REMOTE_DIR
EOF

# 各ファイル/ディレクトリをアップロード
for file in "${UPLOAD_FILES[@]}"; do
    if [ -d "$file" ]; then
        echo "📁 ディレクトリをアップロード: $file"
        echo "mirror --reverse --delete $file $file" >> ftp_commands.txt
    else
        echo "📄 ファイルをアップロード: $file"
        echo "put $file" >> ftp_commands.txt
    fi
done

echo "quit" >> ftp_commands.txt

# FTPコマンドの実行
lftp -f ftp_commands.txt

# 一時ファイルの削除
rm ftp_commands.txt

echo "✅ デプロイが完了しました！"

