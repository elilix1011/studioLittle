FROM nginx:alpine

# 必要なパッケージをインストール
RUN apk add --no-cache \
    curl \
    vim \
    git \
    perl \
    perl-cgi \
    perl-module-build \
    fcgiwrap \
    spawn-fcgi

# fcgiwrapを起動するスクリプトを作成
RUN echo '#!/bin/sh' > /start.sh && \
    echo 'spawn-fcgi -s /var/run/fcgiwrap.socket -M 766 /usr/bin/fcgiwrap' >> /start.sh && \
    echo 'nginx -g "daemon off;"' >> /start.sh && \
    chmod +x /start.sh

# Nginx設定ファイルをコピー
COPY docker/nginx/default.conf /etc/nginx/conf.d/default.conf

# ポート80を公開
EXPOSE 80

# 起動スクリプトを実行
CMD ["/start.sh"]
