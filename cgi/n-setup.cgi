package main;

##======================================================##
##  AmigoNewsBoard�p��{�ݒ�t�@�C��                    ##
##  Copyright(C)2000 cgi-amigo.com All Rights Reserved  ##
##  http://www.cgi-amigo.com/                           ##
##  webmaster@cgi-amigo.com                             ##
##======================================================##

# ���̃X�N���v�g�͖����ł����p�����܂������쌠�͕������Ă��܂���B
# �����̗��p�K��t�@�C��(kitei.txt)�̗��p�K�������̏ゲ���p�������B
# �t�@�C���𕴎������ꍇ��http://www.cgi-amigo.com/kitei.html��育�m�F�������B
# �ŐV�o�[�W������http://www.cgi-amigo.com/��育�m�F�����܂��B

###########################################################

# ���Ǘ��p�p�X���[�h
$AdminPass='hudou802';

# ����{�f�B���N�g��
$BaseDir='http://studiolittle.info/cgi';

# ���ݒu�T�C�g�̍ŒZURL
@MyUrl=('http://studiolittle.info/');

# ���j���[�X�y�[�W���ւ̃����N����(ON=1/OFF=0)
$LinkChkMode=0;

# ���z�[��(�߂��)��URL
$HomeUrl='http://studiolittle.info/';

# ���f�[�^�f�B���N�g��
$DataDir='./data';

# ���摜�f�B���N�g��
$ImageDir='./image';

# �����b�N�f�B���N�g��
$LockDir='./lock';

# �����b�N�^�C�v(1=flock��/2=rename��/3=symlink��/4=mkdir��/5=open��)
$LockType=4;

# �����C���X�N���v�g��
$MainCGI='newsboard.cgi';

# ���L���^�C�g���t�@�C��(title.js)�̃p�X
$TitleFile='./title.js';

# �����[�U�[�ݒ��L���ɂ���(ON=1/OFF=0)
$CookieMode=0;

# ���N�b�L�[�L������(��)
$CookieExpires=120;

# ���f�t�H���g�j���[�X�\������
$DefaultNView=20;

# ���j���[�X�\���������f�t�H���g�ɌŒ�(ON=1/OFF=0)
$NViewFixedMode=0;

# ���ő�j���[�X�\������
$MaxNView=50;

# ���f�t�H���g�������ʕ\������
$DefaultSView=20;

# ���������ʕ\���������f�t�H���g�ɌŒ�(ON=1/OFF=0)
$SViewFixedMode=0;

# ���ő匟�����ʕ\������
$MaxSView=50;

# ���I�[�g�����N�@�\(ON=1/OFF=0)
$AutoLinkMode=1;

# ���I�[�g�����N�̃^�[�Q�b�g
$AutoTarget='_blank';

# ���g�p�\�^�O(���Ȃ��^�O=0/����^�O=1)
%PermitTag=('A'=>1,'B'=>1,'FONT'=>1,'I'=>1,'U'=>1,'PRE'=>1,'HR'=>0,'IMG'=>0);

# ���g�p�\�^�O����
%TagProperty=(
'A'=>'href|target',
'FONT'=>'color|face',
'IMG'=>'src|border',
);

# ���ő�j���[�X����(1�t�@�C��)
$MaxNews=200;

# ���ő�^�C�g������
$MaxTitle=10;

# ���ߋ����O�ő�t�@�C����
$MaxOldFile=10;

# ����Q�d���M�h�~�@�\(ON=1/OFF=0)
$SidChkMode=1;

# ��method�`���`�F�b�N(ON=1/OFF=0)
$MethodChkMode=1;

# ���W�����v�^�C�v(0=Location/1=META)
$LocationType=0;

# �������C��(���{��+9)
$TimeZone=+9;

# ���W�������ݒ�
%GENRE=(
1=>['�g�s�b�N','http://'],
);

###########################################################

# =====================�L���f�U�C���ݒ�========================

###########################
#   �L��1�����̃f�U�C��   #
###########################
sub _Html_List{ print <<EOM;
<TABLE width="100%" cellPadding=0 cellSpacing=0>
<TR><TD bgcolor="#FF9999">&nbsp;$VD[$REC{Title}]</TD></TR>
<TR><TD class="Status">&nbsp;No: $VD[$REC{DataNum}] /&nbsp;Genre: $GENRE{$VD[$REC{Genre}]}[0]&nbsp;/&nbsp;Date: $VD[$REC{Rtime}]</TD></TR></TABLE><BR>
<BLOCKQUOTE class="Comment">$VD[$REC{Comment}]<BR><BR><A href="$VD[$REC{Url}]">$VD[$REC{Url}]</A></BLOCKQUOTE>
EOM
}

#####################################
#   �L��1�����̃f�U�C��(��������)   #
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
