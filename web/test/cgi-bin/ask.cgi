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


	use Logger::MyLogger;
	my $logger = Logger::MyLogger->new;

	our %FORM;
	our $_CONFIG_base_head;
	our $_CONFIG_site_title;
	our $_CONFIG_site_outline_site;
	our @_CONFIG_site_keyword;
	our $_CONFIG_server_ssl_www_root;
	our $_CONFIG_server_ssl_use;
	our $_CONFIG_page_view_mode;
	our $_CONFIG_server_url;
	our $_CONFIG_template_dir;

	our $_CONFIG_session_dir;
	our $_CONFIG_session_file_header;

	require './subroutine.pl';
	require './config_data.cgi';


	our $session_pass = "$_CONFIG_server_ssl_www_root/cgi-bin/$_CONFIG_session_dir";


	&formLoading;

	my $ask_button;
	my $ask_button_flg;
	
	my $load_file  = "$_CONFIG_server_ssl_www_root/cgi-bin/ask/ask_config.cgi";
	my $parts_file = "$_CONFIG_server_ssl_www_root/cgi-bin/ask/ask_parts.cgi";

	open(FILE, $load_file);
	my @load_file = <FILE>;
	close(FILE);
	open(FILE, $parts_file);
	my @parts_file = <FILE>;
	close(FILE);

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
#Session化->End

	our $template = HTML::Template->new(filename => "./$_CONFIG_template_dir/ask.tmp");


	#_認証ページのチェック
	my $pagelink_file = './module_pageLink.cgi';
	if(($_CONFIG_server_ssl_use eq '1') && ($_CONFIG_page_view_mode  ne 'P')){
		$pagelink_file = "$_CONFIG_server_ssl_www_root/cgi-bin/module_pageLink.cgi";
	}
	open(DATA, $pagelink_file);
	my @pagelink_file = <DATA>;
	close(DATA);
	foreach (@pagelink_file) {
		my @pagelink_line = split(/\t/, $_);
		if ($pagelink_line[0] eq $FORM{'pid'}) {
			if ($pagelink_line[6] ne '0') {
				#my $_COOKIE_lid = &getCookie('ID');
				#my $_COOKIE_lpw = &getCookie('PASSWORD');
				my $_COOKIE_lid = &getLoginCookie('ID', $ENV{'HTTP_COOKIE'}, $logger);
				my $_COOKIE_lpw = &getLoginCookie('PASSWORD', $ENV{'HTTP_COOKIE'}, $logger);
				if(($_CONFIG_server_ssl_use eq '1') && ($_CONFIG_page_view_mode  ne 'P')){
					$_COOKIE_lid = $FORM{'ID'};
					$_COOKIE_lpw = $FORM{'PASSWORD'};
				}
				if ($_COOKIE_lid eq '' && $_COOKIE_lpw eq '') {
					if(($_CONFIG_server_ssl_use eq '1') && ($_CONFIG_page_view_mode  ne 'P')){
						&pageLoginErr("$_CONFIG_server_url");
					} else {
						&pageLoginErr('../');
					}
				}
			}
			last;
		}
	}



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
		ask_page_id         => $FORM{'pid'},
		ask_button          => $ask_button,
		ask_necessity_check => $ask_necessity_check,
		ask_button_flg      => $ask_button_flg,
		top_url             => $top_url,
		FORM_LOOP           => \@$FORM_LOOP,
		seid                => $session_id,
	);
	
	print $_CONFIG_base_head;
	print $template -> output;


	$session->flush();

	&chmodSessionFile ($session_pass . "/", $_CONFIG_session_file_header, $session_id);

exit;
