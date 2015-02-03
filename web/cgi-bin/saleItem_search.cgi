#!/usr/bin/perl
use MODULE::Template;
use MODULE::StringUtil;

	use Logger::MyLogger;
	my $logger = Logger::MyLogger->new;
	our $_CONFIG_template_dir;

	# サイト用サブルーチンファイル読み込み
	require './subroutine.pl';
	# サイト用共通変数ファイル読み込み
	require './config_data.cgi';
	&formLoading;
	
	# メイン記事エリア
	my $template  = "";
	
	#_1ページに表示する件数
	my $page_view_num = 10;
	
	# HTMLテンプレート側のIF文では値有無のチェックのみになるので、選択表示形式それぞれの変数を用意する
	my $vtype    = "";
	my $vtype_t  = "";
	my $vtype_i  = "";
	my $vtype_ti = "";
	if ($FORM{'vtype'} eq 'T') {
		$template       = HTML::Template->new(filename => "./$_CONFIG_template_dir/saleItem_search_title.tmp");
		$vtype_t = '1';
		$vtype  = 'T';
	} elsif ($FORM{'vtype'} eq 'I') {
		$template       = HTML::Template->new(filename => "./$_CONFIG_template_dir/saleItem_search_image.tmp");
		$vtype_i = '1';
		$vtype  = 'I';
	} else {
		$template       = HTML::Template->new(filename => "./$_CONFIG_template_dir/saleItem_search.tmp");
		$vtype  = 'TI';
		$vtype_ti = '1';
	}
	
	my $item_keyword_flg		= 0;
	my $item_price_low_flg		= 0;
	my $item_price_up_flg		= 0;
	my $search_item_price_flg	= 0;
	my $item_price_low_view		= 0;
	my $item_price_up_view		= 0;

	my $from_item_price_low = MODULE::StringUtil::conversionSpecialChar($FORM{'item_price_low'});
	my $from_item_price_up  = MODULE::StringUtil::conversionSpecialChar($FORM{'item_price_up'});

	if( $from_item_price_low =~ /^\d+$/ ) {
		$from_item_price_low = $from_item_price_low;
		$item_price_low_view = &convertMoney($from_item_price_low);
	}
	if( $from_item_price_up =~ /^\d+$/ ) {
		$from_item_price_up = $from_item_price_up;
		$item_price_up_view = &convertMoney($from_item_price_up);
	}


	$item_price_low_flg = 1 if ($FORM{'item_price_low'} ne '');
	$item_price_up_flg  = 1 if ($FORM{'item_price_up'} ne '');
	$search_item_price_flg = 1 if ($item_price_low_flg + $item_price_up_flg);
	
	my $item_keyword = $FORM{'item_keyword'};
	$item_keyword = decodUrl($item_keyword);
	my @item_keyword = split(/ |　/, $FORM{'item_keyword'});
	$item_keyword_flg = 1 if (@item_keyword > 0);
	
	my $skeyword = $FORM{'skeyword'};
	$skeyword = decodUrl($skeyword);
	my @skeyword = split(/ |　/, $FORM{'skeyword'});
	
	my $paging_back = "前へ";
	my $paging_next = "次へ";
	# カテゴリ名
	my $item_category_name = '';
	# 自分のURIを設定
	my $bpage = $ENV{'REQUEST_URI'};
	
	my $list_file;

	my $_COOKIE_lid = &getLoginCookie('ID', $ENV{'HTTP_COOKIE'}, $logger);
	my $_COOKIE_lpw = &getLoginCookie('PASSWORD', $ENV{'HTTP_COOKIE'}, $logger);
	#my $_COOKIE_lid = &getLoginCookie('ID');
	#my $_COOKIE_lpw = &getLoginCookie('PASSWORD');
	if ($_COOKIE_lid eq '' && $_COOKIE_lpw eq '') {
		$list_file = './search/item_data.cgi';
	} else {
		$list_file = './search/item_member_data.cgi';
	}
	$category_file = './search/item_category.cgi';
	$group_file    = './search/item_group.cgi';
	open(DATA, $list_file);
	@list_file = <DATA>;
	close(DATA);
	
	# おすすめ順 | 安い順 | 高い順 | かな順 | 新着順
	# ソートに指定があれば並び替える
	my $stype = "";
	my $stype1_flg = "";
	my $stype2_flg = "";
	my $stype3_flg = "";
	my $stype4_flg = "";
	my $stype5_flg = "";
	if ($FORM{'stype'} eq '1') {
		# おすすめ順
		@list_file = sort { (split(/\t/,$b))[10] <=> (split(/\t/,$a))[10] } @list_file;
		$stype1_flg = '1';
		$stype = '1';
	} elsif ($FORM{'stype'} eq '2') {
		# 安い順
		@list_file = sort { (split(/\t/,$a))[6] <=> (split(/\t/,$b))[6] } @list_file;
		$stype2_flg = '1';
		$stype = '2';
	} elsif ($FORM{'stype'} eq '3') {
		# 高い順
		@list_file = sort { (split(/\t/,$b))[6] <=> (split(/\t/,$a))[6] } @list_file;
		$stype3_flg = '1';
		$stype = '3';
	} elsif ($FORM{'stype'} eq '4') {
		# かな順
		@list_file = sort { (split(/\t/,$a))[5] cmp (split(/\t/,$b))[5] } @list_file;
		$stype4_flg = '1';
		$stype = '4';
	} elsif ($FORM{'stype'} eq '5') {
		# 新着順
		@list_file = sort { (split(/\t/,$b))[1] cmp (split(/\t/,$a))[1] } @list_file;
		$stype5_flg = '1';
		$stype = '5';
	} else {
		@list_file = sort { (split(/\t/,$b))[10] <=> (split(/\t/,$a))[10] } @list_file;
		$stype1_flg = '1';
		$stype = '1';
	}
	
	my @hit_data = ();
	MAIN:foreach (@list_file) {
		my @list_line = split(/\t/, $_);
		if ($FORM{'item_price_low'} ne '') {
			if ($FORM{'item_price_low'} > $list_line[7]) {
				next MAIN;
			}
		}
		if ($FORM{'item_price_up'} ne '') {
			if ($FORM{'item_price_up'} < $list_line[7]) {
				next MAIN;
			}
		}
		next if (&checkDate($list_line[8], $list_line[9]));
		$data_file = sprintf('./search/%02d/%02d.cgi', $list_line[2], $list_line[3]);
		open(DATA, $data_file);
		@data_file = <DATA>;
		close(DATA);
		foreach (@data_file) {
			my @data_line = split(/\t/, $_);
			if ($data_line[0] == $list_line[0]) {
				unless (&isSerachCorrespond(\@data_line, \@item_keyword)) {
					next MAIN;
				}
				unless (&isSerachCorrespond(\@data_line, \@skeyword)) {
					next MAIN;
				}
				my $insert_line = join ("\t", @data_line);
				push (@hit_data, $insert_line);
				last;
			}
		}
	}
	my ($search_flg, $narrow_search_flg);
	if (@hit_data == 0) {
		if ($skeyword eq '') {
			$search_flg = 1;
		} else {
			$narrow_search_flg = 1;
		}
	}

	if( $FORM{'vnum'} eq '' ) {
		$FORM{'vnum'} = 1;
	}

#	$FORM{'form_vnum'} = 1 unless ($FORM{'form_vnum'});
	my $paging_all_number   = @hit_data;
	my $paging_start_number = ($FORM{'vnum'} * 10) - 9;
	my $paging_area;
	my $total_page;
	my $paging_end_number;
	my $top_page;
	my $last_page;
	
	if (($paging_start_number + $page_view_num) > $paging_all_number) {
		$paging_end_number = $paging_all_number;
	} else {
		$paging_end_number = $paging_start_number + $page_view_num - 1;
	}
	
	$paging_back = '' if ($FORM{'vnum'} == 1);
	$paging_next = '' if (($paging_start_number + $page_view_num) > $paging_all_number);
	
	$total_page = $paging_all_number / $page_view_num;
	$total_page++ if($total_page > 0 and $total_page != int($total_page));
	$total_page = int $total_page;
	
	#_ページング表示開始ページ値をセット
	if (0 < ($FORM{'vnum'} - 2)) {
		$top_page = $FORM{'vnum'} - 2;
	} else {
		$top_page = 1;
	}
	
	#_ページング表示最終ページ値をセット
	if (($top_page + 4) > $total_page) {
		$last_page = $total_page;
	} else {
		$last_page = $top_page + 4;
	}
	#_最終的に開始ページを調整
	unless ($last_page == ($top_page + 4)) {
		if ($total_page >= 5) {
			$top_page = $last_page - 4;
		} elsif ($total_page >= 4) {
			$top_page = $last_page - 3;
		}
	}
	
	($paging_back, $paging_area, $paging_next) = &pagingOut($paging_back, $paging_next, $FORM{'vnum'}, $total_page, $top_page, $last_page, '', '', $item_keyword, $FORM{'item_price_low'}, $FORM{'item_price_up'}, $skeyword, $FORM{'stype'}, $FORM{'vtype'}, 'sc');


	my $pretax_flg = '';
	my $pretax_sp_flg = '';
	my $pretax_sp_price = '';
	my $pretax_price = '';


	
	my @LOOP_hash = ();
	# <TR>用カウンタ
	my $j = 0;
	for (my $i = $paging_start_number; $i <= $paging_end_number; $i++) {
		$line = $hit_data[$i - 1];
		# 共通ファイルの分割処理を呼び出し
		&itemMainDataSplit;

		
		#_金額を表示用に成型
		$item_including_tax_price = &convertMoney($item_including_tax_price);
		$item_money_sp_price_tax  = &convertMoney($item_money_sp_price_tax);
		
		
		#_税区分
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
		
		

		$tr_start_flg = 0;
		$tr_end_flg   = 0;
		$j++;
		my $hash2 = "";
		
		#_新着フラグがある場合
#		if ($item_new_arrived_flg) {
#			($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = localtime(time - 60 * 60 * 24 * $_CONFIG_order_new_icon_period);
#			$check_date = sprintf ("%04d%02d%02d", $year + 1900, $mon +1, $mday);
#			if ($check_date  > &editDate($item_cmd_insert_day)) {
#				$item_new_arrived_flg = '';
#			}
#		}
		$item_new_arrived_flg = &isWhatsNewIcon($item_new_arrived_flg, $item_cmd_insert_day, $_CONFIG_order_new_icon_period);

		# 描画パターンに応じてテンプレートへ渡す値を変更する
		# タイトルのみ
		if ($FORM{'vtype'} eq 'T') {
			$hash2 = {
				hinmei                  => $item_name_articles,
				saleItem_detailInfo_url => 'saleItem_detailInfo.cgi?cc=' . $item_cmd_category_id . '&gc=' . $item_product_grp_id . '&ic=' . $item_cmd_basic_id,
				order_new_icon          => &checkUri($_CONFIG_order_new_icon, 1),
				order_new_icon_flg      => $item_new_arrived_flg,
				sp_price_icon           => &checkUri($_CONFIG_order_special_price_icon, 1),
				sp_price_icon_flg       => $item_sp_price_flag,
				sp_price                => $item_money_sp_price_tax,
				recom_icon              => &checkUri($_CONFIG_nomination_icon, 1),
				recom_icon_flg          => $item_recom_flg,
				retail_price            => $item_including_tax_price,
				pretax_sp_price         => $pretax_sp_price,
				pretax_sp_flg           => $pretax_sp_flg,
				pretax_flg              => $pretax_flg,
				pretax_price            => $pretax_price,
			};
		# 画像のみ
		} elsif ($FORM{'vtype'} eq 'I') {
			if($j % 3 == 1) {
				$tr_start_flg = "1";
			}
			if($j % 3 == 0 || $j ==( $#hit_data + 1)) {
				$tr_end_flg = "1";
			}
			$hash2 = {
				hinmei                  => $item_name_articles,
				thumbnail_image_url     => &checkUri(&imgCheck($item_cmd_image_uri_nail, $item_cmd_image_uri_main, 'M'), 1),
				saleItem_detailInfo_url => 'saleItem_detailInfo.cgi?cc=' . $item_cmd_category_id . '&gc=' . $item_product_grp_id . '&ic=' . $item_cmd_basic_id,
				order_new_icon          => &checkUri($_CONFIG_order_new_icon, 1),
				order_new_icon_flg      => $item_new_arrived_flg,
				sp_price_icon           => &checkUri($_CONFIG_order_special_price_icon, 1),
				sp_price_icon_flg       => $item_sp_price_flag,
				sp_price                => $item_money_sp_price_tax,
				recom_icon              => &checkUri($_CONFIG_nomination_icon, 1),
				recom_icon_flg          => $item_recom_flg,
				retail_price            => $item_including_tax_price,
				tr_start_flg            => $tr_start_flg,
				tr_end_flg              => $tr_end_flg,
				pretax_sp_price         => $pretax_sp_price,
				pretax_sp_flg           => $pretax_sp_flg,
				pretax_flg              => $pretax_flg,
				pretax_price            => $pretax_price,
			};
		# タイトル＋画像
		} else {
			$hash2 = {
				hinmei                  => $item_name_articles,
				thumbnail_image_url     => &checkUri(&imgCheck($item_cmd_image_uri_nail, $item_cmd_image_uri_main, 'M'), 1),
				saleItem_detailInfo_url => 'saleItem_detailInfo.cgi?cc=' . $item_cmd_category_id . '&gc=' . $item_product_grp_id . '&ic=' . $item_cmd_basic_id,
				order_new_icon          => &checkUri($_CONFIG_order_new_icon, 1),
				order_new_icon_flg      => $item_new_arrived_flg,
				sp_price_icon           => &checkUri($_CONFIG_order_special_price_icon, 1),
				sp_price_icon_flg       => $item_sp_price_flag,
				sp_price                => $item_money_sp_price_tax,
				recom_icon              => &checkUri($_CONFIG_nomination_icon, 1),
				recom_icon_flg          => $item_recom_flg,
				retail_price            => $item_including_tax_price,
				pretax_sp_price         => $pretax_sp_price,
				pretax_sp_flg           => $pretax_sp_flg,
				pretax_flg              => $pretax_flg,
				pretax_price            => $pretax_price,
			};
		}
		push(@LOOP_hash, $hash2);
		if ($page_view_num <= $j) {
			last;
		}
	}
	
	$template->param(LOOP => \@LOOP_hash);
	# ループ外変数
	$template->param(
		item_keyword_dec      => MODULE::StringUtil::conversionSpecialChar($FORM{'item_keyword'}),
		item_keyword          => MODULE::StringUtil::conversionSpecialChar($item_keyword),
		item_price_low        => $from_item_price_low,
		item_price_up         => $from_item_price_up ,
		item_price_low_view   => $item_price_low_view,
		item_price_up_view    => $item_price_up_view ,
		item_keyword_flg      => $item_keyword_flg,
		item_price_low_flg    => $item_price_low_flg,
		item_price_up_flg     => $item_price_up_flg,
		search_item_price_flg => $search_item_price_flg,
		vtype                 => $vtype,
		vtype_t               => $vtype_t,
		vtype_i               => $vtype_i,
		vtype_ti              => $vtype_ti,
		stype                 => $stype,
		stype1_flg            => $stype1_flg,
		stype2_flg            => $stype2_flg,
		stype3_flg            => $stype3_flg,
		stype4_flg            => $stype4_flg,
		stype5_flg            => $stype5_flg,
		skeyworddec           => MODULE::StringUtil::conversionSpecialChar($FORM{'skeyword'}),
		skeyword              => MODULE::StringUtil::conversionSpecialChar($skeyword),
		pageing_start_number  => $paging_start_number,
		pageing_end_number    => $paging_end_number,
		pageing_all_number    => $paging_all_number,
		pageing_area          => $paging_area,
		pageing_back          => $paging_back,
		pageing_next          => $paging_next,
		tax_string            => $_CONFIG_tax_marking,
		vnum                  => $FORM{'vnum'},
		bpage                 => $bpage,
		search_flg            => $search_flg,
		narrow_search_flg     => $narrow_search_flg,
		CONFIG_business_legis_flg         => $_CONFIG_business_legis_flg,
	);
	
	print $_CONFIG_base_head;
	print $template -> output;
