#!/usr/bin/perl
use CGI::Session qw/-ip_match/;
use CGI::Session::Cleaning;
use MODULE::Template;
use MODULE::StringUtil;

	our $_CONFIG_server_ssl_www_root;
	our $_CONFIG_page_view_mode;
	our $_CONFIG_server_ssl_site_addr;
	our $_CONFIG_server_url;
	our $_CONFIG_order_tag_order;
	our $_CONFIG_template_dir;
	
	our $_CONFIG_session_dir;
	our $_CONFIG_session_file_header;

	require './subroutine.pl';
	require './config_data.cgi';
	our %FORM;
	our $delivery_counter;
	our $pay_counter   = 0;
	&formLoading;


	our $session_pass = "$_CONFIG_server_ssl_www_root/cgi-bin/$_CONFIG_session_dir";

	my @payment_file ;

	
	our $http_path;
	if ($_CONFIG_server_ssl_use ne '0' && $_CONFIG_page_view_mode ne 'P') {
		$http_path = sprintf('%s/cgi-bin', $_CONFIG_server_url);
	} else {
		$http_path = '../cgi-bin';
		$_CONFIG_server_ssl_www_root = '..';
	}
	
	our $template = HTML::Template->new(filename => "./$_CONFIG_template_dir/order_form_check.tmp");
	
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
	if ($ENV{'HTTP_REFERER'} =~ /order_form.cgi/) {
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
	if ($ENV{'HTTP_REFERER'} =~ /order_form_delivery.cgi/) {
		#別途配送先のフォームデータをセッションに格納します。
		$session->param('sp_lname', $FORM{'sp_lname'});				#氏名（姓）
		$session->param('sp_fname', $FORM{'sp_fname'});					#氏名（名）
		$session->param('sp_lname_kana', $FORM{'sp_lname_kana'});		#氏名（姓）カナ
		$session->param('sp_fname_kana', $FORM{'sp_fname_kana'});		#氏名（名）カナ
		$session->param('sp_cname', $FORM{'sp_cname'});					#法人名
		$session->param('sp_cname_kana', $FORM{'sp_cname_kana'});		#法人名カナ
		$session->param('sp_department', $FORM{'sp_department'});		#所属部署/役職名
		$session->param('sp_pcode_first', $FORM{'sp_pcode_first'});		#郵便番号上3桁
		$session->param('sp_pcode_last', $FORM{'sp_pcode_last'});		#郵便番号下4桁
		$session->param('sp_address', $FORM{'sp_address'});				#住所
		$session->param('sp_mail', $FORM{'sp_mail'});					#メールアドレス
		$session->param('sp_mail_check', $FORM{'sp_mail_check'});		#メールアドレス確認
		$session->param('sp_pnum_1', $FORM{'sp_pnum_1'});				#電話番号（市外）
		$session->param('sp_pnum_2', $FORM{'sp_pnum_2'});				#電話番号（市内）
		$session->param('sp_pnum_3', $FORM{'sp_pnum_3'});				#電話番号（番号）
		$session->param('sp_fnum_1', $FORM{'sp_fnum_1'});				#FAX番号（市外）
		$session->param('sp_fnum_2', $FORM{'sp_fnum_2'});				#FAX番号（市内）
		$session->param('sp_fnum_3', $FORM{'sp_fnum_3'});				#FAX番号（番号）
		$session->param('sp_day_pnum_1', $FORM{'sp_day_pnum_1'});		#日中の連絡先（市外）
		$session->param('sp_day_pnum_2', $FORM{'sp_day_pnum_2'});		#日中の連絡先（市内）
		$session->param('sp_day_pnum_3', $FORM{'sp_day_pnum_3'});		#日中の連絡先（番号）
		$session->param('sp_birthyear', $FORM{'sp_birthyear'});			#生年月日（年）
		$session->param('sp_birthmonth', $FORM{'sp_birthmonth'});		#生年月日（月）
		$session->param('sp_birthday', $FORM{'sp_birthday'});			#生年月日（日）
		foreach (@form_file) {
			my @form_line = split(/\t/, $_);
			if ($form_line[9] eq 'A') {
				$session->param("sp_order_$form_line[0]", $FORM{"sp_order_$form_line[0]"});
			}
		}

	}
	
	if ($ENV{'HTTP_REFERER'} =~ /order_form_check.cgi/) {
		if ($FORM{'sp_ship'}) {
			#別途配送先のフォームデータをセッションに格納します。
			$session->param('sp_lname', $FORM{'sp_lname'});				#氏名（姓）
			$session->param('sp_fname', $FORM{'sp_fname'});					#氏名（名）
			$session->param('sp_lname_kana', $FORM{'sp_lname_kana'});		#氏名（姓）カナ
			$session->param('sp_fname_kana', $FORM{'sp_fname_kana'});		#氏名（名）カナ
			$session->param('sp_cname', $FORM{'sp_cname'});					#法人名
			$session->param('sp_cname_kana', $FORM{'sp_cname_kana'});		#法人名カナ
			$session->param('sp_department', $FORM{'sp_department'});		#所属部署/役職名
			$session->param('sp_pcode_first', $FORM{'sp_pcode_first'});		#郵便番号上3桁
			$session->param('sp_pcode_last', $FORM{'sp_pcode_last'});		#郵便番号下4桁
			$session->param('sp_address', $FORM{'sp_address'});				#住所
			$session->param('sp_mail', $FORM{'sp_mail'});					#メールアドレス
			$session->param('sp_mail_check', $FORM{'sp_mail_check'});		#メールアドレス確認
			$session->param('sp_pnum_1', $FORM{'sp_pnum_1'});				#電話番号（市外）
			$session->param('sp_pnum_2', $FORM{'sp_pnum_2'});				#電話番号（市内）
			$session->param('sp_pnum_3', $FORM{'sp_pnum_3'});				#電話番号（番号）
			$session->param('sp_fnum_1', $FORM{'sp_fnum_1'});				#FAX番号（市外）
			$session->param('sp_fnum_2', $FORM{'sp_fnum_2'});				#FAX番号（市内）
			$session->param('sp_fnum_3', $FORM{'sp_fnum_3'});				#FAX番号（番号）
			$session->param('sp_day_pnum_1', $FORM{'sp_day_pnum_1'});		#日中の連絡先（市外）
			$session->param('sp_day_pnum_2', $FORM{'sp_day_pnum_2'});		#日中の連絡先（市内）
			$session->param('sp_day_pnum_3', $FORM{'sp_day_pnum_3'});		#日中の連絡先（番号）
			$session->param('sp_birthyear', $FORM{'sp_birthyear'});			#生年月日（年）
			$session->param('sp_birthmonth', $FORM{'sp_birthmonth'});		#生年月日（月）
			$session->param('sp_birthday', $FORM{'sp_birthday'});			#生年月日（日）
			foreach (@form_file) {
				my @form_line = split(/\t/, $_);
				if ($form_line[9] eq 'A') {
					$session->param("order_$form_line[0]", $FORM{"order_$form_line[0]"});
				}
			}

		} else {
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
					$session->param("sp_order_$form_line[0]", $FORM{"sp_order_$form_line[0]"});
				}
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
	
	our $total_delivery = 0;
	my @delivery_back;
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
		my $pretax_flg			= 0;
		my $pretax_price		= 0;
		my $unit_price_tax_on	= 0;
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
		
		#_配送タイプ
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
					push (@delivery_back, $delivery_line[0])
				}
			} elsif ($_CONFIG_carriage_compu_method eq 'C') {
				$total_delivery += $unit_delivery;
			}
		#}
		
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
			push(@DISCOUNT_LOOP_hash, $hash);
		}
	}
	
	our $discount_flg;
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
	if ($_CONFIG_carriage_free_shipping_set ne '') {
		if ($_CONFIG_carriage_free_shipping_set > $total_amount) {
			$total_amount = $total_amount + $total_delivery;
		} else {
			$total_delivery = 0;
		}
	} else {
		$total_amount = $total_amount + $total_delivery;
	}
	
	my $data_file = "$_CONFIG_server_ssl_www_root/cgi-bin/item_delivery.cgi";
	open(DATA, $data_file);
	my @data_file = <DATA>;
	close(DATA);
	chomp @data_file;
	
	our @DELIVERY_LOOP_hash = ();
	our $delivery_flg;

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
			delivery_comment     => &convertMoney($data_line[51]),
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
	
	my @VIEW_SP_CART_LOOP = ();
	
	our $out_sp_seibetu_flg;
	if ($FORM{'sp_ship'}) {
		our $sp_error_on_flg;
		our $sp_agent_error_flg;
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
		
		our @SP_MUST_ERROR_LOOP = ();
		our @SP_INCORRECT_ERROR_LOOP = ();
		our $sp_email_error_flg;
		
		SPFORM:foreach (@form_file) {
			my @form_line = split(/\t/, $_);
			my @SP_CHECKBOX_LOOP = ();
			
			if ($form_line[4] != 0) {
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
				my $addItem_flg    = 0;

				$order_must_flg = 1 if ($form_line[5]);
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
				$addItem_flg    = 1 if ($form_line[0] >= 12);
				my $sp_seibetu_flg = 0;
				if ($form_line[0] == 11) {
					$sp_seibetu_flg     = 1;
					$out_sp_seibetu_flg = 1;
				}
				
				my $pulldown_flg		= 0;
				my $pd_name				= 0;
				my $checkbox_flg		= 0;
				my $radio_flg			= 0;
				my $order_item_name		= '';
				my $order_item_explan	= '';
				my $text_id				= '';
				my $text_item			= '';
				my $text_flg			= 0;
				
				if ($addItem_flg) {
					$order_item_name   = $form_line[1];
					$pd_name           = 'sp_order_' . $form_line[0];
					my $hit_check;
					if ($form_line[9] eq 'S') {
						$pulldown_flg = 1;
						my @option_list = split(/<RETURN>/, $form_line[10]);
						chomp @option_list;
						my $i = 1;
						foreach (@option_list) {
							if ($FORM{"sp_order_$form_line[0]"} ne '') {
								$pd_option = $option_list[$FORM{"sp_order_$form_line[0]"} - 1];
								$hit_check++;
							}
							$i++;
						}
					} elsif ($form_line[9] eq 'C') {
						$checkbox_flg = 1;
						my @option_list = split(/<RETURN>/, $form_line[10]);
						chomp @option_list;
						$i = 1;
						foreach (@option_list) {
							if ($FORM{"sp_order_$form_line[0]_$i"} ne '') {
								my $sub_hash = {
									sp_c_option => $_,
								};
							push(@SP_CHECKBOX_LOOP, $sub_hash);
							$hit_check++;
							}
							$i++;
						}
					} elsif ($form_line[9] eq 'R') {
						$radio_flg = 1;
						my @option_list = split(/<RETURN>/, $form_line[10]);
						chomp @option_list;
						my $i = 1;
						foreach (@option_list) {
							if ($i == $FORM{"sp_order_$form_line[0]"}) {
								$r_option = $_;
								$hit_check++;
								last;
							}
							$i++;
						}
					} elsif ($form_line[9] eq 'A') {
						$text_item = &strTrim($FORM{"sp_order_$form_line[0]"});
						$text_flg  = 1;
					}
					
				}
				my @area_flg;
				$area_flg[$FORM{'sp_todouhuken'}] = 1;
#				my $sp_sei_fm_flg = 1 if ($FORM{'sp_sei_fm_flg'} eq 'm');
				my $sp_sei_fm_m_flg = '';
				my $sp_sei_fm_f_flg = '';
				if ( $FORM{'sp_sei_fm_flg'} eq 'm' ) {
					$sp_sei_fm_m_flg = 1;
					$sp_sei_fm_f_flg = 0;
				} elsif ( $FORM{'sp_sei_fm_flg'} eq 'f' ) {
					$sp_sei_fm_m_flg = 0;
					$sp_sei_fm_f_flg = 1;
				} else {
					$sp_sei_fm_m_flg = 0;
					$sp_sei_fm_f_flg = 0;
				}

				$hash = {
					sp_order_must_flg         => $order_must_flg,
					sp_name_flg               => $name_flg,
					sp_lname                  => MODULE::StringUtil::conversionSpecialChar($FORM{'sp_lname'}),
					sp_fname                  => MODULE::StringUtil::conversionSpecialChar($FORM{'sp_fname'}),
					sp_lname_kana             => MODULE::StringUtil::conversionSpecialChar($FORM{'sp_lname_kana'}),
					sp_fname_kana             => MODULE::StringUtil::conversionSpecialChar($FORM{'sp_fname_kana'}),
					sp_cname_flg              => $cname_flg,
					sp_cname                  => MODULE::StringUtil::conversionSpecialChar($FORM{'sp_cname'}),
					sp_cname_kana             => MODULE::StringUtil::conversionSpecialChar($FORM{'sp_cname_kana'}),
					sp_department_flg         => $department_flg,
					sp_department             => MODULE::StringUtil::conversionSpecialChar($FORM{'sp_department'}),
					sp_address_flg            => $address_flg,
					sp_pcode_first            => MODULE::StringUtil::conversionSpecialChar($FORM{'sp_pcode_first'}),
					sp_pcode_last             => MODULE::StringUtil::conversionSpecialChar($FORM{'sp_pcode_last'}),
					sp_todouhuken             => MODULE::StringUtil::conversionSpecialChar(&prefOut($FORM{'sp_todouhuken'})),
					sp_address                => MODULE::StringUtil::conversionSpecialChar($FORM{'sp_address'}),
					sp_mail_flg               => $mail_flg,
					sp_mail                   => MODULE::StringUtil::conversionSpecialChar($FORM{'sp_mail'}),
					sp_mail_check             => MODULE::StringUtil::conversionSpecialChar($FORM{'sp_mail_check'}),
					sp_pnum_flg               => $pnum_flg,
					sp_pnum_1                 => MODULE::StringUtil::conversionSpecialChar($FORM{'sp_pnum_1'}),
					sp_pnum_2                 => MODULE::StringUtil::conversionSpecialChar($FORM{'sp_pnum_2'}),
					sp_pnum_3                 => MODULE::StringUtil::conversionSpecialChar($FORM{'sp_pnum_3'}),
					sp_fnum_flg               => $fnum_flg,
					sp_fnum_1                 => MODULE::StringUtil::conversionSpecialChar($FORM{'sp_fnum_1'}),
					sp_fnum_2                 => MODULE::StringUtil::conversionSpecialChar($FORM{'sp_fnum_2'}),
					sp_fnum_3                 => MODULE::StringUtil::conversionSpecialChar($FORM{'sp_fnum_3'}),
					sp_day_pnum_flg           => $day_pnum_flg,
					sp_day_pnum_1             => MODULE::StringUtil::conversionSpecialChar($FORM{'sp_day_pnum_1'}),
					sp_day_pnum_2             => MODULE::StringUtil::conversionSpecialChar($FORM{'sp_day_pnum_2'}),
					sp_day_pnum_3             => MODULE::StringUtil::conversionSpecialChar($FORM{'sp_day_pnum_3'}),
					sp_birth_flg              => $birth_flg,
					sp_birthyear              => MODULE::StringUtil::conversionSpecialChar($FORM{'sp_birthyear'}),
					sp_birthmonth             => MODULE::StringUtil::conversionSpecialChar($FORM{'sp_birthmonth'}),
					sp_birthday               => MODULE::StringUtil::conversionSpecialChar($FORM{'sp_birthday'}),
					sp_seibetu_flg            => $sp_seibetu_flg,
					sp_sei_fm_m_flg           => $sp_sei_fm_m_flg,
					sp_sei_fm_f_flg           => $sp_sei_fm_f_flg,
					sp_addItem_flg            => $addItem_flg,
					sp_order_item_name        => MODULE::StringUtil::conversionSpecialChar($order_item_name),
					sp_addItem_flg            => $addItem_flg,
					sp_order_item_name        => MODULE::StringUtil::conversionSpecialChar($order_item_name),
					sp_pulldown_flg           => $pulldown_flg,
					sp_pd_option              => MODULE::StringUtil::conversionSpecialChar($pd_option),
					sp_checkbox_flg           => $checkbox_flg,
					SP_CHECKBOX_LOOP          => \@SP_CHECKBOX_LOOP,
					sp_radio_flg              => $radio_flg,
					sp_r_option               => MODULE::StringUtil::conversionSpecialChar($r_option),
					sp_text_flg               => $text_flg,
					sp_text_item              => &strBr(MODULE::StringUtil::conversionSpecialChar($text_item)),
				};
				push(@VIEW_SP_CART_LOOP, $hash);
			}
		}
		&checkErrorDelivery;
		my $agent_file = "$_CONFIG_server_ssl_www_root/cgi-bin/search/item_agent.cgi";
		open(DATA, $agent_file);
		my @agent_file = <DATA>;
		close(DATA);
		
		if ($FORM{'pay_num'} == 4) {
			my $agent_count;
			foreach (@agent_file) {
				my @agent_line = split(/\t/, $_);
				if ($agent_line[2] != 0) {
					$agent_count++;
				}
			}
			foreach (@agent_file) {
				my @agent_line = split(/\t/, $_);
				if ($total_amount > 300000) {
					if (($agent_line[0] == 1) && ($agent_count == 1) && ($agent_line[2] == 1)) {
						$sp_agent_error_flg = 1;
						$sp_error_on_flg    = 1;
						last;
					}
				}
			}
		}
		if ($sp_error_on_flg) {
			&outputErrorDelivery();
	&httpHeadOutput($setcook1 . "\n");

			print $template -> output;
			print $sp_error_on_flg;

			$session->flush();

			my $session_file = $session_pass . $_CONFIG_session_file_header . $session_id;

			chmod 0666, $session_file or &outputLog("パーミッション変更エラー :" . $i);

			exit;
		}
	}
	
	my @VIEW_CART_LOOP = ();
	
	our $error_on_flg;
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
	
	#_別途お届け先項目数をカウント
	our $delivery_counter;
	our $out_seibetu_flg;
	FORM:foreach (@form_file) {
		my @form_line = split(/\t/, $_);
		my @PAY_LOOP      = ();
		my @PULLDOWN_LOOP = ();
		my @CHECKBOX_LOOP = ();
		my @RADIO_LOOP    = ();
		
		if ($form_line[4] != 0) {
			$delivery_counter++;
		}
		if ($form_line[2] != 0) {
			my $daikou_flg				= 0;
			my $cerdit_description_flg	= 0;
			my $pay_option				= '';

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
			my $addItem_flg    = 0;

			$order_must_flg = 1 if ($form_line[3]);
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
			$addItem_flg    = 1 if ($form_line[0] >= 12);
			my $seibetu_flg = 0;
			if ($form_line[0] == 11) {
				$seibetu_flg     = 1;
				$out_seibetu_flg = 1;
			}
			
			if ($pay_flg) {
				my $payment_file = "$_CONFIG_server_ssl_www_root/cgi-bin/search/item_payment.cgi";
				open(DATA, $payment_file);
				@payment_file = <DATA>;
				close(DATA);
				
				@payment_file = sort { (split(/\t/,$a))[3] <=> (split(/\t/,$b))[3] } @payment_file;
				
				foreach (@payment_file) {
					my @payment_line = split(/\t/, $_);
					$pay_option = $payment_line[1] if ($payment_line[0] == $FORM{'pay_num'});
				}
				
				my $agent_file = "$_CONFIG_server_ssl_www_root/cgi-bin/search/item_agent.cgi";
				open(DATA, $agent_file);
				my @agent_file = <DATA>;
				close(DATA);
				
				if ($FORM{'pay_num'} == 4) {
					my $agent_count = 0;
					foreach (@agent_file) {
						my @agent_line = split(/\t/, $_);
						if ($agent_line[2] != 0) {
							$agent_count++;
						}
					}
					foreach (@agent_file) {
						my @agent_line = split(/\t/, $_);
						if ($total_amount > 300000) {
							if (($agent_line[0] == 1) && ($agent_count == 1) && ($agent_line[2] == 1)) {
								$agent_error_flg = 1;
								$error_on_flg    = 1;
								last FORM;
							}
						}
					}
				}
			}
			
			my $pulldown_flg	= 0;
			my $pd_name			= '';
			my $checkbox_flg	= 0;
			my $radio_flg		= 0;
			my $order_item_name	= '';
			my $text_id			= '';
			my $text_item		= '';
			my $text_flg		= '';
			
			if ($addItem_flg) {
				$order_item_name   = $form_line[1];
				$pd_name           = 'order_' . $form_line[0];
				my $hit_check;
				if ($form_line[9] eq 'S') {
					$pulldown_flg = 1;
					my @option_list = split(/<RETURN>/, $form_line[10]);
					chomp @option_list;
					my $i = 1;
					foreach (@option_list) {
						if ($FORM{"order_$form_line[0]"} ne '') {
							$pd_option = $option_list[$FORM{"order_$form_line[0]"} - 1];
							$hit_check++;
							last
						}
						$i++;
					}
				} elsif ($form_line[9] eq 'C') {
					$checkbox_flg = 1;
					my @option_list = split(/<RETURN>/, $form_line[10]);
					chomp @option_list;
					$i = 1;
					foreach (@option_list) {
						if ($FORM{"order_$form_line[0]_$i"} ne '') {
							my $sub_hash = {
								c_option => $_,
							};
							push(@CHECKBOX_LOOP, $sub_hash);
							$hit_check++;
						}
						$i++;
					}
				} elsif ($form_line[9] eq 'R') {
					$radio_flg = 1;
					my @option_list = split(/<RETURN>/, $form_line[10]);
					chomp @option_list;
					my $i = 1;
					foreach (@option_list) {
						if ($i == $FORM{"order_$form_line[0]"}) {
							$r_option = $_;
							$hit_check++;
							last;
						}
						$i++;
					}
				} elsif ($form_line[9] eq 'A') {
					$text_item = &strTrim($FORM{"order_$form_line[0]"});
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
				todouhuken             => MODULE::StringUtil::conversionSpecialChar(&prefOut($FORM{'todouhuken'})),
				address                => MODULE::StringUtil::conversionSpecialChar($FORM{'address'}),
				mail_flg               => $mail_flg,
				mail                   => MODULE::StringUtil::conversionSpecialChar($FORM{'mail'}),
				mail_check             => MODULE::StringUtil::conversionSpecialChar($FORM{'mail_check'}),
				pay_flg                => $pay_flg,
				pay_option             => MODULE::StringUtil::conversionSpecialChar($pay_option),
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
				pulldown_flg           => $pulldown_flg,
				pd_option              => MODULE::StringUtil::conversionSpecialChar($pd_option),
				checkbox_flg           => $checkbox_flg,
				CHECKBOX_LOOP          => \@CHECKBOX_LOOP,
				radio_flg              => $radio_flg,
				r_option               => MODULE::StringUtil::conversionSpecialChar($r_option),
				text_flg               => $text_flg,
				text_item              => &strBr(MODULE::StringUtil::conversionSpecialChar($text_item)),
			};
			push(@VIEW_CART_LOOP, $hash);
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
	
	my @CART_LOOP = ();
	my $addItem_flg;
	foreach (@form_file) {
		my @form_line = split(/\t/, $_);
		my @PAY_LOOP      = ();
		my @PULLDOWN_LOOP = ();
		my @CHECKBOX_LOOP = ();
		my @RADIO_LOOP    = ();
		
		if ($form_line[2] != 0) {
			$addItem_flg++;
			my $daikou_flg				= 0;
			my $visa_flg				= 0;
			my $master_flg				= 0;
			my $jcb_flg					= 0;
			my $amex_flg				= 0;
			my $diners_flg				= 0;
			my $cerdit_description_flg	= 0;
			
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
				if ($form_line[9] eq 'S') {
					$pulldown_flg = 1;
					my @option_list = split(/<RETURN>/, $form_line[10]);
					chomp @option_list;
					my $i = 1;
					foreach (@option_list) {
						if ($FORM{"order_$form_line[0]"} ne '') {
							$pd_id     = 'order_' . $form_line[0];
							$pd_option = $FORM{"order_$form_line[0]"};
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
							$c_id = 'order_' . $form_line[0] . '_' . $i;
							$c_option = $FORM{"order_$form_line[0]_$i"};
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
							text_id                => MODULE::StringUtil::conversionSpecialChar($text_id),
							text_item              => &strBr(MODULE::StringUtil::conversionSpecialChar($text_item)),
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
					text_id                => MODULE::StringUtil::conversionSpecialChar($text_id),
					text_item              => &strBr(MODULE::StringUtil::conversionSpecialChar($text_item)),
				};
				push(@CART_LOOP, $hash);
			}
		}
	}
	
	my @SP_CART_LOOP = ();
	my $sp_addItem_flg = 0;
	foreach (@form_file) {
		my @form_line = split(/\t/, $_);
		
		if ($form_line[4] != 0) {
			$sp_addItem_flg++;
			my $credit_flg				= 0;
			my $daikou_flg				= 0;
			my $visa_flg				= 0;
			my $master_flg				= 0;
			my $jcb_flg					= 0;
			my $amex_flg				= 0;
			my $diners_flg				= 0;
			my $cerdit_description_flg	= 0;
			
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
				$pd_name           = 'sp_order_' . $form_line[0];
				if ($form_line[9] eq 'S') {
					$pulldown_flg = 1;
					my @option_list = split(/<RETURN>/, $form_line[10]);
					chomp @option_list;
					my $i = 1;
					foreach (@option_list) {
						if ($FORM{"sp_order_$form_line[0]"} ne '') {
							$pd_id     = 'sp_order_' . $form_line[0];
							$pd_option = $FORM{"sp_order_$form_line[0]"};
						}
						$i++;
					}
				} elsif ($form_line[9] eq 'C') {
					$checkbox_flg = 1;
					my @option_list = split(/<RETURN>/, $form_line[10]);
					chomp @option_list;
					my $i = 1;
					foreach (@option_list) {
						if ($FORM{"sp_order_$form_line[0]_$i"} ne '') {
							$c_id = 'sp_order_' . $form_line[0] . '_' . $i;
							$c_option = $FORM{"sp_order_$form_line[0]_$i"};
							$hash = {
								sp_pulldown_flg           => $pulldown_flg,
								sp_pd_id                  => $pd_id,
								sp_pd_option              => $pd_option,
								sp_checkbox_flg           => $checkbox_flg,
								sp_c_id                   => $c_id,
								sp_c_option               => $c_option,
								sp_radio_flg              => $radio_flg,
								sp_r_id                   => $r_id,
								sp_r_option               => $r_option,
								sp_text_flg               => $text_flg,
								sp_text_id                => MODULE::StringUtil::conversionSpecialChar($text_id),
								sp_text_item              => &strBr(MODULE::StringUtil::conversionSpecialChar($text_item)),
							};
							push(@SP_CART_LOOP, $hash);
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
						if ($i == $FORM{"sp_order_$form_line[0]"}) {
							$r_id = 'sp_order_' . $form_line[0];
							$r_option = $i;
							last;
						}
						$i++;
					}
				} elsif ($form_line[9] eq 'A') {
					$text_id   = 'sp_order_' . $form_line[0];
					$text_item = &strTrim($FORM{"sp_order_$form_line[0]"});
					$text_flg  = 1;
				}
				
				$hash = {
					sp_pulldown_flg           => $pulldown_flg,
					sp_pd_id                  => $pd_id,
					sp_pd_option              => $pd_option,
					sp_checkbox_flg           => $checkbox_flg,
					sp_c_id                   => $c_id,
					sp_c_option               => $c_option,
					sp_radio_flg              => $radio_flg,
					sp_r_id                   => $r_id,
					sp_r_option               => $r_option,
					sp_text_flg               => $text_flg,
					sp_text_id                => MODULE::StringUtil::conversionSpecialChar($text_id),
					sp_text_item              => &strBr(MODULE::StringUtil::conversionSpecialChar($text_item)),
				};
				push(@SP_CART_LOOP, $hash);
			}
		}
	}

	my $name_flg        = 0;
	my $cname_cname_flg = 0;
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
	$cname_cname_flg = 1 if (($FORM{'cname'}) || ($FORM{'cname_kana'}));
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
	$mailguide_flg   = 1 if ($_CONFIG_order_announce_view);

	my $sp_name_flg        = 0;
	my $sp_cname_cname_flg = 0;
	my $sp_department_flg  = 0;
	my $sp_todouhuken      = 0;
	my $sp_address_flg     = 0;
	my $sp_mail_flg        = 0;
	my $sp_pay_flg         = 0;
	my $sp_pnum_flg        = 0;
	my $sp_fnum_flg        = 0;
	my $sp_day_pnum_flg    = 0;
	my $sp_birth_flg       = 0;
	my $sp_dhope_flg       = 0;
	my $sp_mailguide_flg   = 0;

	$sp_name_flg        = 1 if (($FORM{'sp_lname'}) || ($FORM{'sp_fname'}) || ($FORM{'sp_lname_kana'}) || ($FORM{'sp_fname_kana'}));
	$sp_cname_cname_flg = 1 if (($FORM{'sp_cname'}) || ($FORM{'sp_cname_kana'}));
	$sp_department_flg  = 1 if ($FORM{'sp_department'});
	$sp_todouhuken = $FORM{'sp_todouhuken'} if ($FORM{'sp_todouhuken'});
	$sp_address_flg     = 1 if (($FORM{'sp_pcode_first'} ne '') || ($FORM{'sp_pcode_last'} ne ''));
	$sp_mail_flg        = 1 if (($FORM{'sp_mail'}) || ($FORM{'sp_mail_check'}));
	$sp_pay_flg         = 1 if ($FORM{'sp_siharai'});
	$sp_pnum_flg        = 1 if (($FORM{'sp_pnum_1'}) || ($FORM{'sp_pnum_2'}) || ($FORM{'sp_pnum_3'}));
	$sp_fnum_flg        = 1 if (($FORM{'sp_fnum_1'}) || ($FORM{'sp_fnum_2'}) || ($FORM{'sp_fnum_3'}));
	$sp_day_pnum_flg    = 1 if (($FORM{'sp_day_pnum_1'}) || ($FORM{'sp_day_pnum_2'}) || ($FORM{'sp_day_pnum_3'}));
	$sp_birth_flg       = 1 if (($FORM{'sp_birthyear'}) || ($FORM{'sp_birthmonth'}) || ($FORM{'sp_birthday'}));
	$sp_dhope_flg       = 1 if ($FORM{'sp_dhope'});
	$sp_mailguide_flg   = 1 if ($FORM{'sp_mailguide'});
	
	my ($bpage_u_flg, $bpage_s_flg, $bpage_g_flg, $bpage_c_flg);
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

	my $commission_flg = 0;
	my $commission_discount_flg = 0;
	my $commission_discount = 0;
	my $commission_total = 0;
	my $commission = 0;
	#_支払い方法
	my $pay_style = '';

	if ($FORM{'pay_num'}) {
		
		#_支払い方法
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
		
		if ($FORM{'pay_num'} != 0) {
			if ($payment_line[19] ne '' && $total_amount > $payment_line[19]) {
				$commission = int $payment_line[20];
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
				$commission_flg = 1;
				if ($FORM{'pay_num'} == 2) {
					if ($_CONFIG_order_commission_condition[0] ne '') {
						$commission_discount = $_CONFIG_order_commission_amount[0] if ($total_amount >= $_CONFIG_order_commission_condition[0]);
					}
					if ($_CONFIG_order_commission_condition[1] ne '') {
						$commission_discount = $_CONFIG_order_commission_amount[1] if ($total_amount >= $_CONFIG_order_commission_condition[1]);
					}
					if ($_CONFIG_order_commission_condition[2] ne '') {
						$commission_discount = $_CONFIG_order_commission_amount[2] if ($total_amount >= $_CONFIG_order_commission_condition[2]);
					}
					if ( 0 == int $commission_discount ) {
						$commission_discount_flg = 0;
					} else {
						$commission_discount_flg = 1;
					}
					$commission_total = $commission - $commission_discount;
				}
			}
		}
	}





	$template->param(
		name_flg               => $name_flg,
		lname                  => MODULE::StringUtil::conversionSpecialChar($FORM{'lname'}),
		fname                  => MODULE::StringUtil::conversionSpecialChar($FORM{'fname'}),
		lname_kana             => MODULE::StringUtil::conversionSpecialChar($FORM{'lname_kana'}),
		fname_kana             => MODULE::StringUtil::conversionSpecialChar($FORM{'fname_kana'}),
		cname_flg              => $cname_cname_flg,
		cname                  => MODULE::StringUtil::conversionSpecialChar($FORM{'cname'}),
		cname_kana             => MODULE::StringUtil::conversionSpecialChar($FORM{'cname_kana'}),
		department_flg         => $department_flg,
		department             => MODULE::StringUtil::conversionSpecialChar($FORM{'department'}),
		address_flg            => $address_flg,
		pcode_first            => MODULE::StringUtil::conversionSpecialChar($FORM{'pcode_first'}),
		pcode_last             => MODULE::StringUtil::conversionSpecialChar($FORM{'pcode_last'}),
		todouhuken             => MODULE::StringUtil::conversionSpecialChar($todouhuken),
		address                => MODULE::StringUtil::conversionSpecialChar($FORM{'address'}),
		mail_flg               => MODULE::StringUtil::conversionSpecialChar($mail_flg),
		mail                   => MODULE::StringUtil::conversionSpecialChar($FORM{'mail'}),
		mail_check             => MODULE::StringUtil::conversionSpecialChar($FORM{'mail_check'}),
		pay_flg                => $pay_flg,
		pay_num                => MODULE::StringUtil::conversionSpecialChar($FORM{'pay_num'}),
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
		seibetu_flg            => $out_seibetu_flg,
		sei_fm_flg             => $FORM{'sei_fm_flg'},
		
		sp_name_flg            => $sp_name_flg,
		sp_lname               => MODULE::StringUtil::conversionSpecialChar($FORM{'sp_lname'}),
		sp_fname               => MODULE::StringUtil::conversionSpecialChar($FORM{'sp_fname'}),
		sp_lname_kana          => MODULE::StringUtil::conversionSpecialChar($FORM{'sp_lname_kana'}),
		sp_fname_kana          => MODULE::StringUtil::conversionSpecialChar($FORM{'sp_fname_kana'}),
		sp_cname_flg           => $sp_cname_cname_flg,
		sp_cname               => MODULE::StringUtil::conversionSpecialChar($FORM{'sp_cname'}),
		sp_cname_kana          => MODULE::StringUtil::conversionSpecialChar($FORM{'sp_cname_kana'}),
		sp_department_flg      => $sp_department_flg,
		sp_department          => MODULE::StringUtil::conversionSpecialChar($FORM{'sp_department'}),
		sp_address_flg         => $sp_address_flg,
		sp_pcode_first         => MODULE::StringUtil::conversionSpecialChar($FORM{'sp_pcode_first'}),
		sp_pcode_last          => MODULE::StringUtil::conversionSpecialChar($FORM{'sp_pcode_last'}),
		sp_todouhuken          => MODULE::StringUtil::conversionSpecialChar($sp_todouhuken),
		sp_address             => MODULE::StringUtil::conversionSpecialChar($FORM{'sp_address'}),
		sp_mail_flg            => $sp_mail_flg,
		sp_mail                => MODULE::StringUtil::conversionSpecialChar($FORM{'sp_mail'}),
		sp_mail_check          => MODULE::StringUtil::conversionSpecialChar($FORM{'sp_mail_check'}),
		sp_pnum_flg            => $sp_pnum_flg,
		sp_pnum_1              => MODULE::StringUtil::conversionSpecialChar($FORM{'sp_pnum_1'}),
		sp_pnum_2              => MODULE::StringUtil::conversionSpecialChar($FORM{'sp_pnum_2'}),
		sp_pnum_3              => MODULE::StringUtil::conversionSpecialChar($FORM{'sp_pnum_3'}),
		sp_fnum_flg            => $sp_fnum_flg,
		sp_fnum_1              => MODULE::StringUtil::conversionSpecialChar($FORM{'sp_fnum_1'}),
		sp_fnum_2              => MODULE::StringUtil::conversionSpecialChar($FORM{'sp_fnum_2'}),
		sp_fnum_3              => MODULE::StringUtil::conversionSpecialChar($FORM{'sp_fnum_3'}),
		sp_day_pnum_flg        => $sp_day_pnum_flg,
		sp_day_pnum_1          => MODULE::StringUtil::conversionSpecialChar($FORM{'sp_day_pnum_1'}),
		sp_day_pnum_2          => MODULE::StringUtil::conversionSpecialChar($FORM{'sp_day_pnum_2'}),
		sp_day_pnum_3          => MODULE::StringUtil::conversionSpecialChar($FORM{'sp_day_pnum_3'}),
		sp_birth_flg           => $sp_birth_flg,
		sp_birthyear           => MODULE::StringUtil::conversionSpecialChar($FORM{'sp_birthyear'}),
		sp_birthmonth          => MODULE::StringUtil::conversionSpecialChar($FORM{'sp_birthmonth'}),
		sp_birthday            => MODULE::StringUtil::conversionSpecialChar($FORM{'sp_birthday'}),
		sp_seibetu_flg         => $out_sp_seibetu_flg,
		sp_sei_fm_flg          => $FORM{'sp_sei_fm_flg'},
		
		sp_ship_flg            => $delivery_counter,
		dhope_flg              => $dhope_flg,
		dhope                  => &strBr(MODULE::StringUtil::conversionSpecialChar($FORM{'dhope'})),
		mailguide_flg          => $mailguide_flg,
		mailok_flg             => $FORM{'mailguide'},
		idea                   => &strBr(MODULE::StringUtil::conversionSpecialChar($FORM{'idea'})),
		subtotal_amount        => &convertMoney($subtotal_amount),
		tax_string             => $_CONFIG_tax_marking,
		discount_flg           => $discount_flg,
		cash_discount          => &convertMoney($cash_discount),
		total_amount           => &convertMoney($total_amount),
		delivery_flg           => $_CONFIG_carriage_carriage_disp,
		ship_free_flg          => $_CONFIG_carriage_free_shipping_set,
		ship_free_if           => &convertMoney($_CONFIG_carriage_free_shipping_set),
		VIEW_CART_LOOP         => \@VIEW_CART_LOOP,
		addItem_flg            => $addItem_flg,
		CART_LOOP              => \@CART_LOOP,
		sp_addItem_flg         => $sp_addItem_flg,
		VIEW_SP_CART_LOOP      => \@VIEW_SP_CART_LOOP,
		SP_CART_LOOP           => \@SP_CART_LOOP,
		order_cancel_button    => $_CONFIG_order_cancell_button,
		order_check_button     => $_CONFIG_order_verifles_button,
		sp_flg                 => $FORM{'sp_ship'},
		embedding_tag          => &errstrRecover($_CONFIG_order_tag_order),
		
		delivery_amount        => &convertMoney($total_delivery),
		bpage_flg              => $bpage_flg,
		saleItem_id            => $FORM{'saleItem_id'},
		bpage                  => $FORM{'bpage'},
		pid                    => $FORM{'pid'},
		stype                  => $FORM{'stype'},
		vtype                  => $FORM{'vtype'},
		bpage_u_flg            => $bpage_u_flg,
		ukeyword               => MODULE::StringUtil::conversionSpecialChar($FORM{'ukeyword'}),
		bpage_s_flg            => $bpage_s_flg,
		skeyword               => MODULE::StringUtil::conversionSpecialChar($FORM{'skeyword'}),
		bpage_g_flg            => $bpage_g_flg,
		gkeyword               => MODULE::StringUtil::conversionSpecialChar($FORM{'gkeyword'}),
		bpage_c_flg            => $bpage_c_flg,
		ckeyword               => MODULE::StringUtil::conversionSpecialChar($FORM{'ckeyword'}),
		vnum                   => $FORM{'vnum'},

		commission_flg         => $commission_flg,
		commission             => &convertMoney($commission),
		commission_discount_flg   => $commission_discount_flg,
		commission_total       => &convertMoney($commission_total),
		commission_discount    => &convertMoney($commission_discount),
		pay_style              => $pay_style,
	);
	
	&httpHeadOutput($setcook1 . "\n");
	print $template -> output;


	$session->flush();

	&chmodSessionFile ($session_pass, $_CONFIG_session_file_header, $session_id);


exit;

