#!/usr/bin/perl
use CGI::Session qw/-ip_match/;
use CGI::Session::Cleaning;
use MODULE::Template;
use MODULE::StringUtil;
	
	our $_CONFIG_server_ssl_www_root;
	our $_CONFIG_page_view_mode;
	our $_CONFIG_server_ssl_site_addr;
	our $_CONFIG_server_url;
	our $_CONFIG_template_dir;

	our $_CONFIG_session_dir;
	our $_CONFIG_session_file_header;
	
	require './subroutine.pl';
	require './config_data.cgi';
	&formLoading;

	our $session_pass = "$_CONFIG_server_ssl_www_root/cgi-bin/$_CONFIG_session_dir";


	
	our $http_path;
	if ($_CONFIG_server_ssl_use ne '0' && $_CONFIG_page_view_mode ne 'P') {
		$http_path = sprintf('%s/cgi-bin', $_CONFIG_server_url);
		$FORM{'bpage'} =~ m|([^/]+)$|g;
		$FORM{'bpage'} = $http_path . '/' . $1;
	} else {
		$http_path = '../cgi-bin';
		$_CONFIG_server_ssl_www_root = '..';
	}
	
	my $template = HTML::Template->new(filename => "./$_CONFIG_template_dir/order_form.tmp");
	
	$session_name  = 'sessionCart';
	$session_timer = 30;
	
	&getCookie($session_name);
	if ($FORM{'seid'} ne '' && $_CONFIG_server_ssl_use eq '1' && $_CONFIG_page_view_mode ne 'P') {
		$COOKIE{$session_name} = $FORM{'seid'};
	}
	&cleanSession;
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
	
	$FORM{'saleItem_id'} =~ /(\d{2})(\d{2})(\d{8})/;
	my ($cc, $gc, $ic);
	if ($FORM{'cc'}) {
		$cc = $FORM{'cc'}
	} else {
		$cc = $1;
	};
	if ($FORM{'gc'}) {
		$gc = $FORM{'gc'}
	} else {
		$gc = $2
	};
	if ($FORM{'ic'}) {
		$ic = $FORM{'ic'}
	} else {
		$ic = $3
	}
	$valiation = $FORM{"radio_$ic"};
	$order_item_code = $FORM{'saleItem_id'} . $valiation;
	
	$bpage = &decodUrl($FORM{'bpage'});
	
	my $bpage_url  = $FORM{'bpage'};
	my $bpage_url_sub;
	if ($bpage_url =~ /saleItem_detailInfo/) {
		$bpage_url_sub .= sprintf('&cc=%02d', $cc) if ($cc);
		$bpage_url_sub .= sprintf('&gc=%02d', $gc) if ($gc);
		$bpage_url_sub .= sprintf('&ic=%08d', $ic) if ($ic);
	}
	$bpage_url_sub .= sprintf('&pid=%s', $FORM{'pid'}) if ($FORM{'pid'} ne '');
	$bpage_url_sub .= sprintf('&stype=%s', $FORM{'stype'}) if ($FORM{'stype'} ne '');
	$bpage_url_sub .= sprintf('&vtype=%s', $FORM{'vtype'}) if ($FORM{'vtype'} ne '');
	$bpage_url_sub .= sprintf('&ukeyword=%s', $FORM{'ukeyword'}) if ($FORM{'ukeyword'} ne '');
	$bpage_url_sub .= sprintf('&vnum=%s', $FORM{'vnum'}) if ($FORM{'vnum'} ne '');
	
	if ($bpage_url_sub) {
		$bpage_url .= '?' . $bpage_url_sub;
	}
	$bpage_para .= sprintf('&bpage=%s', $bpage);
	$bpage_para .= $bpage_url_sub;
	
	#if (($FORM{'saleItem_id'} ne '') && ($FORM{'order_quantity'} ne '') && ($FORM{'action'} eq '')) {
	#if (($FORM{'saleItem_id'} ne '') && ($FORM{'order_quantity'} ne '')) {
	#	&renewSession($order_item_code, $FORM{'order_quantity'}, $session_name);
	#}
	
	$session->expire('+'.$session_timer.'m');
	$session_cart = $session->param($session_name);
	$session_id   = $session->id;
	
	$setcook1 = &setCookie($session_name, $session_id);
	my $cnt = 0;
	my @LOOP_hash = ();
	my $subtotal_amount;
	
	my $cart_form_error;
	my $agent_error_flg;
	my $error_hinmei;
	
	if ($ENV{'HTTP_REFERER'} =~ /order_cart_info.cgi/ || $ENV{'HTTP_REFERER'} =~ /order_form.cgi/) {
		$FORM{'mailguide'} = '1';
		#_注文数エラーチェック
		foreach $value (@{$session_cart}) {
			my $error_flg;
			my $item_code      = $$value{"item_code"};
			my $order_quantity = $FORM{'order_quantity_' . $$value{"item_code"}};
			
			$item_code =~ /(\d{2})(\d{2})(\d{8})(\d{2})(\d{2})/;
			my $session_cc        = $1;
			my $session_gc        = $2;
			my $session_ic        = $3;
			my $line_vari_v       = $4;
			my $line_vari_h       = $5;
			
			my $data_file = sprintf('%s/cgi-bin/search/%02d/%02d.cgi', $_CONFIG_server_ssl_www_root, $session_cc, $session_gc);
			open(DATA, $data_file);
			my @data_file = <DATA>;
			close(DATA);
			chomp @data_file;
			
			my $session_line;
			foreach (@data_file) {
				my @data_line = split(/\t/, $_);
				if ($data_line[0] eq $session_ic) {
					$session_line = join("\t", @data_line);
					last;
				}
			}
			my $val_data_file = sprintf('%s/cgi-bin/search/%02d/%02d_variation.cgi', $_CONFIG_server_ssl_www_root, $session_cc, $session_gc);
			open(DATA, $val_data_file);
			my @val_data_file = <DATA>;
			close(DATA);
			foreach (@val_data_file) {
				my @data_line = split(/\t/, $_);
				if ($data_line[0] eq $session_ic) {
					$session_line = $session_line . join("\t", @data_line);
					last;
				}
			}
			$line = $session_line;
			&itemMainDataSplitFull;
			
			if ($error_flg eq '') {
				#_最大注文数以上
				if ($item_max_order_receipts ne '') {
					if ($order_quantity > $item_max_order_receipts) {
						$error_flg            = 1;
						$max_error_flg        = 1;
						$error_max_quantity   = $item_max_order_receipts;
						$error_order_quantity = $order_quantity;
					}
				}
			}
			if ($error_flg eq '') {
				#_注文数値チェック
				if (($order_quantity =~ /[\D]/) || ($order_quantity eq '') || ($order_quantity == 0)) {
					$error_flg           = 1;
					$incorrect_error_flg = 1;
					$order_quantity = '';
				}
			}
			my $stk_data_file = sprintf('%s/cgi-bin/search/%02d/%02d_stock.cgi', $_CONFIG_server_ssl_www_root, $session_cc, $session_gc);
			open(DATA, $stk_data_file);
			my @stk_data_file = <DATA>;
			close(DATA);
			$item_code =~ /(\d{12})$/;
			$order_val_code = $1;
			
			if ($error_flg eq '') {
				if ($item_stock_setting_flg) {
					foreach (@stk_data_file) {
						my @data_line = split(/\t/, $_);
						if ($order_val_code eq $data_line[0]) {
							if ($order_quantity > $data_line[1]) {
								$error_flg             = 1;
								$error_stock_error_flg = 1;
								$error_variation_code  = $item_vari_disp;
								$error_stock_quantity  = $data_line[1];
								$error_order_quantity  = $order_quantity;
							}
							last;
						}
					}
				}
			}
			if ($error_flg) {
				$error_hinmei = $item_name_articles;
				if ($item_vari_disp){
					$error_variation_code = 1;
					$error_yoko_title = $item_vari_h_name;
					$error_tate_title = $item_vari_v_name;
					$error_yoko_name  = $item_vari_h_clm[$line_vari_h];
					$error_tate_name  = $item_vari_v_clm[$line_vari_v];
				}
				$cart_form_error++;
			}
		}
		#_注文数の変更
		unless ($cart_form_error) {
			&renewSession($session_cart, %FORM);
			my $count = 0;
			foreach $value (@{$session_cart}) {
				&outputLog("item_code  :" . $$value{"item_code"});
				&outputLog("order_count:" . $$value{"order_count"});
				&outputLog("count      :" . $count);
			}
			$session_cart = $session->param($session_name);
		}
	}
	
	



	#_配送タイプ表示チェックフラグ
	my @deliveryCheck;
	
	foreach $value (@{$session_cart}) {
		
		$$value{"item_code"} =~ /^(\d{2})(\d{2})(\d{8})(\d{2})(\d{2})/;

		my $insert_line;
		
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
				$insert_line = $insert_line . join("\t", @data_line);
				last;
			}
		}
		
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
		
		$line = $insert_line;
		&itemMainDataSplitFull;
		
		my $unit_price;
		my $pretax_flg;
		my $pretax_price;
		my $unit_price_tax_on;
		my $pretax_flg = $_CONFIG_tax_indication;
		if ($_CONFIG_tax_consumer eq 'I') {
			$pretax_flg = '';
			if ($item_sp_price_flag != 0) {
				$pretax_price = $item_money_sp_price_tax;
				$unit_price = $item_money_sp_price_tax;
			} else {
				$pretax_price = $item_including_tax_price;
				$unit_price = $item_including_tax_price;
			}
		} else {
			if ($item_sp_price_flag != 0) {
				$pretax_price = $item_money_sp_price;
				$unit_price = $item_money_sp_price_tax;
			} else {
				$pretax_price = $item_price;
				$unit_price = $item_including_tax_price;
			}
		}
		
		my $hash = "";
		my $amount = $unit_price * $$value{"order_count"};
		
		$subtotal_amount += $amount;
		
		$vari_yoko_name = $item_vari_h_clm[$line_vari_h];
		$vari_tate_name = $item_vari_v_clm[$line_vari_v];
		$hash = {
			main_img_url   => &checkUri(&imgCheck($item_cmd_image_uri_nail, $item_cmd_image_uri_main, 'S'), 1),
			hinmei         => $item_name_articles,
			unit_price     => &convertMoney($unit_price),
			pretax_price   => &convertMoney($pretax_price),
			amount         => &convertMoney($amount),
			pretax_flg     => $pretax_flg,
			delivery_name  => &deliveryOut($item_deli_type_id),
			order_quantity => $$value{"order_count"},
			variation_flg  => $item_vari_disp,
			vari_yoko_name => $vari_yoko_name,
			vari_tate_name => $vari_tate_name,
		};
		push(@LOOP_hash, $hash);
		$deliveryCheck[$item_deli_type_id]++;
	}
	
	$template->param(PURCHASE_LOOP => \@LOOP_hash);
	
	my @LOOP_hash = ();
	my $cash_discount = 0;
	my $cash_discount_par;
	
	for (my $i = 0; $i < 3; $i++) {
		if (($_CONFIG_order_discount_condition[$i] ne '') && ($_CONFIG_order_discount_amount[$i] ne '')) {
			if ($subtotal_amount > 0) {
				if ($_CONFIG_order_discount_condition[$i] <= $subtotal_amount) {
					$cash_discount_par = $_CONFIG_order_discount_amount[$i];
				}
			}
			$hash = {
				discount_if    => &convertMoney($_CONFIG_order_discount_condition[$i]),
				discount_per   => $_CONFIG_order_discount_amount[$i],
			};
			push(@LOOP_hash, $hash);
		}
	}
	
	my $discount_flg;
	if (@LOOP_hash > 0) {
		$discount_flg = 1;
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
	
	$template->param(DISCOUNT_LOOP => \@LOOP_hash);
	my $total_amount = $subtotal_amount - $cash_discount;
	
	
	my $data_file = "$_CONFIG_server_ssl_www_root/cgi-bin/item_delivery.cgi";
	open(DATA, $data_file);
	my @data_file = <DATA>;
	close(DATA);
	chomp @data_file;
	
	my @LOOP_hash = ();
	my $delivery_flg;

	my $delivery_type_flg = 0;
	my $delivery_uniform  = 0;

	foreach (@data_file) {
		chomp $_;
		my @data_line = split(/\t/, $_);
		
		#_配送タイプ表示チェック
		next if $deliveryCheck[$data_line[0]] < 1;
		
		if ($data_line[2] eq 'U') {
			$delivery_type_flg = 1;
		} else {
			$delivery_type_flg = 0;
		}

		$delivery_uniform  = &convertMoney($data_line[3]);

		my $delivery_comment_flg;
		if ($data_line[51]) {
			$delivery_comment_flg = 1;
		}
		$hash = {
			delivery_name        => &convertMoney($data_line[1]),
			delivery_area_1      => &convertMoney($data_line[4]),
			delivery_area_2      => &convertMoney($data_line[5]),
			delivery_area_3      => &convertMoney($data_line[6]),
			delivery_area_4      => &convertMoney($data_line[7]),
			delivery_area_5      => &convertMoney($data_line[8]),
			delivery_area_6      => &convertMoney($data_line[9]),
			delivery_area_7      => &convertMoney($data_line[10]),
			delivery_area_8      => &convertMoney($data_line[11]),
			delivery_area_9      => &convertMoney($data_line[12]),
			delivery_area_10     => &convertMoney($data_line[13]),
			delivery_area_11     => &convertMoney($data_line[14]),
			delivery_area_12     => &convertMoney($data_line[15]),
			delivery_area_13     => &convertMoney($data_line[16]),
			delivery_area_14     => &convertMoney($data_line[17]),
			delivery_area_15     => &convertMoney($data_line[22]),
			delivery_area_16     => &convertMoney($data_line[25]),
			delivery_area_17     => &convertMoney($data_line[23]),
			delivery_area_18     => &convertMoney($data_line[18]),
			delivery_area_19     => &convertMoney($data_line[19]),
			delivery_area_20     => &convertMoney($data_line[20]),
			delivery_area_21     => &convertMoney($data_line[21]),
			delivery_area_22     => &convertMoney($data_line[24]),
			delivery_area_23     => &convertMoney($data_line[26]),
			delivery_area_24     => &convertMoney($data_line[27]),
			delivery_area_25     => &convertMoney($data_line[28]),
			delivery_area_26     => &convertMoney($data_line[29]),
			delivery_area_27     => &convertMoney($data_line[30]),
			delivery_area_28     => &convertMoney($data_line[31]),
			delivery_area_29     => &convertMoney($data_line[32]),
			delivery_area_30     => &convertMoney($data_line[33]),
			delivery_area_31     => &convertMoney($data_line[34]),
			delivery_area_32     => &convertMoney($data_line[35]),
			delivery_area_33     => &convertMoney($data_line[36]),
			delivery_area_34     => &convertMoney($data_line[37]),
			delivery_area_35     => &convertMoney($data_line[38]),
			delivery_area_36     => &convertMoney($data_line[40]),
			delivery_area_37     => &convertMoney($data_line[39]),
			delivery_area_38     => &convertMoney($data_line[41]),
			delivery_area_39     => &convertMoney($data_line[42]),
			delivery_area_40     => &convertMoney($data_line[43]),
			delivery_area_41     => &convertMoney($data_line[44]),
			delivery_area_42     => &convertMoney($data_line[45]),
			delivery_area_43     => &convertMoney($data_line[46]),
			delivery_area_44     => &convertMoney($data_line[47]),
			delivery_area_45     => &convertMoney($data_line[48]),
			delivery_area_46     => &convertMoney($data_line[49]),
			delivery_area_47     => &convertMoney($data_line[50]),
			delivery_comment_flg => $delivery_comment_flg,
			delivery_comment     => $data_line[51],
			delivery_type_flg    => $delivery_type_flg,
			delivery_uniform     => $delivery_uniform,
		};
		push(@LOOP_hash, $hash);
	}
	$template->param(DELIVERY_LOOP => \@LOOP_hash);
	
	
	
#	#_注文フォームグリッド
#	my $form_file = "$_CONFIG_server_ssl_www_root/cgi-bin/search/item_order_form.cgi";
#	open(DATA, $form_file);
#	my @form_file = <DATA>;
#	close(DATA);
	
	@form_file = sort { (split(/\t/,$a))[6] <=> (split(/\t/,$b))[6] } @form_file;
	
	my @CART_LOOP = ();
	my @MUST_ERROR_LOOP = ();
	my @INCORRECT_ERROR_LOOP = ();
	
	my $must_flg = 0;
	
	#_項目数をカウント
	my $delivery_counter;
	my $pay_counter   = 0;
	foreach (@form_file) {
		my @form_line = split(/\t/, $_);
		my @PAY_LOOP      = ();
		my @PULLDOWN_LOOP = ();
		my @CHECKBOX_LOOP = ();
		my @RADIO_LOOP    = ();
		if ($form_line[4] != 0) {
			$delivery_counter++;
		}
		if ($form_line[2] != 0) {
			my $error_check_flg_must = 0;
			my $form_input_flg = 0;
			
			my $credit_flg				= 0;
			my $daikou_flg				= 0;
			my $visa_flg				= 0;
			my $master_flg				= 0;
			my $jcb_flg					= 0;
			my $amex_flg				= 0;
			my $diners_flg				= 0;
			my $cerdit_description_flg	= 0;

			my $order_must_flg = 0;
			my $name_flg       = 0;
			my $cname_flg      = 0;
			my $department_flg = 0;
			my $address_flg    = 0;
			my $mail_flg       = 0;
			my $pay_flg        = 0;
			my $pnum_flg       = 0;
			my $fnum_flg       = 0;
			my $day_pnum_flg   = 0;
			my $birth_flg      = 0;
			my $seibetu_flg    = 0;
			my $addItem_flg    = 0;

			if ($form_line[3]) {
				$order_must_flg = 1 ;
				$must_flg = 1;
			}
			$name_flg       = 1 if ($form_line[0] == 1);
			$cname_flg      = 1 if ($form_line[0] == 2);
			$department_flg = 1 if ($form_line[0] == 3);
			$address_flg    = 1 if ($form_line[0] == 4);
			$mail_flg       = 1 if ($form_line[0] == 5);
			$pay_flg        = 1 if ($form_line[0] == 6);
			$pnum_flg       = 1 if ($form_line[0] == 7);
			$fnum_flg       = 1 if ($form_line[0] == 8);
			$day_pnum_flg   = 1 if ($form_line[0] == 9);
			$birth_flg      = 1 if ($form_line[0] == 10);
			$seibetu_flg    = 1 if ($form_line[0] == 11);
			$addItem_flg    = 1 if ($form_line[0] >= 12);
			
			if ($pay_flg) {
				my $payment_file = "$_CONFIG_server_ssl_www_root/cgi-bin/search/item_payment.cgi";
				open(DATA, $payment_file);
				my @payment_file = <DATA>;
				close(DATA);
				
				@payment_file = sort { (split(/\t/,$a))[3] <=> (split(/\t/,$b))[3] } @payment_file;
				
				PAYMENT:foreach (@payment_file) {
					my @payment_line = split(/\t/, $_);
					my $pay_s_flg = 0;
					$pay_s_flg = 1 if ($payment_line[0] == $FORM{'pay_num'});
					if ($payment_line[0] == 4 && $payment_line[2] ne '0') {
						my $agent_file = "$_CONFIG_server_ssl_www_root/cgi-bin/search/item_agent.cgi";
						open(DATA, $agent_file);
						my @agent_file = <DATA>;
						close(DATA);
						
						my $agent_count;
						foreach (@agent_file) {
							my @agent_line = split(/\t/, $_);
							if ($agent_line[2] != 0) {
								$agent_count++;
							}
						}
						foreach (@agent_file) {
							my @agent_line = split(/\t/, $_);
							#_表示フラグが0の場合次へ
							next if ($agent_line[2] == 0);
							if ($total_amount > 300000) {
								if ($agent_line[0] == 2) {
									$visa_flg               = 1 if ($agent_line[7] != 0);
									$master_flg             = 1 if ($agent_line[8] != 0);
									$jcb_flg                = 1 if ($agent_line[9] != 0);
									$amex_flg               = 1 if ($agent_line[10] != 0);
									$diners_flg             = 1 if ($agent_line[11] != 0);
									$cerdit_description_flg = 1 if ($agent_line[6] ne '');
									$cerdit_description     = $agent_line[6];
									$credit_flg = 1;
									last;
								} elsif (($agent_line[0] == 1) && ($agent_count == 1)) {
									next PAYMENT;
									#_30万オーバーでクロネコのみ選択時は表示無し
								} else {
									next;
								}
							} else {
								if ($agent_line[0] == 1) {
									$visa_flg               = 1 if ($agent_line[7] != 0);
									$master_flg             = 1 if ($agent_line[8] != 0);
									$jcb_flg                = 1 if ($agent_line[9] != 0);
									$amex_flg               = 1 if ($agent_line[10] != 0);
									$diners_flg             = 1 if ($agent_line[11] != 0);
									$cerdit_description_flg = 1 if ($agent_line[6] ne '');
									$cerdit_description     = $agent_line[6];
									$daikou_flg             = 1;
									$credit_flg = 1;
									last;
								} elsif (($agent_line[0] == 2) && ($agent_count == 1)) {
									$visa_flg               = 1 if ($agent_line[7] != 0);
									$master_flg             = 1 if ($agent_line[8] != 0);
									$jcb_flg                = 1 if ($agent_line[9] != 0);
									$amex_flg               = 1 if ($agent_line[10] != 0);
									$diners_flg             = 1 if ($agent_line[11] != 0);
									$cerdit_description_flg = 1 if ($agent_line[6] ne '');
									$cerdit_description     = $agent_line[6];
									$credit_flg = 1;
									last;
								} else {
									next;
								}
							}
						}
					}
					if ($payment_line[2]) {
						my $sub_hash = {
							pay_num    => $payment_line[0],
							pay_option => $payment_line[1],
							pay_s_flg  => $pay_s_flg,
						};
						push(@PAY_LOOP, $sub_hash);
						$pay_counter++;
					}
				}
				
			}
			
			my $pulldown_flg		= 0;
			my $pd_name				= '';
			my $checkbox_flg		= 0;
			my $radio_flg			= 0;
			my $order_item_name		= '';
			my $order_item_explan	= '';
			my $text_id				= '';
			my $text_item			= '';
			my $text_flg			= '';
			
			if ($addItem_flg) {
				$order_item_name   = $form_line[1];
				$order_item_explan = $form_line[8];
				$pd_name           = 'order_' . $form_line[0];
				if ($form_line[9] eq 'S') {
					$pulldown_flg = 1;
					my @option_list = split(/<RETURN>/, $form_line[10]);
					chomp @option_list;
					my $i = 1;
					foreach (@option_list) {
						my $pd_id = $i;
						my $pd_s_flg = 0;
						$pd_s_flg = 1 if ($i == $FORM{"order_$form_line[0]"});
						my $sub_hash = {
							pd_id     => $pd_id,
							pd_s_flg  => $pd_s_flg,
							pd_option => $_,
						};
						push(@PULLDOWN_LOOP, $sub_hash);
						$i++;
					}
				} elsif ($form_line[9] eq 'C') {
					$checkbox_flg = 1;
					my @option_list = split(/<RETURN>/, $form_line[10]);
					chomp @option_list;
					my $i = 1;
					foreach (@option_list) {
						my $c_id = 'order_' . $form_line[0] . '_' . $i;
						my $sub_hash = {
							c_name   => $c_id,
							c_id     => $c_id,
							c_s_flg  => $FORM{"order_$form_line[0]_$i"},
							c_option => $_,
						};
						push(@CHECKBOX_LOOP, $sub_hash);
						$i++;
					}
				} elsif ($form_line[9] eq 'R') {
					$radio_flg = 1;
					my @option_list = split(/<RETURN>/, $form_line[10]);
					chomp @option_list;
					my $i = 1;
					foreach (@option_list) {
						my $r_s_flg = 0;
						if ($i == $FORM{"order_$form_line[0]"}) {
							$r_s_flg = 1;
						}
						my $r_id = 'order_' . $form_line[0];
						my $sub_hash = {
							r_name   => $r_id,
							r_id     => $i,
							r_s_flg  => $r_s_flg,
							r_option => $_,
						};
						push(@RADIO_LOOP, $sub_hash);
						$i++;
					}
				} elsif ($form_line[9] eq 'A') {
					$text_id   = 'order_' . $form_line[0];
					$text_item = $FORM{"order_$form_line[0]"};
					$text_flg  = 1;
				}
			}
			
			my @area_flg;
			$area_flg[$FORM{'todouhuken'}] = 1;
#			$sei_fm_flg = 1 if ($FORM{'sei_fm_flg'} eq 'm');
			my $sei_fm_m_flg = '';
			my $sei_fm_f_flg = '';
			if ( $FORM{'sei_fm_flg'} eq 'm' ) {
				$sei_fm_m_flg = 1;
				$sei_fm_f_flg = 0;
			} elsif ( $FORM{'sei_fm_flg'} eq 'f' ) {
				$sei_fm_m_flg = 0;
				$sei_fm_f_flg = 1;
			} else {
				$sei_fm_m_flg = 0;
				$sei_fm_f_flg = 0;
			}
			$hash = {
				order_must_flg         => $order_must_flg,
				name_flg               => $name_flg,
				lname                  => MODULE::StringUtil::conversionSpecialChar($FORM{'lname'}),
				fname                  => MODULE::StringUtil::conversionSpecialChar($FORM{'fname'}),
				lname_kana             => MODULE::StringUtil::conversionSpecialChar($FORM{'lname_kana'}),
				fname_kana             => MODULE::StringUtil::conversionSpecialChar($FORM{'fname_kana'}),
				cname_flg              => $cname_flg,
				cname                  => MODULE::StringUtil::conversionSpecialChar($FORM{'cname'}),
				cname_kana             => MODULE::StringUtil::conversionSpecialChar($FORM{'cname_kana'}),
				department_flg         => $department_flg,
				department             => MODULE::StringUtil::conversionSpecialChar($FORM{'department'}),
				address_flg            => $address_flg,
				pcode_first            => MODULE::StringUtil::conversionSpecialChar($FORM{'pcode_first'}),
				pcode_last             => MODULE::StringUtil::conversionSpecialChar($FORM{'pcode_last'}),
				area1_flg              => $area_flg[1],
				area2_flg              => $area_flg[2],
				area3_flg              => $area_flg[3],
				area4_flg              => $area_flg[4],
				area5_flg              => $area_flg[5],
				area6_flg              => $area_flg[6],
				area7_flg              => $area_flg[7],
				area8_flg              => $area_flg[8],
				area9_flg              => $area_flg[9],
				area10_flg             => $area_flg[10],
				area11_flg             => $area_flg[11],
				area12_flg             => $area_flg[12],
				area13_flg             => $area_flg[13],
				area14_flg             => $area_flg[14],
				area15_flg             => $area_flg[15],
				area16_flg             => $area_flg[16],
				area17_flg             => $area_flg[17],
				area18_flg             => $area_flg[18],
				area19_flg             => $area_flg[19],
				area20_flg             => $area_flg[20],
				area21_flg             => $area_flg[21],
				area22_flg             => $area_flg[22],
				area23_flg             => $area_flg[23],
				area24_flg             => $area_flg[24],
				area25_flg             => $area_flg[25],
				area26_flg             => $area_flg[26],
				area27_flg             => $area_flg[27],
				area28_flg             => $area_flg[28],
				area29_flg             => $area_flg[29],
				area30_flg             => $area_flg[30],
				area31_flg             => $area_flg[31],
				area32_flg             => $area_flg[32],
				area33_flg             => $area_flg[33],
				area34_flg             => $area_flg[34],
				area35_flg             => $area_flg[35],
				area36_flg             => $area_flg[36],
				area37_flg             => $area_flg[37],
				area38_flg             => $area_flg[38],
				area39_flg             => $area_flg[39],
				area40_flg             => $area_flg[40],
				area41_flg             => $area_flg[41],
				area42_flg             => $area_flg[42],
				area43_flg             => $area_flg[43],
				area44_flg             => $area_flg[44],
				area45_flg             => $area_flg[45],
				area46_flg             => $area_flg[46],
				area47_flg             => $area_flg[47],
				address                => MODULE::StringUtil::conversionSpecialChar($FORM{'address'}),
				mail_flg               => $mail_flg,
				mail                   => MODULE::StringUtil::conversionSpecialChar($FORM{'mail'}),
				mail_check             => MODULE::StringUtil::conversionSpecialChar($FORM{'mail_check'}),
				pay_flg                => $pay_flg,
				PAY_LOOP               => \@PAY_LOOP,
				credit_flg             => $credit_flg,
				daikou_flg             => $daikou_flg,
				visa_flg               => $visa_flg,
				master_flg             => $master_flg,
				jcb_flg                => $jcb_flg,
				amex_flg               => $amex_flg,
				diners_flg             => $diners_flg,
				cerdit_description_flg => $cerdit_description_flg,
				cerdit_description     => $cerdit_description,
				pnum_flg               => $pnum_flg,
				pnum_1                 => MODULE::StringUtil::conversionSpecialChar($FORM{'pnum_1'}),
				pnum_2                 => MODULE::StringUtil::conversionSpecialChar($FORM{'pnum_2'}),
				pnum_3                 => MODULE::StringUtil::conversionSpecialChar($FORM{'pnum_3'}),
				fnum_flg               => $fnum_flg,
				fnum_1                 => MODULE::StringUtil::conversionSpecialChar($FORM{'fnum_1'}),
				fnum_2                 => MODULE::StringUtil::conversionSpecialChar($FORM{'fnum_2'}),
				fnum_3                 => MODULE::StringUtil::conversionSpecialChar($FORM{'fnum_3'}),
				day_pnum_flg           => $day_pnum_flg,
				day_pnum_1             => MODULE::StringUtil::conversionSpecialChar($FORM{'day_pnum_1'}),
				day_pnum_2             => MODULE::StringUtil::conversionSpecialChar($FORM{'day_pnum_2'}),
				day_pnum_3             => MODULE::StringUtil::conversionSpecialChar($FORM{'day_pnum_3'}),
				birth_flg              => $birth_flg,
				birthyear              => MODULE::StringUtil::conversionSpecialChar($FORM{'birthyear'}),
				birthmonth             => MODULE::StringUtil::conversionSpecialChar($FORM{'birthmonth'}),
				birthday               => MODULE::StringUtil::conversionSpecialChar($FORM{'birthday'}),
				seibetu_flg            => $seibetu_flg,
				sei_fm_m_flg           => $sei_fm_m_flg,
				sei_fm_f_flg           => $sei_fm_f_flg,
				addItem_flg            => $addItem_flg,
				order_item_name        => MODULE::StringUtil::conversionSpecialChar($order_item_name),
				order_item_explan      => $order_item_explan,
				pulldown_flg           => $pulldown_flg,
				pd_name                => MODULE::StringUtil::conversionSpecialChar($pd_name),
				PULLDOWN_LOOP          => \@PULLDOWN_LOOP,
				checkbox_flg           => $checkbox_flg,
				CHECKBOX_LOOP          => \@CHECKBOX_LOOP,
				radio_flg              => $radio_flg,
				RADIO_LOOP             => \@RADIO_LOOP,
				text_flg               => $text_flg,
				text_id                => MODULE::StringUtil::conversionSpecialChar($text_id),
				text_item              => MODULE::StringUtil::conversionSpecialChar($text_item),
			};
			push(@CART_LOOP, $hash);
		}
	}
	#_決済不可の場合カート情報へエラー出力
	if ($pay_counter == 0) {
		$agent_error_flg++;
		$cart_form_error++;
	}
	
	#_カート情報エラー
	if ($cart_form_error) {
		#$bpage_url =~ m/^(.+cgi)/i;
		#$bpage_url = $1 . '?';
		#$bpage_url .= $bpage_url_sub;
		
		$cart_count_error++;
		
		#my $template = HTML::Template->new(filename => sprintf('%s/order_cart_info.tmp', $_CONFIG_server_ssl_www_root));
		my $template = HTML::Template->new(filename => sprintf('%s/order_cart_info.tmp', "./$_CONFIG_template_dir/"));
		
		################################
		our @LOOP_hash = ();
		our $subtotal_amount;
		our @deliveryCheck;
		
		#_カートを展開
		@LOOP_hash = ();
		&cartLoopView1(1);
		$template->param(PURCHASE_LOOP => \@LOOP_hash);
		
		our $discount_flg;
		our $cash_discount = 0;
		
		#_割引設定
		@LOOP_hash = ();
		&cartLoopCashDiscount;
		$template->param(
			DISCOUNT_LOOP => \@LOOP_hash,
			cash_discount => &convertMoney($cash_discount),
			discount_flg  => $discount_flg,
		);
		
		@LOOP_hash = ();
		&cartLoopDelivery(1);
		$template->param(
			DELIVERY_LOOP => \@LOOP_hash,
			delivery_flg  => $_CONFIG_carriage_carriage_disp,
		);
		
		#_戻り先URL生成
		my ($bpage_flg, $bpage_u_flg, $bpage_s_flg, $bpage_g_flg, $bpage_c_flg, $send_keyword)
		 = &cartLoopBpage($FORM{'saleItem_id'}, $FORM{'pid'}, $FORM{'ukeyword'}, $FORM{'skeyword'}, $FORM{'gkeyword'}, $FORM{'ckeyword'});
		
		my $order_form_url = './order_form.cgi';
		
		#_合計金額
		my $total_amount = $subtotal_amount - $cash_discount;
		$template->param(
			order_form_url      => $order_form_url,
			tax_string          => $_CONFIG_tax_marking,
			subtotal_amount     => &convertMoney(int $subtotal_amount),
			total_amount        => &convertMoney(int $total_amount),
			msg_flg             => $_CONFIG_order_info_view,
			msg                 => $_CONFIG_order_info_comment,
			ship_free_flg       => $_CONFIG_carriage_free_shipping_set,
			ship_free_if        => &convertMoney($_CONFIG_carriage_free_shipping_set),
			
			error_on_flg        => 1,
			max_error_flg       => $max_error_flg,
			max_quantity        => $error_max_quantity,
			order_quantity      => $error_order_quantity,
			stock_error_flg     => $error_stock_error_flg,
			hinmei              => $error_hinmei,
			variation_code      => $error_variation_code,
			yoko_title          => $error_yoko_title,
			tate_title          => $error_tate_title,
			yoko_name           => $error_yoko_name,
			tate_name           => $error_tate_name,
			stock_quantity      => $error_stock_quantity,
			incorrect_error_flg => $incorrect_error_flg,
			agent_error_flg     => $agent_error_flg,
			
			cart_url            => sprintf('%s/cgi-bin/order_cart_info.cgi', $_CONFIG_server_ssl_www_root),
			bpage_para          => $bpage_para,
			bpage_flg           => $bpage_flg,
			bpage_url           => $bpage_url,
			back_page_url       => $bpage_url,
			bpage               => $bpage_url,
			saleItem_id         => $FORM{'saleItem_id'} . $variation,
			pid                 => $FORM{'pid'},
			stype               => $FORM{'stype'},
			vtype               => $FORM{'vtype'},
			ukeyword            => MODULE::StringUtil::conversionSpecialChar($FORM{'ukeyword'}),
			skeyword            => MODULE::StringUtil::conversionSpecialChar($FORM{'skeyword'}),
			gkeyword            => MODULE::StringUtil::conversionSpecialChar($FORM{'gkeyword'}),
			ckeyword            => MODULE::StringUtil::conversionSpecialChar($FORM{'ckeyword'}),
			vnum                => $FORM{'vnum'},
		);
		##########################
		print $_CONFIG_base_head;
		print $template -> output;
		#printf ('Location:%sorder_cart_info.cgi?error_on_flg=1&%s%s%s', $new_pass, $buffer, "\n", "\n");

		$session->flush();

		&chmodSessionFile ($session_pass, $_CONFIG_session_file_header, $session_id);

		exit;
	}
	
	
	my ($bpage_u_flg, $bpage_s_flg, $bpage_g_flg, $bpage_c_flg, $send_keyword);
	my $bpage_flg  = 1 unless ($FORM{'pid'});
	if ($FORM{'ukeyword'}) {
		$bpage_u_flg = 1;
		$send_keyword = sprintf('&ukeyword=%s', $FORM{'ukeyword'});
	}
	if ($FORM{'skeyword'}) {
		$bpage_s_flg = 1;
		$send_keyword = sprintf('&skeyword=%s', $FORM{'skeyword'});
	}
	if ($FORM{'gkeyword'}) {
		$bpage_g_flg = 1;
		$send_keyword = sprintf('&gkeyword=%s', $FORM{'gkeyword'});
	}
	if ($FORM{'ckeyword'}) {
		$bpage_c_flg = 1;
		$send_keyword = sprintf('&ckeyword=%s', $FORM{'ckeyword'});
	}
	
	my $cart_info_url;
	if ($bpage_flg) {
		$cart_info_url = sprintf('%s/order_cart_info.cgi?bpage=%s&saleItem_id=%s', $http_path, $FORM{'bpage'}, $FORM{'saleItem_id'});
	} else {
		$cart_info_url = sprintf('%s/order_cart_info.cgi?bpage=%s&pid=%s&stype=%s&vtype=%s&vnum=%s%s',
		$http_path, $FORM{'bpage'}, $FORM{'pid'}, $FORM{'stype'}, $FORM{'vtype'}, $FORM{'vnum'}, $send_keyword);
	}
	$template->param(
		subtotal_amount      => &convertMoney($subtotal_amount),
		tax_string           => $_CONFIG_tax_marking,
		bpage_url            => $bpage_url,
		discount_flg         => $discount_flg,
		cash_discount        => &convertMoney($cash_discount),
		total_amount         => &convertMoney($total_amount),
		delivery_flg         => $_CONFIG_carriage_carriage_disp,
		ship_free_flg        => $_CONFIG_carriage_free_shipping_set,
		ship_free_if         => &convertMoney($_CONFIG_carriage_free_shipping_set),
		sp_ship_flg          => $_CONFIG_order_other_view,
		sp_ship_comment      => $_CONFIG_order_other_comment,
		sp_flg               => $FORM{'sp_ship'},
		dhope_flg            => $_CONFIG_order_request_view,
		dhope_commnet        => $_CONFIG_order_request_comment,
		dhope                => MODULE::StringUtil::conversionSpecialChar(&strBrDouble($FORM{'dhope'})),
		mailguide_flg        => $_CONFIG_order_announce_view,
		mailguide_comment    => $_CONFIG_order_announce_comment,
		mailok_flg           => $FORM{'mailguide'},
		idea                 => MODULE::StringUtil::conversionSpecialChar(&strBrDouble($FORM{'idea'})),
		CART_LOOP            => \@CART_LOOP,
		cart_info_url        => $cart_info_url,
		error_on_flg         => $FORM{'error_on_flg'},
		MUST_ERROR_LOOP      => \@MUST_ERROR_LOOP,
		INCORRECT_ERROR_LOOP => \@INCORRECT_ERROR_LOOP,
		sp_ship_flg          => $delivery_counter,
		email_error_flg      => $email_error_flg,
		
		saleItem_id          => $FORM{'saleItem_id'},
		bpage_flg            => $bpage_flg,
		bpage                => $FORM{'bpage'},
		pid                  => $FORM{'pid'},
		stype                => $FORM{'stype'},
		vtype                => $FORM{'vtype'},
		vnum                 => $FORM{'vnum'},
		bpage_u_flg          => $bpage_u_flg,
		ukeyword             => MODULE::StringUtil::conversionSpecialChar($FORM{'ukeyword'}),
		bpage_s_flg          => $bpage_s_flg,
		skeyword             => MODULE::StringUtil::conversionSpecialChar($FORM{'skeyword'}),
		bpage_g_flg          => $bpage_g_flg,
		gkeyword             => MODULE::StringUtil::conversionSpecialChar($FORM{'gkeyword'}),
		bpage_c_flg          => $bpage_c_flg,
		ckeyword             => MODULE::StringUtil::conversionSpecialChar($FORM{'ckeyword'}),
		agent_error_flg      => $agent_error_flg,
		must_flg             => $must_flg,
	);
	
	&httpHeadOutput($setcook1 . "\n");
	print $template -> output;


	$session->flush();

	&chmodSessionFile ($session_pass . "/", $_CONFIG_session_file_header, $session_id);


exit;

