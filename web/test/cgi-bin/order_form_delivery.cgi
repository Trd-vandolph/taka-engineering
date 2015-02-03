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
	our %FORM;
	our $delivery_counter;
	our $pay_counter   = 0;


	our $session_pass = "$_CONFIG_server_ssl_www_root/cgi-bin/$_CONFIG_session_dir";


	
	&formLoading;
	
	our $http_path;
	if ($_CONFIG_server_ssl_use ne '0' && $_CONFIG_page_view_mode ne 'P') {
		$http_path = sprintf('%s/cgi-bin', $_CONFIG_server_url);
	} else {
		$http_path = '../cgi-bin';
		$_CONFIG_server_ssl_www_root = '..';
	}
	
	our $template = HTML::Template->new(filename => "./$_CONFIG_template_dir/order_form_delivery.tmp");
	
	our $session_name  = 'sessionCart';
	our $session_timer = 30;
	
	&getCookie($session_name);
	&cleanSession;
	our $session      = CGI::Session->new(undef, $COOKIE{$session_name}, {Directory=>$session_pass});
	our $session_cart = $session->param($session_name);

#メールデータセッション化->Start
	#_注文フォームグリッド
	my $form_file = "$_CONFIG_server_ssl_www_root/cgi-bin/search/item_order_form.cgi";
	open(DATA, $form_file);
	our @form_file = <DATA>;
	close(DATA);
	@form_file = sort { (split(/\t/,$a))[6] <=> (split(/\t/,$b))[6] } @form_file;
	if ($ENV{'HTTP_REFERER'} =~ /order_form.cgi/ || $ENV{'HTTP_REFERER'} =~ /order_form_delivery.cgi/) {
		#注文者のフォームデータをセッションに格納します。
		$session->param('lname', $FORM{'lname'});				#氏名（姓）
		$session->param('fname', $FORM{'fname'});				#氏名（名）
		$session->param('lname_kana', $FORM{'lname_kana'});		#氏名（姓）カナ
		$session->param('fname_kana', $FORM{'fname_kana'});		#氏名（名）カナ
		$session->param('cname', $FORM{'cname'});				#法人名
		$session->param('cname_kana', $FORM{'cname_kana'});		#法人名カナ
		$session->param('department', $FORM{'department'});		#所属部署/役職名
		$session->param('pcode_first', $FORM{'pcode_first'});	#郵便番号上3桁
		$session->param('pcode_last', $FORM{'pcode_last'});		#郵便番号下4桁
		$session->param('address', $FORM{'address'});			#住所
		$session->param('mail', $FORM{'mail'});					#メールアドレス
		$session->param('mail_check', $FORM{'mail_check'});		#メールアドレス確認
		$session->param('pnum_1', $FORM{'pnum_1'});				#電話番号（市外）
		$session->param('pnum_2', $FORM{'pnum_2'});				#電話番号（市内）
		$session->param('pnum_3', $FORM{'pnum_3'});				#電話番号（番号）
		$session->param('fnum_1', $FORM{'fnum_1'});				#FAX番号（市外）
		$session->param('fnum_2', $FORM{'fnum_2'});				#FAX番号（市内）
		$session->param('fnum_3', $FORM{'fnum_3'});				#FAX番号（番号）
		$session->param('day_pnum_1', $FORM{'day_pnum_1'});		#日中の連絡先（市外）
		$session->param('day_pnum_2', $FORM{'day_pnum_2'});		#日中の連絡先（市内）
		$session->param('day_pnum_3', $FORM{'day_pnum_3'});		#日中の連絡先（番号）
		$session->param('birthyear', $FORM{'birthyear'});		#生年月日（年）
		$session->param('birthmonth', $FORM{'birthmonth'});		#生年月日（月）
		$session->param('birthday', $FORM{'birthday'});			#生年月日（日）
			
		$session->param('dhope', $FORM{'dhope'});			#配送等へのご希望
		$session->param('idea', $FORM{'idea'});			#連絡事項

		foreach (@form_file) {
			my @form_line = split(/\t/, $_);
			if ($form_line[9] eq 'A') {
				$session->param("order_$form_line[0]", $FORM{"order_$form_line[0]"});
			}
		}
	}
	
	#セッションデータを読み込みます。
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

	foreach (@form_file) {
		my @form_line = split(/\t/, $_);
		if ($form_line[9] eq 'A') {
			$FORM{"order_$form_line[0]"} = $session->param("order_$form_line[0]");
			$FORM{"sp_order_$form_line[0]"} = $session->param("sp_order_$form_line[0]");
		}
	}

#メールデータセッション化->End


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
	
	our $bpage_url  = $FORM{'bpage'} . '?';
	my $bpage_url_sub;
	if ($bpage_url =~ /saleItem_detailInfo/) {
		$bpage_url_sub .= sprintf('&cc=%02d', $cc);
		$bpage_url_sub .= sprintf('&gc=%02d', $gc);
		$bpage_url_sub .= sprintf('&ic=%08d', $ic);
	}
	$bpage_url_sub .= sprintf('&pid=%s', $FORM{'pid'}) if ($FORM{'pid'} ne '');
	$bpage_url_sub .= sprintf('&stype=%s', $FORM{'stype'}) if ($FORM{'stype'} ne '');
	$bpage_url_sub .= sprintf('&vtype=%s', $FORM{'vtype'}) if ($FORM{'vtype'} ne '');
	$bpage_url_sub .= sprintf('&ukeyword=%s', $FORM{'ukeyword'}) if ($FORM{'ukeyword'} ne '');
	$bpage_url_sub .= sprintf('&vnum=%s', $FORM{'vnum'}) if ($FORM{'vnum'} ne '');
	
	$bpage_url .= $bpage_url_sub;
	$bpage_para .= sprintf('&bpage=%s', $bpage);
	$bpage_para .= $bpage_url_sub;
	
	$session->expire('+'.$session_timer.'m');
	$session_cart = $session->param($session_name);
	$session_id   = $session->id;
	
	$setcook1 = &setCookie($session_name, $session_id);
	my $cnt = 0;
	our @PURCHASE_LOOP_hash = ();
	our $subtotal_amount;
	
	
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
		
		my $unit_price			= 0;
#		my $pretax_flg			= 0;
		my $pretax_price		= 0;
		my $unit_price_tax_on	= 0;
		my $pretax_flg			= $_CONFIG_tax_indication;
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
		push(@PURCHASE_LOOP_hash, $hash);
		$deliveryCheck[$item_deli_type_id]++;
	}
	
	$template->param(PURCHASE_LOOP => \@PURCHASE_LOOP_hash);
	
	our @DISCOUNT_LOOP_hash = ();
	our $cash_discount = 0;
	my $cash_discount_par = 0;
	
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
			push(@DISCOUNT_LOOP_hash, $hash);
		}
	}
	
	our $discount_flg = 0;
	if (@DISCOUNT_LOOP_hash > 0) {
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
	
	$template->param(DISCOUNT_LOOP => \@DISCOUNT_LOOP_hash);
	our $total_amount = $subtotal_amount - $cash_discount;
	
	
	my $data_file = "$_CONFIG_server_ssl_www_root/cgi-bin/item_delivery.cgi";
	open(DATA, $data_file);
	my @data_file = <DATA>;
	close(DATA);
	chomp @data_file;
	
	our @DELIVERY_LOOP_hash = ();
	our $delivery_flg = 0;

	my $delivery_type_flg = 0;
	my $delivery_uniform  = 0;

	foreach (@data_file) {
		my @data_line = split(/\t/, $_);
		
		#_配送タイプ表示チェック
		next if $deliveryCheck[$data_line[0]] < 1;
		
		if ($data_line[2] eq 'U') {
			$delivery_type_flg = 1;
		} else {
			$delivery_type_flg = 0;
		}

		$delivery_uniform  = &convertMoney($data_line[3]);

		my $delivery_comment_flg = 0;
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
		push(@DELIVERY_LOOP_hash, $hash);
	}
	$template->param(DELIVERY_LOOP => \@DELIVERY_LOOP_hash);
	
	
	
#	#_注文フォームグリッド
#	my $form_file = "$_CONFIG_server_ssl_www_root/cgi-bin/search/item_order_form.cgi";
#	open(DATA, $form_file);
#	our @form_file = <DATA>;
#	close(DATA);
	
	@form_file = sort { (split(/\t/,$a))[6] <=> (split(/\t/,$b))[6] } @form_file;
	
	my @CART_LOOP = ();
	my @SP_MUST_ERROR_LOOP = ();
	my @SP_INCORRECT_ERROR_LOOP = ();
	
	our $addItem_flg	= 0;
	our $error_on_flg	= 0;
	
	#_前後の空白を削除
	$FORM{'lname'}       = &strTrim($FORM{'lname'});
	$FORM{'fname'}       = &strTrim($FORM{'fname'});
	$FORM{'lname_kana'}  = &strTrim($FORM{'lname_kana'});
	$FORM{'fname_kana'}  = &strTrim($FORM{'fname_kana'});
	$FORM{'cname'}       = &strTrim($FORM{'cname'});
	$FORM{'cname_kana'}  = &strTrim($FORM{'cname_kana'});
	$FORM{'department'}  = &strTrim($FORM{'department'});
	$FORM{'pcode_first'} = &strTrim($FORM{'pcode_first'});
	$FORM{'pcode_last'}  = &strTrim($FORM{'pcode_last'});
	$FORM{'address'}     = &strTrim($FORM{'address'});
	$FORM{'mail'}        = &strTrim($FORM{'mail'});
	$FORM{'mail_check'}  = &strTrim($FORM{'mail_check'});
	$FORM{'pnum_1'}      = &strTrim($FORM{'pnum_1'});
	$FORM{'pnum_2'}      = &strTrim($FORM{'pnum_2'});
	$FORM{'pnum_3'}      = &strTrim($FORM{'pnum_3'});
	$FORM{'fnum_1'}      = &strTrim($FORM{'fnum_1'});
	$FORM{'fnum_2'}      = &strTrim($FORM{'fnum_2'});
	$FORM{'fnum_3'}      = &strTrim($FORM{'fnum_3'});
	$FORM{'day_pnum_1'}  = &strTrim($FORM{'day_pnum_1'});
	$FORM{'day_pnum_2'}  = &strTrim($FORM{'day_pnum_2'});
	$FORM{'day_pnum_3'}  = &strTrim($FORM{'day_pnum_3'});
	$FORM{'birthyear'}   = &strTrim($FORM{'birthyear'});
	$FORM{'birthmonth'}  = &strTrim($FORM{'birthmonth'});
	$FORM{'birthday'}    = &strTrim($FORM{'birthday'});
	
	our @MUST_ERROR_LOOP = ();
	our @INCORRECT_ERROR_LOOP = ();
	our $email_error_flg = 0;
	
	FORM:foreach (@form_file) {
		my @form_line = split(/\t/, $_);
		my @PAY_LOOP      = ();
		my @PULLDOWN_LOOP = ();
		my @CHECKBOX_LOOP = ();
		my @RADIO_LOOP    = ();
		
		if ($form_line[2] != 0) {
			my $error_check_flg_must = 0;
			$addItem_flg++;
			my $credit_flg				= 0;
			my $daikou_flg				= 0;
			my $visa_flg				= 0;
			my $master_flg				= 0;
			my $jcb_flg					= 0;
			my $amex_flg				= 0;
			my $diners_flg				= 0;
			my $cerdit_description_flg	= 0;
			
			my $form_input_flg = 0;
			if ($form_line[0] >= 12) {
				
				my $pulldown_flg		= 0;
				my $pd_name				= '';
				my $checkbox_flg		= 0;
				my $radio_flg			= 0;
				my $order_item_name		= '';
				my $order_item_explan	= '';
				my $text_id				= '';
				my $text_item			= '';
				my $text_flg			= '';
				
				$order_item_name   = $form_line[1];
				$order_item_explan = $form_line[8];
				$pd_name           = 'order_' . $form_line[0];
				my $hit_check = 0;
				if ($form_line[9] eq 'S') {
					$pulldown_flg = 1;
					my @option_list = split(/<RETURN>/, $form_line[10]);
					chomp @option_list;
					my $i = 1;
					foreach (@option_list) {
						if ($FORM{"order_$form_line[0]"} ne '') {
							$pd_id     = 'order_' . $form_line[0];
							$pd_option = $FORM{"order_$form_line[0]"};
							$hit_check++;
						}
						$i++;
					}
				} elsif ($form_line[9] eq 'C') {
					$checkbox_flg = 1;
					my @option_list = split(/<RETURN>/, $form_line[10]);
					chomp @option_list;
					my $i = 1;
					foreach (@option_list) {
						if ($FORM{"order_$form_line[0]_$i"} ne '') {
							$hit_check++;
							$hash = {
								pulldown_flg           => $pulldown_flg,
								pd_id                  => $pd_id,
								pd_option              => $pd_option,
								checkbox_flg           => $checkbox_flg,
								c_id                   => 'order_' . $form_line[0] . '_' . $i,
								c_option               => $FORM{"order_$form_line[0]_$i"},
								radio_flg              => $radio_flg,
								r_id                   => $r_id,
								r_option               => $r_option,
								text_flg               => $text_flg,
								text_id                => $text_id,
								text_item              => MODULE::StringUtil::conversionSpecialChar($text_item),
							};
							push(@CART_LOOP, $hash);
						}
						$i++;
					}
					next;
				} elsif ($form_line[9] eq 'R') {
					$radio_flg = 1;
					my @option_list = split(/<RETURN>/, $form_line[10]);
					chomp @option_list;
					my $i = 1;
					foreach (@option_list) {
						if ($i == $FORM{"order_$form_line[0]"}) {
							$r_id = 'order_' . $form_line[0];
							$r_option = $i;
							$hit_check++;
							last;
						}
						$i++;
					}
				} elsif ($form_line[9] eq 'A') {
					$text_id   = 'order_' . $form_line[0];
					$text_item = &strTrim($FORM{"order_$form_line[0]"});
					$text_flg  = 1;
				}
				
				$hash = {
					pulldown_flg           => $pulldown_flg,
					pd_id                  => $pd_id,
					pd_option              => $pd_option,
					checkbox_flg           => $checkbox_flg,
					c_id                   => $c_id,
					c_option               => $c_option,
					radio_flg              => $radio_flg,
					r_id                   => $r_id,
					r_option               => $r_option,
					text_flg               => $text_flg,
					text_id                => $text_id,
					text_item              => MODULE::StringUtil::conversionSpecialChar($text_item),
				};
				push(@CART_LOOP, $hash);
			}
		}
	}
	
	&checkErrorOrder;
	
	if ($error_on_flg) {
		&outputErrorOrder();
		&httpHeadOutput($setcook1 . "\n");
		print $template -> output;


		$session->flush();

		&chmodSessionFile ($session_pass, $_CONFIG_session_file_header, $session_id);

		exit;
	}
	
	if ($FORM{'error_on_flg'}) {
		#_前後の空白を削除
		$FORM{'sp_lname'}       = &strTrim($FORM{'sp_lname'});
		$FORM{'sp_fname'}       = &strTrim($FORM{'sp_fname'});
		$FORM{'sp_lname_kana'}  = &strTrim($FORM{'sp_lname_kana'});
		$FORM{'sp_fname_kana'}  = &strTrim($FORM{'sp_fname_kana'});
		$FORM{'sp_cname'}       = &strTrim($FORM{'sp_cname'});
		$FORM{'sp_cname_kana'}  = &strTrim($FORM{'sp_cname_kana'});
		$FORM{'sp_department'}  = &strTrim($FORM{'sp_department'});
		$FORM{'sp_pcode_first'} = &strTrim($FORM{'sp_pcode_first'});
		$FORM{'sp_pcode_last'}  = &strTrim($FORM{'sp_pcode_last'});
		$FORM{'sp_address'}     = &strTrim($FORM{'sp_address'});
		$FORM{'sp_mail'}        = &strTrim($FORM{'sp_mail'});
		$FORM{'sp_mail_check'}  = &strTrim($FORM{'sp_mail_check'});
		$FORM{'sp_pnum_1'}      = &strTrim($FORM{'sp_pnum_1'});
		$FORM{'sp_pnum_2'}      = &strTrim($FORM{'sp_pnum_2'});
		$FORM{'sp_pnum_3'}      = &strTrim($FORM{'sp_pnum_3'});
		$FORM{'sp_fnum_1'}      = &strTrim($FORM{'sp_fnum_1'});
		$FORM{'sp_fnum_2'}      = &strTrim($FORM{'sp_fnum_2'});
		$FORM{'sp_fnum_3'}      = &strTrim($FORM{'sp_fnum_3'});
		$FORM{'sp_day_pnum_1'}  = &strTrim($FORM{'sp_day_pnum_1'});
		$FORM{'sp_day_pnum_2'}  = &strTrim($FORM{'sp_day_pnum_2'});
		$FORM{'sp_day_pnum_3'}  = &strTrim($FORM{'sp_day_pnum_3'});
		$FORM{'sp_birthyear'}   = &strTrim($FORM{'sp_birthyear'});
		$FORM{'sp_birthmonth'}  = &strTrim($FORM{'sp_birthmonth'});
		$FORM{'sp_birthday'}    = &strTrim($FORM{'sp_birthday'});
	}
	
	my @SP_MUST_ERROR_LOOP = ();
	my @SP_INCORRECT_ERROR_LOOP = ();
	my $email_error_flg = 0;
	
	my $sp_must_flg = 0;
	
	foreach (@form_file) {
		my @form_line = split(/\t/, $_);
		my @PAY_LOOP      = ();
		my @PULLDOWN_LOOP = ();
		my @CHECKBOX_LOOP = ();
		my @RADIO_LOOP    = ();
		
		if ($form_line[4] != 0) {
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

			if ($form_line[5]) {
				$order_must_flg = 1 ;
				$sp_must_flg = 1;
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

			my $pulldown_flg		= 0;
			my $pd_name				= '';
			my $checkbox_flg		= '';
			my $radio_flg			= '';
			my $order_item_name		= '';
			my $order_item_explan	= '';
			my $text_id				= '';
			my $text_item			= '';
			my $text_flg			= '';
			
			my $error_check_flg_must = 0;
			
			if ($addItem_flg) {
				$order_item_name   = $form_line[1];
				$order_item_explan = $form_line[8];
				$pd_name           = 'sp_order_' . $form_line[0];
				if ($form_line[9] eq 'S') {
					$pulldown_flg = 1;
					my @option_list = split(/<RETURN>/, $form_line[10]);
					chomp @option_list;
					my $i = 1;
					foreach (@option_list) {
						my $pd_id = $i;
						my $pd_s_flg = 0;
						$pd_s_flg = 1 if ($i == $FORM{"sp_order_$form_line[0]"});
						my $sub_hash = {
							sp_pd_id     => $pd_id,
							sp_pd_s_flg  => $pd_s_flg,
							sp_pd_option => $_,
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
						my $c_id = 'sp_order_' . $form_line[0] . '_' . $i;
						my $sub_hash = {
							sp_c_name   => $c_id,
							sp_c_id     => $c_id,
							sp_c_s_flg  => $FORM{"sp_order_$form_line[0]_$i"},
							sp_c_option => $_,
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
						$r_s_flg = 1 if ($i == $FORM{"sp_order_$form_line[0]"});
						my $r_id = 'sp_order_' . $form_line[0];
						my $sub_hash = {
							sp_r_name   => $r_id,
							sp_r_id     => $i,
							sp_r_s_flg  => $r_s_flg,
							sp_r_option => $_,
						};
						push(@RADIO_LOOP, $sub_hash);
						$i++;
					}
				} elsif ($form_line[9] eq 'A') {
					$text_id   = 'sp_order_' . $form_line[0];
					$text_item = &strTrim($FORM{"sp_order_$form_line[0]"});
					$text_flg  = 1;
				}
			}
			my @area_flg;
			$area_flg[$FORM{'sp_todouhuken'}] = 1;
			my $sp_sei_m_flg = '';
			my $sp_sei_f_flg = '';
			if ( $FORM{'sp_sei_fm_flg'} eq 'm' ) {
				$sp_sei_m_flg = 1;
				$sp_sei_f_flg = 0;
			} elsif ( $FORM{'sp_sei_fm_flg'} eq 'f' ) {
				$sp_sei_m_flg = 0;
				$sp_sei_f_flg = 1;
			} else {
				$sp_sei_m_flg = 0;
				$sp_sei_f_flg = 0;
			}

			$hash = {
				sp_order_must_flg    => $order_must_flg,
				sp_name_flg          => $name_flg,
				sp_lname             => MODULE::StringUtil::conversionSpecialChar($FORM{'sp_lname'}),
				sp_fname             => MODULE::StringUtil::conversionSpecialChar($FORM{'sp_fname'}),
				sp_lname_kana        => MODULE::StringUtil::conversionSpecialChar($FORM{'sp_lname_kana'}),
				sp_fname_kana        => MODULE::StringUtil::conversionSpecialChar($FORM{'sp_fname_kana'}),
				sp_cname_flg         => $cname_flg,
				sp_cname             => MODULE::StringUtil::conversionSpecialChar($FORM{'sp_cname'}),
				sp_cname_kana        => MODULE::StringUtil::conversionSpecialChar($FORM{'sp_cname_kana'}),
				sp_department_flg    => $department_flg,
				sp_department        => MODULE::StringUtil::conversionSpecialChar($FORM{'sp_department'}),
				sp_address_flg       => $address_flg,
				sp_pcode_first       => MODULE::StringUtil::conversionSpecialChar($FORM{'sp_pcode_first'}),
				sp_pcode_last        => MODULE::StringUtil::conversionSpecialChar($FORM{'sp_pcode_last'}),
				area1_flg            => $area_flg[1],
				area2_flg            => $area_flg[2],
				area3_flg            => $area_flg[3],
				area4_flg            => $area_flg[4],
				area5_flg            => $area_flg[5],
				area6_flg            => $area_flg[6],
				area7_flg            => $area_flg[7],
				area8_flg            => $area_flg[8],
				area9_flg            => $area_flg[9],
				area10_flg           => $area_flg[10],
				area11_flg           => $area_flg[11],
				area12_flg           => $area_flg[12],
				area13_flg           => $area_flg[13],
				area14_flg           => $area_flg[14],
				area15_flg           => $area_flg[15],
				area16_flg           => $area_flg[16],
				area17_flg           => $area_flg[17],
				area18_flg           => $area_flg[18],
				area19_flg           => $area_flg[19],
				area20_flg           => $area_flg[20],
				area21_flg           => $area_flg[21],
				area22_flg           => $area_flg[22],
				area23_flg           => $area_flg[23],
				area24_flg           => $area_flg[24],
				area25_flg           => $area_flg[25],
				area26_flg           => $area_flg[26],
				area27_flg           => $area_flg[27],
				area28_flg           => $area_flg[28],
				area29_flg           => $area_flg[29],
				area30_flg           => $area_flg[30],
				area31_flg           => $area_flg[31],
				area32_flg           => $area_flg[32],
				area33_flg           => $area_flg[33],
				area34_flg           => $area_flg[34],
				area35_flg           => $area_flg[35],
				area36_flg           => $area_flg[36],
				area37_flg           => $area_flg[37],
				area38_flg           => $area_flg[38],
				area39_flg           => $area_flg[39],
				area40_flg           => $area_flg[40],
				area41_flg           => $area_flg[41],
				area42_flg           => $area_flg[42],
				area43_flg           => $area_flg[43],
				area44_flg           => $area_flg[44],
				area45_flg           => $area_flg[45],
				area46_flg           => $area_flg[46],
				area47_flg           => $area_flg[47],
				sp_address           => MODULE::StringUtil::conversionSpecialChar($FORM{'sp_address'}),
				sp_mail_flg          => $mail_flg,
				sp_mail              => MODULE::StringUtil::conversionSpecialChar($FORM{'sp_mail'}),
				sp_mail_check        => MODULE::StringUtil::conversionSpecialChar($FORM{'sp_mail_check'}),
				sp_pnum_flg          => $pnum_flg,
				sp_pnum_1            => MODULE::StringUtil::conversionSpecialChar($FORM{'sp_pnum_1'}),
				sp_pnum_2            => MODULE::StringUtil::conversionSpecialChar($FORM{'sp_pnum_2'}),
				sp_pnum_3            => MODULE::StringUtil::conversionSpecialChar($FORM{'sp_pnum_3'}),
				sp_fnum_flg          => $fnum_flg,
				sp_fnum_1            => MODULE::StringUtil::conversionSpecialChar($FORM{'sp_fnum_1'}),
				sp_fnum_2            => MODULE::StringUtil::conversionSpecialChar($FORM{'sp_fnum_2'}),
				sp_fnum_3            => MODULE::StringUtil::conversionSpecialChar($FORM{'sp_fnum_3'}),
				sp_day_pnum_flg      => $day_pnum_flg,
				sp_day_pnum_1        => MODULE::StringUtil::conversionSpecialChar($FORM{'sp_day_pnum_1'}),
				sp_day_pnum_2        => MODULE::StringUtil::conversionSpecialChar($FORM{'sp_day_pnum_2'}),
				sp_day_pnum_3        => MODULE::StringUtil::conversionSpecialChar($FORM{'sp_day_pnum_3'}),
				sp_birth_flg         => $birth_flg,
				sp_birthyear         => MODULE::StringUtil::conversionSpecialChar($FORM{'sp_birthyear'}),
				sp_birthmonth        => MODULE::StringUtil::conversionSpecialChar($FORM{'sp_birthmonth'}),
				sp_birthday          => MODULE::StringUtil::conversionSpecialChar($FORM{'sp_birthday'}),
				sp_seibetu_flg       => $seibetu_flg,
				sp_sei_m_flg         => $sp_sei_m_flg,
				sp_sei_f_flg         => $sp_sei_f_flg,
				sp_addItem_flg       => $addItem_flg,
				sp_order_item_name   => MODULE::StringUtil::conversionSpecialChar($order_item_name),
				sp_order_item_explan => $order_item_explan,
				sp_pulldown_flg      => $pulldown_flg,
				sp_pd_name           => MODULE::StringUtil::conversionSpecialChar($pd_name),
				sp_PULLDOWN_LOOP     => \@PULLDOWN_LOOP,
				sp_checkbox_flg      => $checkbox_flg,
				sp_CHECKBOX_LOOP     => \@CHECKBOX_LOOP,
				sp_radio_flg         => $radio_flg,
				sp_RADIO_LOOP        => \@RADIO_LOOP,
				sp_text_flg          => $text_flg,
				sp_text_id           => $text_id,
				sp_text_item         => &strBr(MODULE::StringUtil::conversionSpecialChar($text_item)),
			};
			push(@SP_CART_LOOP, $hash);
			
			if ($FORM{'error_on_flg'}) {
				if ($form_line[5] == 1) {
					if ($form_line[0] == 1) {
						if (($FORM{'sp_lname'} eq '') || ($FORM{'sp_lname'} eq '')) {
							$must_error_item_name = 'お名前';
							$form_input_flg = 1;
							my $error_hash = {
								must_error_sp_item_name => MODULE::StringUtil::conversionSpecialChar($must_error_item_name),
								sp_error_input_flg      => $form_input_flg,
							};
							push(@SP_MUST_ERROR_LOOP, $error_hash);
							$sp_error_on_flg = 1;
						}
						if (($FORM{'sp_fname_kana'} eq '') || ($FORM{'sp_lname_kana'} eq '')) {
							$must_error_item_name = 'お名前(フリガナ)';
							$form_input_flg = 1;
							my $error_hash = {
								must_error_sp_item_name => MODULE::StringUtil::conversionSpecialChar($must_error_item_name),
								sp_error_input_flg      => $form_input_flg,
							};
							push(@SP_MUST_ERROR_LOOP, $error_hash);
							$sp_error_on_flg = 1;
						}
					} elsif ($form_line[0] == 2) {
						if ($FORM{'sp_cname'} eq '') {
							$must_error_item_name = '法人名';
							$form_input_flg = 1;
							my $error_hash = {
								must_error_sp_item_name => MODULE::StringUtil::conversionSpecialChar($must_error_item_name),
								sp_error_input_flg      => $form_input_flg,
							};
							push(@SP_MUST_ERROR_LOOP, $error_hash);
							$sp_error_on_flg = 1;
						}
						if ($FORM{'sp_cname_kana'} eq '') {
							$must_error_item_name = '法人名(フリガナ)';
							$form_input_flg = 1;
							my $error_hash = {
								must_error_sp_item_name => MODULE::StringUtil::conversionSpecialChar($must_error_item_name),
								sp_error_input_flg      => $form_input_flg,
							};
							push(@SP_MUST_ERROR_LOOP, $error_hash);
							$sp_error_on_flg = 1;
						}
					} elsif ($form_line[0] == 3) {
						if ($FORM{'sp_department'} eq '') {
							$must_error_item_name = '所属部署';
							$form_input_flg = 1;
							my $error_hash = {
								must_error_sp_item_name => MODULE::StringUtil::conversionSpecialChar($must_error_item_name),
								sp_error_input_flg      => $form_input_flg,
							};
							push(@SP_MUST_ERROR_LOOP, $error_hash);
							$sp_error_on_flg = 1;
						}
					} elsif ($form_line[0] == 4) {
						if (($FORM{'sp_pcode_first'} eq '') || ($FORM{'sp_pcode_last'} eq '') || ($FORM{'sp_address'} eq '')) {
							$must_error_item_name = 'ご住所';
							$form_input_flg = 1;
							my $error_hash = {
								must_error_sp_item_name => MODULE::StringUtil::conversionSpecialChar($must_error_item_name),
								sp_error_input_flg      => $form_input_flg,
							};
							push(@SP_MUST_ERROR_LOOP, $error_hash);
							$sp_error_on_flg = 1;
						}
						if ($FORM{'sp_todouhuken'} eq '') {
							$must_error_item_name = 'ご住所';
							$form_input_flg = 0;
							my $error_hash = {
								must_error_sp_item_name => MODULE::StringUtil::conversionSpecialChar($must_error_item_name),
								sp_error_input_flg      => $form_input_flg,
							};
							push(@SP_MUST_ERROR_LOOP, $error_hash);
							$sp_error_on_flg = 1;
						}
					} elsif ($form_line[0] == 5) {
						if ($FORM{'sp_mail'} eq '') {
							$must_error_item_name = 'メールアドレス';
							$form_input_flg = 1;
							my $error_hash = {
								must_error_sp_item_name => MODULE::StringUtil::conversionSpecialChar($must_error_item_name),
								sp_error_input_flg      => $form_input_flg,
							};
							push(@SP_MUST_ERROR_LOOP, $error_hash);
							$sp_error_on_flg = 1;
						}
						if ($FORM{'sp_mail_check'} eq '') {
							$must_error_item_name = 'メールアドレス(確認用)';
							$form_input_flg = 1;
							my $error_hash = {
								must_error_sp_item_name => MODULE::StringUtil::conversionSpecialChar($must_error_item_name),
								sp_error_input_flg      => $form_input_flg,
							};
							push(@SP_MUST_ERROR_LOOP, $error_hash);
							$sp_error_on_flg = 1;
						}
					} elsif ($form_line[0] == 7) {
						if (($FORM{'sp_pnum_1'} eq '') || ($FORM{'sp_pnum_2'} eq '') || ($FORM{'sp_pnum_3'} eq '')) {
							$must_error_item_name = '電話番号';
							$form_input_flg = 1;
							my $error_hash = {
								must_error_sp_item_name => MODULE::StringUtil::conversionSpecialChar($must_error_item_name),
								sp_error_input_flg      => $form_input_flg,
							};
							push(@SP_MUST_ERROR_LOOP, $error_hash);
							$sp_error_on_flg = 1;
						}
					} elsif ($form_line[0] == 8) {
						if (($FORM{'sp_fnum_1'} eq '') || ($FORM{'sp_fnum_2'} eq '') || ($FORM{'sp_fnum_3'} eq '')) {
							$must_error_item_name = 'FAX番号';
							$form_input_flg = 1;
							my $error_hash = {
								must_error_sp_item_name => MODULE::StringUtil::conversionSpecialChar($must_error_item_name),
								sp_error_input_flg      => $form_input_flg,
							};
							push(@SP_MUST_ERROR_LOOP, $error_hash);
							$sp_error_on_flg = 1;
						}
					} elsif ($form_line[0] == 9) {
						if (($FORM{'sp_day_pnum_1'} eq '') || ($FORM{'sp_day_pnum_2'} eq '') || ($FORM{'sp_day_pnum_3'} eq '')) {
							$must_error_item_name = '日中の連絡先';
							$form_input_flg = 1;
							my $error_hash = {
								must_error_sp_item_name => MODULE::StringUtil::conversionSpecialChar($must_error_item_name),
								sp_error_input_flg      => $form_input_flg,
							};
							push(@SP_MUST_ERROR_LOOP, $error_hash);
							$sp_error_on_flg = 1;
						}
					} elsif ($form_line[0] == 10) {
						if (($FORM{'sp_birthyear'} eq '') || ($FORM{'sp_birthmonth'} eq '') || ($FORM{'sp_birthday'} eq '')) {
							$must_error_item_name = '生年月日';
							$form_input_flg = 1;
							my $error_hash = {
								must_error_sp_item_name => MODULE::StringUtil::conversionSpecialChar($must_error_item_name),
								sp_error_input_flg      => $form_input_flg,
							};
							push(@SP_MUST_ERROR_LOOP, $error_hash);
							$sp_error_on_flg = 1;
						}
					} elsif ($form_line[0] == 11) {
						if ($FORM{'sp_sei_fm_flg'} eq '') {
							$must_error_item_name = '性別';
							$form_input_flg = 0;
							my $error_hash = {
								must_error_sp_item_name => MODULE::StringUtil::conversionSpecialChar($must_error_item_name),
								sp_error_input_flg      => $form_input_flg,
							};
							push(@SP_MUST_ERROR_LOOP, $error_hash);
							$sp_error_on_flg = 1;
						}
					} elsif ($form_line[8] eq 'R') {
						if ($FORM{"sp_order_$form_line[0]"} eq '') {
							$must_error_item_name = $form_line[1];
							$form_input_flg = 0;
							my $error_hash = {
								must_error_sp_item_name => MODULE::StringUtil::conversionSpecialChar($must_error_item_name),
								sp_error_input_flg      => $form_input_flg,
							};
							push(@SP_MUST_ERROR_LOOP, $error_hash);
							$sp_error_on_flg = 1;
						}
					} elsif ($form_line[8] eq 'A') {
						if ($FORM{"sp_order_$form_line[0]"} eq '') {
							$must_error_item_name = $form_line[1];
							$form_input_flg = 1;
							my $error_hash = {
								must_error_sp_item_name => MODULE::StringUtil::conversionSpecialChar($must_error_item_name),
								sp_error_input_flg      => $form_input_flg,
							};
							push(@SP_MUST_ERROR_LOOP, $error_hash);
							$sp_error_on_flg = 1;
						}
					} elsif ($form_line[8] eq 'S') {
						if ($FORM{"sp_order_$form_line[0]"} eq '') {
							$must_error_item_name = $form_line[1];
							$form_input_flg = 0;
							my $error_hash = {
								must_error_sp_item_name => MODULE::StringUtil::conversionSpecialChar($must_error_item_name),
								sp_error_input_flg      => $form_input_flg,
							};
							push(@SP_MUST_ERROR_LOOP, $error_hash);
							$sp_error_on_flg = 1;
						}
					} elsif ($form_line[8] eq 'C') {
						my @option_list = split(/<RETURN>/, $form_line[9]);
						chomp @option_list;
						my $i = 1;
						my $check_list_check = 0;
						foreach (@option_list) {
							my $c_id = 'sp_order_' . $form_line[0] . '_' . $i;
							if ($FORM{"$c_id"} ne '') {
								$check_list_check++;
								last;
							}
							$i++;
						}
						if ($check_list_check == 0) {
							$must_error_item_name = $form_line[1];
							$form_input_flg = 0;
							my $error_hash = {
								must_error_sp_item_name => MODULE::StringUtil::conversionSpecialChar($must_error_item_name),
								sp_error_input_flg      => $form_input_flg,
							};
							push(@SP_MUST_ERROR_LOOP, $error_hash);
							$sp_error_on_flg = 1;
						}
					}
				}
				if ($form_line[0] == 5) {
					if ($FORM{'sp_mail'} || $FORM{'sp_mail_check'}) {
						#_メールアドレスチェック
						my $mail_check_flg = 0;
						unless ($FORM{'sp_mail'} eq $FORM{'sp_mail_check'}) {
							$email_error_flg++;
						}
						unless (&mailChecker($FORM{'sp_mail'})) {
							$mail_check_flg++;
						}
						if ($mail_check_flg) {
							my $error_hash = {
								incorrect_error_sp_item_name => 'メールアドレス',
							};
							push(@SP_INCORRECT_ERROR_LOOP, $error_hash);
							$sp_error_on_flg = 1;
						}
					}
				}
				if ($form_line[0] == 4) {
					#_郵便番号チェック
					my $error_hash;
					if ($FORM{'sp_pcode_first'}) {
						unless (&strIntCheck($FORM{'sp_pcode_first'})) {
							$error_hash = {
								incorrect_error_sp_item_name => 'ご住所',
							};
						}
					}
					if ($FORM{'sp_pcode_last'}) {
						unless (&strIntCheck($FORM{'sp_pcode_last'})) {
							$error_hash = {
								incorrect_error_sp_item_name => 'ご住所',
							};
						}
					}
					if ($error_hash) {
						push(@SP_INCORRECT_ERROR_LOOP, $error_hash);
						$sp_error_on_flg = 1;
					}
				}
				if ($form_line[0] == 10) {
					#_日付チェック
					if (($FORM{'sp_birthyear'} ne '') || ($FORM{'sp_birthmonth'} ne '') || ($FORM{'sp_birthday'} ne '')) {
						unless (&strDateCheck($FORM{'sp_birthyear'}, $FORM{'sp_birthmonth'}, $FORM{'sp_birthday'})) {
							my $error_hash = {
								incorrect_error_sp_item_name => '生年月日',
							};
							push(@SP_INCORRECT_ERROR_LOOP, $error_hash);
							$sp_error_on_flg = 1;
						}
					}
				}
			}
		}
	}

	my $name_flg        = 0;
	my $cname_flg       = 0;
	my $department_flg  = 0;
	my $todouhuken 		= 0;
	my $address_flg     = 0;
	my $mail_flg        = 0;
	my $pay_flg         = 0;
	my $pnum_flg        = 0;
	my $fnum_flg        = 0;
	my $day_pnum_flg    = 0;
	my $birth_flg       = 0;
	my $dhope_flg       = 0;
	my $mailguide_flg   = 0;

	$name_flg        = 1 if (($FORM{'lname'}) || ($FORM{'fname'}) || ($FORM{'lname_kana'}) || ($FORM{'fname_kana'}));
	$cname_flg       = 1 if (($FORM{'cname'}) || ($FORM{'cname_kana'}));
	$department_flg  = 1 if ($FORM{'department'});
	$todouhuken = $FORM{'todouhuken'} if ($FORM{'todouhuken'});
	$address_flg     = 1 if (($FORM{'pcode_first'} ne '') || ($FORM{'pcode_last'} ne ''));
	$mail_flg        = 1 if (($FORM{'mail'}) || ($FORM{'mail_check'}));
	$pay_flg         = 1 if ($FORM{'pay_num'});
	$pnum_flg        = 1 if (($FORM{'pnum_1'}) || ($FORM{'pnum_2'}) || ($FORM{'pnum_3'}));
	$fnum_flg        = 1 if (($FORM{'fnum_1'}) || ($FORM{'fnum_2'}) || ($FORM{'fnum_3'}));
	$day_pnum_flg    = 1 if (($FORM{'day_pnum_1'}) || ($FORM{'day_pnum_2'}) || ($FORM{'day_pnum_3'}));
	$birth_flg       = 1 if (($FORM{'birthyear'}) || ($FORM{'birthmonth'}) || ($FORM{'birthday'}));
	$dhope_flg       = 1 if ($FORM{'dhope'});
	$mailguide_flg   = 1 if ($FORM{'mailguide'});
	#			seibetu_flg            => $seibetu_flg,
	#			sei_m_flg              => $FORM{'sei_m_flg'},
	#			sei_f_flg              => $FORM{'sei_f_flg'},
	
	my $bpage_u_flg = 0;
	my $bpage_s_flg = 0;
	my $bpage_g_flg = 0;
	my $bpage_c_flg = 0;
	my $bpage_flg	= 0;

	$bpage_flg  = 1 unless ($FORM{'pid'});
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
	$template->param(
		name_flg                => $name_flg,
		lname                   => MODULE::StringUtil::conversionSpecialChar($FORM{'lname'}),
		fname                   => MODULE::StringUtil::conversionSpecialChar($FORM{'fname'}),
		lname_kana              => MODULE::StringUtil::conversionSpecialChar($FORM{'lname_kana'}),
		fname_kana              => MODULE::StringUtil::conversionSpecialChar($FORM{'fname_kana'}),
		cname_flg               => $cname_flg,
		cname                   => MODULE::StringUtil::conversionSpecialChar($FORM{'cname'}),
		cname_kana              => MODULE::StringUtil::conversionSpecialChar($FORM{'cname_kana'}),
		department_flg          => $department_flg,
		department              => MODULE::StringUtil::conversionSpecialChar($FORM{'department'}),
		address_flg             => $address_flg,
		pcode_first             => MODULE::StringUtil::conversionSpecialChar($FORM{'pcode_first'}),
		pcode_last              => MODULE::StringUtil::conversionSpecialChar($FORM{'pcode_last'}),
		todouhuken              => MODULE::StringUtil::conversionSpecialChar($todouhuken),
		address                 => MODULE::StringUtil::conversionSpecialChar($FORM{'address'}),
		mail_flg                => $mail_flg,
		mail                    => MODULE::StringUtil::conversionSpecialChar($FORM{'mail'}),
		mail_check              => MODULE::StringUtil::conversionSpecialChar($FORM{'mail_check'}),
		pay_flg                 => $pay_flg,
		pay_num                 => MODULE::StringUtil::conversionSpecialChar($FORM{'pay_num'}),
		pnum_flg                => $pnum_flg,
		pnum_1                  => MODULE::StringUtil::conversionSpecialChar($FORM{'pnum_1'}),
		pnum_2                  => MODULE::StringUtil::conversionSpecialChar($FORM{'pnum_2'}),
		pnum_3                  => MODULE::StringUtil::conversionSpecialChar($FORM{'pnum_3'}),
		fnum_flg                => $fnum_flg,
		fnum_1                  => MODULE::StringUtil::conversionSpecialChar($FORM{'fnum_1'}),
		fnum_2                  => MODULE::StringUtil::conversionSpecialChar($FORM{'fnum_2'}),
		fnum_3                  => MODULE::StringUtil::conversionSpecialChar($FORM{'fnum_3'}),
		day_pnum_flg            => $day_pnum_flg,
		day_pnum_1              => MODULE::StringUtil::conversionSpecialChar($FORM{'day_pnum_1'}),
		day_pnum_2              => MODULE::StringUtil::conversionSpecialChar($FORM{'day_pnum_2'}),
		day_pnum_3              => MODULE::StringUtil::conversionSpecialChar($FORM{'day_pnum_3'}),
		birth_flg               => $birth_flg,
		birthyear               => MODULE::StringUtil::conversionSpecialChar($FORM{'birthyear'}),
		birthmonth              => MODULE::StringUtil::conversionSpecialChar($FORM{'birthmonth'}),
		birthday                => MODULE::StringUtil::conversionSpecialChar($FORM{'birthday'}),
		seibetu_flg             => 1,
		sei_fm_flg              => $FORM{'sei_fm_flg'},
		sp_ship_flg             => $FORM{'sp_ship'},
		dhope_flg               => $dhope_flg,
		dhope                   => &strBr(MODULE::StringUtil::conversionSpecialChar($FORM{'dhope'})),
		mailguide_flg           => $mailguide_flg,
		mailok_flg              => $FORM{'mailguide'},
		idea                    => &strBr(MODULE::StringUtil::conversionSpecialChar($FORM{'idea'})),
		
		subtotal_amount         => &convertMoney($subtotal_amount),
		tax_string              => $_CONFIG_tax_marking,
		bpage_url               => $bpage_url,
		discount_flg            => $discount_flg,
		cash_discount           => &convertMoney($cash_discount),
		total_amount            => &convertMoney($total_amount),
		delivery_flg            => $_CONFIG_carriage_carriage_disp,
		ship_free_flg           => $_CONFIG_carriage_free_shipping_set,
		ship_free_if            => &convertMoney($_CONFIG_carriage_free_shipping_set),
		addItem_flg             => $addItem_flg,
		CART_LOOP               => \@CART_LOOP,
		SP_CART_LOOP            => \@SP_CART_LOOP,
		error_on_flg            => $FORM{'error_on_flg'},
		SP_MUST_ERROR_LOOP      => \@SP_MUST_ERROR_LOOP,
		SP_INCORRECT_ERROR_LOOP => \@SP_INCORRECT_ERROR_LOOP,
		email_error_flg         => $email_error_flg,
		
		bpage_flg               => $bpage_flg,
		saleItem_id             => $FORM{'saleItem_id'},
		bpage                   => $FORM{'bpage'},
		pid                     => $FORM{'pid'},
		stype                   => $FORM{'stype'},
		vtype                   => $FORM{'vtype'},
		bpage_u_flg             => $bpage_u_flg,
		ukeyword                => MODULE::StringUtil::conversionSpecialChar($FORM{'ukeyword'}),
		bpage_s_flg             => $bpage_s_flg,
		skeyword                => MODULE::StringUtil::conversionSpecialChar($FORM{'skeyword'}),
		bpage_g_flg             => $bpage_g_flg,
		gkeyword                => MODULE::StringUtil::conversionSpecialChar($FORM{'gkeyword'}),
		bpage_c_flg             => $bpage_c_flg,
		ckeyword                => MODULE::StringUtil::conversionSpecialChar($FORM{'ckeyword'}),
		vnum                    => $FORM{'vnum'},
		sp_must_flg             => $sp_must_flg,
	);
	
	&httpHeadOutput($setcook1 . "\n");
	print $template -> output;


	$session->flush();

	&chmodSessionFile ($session_pass, $_CONFIG_session_file_header, $session_id);


exit;

