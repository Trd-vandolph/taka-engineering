#!/usr/bin/perl
use CGI::Session qw/-ip_match/;
use CGI::Session::Cleaning;
use MODULE::Template;
use POSIX;
use MODULE::StringUtil;

	our $item_max_order_receipts;
	our $item_name_articles;
	our $_CONFIG_tax_consumer;
	our $_CONFIG_tax_indication;
	our $_CONFIG_server_ssl_use;
	our $_CONFIG_page_view_mode;
	our $_CONFIG_server_ssl_site_addr;
	our $_CONFIG_site_title;
	our $_CONFIG_site_outline_site;
	our @_CONFIG_site_keyword;
	our $_CONFIG_server_ssl_www_root;
	our $_CONFIG_template_dir;
	our $_CONFIG_session_dir;
	our $_CONFIG_session_file_header;
	
	require './subroutine.pl';
	require './config_data.cgi';
	&formLoading;
	
	$_CONFIG_server_ssl_www_root = '../';
	# メイン記事エリア
	my $template = HTML::Template->new(filename => "./$_CONFIG_template_dir/order_cart_info.tmp");
	
	our $session_name  = 'sessionCart';
	our $session_timer = 30;
	
	&getCookie($session_name);
	&cleanSession;
	our $session      = CGI::Session->new(undef, $COOKIE{$session_name}, {Directory=>$_CONFIG_session_dir});
	our $session_cart = $session->param($session_name);
	our $session_id   = $session->id;
	
	my $action = $FORM{'action'};
	
	if (($FORM{'action'} eq 'd') && ($FORM{'cid'} ne '')) {
		&delSession($FORM{'cid'}, $session_name);
	} elsif ($FORM{'action'} eq 'ad') {
		&delAllSession($session_name);
	}
	
	$FORM{'saleItem_id'} =~ /(\d{2})(\d{2})(\d{8})/;
	my ($send_cc, $send_gc, $send_ic);
	if ($FORM{'cc'}) {
		$send_cc = $FORM{'cc'}
	} else {
		$send_cc = $1;
	};
	if ($FORM{'gc'}) {
		$send_gc = $FORM{'gc'}
	} else {
		$send_gc = $2
	};
	if ($FORM{'ic'}) {
		$send_ic = $FORM{'ic'}
	} else {
		$send_ic = $3
	}
	$variation = $FORM{"radio_$send_ic"};
	$order_item_code = $FORM{'saleItem_id'} . $variation;
	
	$bpage = &decodUrl($FORM{'bpage'});
	my $bpage_url = $FORM{'bpage'};
	$bpage_url =~ /(.+cgi).*?/;
	$bpage_url = $1 . '?';
	
	my $bpage_url_sub;
	if ($bpage_url =~ /saleItem_detailInfo/) {
		$bpage_url_sub .= sprintf('&cc=%02d', $send_cc);
		$bpage_url_sub .= sprintf('&gc=%02d', $send_gc);
		$bpage_url_sub .= sprintf('&ic=%08d', $send_ic);
	}
	if ($bpage_url =~ /saleItem_category/) {
		$bpage_url_sub .= sprintf('&cc=%02d', $send_cc);
	}
	if ($bpage_url =~ /saleItem_group/) {
		$bpage_url_sub .= sprintf('&cc=%02d', $send_cc);
		$bpage_url_sub .= sprintf('&gc=%02d', $send_gc);
	}
	if ($bpage_url =~ /saleItem_search/) {
		$bpage_url_sub .= sprintf('&item_keyword=%s', &decodUrl($FORM{'item_keyword'}));
		$bpage_url_sub .= sprintf('&item_price_low=%s', $FORM{'item_price_low'});
		$bpage_url_sub .= sprintf('&item_price_up=%s', $FORM{'item_price_up'});
	}
	$bpage_url_sub .= sprintf('&pid=%s', $FORM{'pid'}) if ($FORM{'pid'} ne '');
	$bpage_url_sub .= sprintf('&stype=%s', $FORM{'stype'}) if ($FORM{'stype'} ne '');
	$bpage_url_sub .= sprintf('&vtype=%s', $FORM{'vtype'}) if ($FORM{'vtype'} ne '');
	$bpage_url_sub .= sprintf('&ukeyword=%s', $FORM{'ukeyword'}) if ($FORM{'ukeyword'} ne '');
	$bpage_url_sub .= sprintf('&vnum=%s', $FORM{'vnum'}) if ($FORM{'vnum'} ne '');
	
	$bpage_url .= $bpage_url_sub;
	$bpage_para .= sprintf('&bpage=%s', $bpage);
	$bpage_para .= $bpage_url_sub;
	
	# 「買い物を続ける」の戻り先を取得
	my $back_page_url = './';
	my @back_page_split = split(/\//, $bpage_url);
	foreach $i (@back_page_split) {
		if($i =~ /\.cgi/) {
			$back_page_url .= $i;
		}
		&outputLog("$i :" . $i);
	}
	
	our $session_set_flg = 1;
	our $error_flg;
	our $error_on_flg;
	our $notselected_error_flg;
	our $timeout_error_flg;
	our $empty_error_flg;
	our $error_stock_error_flg;
	our $error_hinmei;
	our $error_variation_code;
	our $error_yoko_name;
	our $error_tate_name;
	our $error_stock_quantity;
	our $error_order_quantity;
	our $error_max_quantity;
	our $error_yoko_title;
	our $error_tate_title;
	our $agent_error_flg;
	
	#_エラーチェック
	if($action eq 'd' || $action eq 'ad'){
		unless (defined $COOKIE{$session_name}) {
			if ($FORM{'saleItem_id'} ne '') {
				$error_on_flg = 1;
				$timeout_error_flg = 1;
			} else {
				$error_flg    = 1;
				$timeout_error_flg = 1;
			}
		}
	}
	
	if ($FORM{'error_on_flg'} && $FORM{'agent_error'}) {
		$agent_error_flg = 1;
		$error_on_flg    = 1;
	}
	
	if ($action eq 'b' && $error_flg eq '' && $error_on_flg eq '' && $FORM{'error_on_flg'} eq '') {
		my $data_file = sprintf('./search/%02d/%02d.cgi', $send_cc, $send_gc);
		open(DATA, $data_file);
		my @data_file = <DATA>;
		close(DATA);
		chomp @data_file;
		
		my $send_line;
		foreach (@data_file) {
			my @data_line = split(/\t/, $_);
			if ($data_line[0] eq $send_ic) {
				$send_line = join("\t", @data_line);
				last;
			}
		}
		my $val_data_file = sprintf('./search/%02d/%02d_variation.cgi', $send_cc, $send_gc);
		open(DATA, $val_data_file);
		my @val_data_file = <DATA>;
		close(DATA);
		foreach (@val_data_file) {
			my @data_line = split(/\t/, $_);
			if ($data_line[0] eq $send_ic) {
				$send_line = $send_line . join("\t", @data_line);
				last;
			}
		}
		$line = $send_line;
		&itemMainDataSplitFull;
		
		if ($error_flg eq '') {
			#_最大注文数以上
			if ($item_max_order_receipts ne '') {
				if (($FORM{'order_quantity'} > $item_max_order_receipts) || (&summary_order_count($order_item_code, $FORM{'order_quantity'}, $session_name) > $item_max_order_receipts)) {
					$error_flg            = 1;
					$max_error_flg        = 1;
					$error_max_quantity   = $item_max_order_receipts;
					$error_order_quantity = &summary_order_count($order_item_code, $FORM{'order_quantity'}, $session_name);
				}
			}
		}
		if ($error_flg eq '') {
			#_注文数値チェック
			if (($FORM{'order_quantity'} =~ /[\D]/) || ($FORM{'order_quantity'} eq '') || ($FORM{'order_quantity'} == '0')) {
				$error_flg           = 1;
				$incorrect_error_flg = 1;
				$FORM{'order_quantity'} = '';
			}
		}
		if ($error_flg eq '') {
			#_バリエーションが選択されていない
			if ($variation eq '') {
				$error_flg             = 1;
				$notselected_error_flg = 1;
			}
		}
		my $stk_data_file = sprintf('./search/%02d/%02d_stock.cgi', $send_cc, $send_gc);
		open(DATA, $stk_data_file);
		my @stk_data_file = <DATA>;
		close(DATA);
		$order_item_code =~ /(\d{12})$/;
		$order_val_code = $1;
		
		if ($error_flg eq '') {
			if ($item_stock_setting_flg) {
				foreach (@stk_data_file) {
					my @data_line = split(/\t/, $_);
					if ($order_val_code eq $data_line[0]) {
						if ($FORM{'order_quantity'} > $data_line[1]) {
							$error_flg             = 1;
							$error_stock_error_flg = 1;
							$error_variation_code  = $item_vari_disp;
							$error_stock_quantity  = $data_line[1];
							$error_order_quantity  = $FORM{'order_quantity'};
						}
						last;
					}
				}
			}
		}
		if ($error_flg) {
			$session_set_flg      = 0;
			$error_hinmei         = $item_name_articles;
			if ($item_vari_disp){
				$variation =~ /(\d{2})(\d{2})/;
				my $variation_h = $2;
				my $variation_v = $1;
				$error_variation_code = 1;
				$error_yoko_title = $item_vari_h_name;
				$error_tate_title = $item_vari_v_name;
				$error_yoko_name  = $item_vari_h_clm[$variation_h];
				$error_tate_name  = $item_vari_v_clm[$variation_v];
			}
		}
	}
	
	if (($FORM{'saleItem_id'} ne '') && ($FORM{'order_quantity'} ne '') && ($session_set_flg != 0)  && ($action eq 'b')) {
		&addSession($order_item_code, $FORM{'order_quantity'}, $session_name);
	}
	$session->expire('+'.$session_timer.'m');
	$session_cart = $session->param($session_name);
	$session_id   = $session->id;
	
	$setcook1 = &setCookie($session_name, $session_id);
	our @LOOP_hash = ();
	our $subtotal_amount;
	our $cart_hit_flg;
	#_配送タイプ表示チェックフラグ
	our @deliveryCheck;
	#_カートを展開
	&cartLoopView1;
	
	if ($error_flg eq '' && $error_on_flg eq '') {
		unless ($cart_hit_flg) {
			$error_on_flg    = 1;
			$empty_error_flg = 1;
		}
	}
	
	$template->param(PURCHASE_LOOP => \@LOOP_hash);
	
	our @LOOP_hash = ();
	our $discount_flg;
	our $cash_discount = 0;
	
	#_割引設定
	&cartLoopCashDiscount;
	$template->param(
		DISCOUNT_LOOP => \@LOOP_hash,
		cash_discount => &convertMoney($cash_discount),
		discount_flg  => $discount_flg,
	);
	
	our @LOOP_hash = ();
	#_配送タイプ
	&cartLoopDelivery(1);
	$template->param(
		DELIVERY_LOOP => \@LOOP_hash,
		delivery_flg  => $_CONFIG_carriage_carriage_disp,
	);
	
	#_戻り先URL生成
	my ($bpage_flg, $bpage_u_flg, $bpage_s_flg, $bpage_g_flg, $bpage_c_flg, $send_keyword)
	 = &cartLoopBpage($FORM{'saleItem_id'}, $FORM{'pid'}, $FORM{'ukeyword'}, $FORM{'skeyword'}, $FORM{'gkeyword'}, $FORM{'ckeyword'});
	
	my $order_form_url;
	if ($_CONFIG_server_ssl_use ne '0' && $_CONFIG_page_view_mode ne 'P') {
		$order_form_url = sprintf('%s/cgi-bin/order_form.cgi', $_CONFIG_server_ssl_site_addr);
	} else {
		$order_form_url = './order_form.cgi';
	}
	
	my $total_amount = $subtotal_amount - $cash_discount;
	$template->param(
		order_form_url        => $order_form_url,
		subtotal_amount       => &convertMoney(int $subtotal_amount),
		tax_string            => $_CONFIG_tax_marking,
		total_amount          => &convertMoney($total_amount),
		msg_flg               => $_CONFIG_order_info_view,
		msg                   => $_CONFIG_order_info_comment,
		ship_free_flg         => $_CONFIG_carriage_free_shipping_set,
		ship_free_if          => &convertMoney($_CONFIG_carriage_free_shipping_set),
		bpage_para            => $bpage_para,
		
		yoko_title            => $error_yoko_title,
		tate_title            => $error_tate_title,
		error_flg             => $error_flg,
		notselected_error_flg => $notselected_error_flg,
		error_on_flg          => $error_on_flg,
		empty_error_flg       => $empty_error_flg,
		
		timeout_error_flg     => $timeout_error_flg,
		max_error_flg         => $max_error_flg,
		max_quantity          => $error_max_quantity,
		order_quantity        => $error_order_quantity,
		stock_error_flg       => $error_stock_error_flg,
		hinmei                => $error_hinmei,
		variation_code        => $error_variation_code,
		yoko_name             => $error_yoko_name,
		tate_name             => $error_tate_name,
		stock_quantity        => $error_stock_quantity,
		incorrect_error_flg   => $incorrect_error_flg,
		agent_error_flg       => $agent_error_flg,
		
		back_page_url         => $back_page_url,
		
		bpage_url             => $bpage_url,
		seid                  => $session_id,
		bpage_flg             => $bpage_flg,
		saleItem_id           => $FORM{'saleItem_id'} . $variation,
		bpage                 => $bpage_url,
		#bpage                 => MODULE::StringUtil::conversionSpecialChar($FORM{'bpage'}),
		pid                   => $FORM{'pid'},
		stype                 => $FORM{'stype'},
		vtype                 => $FORM{'vtype'},
		ukeyword              => MODULE::StringUtil::conversionSpecialChar($FORM{'ukeyword'}),
		skeyword              => MODULE::StringUtil::conversionSpecialChar($FORM{'skeyword'}),
		gkeyword              => MODULE::StringUtil::conversionSpecialChar($FORM{'gkeyword'}),
		ckeyword              => MODULE::StringUtil::conversionSpecialChar($FORM{'ckeyword'}),
		vnum                  => $FORM{'vnum'},
		CONFIG_business_legis_flg         => $_CONFIG_business_legis_flg,
	);
	
	&httpHeadOutput($setcook1 . "\n");
	print $template -> output;



	$session->flush();

	&chmodSessionFile ($_CONFIG_session_dir, $_CONFIG_session_file_header, $session_id);

exit;
