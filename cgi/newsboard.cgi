#!/usr/bin/perl

##======================================================##
##  AmigoNewsBoard [更新情報ボード]                     ##
##  Copyright(C)2000 cgi-amigo.com All Rights Reserved  ##
##  http://www.cgi-amigo.com/                           ##
##  mail:webmaster@cgi-amigo.com                        ##
##======================================================##

# このスクリプトは無料でご利用頂けますが著作権は放棄していません。
# 利用規定ファイル及びhttp://www.cgi-amigo.com/kitei.htmlの利用規定を厳守してご利用下さい。
# 更新の都合で両規定に違いがある場合はより新しい方の規定をご覧下さい。

###############################################################################

# ■基本設定ファイル
$SetupFile='./n-setup.cgi';

###############################################################################

$Ver='2.25';
$ClenMax=50000;
srand(time()^($$+($$<<15)));
$PID=$$?$$:int(rand(10000)+1);
$NowTime=time;
$Copyright=qq(<CENTER><TABLE height="10"><TBODY><TR><TD></TD></TR></TBODY></TABLE><TABLE border="1" bgcolor="#ffffff"><TBODY><TR><TD align=middle><FONT style="FONT-SIZE: 10pt" face=verdana,arial,serif,tahoma>&nbsp;- <A href="http://www.cgi-amigo.com/" style="color : blue;">AmigoNewsBoard</A> -&nbsp;</FONT></TD></TR></TBODY></TABLE></CENTER>);
$SIG{INT}=$SIG{HUP}=$SIG{QUIT}=$SIG{TERM}=$SIG{__WARN__}=\&SIGExit;
$DomainName=!$ENV{REMOTE_HOST}||$ENV{REMOTE_HOST}eq$ENV{REMOTE_ADDR}?gethostbyaddr(pack('C4',split(/\./,$ENV{REMOTE_ADDR})),2)||$ENV{REMOTE_ADDR}:$ENV{REMOTE_HOST};
%REC=('DataNum'=>0,'Rtime'=>1,'Title'=>2,'Url'=>3,'Genre'=>4,'Comment'=>5);
&Lrequire('./lib/jcode.pl');
&Lrequire($SetupFile);
&GetFormData;
@cmd{'nl','dj','ac','ar','dr','dra','de','uo','uoa','lc','s','sa','lt'}='';
($FORM{cmd} eq '') and $FORM{cmd}='nl';
!exists$cmd{$FORM{cmd}}?&Error('コマンドが不正です。'):&{$FORM{cmd}};

###############################################################################

################
#   Lrequire   #
################
sub Lrequire{ my$lib=shift;
my$name=(split/\//,$lib)[-1];
eval{ require"$lib" } or &Die("$nameを呼び出せません。");}

###############################################################################

################
#   Location   #
################
sub Location{ my$url=shift;
if(!$LocationType){ print"Location: $url\n\n" }
else{ print"Content-type: text/html\n\n";
    print qq(<HTML><HEAD><META HTTP-EQUIV="REFRESH" CONTENT="0;URL=$url"></HEAD></HTML>);
}exit;}

###############################################################################

###################
#   GetFormData   #
###################
sub GetFormData{ my$buff;
if($ENV{REQUEST_METHOD} eq 'POST'){
    ($ENV{CONTENT_LENGTH} > $ClenMax) and &Error('送信データが大きすぎます。');
    read(STDIN,$buff,$ENV{CONTENT_LENGTH});
}else{ $buff=$ENV{QUERY_STRING} }
foreach(split(/&/,$buff)){
    ($key,$val)=split(/=/,$_,2);
    $key=&UrlDecode($key);
    $val=&UrlDecode($val);
    jcode::convert(*val,'sjis');
    $val=&TagEncode($val);
    $val=~s/\t//g;
    $val=~s/(?:\r\n|\r)/\n/g;
    if($FORM{$key} ne '' and $val ne ''){
        $FORM{$key}.="\0";
        $divided{$key}=1;
    }else{ push(@keys,$key) }
    $FORM{$key}.=$val;
}foreach(keys%divided){
    $FORM{$_}=~s/,/，/g;
    $FORM{$_}=~s/\0/,/g;
}}

###############################################################################

#################
#   UrlDecode   #
#################
sub UrlDecode{ my$buff=shift;
$buff=~tr/+/ /;
$buff=~s/%([0-9a-fA-F]{2})/chr(hex($1))/eg; $buff;}

#################
#   UrlEncode   #
#################
sub UrlEncode{ my$buff=shift;
$buff=~s/([^ ])/sprintf('%%%02X',ord($1))/eg;
$buff=~tr/ /+/; $buff;}

###############################################################################

#################
#   TagEncode   #
#################
sub TagEncode{ my$buff=shift;
$buff=~s/</&lt;/g;
$buff=~s/>/&gt;/g;
$buff;}

#################
#   TagDecode   #
#################
sub TagDecode{ my$buff=shift;
$buff=~s/&lt;/</g;
$buff=~s/&gt;/>/g;
$buff;}

###############################################################################

############
#   Html   #
############
sub Html{ my$file=shift;
($file=~/^\//) and &Error('テンプレートの指定が不正です。');
($file=~/\.\./) and &Error('テンプレートの指定が不正です。');
print"Content-Type: text/html\n\n";
eval{ require"./lib/template/$file" } or &Die("$fileを呼び出せません。",1);
print$Copyright;exit;}

###############################################################################

###############
#   SIGExit   #
###############
sub SIGExit{ &Unlock('ALL'); exit(1);}

#############
#   Error   #
#############
sub Error{ $msg=shift;
&Unlock('ALL');
&Html('error.html');}

################
#   Complete   #
################
sub Complete{ $msg=shift;
&Html('complete.html');}

###########
#   Die   #
###########
sub Die{ my($msg,$NoHead)=@_;
$NoHead or print"Content-type: text/html\n\n";
print$msg;exit;}

###############################################################################

#################
#   SetCookie   #
#################
sub SetCookie{ my($cookname,$cookval,$cookexp)=@_;
my$expires;
if($cookexp){
    my@Month=(Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov,Dec);
    my@Week=(Sun,Mon,Tue,Wed,Thu,Fri,Sat);
    my($sec,$min,$hour,$mday,$mon,$year,$wday)=gmtime(time+$cookexp*86400);
    $expires=sprintf("%s, %02d-%s-%04d %02d:%02d:%02d GMT",$Week[$wday],$mday,$Month[$mon],$year+1900,00,00,00);
}$cookname=&UrlEncode($cookname);
$cookval=&UrlEncode($cookval);
print"Set-Cookie: $cookname=$cookval; expires=$expires\n"; 1;}

#################
#   GetCookie   #
#################
sub GetCookie{ my$cookname=shift;
foreach(split(/;/,$ENV{HTTP_COOKIE})){
    $_=&UrlDecode($_);
    my($key,$val)=split(/=/);
    $key=~s/\s//g;
    $buff{$key}=$val;
}foreach(split(/\,/,$buff{$cookname})){
    my($key,$val)=split(/<>/);
    $val=&TagEncode($val);
    $COOKIE{$key}=$val;
}1;}

###############################################################################

############
#   Lock   #
############
sub Lock{ my($n,$lax)=@_;
my$lock="$LockDir/$n.loc";
if($LockType==1){
    open($n,">$lock");
    flock($n,2);
    $LockFile{$n}=1; return(1);
}elsif($LockType==2){
    my$locking="$LockDir/$n.now";
    if(-e$locking and $NowTime-(stat(_))[9]>180){ rename($locking,$lock) }
    for($_=5; $_>=0; $_--){
        if(rename($lock,$locking)){
            utime($NowTime,$NowTime,$locking);
            $LockFile{$n}=1; return(1);
        }sleep(1) if$_;
    }$lax?return(0):&Error('只今ビジー状態です。<BR>しばらく待ってから再度実行して下さい。');
}elsif($LockType==3){
    if(-e$lock and $NowTime-(lstat(_))[9]>180){ unlink$lock }
    for($_=5; $_>=0; $_--){
        if(symlink(".",$lock)){ $LockFile{$n}=1; return(1); }
        sleep(1) if$_;
    }$lax?return(0):&Error('只今ビジー状態です。<BR>しばらく待ってから再度実行して下さい。');
}elsif($LockType==4){
    my$ldir="$LockDir/$n";
    my$ldir2="$LockDir/del";
    for($_=5; $_>=0; $_--){
        if(mkdir($ldir,0755)){ $LockFile{$n}=1; return(1); }
        if($_==0){
            if(mkdir($ldir2,0755)){
                if((-M$ldir)*86400 > 180){
                    if(rename($ldir2,$ldir)){ $LockFile{$n}=1; return(1); }
                    else{ rmdir($ldir2) }
                }else{ rmdir($ldir2) }
            }
        }else{ sleep(1) }
    }$lax?return(0):&Error('只今ビジー状態です。<BR>しばらく待ってから再度実行して下さい。');
}elsif($LockType==5){
    for($_=5; $_>=0; $_--){
        if(!-e$lock){
            open(LOCK,">$lock");
            close(LOCK);
            $LockFile{$n}=1; return(1);
        }if($_){ sleep(1) }
        else{
            if((-M$lock)*86400 > 180){
                open(LOCK,">$lock");
                close(LOCK);
                $LockFile{$n}=1; return(1);
            }
        }
    }$lax?return(0):&Error('只今ビジー状態です。<BR>しばらく待ってから再度実行して下さい。');
}}

##############
#   Unlock   #
##############
sub Unlock{ my$n=shift;
if($n eq 'ALL'){
    foreach(keys%LockFile){
        $LockFile{$_}!=1 and next;
        if($LockType==1){ close($_) }
        elsif($LockType==2){ rename("$LockDir/$_.now","$LockDir/$_.loc") }
        elsif($LockType==3){ unlink("$LockDir/$_.loc") }
        elsif($LockType==4){ rmdir("$LockDir/$_") }
        elsif($LockType==5){ unlink("$LockDir/$_.loc") }
        delete($LockFile{$_});
    }
}else{
    if($LockFile{$n}==1){
        if($LockType==1){ close($n) }
        elsif($LockType==2){ rename("$LockDir/$n.now","$LockDir/$n.loc") }
        elsif($LockType==3){ unlink("$LockDir/$n.loc") }
        elsif($LockType==4){ rmdir("$LockDir/$n") }
        elsif($LockType==5){ unlink("$LockDir/$n.loc") }
        delete($LockFile{$n});
    }
}}

################
#   LockTest   #
################
sub LockTest{ my$type;
eval{ open(TEST,">$LockDir/test.loc");
    flock(TEST,2);
    close(TEST);
    unlink("$LockDir/test.loc");
} and $type.='flock式ロックが利用できます。<BR>';
eval{ open(TEST,">$LockDir/test.loc");
    close(TEST);
    rename("$LockDir/test.loc","$LockDir/test2.loc");
    unlink("$LockDir/test2.loc");
} and $type.='rename式ロックが利用できます。<BR>';
eval{ symlink(".","$LockDir/test.loc");
    unlink("$LockDir/test.loc");
} and $type.='symlink式ロックが利用できます。<BR>';
eval{ mkdir("$LockDir/test",0755);
    rename("$LockDir/test","$LockDir/test2");
    rmdir("$LockDir/test2");
} and $type.='mkdir式ロックが利用できます。<BR>';
$type.='open式ロックが利用できます。<BR>';
&Die($type);}

###############################################################################

##############
#   Secure   #
##############
sub Secure{ my($ref,$method,$admin,$sid,$proxy,$domain,$vip,$lax)=@_;
if($ref){ undef$found;
    if($ENV{HTTP_REFERER} eq ''){
        if($ENV{HTTP_USER_AGENT}=~/^DoCoMo/){ $found=1 }
        else{ $found=0 }
    }else{ foreach(@MyUrl){ if($ENV{HTTP_REFERER}=~/^\Q$_\E/){ $found=1; last } } }
    (!$found) and $lax?return(0):&Error('設置サイト外からの呼び出しです。');
}&MethodCheck if($method);
&AdminCheck if($admin ne '');
&SidCheck($sid) if($sid and $SidChkMode);
1;}

###############################################################################

###################
#   MethodCheck   #
###################
sub MethodCheck{ &Error('METHOD形式が不正です。<BR>POST形式でのみ送信できます。') if($ENV{REQUEST_METHOD} !~ /POST/i); 1;}

##################
#   AdminCheck   #
##################
sub AdminCheck{
if($AdminPass ne ''){
    if($CryptMode){ &Error('管理用パスワードが違います。') if(crypt($FORM{AdminPass},$AdminPass) ne $AdminPass) }
    else{ &Error('管理用パスワードが違います。') if($FORM{AdminPass} ne $AdminPass) }
}1;}

################
#   SidCheck   #
################
sub SidCheck{ my$dir=shift; local(*id);
&FileRead("$dir/submit.dat",*id,1);
($id eq $FORM{SID}) and &Error('同一内容の２重送信です。<BR>送信ボタンは１度だけ押すようにして下さい。'); 1;}

################
#   FileRead   #
################
sub FileRead{ local($file,*line,$type,$name)=@_;
if(!open(FILE,$file)){
    ($name eq '') and $name=(split/\//,$file)[-1];
    &Error("$nameが開けません。");
}if($type){ $line=<FILE> }
else{ @line=<FILE> }
close(FILE);}

#################
#   FileWrite   #
#################
sub FileWrite{ my($file,$data,$open,$name)=@_;
if($open){
    if(!open(FILE,">>$file")){
        ($name eq '') and $name=(split/\//,$file)[-1];
        &Error("$nameが開けません。");
    }
}else{ open(FILE,">$file") }
if(ref$data eq 'ARRAY'){ print FILE @{$data} }
elsif(ref$data eq 'HASH'){ foreach(values%{$data}){ print FILE $_ } }
else{ print FILE $data }
close(FILE);}

###################
#   PageViewSet   #
###################
sub PageViewSet{ my($hit,$hyojisu)=@_;
if($hit<=$hyojisu){ $PageSu=1; $Start=0; $End=$hit-1; }
else{ $PageSu=int($hit/$hyojisu);
    if($hit % $hyojisu){ $PageSu++ }
    $Start=$hyojisu*($FORM{Page}-1);
    if($FORM{Page}==1){ $End=$hyojisu-1 }
    elsif($FORM{Page}==$PageSu){ $End=$hit-1 }
    else{ $End=$Start+$hyojisu-1 }
}}

###############
#   GetDate   #
###############
sub GetDate{ my($time,$format)=@_;
($sec,$min,$hour,$mday,$mon,$year,$wday)=gmtime($time+$TimeZone*3600);
my@mon=qw(Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec);
my@jwday=qw(日 月 火 水 木 金 土);
my@ewday=qw(Sun Mon Tue Wed Thu Fri Sat);
$year+=1900; $mon++;
if($format ne ''){
    $format=~s/{yyyy}/$year/ or
        $format=~s/{yy}/substr($year,2,4)/e or
        $format=~s/{y}/'平成'.($year-1988)/e;
    $format=~s/{mmm}/$mon[$mon-1]/ or
        $format=~s/{mm}/sprintf('%02d',$mon)/e or
        $format=~s/{m}/$mon/;
    $format=~s/{dd}/sprintf('%02d',$mday)/e or
        $format=~s/{d}/$mday/;
    $format=~s/{ww}/$jwday[$wday]/ or
        $format=~s/{w}/$ewday[$wday]/;
    $format=~s/{HH}/$hour<12?'午前':'午後'/e or
        $format=~s/{H}/$hour<12?'AM':'PM'/e;
    $format=~s/{hhhh}/sprintf('%02d',$hour)/e or
        $format=~s/{hhh}/$hour/ or
        $format=~s/{hh}/sprintf('%02d',($hour>11?$hour-12:$hour))/e or
        $format=~s/{h}/($hour>11?$hour-12:$hour)/e;
    $format=~s/{nn}/sprintf('%02d',$min)/e or
        $format=~s/{n}/$min/;
    $format=~s/{ss}/sprintf('%02d',$sec)/e or
        $format=~s/{s}/$sec/;
}$format;}

################
#   AutoLink   #
################
sub AutoLink{ my$buff=shift;
my$url='[\w\.\~\-\_\/\?\=\&\+\:\@\%\;\#\%]+';
my$mail='[\w\'-\*\,-\.\_]+';
$buff=~s/((?:s?https?|ftp):\/\/$url\.$url)/<A href=\"$1\" target=\"$AutoTarget\">$1<\/A>/gio;
$buff=~s/($mail\@$mail\.$mail)/<A href="mailto:$1">$1<\/A>/gio;
$buff;}

##################
#   UnAutoLink   #
##################
sub UnAutoLink{ my$buff=shift;
$buff=~s/<A href="(?:mailto:)?([^"]+)"(?: target="$AutoTarget")?>\1<\/A>/$1/gio;
$buff;}

###################
#   PageControl   #
###################
sub _PageControl{
print qq(<TABLE border=0 cellspacing=0 cellpadding=0><TR align="center"><TD><A href="$BaseDir/$MainCGI?No=$FORM{No}&Num=$FORM{Num}&Page=1"><IMG src="$ImageDir/top.gif" border=0 alt="Top"></A> );
if($PageSu>=3 and $FORM{Page}>=3){
    $MovePage=$FORM{Page}-2;
    print qq(<A href="$BaseDir/$MainCGI?No=$FORM{No}&Num=$FORM{Num}&Page=$MovePage"><IMG src="$ImageDir/back2.gif" border=0 alt="Back"></A> )
}else{ print qq(<IMG src="$ImageDir/back2.gif" border=0> ) }
if($PageSu>=2 and $FORM{Page}>=2){
    $MovePage=$FORM{Page}-1;
    print qq(<A href="$BaseDir/$MainCGI?No=$FORM{No}&Num=$FORM{Num}&Page=$MovePage"><IMG src="$ImageDir/back.gif" border=0 alt="Back"></A>);
}else{ print qq(<IMG src="$ImageDir/back.gif" border=0>) }
print qq(</TD><TD class="PageNum">&nbsp;[$FORM{Page}/$PageSu]&nbsp;</TD><TD>);
if($PageSu>=2 and $FORM{Page}!=$PageSu){
    $MovePage = $FORM{Page}+1;
    print qq(<A href="$BaseDir/$MainCGI?No=$FORM{No}&Num=$FORM{Num}&Page=$MovePage"><IMG src="$ImageDir/next.gif" border=0 alt="Next"></A> );
}else{ print qq(<IMG src="$ImageDir/next.gif" border=0> ) }
if($PageSu>=3 and $FORM{Page}+2<=$PageSu){
    $MovePage=$FORM{Page}+2;
    print qq(<A href="$BaseDir/$MainCGI?No=$FORM{No}&Num=$FORM{Num}&Page=$MovePage"><IMG src="$ImageDir/next2.gif" border=0 alt="Next"></A> );
}else{ print qq(<IMG src="$ImageDir/next2.gif" border=0> ) }
print qq(<A href="$BaseDir/$MainCGI?No=$FORM{No}&Num=$FORM{Num}&Page=$PageSu"><IMG src="$ImageDir/last.gif" border=0 alt="Last"></A></TD></TR></TABLE>);}

###############################################################################

################
#   NewsList   #
################
sub nl{ @MyUrl and $LinkChkMode and &Secure(1);
my$file=$FORM{No}?"$DataDir/old/$FORM{No}.dat":"$DataDir/news.cgi";
&FileRead($file,*NewsLines);
$Num=$FORM{Num}-1; $l=-1;
foreach(0..$#NewsLines){
    my@tmp=split(/<>/,$NewsLines[$_]);
    ($tmp[$REC{Title}] eq '') and next; $l++;
    @{$NEWS{$tmp[$REC{DataNum}]}}=@tmp;
    if($l==$Num){ unshift(@NewsNums,$tmp[$REC{DataNum}]); next; }
    push(@NewsNums,$tmp[$REC{DataNum}]);
}$FORM{Page}=1 unless($FORM{Page});
&GetCookie("AmigoNewsBoard(UserOption)") if($CookieMode);
$FORM{View}=$COOKIE{NView} if($COOKIE{NView});
$FORM{View}=$DefaultNView if(!$FORM{View} or $NViewFixedMode or $FORM{View} > $MaxNView);
&PageViewSet(scalar@NewsNums,$FORM{View});
&Html('news.html');}

#################
#   NewsPrint   #
#################
sub _NewsPrint{
foreach($Start..$End){
    @VD=@{$NEWS{$NewsNums[$_]}};
    $VD[$REC{Rtime}]=&GetDate($VD[$REC{Rtime}],'{yyyy}/{mm}/{dd}({w}) {hhhh}:{nn}:{ss}');
    $VD[$REC{Url}]=($VD[$REC{Url}] eq '' or $VD[$REC{Url}]=~/\D/) ? $VD[$REC{Url}] : $GENRE{$VD[$REC{Url}]}[1];
    &_Html_List;
    push(@NumList,$VD[$REC{DataNum}]);
}}

###############
#   EditNum   #
###############
sub _EditNum{ map{ print qq(<OPTION value="$_">No.$_</OPTION>) }@NumList }

##################
#   DirectJump   #
##################
sub dj{ @MyUrl and $LinkChkMode and &Secure(1);
&FileRead("$DataDir/news.cgi",*NewsLines);
undef$found; $i=0;
foreach(0..$#NewsLines){
    @tmp=split(/<>/,$NewsLines[$_]);
    ($tmp[$REC{Title}] eq '') and next; $i++;
    if($i eq $FORM{Num}){ $found=1; last; }
}($found) and $url=($tmp[$REC{Url}] eq '' or $tmp[$REC{Url}]=~/\D/)?$tmp[$REC{Url}]:$GENRE{$tmp[$REC{Url}]}[1];
($url eq '') and $url=$HomeUrl;
&Location($url);}

####################
#   AdminCertify   #
####################
sub ac{ @MyUrl and $LinkChkMode and &Secure(1);
&Html('certify.html');}

#################
#   AdminRoom   #
#################
sub ar{ &Secure(scalar@MyUrl,$MethodChkMode,'admin');
&Html('room.html');}

##################
#   UserOption   #
##################
sub uo{ @MyUrl and $LinkChkMode and &Secure(1);
&Html('user.html');}

#####################
#   UserOptionAct   #
#####################
sub uoa{ &Secure(scalar@MyUrl,$MethodChkMode);
$FORM{NView}=$DefaultNView unless($FORM{NView});
$FORM{SView}=$DefaultSView unless($FORM{SView});
&SetCookie("AmigoNewsBoard(UserOption)","NView<>$FORM{NView}\,SView<>$FORM{SView}",$CookieExpires) if($CookieMode);
&Complete('ユーザー設定を保存しました。');}

#################
#   LogChange   #
#################
sub lc{ @MyUrl and $LinkChkMode and &Secure(1);
&FileRead("$DataDir/old/index.txt",*IndexLines);
&Html('log-index.html');}

#############
#   Index   #
#############
sub _Index{
foreach(@IndexLines){
    my($LogNo,$StartDate,$EndDate,$StartNum,$EndNum)=split(/<>/);
    my$vn=sprintf("%03d",$LogNo);
    print qq(<TR><TD align="center" class="No"><A href="$BaseDir/$MainCGI?No=$LogNo">$vn</A></TD>);
    $StartDate=&GetDate($StartDate,'{yyyy}/{mm}/{dd}');
    $EndDate=&GetDate($EndDate,'{yyyy}/{mm}/{dd}');
    print qq(<TD align="center" class="Date">$StartDate ～ $EndDate</TD>);
    print qq(<TD align="center" class="Num">$StartNum ～ $EndNum</TD></TR>);
}}

##################
#   NewsSearch   #
##################
sub s{ @MyUrl and $LinkChkMode and &Secure(1);
&Html('search.html');}

#####################
#   NewsSearchAct   #
#####################
sub sa{ &Secure(scalar@MyUrl,$MethodChkMode);
$Stime=$FORM{Term}>0 ? $NowTime-86400*$FORM{Term} : 0;
@STargets=split(/\,/,$FORM{STarget});
$keyword=$FORM{Word};
$keyword=~s/&quot;/\"/g;
$keyword=~s/　/ /g;
$keyword=~s/\t/ /g;
$keyword=~s/^\s+//;
$keyword=~s/\s+$//;
@keyword=split(/ /,$keyword);
my$file=$FORM{No}?"$DataDir/old/$FORM{No}.dat":"$DataDir/news.cgi";
&FileRead($file,*NewsLines);
foreach(@NewsLines){
    my@tmp=split(/<>/);
    last if($Stime > $tmp[$REC{Rtime}]);
    next if($tmp[$REC{Title}] eq '');
    @{$NEWS{$tmp[$REC{DataNum}]}}=@tmp;
    push(@Nums,$tmp[$REC{DataNum}]);
}foreach(@Nums){
    last if($FORM{Max} and $FORM{Max}<=@NewsNums);
    next if($FORM{SGenre} and $FORM{SGenre}!=$NEWS{$_}[$REC{Genre}]);
    undef$STarget;
    foreach$tnum(@STargets){
        if($tnum==3 and $NEWS{$_}[3]!~/\D/){ $NEWS{$_}[3]=$GENRE{$NEWS{$_}[3]}[1] }
        $STarget.="$NEWS{$_}[$tnum]|";
    }$STarget=&TagDecode($STarget);
    if(@keyword){ undef$found;
        foreach$key(@keyword){
            if(index($STarget,$key)>=0){ $found=1; if($FORM{SType} eq 'OR'){ last } }
            else{ if($FORM{SType} eq 'AND'){ $found=0; last } }
        }next unless($found);
    }push(@NewsNums,$_);
}(@NewsNums==0) and &Error('該当するデータが見つかりませんでした。');
$FORM{Page}=1 if($FORM{Page} eq '' or $FORM{MoreSearch});
$FORM{Page}++ if($FORM{NextResult});
$FORM{Page}-- if($FORM{BackResult});
$FORM{Word}=~s/\"/&quot;/g;
&GetCookie("AmigoNewsBoard(UserOption)") if($CookieMode and !$FORM{View});
$FORM{View}=$COOKIE{SView} if($COOKIE{SView});
$FORM{View}=$DefaultSView if(!$FORM{View} or $SViewFixedMode or $FORM{View}>$MaxSView);
&PageViewSet(scalar@NewsNums,$FORM{View});
$Hit=@NewsNums;
&Html('result.html');}

####################
#   PageControl2   #
####################
sub _PageControl2{
if($FORM{Page}>=2){ print qq(<INPUT type="submit" value="前の$FORM{View}件" name="BackResult" style="cursor : hand;"> ) }
if($FORM{Page}<$PageSu){ print qq(<INPUT type="submit" value="次の$FORM{View}件" name="NextResult" style="cursor : hand;">) }}

###################
#   ResultPrint   #
###################
sub _ResultPrint{
foreach($Start..$End){
    @VD=@{$NEWS{$NewsNums[$_]}};
    $VD[$REC{Rtime}]=&GetDate($VD[$REC{Rtime}],'{yyyy}/{mm}/{dd}({w}) {hhhh}:{nn}:{ss}');
    $VD[$REC{Url}]=($VD[$REC{Url}] eq '' or $VD[$REC{Url}]=~/\D/) ? $VD[$REC{Url}] : $GENRE{$VD[$REC{Url}]}[1];
    &_Html_Search;
    push(@NumList,$NewsNums[$_]);
}}

##################
#   NewsRegist   #
##################
sub dr{ &Secure(scalar@MyUrl,$MethodChkMode,'admin');
($RegistTitle,$Type)=('ニュース投稿','New');
&Html('regist.html')}

#################
#   GenreList   #
#################
sub _GenreList{
foreach(sort{$a<=>$b}keys%GENRE){
    if($_==$TD[$REC{Genre}]){ print qq(<OPTION value="$_" selected>$GENRE{$_}[0]</OPTION>) }
    else{ print qq(<OPTION value="$_">$GENRE{$_}[0]</OPTION>) }
}}

################
#   NewsEdit   #
################
sub de{ &Secure(scalar@MyUrl,$MethodChkMode,'admin');
my$file=$FORM{No}?"$DataDir/old/$FORM{No}.dat":"$DataDir/news.cgi";
if($FORM{Delete}){
    &Lock('DATA');
    &FileRead($file,*NewsLines);
    undef$found;
    foreach(0..$#NewsLines){
        my@tmp=split(/<>/,$NewsLines[$_]);
        if($tmp[$REC{DataNum}] eq $FORM{Target}){ $found=1; $Line=$_; @TD=@tmp; last; }
    }($found!=1) and &Error('データが見つかりません。');
    $NewsLines[$Line]="$TD[$REC{DataNum}]<>$TD[$REC{Rtime}]<><><><><>\n";
    &FileRead($TitleFile,*TitleLines);
    undef$found;
    foreach(0..$#TitleLines){
        my@tmp=split(/\'/,$TitleLines[$_]);
        if($FORM{Target} eq $tmp[5]){ $found=1; @tg=@tmp; $Line=$_; last; }
    }if($found){
        $tg[0]=~/^TITLE(\d+)=$/;
        $titlenum=$1-1;
        $sline=$Line+1;
        foreach($sline..$#TitleLines){
            $titlenum++;
            my@tmp=split(/\'/,$TitleLines[$_]);
            $TitleLines[$_]="TITLE$titlenum\=\'$tmp[1]\'\;DATE$titlenum\=\'$tmp[3]\'\;NUM\=\'$tmp[5]\'\;\n";
        }splice(@TitleLines,$Line,1);
    }&FileWrite($file,\@NewsLines);
    &FileWrite($TitleFile,\@TitleLines);
    &FileWrite("$DataDir/submit.dat",$FORM{SID});
    &Unlock('DATA');
    &Complete("No.$TD[$REC{DataNum}]を削除しました。");
}&FileRead($file,*NewsLines);
undef$found;
foreach(0..$#NewsLines){
    my@tmp=split(/<>/,$NewsLines[$_]);
    if($tmp[$REC{DataNum}] eq $FORM{Target}){ $found=1; @TD=@tmp; last; }
}($found!=1) and &Error('データが見つかりません。');
($TD[$REC{Url}]!~/\D/) and $TD[$REC{Url}]='';
foreach(qw(Title Url Genre Comment)){
    if($_ eq 'Comment'){
        $AutoLinkMode and &UnAutoLink($TD[$REC{$_}]);
        $TD[$REC{$_}]=~s/<BR>/\n/g;
    }$TD[$REC{$_}]=~s/"/&quot;/g;
    $TD[$REC{$_}]=&TagEncode($TD[$REC{$_}]);
    $DATA{$_}=$TD[$REC{$_}];
}($RegistTitle,$Type)=('ニュース編集','Edit');
&Html('regist.html');}

###############################################################################

#####################
#   NewsRegistAct   #
#####################
sub dra{ &Secure(scalar@MyUrl,$MethodChkMode,'admin',$DataDir);
($FORM{Title} eq '') and &Error('タイトルが未入力です。');
($FORM{Genre} eq '') and &Error('ジャンルが未入力です。');
($FORM{Comment} eq '') and &Error('コメントが未入力です。');
%PREFORM=%HFORM=%FORM;
foreach(qw(Title Url Genre Comment)){
    if($_ eq 'Comment'){
        $FORM{$_}=&TagConvert($FORM{$_},\%PermitTag,$AutoLinkMode);
        $FORM{$_}=~s/\n/<BR>/g;
    }else{ $FORM{$_}=~s/\n//g }
    $FORM{$_}=~s/<>/&lt;&gt;/g;
}($FORM{Url} eq '' and $FORM{GenreUrl}) and $FORM{Url}=$FORM{Genre};
if($FORM{Preview}==1){
    foreach(qw(Title Url Genre Comment)){
        if($_ eq 'Comment'){
            $PREFORM{$_}=&TagConvert($PREFORM{$_},\%PermitTag,$AutoLinkMode);
            $PREFORM{$_}=~s/\n/<BR>/g;
        }else{ $PREFORM{$_}=~s/\n//g }
        $HFORM{$_}=~s/"/&quot;/g;
    }unless($FORM{Target}){
        &FileRead("$DataDir/news.cgi",*NewsLines);
        $NewsNum=(split/<>/,$NewsLines[0])[$REC{DataNum}];
        $NewsNum++;
    }else{ $NewsNum=$FORM{Target};
        my$file=$FORM{No}?"$DataDir/old/$FORM{No}.dat":"$DataDir/news.cgi";
        &FileRead($file,*NewsLines);
        undef$found;
        foreach(@NewsLines){
            ($num,$NowTime)=split(/<>/,$_);
            if($num eq $FORM{Target}){ $found=1; last; }
        }($found!=1) and &Error('対象データが見つかりません。');
    }$Date=&GetDate($NowTime,'{yyyy}/{mm}/{dd}({w}) {hhhh}:{nn}:{ss}');
    $GenreName=$GENRE{$FORM{Genre}}[0];
    ($FORM{Url} ne '' and $FORM{Url}!~/\D/) and $PREFORM{Url}=$GENRE{$FORM{Genre}}[1];
    &Html('preview.html');
}&Lock('DATA');
if($FORM{Type} eq 'New'){
    &FileRead("$DataDir/news.cgi",*NewsLines);
    &FileRead($TitleFile,*TitleLines);
    $Date=&GetDate($NowTime,'{yyyy}/{mm}/{dd}({w})');
    $num=(split/<>/,$NewsLines[0])[$REC{DataNum}];
    $num++;
    if(@NewsLines>=$MaxNews){
        if($MaxOldFile){
            @OldFiles=glob("$DataDir/old/*.dat");
            &FileRead("$DataDir/old/index.txt",*IndexLines);
            map{ $OldIndex[$_->[0]]="$_->[0]<>$_->[1]<>$_->[2]<>$_->[3]<>$_->[4]<>\n";
                 $IndexNum{$_->[0]}=["$_->[0]","$_->[1]","$_->[2]","$_->[3]","$_->[4]"];
            }map{ [(split/<>/)[0..4]] } @IndexLines;
            $FileSu=@OldFiles+1;
            if(@OldFiles >= $MaxOldFile){
                $DeleteSu=$FileSu-$MaxOldFile;
                foreach(1..$DeleteSu){ unlink"$DataDir/old/$_\.dat" }
                $NewName=0;
                @OldIndex=();
                foreach($DeleteSu+1..@OldFiles){
                    $NewName++;
                    rename("$DataDir/old/$_\.dat","$DataDir/old/$NewName\.dat");
                    push(@OldIndex,"$NewName<>$IndexNum{$_}[1]<>$IndexNum{$_}[2]<>$IndexNum{$_}[3]<>$IndexNum{$_}[4]<>\n");
                }$FileSu=$NewName+1;
            }&FileWrite("$DataDir/old/$FileSu\.dat",\@NewsLines);
            ($StartNum,$StartDate)=split(/<>/,$NewsLines[-1]);
            ($EndNum,$EndDate)=split(/<>/,$NewsLines[0]);
            push(@OldIndex,"$FileSu<>$StartDate<>$EndDate<>$StartNum<>$EndNum<>\n");
            &FileWrite("$DataDir/old/index.txt",\@OldIndex);
        }@NewsLines=();
    }pop(@TitleLines) if(@TitleLines>=$MaxTitle);
    $TitleNum=1;
    foreach(0..$#TitleLines){
        $TitleNum++;
        @SplitTitle=split(/\'/,$TitleLines[$_]);
        $SplitTitle[0]="TITLE$TitleNum\=";
        $SplitTitle[2]="\;DATE$TitleNum\=";
        $TitleLines[$_]=join("\'",@SplitTitle);
    }my$jstitle=$FORM{Title};
    $jstitle=~s/'/’/g;
    unshift(@TitleLines,"TITLE1\=\'$jstitle\'\;DATE1\=\'$Date\'\;NUM\=\'$num\'\;\n");
    unshift(@NewsLines,"$num<>$NowTime<>$FORM{Title}<>$FORM{Url}<>$FORM{Genre}<>$FORM{Comment}<>\n");
    &FileWrite("$DataDir/news.cgi",\@NewsLines);
    &FileWrite($TitleFile,\@TitleLines);
    &FileWrite("$DataDir/submit.dat",$FORM{SID});
    &Unlock('DATA');
    $FORM{Back}='dr';
    &Complete('新規ニュース投稿が完了しました。');
}else{ my$file=$FORM{No}?"$DataDir/old/$FORM{No}.dat":"$DataDir/news.cgi";
    &FileRead($file,*NewsLines);
    undef$found;
    foreach(0..$#NewsLines){
        my@tmp=split(/<>/,$NewsLines[$_]);
        if($tmp[$REC{DataNum}]==$FORM{Target}){ $found=1; $Line=$_; @TD=@tmp; last; }
    }($found!=1) and &Error('対象データが見つかりませんでした。');
    $NewsLines[$Line]="$TD[$REC{DataNum}]<>$TD[$REC{Rtime}]<>$FORM{Title}<>$FORM{Url}<>$FORM{Genre}<>$FORM{Comment}<>\n";
    if($TD[$REC{Title}] ne $FORM{Title}){
        &FileRead($TitleFile,*TitleLines);
        undef$found;
        foreach(0..$#TitleLines){
            @SplitTitle=split(/\'/,$TitleLines[$_]);
            if($FORM{Target} eq $SplitTitle[5]){ $found=1; $Line=$_; last; }
        }if($found){
            my$jstitle=$FORM{Title};
            $jstitle=~s/'/’/g;
            $SplitTitle[1]=$jstitle;
            $TitleLines[$Line]=join("\'",@SplitTitle);
            &FileWrite($TitleFile,\@TitleLines);
        }
    }&FileWrite($file,\@NewsLines);
    &FileWrite("$DataDir/submit.dat",$FORM{SID});
    &Unlock('DATA');
    &Complete("No.$FORM{Target}の編集が完了しました。");
}}

################################################################################

##################
#   TagConvert   #
##################
sub TagConvert{ my($buff,$permit,$link)=@_;
my(@buff,$tag,$text,$TagTmp,$TagName,$property,@OpenTag,$PropertyTmp,$pname,$pval,$found,$CloseTag);
$buff=&TagDecode($buff);
@buff=split(/(<[^>]*>)/,$buff,-1);
$buff=&TagEncode(shift@buff);
$buff=&AutoLink($buff) if($link);
while(($tag,$text)=splice(@buff,0,2)){
    $text=&TagEncode($text);
    $TagTmp=$tag;
    $tag=~s/\n//g;
    if($tag=~/^<(\w+)\s*([^>]*)>$/){
        $TagName=uc$1;
        $property=$2;
        if(exists${$permit}{$TagName}){
            push(@OpenTag,$TagName) if(${$permit}{$TagName}==1);
            undef$PropertyTmp;
            $property=~s/\'/\"/g;
            while($property=~/[\s]*?([^=\W]+)(=[\s]*?(?:"([^"]*)"|([^ ]+)))?/g){
                if($2 ne ''){ $pname=$1;
                    $pval=$3 ne ''?$3:$4;
                    next if($pname !~ /^[\s]*?(?:$TagProperty{$TagName})[\s]*?$/i);
                    $pval=~s/"//g;
                    $PropertyTmp.=qq( $pname="$pval");
                }
            }$tag="<$TagName$PropertyTmp>";
        }else{ $tag=&TagEncode($TagTmp) }
    }elsif($tag=~/^<\/(\w+)>$/){
        $TagName=uc$1;
        undef$tag;
        undef$found;
        foreach(@OpenTag){ if($TagName eq $_){ $found=1; last } }
        if($found){
            while($CloseTag=pop(@OpenTag)){
                $tag.="</$CloseTag>";
                last if($TagName eq $CloseTag);
            }
        }else{ $tag=&TagEncode($TagTmp) }
    }else{ $tag=&TagEncode($TagTmp) }
    if($link){ undef$found;
        foreach(@OpenTag){ if($_ eq 'A'){ $found=1; last } }
        $text=&AutoLink($text) unless($found);
    }$buff.="$tag$text";
}foreach(@OpenTag){ $buff.="</$_>" } $buff;}

################################################################################
