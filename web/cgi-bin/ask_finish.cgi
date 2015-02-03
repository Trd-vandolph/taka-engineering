#!/usr/bin/perl
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
	our @_CONFIG_error_msg;
	our $_CONFIG_carriage_contact;
	our $SUBSTR_ask_mail_1;
	our $return_open;
	our $ret_close;
	our $return_msg;
	our $sendmail;
	our $_CONFIG_server_ssl_use;
	our $_CONFIG_server_url;
	our $_CONFIG_page_view_mode;
	our $_CONFIG_site_title;
	our $_CONFIG_site_outline_site;
	our @_CONFIG_site_keyword;
	our $_CONFIG_server_ssl_www_root;
	our $_CONFIG_server_ssl_site_addr;
	our $_CONFIG_server_mail_address;
	our $_CONFIG_template_dir;
	
	my $ask_recieve_mail       = "";
	my $ask_mail_subject       = "";
	my $ask_mail_header        = "";
	my $ask_mail_footer        = "";
	my $ask_comment            = "";
	my $ask_mail_subject_owner = 'お問い合わせがありました。';
#	my $ask_user_mail_do       = $_CONFIG_server_mail_address;
	my $ask_user_mail_do       = "";
	
	our $_CONFIG_session_dir;
	our $_CONFIG_session_file_header;


	require './subroutine.pl';
	require './config_data.cgi';
	require "$_CONFIG_server_ssl_www_root/cgi-bin/mail/send_mail.pl";
	
	our $session_pass = "$_CONFIG_server_ssl_www_root/cgi-bin/$_CONFIG_session_dir";

	$ask_user_mail_do = $_CONFIG_server_mail_address;
	
	my $load_file          = "$_CONFIG_server_ssl_www_root/cgi-bin/ask/ask_config.cgi";
	my $parts_file         = "$_CONFIG_server_ssl_www_root/cgi-bin/ask/ask_parts.cgi";
	my $mailTemplate_user  = "$_CONFIG_server_ssl_www_root/cgi-bin/mail/mailTemplate_ask_user.cgi";
	my $mailTemplate_owner = "$_CONFIG_server_ssl_www_root/cgi-bin/mail/mailTemplate_ask_owner.cgi";
	my $ask_user_mail;
	
	open(FILE, $load_file);
	my @load_file = <FILE>;
	close(FILE);
	open(FILE, $parts_file);
	my @parts_file = <FILE>;
	close(FILE);
	open(FILE, $mailTemplate_user);
	our @mailTemplate_user = <FILE>;
	close(FILE);
	open(FILE, $mailTemplate_owner);
	our @mailTemplate_owner = <FILE>;
	&outputLog("mailTemplate_owner");
	&outputLog(<FILE>);
	close(FILE);
	
	&formLoading;
	
#Session化->Start
    #SSL／非SSLの前処理
	unless ($_CONFIG_server_ssl_use ne '0' && $_CONFIG_page_view_mode ne 'P') {
		$_CONFIG_server_ssl_www_root = '..';
	}

	#セッション名、セッションタイムの定義
	my $session_name = 'sessionCart';
	my $session_timer = 30;

	#Cookieより現在のセッションIDを取得
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
	
	$session->close;
	$session->delete;
#Session化->End


	
	our $template = HTML::Template->new(filename => "./$_CONFIG_template_dir/ask_finish.tmp");
	
	my @return_line    = &askFormMeta(\@load_file);
	$ask_recieve_mail  = $return_line[4];
	$ask_mail_subject  = &errstrRecover($return_line[5]);
	$ask_mail_header   = &errstrRecover($return_line[6]);
	$ask_mail_footer   = &errstrRecover($return_line[7]);
	$ask_comment       = $return_line[8];
	
	$ask_mail_header = &strBr($ask_mail_header, 1);
	$ask_mail_footer = &strBr($ask_mail_footer, 1);
	
	my $i = 1;
	
	#_送信内容の生成
	@parts_file = sort { (split(/\t/,$a))[3] <=> (split(/\t/,$b))[3] } @parts_file;
	foreach (@parts_file) {
		my @parts_line = split(/\t/, $_);
		if ($FORM{'pid'} eq $parts_line[1] && $parts_line[11] == 1) {
			if ($parts_line[6] eq 'B' ) {
				if ($FORM{"ask_input_value_$parts_line[0]_1"} eq "" && $FORM{"ask_input_value_$parts_line[0]_2"} eq "" && $FORM{"ask_input_value_$parts_line[0]_3"} eq "" ) {
					$SUBSTR_ask_mail_1 = $SUBSTR_ask_mail_1 . sprintf ('%s = %s', $parts_line[4], "\n");
				} else {
					$SUBSTR_ask_mail_1 = $SUBSTR_ask_mail_1 . sprintf ('%s = 西暦 %s年%s月%s日%s', $parts_line[4], $FORM{"ask_input_value_$parts_line[0]_1"}, $FORM{"ask_input_value_$parts_line[0]_2"}, $FORM{"ask_input_value_$parts_line[0]_3"}, "\n");
				}
			} elsif ($parts_line[6] eq 'J') {
				if ($FORM{"ask_input_value_$parts_line[0]_1"} eq "" && $FORM{"ask_input_value_$parts_line[0]_2"} eq "") {
					$SUBSTR_ask_mail_1 = $SUBSTR_ask_mail_1 . sprintf ('%s = %s%s%s', $parts_line[4], &prefOut($FORM{"ask_input_value_$parts_line[0]_3"}), $FORM{"ask_input_value_$parts_line[0]_4"}, "\n");
				} else {
					$SUBSTR_ask_mail_1 = $SUBSTR_ask_mail_1 . sprintf ('%s = %s-%s %s%s%s', $parts_line[4], $FORM{"ask_input_value_$parts_line[0]_1"}, $FORM{"ask_input_value_$parts_line[0]_2"}, &prefOut($FORM{"ask_input_value_$parts_line[0]_3"}), $FORM{"ask_input_value_$parts_line[0]_4"}, "\n");
				}
			} else {
				my $ask_send_value;
				if ($parts_line[6] eq 'M' && $FORM{"ask_input_value_$parts_line[0]"}) {
					$ask_user_mail = $FORM{"ask_input_value_$parts_line[0]"};
				}
				if ($parts_line[6] eq 'R') {
					my @option_list = split(/<RETURN>/, $parts_line[9]);
					chomp @option_list;
					my $i = 1;
					foreach (@option_list) {
						if ($FORM{"ask_input_value_$parts_line[0]"} == $i) {
							$ask_send_value = $_;
							last;
						}
						$i++;
					}
				} elsif ($parts_line[6] eq 'S') {
					my @option_list = split(/<RETURN>/, $parts_line[9]);
					chomp @option_list;
					my $i = 1;
					foreach (@option_list) {
						if ($FORM{"ask_input_value_$parts_line[0]"} == $i) {
							$ask_send_value = $_;
							last;
						}
						$i++;
					}
				} elsif ($parts_line[6] eq 'C') {
					my @check_value_list = split(/\-/, $FORM{"ask_input_value_$parts_line[0]"});
					foreach (@check_value_list) {
						$FORM{"ask_input_value_$parts_line[0]_$_"} = 1;
					}
					my @option_list = split(/<RETURN>/, $parts_line[9]);
					chomp @option_list;
					my $i = 1;
					foreach (@option_list) {
						if ($FORM{"ask_input_value_$parts_line[0]_$i"} == 1) {
							$ask_send_value .= "\n" if $ask_send_value;
							$ask_send_value .= "・".$_;
						}
						$i++;
					}
					$ask_send_value = "\n".$ask_send_value;
				} else {
					$ask_send_value = $FORM{"ask_input_value_$parts_line[0]"};
				}
				$SUBSTR_ask_mail_1 = $SUBSTR_ask_mail_1 . sprintf ('%s = %s%s', $parts_line[4], $ask_send_value, "\n");
			}
			$i++;
		}
	}
	
	if ($ask_user_mail) {
		my $i = 0;
		for (my $i = 0; $i < @mailTemplate_user; $i++) {
			if ($mailTemplate_user[$i] =~ /\$ask_mail_header/) {
				$mailTemplate_user[$i] =~ s/\$ask_mail_header/$ask_mail_header/;
			}
			if ($mailTemplate_user[$i] =~ /\$SUBSTR_ask_mail_1/) {
				$mailTemplate_user[$i] =~ s/\$SUBSTR_ask_mail_1/$SUBSTR_ask_mail_1/;
			}
			if ($mailTemplate_user[$i] =~ /\$ask_mail_footer/) {
				$mailTemplate_user[$i] =~ s/\$ask_mail_footer/$ask_mail_footer/;
			}
		}
		&send_mail_Send($ask_recieve_mail, $ask_user_mail, $ask_mail_subject, join ('', @mailTemplate_user));
	} else {
		$ask_user_mail = $ask_user_mail_do;
	}
	
	my $submit_url;
	if ($_CONFIG_server_ssl_use == 1) {
		$submit_url = sprintf('%s送信元URL=%s/cgi-bin/askItem_finish.cgi', "\n\n", $_CONFIG_server_ssl_site_addr);
	} else {
		$submit_url = sprintf('%s送信元URL=%s/cgi-bin/askItem_finish.cgi', "\n\n", $_CONFIG_server_url);
	}
	
	my $i = 0;
	for (my $i = 0; $i < @mailTemplate_owner; $i++) {
		if ($mailTemplate_owner[$i] =~ /\$SUBSTR_ask_mail_1/) {
			$mailTemplate_owner[$i] =~ s/\$SUBSTR_ask_mail_1/$SUBSTR_ask_mail_1/;
		}
	}
	push (@mailTemplate_owner, $submit_url);
	
	if ($_CONFIG_page_view_mode ne 'P') {
		&send_mail_Send($ask_user_mail, $ask_recieve_mail, $ask_mail_subject_owner, join ('', @mailTemplate_owner));
	}
	if ($return_msg ne '') {
		$ask_comment = $return_msg;
	}
	
	my $top_url;
	if (($_CONFIG_server_ssl_use == 1) && ($_CONFIG_page_view_mode ne 'P')) {
		$top_url = sprintf('%s/', $_CONFIG_server_url);
	} else {
		$top_url = '../';
	}
	
	$template->param(
		ask_page_id      => MODULE::StringUtil::conversionSpecialChar($FORM{'pid'}),
		ask_comment      => $ask_comment,
		top_url          => $top_url,
	);
	
	my $msg = sprintf('お問い合わせ送信完了');
	&outputLog($msg);
	print $_CONFIG_base_head;
	print $template -> output;


	$session->flush();

exit;
