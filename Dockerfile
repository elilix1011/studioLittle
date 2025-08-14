FROM nginx:alpine

# 必要なパッケージをインストール
RUN apk add --no-cache \
    curl \
    vim \
    git \
    perl \
    perl-cgi \
    perl-module-build

# Nginx設定ファイルをコピー
COPY docker/nginx/default.conf /etc/nginx/conf.d/default.conf

# ポート80を公開
EXPOSE 80

# Nginxを起動
CMD ["nginx", "-g", "daemon off;"]
