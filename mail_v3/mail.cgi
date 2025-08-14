#!/usr/bin/perl

#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\  Creation company : DIC Co.,Ltd.
#\\  http://www.d-ic.com/
#\\  DIC-Studio. Mail_v3 Version:1.01 (2008/11/07)
#\\  Copyright (C) DIC All Rights Reserved. ���̃X�N���v�g�̍Ĕz�z�Ȃǂ��֎~���܂�.
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

require "./jcode.pl";
require "./stdio.pl";

##*****<< �ݒu���@ >>******************************************************************************
##
## ���b�f�h�t�@�C���̏����ݒ�����g���̊��ɍ��킹�ăJ�X�^�}�C�Y���Ă��������B
## �����g���̃T�[�o�ɂ���Ă͉��̃t�@�C���\���ł͓��삵�Ȃ��ꍇ������܂��B
##   ���̍ۂ̓T�[�o�Ǘ��҂ɂ��₢���킹���������B
## ��"[]"���̐����̓p�[�~�b�V�����ł��B
##
## public_html/
##  |
##  +-- mail_v3/
##        |    mail.cgi   [755/700]  ���[�����M�{�̂b�f�h
##        |    jcode.pl
##        |    stdio.pl
##        |    tpl1.html   ���̓y�[�W
##        |    tpl2.html   �m�F�y�[�W
##        |    tpl3.html   �����y�[�W
##        |    mailtpl_adm.txt   ���[���e���v���[�g�i�Ǘ��҈��āj
##        |    mailtpl_usr.txt   ���[���e���v���[�g�i���[�U���āj
##        |    attention.gif
##        |    style.css
##        |    index.html
##        |
##        +-- data/     [777/705]
##        |      data.cgi  [666/600]   ���͓��e�ۑ��t�@�C��
##        |      index.html
##        |
##        +-- tmp/      [777/705]
##               index.html
##
## �����̓y�[�W��
## http://�ݒu����URL/mail_v3/mail.cgi
## �ƂȂ�܂��B
## tpl1.html �ɒ��ڃA�N�Z�X����ƁA���������삵�܂���̂ŁA�����ӂ��������B
##
##
##*****<< �o�[�W�����A�b�v��� >>******************************************************************
##
## 2008/11/07 .....Ver1.01
##   �E�`�F�b�N�{�b�N�X�A���W�I�{�^���̃t�H�[���^�O��K�{���������ۂɐ��������삵�Ȃ��s����C��
##
##
##*************************************************************************************************


##=====================================
##      �����ݒ蕔�� ��������         =
##=====================================

# �Ǘ��Җ��E���[���A�h���X

$adm_name = 'Studio little';	# �Ǘ��Җ�
$adm_email = 'little.group.little@gmail.com';	# ���[���A�h���X�i��M��ɂȂ�܂��j
#$adm_email = 'aika_i2005@yahoo.co.jp';	# ���[���A�h���X�i��M��ɂȂ�܂��j
# �Z���N�g���j���[�̃��X�g
# ���̓y�[�W�ɃZ���N�g���j���[������ꍇ�A���� name�l�iname="xxx" �� xxx �̕����j���w�肵�Ă��������B

@sel_list = (
	'who','class','what','contact'
);


# ���͕K�{����
# �u'name�l' => '�G���[���̃��b�Z�[�W',�v�̌`�Ŏw�肵�Ă��������B

%hissu = (
	'name'	=>	'�y�����O�z�������͂��������B',
	'kana'	=>	'�y�t���K�i�z�������͂��������B',
	'email'	=>	'�y���[���A�h���X�z�������͂��������B',
	'message'	=>	'�y���\�����݁E���₢���킹���e�z�������͂��������B',
);


# ���[���̌���

$subject_adm = '�yweb�zstudio little ���\�����݁E���₢���킹';	# �Ǘ��҈��ă��[��
$subject_usr = '���₢���킹���肪�Ƃ��������܂�';	# ���[�U���ă��[��


# ���͓��e�ۑ��t�@�C��
# �����p���́AFTP�\�t�g�Ń_�E�����[�h���A�g���q�� .csv �ɕύX������ɂ����p���������B
# �~�ϕۑ����Ă���܂��̂ŁA�e�ʂɋC��t���Ă��������B

$datafile = './data/data.cgi';



# ���͓��e�ꎞ�ۑ��p�f�B���N�g�� ��/�ŏI���Ȃ�
$input_dir = './tmp';

# �e���v���[�gHTML
$html_form1 = './tpl1.html';	# ���̓t�H�[��
$html_form2 = './tpl2.html';	# ���͊m�F
$html_form3 = './tpl3.html';	# ���M����

# ���[���e���v���[�g
$form_mail1 = './mailtpl_adm.txt';	# �Ǘ��҈�
$form_mail2 = './mailtpl_usr.txt';	# ���[�U��

# ���b�N�f�B���N�g��
$lock = './tmp';

# �Â��u���͏���ۑ������t�@�C���v���폜������� ���b�Ŏw��
$expires = '259200';

# �����i�O���j�b�W�W�������p�������h���j��b�Ŏw��
$time_difference = '32400';

# �N�b�L�[ID
$cookie_id = 'MyCookie';


##=====================================
##      �����ݒ蕔�� �����܂�         =
##=====================================



#������������������������ �������牺���C�������ꍇ�ɂ̓T�|�[�g�ΏۊO�ɂȂ�܂��B�����ӂ��������B ������������������������������������������������������������

##=====================================
## �f�[�^���󂯎��
##=====================================
$separator = ' / ';
%param = ();
@keys = stdio::getFormData(\%param, "1", "UTF8", $separator, "", "utf8");
@keys = grep(!$seen{$_}++, @keys);


##=====================================
## �N�b�L�[��ǂݍ���
##=====================================
%COOKIE = ();
stdio::getCookie(\%COOKIE, $cookie_id);
if(!$COOKIE{'id'}){
	if($param{'mode'}){ &error('�G���[','�N�b�L�[���ǂݍ��߂܂���ł����B���̓t�H�[���ɖ߂��Ă��������B'); }
	
	$time = time;
	$random = stdio::getRandomString(4);
	$COOKIE{'id'} = $time."-".$random;
}


##=====================================
## ���͏��ۑ��t�@�C��
##=====================================
$input_datafile = "$input_dir/$COOKIE{'id'}.cgi";


##=====================================
## �Â����͏��ۑ��t�@�C�����폜����
##=====================================
foreach(glob($input_dir."/*.cgi")){
	@stat = stat;
	$time = time;
	$time -= $expires;
	
	if($stat[9] < $time){ unlink; }
}



#���������� ���[�h �Ȃ� �������� ������������������������������������������������������������������������������������������������������������������������
if($param{'mode'} eq ''){

##=====================================
## ���̓G���[�̕\��
##=====================================
if($param{'action'} eq 'err'){
	if(-e $input_datafile){
		foreach(&fileopen($input_datafile)){
			chomp;
			my ($key, $val) = split(/\t/);
			
			if($key eq 'email'){ $email = $val; }
			
			# �K�{�`�F�b�N
			if(($hissu{$key} and $val eq '') or ($hissu{$key} and $val eq 'dummy')){
				$subst{'error_mes'} .= qq|<li>$hissu{$key}</li>|;
				
				# ���[���K�{�`�F�b�N�ς�
				$email_checked = 1;
			}
			
			# ���[���̃`�F�b�N
			if($key eq 'email' and !$email_checked){
				$string_result = &InputCheck($val, "1", "255");
				if($string_result){
					$subst{'error_mes'} .= qq|<li>�y���[���A�h���X�z�̓��͂�����Ă��܂��B</li>|;
				}
			}
			if($key eq 'email2'){
				if($email ne $val){
					$subst{'error_mes'} .= qq|<li>�y���[���A�h���X�z�Ɓy���[���A�h���X�m�F�p�z�̓��͂��قȂ��Ă��܂��B</li>|;
				}
			}
		}
	}
}

if($subst{'error_mes'}){
	$subst{'error_display'} = 'display: block;';
}


##=====================================
## ���͏��𕜌�
##=====================================
# �Z���N�g���j���[�̃��X�g
foreach(@sel_list){
	$sel{$_} = $_;
}

# ����
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
	if(!$subst{$_}){ $subst{$_} = qq|<option value="" selected="selected">���I�щ�����</option>\n|; }
}


##=====================================
## HTML����
##=====================================
$subst{'copyright'} = qq|<div style="clear:both; width:100%; text-align:right; font-size:12px;">- <a href="http://www.d-ic.com/" target="_blank">���[�����MCGI�F DIC-Studio</a> -</div>|;
foreach(&fileopen($html_form1)){
	if(/_%copyright%_/){
		$c_flag = 1;
		last;
	}
}
if(!$c_flag){ &error('�G���[', '���쌠�\�����폜����Ă��܂��B'); }

$htmldata = &dicTag(&fileopen($html_form1));


##=====================================
## �g�s�l�k�o��
##=====================================
print "Content-type: text/html\n";

stdio::setCookie(\%COOKIE, $cookie_id);

print <<"EOF";

$htmldata
EOF
exit;
}	# ���[�h �Ȃ� �����܂�



#���������� ���[�h check �������� ������������������������������������������������������������������������������������������������������������������������
elsif($param{'mode'} eq 'check'){

##=====================================
## ���͏��ۑ��t�@�C���ɏ�������
##=====================================
foreach(@keys){
	$param{$_} =~ s/\n/<br \/>/g;
	push(@inputdata, "$_\t$param{$_}\n");
}

if(!open(DATA,">$input_datafile")){ stdio::unlock($lock); &error('�V�X�e���G���[',"���͓��e�ꎞ�ۑ��t�@�C���𐶐��ł��܂���ł����B"); }
seek(DATA,0,0);
print DATA @inputdata;
truncate(DATA,tell(DATA));
close(DATA);


##=====================================
## ���̓`�F�b�N
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
## �u���p
##=====================================
foreach(@keys){
	@tmp = ();
	if($_ eq 'mode'){ next; }
	
	$param{$_} =~ s/\n/<br \/>/g;
	
	# dummy�̍폜
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
## HTML����
##=====================================
$subst{'copyright'} = qq|<div style="clear:both; width:100%; text-align:right; font-size:12px;">- <a href="http://www.d-ic.com/" target="_blank">���[�����MCGI�F DIC-Studio</a> -</div>|;
foreach(&fileopen($html_form2)){
	if(/_%copyright%_/){
		$c_flag = 1;
		last;
	}
}
if(!$c_flag){ &error('�G���[', '���쌠�\�����폜����Ă��܂��B'); }

$htmldata = &dicTag(&fileopen($html_form2));


##=====================================
## �g�s�l�k�o��
##=====================================
print <<"EOF";
Content-type: text/html

$htmldata
EOF
exit;
}	# ���[�h check �����܂�



#���������� ���[�h send �������� ������������������������������������������������������������������������������������������������������������������������
elsif($param{'mode'} eq 'send'){

##=====================================
## ���b�N
##=====================================
if(!stdio::lock($lock)){ &error('ERROR','Busy!'); }


##=====================================
## CSV�t�@�C���ɏ�������
##=====================================
if(!open(DATA,"+<$datafile")){ stdio::unlock($lock); &error('�V�X�e���G���[',"���͓��e�ۑ��t�@�C���������݃I�[�v���ł��܂���ł����B"); }
@db = <DATA>;

# ���ݓ���
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
## �A�����b�N
##=====================================
stdio::unlock($lock);


##=====================================
## ���[�����ʒu���p
##=====================================
foreach(@keys){
	$param{$_} =~ s/&lt;br \/&gt;/\n/g;
	
	# %subst
	$subst{$_} = $param{$_};
}


##=====================================
## ���[�����͂𐶐�
##=====================================
$mailbody_adm = &dicTag(&fileopen($form_mail1));
$mailbody_usr = &dicTag(&fileopen($form_mail2));


##=====================================
## ���[�����M�i�Ǘ��҈��j
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
## ���[�����M�i���[�U���j
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
## �ꎞ�t�@�C���폜
##=====================================
unlink $input_datafile;


##=====================================
## HTML����
##=====================================
$subst{'copyright'} = qq|<div style="clear:both; width:100%; text-align:right; font-size:12px;">- <a href="http://www.d-ic.com/" target="_blank">���[�����MCGI�F DIC-Studio</a> -</div>|;
foreach(&fileopen($html_form3)){
	if(/_%copyright%_/){
		$c_flag = 1;
		last;
	}
}
if(!$c_flag){ &error('�G���[', '���쌠�\�����폜����Ă��܂��B'); }

$htmldata = &dicTag(&fileopen($html_form3));


##=====================================
## �g�s�l�k�o��
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
}	# ���[�h send �����܂�





##=====================================
## ����^�O�̒u������
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
## ���͕����̃`�F�b�N
##=====================================
sub InputCheck { # ($param{'email'}, $type ,$maxlength)
	# $type  1=email  2=�d�b��t�@�b�N�X��
	# $maxlength  �ő�o�C�g��
	
# �T���v���i�d���[���`�F�b�N�j
#$string_result = &InputCheck($emailaddress, "1", "255");
#if($string_result){
#	&error('error','E���[���A�h���X�̓��͂�����Ă��܂��B');
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
## �t�@�C���I�[�v��
##=====================================
sub fileopen { # ($filepath)
	local($file) = @_;
	local(@array);
	
	if(!open(IN,$file)){
		stdio::unlock($lock);
		&error('�V�X�e���G���[',"�t�@�C���i$file�j���I�[�v���ł��܂���ł����B"); }
	@array = <IN>;
	close(IN);
	
	return (@array);
}


##=====================================
## �G���[�\��
##=====================================
sub error { # ($error_tile, $error_message)
	
	# ���b�N����
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
	font-family: "Verdana", "Helvetica","�l�r �S�V�b�N", "Osaka�|����";
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
        <td><a href="javascript:history.back()">�R�`�����N���b�N</a>���邩�A�u���E�U�̖߂�{�^�����N���b�N���đO�̉�ʂɈړ����Ă��������B</td>
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
