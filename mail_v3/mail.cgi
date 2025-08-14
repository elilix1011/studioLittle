#!/usr/bin/perl

#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\  Creation company : DIC Co.,Ltd.
#\\  http://www.d-ic.com/
#\\  DIC-Studio. Mail_v3 Version:1.01 (2008/11/07)
#\\  Copyright (C) DIC All Rights Reserved. このスクリプトの再配布などを禁止します.
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

require "./jcode.pl";
require "./stdio.pl";

##*****<< 設置方法 >>******************************************************************************
##
## ※ＣＧＩファイルの初期設定をお使いの環境に合わせてカスタマイズしてください。
## ※お使いのサーバによっては下のファイル構成では動作しない場合があります。
##   その際はサーバ管理者にお問い合わせください。
## ※"[]"内の数字はパーミッションです。
##
## public_html/
##  |
##  +-- mail_v3/
##        |    mail.cgi   [755/700]  メール送信本体ＣＧＩ
##        |    jcode.pl
##        |    stdio.pl
##        |    tpl1.html   入力ページ
##        |    tpl2.html   確認ページ
##        |    tpl3.html   完了ページ
##        |    mailtpl_adm.txt   メールテンプレート（管理者宛て）
##        |    mailtpl_usr.txt   メールテンプレート（ユーザ宛て）
##        |    attention.gif
##        |    style.css
##        |    index.html
##        |
##        +-- data/     [777/705]
##        |      data.cgi  [666/600]   入力内容保存ファイル
##        |      index.html
##        |
##        +-- tmp/      [777/705]
##               index.html
##
## ※入力ページは
## http://設置したURL/mail_v3/mail.cgi
## となります。
## tpl1.html に直接アクセスすると、正しく動作しませんので、ご注意ください。
##
##
##*****<< バージョンアップ情報 >>******************************************************************
##
## 2008/11/07 .....Ver1.01
##   ・チェックボックス、ラジオボタンのフォームタグを必須制限した際に正しく動作しない不具合を修正
##
##
##*************************************************************************************************


##=====================================
##      初期設定部分 ここから         =
##=====================================

# 管理者名・メールアドレス

$adm_name = 'Studio little';	# 管理者名
$adm_email = 'little.group.little@gmail.com';	# メールアドレス（受信先になります）
#$adm_email = 'aika_i2005@yahoo.co.jp';	# メールアドレス（受信先になります）
# セレクトメニューのリスト
# 入力ページにセレクトメニューがある場合、その name値（name="xxx" の xxx の部分）を指定してください。

@sel_list = (
	'who','class','what','contact'
);


# 入力必須項目
# 「'name値' => 'エラー時のメッセージ',」の形で指定してください。

%hissu = (
	'name'	=>	'【お名前】をご入力ください。',
	'kana'	=>	'【フリガナ】をご入力ください。',
	'email'	=>	'【メールアドレス】をご入力ください。',
	'message'	=>	'【お申し込み・お問い合わせ内容】をご入力ください。',
);


# メールの件名

$subject_adm = '【web】studio little お申し込み・お問い合わせ';	# 管理者宛てメール
$subject_usr = 'お問い合わせありがとうございます';	# ユーザ宛てメール


# 入力内容保存ファイル
# ご利用時は、FTPソフトでダウンロードし、拡張子を .csv に変更した後にご利用ください。
# 蓄積保存しておりますので、容量に気を付けてください。

$datafile = './data/data.cgi';



# 入力内容一時保存用ディレクトリ ※/で終わらない
$input_dir = './tmp';

# テンプレートHTML
$html_form1 = './tpl1.html';	# 入力フォーム
$html_form2 = './tpl2.html';	# 入力確認
$html_form3 = './tpl3.html';	# 送信完了

# メールテンプレート
$form_mail1 = './mailtpl_adm.txt';	# 管理者宛
$form_mail2 = './mailtpl_usr.txt';	# ユーザ宛

# ロックディレクトリ
$lock = './tmp';

# 古い「入力情報を保存したファイル」を削除する期限 ※秒で指定
$expires = '259200';

# 時差（グリニッジ標準時＝英国ロンドン）を秒で指定
$time_difference = '32400';

# クッキーID
$cookie_id = 'MyCookie';


##=====================================
##      初期設定部分 ここまで         =
##=====================================



#□□□□□□□□□□□□ ここから下を修正した場合にはサポート対象外になります。ご注意ください。 □□□□□□□□□□□□□□□□□□□□□□□□□□□□□□

##=====================================
## データを受け取る
##=====================================
$separator = ' / ';
%param = ();
@keys = stdio::getFormData(\%param, "1", "SJIS", $separator, "", "sjis");
@keys = grep(!$seen{$_}++, @keys);


##=====================================
## クッキーを読み込む
##=====================================
%COOKIE = ();
stdio::getCookie(\%COOKIE, $cookie_id);
if(!$COOKIE{'id'}){
	if($param{'mode'}){ &error('エラー','クッキーが読み込めませんでした。入力フォームに戻ってください。'); }
	
	$time = time;
	$random = stdio::getRandomString(4);
	$COOKIE{'id'} = $time."-".$random;
}


##=====================================
## 入力情報保存ファイル
##=====================================
$input_datafile = "$input_dir/$COOKIE{'id'}.cgi";


##=====================================
## 古い入力情報保存ファイルを削除する
##=====================================
foreach(glob($input_dir."/*.cgi")){
	@stat = stat;
	$time = time;
	$time -= $expires;
	
	if($stat[9] < $time){ unlink; }
}



#□□□□□ モード なし ここから □□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□
if($param{'mode'} eq ''){

##=====================================
## 入力エラーの表示
##=====================================
if($param{'action'} eq 'err'){
	if(-e $input_datafile){
		foreach(&fileopen($input_datafile)){
			chomp;
			my ($key, $val) = split(/\t/);
			
			if($key eq 'email'){ $email = $val; }
			
			# 必須チェック
			if(($hissu{$key} and $val eq '') or ($hissu{$key} and $val eq 'dummy')){
				$subst{'error_mes'} .= qq|<li>$hissu{$key}</li>|;
				
				# メール必須チェック済み
				$email_checked = 1;
			}
			
			# メールのチェック
			if($key eq 'email' and !$email_checked){
				$string_result = &InputCheck($val, "1", "255");
				if($string_result){
					$subst{'error_mes'} .= qq|<li>【メールアドレス】の入力を誤っています。</li>|;
				}
			}
			if($key eq 'email2'){
				if($email ne $val){
					$subst{'error_mes'} .= qq|<li>【メールアドレス】と【メールアドレス確認用】の入力が異なっています。</li>|;
				}
			}
		}
	}
}

if($subst{'error_mes'}){
	$subst{'error_display'} = 'display: block;';
}


##=====================================
## 入力情報を復元
##=====================================
# セレクトメニューのリスト
foreach(@sel_list){
	$sel{$_} = $_;
}

# 復元
if(-e $input_datafile){
	
	foreach(&fileopen($input_datafile)){
		chomp;
		my($key, $val) = split(/\t/);
		
		$val =~ s/<br \/>/\n/g;
		
		if($sel{$key}){
			if($val){
				$subst{$key} = qq|<option value="$val" selected="selected">$val</option>\n<option value="">-----</option>\n|;
			}
		}
		else{
			foreach(split(/$separator/, $val)){
				$subst{$key."_".$_} = qq|checked="checked"|;
			}
			
			$subst{$key} = $val;
		}
	}
}

foreach(@sel_list){
	if(!$subst{$_}){ $subst{$_} = qq|<option value="" selected="selected">お選び下さい</option>\n|; }
}


##=====================================
## HTML生成
##=====================================
$subst{'copyright'} = qq|<div style="clear:both; width:100%; text-align:right; font-size:12px;">- <a href="http://www.d-ic.com/" target="_blank">メール送信CGI： DIC-Studio</a> -</div>|;
foreach(&fileopen($html_form1)){
	if(/_%copyright%_/){
		$c_flag = 1;
		last;
	}
}
if(!$c_flag){ &error('エラー', '著作権表示が削除されています。'); }

$htmldata = &dicTag(&fileopen($html_form1));


##=====================================
## ＨＴＭＬ出力
##=====================================
print "Content-type: text/html\n";

stdio::setCookie(\%COOKIE, $cookie_id);

print <<"EOF";

$htmldata
EOF
exit;
}	# モード なし ここまで



#□□□□□ モード check ここから □□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□
elsif($param{'mode'} eq 'check'){

##=====================================
## 入力情報保存ファイルに書き込む
##=====================================
foreach(@keys){
	$param{$_} =~ s/\n/<br \/>/g;
	push(@inputdata, "$_\t$param{$_}\n");
}

if(!open(DATA,">$input_datafile")){ stdio::unlock($lock); &error('システムエラー',"入力内容一時保存ファイルを生成できませんでした。"); }
seek(DATA,0,0);
print DATA @inputdata;
truncate(DATA,tell(DATA));
close(DATA);


##=====================================
## 入力チェック
##=====================================
foreach(keys %hissu){
	if($param{$_} eq '' or $param{$_} eq 'dummy'){
		$error_mes = 1;
	}
}

if($param{'email'}){
	$string_result = &InputCheck($param{'email'}, "1", "255");
	if($string_result){
		$error_mes = 1;
	}
}
if($param{'email2'}){
	if($param{'email'} ne $param{'email2'}){
		$error_mes = 1;
	}
}

if($error_mes){
	my ($location, $tmp_param) = split(/\?/, $ENV{'HTTP_REFERER'});
	print "Location: $location?action=err\n\n";
}


##=====================================
## 置換用
##=====================================
foreach(@keys){
	@tmp = ();
	if($_ eq 'mode'){ next; }
	
	$param{$_} =~ s/\n/<br \/>/g;
	
	# dummyの削除
	my @param = split(/$separator/, $param{$_});
	$dummy_cnt = 0;
	$del_cnt = '';
	foreach(@param){
		if($_ eq 'dummy'){ $del_cnt = $dummy_cnt; }
		$dummy_cnt++;
	}
	if($del_cnt ne ''){
		splice(@param, $del_cnt, 1);
	}
	$param{$_} = join("$separator", @param);
	
	# %subst
	$subst{$_} = $param{$_};
	
	# param
	$subst{'param'} .= qq|<input type="hidden" name="$_" value="$subst{$_}" />\n|;
}


##=====================================
## HTML生成
##=====================================
$subst{'copyright'} = qq|<div style="clear:both; width:100%; text-align:right; font-size:12px;">- <a href="http://www.d-ic.com/" target="_blank">メール送信CGI： DIC-Studio</a> -</div>|;
foreach(&fileopen($html_form2)){
	if(/_%copyright%_/){
		$c_flag = 1;
		last;
	}
}
if(!$c_flag){ &error('エラー', '著作権表示が削除されています。'); }

$htmldata = &dicTag(&fileopen($html_form2));


##=====================================
## ＨＴＭＬ出力
##=====================================
print <<"EOF";
Content-type: text/html

$htmldata
EOF
exit;
}	# モード check ここまで



#□□□□□ モード send ここから □□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□
elsif($param{'mode'} eq 'send'){

##=====================================
## ロック
##=====================================
if(!stdio::lock($lock)){ &error('ERROR','Busy!'); }


##=====================================
## CSVファイルに書き込む
##=====================================
if(!open(DATA,"+<$datafile")){ stdio::unlock($lock); &error('システムエラー',"入力内容保存ファイルを書込みオープンできませんでした。"); }
@db = <DATA>;

# 現在日時
$subst{'send_date'} = $now_date = stdio::getTime("%yyyy-%mm-%dd %hh:%nn:%ss", $time_difference);

foreach(@keys){
	if($_ eq 'mode'){ next; }
	if($_ eq 'Submit'){ next; }
	if($_ eq 'submit'){ next; }
	if($_ eq 'email2'){ next; }
	
	$param = $param{$_};
	$param =~ s/&lt;br \/&gt;/ /g;
	push(@regist, qq|"$param"|);
}
$regist = join(",", @regist);

push(@db, qq|"$now_date",$regist\n|);

seek(DATA,0,0);
print DATA @db;
truncate(DATA,tell(DATA));
close(DATA);


##=====================================
## アンロック
##=====================================
stdio::unlock($lock);


##=====================================
## メール文面置換用
##=====================================
foreach(@keys){
	$param{$_} =~ s/&lt;br \/&gt;/\n/g;
	
	# %subst
	$subst{$_} = $param{$_};
}


##=====================================
## メール文章を生成
##=====================================
$mailbody_adm = &dicTag(&fileopen($form_mail1));
$mailbody_usr = &dicTag(&fileopen($form_mail2));


##=====================================
## メール送信（管理者宛）
##=====================================
%header = (
	'To'	=> $adm_name." <".$adm_email.">",
	'From'	=> $param{'email'},
	'Subject'	=> $subject_adm,
	'Mime-Version'	=> '1.0'
);

$mailbody_adm .= "\n";
$mailbody_adm .= "----------------------------------------------------------------\n";
$mailbody_adm .= "Processed       : $date_now\n";
$mailbody_adm .= "Server-Name     : $ENV{'SERVER_NAME'}\n";
$mailbody_adm .= "Script-Name     : $ENV{'SCRIPT_NAME'}\n";
$mailbody_adm .= "HTTP-Referer    : $ENV{'HTTP_REFERER'}\n";
$mailbody_adm .= "HTTP-User-Agent : $ENV{'HTTP_USER_AGENT'}\n";
$mailbody_adm .= "Remote-host     : $ENV{'REMOTE_HOST'}\n";
$mailbody_adm .= "Remote-Addr     : $ENV{'REMOTE_ADDR'}\n";
$mailbody_adm .= "----------------------------------------------------------------\n";

stdio::sendmail(\%header, $mailbody_adm);


##=====================================
## メール送信（ユーザ宛）
##=====================================
%header = (
	'To'	=> $param{'email'},
	'From'	=> $adm_name." <".$adm_email.">",
	'Subject'	=> $subject_usr,
	'Mime-Version'	=> '1.0'
);

if($param{'email'}){
	stdio::sendmail(\%header, $mailbody_usr);
}


##=====================================
## 一時ファイル削除
##=====================================
unlink $input_datafile;


##=====================================
## HTML生成
##=====================================
$subst{'copyright'} = qq|<div style="clear:both; width:100%; text-align:right; font-size:12px;">- <a href="http://www.d-ic.com/" target="_blank">メール送信CGI： DIC-Studio</a> -</div>|;
foreach(&fileopen($html_form3)){
	if(/_%copyright%_/){
		$c_flag = 1;
		last;
	}
}
if(!$c_flag){ &error('エラー', '著作権表示が削除されています。'); }

$htmldata = &dicTag(&fileopen($html_form3));


##=====================================
## ＨＴＭＬ出力
##=====================================
#print <<"EOF";
#Content-type: text/plain
#
#To       => $adm_name <$adm_email>
#From     => $param{'email'}
#Subject  => $subject_adm
#
#$mailbody_adm
#
#
#
#To       => $param{'email'}
#From     => $adm_name <$adm_email>
#Subject  => $subject_usr
#
#$mailbody_usr
#EOF
#exit;
#
#
print <<"EOF";
Content-type: text/html

$htmldata
EOF
exit;
}	# モード send ここまで





##=====================================
## 特殊タグの置き換え
##=====================================
# $htmldata = &dicTag(@html);
sub dicTag # (@html)
{
	local(@array) = @_;
	local($data);
	
	$data = '';
	foreach(@array){
		s/_%(.+?)%_/$subst{$1}/g;
		$data .= $_;
	}
	return($data);
}


##=====================================
## 入力文字のチェック
##=====================================
sub InputCheck { # ($param{'email'}, $type ,$maxlength)
	# $type  1=email  2=電話やファックス等
	# $maxlength  最大バイト数
	
# サンプル（Ｅメールチェック）
#$string_result = &InputCheck($emailaddress, "1", "255");
#if($string_result){
#	&error('error','Eメールアドレスの入力を誤っています。');
#}
	
	local($string, $type, $maxlength) = @_;
	local($error_flag);
	
	if($type eq "1"){
		if($string =~ /[^-.\@_a-zA-Z0-9]/){ $error_flag = '1'; }
		unless($string =~ /[-._a-zA-Z0-9]+\@[-._a-zA-Z0-9]+\.[-._a-zA-Z0-9]+/){ $error_flag = '1'; }
		if($maxlength and (length $string) >= $maxlength){ $error_flag = '1'; }
	}
	elsif($type eq "2"){
		if($string =~ /[^-\(\)0-9]/){ $error_flag = '1'; }
		unless($string =~ /\(?\d+\)?\-?\(?\d+\)?\-?\d+/){ $error_flag = '1'; }
		if($maxlength and (length $string) >= $maxlength){ $error_flag = '1'; }
	}
	
	return ($error_flag);
}


##=====================================
## ファイルオープン
##=====================================
sub fileopen { # ($filepath)
	local($file) = @_;
	local(@array);
	
	if(!open(IN,$file)){
		stdio::unlock($lock);
		&error('システムエラー',"ファイル（$file）をオープンできませんでした。"); }
	@array = <IN>;
	close(IN);
	
	return (@array);
}


##=====================================
## エラー表示
##=====================================
sub error { # ($error_tile, $error_message)
	
	# ロック解除
	stdio::unlock($lock);
	
	print <<"END";
Content-type: text/html

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=shift_jis" />
<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Cache-Control" content="no-cache">
<title>$_[0]</title>
<style type="text/css">
<!--
body {
	font-family: "Verdana", "Helvetica","ＭＳ ゴシック", "Osaka－等幅";
	font-size: 12px;
	color: #333333;
	background-color: #FFFFFF;
	line-height: 150%;
}
td {
font-size: 12px;
line-height: 150%;
}
a {
color: #0000FF;
}
a:hover {
color: #CC0000;
}
.font16 {
font-size: 16px;
}
.titlebar2 {
border-top-width: 1px;
border-right-width: 0px;
border-bottom-width: 1px;
border-left-width: 0px;
border-top-style: solid;
border-right-style: solid;
border-bottom-style: solid;
border-left-style: solid;
border-top-color: #FFCC00;
border-right-color: #FFCC00;
border-bottom-color: #FFCC00;
border-left-color: #FFCC00;
}
-->
</style>
</head>

<body>
<table width="80%" border="0" align="center" cellpadding="0" cellspacing="0">
 <tr>
  <td bgcolor="#FF9900">
   <table width="100%" border="0" cellpadding="5" cellspacing="1">
    <tr>
     <td align="center" bgcolor="#FFCC00">$_[0]</td>
    </tr>
    <tr>
     <td bgcolor="#FFFFFF">
      <table border="0" align="center" cellpadding="20" cellspacing="0">
       <tr>
        <td>$_[1]</td>
       </tr>
      </table>
      <table border="0" align="center" cellpadding="20" cellspacing="0">
       <tr>
        <td><a href="javascript:history.back()">コチラをクリック</a>するか、ブラウザの戻るボタンをクリックして前の画面に移動してください。</td>
       </tr>
      </table>
     </td>
    </tr>
   </table>
   </td>
 </tr>
</table>
</body>
</html>
END
exit;
}
