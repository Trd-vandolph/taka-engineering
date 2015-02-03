#!/usr/bin/perl
#!/usr/bin/perl
use utf8;
use strict;
use English;
use MODULE::Jcode;
use MODULE::Template;
use MODULE::StringUtil;
use CGI::Session qw/-ip_match/;
use CGI::Session::Cleaning;
use POSIX;

	our %FORM;
	our $_CONFIG_base_head;
	our $_CONFIG_site_title;
	our $_CONFIG_site_outline_site;
	our @_CONFIG_site_keyword;
	our $_CONFIG_server_ssl_www_root;
	our $_CONFIG_page_view_mode;
	our $_CONFIG_server_ssl_use;
	our $_CONFIG_template_dir;
	our $_CONFIG_server_url;

	my $ask_button        = "";
	my $ask_bottom_cancel = "";
	my $ask_button_flg    = "";
	my $error_flg = 0;
	
	our $_CONFIG_session_dir;
	our $_CONFIG_session_file_header;

	require './subroutine.pl';
	require './config_data.cgi';
	my $load_file  = "$_CONFIG_server_ssl_www_root/cgi-bin/ask/ask_config.cgi";
	my $parts_file = "$_CONFIG_server_ssl_www_root/cgi-bin/ask/ask_parts.cgi";
	
	our $session_pass = "$_CONFIG_server_ssl_www_root/cgi-bin/$_CONFIG_session_dir";

	open(FILE, $load_file);
	my @load_file = <FILE>;
	close(FILE);
	open(FILE, $parts_file);
	my @parts_file = <FILE>;
	close(FILE);
	
	&formLoading;

#Session->Start
    #SSL／非SSLの前処理
	unless ($_CONFIG_server_ssl_use ne '0' && $_CONFIG_page_view_mode ne 'P') {
		$_CONFIG_server_ssl_www_root = '..';
	}

	#セッション名、セッションタイムの定義
	my $session_name = 'sessionCart';
	my $session_timer = 30;

	#Cookie???ZbVID擾
	our %COOKIE;
#	&getCookie($session_name);
#	if ($FORM{'seid'} ne '' && $_CONFIG_server_ssl_use eq '1' && $_CONFIG_page_view_mode ne 'P') {
		$COOKIE{$session_name} = $FORM{'seid'};
#	}

	#セッションオブジェクト生成
	my $session;
	my $session_id;
#	&cleanSession;
	$session      = CGI::Session->new(undef, $COOKIE{$session_name}, {Directory=>$session_pass});
	foreach (@parts_file) {
		my @parts_line = split(/\t/, $_);
		if ($FORM{'pid'} eq $parts_line[1] && $parts_line[11] == 1) {
			$session->param("ask_input_value_$parts_line[0]", $FORM{"ask_input_value_$parts_line[0]"});
			$session->param("ask_input_value_$parts_line[0]_1", $FORM{"ask_input_value_$parts_line[0]_1"});
			$session->param("ask_input_value_$parts_line[0]_2", $FORM{"ask_input_value_$parts_line[0]_2"});
			$session->param("ask_input_value_$parts_line[0]_3", $FORM{"ask_input_value_$parts_line[0]_3"});
			$session->param("ask_input_value_$parts_line[0]_4", $FORM{"ask_input_value_$parts_line[0]_4"});
			if ($parts_line[6] eq 'C') {
				my $session_value = '';
				my @option_list = split(/<RETURN>/, $parts_line[9]);
				chomp @option_list;
				my $i = 1;
				foreach (@option_list) {
					if ($FORM{"ask_input_value_$parts_line[0]_$i"} == 1) {
						$session->param("ask_input_value_$parts_line[0]_$i", '1');
						$session_value .= '-' if $session_value;
						$session_value .= $i;
					}
					$i++;
				}
				if ($session_value ne '') {
					$session->param("ask_input_value_$parts_line[0]", $session_value);
				}
			}
		}
	}
	foreach (@parts_file) {
		my @parts_line = split(/\t/, $_);
		if ($FORM{'pid'} eq $parts_line[1] && $parts_line[11] == 1) {
			$FORM{"ask_input_value_$parts_line[0]"}   = $session->param("ask_input_value_$parts_line[0]");
			$FORM{"ask_input_value_$parts_line[0]_1"} = $session->param("ask_input_value_$parts_line[0]_1");
			$FORM{"ask_input_value_$parts_line[0]_2"} = $session->param("ask_input_value_$parts_line[0]_2");
			$FORM{"ask_input_value_$parts_line[0]_3"} = $session->param("ask_input_value_$parts_line[0]_3");
			$FORM{"ask_input_value_$parts_line[0]_4"} = $session->param("ask_input_value_$parts_line[0]_4");
			if ($parts_line[6] eq 'C') {
				my @check_value_list = split(/\-/, $FORM{"ask_input_value_$parts_line[0]"});
				foreach (@check_value_list) {
					$FORM{"ask_input_value_$parts_line[0]_$_"} = 1;
				}
			}
		}
	}
	$session_id   = $session->id;
	$session->expire('+'.$session_timer.'m');
#Session化->End


	our $template = HTML::Template->new(filename => "./$_CONFIG_template_dir/ask_check.tmp");
	
	my $i = 1;
	my $necessity_check = 0;
	my @loop_hash = ();
	my @error_loop = ();
	my $email_error_name;
	my $area_error_name;
	my $area_error_count;
	my $address_error_flg;
	my $address_error_name;
	my $date_error_flg;
	my $date_error_name;
	my $zen_num_error_name;
	@parts_file = sort { (split(/\t/,$a))[3] <=> (split(/\t/,$b))[3] } @parts_file;
	foreach (@parts_file) {
		my @parts_line = split(/\t/, $_);
		my ($ask_view_flg, $address_flg, $date_flg);
		if ($FORM{'pid'} eq $parts_line[1] && $parts_line[11] == 1) {
			my $view_value;
			my $submit_value;
			my $insert_hash = "";
			my $input_value_1;
			my $input_value_2;
			my $input_value_3;
			my $input_value_4;
			my $input_value_area;
			my $view_value_1;
			my $view_value_2;
			my $view_value_3;
			my $view_value_4;
			my $view_value_area;
			my $view_value_flg;
			my $date_view_value_flg;
			$necessity_check++ if $parts_line[10] == 1;
			if ($parts_line[6] eq 'C') {
				#_チェックボックス
				my $check_check_box;
				my @option_list = split(/<RETURN>/, $parts_line[9]);
				chomp @option_list;
				my $i = 1;
				foreach (@option_list) {
					if ($FORM{"ask_input_value_$parts_line[0]_$i"} == 1) {
						$view_value   .= '<BR>' if $view_value;
						$view_value   .= $_;
						$submit_value .= '-' if $submit_value;
						$submit_value .= $i;
						$check_check_box++;
					}
					$i++;
				}
				if ($check_check_box eq '' && $parts_line[10] == 1) {
					$error_flg = 1;
					$insert_hash = {
						must_error_ask_name => $parts_line[4],
						error_input_flg     => '1',
					};
					push(@error_loop, $insert_hash);
				}
				$ask_view_flg = 1;
			} elsif ( $parts_line[6] eq 'J') {
				#_住所入力欄タイプ
				$FORM{"ask_input_value_$parts_line[0]_1"}  = &strTrim($FORM{"ask_input_value_$parts_line[0]_1"});
				$FORM{"ask_input_value_$parts_line[0]_2"}  = &strTrim($FORM{"ask_input_value_$parts_line[0]_2"});
				$FORM{"ask_input_value_$parts_line[0]_4"}  = &strTrim($FORM{"ask_input_value_$parts_line[0]_4"});
				$input_value_1    = $FORM{"ask_input_value_$parts_line[0]_1"};
				$input_value_2    = $FORM{"ask_input_value_$parts_line[0]_2"};
				$input_value_area = $FORM{"ask_input_value_$parts_line[0]_3"} if ($FORM{"ask_input_value_$parts_line[0]_3"});
				$input_value_4    = $FORM{"ask_input_value_$parts_line[0]_4"};
				$view_value_1         = $FORM{"ask_input_value_$parts_line[0]_1"};
				$view_value_2         = $FORM{"ask_input_value_$parts_line[0]_2"};
				$view_value_area      = $FORM{"ask_input_value_$parts_line[0]_3"} if ($FORM{"ask_input_value_$parts_line[0]_3"});
				$view_value_4         = $FORM{"ask_input_value_$parts_line[0]_4"};
				#_住所必須チェック
				if ( $input_value_1 eq '' || $input_value_2 eq '' || $input_value_area eq '' || $input_value_4 eq '') {
					if ($parts_line[10] == 1) {
						$error_flg = 1;
						$insert_hash = {
							must_error_ask_name => $parts_line[4],
							error_input_flg     => '1',
						};
						push(@error_loop, $insert_hash);
					}
				}
				#_住所チェック
				if ($parts_line[6] eq 'J' && $input_value_1 && $input_value_2) {
					if ($input_value_1) {
						unless (&strIntCheck($input_value_1)) {
							$address_error_name = $parts_line[4],
							$error_flg          = 1;
							$address_error_flg  = 1;
						}
					}
					if ($input_value_2) {
						unless (&strIntCheck($input_value_2)) {
							$address_error_name = $parts_line[4],
							$error_flg          = 1;
							$address_error_flg  = 1;
						}
					}
				}
				if ($input_value_1 eq '') {
					if ($input_value_2 eq '') {
						$view_value_flg = 0;
					} else {
						$view_value_flg = 1;
					}
				} else {
					$view_value_flg = 1;
				}
				my @area_flg;
				$area_flg[$FORM{"ask_input_value_$parts_line[0]_3"}] = 1;
				$address_flg = 1;
			}
			 elsif ( $parts_line[6] eq 'B') {
				#_年月日入力欄タイプ
				$FORM{"ask_input_value_$parts_line[0]_1"}  = &strTrim($FORM{"ask_input_value_$parts_line[0]_1"});
				$FORM{"ask_input_value_$parts_line[0]_2"}  = &strTrim($FORM{"ask_input_value_$parts_line[0]_2"});
				$FORM{"ask_input_value_$parts_line[0]_3"}  = &strTrim($FORM{"ask_input_value_$parts_line[0]_3"});
				$input_value_1 = $FORM{"ask_input_value_$parts_line[0]_1"};
				$input_value_2 = $FORM{"ask_input_value_$parts_line[0]_2"};
				$input_value_3 = $FORM{"ask_input_value_$parts_line[0]_3"};
				$view_value_1      = $FORM{"ask_input_value_$parts_line[0]_1"};
				$view_value_2      = $FORM{"ask_input_value_$parts_line[0]_2"};
				$view_value_3      = $FORM{"ask_input_value_$parts_line[0]_3"};
				#_年月日必須チェック
				if ($input_value_1 eq '' || $input_value_2 eq '' || $input_value_3 eq '') {
					if ($parts_line[10] == 1) {
						$error_flg = 1;
						$insert_hash = {
							must_error_ask_name => $parts_line[4],
							error_input_flg     => '1',
						};
						push(@error_loop, $insert_hash);
					} 
				}
				#_日付チェック
				if ($input_value_1 ne '' || $input_value_2 ne '' || $input_value_3 ne '') {
					unless (&strDateCheck($input_value_1, $input_value_2, $input_value_3)) {
						$error_flg       = 1;
						$date_error_flg  = 1;
						$date_error_name = $parts_line[4];
					}
				}
				unless ($input_value_1 ne '' && $input_value_2 ne '' && $input_value_3 ne '') {
					$date_view_value_flg = 0;
				} else {
					$date_view_value_flg = 1;
				}
				$date_flg = 1;
			}
			else {
				#_チェックボックス・住所・年月日以外
				$FORM{"ask_input_value_$parts_line[0]"} = &strTrim($FORM{"ask_input_value_$parts_line[0]"});
				$view_value   = $FORM{"ask_input_value_$parts_line[0]"};
				$submit_value = $FORM{"ask_input_value_$parts_line[0]"};
				if ($FORM{"ask_input_value_$parts_line[0]"} eq '' && $parts_line[10] == 1) {
				#_必須チェック
					$error_flg = 1;
					$insert_hash = {
						must_error_ask_name => $parts_line[4],
						error_input_flg     => '1',
					};
					push(@error_loop, $insert_hash);
				}
				#_テキストエリアチェック
				if ($parts_line[6] eq 'A') {
					my $str = $FORM{"ask_input_value_$parts_line[0]"};
					#_文字数チェック（最大全角1000文字）
					if (length(Jcode::convert($str, 'sjis', 'utf8')) > 2000) {
						$error_flg = 1;
						$area_error_name  = $parts_line[4];
						$area_error_count = 1000;
					}
				}
				#_メールアドレスチェック
				if ($parts_line[6] eq 'M' && $FORM{"ask_input_value_$parts_line[0]"} ne '') {
					unless (&mailChecker($FORM{"ask_input_value_$parts_line[0]"})){
						$error_flg        = 1;
						$email_error_name = $parts_line[4];
					}
				}
				if ($parts_line[6] eq 'R') {
					my @option_list = split(/<RETURN>/, $parts_line[9]);
					chomp @option_list;
					my $i = 1;
					foreach (@option_list) {
						if ($FORM{"ask_input_value_$parts_line[0]"} == $i) {
							$view_value = $_;
							last;
						}
						$i++;
					}
				}
				if ($parts_line[6] eq 'S') {
					my @option_list = split(/<RETURN>/, $parts_line[9]);
					chomp @option_list;
					my $i = 1;
					foreach (@option_list) {
						if ($FORM{"ask_input_value_$parts_line[0]"} == $i) {
							$view_value = $_;
							last;
						}
						$i++;
					}
				}
				if ($parts_line[6] eq 'N' && $FORM{"ask_input_value_$parts_line[0]"} ne '') {
					unless (&strZenNumberCheck($FORM{"ask_input_value_$parts_line[0]"})){
						$error_flg          = 1;
						$zen_num_error_name = $parts_line[4];
					}
				}
				$ask_view_flg = 1;
			}
			unless ($error_flg) {
				my $insert_hash = "";
				my $input_icon;
				if ($parts_line[5]) {
					$input_icon = &checkUri($parts_line[5], 1);
				}
				$parts_line[5] = &checkUri($parts_line[5], 1) if $parts_line[5];
				if ($parts_line[6] eq 'C' ) {
					$view_value = &strBr($view_value);
				}
				elsif ($parts_line[6] eq 'J' ) {
					$view_value_1    = &strBr(MODULE::StringUtil::conversionSpecialChar($view_value_1));
					$view_value_2    = &strBr(MODULE::StringUtil::conversionSpecialChar($view_value_2));
					$view_value_area = &strBr(MODULE::StringUtil::conversionSpecialChar(&prefOut($view_value_area)));
					$view_value_4    = &strBr(MODULE::StringUtil::conversionSpecialChar($view_value_4));
				}
				elsif ($parts_line[6] eq 'B' ) {
					$view_value_1    = &strBr(MODULE::StringUtil::conversionSpecialChar($view_value_1));
					$view_value_2    = &strBr(MODULE::StringUtil::conversionSpecialChar($view_value_2));
					$view_value_3    = &strBr(MODULE::StringUtil::conversionSpecialChar($view_value_3));
				}
				elsif ($parts_line[6] eq 'N' ) {
					$view_value = &strZenNumberTrim(&strBr(MODULE::StringUtil::conversionSpecialChar($view_value)));
					$submit_value =  &strZenNumberTrim($submit_value);
				}
				else {
					$view_value = &strBr(MODULE::StringUtil::conversionSpecialChar($view_value));
				}
				$insert_hash = {
					ask_input_nom       => $parts_line[0],
					ask_input_title     => $parts_line[4],
					ask_input_icon      => $parts_line[5],
					ask_input_necessity => $parts_line[10],
					ask_view_flg        => $ask_view_flg,
					address_flg         => $address_flg,
					date_flg            => $date_flg,
					ask_input_value     => &strBrDouble(MODULE::StringUtil::conversionSpecialChar($submit_value)),
					input_value_1       => &strBrDouble(MODULE::StringUtil::conversionSpecialChar($input_value_1)),
					input_value_2       => &strBrDouble(MODULE::StringUtil::conversionSpecialChar($input_value_2)),
					input_value_3       => &strBrDouble(MODULE::StringUtil::conversionSpecialChar($input_value_3)),
					input_value_4       => &strBrDouble(MODULE::StringUtil::conversionSpecialChar($input_value_4)),
					input_value_area    => &strBrDouble(MODULE::StringUtil::conversionSpecialChar(&prefOut($input_value_area))),
					ask_input_view      => $view_value,
					view_value_1        => $view_value_1,
					view_value_2        => $view_value_2,
					view_value_3        => $view_value_3,
					view_value_4        => $view_value_4,
					view_value_area     => $view_value_area,
					date_view_value_flg => $date_view_value_flg,
					view_value_flg      => $view_value_flg,
				};
				push(@loop_hash, $insert_hash);
			}
		}
	}

	#_エラー処理
	if ($error_flg) {
		$template = HTML::Template->new(filename => "./$_CONFIG_template_dir/ask.tmp");
		my  $ask_button;
		my  $ask_button_flg;
		my ($FORM_LOOP, $ask_necessity_check) = &askFormOutput(1, \@parts_file);
		my @return_line    = &askFormMeta(\@load_file);
		$ask_button        = $return_line[1];
		if (@$FORM_LOOP < 1) {
			$ask_button_flg = ' disabled';
		}
		my $top_url;
		if (($_CONFIG_server_ssl_use == 1) && ($_CONFIG_page_view_mode ne 'P')) {
			$top_url = sprintf('%s/', $_CONFIG_server_url);
		} else {
			$top_url = '../';
		}
		$template->param(
			ask_page_id         => MODULE::StringUtil::conversionSpecialChar($FORM{'pid'}),
			ask_button          => $ask_button,
			ask_necessity_check => $ask_necessity_check,
			ask_button_flg      => $ask_button_flg,
			FORM_LOOP           => \@$FORM_LOOP,
			error_flg           => $error_flg,
			MUST_ERROR_LOOP     => \@error_loop,
			email_error_name    => $email_error_name,
			address_error_flg   => $address_error_flg,
			address_error_name  => $address_error_name,
			date_error_flg      => $date_error_flg,
			date_error_name     => $date_error_name,
			area_error_name     => $area_error_name,
			area_error_count    => $area_error_count,
			zen_num_error_name  => $zen_num_error_name,
			top_url             => $top_url,
			seid                => $session_id,
		);
		print $_CONFIG_base_head;
		print $template -> output;
	}
	
	my @return_line    = &askFormMeta(\@load_file);
	$ask_button        = $return_line[2];
	$ask_bottom_cancel = $return_line[3];
	
	if ($error_flg > 0) {
		$ask_button_flg = ' disabled';
	}
	
	$template->param(
		ask_page_id         => MODULE::StringUtil::conversionSpecialChar($FORM{'pid'}),
		ask_necessity_check => $necessity_check,
		ask_button          => $ask_button,
		ask_bottom_cancel   => $ask_bottom_cancel,
		ask_button_flg      => $ask_button_flg,
		error_on_flg        => $error_flg,
		LOOP                => \@loop_hash,
		seid                => $session_id,
	);
	
	print $_CONFIG_base_head;
	print $template -> output;


	$session->flush();

	&chmodSessionFile ($session_pass . "/", $_CONFIG_session_file_header, $session_id);

exit;
