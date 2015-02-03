#!/usr/bin/perl
use strict;
use English;
use MODULE::Jcode;
use MODULE::Template;
use MODULE::Ordernumber;
use MODULE::StringUtil;
use CGI::Session qw/-ip_match/;
use CGI::Session::Cleaning;
	
	our %FORM;
	our %COOKIE;
	our $_CONFIG_base_head;
	our @_CONFIG_error_msg;
	our $_CONFIG_carriage_contact;
	our $_CONFIG_order_announce_view;
	our $_CONFIG_tax_consumer;
	our @_CONFIG_order_discount_condition;
	our @_CONFIG_order_discount_amount;
	our @_CONFIG_order_commission_condition;
	our @_CONFIG_order_commission_amount;
	our $_CONFIG_carriage_carriage_disp;
	our $_CONFIG_carriage_compu_method;
	our $_CONFIG_carriage_free_shipping_set;
	our $_CONFIG_tax_fraction;
	our $_CONFIG_tax_indication;
	
	our $_CONFIG_server_ssl_use;
	our $_CONFIG_server_url;
	our $_CONFIG_server_ssl_site_addr;
	our $_CONFIG_page_view_mode;
	
	our $SUBSTR_ask_mail_1;
	our $SUBSTR_ask_mail_2;
	our $return_open;
	our $ret_close;
	our $return_msg;
	our $err = 0;
	our $sendmail;
	our $session_name  = 'sessionCart';
	our $session_timer = 30;
	
	our $item_name_articles;
	our $item_price;
	our $item_including_tax_price;
	our $item_sp_price_flag;
	our $item_money_sp_price;
	our $item_money_sp_price_tax;
	our $item_deli_type_id;
	our $item_stock_setting_flg;
	our $item_cmd_category_id;
	our $item_product_grp_id;
	our $item_cmd_basic_id;
	our $item_group_name;
	our $item_order_count;
	
	our $_CONFIG_session_dir;
	our $_CONFIG_session_file_header;

	our @item_vari_h_clm;
	our @item_vari_v_clm;
	our $_CONFIG_template_dir;
	
	#_動作確認用
	our $send_mail_massage;
	
	our $_CONFIG_order_mail_address   = "";
	our $_CONFIG_order_mail_subject   = "";
	our $_CONFIG_order_mail_header    = "";
	our $_CONFIG_order_mail_footer    = "";
	our $_CONFIG_order_finish_comment = "";
	our $_CONFIG_server_ssl_www_root;
	our $_CONFIG_page_view_mode;
	our $_CONFIG_server_ssl_site_addr;
	our $_CONFIG_server_url;
	
	my $ask_recieve_mail       = "";
	my $ask_mail_subject       = "";
	my $ask_mail_header        = "";
	my $ask_mail_footer        = "";
	my $ask_comment            = "";
	my $order_mail_subject_owner = 'ホームページより商品のご注文がありました。';
	my @mailTemplate_base_main;
	my @mailTemplate_base_deli;
	my @mailTemplate_base_time;
	my @mailTemplate_base_item;
	my @mailTemplate_base_cost;
	my @mailTemplate_base;
	
	require './subroutine.pl';
	require './config_data.cgi';



	our $session_pass = "$_CONFIG_server_ssl_www_root/cgi-bin/$_CONFIG_session_dir";


	
	our $http_path;
	if ($_CONFIG_server_ssl_use ne '0' && $_CONFIG_page_view_mode ne 'P') {
		$http_path = sprintf('%s/cgi-bin', $_CONFIG_server_url);
	} else {
		$http_path = '../cgi-bin';
		$_CONFIG_server_ssl_www_root = '..';
	}
	require "$_CONFIG_server_ssl_www_root/cgi-bin/mail/send_mail.pl";
	
	&formLoading;
	
	&getCookie($session_name);
	#&cleanSession;
	our $session      = CGI::Session->new(undef, $COOKIE{$session_name}, {Directory=>$session_pass});
	our $session_cart = $session->param($session_name);

#メールデータセッション化->Start
	#注文者フォームデータ
	$FORM{'lname'} = $session->param('lname');				#氏名（姓）
	$FORM{'fname'} = $session->param('fname');				#氏名（名）
	$FORM{'lname_kana'} = $session->param('lname_kana');	#氏名（姓）カナ
	$FORM{'fname_kana'} = $session->param('fname_kana');	#氏名（名）カナ
	$FORM{'cname'} = $session->param('cname');				#法人名
	$FORM{'cname_kana'} = $session->param('cname_kana');	#法人名カナ
	$FORM{'department'} = $session->param('department');	#所属部署/役職名
	$FORM{'pcode_first'} = $session->param('pcode_first');	#郵便番号上3桁
	$FORM{'pcode_last'} = $session->param('pcode_last');	#郵便番号下4桁
	$FORM{'address'} = $session->param('address');			#住所
	$FORM{'mail'} = $session->param('mail');				#メールアドレス
	$FORM{'mail_check'} = $session->param('mail_check');	#メールアドレス確認
	$FORM{'pnum_1'} = $session->param('pnum_1');			#電話番号（市外）
	$FORM{'pnum_2'} = $session->param('pnum_2');			#電話番号（市内）
	$FORM{'pnum_3'} = $session->param('pnum_3');			#電話番号（番号）
	$FORM{'fnum_1'} = $session->param('fnum_1');			#FAX番号（市外）
	$FORM{'fnum_2'} = $session->param('fnum_2');			#FAX番号（市内）
	$FORM{'fnum_3'} = $session->param('fnum_3');			#FAX番号（番号）
	$FORM{'day_pnum_1'} = $session->param('day_pnum_1');	#日中の連絡先（市外）
	$FORM{'day_pnum_2'} = $session->param('day_pnum_2');	#日中の連絡先（市内）
	$FORM{'day_pnum_3'} = $session->param('day_pnum_3');	#日中の連絡先（番号）
	$FORM{'birthyear'} = $session->param('birthyear');		#生年月日（年）
	$FORM{'birthmonth'} = $session->param('birthmonth');	#生年月日（月）
	$FORM{'birthday'} = $session->param('birthday');		#生年月日（日）
	
	#別途配送先フォームデータ
	$FORM{'sp_lname'} = $session->param('sp_lname');				#氏名（姓）
	$FORM{'sp_fname'} = $session->param('sp_fname');				#氏名（名）
	$FORM{'sp_lname_kana'} = $session->param('sp_lname_kana');		#氏名（姓）カナ
	$FORM{'sp_fname_kana'} = $session->param('sp_fname_kana');		#氏名（名）カナ
	$FORM{'sp_cname'} = $session->param('sp_cname');				#法人名
	$FORM{'sp_cname_kana'} = $session->param('sp_cname_kana');		#法人名カナ
	$FORM{'sp_department'} = $session->param('sp_department');		#所属部署/役職名
	$FORM{'sp_pcode_first'} = $session->param('sp_pcode_first');	#郵便番号上3桁
	$FORM{'sp_pcode_last'} = $session->param('sp_pcode_last');		#郵便番号下4桁
	$FORM{'sp_address'} = $session->param('sp_address');			#住所
	$FORM{'sp_mail'} = $session->param('sp_mail');					#メールアドレス
	$FORM{'sp_mail_check'} = $session->param('sp_mail_check');		#メールアドレス確認
	$FORM{'sp_pnum_1'} = $session->param('sp_pnum_1');				#電話番号（市外）
	$FORM{'sp_pnum_2'} = $session->param('sp_pnum_2');				#電話番号（市内）
	$FORM{'sp_pnum_3'} = $session->param('sp_pnum_3');				#電話番号（番号）
	$FORM{'sp_fnum_1'} = $session->param('sp_fnum_1');				#FAX番号（市外）
	$FORM{'sp_fnum_2'} = $session->param('sp_fnum_2');				#FAX番号（市内）
	$FORM{'sp_fnum_3'} = $session->param('sp_fnum_3');				#FAX番号（番号）
	$FORM{'sp_day_pnum_1'} = $session->param('sp_day_pnum_1');		#日中の連絡先（市外）
	$FORM{'sp_day_pnum_2'} = $session->param('sp_day_pnum_2');		#日中の連絡先（市内）
	$FORM{'sp_day_pnum_3'} = $session->param('sp_day_pnum_3');		#日中の連絡先（番号）
	$FORM{'sp_birthyear'} = $session->param('sp_birthyear');		#生年月日（年）
	$FORM{'sp_birthmonth'} = $session->param('sp_birthmonth');		#生年月日（月）
	$FORM{'sp_birthday'} = $session->param('sp_birthday');			#生年月日（日）

	$FORM{'dhope'} = $session->param('dhope');			#配送等へのご希望
	$FORM{'idea'} = $session->param('idea');			#連絡事項

	#_注文フォームグリッド
	my $form_file = "$_CONFIG_server_ssl_www_root/cgi-bin/search/item_order_form.cgi";
	open(DATA, $form_file);
	our @form_file = <DATA>;
	close(DATA);
	@form_file = sort { (split(/\t/,$a))[6] <=> (split(/\t/,$b))[6] } @form_file;
	foreach (@form_file) {
		my @form_line = split(/\t/, $_);
		if ($form_line[9] eq 'A') {
			$FORM{"order_$form_line[0]"} = $session->param("order_$form_line[0]");
			$FORM{"sp_order_$form_line[0]"} = $session->param("sp_order_$form_line[0]");
		}
	}

#メールデータセッション化->End

	#セッションチェック
	&isSessionCartEmpty;

	our $session_id   = $session->id;
	$session->expire('+'.$session_timer.'m');
	
	
	my $load_file       = "$_CONFIG_server_ssl_www_root/cgi-bin/search/user_askItem_config_data.cgi";
	$FORM{'item_code'} =~ /(\d{2})(\d{2})(\d{8})/;
	my $category_code = $1;
	my $group_code    = $2;
	my $item_code     = $3;
	my $item_name	  = '';
	my $data_file     = sprintf('%s/cgi-bin/search/%s/%s.cgi', $_CONFIG_server_ssl_www_root, $category_code, $group_code);
	my $mailTemplate_user  = "$_CONFIG_server_ssl_www_root/cgi-bin/mail/mailTemplate_order_user.cgi";
	my $mailTemplate_owner = "$_CONFIG_server_ssl_www_root/cgi-bin/mail/mailTemplate_order_owner.cgi";
	
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
	
#	#_注文フォームグリッド
#	my $form_file = "$_CONFIG_server_ssl_www_root/cgi-bin/search/item_order_form.cgi";
#	open(DATA, $form_file);
#	my @form_file = <DATA>;
#	close(DATA);
	@form_file = sort { (split(/\t/,$a))[6] <=> (split(/\t/,$b))[6] } @form_file;
	
		#if ($FORM{'saleItem_id'});
		#if ($FORM{'bpage'});
		#if ($FORM{'pid'});
		#if ($FORM{'stype'});
		#if ($FORM{'vtype'});
		#if ($FORM{'ukeyword'});
		#if ($FORM{'skeyword'});
		#if ($FORM{'gkeyword'});
		#if ($FORM{'ckeyword'});
		#if ($FORM{'vnum'});
		#if ($FORM{'bpage'});
	foreach (@form_file) {
		my @form_line = split(/\t/, $_);
		if ($form_line[0] == 1 && $form_line[2] == 1) {
			push (@mailTemplate_base_main, sprintf('◇お名前 %s %s 様%s',           $FORM{'lname'}, $FORM{'fname'}, "\n"));# if (($FORM{'lname'}) || ($FORM{'fname'}));
			push (@mailTemplate_base_main, sprintf('◇お名前(フリガナ) %s %s%s',    $FORM{'lname_kana'}, $FORM{'fname_kana'}, "\n"));# if (($FORM{'lname_kana'}) || ($FORM{'fname_kana'}));
		}
		if ($form_line[0] == 2 && $form_line[2] == 1) {
			push (@mailTemplate_base_main, sprintf('◇法人名 %s%s',                 $FORM{'cname'}, "\n"));# if ($FORM{'cname'});
			push (@mailTemplate_base_main, sprintf('◇法人名(フリガナ) %s%s',       $FORM{'cname_kana'}, "\n"));# if ($FORM{'cname_kana'});
		}
		if ($form_line[0] == 3 && $form_line[2] == 1) {
			push (@mailTemplate_base_main, sprintf('◇所属部署/役職名 %s%s',        $FORM{'department'}, "\n"));# if ($FORM{'department'});
		}
		if ($form_line[0] == 4 && $form_line[2] == 1) {
			push (@mailTemplate_base_main, sprintf('◇ご住所 %s-%s %s %s%s',        $FORM{'pcode_first'}, $FORM{'pcode_last'}, &prefOut($FORM{'todouhuken'}), $FORM{'address'}, "\n"));# if (($FORM{'lname'}) || ($FORM{'fname'}) || ($FORM{'todouhuken'}) || ($FORM{'address'}));
		}
		if ($form_line[0] == 5 && $form_line[2] == 1) {
			#hirokoba
			push (@mailTemplate_base_main, sprintf('◇メールアドレス %s%s',         $FORM{'mail'}, "\n"));# if ($FORM{'mail'});
		}
		if ($form_line[0] == 7 && $form_line[2] == 1) {
			push (@mailTemplate_base_main, sprintf('◇電話番号 %s-%s-%s%s',         $FORM{'pnum_1'}, $FORM{'pnum_2'}, $FORM{'pnum_3'}, "\n"));# if (($FORM{'pnum_1'}) || ($FORM{'pnum_2'}) || ($FORM{'pnum_3'}));
		}
		if ($form_line[0] == 8 && $form_line[2] == 1) {
			push (@mailTemplate_base_main, sprintf('◇FAX番号 %s-%s-%s%s',          $FORM{'fnum_1'}, $FORM{'fnum_2'}, $FORM{'fnum_3'}, "\n"));# if (($FORM{'fnum_1'}) || ($FORM{'fnum_2'}) || ($FORM{'fnum_3'}));
		}
		if ($form_line[0] == 9 && $form_line[2] == 1) {
			push (@mailTemplate_base_main, sprintf('◇日中の連絡先 %s-%s-%s%s',     $FORM{'day_pnum_1'}, $FORM{'day_pnum_2'}, $FORM{'day_pnum_3'}, "\n"));# if (($FORM{'day_pnum_1'}) || ($FORM{'day_pnum_2'}) || ($FORM{'day_pnum_3'}));
		}
		if ($form_line[0] == 10 && $form_line[2] == 1) {
			push (@mailTemplate_base_main, sprintf('◇生年月日 西暦%s年%s月%s日%s', $FORM{'birthyear'}, $FORM{'birthmonth'}, $FORM{'birthday'}, "\n"));# if (($FORM{'birthyear'}) || ($FORM{'birthmonth'}) || ($FORM{'birthday'}));
		}
		if ($form_line[0] == 11 && $form_line[2] == 1) {
			if ($FORM{'sei_fm_flg'} eq 'm') {
				push (@mailTemplate_base_main, sprintf('◇性別 男性%s', "\n"));
			} elsif ($FORM{'sei_fm_flg'} eq 'f') {
				push (@mailTemplate_base_main, sprintf('◇性別 女性%s', "\n"));
			}
		}
	}
	foreach (@form_file) {
		my @form_line = split(/\t/, $_);
		next unless ($form_line[0] >= 12);
		next if ($form_line[2] == 0);
		my $option_value = '';
		if ($form_line[9] eq 'S') {
			my @option_list = split(/<RETURN>/, $form_line[10]);
			chomp @option_list;
			foreach (@option_list) {
				if ($FORM{"order_$form_line[0]"} ne '') {
					$option_value = $option_list[$FORM{"order_$form_line[0]"} - 1];
					last;
				}
			}
		} elsif ($form_line[9] eq 'C') {
			my @option_list = split(/<RETURN>/, $form_line[10]);
			chomp @option_list;
			my $i = 1;
			foreach (@option_list) {
				if ($FORM{"order_$form_line[0]_$i"} ne '') {
					$option_value .= sprintf('%s          ・%s', "\n", $_);
				}
				$i++;
			}
		} elsif ($form_line[9] eq 'R') {
			my @option_list = split(/<RETURN>/, $form_line[10]);
			chomp @option_list;
			my $i = 1;
			foreach (@option_list) {
				if ($i == $FORM{"order_$form_line[0]"}) {
					$option_value = $_;
					last;
				}
				$i++;
			}
		} elsif ($form_line[9] eq 'A') {
			$option_value = $FORM{"order_$form_line[0]"};
		}
		push (@mailTemplate_base_main, sprintf('◇%s %s%s', $form_line[1], $option_value, "\n"));
	}
	push (@mailTemplate_base_main, sprintf('◇連絡事項 %s%s',               $FORM{'idea'}, "\n")) if ($FORM{'idea'});
	push (@mailTemplate_base_main, sprintf('◇配送等へのご希望 %s%s',       $FORM{'dhope'}, "\n")) if ($FORM{'dhope'});
	if ($_CONFIG_order_announce_view != 0) {
		if ($FORM{'mailguide'}) {
			push (@mailTemplate_base_main, sprintf('◇メールでの案内 メールでの案内を希望する%s', "\n"));
		} else {
			push (@mailTemplate_base_main, sprintf('◇メールでの案内 メールでの案内を希望しない%s', "\n"));
		}
	}
	
	if ($FORM{'sp_ship'}) {
		foreach (@form_file) {
			my @form_line = split(/\t/, $_);
			if ($form_line[0] == 1 && $form_line[4] == 1) {
				push (@mailTemplate_base_deli, sprintf('◇お名前 %s %s 様%s',           $FORM{'sp_lname'}, $FORM{'sp_fname'}, "\n"));# if (($FORM{'sp_lname'}) || ($FORM{'sp_fname'}));
				push (@mailTemplate_base_deli, sprintf('◇お名前(フリガナ) %s %s%s',    $FORM{'sp_lname_kana'}, $FORM{'sp_fname_kana'}, "\n"));# if (($FORM{'sp_lname_kana'}) || ($FORM{'sp_fname_kana'}));
			}
			if ($form_line[0] == 2 && $form_line[4] == 1) {
				push (@mailTemplate_base_deli, sprintf('◇法人名 %s%s',                 $FORM{'sp_cname'}, "\n"));# if ($FORM{'sp_cname'});
				push (@mailTemplate_base_deli, sprintf('◇法人名(フリガナ) %s%s',       $FORM{'sp_cname_kana'}, "\n"));# if ($FORM{'sp_cname_kana'});
			}
			if ($form_line[0] == 3 && $form_line[4] == 1) {
				push (@mailTemplate_base_deli, sprintf('◇所属部署/役職名 %s%s',        $FORM{'sp_department'}, "\n"));# if ($FORM{'sp_department'});
			}
			if ($form_line[0] == 4 && $form_line[4] == 1) {
				push (@mailTemplate_base_deli, sprintf('◇ご住所 %s-%s %s %s%s',        $FORM{'sp_pcode_first'}, $FORM{'sp_pcode_last'}, &prefOut($FORM{'sp_todouhuken'}), $FORM{'sp_address'}, "\n"));# if (($FORM{'sp_pcode_first'}) || ($FORM{'sp_pcode_last'}) || ($FORM{'sp_todouhuken'}) || ($FORM{'sp_address'}));
			}
			if ($form_line[0] == 5 && $form_line[4] == 1) {
				push (@mailTemplate_base_deli, sprintf('◇メールアドレス %s%s',         $FORM{'sp_mail'}, "\n"));# if ($FORM{'sp_mail'});
			}
			if ($form_line[0] == 7 && $form_line[4] == 1) {
				push (@mailTemplate_base_deli, sprintf('◇電話番号 %s-%s-%s%s',         $FORM{'sp_pnum_1'}, $FORM{'sp_pnum_2'}, $FORM{'sp_pnum_3'}, "\n"));# if (($FORM{'sp_pnum_1'}) || ($FORM{'sp_pnum_2'}) || ($FORM{'sp_pnum_3'}));
			}
			if ($form_line[0] == 8 && $form_line[4] == 1) {
				push (@mailTemplate_base_deli, sprintf('◇FAX番号 %s-%s-%s%s',          $FORM{'sp_fnum_1'}, $FORM{'sp_fnum_2'}, $FORM{'sp_fnum_3'}, "\n"));# if (($FORM{'sp_fnum_1'}) || ($FORM{'sp_fnum_2'}) || ($FORM{'sp_fnum_3'}));
			}
			if ($form_line[0] == 9 && $form_line[4] == 1) {
				push (@mailTemplate_base_deli, sprintf('◇日中の連絡先 %s-%s-%s%s',     $FORM{'sp_day_pnum_1'}, $FORM{'sp_day_pnum_2'}, $FORM{'sp_day_pnum_3'}, "\n"));# if (($FORM{'sp_day_pnum_1'}) || ($FORM{'sp_day_pnum_2'}) || ($FORM{'sp_day_pnum_3'}));
			}
			if ($form_line[0] == 10 && $form_line[4] == 1) {
				push (@mailTemplate_base_deli, sprintf('◇生年月日 西暦%s年%s月%s日%s', $FORM{'sp_birthyear'}, $FORM{'sp_birthmonth'}, $FORM{'sp_birthday'}, "\n"));# if (($FORM{'sp_birthyear'}) || ($FORM{'sp_birthmonth'}) || ($FORM{'sp_birthday'}));
			}
			if ($form_line[0] == 11 && $form_line[4] == 1) {
				if ($FORM{'sp_sei_fm_flg'} eq 'm') {
					push (@mailTemplate_base_deli, sprintf('◇性別 男性%s', "\n"));
				} elsif ($FORM{'sp_sei_fm_flg'} eq 'f') {
					push (@mailTemplate_base_deli, sprintf('◇性別 女性%s', "\n"));
				}
			}
		}
		foreach (@form_file) {
			my @form_line = split(/\t/, $_);
			next unless ($form_line[0] >= 12);
			next if ($form_line[4] == 0);
			my $sp_option_value = '';
			if ($form_line[9] eq 'S') {
				my @option_list = split(/<RETURN>/, $form_line[10]);
				chomp @option_list;
				foreach (@option_list) {
					if ($FORM{"sp_order_$form_line[0]"} ne '') {
						$sp_option_value = $option_list[$FORM{"sp_order_$form_line[0]"} - 1];
						last;
					}
				}
			} elsif ($form_line[9] eq 'C') {
				my @option_list = split(/<RETURN>/, $form_line[10]);
				chomp @option_list;
				my $i = 1;
				foreach (@option_list) {
					if ($FORM{"sp_order_$form_line[0]_$i"} ne '') {
						$sp_option_value .= sprintf('%s          ・%s', "\n", $_);
					}
					$i++;
				}
			} elsif ($form_line[9] eq 'R') {
				my @option_list = split(/<RETURN>/, $form_line[10]);
				chomp @option_list;
				my $i = 1;
				foreach (@option_list) {
					if ($i == $FORM{"sp_order_$form_line[0]"}) {
						$sp_option_value = $_;
						last;
					}
					$i++;
				}
			} elsif ($form_line[9] eq 'A') {
				$sp_option_value = $FORM{"sp_order_$form_line[0]"};
			}
			push (@mailTemplate_base_deli, sprintf('◇%s %s%s', $form_line[1], $sp_option_value, "\n"));
		}
	} else {
		push (@mailTemplate_base_deli, sprintf('　同上%s', "\n"));
	}
	
	#_送信日時の生成
	my $today_time = time();
	my ($sec, $min, $hour, $mday, $month, $year, undef, undef) = localtime($today_time);
	push (@mailTemplate_base_time, sprintf("◇送信日時　%04d-%02d-%02d %02d\:%02d:%02d%s", $year + 1900, $month + 1, $mday, $hour, $min, $sec, "\n"));
	push (@mailTemplate_base_time, "\n");
	
	my $subtotal_amount	= 0;
	my $total_delivery	= 0;
	my @delivery_back	= ();
	my @cart_data		= ();
	foreach my $value (@{$session_cart}) {
		$$value{"item_code"} =~ /^(\d{2})(\d{2})(\d{8})(\d{2})(\d{2})/;
		my $insert_line	= '';
		my $line_cc = $1;
		my $line_gc = $2;
		my $line_ic = $3;
		my $line_vari_v = $4;
		my $line_vari_h = $5;
		
		my $data_file = sprintf('%s/cgi-bin/search/%02d/%02d.cgi', $_CONFIG_server_ssl_www_root, $line_cc, $line_gc);
		open(DATA, $data_file);
		my @data_file = <DATA>;
		close(DATA);
		chomp @data_file;
		
		my $insert_line_var	= 0;
		foreach (@data_file) {
			my @data_line = split(/\t/, $_);
			if ($data_line[0] eq $line_ic) {
				$insert_line     = join("\t", @data_line);
				$insert_line_var = $insert_line . "\t" . $line_vari_v . $line_vari_h . "\t" . $$value{"order_count"};
				last;
			}
		}
		push (@cart_data, $insert_line_var);
		
		my $val_data_file = sprintf('%s/cgi-bin/search/%02d/%02d_variation.cgi', $_CONFIG_server_ssl_www_root, $line_cc, $line_gc);
		open(DATA, $val_data_file);
		my @val_data_file = <DATA>;
		close(DATA);
		
		foreach (@val_data_file) {
			my @data_line = split(/\t/, $_);
			if ($data_line[0] eq $line_ic) {
				$insert_line = $insert_line . join("\t", @data_line);
				last;
			}
		}
		
		our $line = $insert_line;
		&itemMainDataSplitFull;
		#our $line = $insert_line;
		#&itemMainDataSplit;
		
		my $unit_price		= 0;
#		my $pretax_flg		= 0;
		my $pretax_price	= 0;
		my $pretax_flg = $_CONFIG_tax_indication;
		if ($_CONFIG_tax_consumer eq 'I') {
			$pretax_flg = '';
			if ($item_sp_price_flag != 0) {
				$pretax_price = $item_money_sp_price_tax;
				$unit_price   = $item_money_sp_price_tax;
			} else {
				$pretax_price = $item_including_tax_price;
				$unit_price   = $item_including_tax_price;
			}
		} else {
			#$pretax_flg = 1;
			if ($item_sp_price_flag != 0) {
				$pretax_price = $item_money_sp_price;
				$unit_price   = $item_money_sp_price_tax;
			} else {
				$pretax_price = $item_price;
				$unit_price   = $item_including_tax_price;
			}
		}
		my $amount = $unit_price * $$value{"order_count"};
		$subtotal_amount += $amount;
		
		#_配送タイプ名
		my $delivery_file = "$_CONFIG_server_ssl_www_root/cgi-bin/item_delivery.cgi";
		open(DATA, $delivery_file);
		my @delivery_file = <DATA>;
		close(DATA);
		my @delivery_line;
		foreach (@delivery_file) {
			@delivery_line = split(/\t/, $_);
			if ($item_deli_type_id == $delivery_line[0]) {
				last;
			}
		}
		
		#_配送料
		#if ($_CONFIG_carriage_carriage_disp != 0) {
			#_とりあえずこの商品の送料を出力
			my $unit_delivery;
			my $delivery_pref;
			if ($FORM{'sp_todouhuken'}) {
				$delivery_pref = $FORM{'sp_todouhuken'}
			} else {
				$delivery_pref = $FORM{'todouhuken'}
			}
			if ($delivery_line[2] eq 'D') {
				$unit_delivery = $delivery_line[3 + $delivery_pref];
				#一部設定する場所を変更する。
				if ($delivery_pref eq '15') {
					#山梨県
					$unit_delivery = $delivery_line[22];
				}
				if ($delivery_pref eq '16') {
					#静岡県
					$unit_delivery = $delivery_line[25];
				}
				if ($delivery_pref eq '17') {
					#長野県
					$unit_delivery = $delivery_line[23];
				}
				if ($delivery_pref eq '18') {
					#新潟県
					$unit_delivery = $delivery_line[18];
				}
				if ($delivery_pref eq '19') {
					#富山県
					$unit_delivery = $delivery_line[19];
				}
				if ($delivery_pref eq '20') {
					#石川県
					$unit_delivery = $delivery_line[20];
				}
				if ($delivery_pref eq '21') {
					#福井県
					$unit_delivery = $delivery_line[21];
				}
				if ($delivery_pref eq '22') {
					#岐阜県
					$unit_delivery = $delivery_line[24];
				}
			} else {
				$unit_delivery = $delivery_line[3];
			}
			if ($_CONFIG_carriage_compu_method eq 'H') {
				if ($total_delivery < $unit_delivery) {
					$total_delivery = $unit_delivery;
				}
			} elsif ($_CONFIG_carriage_compu_method eq 'T') {
				my $check_flg = 0;
				foreach (@delivery_back) {
					if ($_ == $item_deli_type_id) {
						$check_flg = 1;
						last;
					}
				}
				if ($check_flg == 0) {
					$total_delivery += $unit_delivery;
					push (@delivery_back, $delivery_line[0]);
				}
			} elsif ($_CONFIG_carriage_compu_method eq 'C') {
				$total_delivery += $unit_delivery;
			}
		#}
		
		my ($vari_yoko_name, $vari_tate_name);
		$vari_yoko_name = $item_vari_h_clm[$line_vari_h];
		$vari_tate_name = $item_vari_v_clm[$line_vari_v];
		
		if ($vari_yoko_name || $vari_tate_name) {
			push (@mailTemplate_base_item, sprintf('◇商品名 %s(%s・%s)%s', &errstrRecover(&strBr($item_name_articles, 1)), $vari_yoko_name, $vari_tate_name, "\n"));
		} else {
			push (@mailTemplate_base_item, sprintf('◇商品名 %s%s', &errstrRecover(&strBr($item_name_articles, 1)), "\n"));
		}
		if ($pretax_flg == 1) {
			push (@mailTemplate_base_item, sprintf('◇価格 %s円(税抜 %s円)%s', &convertMoney($unit_price), &convertMoney($pretax_price), "\n"));
		} else {
			push (@mailTemplate_base_item, sprintf('◇価格 %s円%s', &convertMoney($unit_price), "\n"));
		}
		push (@mailTemplate_base_item, sprintf('◇注文数 %s%s', &convertMoney($$value{"order_count"}), "\n"));
		push (@mailTemplate_base_item, sprintf('◇金額 %s円%s', &convertMoney($amount), "\n"));
		push (@mailTemplate_base_item, sprintf('◇配送タイプ %s%s', $delivery_line[1], "\n"));
		push (@mailTemplate_base_item, "\n");
	}
	
	my $total_amount	= 0;
	my $agent_flg		= 0;
	if ($FORM{'pay_num'}) {
		my $payment_file    = "$_CONFIG_server_ssl_www_root/cgi-bin/search/item_payment.cgi";
		open(DATA, $payment_file);
		my @payment_file = <DATA>;
		close(DATA);
		
		#_支払い方法
		my $pay_style = '';
		my @payment_line;
		if ($FORM{'pay_num'} != 0) {
			foreach (@payment_file) {
				@payment_line = split(/\t/, $_);
				if ($FORM{'pay_num'} == $payment_line[0]) {
					$agent_flg = 1 if ($FORM{'pay_num'} == 4);
					$pay_style = $payment_line[1];
					last;
				}
			}
		}
		
		#_割引
		my $cash_discount = 0;
		my $cash_discount_par = 0;
		if ($subtotal_amount > 0) {
			for (my $i = 0; $i < 3; $i++) {
				if (($_CONFIG_order_discount_condition[$i] ne '') && ($_CONFIG_order_discount_amount[$i] ne '')) {
					if ($_CONFIG_order_discount_condition[$i] <= $subtotal_amount) {
						$cash_discount_par = $_CONFIG_order_discount_amount[$i];
					}
				}
			}
			
			my $discount_flg = 1;
			if ($cash_discount_par) {
				$cash_discount = ($cash_discount_par * $subtotal_amount) / 100;
			}
		}
		#_端数の設定の処理
		if ($_CONFIG_tax_fraction eq 'D') {
			$cash_discount = int $cash_discount;
		}
		if ($_CONFIG_tax_fraction eq 'R') {
			$cash_discount = int ($cash_discount+ 0.5);
		}
		if ($_CONFIG_tax_fraction eq 'U') {
			$cash_discount = &ceil($cash_discount);
		}
		
		push (@mailTemplate_base_cost, sprintf('■小計 %s円%s', &convertMoney(int $subtotal_amount), "\n"));
		if ($cash_discount != 0) {
			push (@mailTemplate_base_cost, sprintf('■割引 %s円%s', &convertMoney($cash_discount), "\n"));
		}
		if ($_CONFIG_carriage_free_shipping_set ne '') {
			if ($subtotal_amount >= $_CONFIG_carriage_free_shipping_set) {
				$total_delivery = 0;
			}
		}
		#if ($_CONFIG_carriage_carriage_disp == 1) {
			push (@mailTemplate_base_cost, sprintf('■配送料 %s円%s', &convertMoney(int $total_delivery), "\n"));
		#}
		$total_amount = $subtotal_amount - $cash_discount + $total_delivery;
		push (@mailTemplate_base_cost, sprintf('■合計金額 %s円(税込)%s', &convertMoney($total_amount), "\n"));
		push (@mailTemplate_base_cost, sprintf('■支払い方法 %s%s', $pay_style, "\n"));
		my $commission = 0;
		if ($FORM{'pay_num'} != 0) {
			if ($payment_line[19] ne '' && $total_amount > $payment_line[19]) {
				$commission = $payment_line[20];
			} elsif ($payment_line[7] ne '' && $total_amount <= $payment_line[7]) {
				$commission = $payment_line[8];
			} elsif ($payment_line[9] ne '' && $total_amount <= $payment_line[9]) {
				$commission = $payment_line[10];
			} elsif ($payment_line[11] ne '' && $total_amount <= $payment_line[11]) {
				$commission = $payment_line[12];
			} elsif ($payment_line[13] ne '' && $total_amount <= $payment_line[13]) {
				$commission = $payment_line[14];
			} elsif ($payment_line[15] ne '' && $total_amount <= $payment_line[15]) {
				$commission = $payment_line[16];
			} elsif ($payment_line[17] ne '' && $total_amount <= $payment_line[17]) {
				$commission = $payment_line[18];
			}
			if ($commission != 0) {
				push (@mailTemplate_base_cost, sprintf('          ■手数料 %s円%s', &convertMoney(int $commission), "\n"));
				if ($FORM{'pay_num'} == 2) {
					my $commission_discount;
					if ($_CONFIG_order_commission_condition[0] ne '') {
						$commission_discount = $_CONFIG_order_commission_amount[0] if ($total_amount >= $_CONFIG_order_commission_condition[0]);
					}
					if ($_CONFIG_order_commission_condition[1] ne '') {
						$commission_discount = $_CONFIG_order_commission_amount[1] if ($total_amount >= $_CONFIG_order_commission_condition[1]);
					}
					if ($_CONFIG_order_commission_condition[2] ne '') {
						$commission_discount = $_CONFIG_order_commission_amount[2] if ($total_amount >= $_CONFIG_order_commission_condition[2]);
					}

					if ( 0 ne (int $commission_discount) ) {
						push (@mailTemplate_base_cost, sprintf('          ■手数料割引 %s円%s', &convertMoney(int $commission_discount), "\n"));
						$commission -= $commission_discount;
						push (@mailTemplate_base_cost, sprintf('          ■手数料合計 %s円%s', &convertMoney(int $commission), "\n"));
					}
				}
#				push (@mailTemplate_base_cost, sprintf('          ■手数料合計 %s円%s', int $commission, "\n"));
			}
		}
	}
	
	my $order_user_mail = $FORM{'mail'};
	my $template = HTML::Template->new(filename => "./$_CONFIG_template_dir/order_form_jump.tmp");
	
	my $order_mail_header_name = '';
	if (($FORM{'lname'}) || ($FORM{'fname'})) {
		$order_mail_header_name = sprintf('%s %s 様(%s)%s%s', $FORM{'lname'}, $FORM{'fname'}, $order_user_mail, "\n", "\n");
	} elsif ($FORM{'cname'}) {
		$order_mail_header_name = sprintf('%s 様(%s)%s%s', $FORM{'cname'}, $order_user_mail, "\n", "\n");
	} else {
		$order_mail_header_name = sprintf('%s 様%s%s', $order_user_mail, "\n", "\n");
	}
	$_CONFIG_order_mail_header = &errstrRecover(&strBr($_CONFIG_order_mail_header, 1));
	$_CONFIG_order_mail_header = $order_mail_header_name . $_CONFIG_order_mail_header;
	$_CONFIG_order_mail_footer = &errstrRecover(&strBr($_CONFIG_order_mail_footer, 1));
	
	foreach my $line (@data_file) {
		my @data_line = split(/\t/, $line);
		if ($data_line[0] == $item_code) {
			$item_name = $data_line[4];
		}
	}
	unless (&mailChecker($order_user_mail)) {
		$err = 1;
	}
	unless (&mailChecker($_CONFIG_order_mail_address)) {
		$err = 1;
	}
	
	for (my $i = 0; $i < @mailTemplate_user; $i++) {
		if ($mailTemplate_user[$i] =~ /\$SUBSTR_order_mail_1/) {
			$mailTemplate_user[$i] =~ s/\$SUBSTR_order_mail_1/$_CONFIG_order_mail_header/;
		}
		if ($mailTemplate_user[$i] =~ /\$SUBSTR_order_mail_2/) {
			$mailTemplate_user[$i] =~ s/\$SUBSTR_order_mail_2/@mailTemplate_base_main/;
		}
		if ($mailTemplate_user[$i] =~ /\$SUBSTR_order_mail_3/) {
			$mailTemplate_user[$i] =~ s/\$SUBSTR_order_mail_3/@mailTemplate_base_deli/;
		}
		if ($mailTemplate_user[$i] =~ /\$SUBSTR_order_mail_4/) {
			$mailTemplate_user[$i] =~ s/\$SUBSTR_order_mail_4/@mailTemplate_base_item/;
		}
		if ($mailTemplate_user[$i] =~ /\$SUBSTR_order_mail_5/) {
			$mailTemplate_user[$i] =~ s/\$SUBSTR_order_mail_5/@mailTemplate_base_cost/;
		}
		if ($mailTemplate_user[$i] =~ /\$SUBSTR_order_mail_6/) {
			$mailTemplate_user[$i] =~ s/\$SUBSTR_order_mail_6/$_CONFIG_order_mail_footer/;
		}
	}
	if ($err == 0 && $_CONFIG_page_view_mode ne 'P') {
		&send_mail_Send($_CONFIG_order_mail_address, $order_user_mail, &errstrRecover(&strBr($_CONFIG_order_mail_subject, 1)), join ('', @mailTemplate_user));
	}
	
	my $submit_url = '';
	if ($_CONFIG_server_ssl_use == 1 ) {
		$submit_url = sprintf('%s送信元URL=%s/cgi-bin/order_form_jump.cgi', "\n", $_CONFIG_server_ssl_site_addr);
	} else {
		$submit_url = sprintf('%s送信元URL=%s/cgi-bin/order_form_jump.cgi', "\n", $_CONFIG_server_url);
	}
	
	for (my $i = 0; $i < @mailTemplate_owner; $i++) {
		if ($mailTemplate_owner[$i] =~ /\$SUBSTR_order_mail_1/) {
			$mailTemplate_owner[$i] =~ s/\$SUBSTR_order_mail_1/@mailTemplate_base_main/;
		}
		if ($mailTemplate_owner[$i] =~ /\$SUBSTR_order_mail_2/) {
			$mailTemplate_owner[$i] =~ s/\$SUBSTR_order_mail_2/@mailTemplate_base_deli/;
		}
		if ($mailTemplate_owner[$i] =~ /\$SUBSTR_order_mail_3/) {
			$mailTemplate_owner[$i] =~ s/\$SUBSTR_order_mail_3/@mailTemplate_base_time/;
		}
		if ($mailTemplate_owner[$i] =~ /\$SUBSTR_order_mail_4/) {
			$mailTemplate_owner[$i] =~ s/\$SUBSTR_order_mail_4/@mailTemplate_base_item/;
		}
		if ($mailTemplate_owner[$i] =~ /\$SUBSTR_order_mail_5/) {
			$mailTemplate_owner[$i] =~ s/\$SUBSTR_order_mail_5/@mailTemplate_base_cost/;
		}
		if ($mailTemplate_owner[$i] =~ /\$SUBSTR_order_mail_6/) {
			$mailTemplate_owner[$i] =~ s/\$SUBSTR_order_mail_6/$submit_url/;
		}
	}
	
	if ($err == 0 && $_CONFIG_page_view_mode ne 'P') {
		&send_mail_Send($order_user_mail, $_CONFIG_order_mail_address, $order_mail_subject_owner, join ('', @mailTemplate_owner));
	}
	if ($return_msg ne '') {
		$ask_comment = $return_msg;
	}
	
	
	#_在庫も減らす
	foreach our $line (@cart_data) {
		&itemMainDataSplit;
		if ($item_stock_setting_flg) {
			my $edit_check = 0;
			my $stock_file = sprintf('%s/cgi-bin/search/%02d/%02d_stock.cgi', $_CONFIG_server_ssl_www_root, $item_cmd_category_id, $item_product_grp_id);
			open(DATA, $stock_file);
			my @stock_file = <DATA>;
			close(DATA);
			my $i = 0;
			foreach (@stock_file) {
				my @stock_line = split(/\t/, $_);
				$stock_line[0] =~ /^(\d{8})(\d{2})(\d{2})/;
				my $stk_item_code = $1;
				my $stk_h_code    = $3;
				my $stk_v_code    = $2;
				$item_group_name =~ /^(\d{2})(\d{2})/;
				my $line_vari_v = $1;
				my $line_vari_h = $2;
				if ($item_cmd_basic_id eq $stk_item_code) {
					if (($stk_h_code eq '00' && $stk_v_code eq '00') || ($stk_h_code eq $line_vari_h && $stk_v_code eq $line_vari_v)) {
						$stock_file[$i] = sprintf('%s	%s	%s', $stock_line[0], $stock_line[1] - $item_order_count, $stock_line[2], "\n");
						$edit_check++;
					}
				}
				$i++;
			}
			if ($edit_check > 0) {
				open(OUT,"> $stock_file");
				print OUT @stock_file;
				close(OUT);
			}
		}
	}

#	my $top_url;
#	if (($_CONFIG_server_ssl_use == 1) && ($_CONFIG_page_view_mode ne 'P')) {
#		$top_url = sprintf('%s/', $_CONFIG_server_url);
#	} else {
#		$top_url = '../';
#	}
	
	$template->param(
		todouhuken       => $FORM{'todouhuken'},
		sp_todouhuken    => $FORM{'sp_todouhuken'},
		timestamp        => time,
		pay_num          => $FORM{'pay_num'},
	);
	
	#_正常終了した時点でカート情報削除
	#&delAllSession($session_name);
	
	my $msg = sprintf('ID=%s メール送信完了', $session->id);
	&outputLog($msg);
	print $_CONFIG_base_head;
	print $template -> output;


	$session->flush();

	&chmodSessionFile ($session_pass, $_CONFIG_session_file_header, $session_id);


exit;

