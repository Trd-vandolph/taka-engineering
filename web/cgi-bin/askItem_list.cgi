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
	
	# HTMLテンプレート側のIF文では値有無のチェックのみになるので、選択表示形式それぞれの変数を用意する
	my $vtype    = "";
	my $vtype_t  = "";
	my $vtype_i  = "";
	my $vtype_ti = "";
	
	# 絞り込み検索
	my $akeyword = $FORM{'akeyword'};
	$akeyword = decodUrl($akeyword);
	my @akeyword = split(/ |　/, $FORM{'akeyword'});
	
	# 自分のURIを設定
	my $bpage = $ENV{'REQUEST_URI'};
	
	#_認証ページのチェック
	$pagelink_file = './module_pageLink.cgi';
	open(DATA, $pagelink_file);
	@pagelink_file = <DATA>;
	close(DATA);
	foreach (@pagelink_file) {
		my @pagelink_line = split(/\t/, $_);
		if ($pagelink_line[0] eq $FORM{'pid'}) {
			if ($pagelink_line[6] ne '0') {
				#my $_COOKIE_lid = &getCookie('ID');
				#my $_COOKIE_lpw = &getCookie('PASSWORD');
				my $_COOKIE_lid = &getLoginCookie('ID', $ENV{'HTTP_COOKIE'}, $logger);
				my $_COOKIE_lpw = &getLoginCookie('PASSWORD', $ENV{'HTTP_COOKIE'}, $logger);
				if ($_COOKIE_lid eq '' && $_COOKIE_lpw eq '') {
					&pageLoginErr('../');
				}
			}
			last;
		}
	}
	
	$config_file   = './search/user_askItem_config_data.cgi';
	$list_file     = sprintf('./search/user_askItem_%d.cgi', $FORM{'pid'});
	open(DATA, $config_file);
	@config_file = <DATA>;
	close(DATA);
	open(DATA, $list_file);
	@list_file = <DATA>;
	close(DATA);
	
	my @config_data;
	foreach (@config_file) {
		chomp $_;
		my @config_line = split(/\t/, $_);
		if ($config_line[0] == $FORM{'pid'}) {
			@config_data = @config_line;
			last;
		}
	}
	
	my $stype1_flg = "";
	my $stype2_flg = "";
	my $stype3_flg = "";
	my $stype4_flg = "";
	my $stype5_flg = "";
	
	if ($FORM{'stype'} eq '1') {
		# おすすめ順
		@list_file = sort { (split(/\t/,$b))[12] <=> (split(/\t/,$a))[12] } @list_file;
		$stype1_flg = '1';
	} elsif ($FORM{'stype'} eq '2') {
		# 安い順
		@list_file = sort { (split(/\t/,$a))[8] <=> (split(/\t/,$b))[8] } @list_file;
		$stype2_flg = '1';
	} elsif ($FORM{'stype'} eq '3') {
		# 高い順
		@list_file = sort { (split(/\t/,$b))[8] <=> (split(/\t/,$a))[8] } @list_file;
		$stype3_flg = '1';
	} elsif ($FORM{'stype'} eq '4') {
		# かな順
		@list_file = sort { (split(/\t/,$a))[7] cmp (split(/\t/,$b))[7] } @list_file;
		$stype4_flg = '1';
	} elsif ($FORM{'stype'} eq '5') {
		# 新着順
		@list_file = sort { (split(/\t/,$b))[3] cmp (split(/\t/,$a))[3] } @list_file;
		$stype5_flg = '1';
	} else {
		@list_file = sort { (split(/\t/,$a))[1] <=> (split(/\t/,$b))[1] } @list_file;
	}
	
	my @hit_data = ();
	MAIN:foreach (@list_file) {
		my @list_line = split(/\t/, $_);
		next if (&checkDate($list_line[10], $list_line[11]));
		my $insert_line1 = '';
		my $insert_line2 = '';
		my $data_file = sprintf('./search/%02d/%02d.cgi', $list_line[4], $list_line[5]);
		open(DATA, $data_file);
		@data_file = <DATA>;
		close(DATA);
		chomp @data_file;
		foreach (@data_file) {
			my @data_line = split(/\t/, $_);
			if ($data_line[0] == $list_line[2]) {
				unless (&isSerachCorrespond(\@data_line, \@akeyword)) {
					next MAIN;
				}
				$insert_line1 = join("\t", @data_line);
				last;
			}
		}
		my $data_file = sprintf('./search/%02d/%02d_variation.cgi', $list_line[4], $list_line[5]);
		open(DATA, $data_file);
		@data_file = <DATA>;
		close(DATA);
		foreach (@data_file) {
			my @data_line = split(/\t/, $_);
			if ($data_line[0] == $list_line[2]) {
				$insert_line2 = join("\t", @data_line);
				last;
			}
		}
		push (@hit_data, $insert_line1 . $insert_line2) if ($insert_line1 ne '');
	}
	my $narrow_search_flg;
	my $no_item_flg;
	if (@hit_data == 0) {
		if ($akeyword eq '') {
			$no_item_flg = 1;
			$narrow_search_flg = 1;
			#&apricationErr('../');
		} else {
			$narrow_search_flg = 1;
		}
	}

	if ($FORM{'vtype'} eq '') {
		if ($config_data[3]) {
			$FORM{'vtype'} = 'TI';
		} else {
			$FORM{'vtype'} = 'T';
		}
	}
	
	if( $FORM{'vnum'} eq '' ) {
		$FORM{'vnum'} = 1;
	}
	#_1ページに表示する件数
	my $page_view_num = $config_data[20];
	my $paging_back   = $config_data[22];
	my $paging_next   = $config_data[21];
#	$FORM{'vnum'} = 1 unless ($FORM{'vnum'});
	my $paging_all_number   = @hit_data;
	my $paging_start_number = ($FORM{'vnum'} * $page_view_num) - ($page_view_num - 1);
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
	
	if ($paging_all_number ne '' && $page_view_num ne '') {
		$total_page = $paging_all_number / $page_view_num;
	}
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
	
	($paging_back, $paging_area, $paging_next) = &pagingOut($paging_back, $paging_next, $FORM{'vnum'}, $total_page, $top_page, $last_page, $FORM{'pid'}, '', '', '', '', $akeyword, $FORM{'stype'}, $FORM{'vtype'}, 'ac');
	
	# この頁の任意項目表示フラグを取得
	my $i = 1;
	my @arbitrary_item_num;
	my @arbitrary_item_name;
	for (my $j = 9; $j <= 19; $j++) {
		if ($config_data[$j] != 0) {
			if ($j == 9) {
				$arbitrary_item_name[$i] = '簡易説明';
				$arbitrary_item_num[$i]  = 'D1';
			} elsif ($j == 10) {
				$arbitrary_item_name[$i] = '説明';
				$arbitrary_item_num[$i]  = 'D2';
			} elsif ($j == 11) {
				$arbitrary_item_name[$i] = '掲載期間';
				$arbitrary_item_num[$i]  = 'D3';
			} elsif ($j >= 12) {
				$arbitrary_item_name[$i] = $_CONFIG_item_option_title[$j - 11];
				$arbitrary_item_num[$i]  = $j - 11;
			}
			$i++;
		}
	}
	#my $i = 1;
	#my @arbitrary_item_num;
	#my @arbitrary_item_name;
	#for (my $j = 13; $j <= 20; $j++) {
	#	if ($config_data[$j] != 0) {
	#		$arbitrary_item_name[$i] = $_CONFIG_item_option_title[$i];
	#		$arbitrary_item_num[$i]  = $j - 12;
	#		$i++;
	#	}
	#}
	
#	if ($FORM{'vtype'} eq '') {
#		if ($config_data[3]) {
#			$FORM{'vtype'} = 'TI';
#		} else {
#			$FORM{'vtype'} = 'T';
#		}
#	}
	if($config_data[1] eq '1') {
		# 1→大
		if ($FORM{'vtype'} eq 'T') {
			$template       = HTML::Template->new(filename => "./$_CONFIG_template_dir/askItem_list_large_title.tmp");
			$vtype_t = '1';
		} elsif ($FORM{'vtype'} eq 'I') {
			$template       = HTML::Template->new(filename => "./$_CONFIG_template_dir/askItem_list_large_image.tmp");
			$vtype_i = '1';
		} else {
			$template       = HTML::Template->new(filename => "./$_CONFIG_template_dir/askItem_list_large.tmp");
			$vtype_ti = '1';
		}
	} elsif($config_data[1] eq '2') {
		# 2→中
		if ($FORM{'vtype'} eq 'T') {
			$template       = HTML::Template->new(filename => "./$_CONFIG_template_dir/askItem_list_middle_title.tmp");
			$vtype_t = '1';
		} elsif ($FORM{'vtype'} eq 'I') {
			$template       = HTML::Template->new(filename => "./$_CONFIG_template_dir/askItem_list_middle_image.tmp");
			$vtype_i = '1';
		} else {
			$template       = HTML::Template->new(filename => "./$_CONFIG_template_dir/askItem_list_middle.tmp");
			$vtype_ti = '1';
		}
	} elsif($config_data[1] eq '3') {
		# 3→小
		if ($FORM{'vtype'} eq 'T') {
			$template       = HTML::Template->new(filename => "./$_CONFIG_template_dir/askItem_list_small_title.tmp");
			$vtype_t = '1';
		} elsif ($FORM{'vtype'} eq 'I') {
			$template       = HTML::Template->new(filename => "./$_CONFIG_template_dir/askItem_list_small_image.tmp");
			$vtype_i = '1';
		} else {
			$template       = HTML::Template->new(filename => "./$_CONFIG_template_dir/askItem_list_small.tmp");
			$vtype_ti = '1';
		}
	}
	
	my @LOOP_hash = ();
	# <TR>用カウンタ
	my $lop = 0;
	for (my $i = $paging_start_number; $i <= $paging_end_number; $i++) {
		$lop++;
		$line = $hit_data[$i - 1];
		# 共通ファイルの分割処理を呼び出し
		&itemMainDataSplitFull;

		
		my $tr_start_flg = "";
		my $tr_end_flg   = "";
		
		#_販売期間を調べる
		my $in_term_saled_flg = &checkDate($item_sales_beginning, $item_sales_term);
		
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
		
		#_新着フラグがある場合
		#if ($item_new_arrived_flg) {
		#	($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = localtime(time - 60 * 60 * 24 * $_CONFIG_order_new_icon_period);
		#	$check_date = sprintf ("%04d%02d%02d", $year + 1900, $mon +1, $mday);
		#	if ($check_date  > &editDate($item_cmd_insert_day)) {
		#		$item_new_arrived_flg = '';
		#	}
		#}
		$item_new_arrived_flg = &isWhatsNewIcon($item_new_arrived_flg, $item_cmd_insert_day, $_CONFIG_order_new_icon_period);		# 任意項目設定

		my @SALEITEM_INFO_LOOP = ();
		my $item_description;
		my $hash3 = "";
		for (my $j = 9; $j <= 19; $j++) {
			if ($config_data[$j] != 0) {
				if ($j == 9) {
					$hash3 = {
						saleItem_info_name => '簡易説明',
						saleItem_info      => $item_cmd_finding,
					};
					push(@SALEITEM_INFO_LOOP, $hash3);
				} elsif ($j == 10) {
					$item_description = $item_explanation;
					#$hash3 = {
					#	saleItem_info_name => '説明',
					#	saleItem_info      => $item_explanation,
					#};
					#push(@SALEITEM_INFO_LOOP, $hash3);
				} elsif ($j == 11) {
					$hash3 = {
						saleItem_info_name => '掲載期間',
						saleItem_info      => $item_publishing_beginning . '〜' . $item_publishing_end,
					};
					push(@SALEITEM_INFO_LOOP, $hash3);
				} elsif ($j >= 12) {
					next unless $_CONFIG_item_option_title[$j - 11] && $item_arbitrary_item[$j - 11];
					$hash3 = {
						saleItem_info_name => $_CONFIG_item_option_title[$j - 11],
						saleItem_info      => $item_arbitrary_item[$j - 11],
					};
					push(@SALEITEM_INFO_LOOP, $hash3);
				}
			}
		}
		#for ($j = 1; $j <= 8; $j++) {
		#	if ($item_arbitrary_item[$j]) {
		#		$hash3 = {
		#			saleItem_info_name => $_CONFIG_item_option_title[$j],
		#			saleItem_info      => $item_arbitrary_item[$j],
		#		};
		#		push(@SALEITEM_INFO_LOOP, $hash3);
		#	}
		#}
		
		my $delivery_type = $item_deli_type_id;
		
		# バリエーション
		my $variation_code = 1 if ($item_vari_disp != 0);
		
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
		

		# 在庫
		my $stock_total_unstocked = '';
		if(0 < $item_stock_total) {
			$stock_total_unstocked = '1';
		}

		my $stock_file = sprintf('./search/%02d/%02d_stock.cgi', $item_cmd_category_id, $item_product_grp_id);
		open(DATA, $stock_file);
		@stock_file = <DATA>;
		close(DATA);
		@stock_file = sort { (split(/\,/,$a))[0] <=> (split(/\,/,$b))[0] } @stock_file;
		foreach (@stock_file) {
			my $hash_data = "";
			my @stock_line = split(/\t/, $_);
			$stock_line[0] =~ /(\d{8})(\d{2})(\d{2})/;
			if (($1 eq $item_cmd_basic_id) && ($2 eq '01')) {
				my $unstocked_flg   = 1 if ($stock_line[1] < 1);
				my $stock_alert_flg = 1 if ($stock_line[1] < $stock_line[2]);
				$hash_data = {
					unstocked01_flg   => $unstocked_flg,
				};
				push(@variation01, $hash_data);
			} elsif (($1 eq $item_cmd_basic_id) && ($2 eq '02')) {
				my $unstocked_flg   = 1 if ($stock_line[1] < 1);
				my $stock_alert_flg = 1 if ($stock_line[1] < $stock_line[2]);
				$hash_data = {
					unstocked02_flg   => $unstocked_flg,
				};
				push(@variation02, $hash_data);
			} elsif (($1 eq $item_cmd_basic_id) && ($2 eq '03')) {
				my $unstocked_flg   = 1 if ($stock_line[1] < 1);
				my $stock_alert_flg = 1 if ($stock_line[1] < $stock_line[2]);
				$hash_data = {
					unstocked03_flg   => $unstocked_flg,
				};
				push(@variation03, $hash_data);
			} elsif (($1 eq $item_cmd_basic_id) && ($2 eq '04')) {
				my $unstocked_flg   = 1 if ($stock_line[1] < 1);
				my $stock_alert_flg = 1 if ($stock_line[1] < $stock_line[2]);
				$hash_data = {
					unstocked04_flg   => $unstocked_flg,
				};
				push(@variation04, $hash_data);
			} elsif (($1 eq $item_cmd_basic_id) && ($2 eq '05')) {
				my $unstocked_flg   = 1 if ($stock_line[1] < 1);
				my $stock_alert_flg = 1 if ($stock_line[1] < $stock_line[2]);
				$hash_data = {
					unstocked05_flg   => $unstocked_flg,
				};
				push(@variation05, $hash_data);
			} elsif (($1 eq $item_cmd_basic_id) && ($2 eq '06')) {
				my $unstocked_flg   = 1 if ($stock_line[1] < 1);
				my $stock_alert_flg = 1 if ($stock_line[1] < $stock_line[2]);
				$hash_data = {
					unstocked06_flg   => $unstocked_flg,
				};
				push(@variation06, $hash_data);
			} elsif (($1 eq $item_cmd_basic_id) && ($2 eq '07')) {
				my $unstocked_flg   = 1 if ($stock_line[1] < 1);
				my $stock_alert_flg = 1 if ($stock_line[1] < $stock_line[2]);
				$hash_data = {
					unstocked07_flg   => $unstocked_flg,
				};
				push(@variation07, $hash_data);
			} elsif (($1 eq $item_cmd_basic_id) && ($2 eq '08')) {
				my $unstocked_flg   = 1 if ($stock_line[1] < 1);
				my $stock_alert_flg = 1 if ($stock_line[1] < $stock_line[2]);
				$hash_data = {
					unstocked08_flg   => $unstocked_flg,
				};
				push(@variation08, $hash_data);
			} elsif (($1 eq $item_cmd_basic_id) && ($2 eq '09')) {
				my $unstocked_flg   = 1 if ($stock_line[1] < 1);
				my $stock_alert_flg = 1 if ($stock_line[1] < $stock_line[2]);
				$hash_data = {
					unstocked09_flg   => $unstocked_flg,
				};
				push(@variation09, $hash_data);
			} elsif (($1 eq $item_cmd_basic_id) && ($2 eq '10')) {
				my $unstocked_flg   = 1 if ($stock_line[1] < 1);
				my $stock_alert_flg = 1 if ($stock_line[1] < $stock_line[2]);
				$hash_data = {
					unstocked10_flg   => $unstocked_flg,
				};
				push(@variation10, $hash_data);
			}
		}
		my $detailInfo_url = sprintf('askItem_detail.cgi?cc=%s&gc=%s&ic=%s&pid=%s&lid=%s&lpw=%s&pl=%s&il=%s', $item_cmd_category_id, $item_product_grp_id, $item_cmd_basic_id, $FORM{'pid'}, $_COOKIE_lid, $_COOKIE_lpw, $_COOKIE_pl, $_COOKIE_il);
		my $hash2 = "";
		if($config_data[1] eq '1') {
			# 1→大
			# 描画パターンに応じてテンプレートへ渡す値を変更する
			# タイトルのみ
			if ($FORM{'vtype'} eq 'T') {
				$hash2 = {
					hinmei                  => $item_name_articles,
					saleItem_detailInfo_url => $detailInfo_url,
					order_new_icon          => &checkUri($_CONFIG_order_new_icon, 1),
					#order_new_icon_flg      => $order_new_icon_flg,
					order_new_icon_flg      => $item_new_arrived_flg,
					sp_price_icon           => &checkUri($_CONFIG_order_special_price_icon, 1),
					sp_price_icon_flg       => $item_sp_price_flag,
					#sp_price_icon_flg       => $sp_price_icon_flg,
					recom_icon              => &checkUri($_CONFIG_nomination_icon, 1),
					recom_icon_flg          => $item_recom_flg,
					pid                     => $FORM{'pid'},
					SALEITEM_INFO_LOOP      => \@SALEITEM_INFO_LOOP,
					stock_total_flg         => $item_stock_amount_disp,
					stock_total_unstocked   => $stock_total_unstocked,
					yoko1                   => $item_vari_h_clm[1],
					yoko2                   => $item_vari_h_clm[2],
					yoko3                   => $item_vari_h_clm[3],
					yoko4                   => $item_vari_h_clm[4],
					yoko5                   => $item_vari_h_clm[5],
					yoko6                   => $item_vari_h_clm[6],
					yoko7                   => $item_vari_h_clm[7],
					yoko8                   => $item_vari_h_clm[8],
					yoko9                   => $item_vari_h_clm[9],
					yoko10                  => $item_vari_h_clm[10],
					tate1                   => $item_vari_v_clm[1],
					tate2                   => $item_vari_v_clm[2],
					tate3                   => $item_vari_v_clm[3],
					tate4                   => $item_vari_v_clm[4],
					tate5                   => $item_vari_v_clm[5],
					tate6                   => $item_vari_v_clm[6],
					tate7                   => $item_vari_v_clm[7],
					tate8                   => $item_vari_v_clm[8],
					tate9                   => $item_vari_v_clm[9],
					tate10                  => $item_vari_v_clm[10],
					variation_code          => $variation_code,
					variation01             => \@variation01,
					variation02             => \@variation02,
					variation03             => \@variation03,
					variation04             => \@variation04,
					variation05             => \@variation05,
					variation06             => \@variation06,
					variation07             => \@variation07,
					variation08             => \@variation08,
					variation09             => \@variation09,
					variation10             => \@variation10,
					yoko_title              => $item_vari_h_name,
					tate_title              => $item_vari_v_name,
					retail_price            => $item_including_tax_price,
					sp_price                => $item_money_sp_price_tax,
					delivery_type           => &deliveryOut($delivery_type),
					pretax_sp_price         => $pretax_sp_price,
					pretax_sp_flg           => $pretax_sp_flg,
					pretax_flg              => $pretax_flg,
					pretax_price            => $pretax_price,
					item_description        => $item_description,
				};
			# 画像のみ
			} elsif ($FORM{'vtype'} eq 'I') {
				if($lop % 2 == 1) {
					$tr_start_flg = "1";
				}
				if($lop % 2 == 0 || $lop ==( $#MAIN + 1)) {
					$tr_end_flg = "1";
				}
				$hash2 = {
					hinmei                  => $item_name_articles,
					thumbnail_image_url     => &checkUri(&imgCheck($item_cmd_image_uri_nail, $item_cmd_image_uri_main, 'L'), 1),
					saleItem_detailInfo_url => $detailInfo_url,
					order_new_icon          => &checkUri($_CONFIG_order_new_icon, 1),
					#order_new_icon_flg      => $order_new_icon_flg,
					order_new_icon_flg      => $item_new_arrived_flg,
					sp_price_icon           => &checkUri($_CONFIG_order_special_price_icon, 1),
					sp_price_icon_flg       => $item_sp_price_flag,
					#sp_price_icon_flg       => $sp_price_icon_flg,
					recom_icon              => &checkUri($_CONFIG_nomination_icon, 1),
					recom_icon_flg          => $item_recom_flg,
					pid                     => $FORM{'pid'},
					tr_start_flg            => $tr_start_flg,
					tr_end_flg              => $tr_end_flg,
					retail_price            => $item_including_tax_price,
					sp_price                => $item_money_sp_price_tax,
					pretax_sp_price         => $pretax_sp_price,
					pretax_sp_flg           => $pretax_sp_flg,
					pretax_flg              => $pretax_flg,
					pretax_price            => $pretax_price,
				};
			# タイトル＋画像
			} else {
				$hash2 = {
					hinmei                  => $item_name_articles,
					thumbnail_image_url     => &checkUri(&imgCheck($item_cmd_image_uri_nail, $item_cmd_image_uri_main, 'L'), 1),
					saleItem_detailInfo_url => $detailInfo_url,
					order_new_icon          => &checkUri($_CONFIG_order_new_icon, 1),
					#order_new_icon_flg      => $order_new_icon_flg,
					order_new_icon_flg      => $item_new_arrived_flg,
					sp_price_icon           => &checkUri($_CONFIG_order_special_price_icon, 1),
					#sp_price_icon_flg       => $sp_price_icon_flg,
					sp_price_icon_flg       => $item_sp_price_flag,
					recom_icon              => &checkUri($_CONFIG_nomination_icon, 1),
					recom_icon_flg          => $item_recom_flg,
					pid                     => $FORM{'pid'},
					SALEITEM_INFO_LOOP      => \@SALEITEM_INFO_LOOP,
					stock_total_flg         => $item_stock_amount_disp,
					stock_total_unstocked   => $stock_total_unstocked,
					yoko1                   => $item_vari_h_clm[1],
					yoko2                   => $item_vari_h_clm[2],
					yoko3                   => $item_vari_h_clm[3],
					yoko4                   => $item_vari_h_clm[4],
					yoko5                   => $item_vari_h_clm[5],
					yoko6                   => $item_vari_h_clm[6],
					yoko7                   => $item_vari_h_clm[7],
					yoko8                   => $item_vari_h_clm[8],
					yoko9                   => $item_vari_h_clm[9],
					yoko10                  => $item_vari_h_clm[10],
					tate1                   => $item_vari_v_clm[1],
					tate2                   => $item_vari_v_clm[2],
					tate3                   => $item_vari_v_clm[3],
					tate4                   => $item_vari_v_clm[4],
					tate5                   => $item_vari_v_clm[5],
					tate6                   => $item_vari_v_clm[6],
					tate7                   => $item_vari_v_clm[7],
					tate8                   => $item_vari_v_clm[8],
					tate9                   => $item_vari_v_clm[9],
					tate10                  => $item_vari_v_clm[10],
					variation_code          => $variation_code,
					variation01             => \@variation01,
					variation02             => \@variation02,
					variation03             => \@variation03,
					variation04             => \@variation04,
					variation05             => \@variation05,
					variation06             => \@variation06,
					variation07             => \@variation07,
					variation08             => \@variation08,
					variation09             => \@variation09,
					variation10             => \@variation10,
					yoko_title              => $item_vari_h_name,
					tate_title              => $item_vari_v_name,
					retail_price            => $item_including_tax_price,
					sp_price                => $item_money_sp_price_tax,
					delivery_type           => &deliveryOut($delivery_type),
					pretax_sp_price         => $pretax_sp_price,
					pretax_sp_flg           => $pretax_sp_flg,
					pretax_flg              => $pretax_flg,
					pretax_price            => $pretax_price,
					item_description        => $item_description,
				};
			}
		} elsif($config_data[1] eq '2') {
			# 2→中
			# 描画パターンに応じてテンプレートへ渡す値を変更する
			# タイトルのみ
			#my $item_description_flg = "1";
			#my $item_description = $item_cmd_finding;
			#my $saleItem_info_1_flg ="0";
			#my $saleItem_info_2_flg ="0";
			#my $saleItem_info_3_flg ="0";
			#
			## 任意項目
			#if($i % 4 == 0 ) {
			#	$saleItem_info_1_flg = "0";
			#}
			#if($i % 4 == 1) {
			#	$saleItem_info_1_flg = "1";
			#}
			#if($i % 4 == 2) {
			#	$saleItem_info_1_flg = "1";
			#	$saleItem_info_2_flg = "1";
			#}
			#if($i % 4 == 3) {
			#	$saleItem_info_1_flg = "1";
			#	$saleItem_info_2_flg = "1";
			#	$saleItem_info_3_flg = "1";
			#}
			my $item_description_flg;
			my $item_description;
			my @saleItem_info;
			my @view_arbitrary_item_name;
			for ($l = 1; $l <= 3; $l++) {
				if ($arbitrary_item_num[$l] eq 'D1') {
					$item_description_flg = "1";
					$item_description     = $item_cmd_finding;
					$view_arbitrary_item_name[$l] = '';
				} elsif  ($arbitrary_item_num[$l] eq 'D2') {
					$saleItem_info[$l] = $item_explanation;
					$view_arbitrary_item_name[$l] = $arbitrary_item_name[$l];
				} elsif ($arbitrary_item_num[$l] eq 'D3') {
					$saleItem_info[$l] = $item_publishing_beginning . '〜' . $item_publishing_end;
					$view_arbitrary_item_name[$l] = $arbitrary_item_name[$l];
				} else {
					$saleItem_info[$l] = $item_arbitrary_item[$arbitrary_item_num[$l]];
					$view_arbitrary_item_name[$l] = $arbitrary_item_name[$l];
				}
			}
			for ($l = 1; $l <= 3; $l++) {
				if ($saleItem_info[$l] eq '') {
					$saleItem_info[$l]       = $saleItem_info[$l + 1];
					$view_arbitrary_item_name[$l] = $arbitrary_item_name[$l + 1];
					$saleItem_info[$l + 1]       = '';
					$view_arbitrary_item_name[$l + 1] = '';
				}
			}
			my $saleItem_info_1_flg = 0;
			my $saleItem_info_2_flg = 0;
			my $saleItem_info_3_flg = 0;

			$saleItem_info_1_flg = 1 if ($arbitrary_item_name[1] && $saleItem_info[1]);
			$saleItem_info_2_flg = 1 if ($arbitrary_item_name[2] && $saleItem_info[2]);
			$saleItem_info_3_flg = 1 if ($arbitrary_item_name[3] && $saleItem_info[3]);

			
			
			# タイトルのみ
			if ($FORM{'vtype'} eq 'T') {
				$hash2 = {
					hinmei                  => $item_name_articles,
					saleItem_detailInfo_url => $detailInfo_url,
					order_new_icon          => &checkUri($_CONFIG_order_new_icon, 1),
					order_new_icon_flg      => $item_new_arrived_flg,
					sp_price_icon           => &checkUri($_CONFIG_order_special_price_icon, 1),
					sp_price_icon_flg       => $item_sp_price_flag,
					recom_icon              => &checkUri($_CONFIG_nomination_icon, 1),
					recom_icon_flg          => $item_recom_flg,
					pid                     => $FORM{'pid'},
					retail_price            => $item_including_tax_price,
					sp_price                => $item_money_sp_price_tax,
					item_description_flg    => $item_description_flg,
					item_description        => $item_cmd_finding,
					saleItem_info_1_flg     => $saleItem_info_1_flg,
					saleItem_info_name_1    => $view_arbitrary_item_name[1],
					saleItem_info_1         => $saleItem_info[1],
					saleItem_info_2_flg     => $saleItem_info_2_flg,
					saleItem_info_name_2    => $view_arbitrary_item_name[2],
					saleItem_info_2         => $saleItem_info[2],
					saleItem_info_3_flg     => $saleItem_info_3_flg,
					saleItem_info_name_3    => $view_arbitrary_item_name[3],
					saleItem_info_3         => $saleItem_info[3],
					pretax_sp_price         => $pretax_sp_price,
					pretax_sp_flg           => $pretax_sp_flg,
					pretax_flg              => $pretax_flg,
					pretax_price            => $pretax_price,
				};
			# 画像のみ
			} elsif ($FORM{'vtype'} eq 'I') {
				if($lop % 3 == 1) {
					$tr_start_flg = "1";
				}
				if($lop % 3 == 0 || $lop ==( $#MAIN + 1)) {
					$tr_end_flg = "1";
				}
				$hash2 = {
					hinmei                  => $item_name_articles,
					thumbnail_image_url     => &checkUri(&imgCheck($item_cmd_image_uri_nail, $item_cmd_image_uri_main, 'M'), 1),
					saleItem_detailInfo_url => $detailInfo_url,
					order_new_icon          => &checkUri($_CONFIG_order_new_icon, 1),
					order_new_icon_flg      => $item_new_arrived_flg,
					sp_price_icon           => &checkUri($_CONFIG_order_special_price_icon, 1),
					sp_price_icon_flg       => $item_sp_price_flag,
					recom_icon              => &checkUri($_CONFIG_nomination_icon, 1),
					recom_icon_flg          => $item_recom_flg,
					pid                     => $FORM{'pid'},
					tr_start_flg            => $tr_start_flg,
					tr_end_flg              => $tr_end_flg,
					retail_price            => $item_including_tax_price,
					sp_price                => $item_money_sp_price_tax,
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
					saleItem_detailInfo_url => $detailInfo_url,
					order_new_icon          => &checkUri($_CONFIG_order_new_icon, 1),
					order_new_icon_flg      => $item_new_arrived_flg,
					sp_price_icon           => &checkUri($_CONFIG_order_special_price_icon, 1),
					sp_price_icon_flg       => $item_sp_price_flag,
					recom_icon              => &checkUri($_CONFIG_nomination_icon, 1),
					recom_icon_flg          => $item_recom_flg,
					pid                     => $FORM{'pid'},
					retail_price            => $item_including_tax_price,
					sp_price                => $item_money_sp_price_tax,
					item_description_flg    => $item_description_flg,
					item_description        => $item_cmd_finding,
					saleItem_info_1_flg     => $saleItem_info_1_flg,
					saleItem_info_name_1    => $view_arbitrary_item_name[1],
					saleItem_info_1         => $saleItem_info[1],
					saleItem_info_2_flg     => $saleItem_info_2_flg,
					saleItem_info_name_2    => $view_arbitrary_item_name[2],
					saleItem_info_2         => $saleItem_info[2],
					saleItem_info_3_flg     => $saleItem_info_3_flg,
					saleItem_info_name_3    => $view_arbitrary_item_name[3],
					saleItem_info_3         => $saleItem_info[3],
					pretax_sp_price         => $pretax_sp_price,
					pretax_sp_flg           => $pretax_sp_flg,
					pretax_flg              => $pretax_flg,
					pretax_price            => $pretax_price,
				};
			}
		} elsif($config_data[1] eq '3') {
			# 3→小
			# 描画パターンに応じてテンプレートへ渡す値を変更する
			#my $saleItem_info_1_flg = 1 if ($item_arbitrary_item[$arbitrary_item_num[1]]);
			#my $saleItem_info_2_flg = 1 if ($item_arbitrary_item[$arbitrary_item_num[2]]);
			#my $saleItem_info_3_flg = 1 if ($item_arbitrary_item[$arbitrary_item_num[3]]);
			#my $saleItem_info_4_flg = 1 if ($item_arbitrary_item[$arbitrary_item_num[4]]);
			#my $saleItem_info_5_flg = 1 if ($item_arbitrary_item[$arbitrary_item_num[5]]);
			my @saleItem_info;
			for ($l = 1; $l <= 5; $l++) {
				if ($arbitrary_item_num[$l] eq 'D1') {
					$saleItem_info[$l] = $item_cmd_finding;
				} elsif  ($arbitrary_item_num[$l] eq 'D2') {
					$saleItem_info[$l] = $item_explanation;
				} elsif ($arbitrary_item_num[$l] eq 'D3') {
					$saleItem_info[$l] = $item_publishing_beginning . '〜' . $item_publishing_end;
				} else {
					$saleItem_info[$l] = $item_arbitrary_item[$arbitrary_item_num[$l]];
				}
			}
			my $saleItem_info_1_flg = 1 if ($arbitrary_item_name[1]);
			my $saleItem_info_2_flg = 1 if ($arbitrary_item_name[2]);
			my $saleItem_info_3_flg = 1 if ($arbitrary_item_name[3]);
			my $saleItem_info_4_flg = 1 if ($arbitrary_item_name[4]);
			my $saleItem_info_5_flg = 1 if ($arbitrary_item_name[5]);
			
			$saleItem_info[1] = '&nbsp' unless ($saleItem_info[1]);
			$saleItem_info[2] = '&nbsp' unless ($saleItem_info[2]);
			$saleItem_info[3] = '&nbsp' unless ($saleItem_info[3]);
			$saleItem_info[4] = '&nbsp' unless ($saleItem_info[4]);
			$saleItem_info[5] = '&nbsp' unless ($saleItem_info[5]);
			
			
			# タイトルのみ
			if ($FORM{'vtype'} eq 'T') {
				$hash2 = {
					hinmei                  => $item_name_articles,
					saleItem_detailInfo_url => $detailInfo_url,
					order_new_icon          => &checkUri($_CONFIG_order_new_icon, 1),
					#order_new_icon_flg      => $order_new_icon_flg,
					order_new_icon_flg      => $item_new_arrived_flg,
					sp_price_icon           => &checkUri($_CONFIG_order_special_price_icon, 1),
					sp_price_icon_flg       => $item_sp_price_flag,
					#sp_price_icon_flg       => $sp_price_icon_flg,
					recom_icon              => &checkUri($_CONFIG_nomination_icon, 1),
					recom_icon_flg          => $item_recom_flg,
					pid                     => $FORM{'pid'},
					retail_price            => $item_including_tax_price,
					sp_price                => $item_money_sp_price_tax,
					saleItem_info_1_flg     => $saleItem_info_1_flg,
					saleItem_info_2_flg     => $saleItem_info_2_flg,
					saleItem_info_3_flg     => $saleItem_info_3_flg,
					saleItem_info_4_flg     => $saleItem_info_4_flg,
					saleItem_info_5_flg     => $saleItem_info_5_flg,
					saleItem_info_1         => $saleItem_info[1],
					saleItem_info_2         => $saleItem_info[2],
					saleItem_info_3         => $saleItem_info[3],
					saleItem_info_4         => $saleItem_info[4],
					saleItem_info_5         => $saleItem_info[5],
					pretax_sp_price         => $pretax_sp_price,
					pretax_sp_flg           => $pretax_sp_flg,
					pretax_flg              => $pretax_flg,
					pretax_price            => $pretax_price,
				};
			# 画像のみ
			} elsif ($FORM{'vtype'} eq 'I') {
				if($lop % 4 == 1) {
					$tr_start_flg = "1";
				}
				if($lop % 4 == 0 || $lop ==( $#MAIN + 1)) {
					$tr_end_flg = "1";
				}
				$hash2 = {
					hinmei                  => $item_name_articles,
					thumbnail_image_url     => &checkUri(&imgCheck($item_cmd_image_uri_nail, $item_cmd_image_uri_main, 'S'), 1),
					saleItem_detailInfo_url => $detailInfo_url,
					order_new_icon          => &checkUri($_CONFIG_order_new_icon, 1),
					#order_new_icon_flg      => $order_new_icon_flg,
					order_new_icon_flg      => $item_new_arrived_flg,
					sp_price_icon           => &checkUri($_CONFIG_order_special_price_icon, 1),
					sp_price_icon_flg       => $item_sp_price_flag,
					#sp_price_icon_flg       => $sp_price_icon_flg,
					recom_icon              => &checkUri($_CONFIG_nomination_icon, 1),
					recom_icon_flg          => $item_recom_flg,
					pid                     => $FORM{'pid'},
					tr_start_flg            => $tr_start_flg,
					tr_end_flg              => $tr_end_flg,
					retail_price            => $item_including_tax_price,
					sp_price                => $item_money_sp_price_tax,
					pretax_sp_price         => $pretax_sp_price,
					pretax_sp_flg           => $pretax_sp_flg,
					pretax_flg              => $pretax_flg,
					pretax_price            => $pretax_price,
				};
			# タイトル＋画像
			} else {
				$hash2 = {
					hinmei                  => $item_name_articles,
					thumbnail_image_url     => &checkUri(&imgCheck($item_cmd_image_uri_nail, $item_cmd_image_uri_main, 'S'), 1),
					saleItem_detailInfo_url => $detailInfo_url,
					order_new_icon          => &checkUri($_CONFIG_order_new_icon, 1),
					order_new_icon_flg      => $item_new_arrived_flg,
					sp_price_icon           => &checkUri($_CONFIG_order_special_price_icon, 1),
					sp_price_icon_flg       => $item_sp_price_flag,
					recom_icon              => &checkUri($_CONFIG_nomination_icon, 1),
					recom_icon_flg          => $item_recom_flg,
					pid                     => $FORM{'pid'},
					retail_price            => $item_including_tax_price,
					sp_price                => $item_money_sp_price_tax,
					saleItem_info_1_flg     => $saleItem_info_1_flg,
					saleItem_info_2_flg     => $saleItem_info_2_flg,
					saleItem_info_3_flg     => $saleItem_info_3_flg,
					saleItem_info_4_flg     => $saleItem_info_4_flg,
					saleItem_info_5_flg     => $saleItem_info_5_flg,
					saleItem_info_1         => $saleItem_info[1],
					saleItem_info_2         => $saleItem_info[2],
					saleItem_info_3         => $saleItem_info[3],
					saleItem_info_4         => $saleItem_info[4],
					saleItem_info_5         => $saleItem_info[5],
					pretax_sp_price         => $pretax_sp_price,
					pretax_sp_flg           => $pretax_sp_flg,
					pretax_flg              => $pretax_flg,
					pretax_price            => $pretax_price,
				};
			}
		}
		push(@LOOP_hash, $hash2);
	}
	
	$template->param(SALEITEM_LOOP  => \@LOOP_hash);
	
	# ヘッダフラグ
	my $hedder_flg       = 1 if ($config_data[4] ne '') || ($config_data[5] ne '');
	my $hedder_image_flg = 1 if ($config_data[4] ne '');
	my $footer_flg       = 1 if ($config_data[6] ne '');
	
	my ($meta_title, $meta_description, $meta_keywords, $header_addition);
	if ($config_data[28] == 1) {
		$meta_title       = $_CONFIG_site_title;
		$meta_description = &strBr($_CONFIG_site_outline_site, 1);
		for (my $i = 1; $i <= 10; $i++) {
			if ($_CONFIG_site_keyword[$i]) {
				$meta_keywords .= $_CONFIG_site_keyword[$i] . ',';
			}
		}
		chop $meta_keywords;
	} else {
		$meta_title       = $config_data[29];
		$meta_description = &strBr($config_data[30], 1);
		for (my $i = 31; $i <= 40; $i++) {
			if ($config_data[$i]) {
				$meta_keywords .= $config_data[$i] . ',';
			}
		}
		chop $meta_keywords;
	}
	if ($config_data[42] == 1) {
		$header_addition = $_CONFIG_site_header_addition;
	} else {
		$header_addition = $config_data[41];
		$header_addition =~ s/<RETURN>/\x0A/g;
		$header_addition =~ s/<TAB>/\t/g;
	}
	
	# ループ外変数
	if ($config_data[1] eq '3' && ($FORM{'vtype'} eq 'T' || $FORM{'vtype'} eq 'TI')) {
		my $saleItem_info_1_flg = 1 if ($arbitrary_item_name[1]);
		my $saleItem_info_2_flg = 1 if ($arbitrary_item_name[2]);
		my $saleItem_info_3_flg = 1 if ($arbitrary_item_name[3]);
		my $saleItem_info_4_flg = 1 if ($arbitrary_item_name[4]);
		my $saleItem_info_5_flg = 1 if ($arbitrary_item_name[5]);
		$template->param(
			saleItem_info_1_flg  => $saleItem_info_1_flg,
			saleItem_info_2_flg  => $saleItem_info_2_flg,
			saleItem_info_3_flg  => $saleItem_info_3_flg,
			saleItem_info_4_flg  => $saleItem_info_4_flg,
			saleItem_info_5_flg  => $saleItem_info_5_flg,
			saleItem_info_name_1 => $arbitrary_item_name[1],
			saleItem_info_name_2 => $arbitrary_item_name[2],
			saleItem_info_name_3 => $arbitrary_item_name[3],
			saleItem_info_name_4 => $arbitrary_item_name[4],
			saleItem_info_name_5 => $arbitrary_item_name[5],
		);
	}
	$template->param(
		vtype                => $FORM{'vtype'},
		vtype_t              => $vtype_t,
		vtype_i              => $vtype_i,
		vtype_ti             => $vtype_ti,
		stype                => $FORM{'stype'},
		stype1_flg           => $stype1_flg,
		stype2_flg           => $stype2_flg,
		stype3_flg           => $stype3_flg,
		stype4_flg           => $stype4_flg,
		stype5_flg           => $stype5_flg,
		akeyworddec          => MODULE::StringUtil::conversionSpecialChar($FORM{'akeyword'}),
		akeyword             => MODULE::StringUtil::conversionSpecialChar($akeyword),
		pageing_start_number => $paging_start_number,
		pageing_end_number   => $paging_end_number,
		pageing_all_number   => $paging_all_number,
		pageing_area         => $paging_area,
		pageing_back         => $paging_back,
		pageing_next         => $paging_next,
		tax_string           => $_CONFIG_tax_marking,
		pid                  => $FORM{'pid'},
		hedder_flg           => $hedder_flg,
		hedder_image_flg     => $hedder_image_flg,
		hedder_image_url     => &checkUri($config_data[4], 1),
		hedder_comment       => $config_data[5],
		search_form_flg      => $config_data[2],
		footer_flg           => $footer_flg,
		footer_comment       => $config_data[6],
		narrow_search_flg    => $narrow_search_flg,
		no_item_flg          => $no_item_flg,
		meta_title           => $meta_title,
		meta_description     => &strBr($meta_description, 1),
		meta_keywords        => $meta_keywords,
		vnum                 => $FORM{'vnum'},
		CONFIG_business_legis_flg         => $_CONFIG_business_legis_flg,
		header_addition      => $header_addition,
	);
	
	print $_CONFIG_base_head;
	print $template -> output;

