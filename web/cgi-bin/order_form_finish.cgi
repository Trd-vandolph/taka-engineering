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
	our $_CONFIG_order_tag_finish;
	
	our $_CONFIG_server_ssl_use;
	our $_CONFIG_server_url;
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
	
	our $_CONFIG_order_mail_address   = "";
	our $_CONFIG_order_mail_subject   = "";
	our $_CONFIG_order_mail_header    = "";
	our $_CONFIG_order_mail_footer    = "";
	our $_CONFIG_order_finish_comment = "";
	our $_CONFIG_server_ssl_www_root;
	our $_CONFIG_page_view_mode;
	our $_CONFIG_server_ssl_site_addr;
	our $_CONFIG_server_url;
	
	our @item_vari_h_clm;
	our @item_vari_v_clm;
	our $_CONFIG_template_dir;
	
	our $_CONFIG_session_dir;
	our $_CONFIG_session_file_header;

	my $ask_recieve_mail       = "";
	my $ask_mail_subject       = "";
	my $ask_mail_header        = "";
	my $ask_mail_footer        = "";
	my $ask_comment            = "";
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
	our $session      = CGI::Session->new(undef, $COOKIE{$session_name}, {Directory=>$session_pass});
	our $session_cart = $session->param($session_name);
	our $session_id   = $session->id;
	
	#セッションチェック
	#&isSessionCartEmpty;

	$session->expire('+'.$session_timer.'m');
	
	
	my $load_file = "$_CONFIG_server_ssl_www_root/cgi-bin/search/user_askItem_config_data.cgi";
	my $mailTemplate_user  = "$_CONFIG_server_ssl_www_root/cgi-bin/mail/mailTemplate_askItem_user.cgi";
	my $mailTemplate_owner = "$_CONFIG_server_ssl_www_root/cgi-bin/mail/mailTemplate_askItem_owner.cgi";
	
	open(FILE, $load_file);
	my @load_file = <FILE>;
	close(FILE);
	open(FILE, $mailTemplate_user);
	my @mailTemplate_user = <FILE>;
	close(FILE);
	open(FILE, $mailTemplate_owner);
	my @mailTemplate_owner = <FILE>;
	close(FILE);
	
	my $subtotal_amount	= 0;
	my $total_delivery	= 0;
	my @delivery_back = ();
	my @cart_data = ();
	
	my $item_name		= '';
	my $item_count		= 0;
	my $max_unit_price	= 0;
	foreach my $value (@{$session_cart}) {
		$$value{"item_code"} =~ /^(\d{2})(\d{2})(\d{8})(\d{2})(\d{2})/;
		my $insert_line = '';
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
		
		foreach (@data_file) {
			my @data_line = split(/\t/, $_);
			if ($data_line[0] eq $line_ic) {
				$insert_line = join("\t", @data_line);
				$insert_line = $insert_line . "\t" . $line_vari_v . $line_vari_h . "\t" . $$value{"order_count"};
				last;
			}
		}
		push (@cart_data, $insert_line);
		our $line = $insert_line;
		&itemMainDataSplit;
		
		my $unit_price		= 0;
		my $pretax_flg		= 0;
		my $pretax_price	= 0;
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
			$pretax_flg = 1;
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
		my $unit_delivery;
		my $delivery_pref;
		if ($FORM{'sp_todouhuken'}) {
			$delivery_pref = $FORM{'s_pref'}
		} else {
			$delivery_pref = $FORM{'pref'}
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
				push (@delivery_back, $delivery_line[0])
			}
		} elsif ($_CONFIG_carriage_compu_method eq 'C') {
			$total_delivery += $unit_delivery;
		}
		
		my ($vari_yoko_name, $vari_tate_name);
		$vari_yoko_name = $item_vari_h_clm[$line_vari_h];
		$vari_tate_name = $item_vari_v_clm[$line_vari_v];
		
		if ($max_unit_price < $unit_price) {
			if ($vari_yoko_name || $vari_tate_name) {
				$item_name = sprintf('%s(%s・%s)', $item_name_articles, $vari_yoko_name, $vari_tate_name);
			} else {
				$item_name = sprintf('%s', $item_name_articles);
			}
		}
		$item_count++;
	}
	
	if ($item_count > 1) {
		$item_name = sprintf('%s 他', $item_name);
	}
	
	my $total_amount	= 0;
	my $agent_flg		= 0;
	my $commission		= 0;
	if ($FORM{'pay_num'}) {
		my $payment_file    = "$_CONFIG_server_ssl_www_root/cgi-bin/search/item_payment.cgi";
		open(DATA, $payment_file);
		my @payment_file = <DATA>;
		close(DATA);
		
		#_支払い方法
		my $pay_style		= '';
		my @payment_line	= '';
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
		my $cash_discount		= 0;
		my $cash_discount_par	= 0;
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
		
		push (@mailTemplate_base, sprintf('※お支払い金額・方法%s', "\n"));
		push (@mailTemplate_base, sprintf('■小計 %s円%s', &convertMoney(int $subtotal_amount), "\n"));
		push (@mailTemplate_base, sprintf('■割引 %s円%s', &convertMoney($cash_discount), "\n"));
		if ($_CONFIG_carriage_free_shipping_set ne '') {
			if ($subtotal_amount >= $_CONFIG_carriage_free_shipping_set) {
				$total_delivery = 0;
			}
		}
		if ($_CONFIG_carriage_carriage_disp == 1) {
			push (@mailTemplate_base, sprintf('■配送料 %s円%s', &convertMoney(int $total_delivery), "\n"));
		}
		$total_amount = $subtotal_amount - $cash_discount + $total_delivery;
		push (@mailTemplate_base, sprintf('■合計金額 %s円(税込)%s', &convertMoney($total_amount), "\n"));
		push (@mailTemplate_base, sprintf('■支払い方法 %s%s', $pay_style, "\n"));
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
				push (@mailTemplate_base, sprintf('          ■手数料 %s円%s', $commission, "\n"));
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
					push (@mailTemplate_base, sprintf('          ■手数料割引 %s円%s', $commission_discount, "\n"));
					$commission -= $commission_discount;
				}
				push (@mailTemplate_base, sprintf('          ■手数料合計 %s円%s', $commission, "\n"));
			}
		}
	}
	
	my $template = HTML::Template->new(filename => "./$_CONFIG_template_dir/order_form_finish.tmp");
	
	if ($return_msg ne '') {
		$ask_comment = $return_msg;
	}
	
	$template->param(
		sendmail_comment => $ask_comment,
	);
	

	my $kuronekoyamato_url='';
	my $trader_code='';
	my $order_no='';
	my $goods_name='';
	my $settle_price='';
	my $zeusu_url='';
	my $clientip='';
	my $money='';
	my $sumbit_flg='0';

	if ($agent_flg == 1) {
		my $agent_file    = "$_CONFIG_server_ssl_www_root/cgi-bin/search/item_agent.cgi";
		open(DATA, $agent_file);
		my @agent_file = <DATA>;
		close(DATA);
		
		my $form_agent_url;
		foreach (@agent_file) {
			my @agent_line = split(/\t/, $_);
			if ($total_amount > 300000) {
				if ($agent_line[0] == 2 && $agent_line[2] == 1) {
					$zeusu_url = $agent_line[5];
					$clientip = $agent_line[4];
					$money = ($total_amount + $commission);
					$sumbit_flg = '2';
#					$form_agent_url  = $agent_line[5] . '?';
#					$form_agent_url .= '&send=mail';
#					$form_agent_url .= "&clientip=$agent_line[4]";
#					$form_agent_url .= "&money=" . ($total_amount + $commission);
#					$form_agent_url .= '&custom=yes';
#					$form_agent_url .= '&telnocheck=yes';
#					$form_agent_url .= '&dtype=en';
					last;
				}
			} else {
				if ($agent_line[0] == 1 && $agent_line[2] == 1) {
					$kuronekoyamato_url = $agent_line[5];
					$trader_code = $agent_line[4];
					$order_no = ORDERNUMBER::getNumber($_CONFIG_server_ssl_www_root);
					$goods_name = $item_name;
					#$goods_name = Jcode::convert($item_name, "sjis", "utf8");
					$settle_price = ($total_amount + $commission);
					$sumbit_flg = '1';
#					$form_agent_url  = $agent_line[5] . '?';
#					$form_agent_url .= "&trader_code=$agent_line[4]";
#					$form_agent_url .= "&order_no=" . ORDERNUMBER::getNumber($_CONFIG_server_ssl_www_root);
#					$form_agent_url .= "&goods_name=" . &decodUrl($item_name);
#					$form_agent_url .= "&settle_price=" . ($total_amount + $commission);
					last;
				} elsif ($agent_line[0] == 2 && $agent_line[2] == 1) {
					$zeusu_url = $agent_line[5];
					$clientip = $agent_line[4];
					$money = ($total_amount + $commission);
					$sumbit_flg = '2';
#					$form_agent_url  = $agent_line[5] . '?';
#					$form_agent_url .= '&send=mail';
#					$form_agent_url .= "&clientip=$agent_line[4]";
#					$form_agent_url .= "&money=" . ($total_amount + $commission);
#					$form_agent_url .= '&custom=yes';
#					$form_agent_url .= '&telnocheck=yes';
#					$form_agent_url .= '&dtype=en';
					last;
				}
			}
		}
		$template->param(
			form_agent_url => $form_agent_url,
		);
	}
	
	my $top_url = '';
	if (($_CONFIG_server_ssl_use == 1) && ($_CONFIG_page_view_mode ne 'P')) {
		$top_url = sprintf('%s/', $_CONFIG_server_url);
	} else {
		$top_url = '../';
	}
	


	my $session_cart_num = @{$session_cart};
	if( $session_cart_num <= 0 ) {
#		&apricationErr($top_url);
	} else {
		#クレジット
		$session->param('trader_code', $trader_code);
		$session->param('order_no', $order_no);
		$session->param('goods_name', $goods_name);
		$session->param('settle_price', $settle_price);
		$session->param('zeusu_url', $zeusu_url);
		$session->param('clientip', $clientip);
		$session->param('money', $money);
		$session->param('sumbit_flg', $sumbit_flg);
	}



	$template->param(
		top_url            => $top_url,
		sendmail_comment   => &errstrRecover($_CONFIG_order_finish_comment),
		embedding_tag      => &errstrRecover($_CONFIG_order_tag_finish),
		kuronekoyamato_url => $kuronekoyamato_url,
		trader_code        => $session->param('trader_code'),
		order_no           => $session->param('order_no'),
		goods_name         => $session->param('goods_name'),
		settle_price       => $session->param('settle_price'),
		zeusu_url          => $session->param('zeusu_url'),
		clientip           => $session->param('clientip'),
		money              => $session->param('money'),
		sumbit_flg         => $session->param('sumbit_flg'),
	);
	
	#_正常終了した時点でカート情報削除
	&delAllSession($session_name);
	



	#セッションにあるメールデータを削除します。
	$session->param('lname', '');				#氏名（姓）
	$session->param('fname', '');				#氏名（名）
	$session->param('lname_kana', '');		#氏名（姓）カナ
	$session->param('fname_kana', '');		#氏名（名）カナ
	$session->param('cname', '');				#法人名
	$session->param('cname_kana', '');		#法人名カナ
	$session->param('department', '');		#所属部署/役職名
	$session->param('pcode_first', '');	#郵便番号上3桁
	$session->param('pcode_last', '');		#郵便番号下4桁
	$session->param('address', '');			#住所
	$session->param('mail', '');					#メールアドレス
	$session->param('mail_check', '');		#メールアドレス確認
	$session->param('pnum_1', '');				#電話番号（市外）
	$session->param('pnum_2', '');				#電話番号（市内）
	$session->param('pnum_3', '');				#電話番号（番号）
	$session->param('fnum_1', '');				#FAX番号（市外）
	$session->param('fnum_2', '');				#FAX番号（市内）
	$session->param('fnum_3', '');				#FAX番号（番号）
	$session->param('day_pnum_1', '');		#日中の連絡先（市外）
	$session->param('day_pnum_2', '');		#日中の連絡先（市内）
	$session->param('day_pnum_3', '');		#日中の連絡先（番号）
	$session->param('birthyear', '');		#生年月日（年）
	$session->param('birthmonth', '');		#生年月日（月）
	$session->param('birthday', '');			#生年月日（日）

	$session->param('dhope', '');			#配送等へのご希望
	$session->param('idea', '');			#連絡事項
	
	$session->param('sp_lname', '');				#氏名（姓）
	$session->param('sp_fname', '');					#氏名（名）
	$session->param('sp_lname_kana', '');		#氏名（姓）カナ
	$session->param('sp_fname_kana', '');		#氏名（名）カナ
	$session->param('sp_cname', '');					#法人名
	$session->param('sp_cname_kana', '');		#法人名カナ
	$session->param('sp_department', '');		#所属部署/役職名
	$session->param('sp_pcode_first', '');		#郵便番号上3桁
	$session->param('sp_pcode_last', '');		#郵便番号下4桁
	$session->param('sp_address', '');				#住所
	$session->param('sp_mail', '');					#メールアドレス
	$session->param('sp_mail_check', '');		#メールアドレス確認
	$session->param('sp_pnum_1', '');				#電話番号（市外）
	$session->param('sp_pnum_2', '');				#電話番号（市内）
	$session->param('sp_pnum_3', '');				#電話番号（番号）
	$session->param('sp_fnum_1', '');				#FAX番号（市外）
	$session->param('sp_fnum_2', '');				#FAX番号（市内）
	$session->param('sp_fnum_3', '');				#FAX番号（番号）
	$session->param('sp_day_pnum_1', '');		#日中の連絡先（市外）
	$session->param('sp_day_pnum_2', '');		#日中の連絡先（市内）
	$session->param('sp_day_pnum_3', '');		#日中の連絡先（番号）
	$session->param('sp_birthyear', '');			#生年月日（年）
	$session->param('sp_birthmonth', '');		#生年月日（月）
	$session->param('sp_birthday', '');			#生年月日（日）
		
	my $form_file = "$_CONFIG_server_ssl_www_root/cgi-bin/search/item_order_form.cgi";
	open(DATA, $form_file);
	my @form_file = <DATA>;
	close(DATA);
	@form_file = sort { (split(/\t/,$a))[6] <=> (split(/\t/,$b))[6] } @form_file;

	foreach (@form_file) {
		my @form_line = split(/\t/, $_);
		if ($form_line[9] eq 'A') {
			$session->param("order_$form_line[0]", '');
			$session->param("sp_order_$form_line[0]", '');
		}
	}

	
	my $msg = sprintf('ID=%s 注文完了', $session->id);
	&outputLog($msg);
	print $_CONFIG_base_head;
	print $template -> output;


	$session->flush();
	
exit;

