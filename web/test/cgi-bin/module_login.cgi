#!/usr/bin/perl
	use Logger::MyLogger;
	my $logger = Logger::MyLogger->new;

	our $_CONFIG_module_login_title;
	our $_CONFIG_base_head;
	require './config_data.cgi';
	require './subroutine.pl';
	
	#パスワードファイル
	$password_file = './member/login_data.cgi';
	#クッキーの有効期間 1:セッション内 0:最終実行後30日間有効
	$session = 1;
	&formLoading;
	
	#if ($FORM{'ID'} =~ /\W/ || $FORM{'PASSWORD'} =~ /\W/) { &error("エラー", $_CONFIG_error_msg[9901]);}
	
	#クッキー取得
	my $cookie_path = $_CONFIG_init_folder;
	my $cookies = $ENV{'HTTP_COOKIE'};
	
	@pairs = split(/;/,$cookies);
	foreach $pair (@pairs) {
		($name,$value,$expires) = split(/=/,$pair);
		$name =~ s/ //g;
		$COOKIE{$name} = $value;
		$COOKIE_expires{$name} = $expires;
	}


	my $_COOKIE_lid = &getLoginCookie('ID', $ENV{'HTTP_COOKIE'}, $logger);
	my $_COOKIE_lpw = &getLoginCookie('PASSWORD', $ENV{'HTTP_COOKIE'}, $logger);
	my $_COOKIE_lst = &getLoginCookie('LOGIN_STATUS', $ENV{'HTTP_COOKIE'}, $logger);
	$COOKIE{'ID'}            = $_COOKIE_lid;
	$COOKIE{'PASSWORD'}      = $_COOKIE_lpw;
	$COOKIE{'LOGIN_STATUS'}  = $_COOKIE_lst;

	$FORM{'LOGIN_STATUS'} = $_COOKIE_lst;

&outputLog ("FORM{'loginKeep'}              :$FORM{'loginKeep'}");
&outputLog ("FORM{'ID'}                     :$FORM{'ID'}");
&outputLog ("FORM{'PASSWORD'}               :$FORM{'PASSWORD'}");
&outputLog ("FORM{'action'}                 :$FORM{'action'}");
&outputLog ("FORM{'LOGIN_STATUS'}           :$FORM{'LOGIN_STATUS'}");
&outputLog ("COOKIE{'ID'}                   :$COOKIE{'ID'}");
&outputLog ("COOKIE_expires{'ID'}           :$COOKIE_expires{'ID'}");
&outputLog ("COOKIE{'PASSWORD'}             :$COOKIE{'PASSWORD'}");
&outputLog ("COOKIE_expires{'PASSWORD'}     :$COOKIE_expires{'PASSWORD'}");
&outputLog ("COOKIE{'LOGIN_STATUS'}         :$COOKIE{'LOGIN_STATUS'}");
&outputLog ("COOKIE_expires{'LOGIN_STATUS'} :$COOKIE_expires{'LOGIN_STATUS'}");
&outputLog ("cookies                        :$cookies");



#分岐
if ($FORM{'action'} eq 'logout') {
	&cookie;
	#$cook="ID\:\,PASSWORD\:";
	my $setCookie1 = "Set-Cookie: ID= ; path=$cookie_path; expires=$date_gmt\n";
	my $setCookie2 = "Set-Cookie: PASSWORD= ; path=$cookie_path; expires=$date_gmt\n";
	my $setCookie3 = "Set-Cookie: LOGIN_STATUS=; path=$cookie_path; expires=$date_gmt\n";

	print $setCookie1;
	print $setCookie2;
	print $setCookie3;

&outputLog ($setCookie1);
&outputLog ($setCookie2);
&outputLog ($setCookie3);


	&input_form;
} elsif ($FORM{'ID'} ne '' && $FORM{'PASSWORD'} ne '') {
	$FORM{'PASSWORD'} = &cipher($FORM{'PASSWORD'});
	&passwd;
	&access_ok($FORM{'ID'});
} elsif ($COOKIE{'ID'} ne '' && $COOKIE{'PASSWORD'} ne '') {
	$FORM{'ID'} = $COOKIE{'ID'};
	$FORM{'PASSWORD'} = $COOKIE{'PASSWORD'};
	&passwd;
	&access_ok($FORM{'ID'});
} elsif ($FORM{'ID'} ne '') {
	&error('', $_CONFIG_error_msg[9901]);
} elsif ($FORM{'PASSWORD'} ne '') {
	&error('', $_CONFIG_error_msg[9901]);
} else {
	&input_form;
}

sub input_form {
	print $_CONFIG_base_head;
print <<"EOF";
						<div class="div_moduleLeft">
							<form class="form_module" name="ajaxForm" onSubmit="login();return false;">
								<!-- <input type="hidden" name="action" size="16" maxlength="16"  > -->
								<div class="div_userNinsyouModuleCenter">
									$_CONFIG_module_login_title
								</div>
									ID<br>
									<input type="text" name="ID" size="16"maxlength="16" class="input_tyuumonsuu text_font"><BR>
									パスワード<br>
									<input type="password" name="PASSWORD" size="16"maxlength="16" class="input_tyuumonsuu text_font"><BR>
									<input type="checkbox" name="loginKeep" value="1"> ログイン状態を保持する<BR>
								<div class="div_userNinsyouModuleCenter">
									<input type="submit" value="ログイン">
								</div>
							</form>
						</div>
EOF
	exit;
}

sub cookie {

	if ($FORM{'loginKeep'} eq '1' || $FORM{'LOGIN_STATUS'} eq '1') {

&outputLog ("expires OK");

		($secg,$ming,$hourg,$mdayg,$mong,$yearg,$wdayg,$ydayg,$isdstg) = gmtime(time + 180*24*60*60);
		$y0="Sunday"; $y1="Monday"; $y2="Tuesday"; $y3="Wednesday"; $y4="Thursday"; $y5="Friday"; $y6="Saturday";
		@youbi = ($y0,$y1,$y2,$y3,$y4,$y5,$y6);
		$m0="Jan"; $m1="Feb"; $m2="Mar"; $m3="Apr"; $m4="May"; $m5="Jun";
		$m6="Jul"; $m7="Aug"; $m8="Sep"; $m9="Oct"; $m10="Nov"; $m11="Dec";
		@monthg = ($m0,$m1,$m2,$m3,$m4,$m5,$m6,$m7,$m8,$m9,$m10,$m11);
		$date_gmt = sprintf("%s\, %02d\-%s\-%04d %02d:%02d:%02d GMT",$youbi[$wdayg],$mdayg,$monthg[$mong],$yearg +1900,$hourg,$ming,$secg);
	}
	else {
		$date_gmt = '';
&outputLog ("expires NG");
	}
}

sub passwd {
	if (!open(DB,"$password_file")) { &error("エラー","パスワードファイルを処理できません."); }
	@lines = <DB>;
	close(DB);
	
	my $id;
	my $pwd;
	my $hit_check = 0;
	foreach my $line (@lines) {
		($id, $pwd) = split(/\t/, $line);
		$id =~ s/\s*$//;
		my $ans = &decipher($pwd, $FORM{'PASSWORD'});
		if (($FORM{'ID'} eq $id) && ($ans)) {
			$hit_check++;
			&cookie;
			#$cook = "ID=$FORM{'ID'}\,PASSWORD=$FORM{'PASSWORD'}";
			#print "Set-Cookie: $cookie_path=$cook; path=$cookie_path; expires=$date_gmt\n";
			my $setCookie1 = "Set-Cookie: ID=$FORM{'ID'}; path=$cookie_path; expires=$date_gmt\n";
			my $setCookie2 = "Set-Cookie: PASSWORD=$FORM{'PASSWORD'}; path=$cookie_path; expires=$date_gmt\n";
			
			my $status = '';
			if($date_gmt){
				$status = '1';
			}
			my $setCookie3 = "Set-Cookie: LOGIN_STATUS=$status; path=$cookie_path; expires=$date_gmt\n";
			print $setCookie1;
			print $setCookie2;
			print $setCookie3;

&outputLog ($setCookie1);
&outputLog ($setCookie2);
&outputLog ($setCookie3);

			last;
		}
	}
	if ($hit_check == 0) {
		&error('', $_CONFIG_error_msg[9901]);
	}
}

sub error {

	print $_CONFIG_base_head;
print <<"EOF";
						<div class="div_moduleLeft">
							<form class="form_module" name="ajaxForm" onSubmit="login();return false;">
								<!-- <input type="hidden" name="action" size="16"maxlength="16" class="input_tyuumonsuu text_font" /> -->
								<div class="div_userNinsyouModuleCenter">
									$_CONFIG_module_login_title
								</div>
								<div class="div_userNinsyouModuleCenter">
									ユーザーID・パスワードに誤りがあるか、登録されていません。
								</div>
									ID<br>
									<input type="text" name="ID" size="16" maxlength="16" class="input_tyuumonsuu text_font" /><BR>
									パスワード<br>
									<input type="password" name="PASSWORD" size="16" maxlength="16" class="input_tyuumonsuu text_font" /><BR>
									<input type="checkbox" name="loginKeep" value="1"> ログイン状態を保持する<BR>
								<div class="div_userNinsyouModuleCenter">
									<input type="submit" value="ログイン">
									<BR>$_[1]
								</div>
							</form>
						</div>
EOF
	exit;
}

sub access_ok {
	print $_CONFIG_base_head;
	print <<"EOF";
						<div class="div_moduleLeft">
							<form class="form_module" name="ajaxForm" onSubmit="logout();return false;">
								<!-- <input type="hidden" name="action" size="16" maxlength="16" class="input_tyuumonsuu text_font"> -->
								<div class="div_userNinsyouModuleCenter">
									$_CONFIG_module_login_title
								</div>
								ようこそ@_さん
								<div class="div_userNinsyouModuleCenter">
									<input type="submit" value="ログアウト">
								</div>
							</form>
						</div>
EOF
	exit;
}
sub decipher{
	my ($passwd1, $passwd2) = @_;

	my $crypt_passwd = '';

	if(8 < length ($passwd1)) {
		$crypt_passwd = crypt( $passwd1, $passwd2 ) . crypt( substr($passwd1, 8, length ($passwd1) - 8), $passwd2 );
	} else {
		$crypt_passwd = crypt( $passwd1, $passwd2 );
	}

&outputLog ("decipher crypt_passwd          :$crypt_passwd");
&outputLog ("decipher passwd2               :$passwd2");
	# 暗号のチェック
	if ( $crypt_passwd eq $passwd2 ) {
		return 1;
	} else {
		return 0;
	}
}
sub cipher {
	my ($val) = @_;
	
	my( $sec, $min, $hour, $day, $mon, $year, $weekday ) 
		= localtime( time );
	my( @token ) = ( '0'..'9', 'A'..'Z', 'a'..'z' );
	$salt = $token[(time | $$) % scalar(@token)];
	$salt .= $token[($sec + $min*60 + $hour*60*60) % scalar(@token)];

	my $crypt_passwd = '';

	if(8 < length ($val)) {
		$crypt_passwd = crypt( $val, $salt ) . crypt( substr($val, 8, length ($val) - 8), $salt );
	} else {
	$crypt_passwd = crypt( $val, $salt );
	}
                                            
&outputLog ("cipher crypt_passwd            :$crypt_passwd");

	return $crypt_passwd;

}
