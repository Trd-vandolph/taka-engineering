#!/usr/bin/perl
use MODULE::Template;
use MODULE::StringUtil;
	
	our $_CONFIG_server_ssl_use;
	our $_CONFIG_page_view_mode;
	our $_CONFIG_server_ssl_site_addr;
	our $_CONFIG_order_tag_askItem;
	our $_CONFIG_template_dir;

	# サイト用サブルーチンファイル読み込み
	require './subroutine.pl';
	# サイト用共通変数ファイル読み込み
	require './config_data.cgi';
	
	&formLoading;
	
	my $template = HTML::Template->new(filename => "./$_CONFIG_template_dir/askItem_detail.tmp");
	
	my $insert_line;
	
	my $data_file = sprintf('./search/%02d/%02d.cgi', $FORM{'cc'}, $FORM{'gc'});
	open(DATA, $data_file);
	my @data_file = <DATA>;
	close(DATA);
	chomp @data_file;
	
	my $this_counter = 0;
	foreach (@data_file) {
		my @data_line = split(/\t/, $_);
		if ($data_line[0] eq $FORM{'ic'}) {
			$insert_line = $insert_line . join("\t", @data_line);
			last;
		}
		$this_counter++;
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
	@stock_file = sort { (split(/\,/,$a))[0] <=> (split(/\,/,$b))[0] } @stock_file;
	foreach (@stock_file) {
		my $hash_data  = "";
		my @stock_line = split(/\t/, $_);
		$stock_line[0] =~ /(\d{8})(\d{2})(\d{2})/;
		if (($1 eq $item_cmd_basic_id) && ($2 eq '01')) {
			my $unstocked_flg   = 1 if ($stock_line[1] < 1);
			$hash_data = {
				unstocked01_flg   => $unstocked_flg,
			};
			push(@variation01, $hash_data);
		} elsif (($1 eq $item_cmd_basic_id) && ($2 eq '02')) {
			my $unstocked_flg   = 1 if ($stock_line[1] < 1);
			$hash_data = {
				unstocked02_flg   => $unstocked_flg,
			};
			push(@variation02, $hash_data);
		} elsif (($1 eq $item_cmd_basic_id) && ($2 eq '03')) {
			my $unstocked_flg   = 1 if ($stock_line[1] < 1);
			$hash_data = {
				unstocked03_flg   => $unstocked_flg,
			};
			push(@variation03, $hash_data);
		} elsif (($1 eq $item_cmd_basic_id) && ($2 eq '04')) {
			my $unstocked_flg   = 1 if ($stock_line[1] < 1);
			$hash_data = {
				unstocked04_flg   => $unstocked_flg,
			};
			push(@variation04, $hash_data);
		} elsif (($1 eq $item_cmd_basic_id) && ($2 eq '05')) {
			my $unstocked_flg   = 1 if ($stock_line[1] < 1);
			$hash_data = {
				unstocked05_flg   => $unstocked_flg,
			};
			push(@variation05, $hash_data);
		} elsif (($1 eq $item_cmd_basic_id) && ($2 eq '06')) {
			my $unstocked_flg   = 1 if ($stock_line[1] < 1);
			$hash_data = {
				unstocked06_flg   => $unstocked_flg,
			};
			push(@variation06, $hash_data);
		} elsif (($1 eq $item_cmd_basic_id) && ($2 eq '07')) {
			my $unstocked_flg   = 1 if ($stock_line[1] < 1);
			$hash_data = {
				unstocked07_flg   => $unstocked_flg,
			};
			push(@variation07, $hash_data);
		} elsif (($1 eq $item_cmd_basic_id) && ($2 eq '08')) {
			my $unstocked_flg   = 1 if ($stock_line[1] < 1);
			$hash_data = {
				unstocked08_flg   => $unstocked_flg,
			};
			push(@variation08, $hash_data);
		} elsif (($1 eq $item_cmd_basic_id) && ($2 eq '09')) {
			my $unstocked_flg   = 1 if ($stock_line[1] < 1);
			$hash_data = {
				unstocked09_flg   => $unstocked_flg,
			};
			push(@variation09, $hash_data);
		} elsif (($1 eq $item_cmd_basic_id) && ($2 eq '10')) {
			my $unstocked_flg   = 1 if ($stock_line[1] < 1);
			$hash_data = {
				unstocked10_flg   => $unstocked_flg,
			};
			push(@variation10, $hash_data);
		}
	}
	
	# 簡易説明
	my $simple_description_flg = 1 if ($item_cmd_finding ne '');
	
	# 掲載期間
	my $term_posted_flg = 1 if (($item_publishing_beginning ne '') || ($item_publishing_end ne ''));
	my $term_posted_flg = 1 if (($item_publishing_end ne '9998/12/31'));

	my $error_flg;
	#_掲載期間チェック
	$error_flg = &checkDate($item_publishing_beginning, $item_publishing_end);
	#_公開フラグチェック
	if ($item_opening_to_public eq '0') {
		$error_flg = 1;
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
	
	# 任意
	my $anyItem_info_1_flg = 1 if ($item_arbitrary_item[1] ne '');
	my $anyItem_info_2_flg = 1 if ($item_arbitrary_item[2] ne '');
	my $anyItem_info_3_flg = 1 if ($item_arbitrary_item[3] ne '');
	my $anyItem_info_4_flg = 1 if ($item_arbitrary_item[4] ne '');
	my $anyItem_info_5_flg = 1 if ($item_arbitrary_item[5] ne '');
	my $anyItem_info_6_flg = 1 if ($item_arbitrary_item[6] ne '');
	my $anyItem_info_7_flg = 1 if ($item_arbitrary_item[7] ne '');
	my $anyItem_info_8_flg = 1 if ($item_arbitrary_item[8] ne '');
	

	# 在庫
	my $stock_total_unstocked = '';
	if(0 < $item_stock_total) {
		$stock_total_unstocked = '1';
	}
	
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
	
	my $askItem_form_url;
	if ($_CONFIG_server_ssl_use ne '0' && $_CONFIG_page_view_mode ne 'P') {
		$askItem_form_url = sprintf('%s/cgi-bin/askItem_form.cgi', $_CONFIG_server_ssl_site_addr);
	} else {
		$askItem_form_url = './askItem_form.cgi';
	}
	
	# エラーチェック
	my $err_retuen_flg = 1 if (($FORM{'erra'} ne '') || ($FORM{'errb'} ne '') || ($FORM{'errc'} ne ''));
	
	$template->param(
		main_image_url          => &checkUri(&imgCheck($item_cmd_image_uri_main, '', 'L'), 1),
		sub1_image_url          => &checkUri(&imgCheck($item_cmd_image_uri_sub1, '', 'L'), 1),
		sub2_image_url          => &checkUri(&imgCheck($item_cmd_image_uri_sub2, '', 'L'), 1),
		hinmei                  => $item_name_articles,
		item_description        => $item_explanation,
		main_percent            => $main_percent,
		sub1_percent            => $sub1_percent,
		sub2_percent            => $sub2_percent,
		main_px                 => $main_px,
		sub1_px                 => $sub1_px,
		sub2_px                 => $sub2_px,
		main_flg                => $main_flg,
		sub1_flg                => $sub1_flg,
		sub2_flg                => $sub2_flg,
		retail_price            => &convertMoney($item_including_tax_price),
		sp_price_icon           => &checkUri($_CONFIG_order_special_price_icon, 1),
		sp_price_icon_flg       => $item_sp_price_flag,
		sp_price                => &convertMoney($item_money_sp_price_tax),
		recom_icon              => &checkUri($_CONFIG_nomination_icon, 1),
		recom_icon_flg          => $item_recom_flg,
		order_new_icon_flg      => $item_new_arrived_flg,
		order_new_icon          => &checkUri($_CONFIG_order_new_icon, 1),
		delivery_type           => &deliveryOut($item_deli_type_id),
		simple_description_flg  => $simple_description_flg,
		simple_description      => $item_cmd_finding,
		term_posted_flg         => $term_posted_flg,
		term_posted_start       => $item_publishing_beginning,
		term_posted_fin         => $item_publishing_end,
		anyItem_info_1_flg      => $anyItem_info_1_flg,
		anyItem_info_1_name     => $_CONFIG_item_option_title[1],
		anyItem_info_1          => $item_arbitrary_item[1],
		anyItem_info_2_flg      => $anyItem_info_2_flg,
		anyItem_info_2_name     => $_CONFIG_item_option_title[2],
		anyItem_info_2          => $item_arbitrary_item[2],
		anyItem_info_3_flg      => $anyItem_info_3_flg,
		anyItem_info_3_name     => $_CONFIG_item_option_title[3],
		anyItem_info_3          => $item_arbitrary_item[3],
		anyItem_info_4_flg      => $anyItem_info_4_flg,
		anyItem_info_4_name     => $_CONFIG_item_option_title[4],
		anyItem_info_4          => $item_arbitrary_item[4],
		anyItem_info_5_flg      => $anyItem_info_5_flg,
		anyItem_info_5_name     => $_CONFIG_item_option_title[5],
		anyItem_info_5          => $item_arbitrary_item[5],
		anyItem_info_6_flg      => $anyItem_info_6_flg,
		anyItem_info_6_name     => $_CONFIG_item_option_title[6],
		anyItem_info_6          => $item_arbitrary_item[6],
		anyItem_info_7_flg      => $anyItem_info_7_flg,
		anyItem_info_7_name     => $_CONFIG_item_option_title[7],
		anyItem_info_7          => $item_arbitrary_item[7],
		anyItem_info_8_flg      => $anyItem_info_8_flg,
		anyItem_info_8_name     => $_CONFIG_item_option_title[8],
		anyItem_info_8          => $item_arbitrary_item[8],
		stock_total_flg         => $item_stock_amount_disp,
		stock_total_unstocked   => $stock_total_unstocked,
		variation_code          => $item_vari_disp,
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
		yoko_title              => $item_vari_h_name,
		tate_title              => $item_vari_v_name,
		tax_string              => $_CONFIG_tax_marking,
		saleItem_id             => sprintf('%02d%02d%08d',$FORM{'cc'}, $FORM{'gc'}, $FORM{'ic'}),
		pid                     => $FORM{'pid'},
		error_flg               => $error_flg,
		top_url                 => '',
		askItem_form_url        => $askItem_form_url,
		embedding_tag           => &errstrRecover($_CONFIG_order_tag_askItem),
		pretax_sp_flg           => $pretax_sp_flg,
		pretax_price            => $pretax_price,
		pretax_flg              => $pretax_flg,
		pretax_sp_price         => $pretax_sp_price,
		CONFIG_business_legis_flg         => $_CONFIG_business_legis_flg,
	);
	
	print $_CONFIG_base_head;
	print $template -> output;
