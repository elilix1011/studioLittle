FROM nginx:alpine

# 必要なパッケージのインストール
RUN apk add --no-cache \
    curl \
    vim \
    git

# Nginx設定のコピー
COPY docker/nginx/default.conf /etc/nginx/conf.d/default.conf

# 作業ディレクトリの設定
WORKDIR /var/www/html

# ポートの公開
EXPOSE 80

# ヘルスチェック
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost/ || exit 1
