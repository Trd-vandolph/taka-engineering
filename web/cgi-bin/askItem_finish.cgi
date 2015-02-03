#!/usr/bin/perl
use CGI::Session qw/-ip_match/;
use CGI::Session::Cleaning;
use strict;
use English;
use MODULE::Jcode;
use MODULE::Template;
use MODULE::StringUtil;
use POSIX;
	
	our %FORM;
	our $_CONFIG_base_head;
	our @_CONFIG_error_msg;
	our $_CONFIG_carriage_contact;
	our $SUBSTR_ask_mail_1;
	our $SUBSTR_ask_mail_2;
	our $return_open;
	our $ret_close;
	our $return_msg;
	our $err = 0;
	our $sendmail;
	our $_CONFIG_server_ssl_www_root;
	our $_CONFIG_server_url;
	our $_CONFIG_server_ssl_use;
	our $_CONFIG_page_view_mode;
	our $_CONFIG_server_ssl_site_addr;
	our $_CONFIG_template_dir;
	
	my $ask_recieve_mail       = "";
	my $ask_mail_subject       = "";
	my $ask_mail_header        = "";
	my $ask_mail_footer        = "";
	my $ask_comment            = "";
	my $ask_mail_subject_owner = 'お問い合わせがありました。';
	
	our $_CONFIG_session_dir;
	our $_CONFIG_session_file_header;


	require './subroutine.pl';
	require './config_data.cgi';
	require "$_CONFIG_server_ssl_www_root/cgi-bin/mail/send_mail.pl";
	
	our $session_pass = "$_CONFIG_server_ssl_www_root/cgi-bin/$_CONFIG_session_dir";

	&formLoading;

    #SSL／非SSLの前処理
	unless ($_CONFIG_server_ssl_use ne '0' && $_CONFIG_page_view_mode ne 'P') {
		$_CONFIG_server_ssl_www_root = '..';
	}

	#セッション名、セッションタイムの定義
	my $session_name = 'sessionCart';
	my $mail_adrs_key = 'mail_adrs';
	my $mail_msg_key  = 'mail_msg';
	#my $session_timer = 30;

	#Cookieより現在のセッションIDを取得
	our %COOKIE;
#	&getCookie($session_name);
#	if ($FORM{'seid'} ne '' && $_CONFIG_server_ssl_use eq '1' && $_CONFIG_page_view_mode ne 'P') {
		$COOKIE{$session_name} = $FORM{'seid'};
#	}

	#セッションオブジェクト生成
	my $session;
	my $session_mail_adrs;
	my $session_mail_msg;
	my $session_id;
#	&cleanSession;
	$session      = CGI::Session->new(undef, $COOKIE{$session_name}, {Directory=>$session_pass});
	$session_mail_adrs = $session->param($mail_adrs_key);
	$session_mail_msg = $session->param($mail_msg_key);
	$session_id   = $session->id;

	#セッションオブジェクトより情報を取得
	my $mail_adrs = $session_mail_adrs;
	my $mail_msg  = $session_mail_msg;
	
	$session->close;
	$session->delete;

	my $load_file       = "$_CONFIG_server_ssl_www_root/cgi-bin/search/user_askItem_config_data.cgi";
	$FORM{'item_code'} =~ /(\d{2})(\d{2})(\d{8})/;
	my $category_code = $1;
	my $group_code    = $2;
	my $item_code     = $3;
	my $item_name;
	my $data_file     = sprintf('%s/cgi-bin/search/%s/%s.cgi', $_CONFIG_server_ssl_www_root, $category_code, $group_code);
	my $mailTemplate_user  = "$_CONFIG_server_ssl_www_root/cgi-bin/mail/mailTemplate_askItem_user.cgi";
	my $mailTemplate_owner = "$_CONFIG_server_ssl_www_root/cgi-bin/mail/mailTemplate_askItem_owner.cgi";
	
	open(FILE, $load_file);
	my @load_file = <FILE>;
	close(FILE);
	open(FILE, $data_file);
	my @data_file = <FILE>;
	close(FILE);
	open(FILE, $mailTemplate_user);
	my @mailTemplate_user = <FILE>;
	close(FILE);
	open(FILE, $mailTemplate_owner);
	my @mailTemplate_owner = <FILE>;
	close(FILE);
	
	
#	my $ask_user_mail = $FORM{'askItem_input_mail'};
	my $template = HTML::Template->new(filename => "./$_CONFIG_template_dir/askItem_finish.tmp");
	
	foreach my $line (@load_file) {
		my @load_line = split(/\t/, $line);
		if ($load_line[0] == $FORM{'pid'}) {
			$ask_recieve_mail  = $load_line[23];
			$ask_mail_subject  = $load_line[24];
			$ask_mail_header   = $load_line[25];
			$ask_mail_footer   = $load_line[26];
			$ask_comment       = $load_line[27];
			last;
		}
	}
	
	$ask_mail_header = &errstrRecover(&strBr($ask_mail_header, 1));
	$ask_mail_footer = &errstrRecover(&strBr($ask_mail_footer, 1));
	
	foreach my $line (@data_file) {
		my @data_line = split(/\t/, $line);
		if ($data_line[0] == $item_code) {
			$item_name = &errstrRecover(&strBr($data_line[4], 1));
		}
	}
	unless (&send_mail_Check($mail_adrs)) {
		$return_msg = $_CONFIG_error_msg[9951];
		$err = 1;
	}
	unless (&send_mail_Check($ask_recieve_mail)) {
		$return_msg = $_CONFIG_error_msg[9951];
		$err = 1;
	}
	
#	$FORM{'askItem_input_message'} = &strBr($FORM{'askItem_input_message'}, 1);
#	if ($ask_user_mail) {
#		my $i = 0;
#		for (my $i = 0; $i < @mailTemplate_user; $i++) {
#			if ($mailTemplate_user[$i] =~ /\$askItem_mail_header/) {
#				$mailTemplate_user[$i] =~ s/\$askItem_mail_header/$ask_mail_header/;
#			}
#			if ($mailTemplate_user[$i] =~ /\$SUBSTR_askItem_item_name/) {
#				$mailTemplate_user[$i] =~ s/\$SUBSTR_askItem_item_name/$item_name/;
#			}
#			if ($mailTemplate_user[$i] =~ /\$SUBSTR_askItem_mail/) {
#				$mailTemplate_user[$i] =~ s/\$SUBSTR_askItem_mail/$FORM{'askItem_input_mail'}/;
#			}
#			if ($mailTemplate_user[$i] =~ /\$SUBSTR_askItem_message/) {
#				$mailTemplate_user[$i] =~ s/\$SUBSTR_askItem_message/$FORM{'askItem_input_message'}/;
#			}
#			if ($mailTemplate_user[$i] =~ /\$askItem_mail_footer/) {
#				$mailTemplate_user[$i] =~ s/\$askItem_mail_footer/$ask_mail_footer/;
#			}
#		}
#		if ($err == 0 && ($_CONFIG_page_view_mode ne 'P')) {
#			&send_mail_Send($ask_recieve_mail, $ask_user_mail, $ask_mail_subject, join ('', @mailTemplate_user));
#		}
#	}
	
	if ($mail_adrs) {
		my $i = 0;
		for (my $i = 0; $i < @mailTemplate_user; $i++) {
			if ($mailTemplate_user[$i] =~ /\$askItem_mail_header/) {
				$mailTemplate_user[$i] =~ s/\$askItem_mail_header/$ask_mail_header/;
			}
			if ($mailTemplate_user[$i] =~ /\$SUBSTR_askItem_item_name/) {
				$mailTemplate_user[$i] =~ s/\$SUBSTR_askItem_item_name/$item_name/;
			}
			if ($mailTemplate_user[$i] =~ /\$SUBSTR_askItem_mail/) {
				$mailTemplate_user[$i] =~ s/\$SUBSTR_askItem_mail/$mail_adrs/;
			}
			if ($mailTemplate_user[$i] =~ /\$SUBSTR_askItem_message/) {
				$mailTemplate_user[$i] =~ s/\$SUBSTR_askItem_message/$mail_msg/;
			}
			if ($mailTemplate_user[$i] =~ /\$askItem_mail_footer/) {
				$mailTemplate_user[$i] =~ s/\$askItem_mail_footer/$ask_mail_footer/;
			}
		}
		if ($err == 0 && ($_CONFIG_page_view_mode ne 'P')) {
			&send_mail_Send($ask_recieve_mail, $mail_adrs, $ask_mail_subject, join ('', @mailTemplate_user));
		}
	}

	
	my $submit_url;
	if ($_CONFIG_server_ssl_use == 1) {
		$submit_url = sprintf('%s送信元URL=%s/cgi-bin/askItem_finish.cgi', "\n\n", $_CONFIG_server_ssl_site_addr);
	} else {
		$submit_url = sprintf('%s送信元URL=%s/cgi-bin/askItem_finish.cgi', "\n\n", $_CONFIG_server_url);
	}
	
	my $i = 0;
#	for (my $i = 0; $i < @mailTemplate_owner; $i++) {
#		if ($mailTemplate_owner[$i] =~ /\$SUBSTR_askItem_item_name/) {
#			$mailTemplate_owner[$i] =~ s/\$SUBSTR_askItem_item_name/$item_name/;
#		}
#		if ($mailTemplate_owner[$i] =~ /\$SUBSTR_askItem_item_code/) {
#			$mailTemplate_owner[$i] =~ s/\$SUBSTR_askItem_item_code/$item_code/;
#		}
#		if ($mailTemplate_owner[$i] =~ /\$SUBSTR_askItem_mail/) {
#			$mailTemplate_owner[$i] =~ s/\$SUBSTR_askItem_mail/$FORM{'askItem_input_mail'}/;
#		}
#		if ($mailTemplate_owner[$i] =~ /\$SUBSTR_askItem_message/) {
#			$mailTemplate_owner[$i] =~ s/\$SUBSTR_askItem_message/$FORM{'askItem_input_message'}/;
#		}
#	}
#	push (@mailTemplate_owner, $submit_url);
	
#	if ($err == 0 && ($_CONFIG_page_view_mode ne 'P')) {
#		&send_mail_Send($ask_user_mail, $ask_recieve_mail, $ask_mail_subject, join ('', @mailTemplate_owner));
#	}

	for (my $i = 0; $i < @mailTemplate_owner; $i++) {
		if ($mailTemplate_owner[$i] =~ /\$SUBSTR_askItem_item_name/) {
			$mailTemplate_owner[$i] =~ s/\$SUBSTR_askItem_item_name/$item_name/;
		}
		if ($mailTemplate_owner[$i] =~ /\$SUBSTR_askItem_item_code/) {
			$mailTemplate_owner[$i] =~ s/\$SUBSTR_askItem_item_code/$item_code/;
		}
		if ($mailTemplate_owner[$i] =~ /\$SUBSTR_askItem_mail/) {
			$mailTemplate_owner[$i] =~ s/\$SUBSTR_askItem_mail/$mail_adrs/;
		}
		if ($mailTemplate_owner[$i] =~ /\$SUBSTR_askItem_message/) {
			$mailTemplate_owner[$i] =~ s/\$SUBSTR_askItem_message/$mail_msg /;
		}
	}
	push (@mailTemplate_owner, $submit_url);
	
	if ($err == 0 && ($_CONFIG_page_view_mode ne 'P')) {
		&send_mail_Send($mail_adrs, $ask_recieve_mail, $ask_mail_subject_owner, join ('', @mailTemplate_owner));
	}

	my $top_url;
	#_戻り先URL
	my $askItem_detail_url;
	if ($_CONFIG_server_ssl_use ne '0' && $_CONFIG_page_view_mode ne 'P') {
		$top_url = $_CONFIG_server_url;
	} else {
		$top_url = '../';
	}
	
	$template->param(
		pid                 => $FORM{'pid'},
		askItem_fin_comment => $ask_comment,
		top_url             => $top_url,
	);
	
	my $msg = sprintf('商品お問い合わせ送信完了');
	&outputLog($msg);
	print $_CONFIG_base_head;
	print $template -> output;


	$session->flush();

exit;
