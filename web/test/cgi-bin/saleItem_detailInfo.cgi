#!/usr/bin/perl
use MODULE::Template;
use MODULE::StringUtil;
use CGI::Session qw/-ip_match/;
use CGI::Session::Cleaning;
	
	our $_CONFIG_order_button;
	my $error_flg ='';
	our $_CONFIG_template_dir;

	# サイト用サブルーチンファイル読み込み
	require './subroutine.pl';
	# サイト用共通変数ファイル読み込み
	require './config_data.cgi';
	&formLoading;
	
	# 買い物を続けるから戻ってきた場合の処理(数置き換え)
	&setOrderCount;
	
	my $template = HTML::Template->new(filename => "./$_CONFIG_template_dir/saleItem_detailInfo.tmp");

	# 自分のURIを設定
	#my $bpage = $ENV{'REQUEST_URI'};
	my $bpage = $ENV{'SCRIPT_NAME'} . '?cc=' . $FORM{'cc'} . '&gc=' . $FORM{'gc'} . '&ic=' . $FORM{'ic'};

	my $insert_line;
	
	# 商品チェック処理
	my $list_file;
	$list_file = './search/item_data.cgi';
	$category_file = './search/item_category.cgi';
	$group_file    = './search/item_group.cgi';
	my $hit_lfg = '';
	my $_COOKIE_lid = &getLoginCookie('ID', $ENV{'HTTP_COOKIE'}, $logger);
	my $_COOKIE_lpw = &getLoginCookie('PASSWORD', $ENV{'HTTP_COOKIE'}, $logger);
	if ($_COOKIE_lid eq '' && $_COOKIE_lpw eq '') {
		$list_file = './search/item_data.cgi';
	} else {
		$list_file = './search/item_member_data.cgi';
	}

	open(DATA, $list_file);
	@list_file = <DATA>;
	close(DATA);

	MAIN:foreach (@list_file) {
		my @list_line = split(/\t/, $_);
		if($FORM{'ic'} eq $list_line[0]){
			$hit_lfg= '1';
			last;
		}
	}
	if($hit_lfg ne '1') {
		$hit_lfg = '';
		if ($_COOKIE_lid eq '' && $_COOKIE_lpw eq '') {
			$list_file = './search/item_member_data.cgi';
			open(DATA, $list_file);
			@list_file = <DATA>;
			close(DATA);
			MAIN:foreach (@list_file) {
				my @list_line = split(/\t/, $_);
				if($FORM{'ic'} eq $list_line[0]){
					$hit_lfg= '1';
					last;
				}
			}
			if($hit_lfg eq '1'){
				&pageLoginErr('../');
			} else {
				$error_flg = '1';
			}
		} else {
			$error_flg = '1';
		}
	}

#	my ($search_flg, $narrow_search_flg);
#	if (@hit_data == 0) {
#		if ($skeyword eq '') {
#			$search_flg = 1;
#		} else {
#			$narrow_search_flg = 1;
#		}
#	}




	my $data_file = sprintf('./search/%02d/%02d.cgi', $FORM{'cc'}, $FORM{'gc'});
	open(DATA, $data_file);
	my @data_file = <DATA>;
	close(DATA);
	chomp @data_file;
	
	foreach (@data_file) {
		my @data_line = split(/\t/, $_);
		if ($data_line[0] eq $FORM{'ic'}) {
			$insert_line = $insert_line . join("\t", @data_line);
			last;
		}
	}
	my $val_data_file = sprintf('./search/%02d/%02d_variation.cgi', $FORM{'cc'}, $FORM{'gc'});
	open(DATA, $val_data_file);
	my @val_data_file = <DATA>;
	close(DATA);
	foreach (@val_data_file) {
		my @data_line = split(/\t/, $_);
		if ($data_line[0] eq $FORM{'ic'}) {
			$data_line[0] = '';
			$insert_line = $insert_line . join("\t", @data_line);
			last;
		}
	}
	$line = $insert_line;
	&itemMainDataSplitFull;
	
	my $main_percent;
	my $sub1_percent;
	my $sub2_percent;
	my $main_px;
	my $sub1_px;
	my $sub2_px;
	my $main_flg = '0';
	my $sub1_flg = '0';
	my $sub2_flg = '0';
	my $check_stock_alert = 0;
	
	if ($item_cmd_image_unit_main eq 'X') {
		$main_px      = $item_cmd_image_size_main;
	} else {
		$main_percent = $item_cmd_image_size_main;
		$main_flg = '1';
	}
	if ($item_cmd_image_unit_sub1 eq 'X') {
		$sub1_px      = $item_cmd_image_size_sub1;
	} else {
		$sub1_percent = $item_cmd_image_size_sub1;
		$sub1_flg = '1';
	}
	if ($item_cmd_image_unit_sub2 eq 'X') {
		$sub2_px      = $item_cmd_image_size_sub2;
	} else {
		$sub2_percent = $item_cmd_image_size_sub2;
		$sub2_flg = '1';
	}
	
	
	# 品切れ
	#my $unstocked_flg     = $item_process_out_stock;
	my $unstocked_flg     = 0;
	
	#_税区分
	my $pretax_flg = '';
	my $pretax_sp_flg = '';
	my $pretax_sp_price = '';
	my $pretax_price = '';
	if ($_CONFIG_tax_consumer eq 'O') {
		if ($_CONFIG_tax_indication) {
			$pretax_flg    = '1';
			$pretax_sp_flg = '1';
		}
		$pretax_sp_price = &convertMoney($item_money_sp_price);
		$pretax_price = &convertMoney($item_price);
	} else {
		$pretax_flg = '0';
		$pretax_sp_flg = '0';
		$pretax_sp_price = '';
		$pretax_price = '';
	}
	
	#_新着フラグがある場合
#	if ($item_new_arrived_flg) {
#		($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = localtime(time - 60 * 60 * 24 * $_CONFIG_order_new_icon_period);
#		$check_date = sprintf ("%04d%02d%02d", $year + 1900, $mon +1, $mday);
#		if ($check_date  > &editDate($item_cmd_insert_day)) {
#			$item_new_arrived_flg = '';
#		}
#	}
	$item_new_arrived_flg = &isWhatsNewIcon($item_new_arrived_flg, $item_cmd_insert_day, $_CONFIG_order_new_icon_period);
	
	# レビュー
	my $data_file = sprintf('./search/%02d/%02d_review.cgi', $FORM{'cc'}, $FORM{'gc'});
	open(DATA, $data_file);
	my @data_file = <DATA>;
	close(DATA);
	my $review_flg  = $item_review_disp,
	my $reviewNone_flg = '0';
	my @REVIEW_LOOP = ();
	my @REVIEW_NONE_LOOP = ();
	
	$i = 1;
	foreach (@data_file) {
		my @data_line = split(/\t/, $_);
		if (($data_line[0] eq $FORM{'ic'}) && ($i <= 3)) {
			my $hash1 = {
				review_title   => $data_line[3],
				review_comment => $data_line[4] ,
				review_user    => $data_line[2],
			};
			push(@REVIEW_LOOP, $hash1);
			$i++;
		} elsif (($data_line[0] eq $FORM{'ic'}) && ($i > 3)) {
			my $hash1 = {
				review_title   => $data_line[3],
				review_comment => $data_line[4] ,
				review_user    => $data_line[2],
			};
			push(@REVIEW_NONE_LOOP, $hash1);
			$i++;
		}
		if ($i > 50) {
			last;
		}
	}
	$reviewNone_flg = '1' if (@REVIEW_NONE_LOOP);
	
	# おすすめ
	my $recon_saleItem_flg = '0';
	my @RECOM_LOOP = ();
	for ($i = 1; $i <= 3; $i++) {
		$item_recom_cmd_id[$i] =~ /(\d{2})(\d{2})(\d{8})/;
		next if ($1 eq '00000000' || $1 eq '');
		my $recom_code = $3;
		my $data_file = sprintf('./search/%02d/%02d.cgi', $1, $2);
		open(DATA, $data_file);
		my @data_file = <DATA>;
		close(DATA);
		my $recom_data_line;
		foreach (@data_file) {
			my @data_line = split(/\t/, $_);
			if ($recom_code == $data_line[0]) {
				$recom_data_line = $_;
				last;
			}
		}
		next if ($recom_data_line eq '');
		chomp $recom_data_line;
		my @data_line = split(/\t/, $recom_data_line);
		next if ($data_line[54] eq '0');
		$hash1 = {
			saleItem_detailInfo_url => 'saleItem_detailInfo.cgi?cc=' . $data_line[2] . '&gc=' . $data_line[3] . '&ic=' . $data_line[0],
			thumbnail_image_url     => &checkUri(&imgCheck($data_line[45], $data_line[36], 'M'), 1),
			hinmei                  => $data_line[4],
		};
		push(@RECOM_LOOP, $hash1);
	}
	$recon_saleItem_flg = '1' if (@RECOM_LOOP);
	
	# 関連商品
	my $data_file = sprintf('./search/%02d/%02d.cgi', $FORM{'cc'}, $FORM{'gc'});
	open(DATA, $data_file);
	my @data_file = <DATA>;
	close(DATA);
	
	my $search_file;
	my $_COOKIE_lid = &getLoginCookie('ID');
	my $_COOKIE_lpw = &getLoginCookie('PASSWORD');
	if ($_COOKIE_lid eq '' && $_COOKIE_lpw eq '') {
		$search_file = './search/item_data.cgi';
	} else {
		$search_file = './search/item_member_data.cgi';
	}
	open(DATA, $search_file);
	my @search_file = <DATA>;
	close(DATA);
	
	my @hit_data;
	foreach (@search_file) {
		my @search_line = split(/\t/, $_);
		if ($search_line[2] == $FORM{'cc'} && $search_line[3] == $FORM{'gc'}) {
			foreach (@data_file) {
				my @data_line = split(/\t/, $_);
				if (($search_line[0] == $data_line[0]) && (!&checkDate($data_line[24], $data_line[25]))) {
					push (@hit_data, join ("\t", @data_line));
				}
			}
		}
	}
	my $related_saleItem_flg = '0';
	my @RELATED_LOOP = ();
	$i = 0;
	my @back_rand;
	
	my $rand_lop = 5;
	$rand_lop = (@hit_data - 1) if ((@hit_data - 1) < 5);
	RAND:while ($i < $rand_lop)
	{
		my $num = int (rand (@hit_data));
		foreach (@back_rand) {
			if ($num == $_) {
				next RAND;
			}
		}
		my @data_line = split(/\t/, $hit_data[$num]);
		if ($data_line[0] eq $FORM{'ic'}) {
			next RAND;
		}
		my $tr_start_flg = "";
		my $tr_end_flg   = "";
		if($i == 0 || $i == 3){
			$tr_start_flg = "1";
		}
		# $j==4 は要素の最大とする
		if($i==2 || $i==4){
			$tr_end_flg = "1";
		}
		$hash1 = {
			saleItem_detailInfo_url => 'saleItem_detailInfo.cgi?cc=' . $data_line[2] . '&gc=' . $data_line[3] . '&ic=' . $data_line[0],
			thumbnail_image_url     => &checkUri(&imgCheck($data_line[45], $data_line[36], 'L'), 1),
			hinmei                  => $data_line[4],
			tr_start_flg            => $tr_start_flg,
			tr_end_flg              => $tr_end_flg,
		};
		push(@RELATED_LOOP, $hash1);
		$back_rand[$i] = $num;
		$i++;
	}
	$related_saleItem_flg = '1' if (@RELATED_LOOP);
	
	# 在庫系
	my $stock_total_flg       = $item_stock_amount_disp;
	my $stock_total           = &getTotalStock($item_cmd_category_id, $item_product_grp_id, $item_cmd_basic_id);
	
	my $delivery_type = $item_deli_type_id;
	
	my @variation01 = ();
	my @variation02 = ();
	my @variation03 = ();
	my @variation04 = ();
	my @variation05 = ();
	my @variation06 = ();
	my @variation07 = ();
	my @variation08 = ();
	my @variation09 = ();
	my @variation10 = ();
	
	my $stock_file = sprintf('./search/%02d/%02d_stock.cgi', $item_cmd_category_id, $item_product_grp_id);
	open(DATA, $stock_file);
	@stock_file = <DATA>;
	close(DATA);
	#_在庫設定フラグが偽の場合、在庫数量表示は偽とする
	if ($item_stock_setting_flg eq '0') {
		$item_stock_amount_disp = '0';
	}
	
	# 在庫
	my $stock_alert_check = 0;
	my $stock_total_alert_flg = 0;
	
	my $stock_total_unstocked = 1;
	my $unstocked_flg = '0';
	if (0 >= $stock_total) {
		if ($item_process_out_stock ne '0') {
			$unstocked_flg = '1';
		}
		$stock_total_unstocked = 0;
	} elsif ($item_stock_number_alert > $stock_total) {
		$stock_total_alert_flg = '1';
	}


	@stock_file = sort { (split(/\,/,$a))[0] <=> (split(/\,/,$b))[0] } @stock_file;
	foreach (@stock_file) {
		my $hash_data  = "";
		my @stock_line = split(/\t/, $_);
		$stock_line[0] =~ /(\d{8})(\d{2})(\d{2})/;
		if (($1 eq $item_cmd_basic_id) && ($2 eq '01')) {
			my $unstocked_flg;
			my $stock_alert_flg;
			if ($stock_line[1] < 1) {
				$unstocked_flg   = 1;
			} elsif ($stock_line[1] < $stock_line[2]) {
				$stock_alert_flg   = 1;
				$stock_alert_check = 1;
			}
			#_在庫設定フラグが偽の場合、在庫数比較フラグ無し
			if ($item_stock_setting_flg eq '0') {
				$unstocked_flg   = 0;
				$stock_alert_flg = 0;
			}
			$hash_data = {
				stock_total_flg   => $item_stock_amount_disp,
				unstocked01_flg   => $unstocked_flg,
				saleItem_id       => $1,
				variation_yoko_id => $3,
				stock_quantity    => $stock_line[1],
				stock_alert_flg   => $stock_alert_flg,
			};
			push(@variation01, $hash_data);
		} elsif (($1 eq $item_cmd_basic_id) && ($2 eq '02')) {
			my $unstocked_flg;
			my $stock_alert_flg;
			if ($stock_line[1] < 1) {
				$unstocked_flg   = 1;
			} elsif ($stock_line[1] < $stock_line[2]) {
				$stock_alert_flg   = 1;
				$stock_alert_check = 1;
			}
			#_在庫設定フラグが偽の場合、在庫数比較フラグ無し
			if ($item_stock_setting_flg eq '0') {
				$unstocked_flg   = 0;
				$stock_alert_flg = 0;
			}
			$hash_data = {
				stock_total_flg   => $item_stock_amount_disp,
				unstocked02_flg   => $unstocked_flg,
				saleItem_id       => $1,
				variation_yoko_id => $3,
				stock_quantity    => $stock_line[1],
				stock_alert_flg   => $stock_alert_flg,
			};
			push(@variation02, $hash_data);
		} elsif (($1 eq $item_cmd_basic_id) && ($2 eq '03')) {
			my $unstocked_flg;
			my $stock_alert_flg;
			if ($stock_line[1] < 1) {
				$unstocked_flg   = 1;
			} elsif ($stock_line[1] < $stock_line[2]) {
				$stock_alert_flg   = 1;
				$stock_alert_check = 1;
			}
			#_在庫設定フラグが偽の場合、在庫数比較フラグ無し
			if ($item_stock_setting_flg eq '0') {
				$unstocked_flg   = 0;
				$stock_alert_flg = 0;
			}
			$hash_data = {
				stock_total_flg   => $item_stock_amount_disp,
				unstocked03_flg   => $unstocked_flg,
				saleItem_id       => $1,
				variation_yoko_id => $3,
				stock_quantity    => $stock_line[1],
				stock_alert_flg   => $stock_alert_flg,
			};
			push(@variation03, $hash_data);
		} elsif (($1 eq $item_cmd_basic_id) && ($2 eq '04')) {
			my $unstocked_flg;
			my $stock_alert_flg;
			if ($stock_line[1] < 1) {
				$unstocked_flg   = 1;
			} elsif ($stock_line[1] < $stock_line[2]) {
				$stock_alert_flg   = 1;
				$stock_alert_check = 1;
			}
			#_在庫設定フラグが偽の場合、在庫数比較フラグ無し
			if ($item_stock_setting_flg eq '0') {
				$unstocked_flg   = 0;
				$stock_alert_flg = 0;
			}
			$hash_data = {
				stock_total_flg   => $item_stock_amount_disp,
				unstocked04_flg   => $unstocked_flg,
				saleItem_id       => $1,
				variation_yoko_id => $3,
				stock_quantity    => $stock_line[1],
				stock_alert_flg   => $stock_alert_flg,
			};
			push(@variation04, $hash_data);
		} elsif (($1 eq $item_cmd_basic_id) && ($2 eq '05')) {
			my $unstocked_flg;
			my $stock_alert_flg;
			if ($stock_line[1] < 1) {
				$unstocked_flg   = 1;
			} elsif ($stock_line[1] < $stock_line[2]) {
				$stock_alert_flg   = 1;
				$stock_alert_check = 1;
			}
			#_在庫設定フラグが偽の場合、在庫数比較フラグ無し
			if ($item_stock_setting_flg eq '0') {
				$unstocked_flg   = 0;
				$stock_alert_flg = 0;
			}
			$hash_data = {
				stock_total_flg   => $item_stock_amount_disp,
				unstocked05_flg   => $unstocked_flg,
				saleItem_id       => $1,
				variation_yoko_id => $3,
				stock_quantity    => $stock_line[1],
				stock_alert_flg   => $stock_alert_flg,
			};
			push(@variation05, $hash_data);
		} elsif (($1 eq $item_cmd_basic_id) && ($2 eq '06')) {
			my $unstocked_flg;
			my $stock_alert_flg;
			if ($stock_line[1] < 1) {
				$unstocked_flg   = 1;
			} elsif ($stock_line[1] < $stock_line[2]) {
				$stock_alert_flg   = 1;
				$stock_alert_check = 1;
			}
			#_在庫設定フラグが偽の場合、在庫数比較フラグ無し
			if ($item_stock_setting_flg eq '0') {
				$unstocked_flg   = 0;
				$stock_alert_flg = 0;
			}
			$hash_data = {
				stock_total_flg   => $item_stock_amount_disp,
				unstocked06_flg   => $unstocked_flg,
				saleItem_id       => $1,
				variation_yoko_id => $3,
				stock_quantity    => $stock_line[1],
				stock_alert_flg   => $stock_alert_flg,
			};
			push(@variation06, $hash_data);
		} elsif (($1 eq $item_cmd_basic_id) && ($2 eq '07')) {
			my $unstocked_flg;
			my $stock_alert_flg;
			if ($stock_line[1] < 1) {
				$unstocked_flg   = 1;
			} elsif ($stock_line[1] < $stock_line[2]) {
				$stock_alert_flg   = 1;
				$stock_alert_check = 1;
			}
			#_在庫設定フラグが偽の場合、在庫数比較フラグ無し
			if ($item_stock_setting_flg eq '0') {
				$unstocked_flg   = 0;
				$stock_alert_flg = 0;
			}
			$hash_data = {
				stock_total_flg   => $item_stock_amount_disp,
				unstocked07_flg   => $unstocked_flg,
				saleItem_id       => $1,
				variation_yoko_id => $3,
				stock_quantity    => $stock_line[1],
				stock_alert_flg   => $stock_alert_flg,
			};
			push(@variation07, $hash_data);
		} elsif (($1 eq $item_cmd_basic_id) && ($2 eq '08')) {
			my $unstocked_flg;
			my $stock_alert_flg;
			if ($stock_line[1] < 1) {
				$unstocked_flg   = 1;
			} elsif ($stock_line[1] < $stock_line[2]) {
				$stock_alert_flg   = 1;
				$stock_alert_check = 1;
			}
			#_在庫設定フラグが偽の場合、在庫数比較フラグ無し
			if ($item_stock_setting_flg eq '0') {
				$unstocked_flg   = 0;
				$stock_alert_flg = 0;
			}
			$hash_data = {
				stock_total_flg   => $item_stock_amount_disp,
				unstocked08_flg   => $unstocked_flg,
				saleItem_id       => $1,
				variation_yoko_id => $3,
				stock_quantity    => $stock_line[1],
				stock_alert_flg   => $stock_alert_flg,
			};
			push(@variation08, $hash_data);
		} elsif (($1 eq $item_cmd_basic_id) && ($2 eq '09')) {
			my $unstocked_flg;
			my $stock_alert_flg;
			if ($stock_line[1] < 1) {
				$unstocked_flg   = 1;
			} elsif ($stock_line[1] < $stock_line[2]) {
				$stock_alert_flg   = 1;
				$stock_alert_check = 1;
			}
			#_在庫設定フラグが偽の場合、在庫数比較フラグ無し
			if ($item_stock_setting_flg eq '0') {
				$unstocked_flg   = 0;
				$stock_alert_flg = 0;
			}
			$hash_data = {
				stock_total_flg   => $item_stock_amount_disp,
				unstocked09_flg   => $unstocked_flg,
				saleItem_id       => $1,
				variation_yoko_id => $3,
				stock_quantity    => $stock_line[1],
				stock_alert_flg   => $stock_alert_flg,
			};
			push(@variation09, $hash_data);
		} elsif (($1 eq $item_cmd_basic_id) && ($2 eq '10')) {
			my $unstocked_flg;
			my $stock_alert_flg;
			if ($stock_line[1] < 1) {
				$unstocked_flg   = 1;
			} elsif ($stock_line[1] < $stock_line[2]) {
				$stock_alert_flg   = 1;
				$stock_alert_check = 1;
			}
			#_在庫設定フラグが偽の場合、在庫数比較フラグ無し
			if ($item_stock_setting_flg eq '0') {
				$unstocked_flg   = 0;
				$stock_alert_flg = 0;
			}
			$hash_data = {
				stock_total_flg   => $item_stock_amount_disp,
				unstocked10_flg   => $unstocked_flg,
				saleItem_id       => $1,
				variation_yoko_id => $3,
				stock_quantity    => $stock_line[1],
				stock_alert_flg   => $stock_alert_flg,
			};
			push(@variation10, $hash_data);
		}
	}
	
	# 簡易説明
	my $simple_description_flg = 1 if ($item_cmd_finding ne '');
	
	# 掲載期間
	my $term_posted_flg = 1 if (($item_publishing_beginning ne '') || ($item_publishing_end ne ''));
	my $term_posted_flg = 1 if (($item_publishing_end ne '9998/12/31'));
	#_掲載期間チェック
#	my $error_flg;
	if ($error_flg ne '1') {
		$error_flg = &checkDate($item_publishing_beginning, $item_publishing_end);
	}
	#_公開フラグチェック
	if ($item_opening_to_public eq '0') {
		$error_flg = 1;
	}
	#_販売期間チェック
	my $in_term_saled_flg = 1 unless(&checkDate($item_sales_beginning, $item_sales_term));
	
	# 任意
	my $anyItem_info_1_flg = 1 if ($item_arbitrary_item[1] ne '');
	my $anyItem_info_2_flg = 1 if ($item_arbitrary_item[2] ne '');
	my $anyItem_info_3_flg = 1 if ($item_arbitrary_item[3] ne '');
	my $anyItem_info_4_flg = 1 if ($item_arbitrary_item[4] ne '');
	my $anyItem_info_5_flg = 1 if ($item_arbitrary_item[5] ne '');
	my $anyItem_info_6_flg = 1 if ($item_arbitrary_item[6] ne '');
	my $anyItem_info_7_flg = 1 if ($item_arbitrary_item[7] ne '');
	my $anyItem_info_8_flg = 1 if ($item_arbitrary_item[8] ne '');
	
	#my $stock_total_alert_flg = $check_stock_alert;
	$template->param(
		main_image_url         => &checkUri(&imgCheck($item_cmd_image_uri_main, '', 'L'), 1),
		sub1_image_url         => &checkUri(&imgCheck($item_cmd_image_uri_sub1, '', 'L'), 1),
		sub2_image_url         => &checkUri(&imgCheck($item_cmd_image_uri_sub2, '', 'L'), 1),
		hinmei                 => $item_name_articles,
		item_description       => $item_explanation,
		main_percent           => $main_percent,
		sub1_percent           => $sub1_percent,
		sub2_percent           => $sub2_percent,
		main_px                => $main_px,
		sub1_px                => $sub1_px,
		sub2_px                => $sub2_px,
		main_flg               => $main_flg,
		sub1_flg               => $sub1_flg,
		sub2_flg               => $sub2_flg,
		retail_price           => &convertMoney($item_including_tax_price),
		sp_price_icon          => &checkUri($_CONFIG_order_special_price_icon, 1),
		sp_price_icon_flg      => $item_sp_price_flag,
		sp_price               => &convertMoney($item_money_sp_price_tax),
		recom_icon             => &checkUri($_CONFIG_nomination_icon, 1),
		recom_icon_flg         => $item_recom_flg,
		order_new_icon_flg     => $item_new_arrived_flg,
		order_new_icon         => &checkUri($_CONFIG_order_new_icon, 1),
		delivery_type          => &deliveryOut($item_deli_type_id),
		simple_description_flg => $simple_description_flg,
		simple_description     => $item_cmd_finding,
		term_posted_flg        => $term_posted_flg,
		term_posted_start      => $item_publishing_beginning,
		term_posted_fin        => $item_publishing_end,
		anyItem_info_1_flg     => $anyItem_info_1_flg,
		anyItem_info_1_name    => $_CONFIG_item_option_title[1],
		anyItem_info_1         => $item_arbitrary_item[1],
		anyItem_info_2_flg     => $anyItem_info_2_flg,
		anyItem_info_2_name    => $_CONFIG_item_option_title[2],
		anyItem_info_2         => $item_arbitrary_item[2],
		anyItem_info_3_flg     => $anyItem_info_3_flg,
		anyItem_info_3_name    => $_CONFIG_item_option_title[3],
		anyItem_info_3         => $item_arbitrary_item[3],
		anyItem_info_4_flg     => $anyItem_info_4_flg,
		anyItem_info_4_name    => $_CONFIG_item_option_title[4],
		anyItem_info_4         => $item_arbitrary_item[4],
		anyItem_info_5_flg     => $anyItem_info_5_flg,
		anyItem_info_5_name    => $_CONFIG_item_option_title[5],
		anyItem_info_5         => $item_arbitrary_item[5],
		anyItem_info_6_flg     => $anyItem_info_6_flg,
		anyItem_info_6_name    => $_CONFIG_item_option_title[6],
		anyItem_info_6         => $item_arbitrary_item[6],
		anyItem_info_7_flg     => $anyItem_info_7_flg,
		anyItem_info_7_name    => $_CONFIG_item_option_title[7],
		anyItem_info_7         => $item_arbitrary_item[7],
		anyItem_info_8_flg     => $anyItem_info_8_flg,
		anyItem_info_8_name    => $_CONFIG_item_option_title[8],
		anyItem_info_8         => $item_arbitrary_item[8],
		variation_code         => $item_vari_disp,
		variation01            => \@variation01,
		variation02            => \@variation02,
		variation03            => \@variation03,
		variation04            => \@variation04,
		variation05            => \@variation05,
		variation06            => \@variation06,
		variation07            => \@variation07,
		variation08            => \@variation08,
		variation09            => \@variation09,
		variation10            => \@variation10,
		yoko1                  => $item_vari_h_clm[1],
		yoko2                  => $item_vari_h_clm[2],
		yoko3                  => $item_vari_h_clm[3],
		yoko4                  => $item_vari_h_clm[4],
		yoko5                  => $item_vari_h_clm[5],
		yoko6                  => $item_vari_h_clm[6],
		yoko7                  => $item_vari_h_clm[7],
		yoko8                  => $item_vari_h_clm[8],
		yoko9                  => $item_vari_h_clm[9],
		yoko10                 => $item_vari_h_clm[10],
		tate1                  => $item_vari_v_clm[1],
		tate2                  => $item_vari_v_clm[2],
		tate3                  => $item_vari_v_clm[3],
		tate4                  => $item_vari_v_clm[4],
		tate5                  => $item_vari_v_clm[5],
		tate6                  => $item_vari_v_clm[6],
		tate7                  => $item_vari_v_clm[7],
		tate8                  => $item_vari_v_clm[8],
		tate9                  => $item_vari_v_clm[9],
		tate10                 => $item_vari_v_clm[10],
		yoko_title             => $item_vari_h_name,
		tate_title             => $item_vari_v_name,
		unstocked_comment      => $item_comment_out_stock,
		REVIEW_LOOP            => \@REVIEW_LOOP,
		review_flg             => $item_review_disp,
		error_flg              => $error_flg,
		top_url                => '../',
		reviewNone_flg         => $reviewNone_flg,
		REVIEW_NONE_LOOP       => \@REVIEW_NONE_LOOP,
		recon_saleItem_flg     => $recon_saleItem_flg,
		RECOM_LOOP             => \@RECOM_LOOP,
		related_saleItem_flg   => $related_saleItem_flg,
		RELATED_LOOP           => \@RELATED_LOOP,
		tax_string             => $_CONFIG_tax_marking,
		order_button           => $_CONFIG_order_button,
		bpage                  => $bpage,
		saleItem_id            => sprintf ('%02d%02d%08d', $FORM{'cc'}, $FORM{'gc'}, $FORM{'ic'}),
		saleItem_id_sub        => sprintf ('%08d', $FORM{'ic'}),
		in_term_saled_flg      => $in_term_saled_flg,
		stock_total_alert_flg  => $stock_total_alert_flg,
		stock_total_flg        => $item_stock_amount_disp,
		stock_total            => $stock_total,
		pretax_sp_flg          => $pretax_sp_flg,
		pretax_price           => $pretax_price,
		pretax_flg             => $pretax_flg,
		pretax_sp_price        => $pretax_sp_price,
		unstocked_flg          => $unstocked_flg,
		stock_total_unstocked  => $stock_total_unstocked,
		stock_alert_flg        => $stock_alert_check,
		item_stock_setting_flg => $item_stock_setting_flg,
		CONFIG_business_legis_flg         => $_CONFIG_business_legis_flg,
	);
	
	print $_CONFIG_base_head;
	print $template -> output;
