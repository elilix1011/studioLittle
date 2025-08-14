package stdio;

;# <stdio.pl> CGI STandarD Input Output - Perl Library.
;#   Version 9.07 (Updated at August 23, 2004)
;#   Copyright(C)1998-2004 WEB POWER. All Rights Reserved.
;#   The latest programs are found at <http://www.webpower.jp/>

;$version  = 'stdio.pl/9.07';     # Version information about 'stdio.pl'.
;$max_byte = 5242880;             # Maximum bytes to accept by multipart/form-data.
;$ses_byte = 1024;                # Record bytes of setSession/getSession function.
;$sendmail = '/usr/sbin/sendmail'; # Path of 'sendmail' program.
;$tmp_dir  = '/tmp/';             # Path of directory for temporary files. (chmod 777)
;$inet     = 2;                   # AF_INET (for Socket connection)
;$stream   = 1;                   # SOCK_STREAM (for Socket connection)

srand(time^($$+($$<<15))||time);
$version   = $version;

;# ============================
;# Set/Get Cookies.
;# ============================

sub setCookie #(*cookie_body, $cookie_id, $expires, $path, $domain, $secure, $return_value)
{
  local(*cookie_body, $cookie_id, $expires, $path, $domain, $secure, $return_value) = @_;
  local($cookie);

  $cookie_id = $1 if ($cookie_id eq "" && $ENV{'SCRIPT_NAME'} =~ /([^\\\/]+)$/);
  &urlencode(*cookie_id);
  if (%cookie_body) {
    local(@cookie);
    while(($key, $val) = each %cookie_body) {
      push @cookie, &urlencode_($key) . "=" . &urlencode_($val);
    }
    $cookie = join "&", @cookie;
  } elsif (@cookie_body) {
    local(@cookie);
    foreach (@cookie_body) {
      push @cookie, &urlencode_($_);
    }
    $cookie = join "&", @cookie;
  } elsif (defined $cookie_body) {
    $cookie = $cookie_body;
  }
  if ($expires eq "-1") {
    $cookie .= '; expires=Mon, 01-Jan-1990 00:00:00 GMT';
  } elsif ($expires =~ /^\d+$/) {
    local(@gmtime) = split / +/, scalar gmtime(time + $expires);
    $cookie .= "; expires=$gmtime[0], $gmtime[2]-$gmtime[1]-$gmtime[4] $gmtime[3] GMT";
  } elsif ($expires) {
    $cookie .= "; expires=$expires";
  }
  $cookie .= "; domain=$domain" if ($domain);
  $cookie .= "; path=$path" if ($path);
  $cookie .= "; secure" if ($secure);
  return "$cookie_id=$cookie" if ($return_value && $cookie_id ne "" && $cookie ne "");
  print "Set-Cookie: $cookie_id=$cookie\n" if ($cookie_id ne "" && $cookie ne "");
  return;
}

sub getCookie #(*cookie_body, $cookie_id)
{
  local(*cookie_body, $cookie_id) = @_;
  local(@array);

  $cookie_id = $1 if ($cookie_id eq "" && $ENV{'SCRIPT_NAME'} =~ /([^\\\/]+)$/);
  &urlencode(*cookie_id);
  foreach (split /;/, $ENV{'HTTP_COOKIE'}) {
    local($key, $val) = split /=/, $_, 2;
    $key =~ tr/ \a\b\f\r\n\t//d;
    if ($key eq $cookie_id) {
      foreach (split /&/, $val) {
        if (!/=/) {
          push @cookie_body, &urldecode_($_);
          @array = @cookie_body
        } else {
          local($key, $val) = split /=/, $_, 2;
          &urldecode(*key);
          $cookie_body{$key} = &urldecode_($val);
          push @array, $key;
        }
      }
      return @array;
    }
  }
  return;
}

;# ============================
;# Session Control.
;# ============================

sub setSession #($ses_file, *ses_body, $ses_id, $expires)
{
  local($ses_file, *ses_body, $ses_id, $expires) = @_;
  local(@point, $flag, $data, $buf, $size, $i, $j);

  $flag = $i = $j = $size = 0;
  $ses_id = $ENV{'REMOTE_ADDR'} if ($ses_id eq "");
  &urlencode(*ses_id);
  $ses_file =~ s/^\/\/\//$tmp_dir/;
  if (%ses_body || @ses_body) {
    local(@data);
    if (%ses_body) {
      while (($key, $val) = each %ses_body) {
        push @data, &urlencode_($key) . "=" . &urlencode_($val);
      }
    } else {
      foreach (@ses_body) {
        push @data, &urlencode_($_);
      }
    }
    $expires = $expires ? $expires + time : 3600 + time;
    $data = "\a$ses_id\t$expires\t" . join("\t", @data) . "\t";
    if (length $data > $ses_byte - 1) {
      $size = $ses_byte;
      $data = substr $data, 0, ($ses_byte - 1);
    } elsif (length $data < $ses_byte - 1) {
      $size = length($data) + 1;
      $data .= " " x ($ses_byte - length($data) - 1);
    }
  } else {
    $size = 1;
    $data = " " x ($ses_byte - 1);
  }
  $data .= "\x0a";
  if (!open IO, "+<$ses_file") {
    if (!-f "$ses_file" && open OUT, ">$ses_file") {
      binmode OUT;
      print OUT $data;
      close OUT;
      return $size;
    }
    return 0;
  }
  binmode IO;
  select((select(IO), $| = 1)[0]);
  while (read IO, $buf, $ses_byte) {
    if ($buf =~ /^ /) {
      $point[$j++] = tell(IO) - $ses_byte;
      $i ++;
      next;
    } elsif ($buf !~ /^\a/ || $buf !~ /\x0a$/) {
      close IO;
      return "";
    }
    local($ses_id2, $expires2) = split /\t/, substr($buf, 1), 3;
    $i = 0;
    if ($expires2 - time > 0) {
      if (!$flag && $ses_id2 eq $ses_id) {
        $flag = 1;
        seek IO, $ses_byte * -1, 1;
        print IO $data;
      }
    } else {
      seek IO, $ses_byte * -1, 1;
      print IO " " x ($ses_byte - 1) . "\x0a";
    }
  }
  if ($i || !$flag) {
    return 0 if (!&lock($ses_file));
    if ($i) {
      eval { truncate(IO, (-s $ses_file) - $i * $ses_byte); };
    }
    if (!$flag) {
      foreach (@point) {
        local($buf);
        last if ($_ eq "");
        seek IO, $_, 0;
        read IO, $buf, 1;
        if ($buf eq " ") {
          seek IO, $_, 0;
          $flag = 1;
          last;
        }
      }
      seek IO, 0, 2 if (!$flag);
      print IO $data;
    }
    &unlock($ses_file);
  }
  close IO;
  return $size;
}

sub getSession #($ses_file, *ses_body, $ses_id, $expires)
{
  local($ses_file, *ses_body, $ses_id, $expires) = @_;
  local($point, $buf, $size);

  $flag = $point = $size = 0;
  $ses_id = $ENV{'REMOTE_ADDR'} if ($ses_id eq "");
  &urlencode(*ses_id);
  $ses_file =~ s/^\/\/\//$tmp_dir/;
  return 0 if (!open IO, "+<$ses_file");
  binmode IO;
  select((select(IO), $| = 1)[0]);
  while (read IO, $buf, $ses_byte) {
    if ($buf =~ /^ /) {
      next;
    } elsif ($buf !~ /^\a/ || $buf !~ /\x0a$/) {
      close IO;
      return "";
    }
    $buf =~ s/\x0a$//;
    local($ses_id2, $expires2, @field) = split /\t/, substr($buf, 1);
    if ($expires2 - time > 0) {
      if (!$size && $ses_id2 eq $ses_id) {
        $buf =~ tr/ //d;
        $size = 1 + length $buf;
        foreach (@field) {
          last if (/^ /);
          if (!/=/) {
            push @ses_body, &urldecode_($_);
          } else {
            local($key, $val) = split /=/, $_, 2;
            &urldecode(*key);
            $ses_body{$key} = &urldecode_($val);
          }
        }
        if ($expires == -1) {
          seek IO, $ses_byte * -1, 1;
          print IO " " x ($ses_byte - 1) . "\x0a";
        } elsif ($expires) {
          local($data);
          $expires2 = time + $expires;
          $data = "\a$ses_id2\t$expires2\t" . join("\t", @field) . "\t";
          if (length $data > $ses_byte - 1) {
            $data = substr $data, 0, ($ses_byte - 1);
          } elsif (length $data < $ses_byte - 1) {
            $data .= " " x ($ses_byte - length($data) - 1);
          }
          seek IO, $ses_byte * -1, 1;
          print IO $data . "\x0a";
        }
      }
    } else {
      seek IO, $ses_byte * -1, 1;
      print IO " " x ($ses_byte - 1) . "\x0a";
    }
  }
  close IO;
  return $size;
}

;# ============================
;# Get STDIN Data & Decode.
;# ============================

#sub getFormData #(*IN, $tr_tags, $jcode, $multi_keys, $file_dir)
sub getFormData #(*IN, $tr_tags, $jcode, $multi_keys, $file_dir, $jcode2)
{
  return $ENV{'CONTENT_TYPE'} =~ /^multipart\/form-data;/i ? &getMultipartFormData(@_) : &getUrlencodedFormData(@_);
}

#sub getUrlencodedFormData #(*IN, $tr_tags, $jcode, $multi_keys)
sub getUrlencodedFormData #(*IN, $tr_tags, $jcode, $multi_keys, '', $jcode2)
{
  local(*IN, $tr_tags, $jcode, $multi_keys, $file_dir, $jcode2) = @_;
  local($buffer, @keys, $h2z);

  return if ($ENV{'CONTENT_LENGTH'} > 131072 || $ENV{'CONTENT_TYPE'} =~ /^multipart\/form-data;/i);
  if ($ENV{'REQUEST_METHOD'} eq 'POST') {
    read STDIN, $buffer, $ENV{'CONTENT_LENGTH'};
  } else {
    $buffer = $ENV{'QUERY_STRING'};
  }
  return if ($buffer eq "" || length $buffer > 131072);
  $h2z = $jcode =~ tr/A-Z/a-z/ ? "z" : "";
  foreach (split /[&;]/o, $buffer) {
    local($key, $val) = split /=/, $_, 2;
    &urldecode(*key);
    &urldecode(*val);
    if ($jcode && $jcode'version) {
      &jcode'convert(*key, $jcode, "", $h2z);
      &jcode'convert(*val, $jcode, "$jcode2", $h2z);
    }
    $key =~ s/\x0d\x0a|\x0d|\x0a/\n/g;
    $key =~ tr/\t\a\b\e\f\0//d;
    $val =~ s/\x0d\x0a|\x0d|\x0a/\n/g;
    $val =~ tr/\t\a\b\e\f\0//d;
    if ($tr_tags) {
      &trString(*key, 1);
      &trString(*val, 1);
      if ($tr_tags == 2) {
        $key =~ s/\n/<br \/>/g;
        $val =~ s/\n/<br \/>/g;
      }
    }
    if ($multi_keys ne "") {
      $IN{$key} .= defined $IN{$key} ? "$multi_keys$val" : $val;
    } else {
      $IN{$key} = $val;
    }
    push @keys, $key;
  }
  return @keys;
}

sub getMultipartFormData #(*IN, $tr_tags, $jcode, $multi_keys, $file_dir)
{
  local(*IN, $tr_tags, $jcode, $multi_keys, $file_dir) = @_;
  local(@keys, $boundary, $key, $val, $buf1, $buf2, $buf3, $len, $path, $flag, $file, $text, $type, $open, $h2z, $i);

  return if ($ENV{'CONTENT_LENGTH'} > $max_byte || $ENV{'CONTENT_TYPE'} !~ /^multipart\/form-data; *boundary=(.+)/);
  $boundary = $1;
  $file_dir =~ s/^\/\/\//$tmp_dir/;
  $h2z = $jcode =~ tr/A-Z/a-z/ ? "z" : "";
  binmode STDIN;

 out:
  while (read STDIN, $buf1, 4096) {
    local($offset, $start) = 0;
    $buf1 .= getc STDIN if (substr($buf1, -1, 1) eq "\x0d");
    while (1) {
      local($pos, $buf);
      $pos = index $buf1, "\x0d\x0a", $start;
      if ($pos == -1) {
        last if (length($buf1) == $offset);
        $buf   = !$offset ? $buf1 : substr $buf1, $offset, (length($buf1) - $offset);
        $offset= length $buf1;
      } else {
        $start = $pos + 2;
        $buf   = substr $buf1, $offset, $start - $offset;
        $offset= $start;
      }
      $buf = $buf2 . $buf if ($buf2 ne "");
      undef $buf2;
      if (substr($buf, -2, 2) ne "\x0d\x0a") {
        if ($open && $flag == 2 && length($buf) > length($boundary) + 8) {
          if ($buf3 ne "") {
            print OUT $buf3;
            undef $buf3;
          }
          print OUT $buf;
        } else {
          $buf2 = $buf;
        }
        next;
      }
      if ($flag == 2) {
        if (index($buf, "--$boundary") == 0) {
          &jcode'convert(*key, $jcode, "", $h2z) if ($jcode && $jcode'version);
          $key =~ s/\x0d\x0a|\x0d|\x0a/\n/g;
          $key =~ tr/\t\a\b\e\f\0//d;
          if ($tr_tags) {
            &trString(*key, 1);
            $key =~ s/\n/<br \/>/g if ($tr_tags == 2);
          }
          push @keys, $key;
          if ($text) {
            &jcode'convert(*val, $jcode, "", $h2z) if ($jcode && $jcode'version);
            $val =~ s/\x0d\x0a$//;
            $val =~ s/\x0d\x0a|\x0d|\x0a/\n/g;
            $val =~ tr/\t\a\b\e\f\0//d;
            if ($tr_tags) {
              &trString(*val, 1);
              $val =~ s/\n/<br \/>/g if ($tr_tags == 2);
            }
            if ($multi_keys ne "") {
              $IN{$key} .= defined $IN{$key} ? "$multi_keys$val" : $val;
            } else {
              $IN{$key} = $val;
            }
          } else {
            if ($open) {
              $buf3 =~ s/\x0d\x0a$//;
              print OUT $buf3;
              close OUT;
              $IN{"$key->size"} = (-s $file);
              $IN{$key} = $file;
            } else {
              $val =~ s/\x0d\x0a$//;
              $IN{$key} = $val;
              $IN{"$key->size"} = length $val;
            }
            &jcode'convert(*path, $jcode, "", $h2z) if ($jcode && $jcode'version);
            $IN{"$key->path"} = $path;
            $IN{"$key->name"} = $1 if ($path =~ /([^\\\/]+)$/);
            $IN{"$key->type"} = $type;
          }
          $len += length $key + length $val;
          ($text, $type, $flag, $path, $open, $file, $key, $val, $buf3) = undef;
          last out if ($buf =~ /--\x0d\x0a$/ || $len > 131072);
        } elsif ($open) {
          print OUT $buf3 if ($buf3 ne "");
          $buf3 = $buf;
        } else {
          $val .= $buf;
          last out if (length $val > 131072);
        }
      } elsif ($flag && !$text && $buf =~ /^Content-Type: *([^\s]+)/i) {
        $type = $1;
      } elsif ($flag && $buf eq "\x0d\x0a") {
        $flag = 2;
      } elsif ($buf =~ /^Content-Disposition: *([^;]*); *name="([^"]*)"; *filename="([^"]*)"/i) {
        $key  = $2;
        $path = $3;
        $flag = 1;
        if ($path ne "" && $file_dir ne "") {
          if ($IN{$key} eq "") {
            $i ++;
            $file = sprintf "$file_dir%d-$i.tmp", $$+time;
          } else {
            $file = $IN{$key};
          }
          if (open OUT, ">$file") {
            binmode OUT;
            push @file, $file;
            $open = 1;
          }
        }
      } elsif ($buf =~ /^Content-Disposition: *([^;]*); *name="([^;]*)"/i) {
        $key  = $2;
        $flag = 1;
        $text = 1;
      }
    }
  }
  return @keys;
}

;# ============================
;# Set Form Data.
;# ============================

sub setQueryString #(*hash, *array, $separator, $cut_blank)
{
  local(*hash, *array, $separator, $cut_blank) = @_;
  local(@query);

  $separator = ";" if ($separator eq "");
  @array = sort keys %hash if (!@array);
  foreach (@array) {
    local($val) = $hash{$_};
    next if ($cut_blank && $val eq "");
    &urlencode(*val);
    push @query, "$_=$val";
  }
  return join $separator, @query;
}

sub setHiddenForm #(*hash, *array, $separator, $cut_blank)
{
  local(*hash, *array, $separator, $cut_blank) = @_;
  local(@query);

  $separator = "\n" if ($separator eq "");
  @array = sort keys %hash if (!@array);
  foreach (@array) {
    local($key, $val) = ($_, $hash{$_});
    next if ($cut_blank && $val eq "");
    &trString(*key, 1);
    $key =~ s/\n/&#10;/g;
    &trString(*val, 1);
    $val =~ s/\n/&#10;/g;
    push @query, qq|<input type="hidden" name="$key" value="$val" />|;
  }
  return join $separator, @query;
}

;# ============================
;# Get day & time.
;# ============================

sub getTime #($time_format, $time_difference, $base_time)
{
  local($time_format, $time_difference, $base_time) = @_;
  local(@time);

  $base_time = time if ($base_time eq "");
  if ($time_format ne "") {
    @time = gmtime($base_time + $time_difference);
  } else {
    return scalar gmtime($base_time + $time_difference);
  }
  $time_format =~ s/%%/%\a/g;
  $time_format =~ s/%mm/sprintf("%02d",$time[4]+1)/eg;
  $time_format =~ s/%m/$time[4]+1/eg;
  $time_format =~ s/%yyyy/$time[5]+1900/eg;
  $time_format =~ s/%yyy/$time[5]-88/eg;
  $time_format =~ s/%yy/substr($time[5]+1900, 2, 2)/eg;
  $time_format =~ s/%y/substr($time[5]+1900, 3, 1)/eg;
  $time_format =~ s/%dd/sprintf("%02d",$time[3])/eg;
  $time_format =~ s/%d/$time[3]/g;
  $time_format =~ s/%hh/sprintf("%02d",$time[2])/eg;
  $time_format =~ s/%h/$time[2]/g;
  $time_format =~ s/%nn/sprintf("%02d",$time[1])/eg;
  $time_format =~ s/%n/$time[1]/eg;
  $time_format =~ s/%ss/sprintf("%02d",$time[0])/eg;
  $time_format =~ s/%s/$time[0]/eg;
  $time_format =~ s/%ww4/$time[6]/g;
  if ($time[2] < 12) {
    local($ap) = $1 if ($time_format =~ s/%\{(.+)\|(.+)\}/%ap/g);
    $ap = 'AM' if ($ap eq "");
    $time[7] = $time[2];
    $time_format =~ s/%ap/$ap/gi;
  } else {
    local($ap) = $2 if ($time_format =~ s/%\{(.+)\|(.+)\}/%ap/g);
    $ap = 'PM' if ($ap eq "");
    $time[7] = $time[2] == 12 ? 12 : $time[2] - 12;
    $time_format =~ s/%ap/$ap/gi;
  }
  $time_format =~ s/%HH/sprintf("%02d",$time[7])/eg;
  $time_format =~ s/%H/$time[7]/g;
  if ($time_format =~ /%ww2/) {
    local(@week) = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat');
    $time_format =~ s/%ww2/$week[$time[6]]/g;
  }
  if ($time_format =~ /%ww3/) {
    local(@week) = ('Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday');
    $time_format =~ s/%ww3/$week[$time[6]]/g;
  }
  if ($time_format =~ /%ww/) {
    local(@week) = ('“ú','ŒŽ','‰Î','…','–Ø','‹à','“y');
    $time_format =~ s/%ww/$week[$time[6]]/g;
  }
  if ($time_format =~ /%MM2/) {
    local(@month) = ('January','Februay','March','April','May','June','July','August','September','October','November','December');
    $time_format =~ s/%MM2/$month[$time[4]]/g;
  }
  if ($time_format =~ /%MM/) {
    local(@month) = ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec');
    $time_format =~ s/%MM/$month[$time[4]]/g;
  }
  $time_format =~ s/%\a/%/g;
  return $time_format;
}

;# ============================
;# Get UTC Serial Time.
;# ============================

sub getSerialTime #($time_zone, $year, $month, $day, $hour, $min, $sec)
{
  local($time_zone, $year, $month, $day, $hour, $min, $sec) = @_;
  local(@day_month, $age, $leap, $time);

  return if ($year eq "");
  @day_month = (0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334);
  if ($month =~ /^\w{3,9}$/) {
    local(%month) = ('jan'=>1,'feb'=>2,'mar'=>3,'apr'=>4,'may'=>5,'jun'=>6,'jul'=>7,'aug'=>8,'sep'=>9,'oct'=>10,'nov'=>11,'dec'=>12);
    $month = substr $month, 0, 3;
    $month =~ tr/A-Z/a-z/;
    $month = $month{$month};
  }
  $month = 1 if (!$month);
  $day   = 1 if (!$day);
  $age   = $year - 1970;
  $leap  = 1970 <= $year ? &getLeapYearTimes(1970, $year) : &getLeapYearTimes($year, 1970);
  $leap -- if ($year % 4 == 0 && ($year % 400 == 0 || $year % 100 != 0));
  $time  = ($age - $leap) * 31536000;
  $time += $leap * 31622400;
  $time += $day_month[$month-1] * 86400;
  $time += 86400 if ($month >= 3 && $year % 4 == 0 && ($year % 400 == 0 || $year % 100 != 0));
  $time += ($day - 1)  * 86400;
  $time += $hour * 3600;
  $time += $min  * 60;
  $time += $sec;
  return $time - $time_zone;
}

sub getLeapYearTimes #($year1, $year2)
{
  local($year1, $year2) = @_;
  local($year1x, $year2x, $leap);

  return if ($year2 - $year1 < 0);
  while ($year1 % 4 != 0) {
    $year1 ++;
  }
  $year1 += 4 if ($year1 % 100 == 0 && $year1 % 400 != 0);
  while ($year2 % 4 != 0) {
    $year2 --;
  }
  $year2 -= 4 if ($year2 % 100 == 0 && $year2 % 400 != 0);
  $leap = ($year2 - $year1) / 4 + 1;
  $year1x = int($year1 / 100);
  $year2x = int($year2 / 100);
  if ($year2x - $year1x > 0) {
    local($i) = 0;
    for ($year1x .. $year2x) {
      $i ++ if ($_ % 4 == 0);
    }
    $leap -= $year2x - $year1x - $i;
  }
  return $leap;
}

;# ============================
;# Encode / Decode.
;# ============================

sub base64encode_ #($data, $ins_lf)
{
  local($data, $ins_lf) = @_;

  &base64encode(*data, $ins_lf);
  return $data;
}

sub base64encode #(*data, $ins_lf)
{
  local(*data, $ins_lf) = @_;
  local($length, $result, $base, $i, $j);

  $base = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
  $data = unpack "B*", $data;
  for ($i = 0, $j = 1; $length = substr($data, $i, 6); $i += 6, $j ++) {
    $result .= substr($base, ord(pack("B*", "00" . $length)), 1);
    if (length $length == 2) {
      $result .= "==";
    } elsif (length $length == 4) {
      $result .= "=";
    }
    $result .= "\n" if ($ins_lf && $j % $ins_lf == 0);
  }
  $data = $result;
}

sub base64decode_ #($data)
{
  local($data) = @_;

  &base64decode(*data);
  return $data;
}

sub base64decode #(*data)
{
  local(*data) = $_[0];
  local($result, $length);

  $data =~ tr|A-Za-z0-9+=/||cd;
  return if ($data eq "");
  return if (length($data) % 4);

  $data =~ s/=+$//;
  $data =~ tr|A-Za-z0-9+/| -_|;
  while ($data =~ /(.{1,60})/g) {
    $length  = pack("C", 32 + int length($1) * 3 / 4);
    $result .= unpack "u", $length . $1;
  }
  $data = $result;
}

sub urlencode_ #($data)
{
  local($data) = @_;

  &urlencode(*data);
  return $data;
}

sub urlencode #(*data)
{
  local(*data) = @_;

  $data =~ s/([^\w\-.* ])/sprintf('%%%02x', ord $1)/eg;
  $data =~ tr/ /+/;
}

sub urldecode_ #($data)
{
  local($data) = @_;

  &urldecode(*data);
  return $data;
}

sub urldecode #(*data)
{
  local(*data) = @_;

  $data =~ tr/+/ /;
  $data =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex $1)/eg;
}

;# ============================
;# Transfer String.
;# ============================

sub trString_ #($str, $html, $lc, $z2h, $k2h, $rmstr)
{
  local($str) = shift;

  &trString(*str, @_);
  return $str;
}

sub trString #(*str, $html, $lc, $z2h, $k2h, $rmstr)
{
  local(*str, $html, $lc, $z2h, $k2h, $rmstr) = @_;

  if ($html) {
    if ($html == 2) {
      $str =~ s/&gt;/>/g;
      $str =~ s/&lt;/</g;
      $str =~ s/&quot;/"/g;
      $str =~ s/&amp;/&/g;
    } else {
      $str =~ s/&/&amp;/g;
      $str =~ s/"/&quot;/g;
      $str =~ s/</&lt;/g;
      $str =~ s/>/&gt;/g;
    }
  }
  if ($jcode'version) {
    local($from, $to);
    if ($k2h) {
      $from = 'ƒAƒCƒEƒGƒIƒJƒLƒNƒPƒRƒTƒVƒXƒZƒ\ƒ^ƒ`ƒcƒeƒgƒiƒjƒkƒlƒmƒnƒqƒtƒwƒzƒ}ƒ~ƒ€ƒƒ‚ƒ„ƒ†ƒˆƒ‰ƒŠƒ‹ƒŒƒƒƒ’ƒ“ƒKƒMƒOƒQƒSƒUƒWƒYƒ[ƒ]ƒ_ƒaƒdƒfƒhƒoƒrƒuƒxƒ{ƒpƒsƒvƒyƒ|‚î‚ïƒ@ƒBƒDƒFƒHƒƒƒ…ƒ‡ƒb';
      $to   = '‚ ‚¢‚¤‚¦‚¨‚©‚«‚­‚¯‚±‚³‚µ‚·‚¹‚»‚½‚¿‚Â‚Ä‚Æ‚È‚É‚Ê‚Ë‚Ì‚Í‚Ð‚Ó‚Ö‚Ù‚Ü‚Ý‚Þ‚ß‚à‚â‚ä‚æ‚ç‚è‚é‚ê‚ë‚í‚ð‚ñ‚ª‚¬‚®‚°‚²‚´‚¶‚¸‚º‚¼‚¾‚À‚Ã‚Å‚Ç‚Î‚Ñ‚Ô‚×‚Ú‚Ï‚Ò‚Õ‚Ø‚Ûƒƒ‘‚Ÿ‚¡‚£‚¥‚§‚á‚ã‚å‚Á';
      if ($k2h == 2) {
        local($tmp_var) = $to;
        $to = $from;
        $from = $tmp_var;
      }
    }
    if ($z2h) {
      $from .= '‚O‚P‚Q‚R‚S‚T‚U‚V‚W‚X‚`‚a‚b‚c‚d‚e‚f‚g‚h‚i‚j‚k‚l‚m‚n‚o‚p‚q‚r‚s‚t‚u‚v‚w‚x‚y‚‚‚‚ƒ‚„‚…‚†‚‡‚ˆ‚‰‚Š‚‹‚Œ‚‚Ž‚‚‚‘‚’‚“‚”‚•‚–‚—‚˜‚™‚š{^OQb–IHh”“•—FG@|';
      $to   .= '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+=/^_|*!?"#$\%&@:; -';
      if ($z2h == 2) {
        local($tmp_var) = $to;
        $to = $from;
        $from = $tmp_var;
      }
    }
    if ($rmstr) {
      $from .= $rmstr;
      $to   .= "\a";
    }
    if ($from ne "" && $to ne "") {
      &jcode'tr(*str, $from, $to);
      $str =~ tr/\a//d if ($rmstr);
    }
  }
  if ($lc) {
    if ($lc == 2) {
      $str =~ tr/a-z/A-Z/;
    } else {
      $str =~ tr/A-Z/a-z/;
    }
  }
}

;# ============================
;# Search String.
;# ============================

sub searchString #($str, $key, $mhmode)
{
  local($str, $key, $mhmode) = @_;

  return if ($str eq "" || $key eq "");
  if ($mhmode == 2 || $mhmode =~ /^BOOLEAN$/i || $mhmode =~ /^BLN$/i) {
    local($expr);
    $key =~ s/ OR / | /gi;
    $key =~ s/ AND / & /gi;
    $key =~ s/(^| )NOT / ! /gi;
    $key =~ tr/ //d;
    foreach (split /([!&|\(\)])/, $key) {
      if (/^[!&|\(\)]$/) {
        $expr .= $_;
      } elsif ($_ ne "") {
        $expr .= &searchString_by_wc(*str, $_);
      }
    }
    $expr =~ tr/&|/*+/;
    $expr =~ s/(\d+|\))!/$1*!/g;
    $expr = eval $expr;
    return "" if ($expr eq "");
    return $expr ? 1 : 0;
  } elsif ($mhmode == 2 || $mhmode =~ /^OR$/i) {
    foreach (split / +/, $key) {
      if (s/^[-!]//) {
        return 1 if (!&searchString_by_wc(*str, $_));
      } elsif (&searchString_by_wc(*str, $_)) {
        return 1;
      }
    }
    return 0;
  } else { 
    foreach (split / +/, $key) {
      if (s/^[-!]//) {
        return 0 if (&searchString_by_wc(*str, $_));
      } elsif (!&searchString_by_wc(*str, $_)) {
        return 0;
      }
    }
    return 1;
  }
}

sub searchString_by_wc #(*str, $key)
{
  local(*str, $key) = @_;
  local($flag) = 0;

  $key =~ s/\*\*/\a/g;
  $key =~ s/\*{2,}/*/g;
  $key =~ s/^\*//;
  $key =~ s/\*$//;
  foreach (split /\*/, $key) {
    local($result);
    tr/\a/*/;
    if (($result = index($str, $_)) != -1) {
      $flag = !$flag || ($result >= $flag && $result <= $flag + 32) ? $result + length : 0 ;
    } else {
      return 0;
    }
    last if (!$flag);
  }
  return $flag ? 1 : 0;
}

;# ============================
;# Make Random String.
;# ============================

sub getRandomString #($len, $str)
{
  local($len, $str) = @_;
  local(@str) = $str ? split //, $str : ('A'..'Z','a'..'z','0'..'9');

  undef $str;
  $len = 8 if (!$len);
  for (1 .. $len) {
    $str .= $str[int rand($#str+1)];
  }
  return $str;
}

;# ============================
;# Set Link.
;# ============================

sub setLink_ #($str, $attribute, $uri_str, $mail_str)
{
  local($str) = shift;

  &setLink(*str, @_);
  return $str;
}

sub setLink #(*str, $attribute, $uri_str, $mail_str)
{
  local(*str, $attribute, $uri_str, $mail_str) = @_;
  local($element, $new_str);

  $attribute = " $attribute" if ($attribute ne "");
  foreach (split /(<[^>]*>)/, $str) {
    if (/^<(a|button|textarea|script|head)/i) {
        $element = $1;
    } elsif ($element && /^<\/$element/) {
        $element = "";
    } elsif (!$element && ! /^</) {
      tr/\a//d;
      s/&amp;/\a/g;
      if ($uri_str ne "") {
        s/((view-source:)?(https?|ftp|gopher|telnet|news|wais|nntp|rtsp|mms):\/\/[-+:.@\w]{4,64}(\/[-.?+:;!#%=@~^\$\a\w\/\[\]]{0,256})?)/<a href=\"$1\"$attribute>$uri_str<\/a>/g;
      } else {
        s/((view-source:)?(https?|ftp|gopher|telnet|news|wais|nntp|rtsp|mms):\/\/[-+:.@\w]{4,64}(\/[-.?+:;!#%=@~^\$\a\w\/\[\]]{0,256})?)/<a href=\"$1\"$attribute>$1<\/a>/g;
      }
      if ($mail_str ne "") {
        s/(mailto:[-+.\w]{1,32}@[-+.\w]*[-A-Za-z0-9]{2,32}\.[A-Za-z]{1,6}(\?[-.?+:;!#%=@~^\$\a\w\/\[\]]{0,256})?)\b/<a href="$1">$mail_str<\/a>/g;
      } else {
        s/(mailto:[-+.\w]{1,32}@[-+.\w]*[-A-Za-z0-9]{2,32}\.[A-Za-z]{1,6})(\?[-.?+:;!#%=@~^\$\a\w\/\[\]]{0,256})?\b/<a href="$1$2">$1<\/a>/g;
      }
      s/\a/&amp;/g;
    }
    $new_str .= $_;
  }
  $str = $new_str;
}

;# ============================
;# Set Comma per 3 figures.
;# ============================

sub setComma #($str)
{
  local($str) = $_[0];

  if ($str =~ /^(-?)([\dA-Fa-f]+)(\..*)?$/) {
    local($mns, $str, $dot) = ($1, $2, $3);
    1 while $str =~ s/([\dA-Fa-f]+)([\dA-Fa-f]{3})/$1,$2/;
    return "$mns$str$dot";
  }
  return $str;
}

;# ============================
;# Lock Check / Lock / Unlock
;# ============================

sub lock #($lock_dir)
{
  local($lock_dir) = "$_[0].lock";
  local($lock_dir2, $i);

  $lock_dir =~ s/^\/\/\//$tmp_dir/;
  $lock_dir2 = $lock_dir . "2";
  $i = 0;
  if ((-M $lock_dir) * 86400 > 180) {
    rmdir $lock_dir;
    rmdir $lock_dir2;
  }
  while(!mkdir $lock_dir, 0755) {
    sleep 1;
    if (++ $i >= 3) {
      if (mkdir $lock_dir2, 0755) {
        if ((-M $lock_dir) * 86400 > 60) {
          return 1 if (rename $lock_dir2, $lock_dir);
        }
        rmdir $lock_dir2;
        return 0;
      }
      if ((-M $lock_dir2) * 86400 > 30) {
        if ((-M $lock_dir) * 86400 > 60) {
          return 1 if (rename $lock_dir2, $lock_dir);
        }
        rmdir $lock_dir2;
      }
      return 0;
    }
  }
  return 1;
}

sub unlock #($lock_dir)
{
  local($lock_dir) = "$_[0].lock";

  $lock_dir =~ s/^\/\/\//$tmp_dir/;
  return rmdir $lock_dir if (-d $lock_dir);
}

sub lockCheck #($lock_dir)
{
  local($lock_dir) = "$_[0].lock";
  local($lock_dir2, $i);

  $lock_dir =~ s/^\/\/\//$tmp_dir/;
  $lock_dir2 = $lock_dir . "2";
  $i = 0;
  return 1 if ((-M $lock_dir) * 86400 > 60);
  while (-d $lock_dir) {
    sleep 1;
    return 0 if (++ $i >= 3);
  }
  return 1;
}

;# ============================
;# (HTTP) Socket Connection.
;# ============================

sub openSocket #($SOCK, $uri, $method, *header, $stdin)
{
  local($SOCK, $uri, $method, *header, $stdin) = @_;
  local($host, $path, $addr, $http, $port, $proc, $flag1, $flag2);

  $SOCK = "main'$SOCK" if ($SOCK !~ /[':]/);
  $http = $uri =~ s/^http\:\/\///i;
  ($host, $path) = split /[ \/]/, $uri, 2;
  ($host, $port) = split /:/, $host, 2;
  $path = $path =~ /^http:/ ? " $path" : "/$path";
  $port = 80 if (!$port);
  $method = "GET" if (!$method);
  if ($host =~ /^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$/) {
    $addr = pack('C4', (split /\./, $host)[0..3]);
  } elsif (!($addr = gethostbyname $host)) {
    return 0;
  }
  if ($INC{'Socket.pm'}) {
    $inet   = &main'AF_INET;
    $stream = &main'SOCK_STREAM;
  }
  $proc = pack('S n a4 x8', $inet, $port, $addr);
  return 0 if (!socket $SOCK, $inet, $stream, getprotobyname("tcp"));
  return 0 if (!connect $SOCK, $proc);
  select((select($SOCK), $| = 1)[0]);
  if ($http) {
    print $SOCK "$method $path HTTP/1.1\x0d\x0a"
              . "Host: $host\x0d\x0a";
    foreach (sort keys %header) {
      next if ($header{$_} =~ /^\s*$/);
      $header{$_} =~ tr/\x0d\x0a//d;
      print $SOCK "$_: $header{$_}\x0d\x0a";
      $flag1 = 1 if (/^Content-Type/i);
      $flag2 = 1 if (/^Content-Length/i);
    }
    if ($method ne "GET" && $stdin ne "") {
      print $SOCK "Content-Type: application/x-www-form-urlencoded\x0d\x0a" if (!$flag1);
      print $SOCK "Content-Length: ", length $stdin, "\x0d\x0a" if (!$flag2);
      print $SOCK "\x0d\x0a"
                . $stdin;
    } else {
      print $SOCK "\x0d\x0a";
    }
  }
  return 1;
}

sub closeSocket #($SOCK)
{
  local($SOCK) = @_;

  $SOCK = "main'$SOCK" if ($SOCK !~ /[':]/);
  return close $SOCK;
}

;# ============================
;# Send Email.
;# ============================

sub sendmail #(*header, $body, $html_body, $mime_encode, @attachments)
{
  local(*header, $body, $html_body, $mime_encode, @attachments) = @_;
  local($boundary, $text);

  return 0 if (!open ML, "| $sendmail -t -i");
  while (($key, $val) = each %header) {
    local($val2);
    next if ($val =~ /^\s*$/);
    $val =~ tr/\x0d\x0a//d;
    foreach (split /( +|")/, $val) {
      if (/[^\x20-\x7e]/) {
        &jcode'convert(*_, 'jis') if ($jcode'version);
        &base64encode(*_);
        $val2 .= "=?ISO-2022-JP?B?$_?=";
      } else {
        $val2 .= $_;
      }
    }
    $val = $val2;
    print ML "$key: $val\n";
  }
  if (@attachments) {
    $boundary = '===' . time . $$ . time . '===';
    print ML "Content-Type: multipart/mixed;\n"
           . qq(\tboundary="$boundary"\n\n)
           . "This is a multipart message in MIME format.\n\n"
           . "--$boundary\n";
  } elsif ($body && $html_body) {
    $boundary = '===' . time . $$ . time . '===';
    print ML "Content-Type: multipart/alternative;\n"
           . qq(\tboundary="$boundary"\n\n)
           . "This is a multipart message in MIME format.\n\n"
           . "--$boundary\n";
  }
  $text = !$body && $html_body ? 'html' : 'plain';
  $body = $html_body if ($text eq "html");
  &jcode'convert(*body, 'jis') if ($jcode'version);
  print ML "Content-Type: text/$text"
         . qq(; charset="ISO-2022-JP"\n)
         . "Content-Transfer-Encoding: 7bit\n\n"
         . "$body\n";
  if ($text eq "plain" && $html_body) {
    print ML "--$boundary\n"
           . qq(Content-Type: text/html; charset="ISO-2022-JP"\n)
           . "Content-Transfer-Encoding: 7bit\n\n";
    &jcode'convert(*html_body, 'jis') if ($jcode'version);
    print ML "$html_body\n";
    print ML "--$boundary--\n" if (!@attachments);
  }
  if (@attachments) {
    foreach $file (@attachments) {
      local($file, $type, $name, $encode) = split / *; */, $file;
      local($cache_file, $command);
      $name = (!$name && $file =~ /([^\/]+$)/) ? $1 : $name;
      $type = &getMimeType($file) if (!$type);
      &jcode'convert(*name, 'jis') if ($jcode'version);
      $name = "=?ISO-2022-JP?B?" . base64encode_($name) . "?=" if ($name =~ /[^\w\-\[\]\(\).]/);
      $encode = $mime_encode if ($encode eq "");
      ($encode, $command) = split / +/, $encode;
      if ($command eq "cache") {
        local($suffix) = $encode =~ /^uu(encode)?$/ ? "uu.cache" : "b64.cache";
        $cache_file = &base64encode_($file);
        $cache_file =~ tr/+\//-_/;
        $cache_file = "$tmp_dir$cache_file.$suffix";
        if (-r $cache_file) {
          $file = $cache_file;
          $command = "encoded";
        }
      }
      if ($command eq "encoded") {
        if (open IN, $file) {
          local($buffer);
          binmode IN;
          print ML "--$boundary\n"
             . qq(Content-Type: $type; name="$name"\n);
          if ($encode =~ /^uu(encode)?$/i) {
            print ML "Content-Transfer-Encoding: X-uuencode\n"
                 . qq(Content-Disposition: attachment; filename="$name"\n\n);
          } else {
            print ML "Content-Transfer-Encoding: Base64\n"
                 . qq(Content-Disposition: attachment; filename="$name"\n\n);
          }
          print ML $buffer while (read IN, $buffer, 4096);
          close IN;
          print ML "\n";
        }
      } elsif (open IN, $file) {
        local($file_size) = (-s $file);
        if ($cache_file && open CC, ">$cache_file") {
          binmode CC;
        } else {
          $cache_file = "";
        }
        binmode IN;
        print ML "--$boundary\n"
             . qq(Content-Type: $type; name="$name"\n);
        if ($encode =~ /^uu(encode)?$/i) {
          local($read, $buffer);
          print ML "Content-Transfer-Encoding: X-uuencode\n"
               . qq(Content-Disposition: attachment; filename="$name"\n\n)
               .   "begin 666 $name\n";
          print CC "begin 666 $name\n" if ($cache_file);
          while ($read = read IN, $buffer, 1035) {
            local($data);
            while ($buffer =~ s/^((.|\n|\r){45})//) {
              $data .= pack("u", $&);
            }
            if ($read == 1035) {
              print ML $data;
              print CC $data if ($cache_file);
              next;
            }
            print ML $data;
            print ML pack("u", $buffer) if ($buffer ne "");
            if ($cache_file) {
              print CC $data;
              print CC pack("u", $buffer) if ($buffer ne "");
            }
          }
          print ML "`\n"
                 . "end\n";
          print CC "`\n"
                 . "end\n" if ($cache_file);
        } else {
          local($base, $read, $buffer, $j);
          $base = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
          $j = 1;
          print ML "Content-Transfer-Encoding: Base64\n"
               . qq(Content-Disposition: attachment; filename="$name"\n\n);
          while ($read = read IN, $buffer, 1026) {
            local($data, $length, $i);
            $i = $length = 0;
            $buffer = unpack "B*", $buffer;
            while ($length = substr($buffer, $i, 6)) {
              $data .= substr($base, ord pack("B*", "00".$length), 1);
              if ($read != 1026 || tell(IN) == $file_size) {
                if (length $length == 2) {
                  $data .= "==";
                } elsif (length $length == 4) {
                  $data .= "=";
                }
              }
              $data .= "\n" if ($j++ % 76 == 0);
              $i += 6;
            }
            print ML $data;
            print CC $data if ($cache_file);
          }
        }
        close CC if ($cache_file);
        close IN;
        print ML "\n";
      }
    }
    print ML "--$boundary--\n";
  }
  close ML;
  return 1;
}

sub removeCacheFiles #(@attachments)
{
  local(@attachments) = @_;

  foreach (@attachments) {
    local($cache_file) = &base64encode_($_);
    $cache_file =~ tr/+\//-_/;
    unlink "$tmp_dir$cache_file.b64.cache" if (-f "$tmp_dir$cache_file.b64.cache");
    unlink "$tmp_dir$cache_file.uu.cache" if (-f "$tmp_dir$cache_file.uu.cache");
  }
}

;# ============================
;# Shuffle Array.
;# ============================

sub shuffleArray #(@array)
{
  local(@array) = @_;
  local(@new_array);

  while (@array) {
    push @new_array, splice(@array, int(rand $#array + 1), 1);
  }
  return @new_array;
}

;# ============================
;# Get Image Pixel Size.
;# ============================

sub getImageSize #($file_name)
{
  local($file_name) = @_;
  local($head);

  return if (!open IN, $file_name);
  binmode IN;
  read IN, $head, 8;
  if ($head eq "\x89\x50\x4e\x47\x0d\x0a\x1a\x0a") {
    local($width, $height);
    if (read(IN, $head, 4) != 4 || read(IN, $head, 4) != 4 || $head ne 'IHDR') {
      close IN;
      return "PNG", 0;
    }
    read IN, $head, 8;
    close IN;
    $width = unpack "N", substr($head, 0, 4);
    $height = unpack "N", substr($head, 4, 4);
    return "PNG", $width, $height;
  }
  $head = substr $head, 0, 3;
  if ($head eq "\x47\x49\x46") {
    local($head, $width, $height);
    seek IN, 6, 0;
    read IN, $head, 4;
    close IN;
    ($width, $height) = unpack "vv", $head;
    return "GIF", $width, $height;
  }
  $head = substr $head, 0, 2;
  if ($head eq "\xff\xd8") {
    local($head, $width, $height, $w1, $w2, $h1, $h2, $l1, $l2, $length);
    seek IN, 2, 0;
    while (read IN, $head, 1) {
      last if ($head eq "");
      if ($head eq "\xff") {
        $head = getc IN;
        if ($head =~ /^[\xc0-\xc3\xc5-\xcf]$/) {
          seek IN, 3, 1;
          last if (read(IN, $head, 4) != 4);
          close IN;
          ($h1, $h2, $w1, $w2) = unpack "C4", $head;
          $height = $h1 * 256 + $h2;
          $width  = $w1 * 256 + $w2;
          return "JPG", $width, $height;
        } elsif ($head eq "\xd9" || $head eq "\xda") {
          last;
        } else {
          last if (read(IN, $head, 2) != 2);
          ($l1, $l2) = unpack "CC", $head;
          $length = $l1 * 256 + $l2;
          seek IN, $length - 2, 1;
        }
      }
    }
    close IN;
    return "JPG", 0;
  }
  close IN;
  return 0;
}

;# ============================
;# Get MIME Type.
;# ============================

sub getMimeType #($file_name)
{
  local($file_name) = @_;
  local(%mime_type) = (
    'asc'   => 'text/plain',    'css'   => 'text/css',      'csv'   => 'text/plain',    'hdml'  => 'text/x-hdml',
    'htm'   => 'text/html',     'html'  => 'text/html',     'mld'   => 'text/plain',    'rtf'   => 'text/rtf',
    'rtx'   => 'text/richtext', 'stm'   => 'text/html',     'shtml' => 'text/html',     'txt'   => 'text/plain',
    'vcf'   => 'text/x-vcard',  'xml'   => 'text/xml',      'xsl'   => 'text/xsl',      'xul'   => 'text/xul',

    'bmp'   => 'image/bmp',     'gif'   => 'image/gif',     'ico'   => 'image/x-icon',  'jpeg'  => 'image/jpeg',
    'jpg'   => 'image/jpeg',    'png'   => 'image/png',     'tif'   => 'image/tiff',    'tiff'  => 'image/tiff',

    'au'    => 'audio/basic',   'es'    => 'audio/echospeech',                          'esl'   => 'audio/echospeech',
    'm3u'   => 'audio/x-mpegurl',                           'midi'  => 'audio/midi',    'mid'   => 'addio/midi',
    'mp2'   => 'audio/mpeg',    'mp3'   => 'audio/mpeg',    'qcp'   => 'audio/vnd.qcelp',
    'rpm'   => 'audio/x-pn-RealAudio-plugin',               'smd'   => 'audio/x-smd',   'wav'   => 'audio/x-wav',
    'wma'   => 'audio/x-ms-wma',

    '3gp'   => 'video/3gpp',    '3gp2'  => 'video/3gpp2',   'asf'   => 'video/x-ms-asf','amc'   => 'application/x-mpeg',
    'avi'   => 'video/msvideo', 'mmf'   => 'application/x-smaf',                        'mov'   => 'video/quicktime',
    'mp4'   => 'video/mp4',     'mpg'   => 'video/mpeg',    'mpeg'  => 'video/mpeg',    'mpg4'  => 'video/mp4',
    'qt'    => 'video/quicktime',                           'vdo'   => 'video/vdo',     'viv'   => 'video/vivo',
    'vivo'  => 'video/vivo',    'wmv'   => 'video/x-ms-wmv','wvx'   => 'video/x-ms-wvx',

    'doc'   => 'application/msword',                        'gz'    => 'application/x-gzip',
    'hlp'   => 'application/winhlp',                        'js'    => 'application/x-javascript',
    'lha'   => 'application/x-lzh',                         'lzh'   => 'application/x-lzh',
    'pdf'   => 'application/pdf',                           'ppt'   => 'application/vnd.ms-powerpoint',
    'pmd'   => 'application/x-pmd',                         'sea'   => 'application/x-stuffit',
    'sh'    => 'application/x-sh',                          'sit'   => 'application/x-stuffit',
    'swf'   => 'application/x-shockwave-flash',             'tar'   => 'application/x-tar',
    'taz'   => 'application/x-tar',                         'tgz'   => 'application/x-tar',
    'xhtml' => 'application/xhtml+xml',                     'wmf'   => 'application/x-msmetafile',
    'xls'   => 'application/vnd.ms-excel',                  'zip'   => 'application/zip',

    'uu'    => 'x-uuencode',    'uue'   => 'x-uuencode',
  );

  $file_name =~ tr/A-Z/a-z/;
  $file_name = ($file_name =~ /\.?(\w+)$/) ? $1 : "";
  return defined $mime_type{$file_name} ? $mime_type{$file_name} : 'application/octet-stream';
}
1;
