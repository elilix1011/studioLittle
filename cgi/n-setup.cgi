package main;

##======================================================##
##  AmigoNewsBoard用基本設定ファイル                    ##
##  Copyright(C)2000 cgi-amigo.com All Rights Reserved  ##
##  http://www.cgi-amigo.com/                           ##
##  webmaster@cgi-amigo.com                             ##
##======================================================##

# このスクリプトは無料でご利用頂けますが著作権は放棄していません。
# 同梱の利用規定ファイル(kitei.txt)の利用規定を厳守の上ご利用下さい。
# ファイルを紛失した場合はhttp://www.cgi-amigo.com/kitei.htmlよりご確認下さい。
# 最新バージョンもhttp://www.cgi-amigo.com/よりご確認頂けます。

###########################################################

# ■管理用パスワード
$AdminPass='hudou802';

# ■基本ディレクトリ
$BaseDir='http://studiolittle.info/cgi';

# ■設置サイトの最短URL
@MyUrl=('http://studiolittle.info/');

# ■ニュースページ等へのリンク制限(ON=1/OFF=0)
$LinkChkMode=0;

# ■ホーム(戻り先)のURL
$HomeUrl='http://studiolittle.info/';

# ■データディレクトリ
$DataDir='./data';

# ■画像ディレクトリ
$ImageDir='./image';

# ■ロックディレクトリ
$LockDir='./lock';

# ■ロックタイプ(1=flock式/2=rename式/3=symlink式/4=mkdir式/5=open式)
$LockType=4;

# ■メインスクリプト名
$MainCGI='newsboard.cgi';

# ■記事タイトルファイル(title.js)のパス
$TitleFile='./title.js';

# ■ユーザー設定を有効にする(ON=1/OFF=0)
$CookieMode=0;

# ■クッキー有効期限(日)
$CookieExpires=120;

# ■デフォルトニュース表示件数
$DefaultNView=20;

# ■ニュース表示件数をデフォルトに固定(ON=1/OFF=0)
$NViewFixedMode=0;

# ■最大ニュース表示件数
$MaxNView=50;

# ■デフォルト検索結果表示件数
$DefaultSView=20;

# ■検索結果表示件数をデフォルトに固定(ON=1/OFF=0)
$SViewFixedMode=0;

# ■最大検索結果表示件数
$MaxSView=50;

# ■オートリンク機能(ON=1/OFF=0)
$AutoLinkMode=1;

# ■オートリンクのターゲット
$AutoTarget='_blank';

# ■使用可能タグ(閉じないタグ=0/閉じるタグ=1)
%PermitTag=('A'=>1,'B'=>1,'FONT'=>1,'I'=>1,'U'=>1,'PRE'=>1,'HR'=>0,'IMG'=>0);

# ■使用可能タグ属性
%TagProperty=(
'A'=>'href|target',
'FONT'=>'color|face',
'IMG'=>'src|border',
);

# ■最大ニュース件数(1ファイル)
$MaxNews=200;

# ■最大タイトル件数
$MaxTitle=10;

# ■過去ログ最大ファイル数
$MaxOldFile=10;

# ■誤２重送信防止機能(ON=1/OFF=0)
$SidChkMode=1;

# ■method形式チェック(ON=1/OFF=0)
$MethodChkMode=1;

# ■ジャンプタイプ(0=Location/1=META)
$LocationType=0;

# ■時差修正(日本は+9)
$TimeZone=+9;

# ■ジャンル設定
%GENRE=(
1=>['トピック','http://'],
);

###########################################################

# =====================記事デザイン設定========================

###########################
#   記事1件分のデザイン   #
###########################
sub _Html_List{ print <<EOM;
<TABLE width="100%" cellPadding=0 cellSpacing=0>
<TR><TD bgcolor="#FF9999">&nbsp;$VD[$REC{Title}]</TD></TR>
<TR><TD class="Status">&nbsp;No: $VD[$REC{DataNum}] /&nbsp;Genre: $GENRE{$VD[$REC{Genre}]}[0]&nbsp;/&nbsp;Date: $VD[$REC{Rtime}]</TD></TR></TABLE><BR>
<BLOCKQUOTE class="Comment">$VD[$REC{Comment}]<BR><BR><A href="$VD[$REC{Url}]">$VD[$REC{Url}]</A></BLOCKQUOTE>
EOM
}

#####################################
#   記事1件分のデザイン(検索結果)   #
#####################################
sub _Html_Search{ print <<EOM;
<TABLE width="100%" cellPadding=0 cellSpacing=0>
<TR><TD bgcolor="#FF9999">&nbsp;$VD[$REC{Title}]</TD></TR>
<TR><TD class="Status">&nbsp;No: $VD[$REC{DataNum}] /&nbsp;Genre: $GENRE{$VD[$REC{Genre}]}[0]&nbsp;/&nbsp;Date: $VD[$REC{Rtime}]</TD></TR></TABLE><BR>
<BLOCKQUOTE class="Comment">$VD[$REC{Comment}]<BR><BR><A href="$VD[$REC{Url}]">$VD[$REC{Url}]</A></BLOCKQUOTE>
EOM
}

###########################################################
1;
