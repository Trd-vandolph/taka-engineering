sub apricationErr{
	my $str = $_[0];
	$template = HTML::Template->new(filename => "./$_CONFIG_template_dir/error_application.tmp");
	$template->param(
		top_url => $str,
	);
	print $_CONFIG_base_head;
	print $template -> output;
	exit;
}

sub pageLoginErr{
	my $str = $_[0];
	$template = HTML::Template->new(filename => "./$_CONFIG_template_dir/error_login.tmp");
	$template->param(
		top_url => $str,
	);
	print $_CONFIG_base_head;
	print $template -> output;
	exit;
}

sub getLoginCookie {
	my $str = $_[0];
	my $cookies = $_[1];
	my $logger = $_[2];
	my ($xx, $name, $value);
	#foreach $xx (split(/;/, $ENV{'HTTP_COOKIE'})) {
	#	($name, $value) = split(/=/, $xx);
	#	next if ($str ne $name);
	#	$value =~ s/%([0-9A-Fa-f][0-9A-Fa-f])/pack("C", hex($1))/eg;
	#	$COOKIE{$name} = $value;
	#	return $value;
	#}
	my $cookies = $ENV{'HTTP_COOKIE'};
	my @pairs = split(/;/,$cookies);
	my %COOKIE;
	foreach my $pair (@pairs) {
		my ($name,$value) = split(/=/,$pair);
		$name =~ s/ //g;
		$COOKIE{$name} = $value;
	}
	return $COOKIE{$str};
}

sub getCookie {
	local($xx, $name, $value);
	foreach $xx (split(/;\s*/, $ENV{'HTTP_COOKIE'})) {
		($name, $value) = split(/=/, $xx);
		next if ($session_name ne $name);
		$value =~ s/%([0-9A-Fa-f][0-9A-Fa-f])/pack("C", hex($1))/eg;
		$COOKIE{$name} = $value;
		last;
	}
}

sub outputLog {
	use Logger::MyLogger;
	our $logger = Logger::MyLogger->new;
	$logger->appendLog("$_[0]");
}

sub formLoading {
	my $buffer;
	my @pairs;
	if ($ENV{'REQUEST_METHOD'} eq 'POST') {
		read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
		@pairs = split(/&/, $buffer);
		my $back_name = "";
		foreach my $pair (@pairs) {
			(my $name, my $value) = split(/=/, $pair);
			$value =~ tr/+/ /;
			$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
			if ($back_name eq $name) {
				$FORM{$name} = $FORM{$name} . ' ' . $value;
			} else {
				$FORM{$name} = $value;
			}
			$back_name = $name;
		}
	}
	$buffer = $ENV{'QUERY_STRING'};

	@pairs = split(/&/, $buffer);
	my $back_name = "";
	foreach my $pair (@pairs) {
		(my $name, my $value) = split(/=/, $pair);
		$value =~ tr/+/ /;
		$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
		if ($back_name eq $name) {
			$FORM{$name} = $FORM{$name} . ' ' . $value;
		} else {
			$FORM{$name} = $value;
		}
		$back_name = $name;
	}
}
sub strBr {
	(my $str, my $type_flg) = @_;
	if ($type_flg == 1) {
		$str =~ s/<BR>/\x0A/g;
		$str =~ s/<BR>/\x0D/g;
		$str =~ s/<BR>/\x0D\x0A/g;
		return $str;
	} else {
		$str =~ s/\x0D\x0A/<BR>/g;
		$str =~ s/\x0D/<BR>/g;
		$str =~ s/\x0A/<BR>/g;
		return $str;
	}
}

sub strBrDouble {
	(my $str, my $type_flg) = @_;
	$str =~ s/\x0D//g;
	return $str;
}

sub editDate {
	my $str = $_[0];
	$str =~ /(\d{4})\/(\d{2})\/(\d{2})/;
	return $1 . $2 . $3;
}

sub checkDate {
	(my $daystart, my $daylast) = @_;
	my( undef, undef, undef, $day, $mon, $year ) = localtime(time);
	$mon += 1;
	$year += 1900;
	my $today = sprintf('%04d%02d%02d',$year, $mon, $day);
	$daystart =~ m|(\d+)/(\d+)/(\d+)|;
	$daystart = sprintf('%04d%02d%02d', $1, $2, $3);
	$daylast  =~ m|(\d+)/(\d+)/(\d+)|;
	$daylast  = sprintf('%04d%02d%02d', $1, $2, $3);
	if ($daystart <= $today && $today <= $daylast) {
		return 0;
	} else {
		return 1;
	}
}

sub itemMainDataSplit {
	(
		$item_cmd_basic_id,			$item_cmd_insert_day,		$item_cmd_category_id,		$item_product_grp_id,
		$item_name_articles,		$item_name_kana,			$item_cmd_finding,			$item_explanation,
		$item_cmd_keyword,			$item_price,				$item_including_tax_price,	$item_vari_disp,
		$item_stock_setting_flg,	$item_stock_amount_disp,	$item_stock_total,			$item_stock_number_alert,
		$item_process_out_stock,	$item_comment_out_stock,	$item_new_arrived_flg,		$item_deli_type_id,
		$item_sp_price_flag,		$item_money_sp_price,		$item_money_sp_price_tax,	$item_max_order_receipts,
		$item_sales_beginning,		$item_sales_term,			$item_publishing_beginning,	$item_publishing_end,
		$item_arbitrary_item[1],	$item_arbitrary_item[2],	$item_arbitrary_item[3],	$item_arbitrary_item[4],
		$item_arbitrary_item[5],	$item_arbitrary_item[6],	$item_arbitrary_item[7],	$item_arbitrary_item[8],
		$item_cmd_image_uri_main,	$item_cmd_image_size_main,	$item_cmd_image_unit_main,	$item_cmd_image_uri_sub1,
		$item_cmd_image_size_sub1,	$item_cmd_image_unit_sub1,	$item_cmd_image_uri_sub2,	$item_cmd_image_size_sub2,
		$item_cmd_image_unit_sub2,	$item_cmd_image_uri_nail,	$item_cmd_image_size_nail,	$item_cmd_image_unit_nail,
		$item_recom_cmd_id1,		$item_recom_cmd_id2,		$item_recom_cmd_id3,		$item_recom_flg,
		$item_recom_degree,			$item_review_disp,			$item_opening_to_public,	$item_group_name,
		$item_order_count
	) = split(/\t/, $line);
}

sub itemMainDataSplitFull {
	# V1.68 行データへのTrim処理を追加
	$line =~ s/^\s*(.*?)\s*$/$1/;
	(
		$item_cmd_basic_id,			$item_cmd_insert_day,		$item_cmd_category_id,		$item_product_grp_id,
		$item_name_articles,		$item_name_kana,			$item_cmd_finding,			$item_explanation,
		$item_cmd_keyword,			$item_price,				$item_including_tax_price,	$item_vari_disp,
		$item_stock_setting_flg,	$item_stock_amount_disp,	$item_stock_total,			$item_stock_number_alert,
		$item_process_out_stock,	$item_comment_out_stock,	$item_new_arrived_flg,		$item_deli_type_id,
		$item_sp_price_flag,		$item_money_sp_price,		$item_money_sp_price_tax,	$item_max_order_receipts,
		$item_sales_beginning,		$item_sales_term,			$item_publishing_beginning,	$item_publishing_end,
		$item_arbitrary_item[1],	$item_arbitrary_item[2],	$item_arbitrary_item[3],	$item_arbitrary_item[4],
		$item_arbitrary_item[5],	$item_arbitrary_item[6],	$item_arbitrary_item[7],	$item_arbitrary_item[8],
		$item_cmd_image_uri_main,	$item_cmd_image_size_main,	$item_cmd_image_unit_main,	$item_cmd_image_uri_sub1,
		$item_cmd_image_size_sub1,	$item_cmd_image_unit_sub1,	$item_cmd_image_uri_sub2,	$item_cmd_image_size_sub2,
		$item_cmd_image_unit_sub2,	$item_cmd_image_uri_nail,	$item_cmd_image_size_nail,	$item_cmd_image_unit_nail,
		$item_recom_cmd_id[1],		$item_recom_cmd_id[2],		$item_recom_cmd_id[3],		$item_recom_flg,
		$item_recom_degree,			$item_review_disp,			$item_opening_to_public,	,
		$item_vari_h_name,			$item_vari_h_clm[1],		$item_vari_h_clm[2],		$item_vari_h_clm[3],
		$item_vari_h_clm[4],		$item_vari_h_clm[5],		$item_vari_h_clm[6],		$item_vari_h_clm[7],
		$item_vari_h_clm[8],		$item_vari_h_clm[9],		$item_vari_h_clm[10],		$item_vari_v_name,
		$item_vari_v_clm[1],		$item_vari_v_clm[2],		$item_vari_v_clm[3],		$item_vari_v_clm[4],
		$item_vari_v_clm[5],		$item_vari_v_clm[6],		$item_vari_v_clm[7],		$item_vari_v_clm[8],
		$item_vari_v_clm[9],		$item_vari_v_clm[10]
	) = split(/\t/, $line);
}

sub decodUrl {
	my $str = $_[0];
	$str =~ s/([^\w ])/'%' . unpack('H2', $1)/eg;
	$str =~ tr/ /+/;
	return $str;
}

sub imgCheck {
	my ($str_1, $str_2, $img_type) = @_;
	my $str;
	if ($str_1 eq '' && $str_2 eq '') {
		if ($img_type eq 'S') {
			$str = '/img/nowprinting_65.png';
		} elsif ($img_type eq 'M') {
			$str = '/img/nowprinting_130.png';
		} elsif ($img_type eq 'L') {
			$str = '/img/nowprinting_300.png';
		} else {
			$str = '/img/nowprinting_300.png';
		}
	} elsif ($str_1 eq '') {
		$str = $str_2;
	} else {
		$str = $str_1;
	}
	return $str;
}

sub mailChecker {
	(my $str) = @_;
	# メールの型で無かった場合0を返す
	if ($str =~ /^([\w-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([\w-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$/ ) {
	#if ($str =~ /^[0-9a-zA-Z]+[0-9a-zA-Z-_]+\@[0-9a-zA-Z-_]+(\.[0-9a-zA-Z-_]+)+?$/ ) {
		return 1;
	} else {
		return 0;
	}
}

sub strIntCheck {
	my $str = $_[0];
	# 半角数値型で無かった場合0を返す
	if ($str =~ /[\D]+/ ) {
		return 0;
	} else {
		return 1;
	}
}

sub strDateCheck {
#	use Time::Local;
#	my($year, $mon, $day) = @_;
#	eval {
#		timelocal(0, 0, 0, $day, $mon-1, $year-1900);
#	};
#	if ($@) {
#		return 0;
#	}
#	if ($mon == 12) {
#		$mon = 0;
#	}
#	my $time = timelocal(0, 0, 0, 1, $mon, $year-1900);
#	$time -= 60 * 60 * 24;
#	my @date = localtime($time);
#	if ($day > $date[3]) {
#		return 0;
#	}
#	return 1;

	my($year, $month, $day) = @_;
	my(@mlast) = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31);
	
	if ($month < 1 || 12 < $month) { return 0; }
	
	if ($month == 2) {
		if ( (($year % 4 == 0) && ($year % 100 != 0)) || ($year % 400 == 0) ) {
			$mlast[1]++;
		}
	}
	
	if ($day < 1 || $mlast[$month-1] < $day) { return 0; }
	
	return 1;
}

sub errstrConvert {
	(my $str) = @_;
	$str =~ s/&/&amp;/g;
	$str =~ s/\"/&quot;/g;#"
	$str =~ s/</&lt;/g;
	$str =~ s/>/&gt;/g;
	$str =~ s/ /&nbsp;/g;
	#$str =~ s/\\/&yen;/g;
	return $str;
}

sub errstrRecover {
	(my $str) = @_;
	$str =~ s/&amp;/&/g;
	$str =~ s/&quot;/\"/g;#"
	$str =~ s/&lt;/</g;
	$str =~ s/&gt;/>/g;
	$str =~ s/&nbsp;/ /g;
	$str =~ s/&yen;/\\/g;
	return $str;
}

sub deliveryOut {
	my $str = $_[0];
	my $return_str;
	my $list_file    = "$_CONFIG_server_ssl_www_root/cgi-bin/item_delivery.cgi";
	open(DATA, $list_file);
	my @list_file = <DATA>;
	close(DATA);
	foreach (@list_file) {
		my @list_line = split(/\t/, $_);
		if ($str == $list_line[0]) {
			$return_str = $list_line[1];
		}
	}
	return $return_str;
}

sub prefOut {
	my $str = $_[0];
	my $return_str;
	my @pref_list;
	
	$pref_list[1]  = '北海道';
	$pref_list[2]  = '青森県';
	$pref_list[3]  = '岩手県';
	$pref_list[4]  = '宮城県';
	$pref_list[5]  = '秋田県';
	$pref_list[6]  = '山形県';
	$pref_list[7]  = '福島県';
	$pref_list[8]  = '茨城県';
	$pref_list[9]  = '栃木県';
	$pref_list[10] = '群馬県';
	$pref_list[11] = '埼玉県';
	$pref_list[12] = '千葉県';
	$pref_list[13] = '東京都';
	$pref_list[14] = '神奈川県';
	$pref_list[15] = '山梨県';
	$pref_list[16] = '静岡県';
	$pref_list[17] = '長野県';
	$pref_list[18] = '新潟県';
	$pref_list[19] = '富山県';
	$pref_list[20] = '石川県';
	$pref_list[21] = '福井県';
	$pref_list[22] = '岐阜県';
	$pref_list[23] = '愛知県';
	$pref_list[24] = '三重県';
	$pref_list[25] = '滋賀県';
	$pref_list[26] = '京都府';
	$pref_list[27] = '大阪府';
	$pref_list[28] = '兵庫県';
	$pref_list[29] = '奈良県';
	$pref_list[30] = '和歌山県';
	$pref_list[31] = '鳥取県';
	$pref_list[32] = '島根県';
	$pref_list[33] = '岡山県';
	$pref_list[34] = '広島県';
	$pref_list[35] = '山口県';
	$pref_list[36] = '徳島県';
	$pref_list[37] = '香川県';
	$pref_list[38] = '愛媛県';
	$pref_list[39] = '高知県';
	$pref_list[40] = '福岡県';
	$pref_list[41] = '佐賀県';
	$pref_list[42] = '長崎県';
	$pref_list[43] = '熊本県';
	$pref_list[44] = '大分県';
	$pref_list[45] = '宮崎県';
	$pref_list[46] = '鹿児島県';
	$pref_list[47] = '沖縄県';
	$return_str = $pref_list[$str];
	return $return_str;
}

sub checkUri {
	my $str  = $_[0];
	my $type = $_[1];
	if ($type == 1) {
		if ($str =~ /^\/.+?/) {
			$str = '..' . $str;
			return $str;
		} else {
			$str = '../' . $str;
			return $str;
		}
	} else {
		if ($str =~ /^\/.+?/) {
			return $str;
		} else {
			$str = '/' . $str;
			return $str;
		}
	}
}

sub convertMoney {
	my $num = $_[0];
	$num = reverse $num;
	$num =~ s/(\d{3})(?=\d)(?!\d*\.)/$1,/g;
	$num = reverse $num;
	return $num
}

sub pagingOut {
	(my $db_page_turning_last, my $db_page_turning_next, my $page_counter, my $total_page, my $top_page, my $last_page, my $form_cc, my $form_gc, my $form_item_keyword, my $form_price_low, my $form_price_up, my $form_keyword, my $form_stype, my $form_vtype, my $type) = @_;
	my $paging_line = "";
	if ($type eq 'cc') {
		for (my $i = $top_page; $i <= $last_page; $i++) {
			if ($i > $top_page) {
				$paging_line = $paging_line . sprintf('&nbsp;|&nbsp;');
			}
			if ($page_counter == $i) {
				$paging_line = $paging_line . sprintf(' %d ', $i);
			} else {
				$paging_line = $paging_line . sprintf('&nbsp;<a href="?cc=%s&ckeyword=%s&stype=%s&vtype=%s&vnum=%s">%d</a>&nbsp;',
				$form_cc, $form_keyword, $form_stype, $form_vtype, $i, $i);
			}
		}
		if ($db_page_turning_last ne ''){
			$db_page_turning_last = sprintf('<a href="?cc=%s&ckeyword=%s&stype=%s&vtype=%s&vnum=%s">%s</a>',
			$form_cc, $form_keyword, $form_stype, $form_vtype, $page_counter-1 ,$db_page_turning_last);
		}
		if ($db_page_turning_next ne ''){
			$db_page_turning_next = sprintf('<a href="?cc=%s&ckeyword=%s&stype=%s&vtype=%s&vnum=%s">%s</a>',
			$form_cc, $form_keyword, $form_stype, $form_vtype, $page_counter+1 ,$db_page_turning_next);
		}
	} elsif ($type eq 'gc') {
		for (my $i = $top_page; $i <= $last_page; $i++) {
			if ($i > $top_page) {
				$paging_line = $paging_line . sprintf('&nbsp;|&nbsp;');
			}
			if ($page_counter == $i) {
				$paging_line = $paging_line . sprintf(' %d ', $i);
			} else {
				$paging_line = $paging_line . sprintf('&nbsp;<a href="?cc=%s&gc=%s&gkeyword=%s&stype=%s&vtype=%s&vnum=%s">%d</a>&nbsp;',
				$form_cc, $form_gc, $form_keyword, $form_stype, $form_vtype, $i, $i);
			}
		}
		if ($db_page_turning_last ne ''){
			$db_page_turning_last = sprintf('<a href="?cc=%s&gc=%s&gkeyword=%s&stype=%s&vtype=%s&vnum=%s">%s</a>',
			$form_cc, $form_gc, $form_keyword, $form_stype, $form_vtype, $page_counter-1 ,$db_page_turning_last);
		}
		if ($db_page_turning_next ne ''){
			$db_page_turning_next = sprintf('<a href="?cc=%s&gc=%s&gkeyword=%s&stype=%s&vtype=%s&vnum=%s">%s</a>',
			$form_cc, $form_gc, $form_keyword, $form_stype, $form_vtype, $page_counter+1 ,$db_page_turning_next);
		}
	} elsif ($type eq 'sc') {
		for (my $i = $top_page; $i <= $last_page; $i++) {
			if ($i > $top_page) {
				$paging_line = $paging_line . sprintf('&nbsp;|&nbsp;');
			}
			if ($page_counter == $i) {
				$paging_line = $paging_line . sprintf(' %d ', $i);
			} else {
				$paging_line = $paging_line . sprintf('&nbsp;<a href="?item_keyword=%s&item_price_low=%s&item_price_up=%s&skeyword=%s&stype=%s&vtype=%s&vnum=%s">%d</a>&nbsp;',
				$form_item_keyword, $form_price_low, $form_price_up, $form_keyword, $form_stype, $form_vtype, $i, $i);
			}
		}
		if ($db_page_turning_last ne ''){
			$db_page_turning_last = sprintf('<a href="?item_keyword=%s&item_price_low=%s&item_price_up=%s&skeyword=%s&stype=%s&vtype=%s&vnum=%s">%s</a>',
			$form_item_keyword, $form_price_low, $form_price_up, $form_keyword, $form_stype, $form_vtype, $page_counter-1 ,$db_page_turning_last);
		}
		if ($db_page_turning_next ne ''){
			$db_page_turning_next = sprintf('<a href="?item_keyword=%s&item_price_low=%s&item_price_up=%s&skeyword=%s&stype=%s&vtype=%s&vnum=%s">%s</a>',
			$form_item_keyword, $form_price_low, $form_price_up, $form_keyword, $form_stype, $form_vtype, $page_counter+1 ,$db_page_turning_next);
		}
	} elsif ($type eq 'uc') {
		for (my $i = $top_page; $i <= $last_page; $i++) {
			if ($i > $top_page) {
				$paging_line = $paging_line . sprintf('&nbsp;|&nbsp;');
			}
			if ($page_counter == $i) {
				$paging_line = $paging_line . sprintf(' %d ', $i);
			} else {
				$paging_line = $paging_line . sprintf('&nbsp;<a href="?pid=%s&ukeyword=%s&stype=%s&vtype=%s&vnum=%s">%d</a>&nbsp;',
				$form_cc, $form_keyword, $form_stype, $form_vtype, $i, $i);
			}
		}
		if ($db_page_turning_last ne ''){
			$db_page_turning_last = sprintf('<a href="?pid=%s&ukeyword=%s&stype=%s&vtype=%s&vnum=%s">%s</a>',
			$form_cc, $form_keyword, $form_stype, $form_vtype, $page_counter-1 ,$db_page_turning_last);
		}
		if ($db_page_turning_next ne ''){
			$db_page_turning_next = sprintf('<a href="?pid=%s&ukeyword=%s&stype=%s&vtype=%s&vnum=%s">%s</a>',
			$form_cc, $form_keyword, $form_stype, $form_vtype, $page_counter+1 ,$db_page_turning_next);
		}
	} elsif ($type eq 'ac') {
		for (my $i = $top_page; $i <= $last_page; $i++) {
			if ($i > $top_page) {
				$paging_line = $paging_line . sprintf('&nbsp;|&nbsp;');
			}
			if ($page_counter == $i) {
				$paging_line = $paging_line . sprintf(' %d ', $i);
			} else {
				$paging_line = $paging_line . sprintf('&nbsp;<a href="?pid=%s&akeyword=%s&stype=%s&vtype=%s&vnum=%s">%d</a>&nbsp;',
				$form_cc, $form_keyword, $form_stype, $form_vtype, $i, $i);
			}
		}
		if ($db_page_turning_last ne ''){
			$db_page_turning_last = sprintf('<a href="?pid=%s&akeyword=%s&stype=%s&vtype=%s&vnum=%s">%s</a>',
			$form_cc, $form_keyword, $form_stype, $form_vtype, $page_counter-1 ,$db_page_turning_last);
		}
		if ($db_page_turning_next ne ''){
			$db_page_turning_next = sprintf('<a href="?pid=%s&akeyword=%s&stype=%s&vtype=%s&vnum=%s">%s</a>',
			$form_cc, $form_keyword, $form_stype, $form_vtype, $page_counter+1 ,$db_page_turning_next);
		}
	}
	return ($db_page_turning_last, $paging_line, $db_page_turning_next);
}

sub strTrim {
	#shift_jis専用
	my $str = shift;
	#$onebyte = '[\x00-\x7F\xA1-\xDF]';
	#$space = '(?:[\ \n\r\t\f]|\x81\x40)';
	#$twobyte = '(?:[\x81-\x9F\xE0-\xFC][\x40-\x7E\x80-\xFC])'; 

	my $len = index($str, ' ');

	# 文字毎に区切る
	#$str =~ s/($onebyte)/$1\0/g;
	#$str =~ s/$twobyte(.)\0/$1$2\0\0/g; 

	#my @strlist = split(/\0/, $str);
	#my @strlist = split(/\0/, $str);
	#my @newstrlist;
	#foreach my $mystr ( @strlist ) {
	#	$mystr =~ s/^$space*//;
	#	$mystr =~ s/\0//;
	#	push (@newstrlist, $mystr);
	#}
	
	#return join ('', @newstrlist);
	return $str;
}

sub strKanaCheck {
	my $str = shift;
	#utf8::decode($str);
	#if ($str =~ /^([\x{30A1}-\x{30F6}|\x{30FC}])+$/) {
	if ($str =~ /^(\x83[\x40-\x96]|\x81[\x5B])+$/) {
		return 1;
	} else {
		return 0;
	}
}

sub strLocation {
	my @pass = split(/\//, $ENV{'REQUEST_URI'});
	my $new_passs = "";
	my $str = shift;

	if($_CONFIG_page_view_mode eq 'P') {
		for (my $i = 0; $i < $#pass; $i++) {
			$new_passs = $new_passs .  @pass[$i] . '/';
		}
		#$str =  'http://' . $ENV{'SERVER_NAME'} . ':' . $ENV{'SERVER_PORT'} . $new_passs;
		$str =  'http://localhost:' . $ENV{'SERVER_PORT'} . $new_passs;
	} else {
		for (my $i = 0; $i < $#pass; $i++) {
			$new_passs = $new_passs .  @pass[$i] . '/';
		}
		$str =  'http://' . $ENV{'SERVER_NAME'} . ':' . $ENV{'SERVER_PORT'} . $new_passs;
	}
	
	return $str;
}

sub setCookie {
	local($tmp, $val);
	$val = $_[1];
	$val =~ s/(\W)/sprintf("%%%02X", unpack("C", $1))/eg;
	$tmp = "Set-Cookie: ";
	$tmp .= "$_[0]=$val; ";
	($sec, $min, $hour, $day, $month, $year, $wday) = gmtime(time + 1 * $session_timer * 60);
	my @week    = ('Sun', 'Mon', 'Tue', 'Wed', 'Thr', 'Fri', 'Sat');
	my @months  = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec');
	my $expires = sprintf('%s, %02d\-%s\-%04d %02d:%02d:%02d GMT', $week[$wday], $day, $months[$month], $year+1900, $hour, $min, $sec);
	$tmp .= "expires=$expires;";
	return($tmp);
}

sub clearCookie {
	$tmp = "Set-Cookie: ";
	$tmp .= "$_[0]=xx; ";
	$tmp .= " expires=Tue, 1-Jan-1980 00:00:00 GMT;";
	return($tmp);
}

sub delSession {
	my($del_num, $session_name) = @_;
	@cart = @{$session_cart};
	splice @cart, $del_num, 1;
	$session->param($session_name, \@cart);
}
sub delAllSession {
	my $session_name = $_[0];
	my @cart = @{$session_cart};
	splice @cart, 0;
	$session->param($session_name, \@cart);
}

sub setSession {
	my($item_code, $order_count, $session_name) = @_;
	my $max_index                   = @{$session_cart};
	my @cart                        = @{$session_cart};
	$cart_of_hash{'item_code'}      = $item_code;
	$cart_of_hash{'order_count'}    = $order_count;
	$cart[$max_index]               = \%cart_of_hash;
	$session->param($session_name, \@cart);
}
sub cleanSession {
	$session = CGI::Session->new(undef, $COOKIE{$session_name}, {Directory=>"$_CONFIG_server_ssl_www_root/cgi-bin/session"});
	$session->close;
	$session->delete;
	my $cleaning = CGI::Session::Cleaning->new('driver:File', {Directory=>"$_CONFIG_server_ssl_www_root/cgi-bin/session"} );
	$cleaning->sweep;
}
sub addSession {
	my($item_code, $order_count, $session_name) = @_;
	my $max_index                   = @{$session_cart};
	my @cart                        = @{$session_cart};
	my $count   = 0;
	my $add_flg = 0;
	foreach $value (@{$session_cart}) {
		if($$value{"item_code"} eq $item_code) {
			$order_count =  $order_count + $$value{'order_count'};
			$add_flg = 1;
			last;
		}
		$count++;
	}
	if($add_flg == 1){
		$cart_of_hash{'item_code'}      = $item_code;
		$cart_of_hash{'order_count'}    = $order_count;
		$cart[$count]                   = \%cart_of_hash;
		$session->param($session_name, \@cart);
	} else {
		&setSession($item_code, $order_count, $session_name);
	}
}

sub renewSession {
	my $session_cart = $_[0];
	my @copy_cart;
	
	foreach $value (@{$session_cart}) {
		my $item_code      = $$value{"item_code"};
		my $order_quantity = $FORM{'order_quantity_' . $$value{"item_code"}};
		
		my %cart_of_hash;
		$cart_of_hash{'item_code'}      = $item_code;
		$cart_of_hash{'order_count'}    = $order_quantity;
		push @copy_cart, \%cart_of_hash;
	}
	$session->param($session_name, \@copy_cart);
}

sub session_cart_copy {
	my @copy_cart;
	foreach $value (@{$session_cart}) {
		my %cart_of_hash;
		$cart_of_hash{'item_code'}      = $$value{"item_code"};
		$cart_of_hash{'order_count'}    = $$value{"order_count"};
		push @copy_cart, \%cart_of_hash;
	}
	return @copy_cart;
}
sub summary_order_count {
	my($item_code, $order_count, $session_name) = @_;
	my $max_index                   = @{$session_cart};
	my @cart                        = @{$session_cart};
	my $count = 0;
	my $add_flg = 0;

	foreach $value (@{$session_cart}) {
		if($$value{"item_code"} eq $item_code) {
			$order_count =  $order_count + $$value{'order_count'};
			$add_flg = 1;
			last;
		}
		$count++;
	}
	return $order_count;
}

sub outputErrorOrder {
	my @CART_LOOP = ();
	
	#_注文フォームグリッド
	my $form_file = "$_CONFIG_server_ssl_www_root/cgi-bin/search/item_order_form.cgi";
	open(DATA, $form_file);
	my @form_file = <DATA>;
	close(DATA);
	
	my $must_flg = 0;

	@form_file = sort { (split(/\t/,$a))[6] <=> (split(/\t/,$b))[6] } @form_file;
	#_項目数をカウント
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
			my $error_check_flg_must	= 0;
			my $form_input_flg			= 0;
			
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
					my $pay_s_flg = 1 if ($payment_line[0] == $FORM{'pay_num'});
					if ($payment_line[0] == 4 && $payment_line[2] != 0) {
						$credit_flg = 1;
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
									last;
								} elsif (($agent_line[0] == 1) && ($agent_count == 1)) {
									$credit_flg = 0;
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
									last;
								} elsif (($agent_line[0] == 2) && ($agent_count == 1)) {
									$visa_flg               = 1 if ($agent_line[7] != 0);
									$master_flg             = 1 if ($agent_line[8] != 0);
									$jcb_flg                = 1 if ($agent_line[9] != 0);
									$amex_flg               = 1 if ($agent_line[10] != 0);
									$diners_flg             = 1 if ($agent_line[11] != 0);
									$cerdit_description_flg = 1 if ($agent_line[6] ne '');
									$cerdit_description     = $agent_line[6];
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
			my $text_flg			= 0;
			
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
				order_item_name        => $order_item_name,
				order_item_explan      => $order_item_explan,
				pulldown_flg           => $pulldown_flg,
				pd_name                => $pd_name,
				PULLDOWN_LOOP          => \@PULLDOWN_LOOP,
				checkbox_flg           => $checkbox_flg,
				CHECKBOX_LOOP          => \@CHECKBOX_LOOP,
				radio_flg              => $radio_flg,
				RADIO_LOOP             => \@RADIO_LOOP,
				text_flg               => $text_flg,
				text_id                => $text_id,
				text_item              => MODULE::StringUtil::conversionSpecialChar($text_item),
			};
			push(@CART_LOOP, $hash);
		}
	}
	my @pairs = split(/&/, $FORM{'bpage'});
	foreach my $pair (@pairs) {
		(my $name, my $value) = split(/=/, $pair);
		if (
			($name eq 'saleItem_id') || ($name eq 'pid')      || ($name eq 'stype')    ||
			($name eq 'vtype')       || ($name eq 'ukeyword') || ($name eq 'skeyword') ||
			($name eq 'gkeyword')    || ($name eq 'ckeyword') || ($name eq 'vnum')
		) {
			$FORM{$name} = $value;
		}
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
	
	$template = HTML::Template->new(filename => "./$_CONFIG_template_dir/order_form.tmp");
	$template->param(PURCHASE_LOOP => \@PURCHASE_LOOP_hash);
	$template->param(DISCOUNT_LOOP => \@DISCOUNT_LOOP_hash);
	$template->param(DELIVERY_LOOP => \@DELIVERY_LOOP_hash);
	
	$template->param(
		subtotal_amount      => &convertMoney($subtotal_amount),
		tax_string           => $_CONFIG_tax_marking,
		bpage_url            => $bpage_url,
		discount_flg         => $discount_flg,
		cash_discount        => &convertMoney($cash_discount),
		total_amount         => &convertMoney($total_amount - $total_delivery),
		delivery_flg         => $_CONFIG_carriage_carriage_disp,
		ship_free_flg        => $_CONFIG_carriage_free_shipping_set,
		ship_free_if         => &convertMoney($_CONFIG_carriage_free_shipping_set),
		sp_ship_flg          => $_CONFIG_order_other_view,
		sp_ship_comment      => $_CONFIG_order_other_comment,
		sp_flg               => $FORM{'sp_ship'},
		dhope_flg            => $_CONFIG_order_request_view,
		dhope_commnet        => $_CONFIG_order_request_comment,
		dhope                => &strBrDouble(MODULE::StringUtil::conversionSpecialChar($FORM{'dhope'})),
		mailguide_flg        => $_CONFIG_order_announce_view,
		mailguide_comment    => $_CONFIG_order_announce_comment,
		mailok_flg           => $FORM{'mailguide'},
		idea                 => &strBrDouble(MODULE::StringUtil::conversionSpecialChar($FORM{'idea'})),
		CART_LOOP            => \@CART_LOOP,
		cart_info_url        => $cart_info_url,
		error_on_flg         => $error_on_flg,
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
}

sub checkErrorOrder {
	FORM:foreach (@form_file) {
		my @form_line = split(/\t/, $_);
		my @PAY_LOOP      = ();
		my @PULLDOWN_LOOP = ();
		my @CHECKBOX_LOOP = ();
		my @RADIO_LOOP    = ();
		
		if ($form_line[2] != 0) {
			my $error_check_flg_must	= 0;
			my $daikou_flg				= 0;
			my $visa_flg				= 0;
			my $master_flg				= 0;
			my $jcb_flg					= 0;
			my $amex_flg				= 0;
			my $diners_flg				= 0;
			my $cerdit_description_flg	= 0;
			
			my $form_input_flg;
			if ($form_line[3] == 1) {
				if ($form_line[0] == 1) {
					if (($FORM{'lname'} eq '') || ($FORM{'lname'} eq '')) {
						$must_error_item_name = 'お名前';
						$form_input_flg = 1;
						my $error_hash = {
							must_error_item_name => $must_error_item_name,
							error_input_flg      => $form_input_flg,
						};
						push(@MUST_ERROR_LOOP, $error_hash);
						$error_on_flg = 1;
					}
					if (($FORM{'fname_kana'} eq '') || ($FORM{'lname_kana'} eq '')) {
						$must_error_item_name = 'お名前フリガナ';
						$form_input_flg = 1;
						my $error_hash = {
							must_error_item_name => $must_error_item_name,
							error_input_flg      => $form_input_flg,
						};
						push(@MUST_ERROR_LOOP, $error_hash);
						$error_on_flg = 1;
					}
				} elsif ($form_line[0] == 2) {
					if ($FORM{'cname'} eq '') {
						$must_error_item_name = '法人名';
						$form_input_flg = 1;
						my $error_hash = {
							must_error_item_name => $must_error_item_name,
							error_input_flg      => $form_input_flg,
						};
						push(@MUST_ERROR_LOOP, $error_hash);
						$error_on_flg = 1;
					}
					if ($FORM{'cname_kana'} eq '') {
						$must_error_item_name = '法人名フリガナ';
						$form_input_flg = 1;
						my $error_hash = {
							must_error_item_name => $must_error_item_name,
							error_input_flg      => $form_input_flg,
						};
						push(@MUST_ERROR_LOOP, $error_hash);
						$error_on_flg = 1;
					}
				} elsif ($form_line[0] == 3) {
					if ($FORM{'department'} eq '') {
						$must_error_item_name = '所属部署';
						$form_input_flg = 1;
						my $error_hash = {
							must_error_item_name => $must_error_item_name,
							error_input_flg      => $form_input_flg,
						};
						push(@MUST_ERROR_LOOP, $error_hash);
						$error_on_flg = 1;
					}
				} elsif ($form_line[0] == 4) {
					if (($FORM{'pcode_first'} eq '') || ($FORM{'pcode_last'} eq '') || ($FORM{'address'} eq '')) {
						$must_error_item_name = 'ご住所';
						$form_input_flg = 1;
						my $error_hash = {
							must_error_item_name => $must_error_item_name,
							error_input_flg      => $form_input_flg,
						};
						push(@MUST_ERROR_LOOP, $error_hash);
						$error_on_flg = 1;
					}
					if ($FORM{'todouhuken'} eq '') {
						$must_error_item_name = 'ご住所';
						$form_input_flg = 0;
						my $error_hash = {
							must_error_item_name => $must_error_item_name,
							error_input_flg      => $form_input_flg,
						};
						push(@MUST_ERROR_LOOP, $error_hash);
						$error_on_flg = 1;
					}
				} elsif ($form_line[0] == 5) {
					if ($FORM{'mail'} eq '') {
						$must_error_item_name = 'メールアドレス';
						$form_input_flg = 1;
						my $error_hash = {
							must_error_item_name => $must_error_item_name,
							error_input_flg      => $form_input_flg,
						};
						push(@MUST_ERROR_LOOP, $error_hash);
						$error_on_flg = 1;
					}
					if ($FORM{'mail_check'} eq '') {
						$must_error_item_name = 'メールアドレス(確認用)';
						$form_input_flg = 1;
						my $error_hash = {
							must_error_item_name => $must_error_item_name,
							error_input_flg      => $form_input_flg,
						};
						push(@MUST_ERROR_LOOP, $error_hash);
						$error_on_flg = 1;
					}
				} elsif ($form_line[0] == 6) {
					if ($FORM{'pay_num'} eq '') {
						$must_error_item_name = '支払方法';
						$form_input_flg = 0;
						my $error_hash = {
							must_error_item_name => $must_error_item_name,
							error_input_flg      => $form_input_flg,
						};
						push(@MUST_ERROR_LOOP, $error_hash);
						$error_on_flg = 1;
					}
				} elsif ($form_line[0] == 7) {
					if (($FORM{'pnum_1'} eq '') || ($FORM{'pnum_2'} eq '') || ($FORM{'pnum_3'} eq '')) {
						$must_error_item_name = '電話番号';
						$form_input_flg = 1;
						my $error_hash = {
							must_error_item_name => $must_error_item_name,
							error_input_flg      => $form_input_flg,
						};
						push(@MUST_ERROR_LOOP, $error_hash);
						$error_on_flg = 1;
					}
				} elsif ($form_line[0] == 8) {
					if (($FORM{'fnum_1'} eq '') || ($FORM{'fnum_2'} eq '') || ($FORM{'fnum_3'} eq '')) {
						$must_error_item_name = 'FAX番号';
						$form_input_flg = 1;
						my $error_hash = {
							must_error_item_name => $must_error_item_name,
							error_input_flg      => $form_input_flg,
						};
						push(@MUST_ERROR_LOOP, $error_hash);
						$error_on_flg = 1;
					}
				} elsif ($form_line[0] == 9) {
					if (($FORM{'day_pnum_1'} eq '') || ($FORM{'day_pnum_2'} eq '') || ($FORM{'day_pnum_3'} eq '')) {
						$must_error_item_name = '日中の連絡先';
						$form_input_flg = 1;
						my $error_hash = {
							must_error_item_name => $must_error_item_name,
							error_input_flg      => $form_input_flg,
						};
						push(@MUST_ERROR_LOOP, $error_hash);
						$error_on_flg = 1;
					}
				} elsif ($form_line[0] == 10) {
					if (($FORM{'birthyear'} eq '') || ($FORM{'birthmonth'} eq '') || ($FORM{'birthday'} eq '')) {
						$must_error_item_name = '生年月日';
						$form_input_flg = 1;
						my $error_hash = {
							must_error_item_name => $must_error_item_name,
							error_input_flg      => $form_input_flg,
						};
						push(@MUST_ERROR_LOOP, $error_hash);
						$error_on_flg = 1;
					}
				} elsif ($form_line[0] == 11) {
					if ($FORM{'sei_fm_flg'} eq '') {
						$must_error_item_name = '性別';
						$form_input_flg = 0;
						my $error_hash = {
							must_error_item_name => $must_error_item_name,
							error_input_flg      => $form_input_flg,
						};
						push(@MUST_ERROR_LOOP, $error_hash);
						$error_on_flg = 1;
					}
				} elsif ($form_line[9] eq 'R') {
					if ($FORM{"order_$form_line[0]"} eq '') {
						$must_error_item_name = $form_line[1];
						$form_input_flg = 0;
						my $error_hash = {
							must_error_item_name => $must_error_item_name,
							error_input_flg      => $form_input_flg,
						};
						push(@MUST_ERROR_LOOP, $error_hash);
						$error_on_flg = 1;
					}
				} elsif ($form_line[9] eq 'A') {
					if (&strTrim($FORM{"order_$form_line[0]"}) eq '') {
						$must_error_item_name = $form_line[1];
						$form_input_flg = 1;
						my $error_hash = {
							must_error_item_name => $must_error_item_name,
							error_input_flg      => $form_input_flg,
						};
						push(@MUST_ERROR_LOOP, $error_hash);
						$error_on_flg = 1;
					}
				} elsif ($form_line[9] eq 'S') {
					if ($FORM{"order_$form_line[0]"} eq '') {
						$must_error_item_name = $form_line[1];
						$form_input_flg = 0;
						my $error_hash = {
							must_error_item_name => $must_error_item_name,
							error_input_flg      => $form_input_flg,
						};
						push(@MUST_ERROR_LOOP, $error_hash);
						$error_on_flg = 1;
					}
				} elsif ($form_line[9] eq 'C') {
					my @option_list = split(/<RETURN>/, $form_line[10]);
					chomp @option_list;
					my $i = 1;
					my $check_list_check = 0;
					foreach (@option_list) {
						my $c_id = 'order_' . $form_line[0] . '_' . $i;
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
							must_error_item_name => $must_error_item_name,
							error_input_flg      => $form_input_flg,
						};
						push(@MUST_ERROR_LOOP, $error_hash);
						$error_on_flg = 1;
					}
				}
			}
			if ($form_line[0] == 1) {
				if ($FORM{'fname_kana'} ne '' || $FORM{'lname_kana'} ne '') {
					#_カナチェック
					unless (&strKanaCheck($FORM{'fname_kana'}) && &strKanaCheck($FORM{'lname_kana'})) {
						my $error_hash = {
							incorrect_error_item_name => 'お名前フリガナ',
						};
						push(@INCORRECT_ERROR_LOOP, $error_hash);
						$error_on_flg = 1;
					}
				}
			}
			if ($form_line[0] == 2) {
				if ($FORM{'cname_kana'} ne '') {
					#_カナチェック
					unless (&strKanaCheck($FORM{'cname_kana'})) {
						my $error_hash = {
							incorrect_error_item_name => '法人名フリガナ',
						};
						push(@INCORRECT_ERROR_LOOP, $error_hash);
						$error_on_flg = 1;
					}
				}
			}
			if ($form_line[0] == 5) {
				if ($FORM{'mail'} ne '' || $FORM{'mail_check'} ne '') {
					#_メールアドレスチェック
					my $mail_check_flg;
					unless ($FORM{'mail'} eq $FORM{'mail_check'}) {
						$email_error_flg++;
						$error_on_flg = 1;
					}
					unless (&mailChecker($FORM{'mail'})) {
						$mail_check_flg++;
					}
					if ($mail_check_flg) {
						my $error_hash = {
							incorrect_error_item_name => 'メールアドレス',
						};
						push(@INCORRECT_ERROR_LOOP, $error_hash);
						$error_on_flg = 1;
					}
				}
			}
			if ($form_line[0] == 4) {
				#_郵便番号チェック
				my $error_hash;
				if ($FORM{'pcode_first'} ne '') {
					unless (&strIntCheck($FORM{'pcode_first'})) {
						$error_hash = {
							incorrect_error_item_name => 'ご住所',
						};
					}
				}
				if ($FORM{'pcode_last'} ne '') {
					unless (&strIntCheck($FORM{'pcode_last'})) {
						$error_hash = {
							incorrect_error_item_name => 'ご住所',
						};
					}
				}
				if ($error_hash) {
					push(@INCORRECT_ERROR_LOOP, $error_hash);
					$error_on_flg = 1;
				}
			}
			if ($form_line[0] == 10) {
				#_日付チェック
				if (($FORM{'birthyear'} ne '') || ($FORM{'birthmonth'} ne '') || ($FORM{'birthday'} ne '')) {
					unless (&strDateCheck($FORM{'birthyear'}, $FORM{'birthmonth'}, $FORM{'birthday'})) {
						my $error_hash = {
							incorrect_error_item_name => '生年月日',
						};
						push(@INCORRECT_ERROR_LOOP, $error_hash);
						$error_on_flg = 1;
					}
				}
			}
		}
	}
}

sub outputErrorDelivery {
	my @SP_CART_LOOP;
	#_注文フォームグリッド
	my $form_file = "$_CONFIG_server_ssl_www_root/cgi-bin/search/item_order_form.cgi";
	open(DATA, $form_file);
	our @form_file = <DATA>;
	close(DATA);
	
	my $sp_must_flg = 0;
	
	@form_file = sort { (split(/\t/,$a))[6] <=> (split(/\t/,$b))[6] } @form_file;
	
	foreach (@form_file) {
		my @form_line = split(/\t/, $_);
		my @PAY_LOOP      = ();
		my @PULLDOWN_LOOP = ();
		my @CHECKBOX_LOOP = ();
		my @RADIO_LOOP    = ();
		
		if ($form_line[4] != 0) {
			my $cerdit_description_flg	= 0;
			my $daikou_flg				= 0;
			my $visa_flg				= 0;
			my $master_flg				= 0;
			my $jcb_flg					= 0;
			my $amex_flg				= 0;
			my $diners_flg				= 0;

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
			my $checkbox_flg		= 0;
			my $radio_flg			= 0;
			my $order_item_name		= '';
			my $order_item_explan	= '';
			my $text_id				= '';
			my $text_item			= '';
			my $text_flg			= 0;
			
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
				sp_sei_m_flg         => $FORM{'sp_sei_m_flg'},
				sp_sei_f_flg         => $FORM{'sp_sei_f_flg'},
				sp_addItem_flg       => $addItem_flg,
				sp_order_item_name   => $order_item_name,
				sp_order_item_explan => $order_item_explan,
				sp_pulldown_flg      => $pulldown_flg,
				sp_pd_name           => $pd_name,
				sp_PULLDOWN_LOOP     => \@PULLDOWN_LOOP,
				sp_checkbox_flg      => $checkbox_flg,
				sp_CHECKBOX_LOOP     => \@CHECKBOX_LOOP,
				sp_radio_flg         => $radio_flg,
				sp_RADIO_LOOP        => \@RADIO_LOOP,
				sp_text_flg          => $text_flg,
				sp_text_id           => $text_id,
				sp_text_item         => MODULE::StringUtil::conversionSpecialChar($text_item),
			};
			push(@SP_CART_LOOP, $hash);
			
		}
	}
	my @pairs = split(/&/, $FORM{'bpage'});
	foreach my $pair (@pairs) {
		(my $name, my $value) = split(/=/, $pair);
		if (
			($name eq 'saleItem_id') || ($name eq 'pid')      || ($name eq 'stype')    ||
			($name eq 'vtype')       || ($name eq 'ukeyword') || ($name eq 'skeyword') ||
			($name eq 'gkeyword')    || ($name eq 'ckeyword') || ($name eq 'vnum')
		) {
			$FORM{$name} = $value;
		}
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
	
	$template = HTML::Template->new(filename => "./$_CONFIG_template_dir/order_form_delivery.tmp");
	$template->param(PURCHASE_LOOP => \@PURCHASE_LOOP_hash);
	$template->param(DISCOUNT_LOOP => \@DISCOUNT_LOOP_hash);
	$template->param(DELIVERY_LOOP => \@DELIVERY_LOOP_hash);
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
				my $text_flg			= 0;
				
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
							text_id                => $text_id,
							text_item              => $text_item,
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
					text_id                => $text_id,
					text_item              => $text_item,
				};
				push(@CART_LOOP, $hash);
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
	$address_flg     = 1 if (($FORM{'pcode_first'}) || ($FORM{'pcode_last'}));
	$mail_flg        = 1 if (($FORM{'mail'}) || ($FORM{'mail_check'}));
	$pay_flg         = 1 if ($FORM{'pay_num'});
	$pnum_flg        = 1 if (($FORM{'pnum_1'}) || ($FORM{'pnum_2'}) || ($FORM{'pnum_3'}));
	$fnum_flg        = 1 if (($FORM{'fnum_1'}) || ($FORM{'fnum_2'}) || ($FORM{'fnum_3'}));
	$day_pnum_flg    = 1 if (($FORM{'day_pnum_1'}) || ($FORM{'day_pnum_2'}) || ($FORM{'day_pnum_3'}));
	$birth_flg       = 1 if (($FORM{'birthyear'}) || ($FORM{'birthmonth'}) || ($FORM{'birthday'}));
	$dhope_flg       = 1 if ($FORM{'dhope'});
	$mailguide_flg   = 1 if ($FORM{'mailguide'});
	my $bpage_u_flg = 0;
	my $bpage_s_flg = 0;
	my $bpage_g_flg = 0;
	my $bpage_c_flg = 0;
	my $bpage_flg   = 0;
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
		todouhuken              => $todouhuken,
		address                 => MODULE::StringUtil::conversionSpecialChar($FORM{'address'}),
		mail_flg                => $mail_flg,
		mail                    => MODULE::StringUtil::conversionSpecialChar($FORM{'mail'}),
		mail_check              => MODULE::StringUtil::conversionSpecialChar($FORM{'mail_check'}),
		pay_flg                 => $pay_flg,
		pay_num                 => $FORM{'pay_num'},
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
		dhope                   => &strBrDouble(MODULE::StringUtil::conversionSpecialChar($FORM{'dhope'})),
		mailguide_flg           => $mailguide_flg,
		mailok_flg              => $FORM{'mailguide'},
		idea                    => &strBrDouble(MODULE::StringUtil::conversionSpecialChar($FORM{'idea'})),
		
		subtotal_amount         => &convertMoney($subtotal_amount),
		tax_string              => $_CONFIG_tax_marking,
		bpage_url               => $bpage_url,
		discount_flg            => $discount_flg,
		cash_discount           => &convertMoney($cash_discount),
		total_amount            => &convertMoney($total_amount - $total_delivery),
		delivery_flg            => $_CONFIG_carriage_carriage_disp,
		ship_free_flg           => $_CONFIG_carriage_free_shipping_set,
		ship_free_if            => &convertMoney($_CONFIG_carriage_free_shipping_set),
		addItem_flg             => $addItem_flg,
		CART_LOOP               => \@CART_LOOP,
		SP_CART_LOOP            => \@SP_CART_LOOP,
		error_on_flg            => $sp_error_on_flg,
		SP_MUST_ERROR_LOOP      => \@SP_MUST_ERROR_LOOP,
		SP_INCORRECT_ERROR_LOOP => \@SP_INCORRECT_ERROR_LOOP,
		email_error_flg         => $sp_email_error_flg,
		agent_error_flg         => $sp_agent_error_flg,
		
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
}

sub checkErrorDelivery {
	SPFORM:foreach (@form_file) {
		my @form_line = split(/\t/, $_);
		my @PAY_LOOP      = ();
		my @PULLDOWN_LOOP = ();
		my @CHECKBOX_LOOP = ();
		my @RADIO_LOOP    = ();
		
		if ($form_line[4] != 0) {
			my $error_check_flg_must	= 0;
			my $daikou_flg				= 0;
			my $visa_flg				= 0;
			my $master_flg				= 0;
			my $jcb_flg					= 0;
			my $amex_flg				= 0;
			my $diners_flg				= 0;
			my $cerdit_description_flg	= 0;
			
			if ($form_line[5] == 1) {
				if ($form_line[0] == 1) {
					if (($FORM{'sp_lname'} eq '') || ($FORM{'sp_lname'} eq '')) {
						$must_error_item_name = 'お名前';
						$form_input_flg = 1;
						my $error_hash = {
							must_error_sp_item_name => $must_error_item_name,
							sp_error_input_flg      => $form_input_flg,
						};
						push(@SP_MUST_ERROR_LOOP, $error_hash);
						$sp_error_on_flg = 1;
					}
					if (($FORM{'sp_fname_kana'} eq '') || ($FORM{'sp_lname_kana'} eq '')) {
						$must_error_item_name = 'お名前フリガナ';
						$form_input_flg = 1;
						my $error_hash = {
							must_error_sp_item_name => $must_error_item_name,
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
							must_error_sp_item_name => $must_error_item_name,
							sp_error_input_flg      => $form_input_flg,
						};
						push(@SP_MUST_ERROR_LOOP, $error_hash);
						$sp_error_on_flg = 1;
					}
					if ($FORM{'sp_cname_kana'} eq '') {
						$must_error_item_name = '法人名フリガナ';
						$form_input_flg = 1;
						my $error_hash = {
							must_error_sp_item_name => $must_error_item_name,
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
							must_error_sp_item_name => $must_error_item_name,
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
							must_error_sp_item_name => $must_error_item_name,
							sp_error_input_flg      => $form_input_flg,
						};
						push(@SP_MUST_ERROR_LOOP, $error_hash);
						$sp_error_on_flg = 1;
					}
					if ($FORM{'sp_todouhuken'} eq '') {
						$must_error_item_name = 'ご住所';
						$form_input_flg = 0;
						my $error_hash = {
							must_error_sp_item_name => $must_error_item_name,
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
							must_error_sp_item_name => $must_error_item_name,
							sp_error_input_flg      => $form_input_flg,
						};
						push(@SP_MUST_ERROR_LOOP, $error_hash);
						$sp_error_on_flg = 1;
					}
					if ($FORM{'sp_mail_check'} eq '') {
						$must_error_item_name = 'メールアドレス(確認用)';
						$form_input_flg = 1;
						my $error_hash = {
							must_error_sp_item_name => $must_error_item_name,
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
							must_error_sp_item_name => $must_error_item_name,
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
							must_error_sp_item_name => $must_error_item_name,
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
							must_error_sp_item_name => $must_error_item_name,
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
							must_error_sp_item_name => $must_error_item_name,
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
							must_error_sp_item_name => $must_error_item_name,
							sp_error_input_flg      => $form_input_flg,
						};
						push(@SP_MUST_ERROR_LOOP, $error_hash);
						$sp_error_on_flg = 1;
					}
				} elsif ($form_line[9] eq 'R') {
					if ($FORM{"sp_order_$form_line[0]"} eq '') {
						$must_error_item_name = $form_line[1];
						$form_input_flg = 0;
						my $error_hash = {
							must_error_sp_item_name => $must_error_item_name,
							sp_error_input_flg      => $form_input_flg,
						};
						push(@SP_MUST_ERROR_LOOP, $error_hash);
						$sp_error_on_flg = 1;
					}
				} elsif ($form_line[9] eq 'A') {
					if (&strTrim($FORM{"sp_order_$form_line[0]"}) eq '') {
						$must_error_item_name = $form_line[1];
						$form_input_flg = 1;
						my $error_hash = {
							must_error_sp_item_name => $must_error_item_name,
							sp_error_input_flg      => $form_input_flg,
						};
						push(@SP_MUST_ERROR_LOOP, $error_hash);
						$sp_error_on_flg = 1;
					}
				} elsif ($form_line[9] eq 'S') {
					if ($FORM{"sp_order_$form_line[0]"} eq '') {
						$must_error_item_name = $form_line[1];
						$form_input_flg = 0;
						my $error_hash = {
							must_error_sp_item_name => $must_error_item_name,
							sp_error_input_flg      => $form_input_flg,
						};
						push(@SP_MUST_ERROR_LOOP, $error_hash);
						$sp_error_on_flg = 1;
					}
				} elsif ($form_line[9] eq 'C') {
					my @option_list = split(/\\n/, $form_line[10]);
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
							must_error_sp_item_name => $must_error_item_name,
							sp_error_input_flg      => $form_input_flg,
						};
						push(@SP_MUST_ERROR_LOOP, $error_hash);
						$sp_error_on_flg = 1;
					}
				}
			}
			if ($form_line[0] == 1) {
				if ($FORM{'sp_fname_kana'} ne '' || $FORM{'sp_lname_kana'} ne '') {
					#_カナチェック
					unless (&strKanaCheck($FORM{'sp_fname_kana'}) && &strKanaCheck($FORM{'sp_lname_kana'})) {
						my $error_hash = {
							incorrect_error_sp_item_name => 'お名前フリガナ',
						};
						push(@SP_INCORRECT_ERROR_LOOP, $error_hash);
						$sp_error_on_flg = 1;
					}
				}
			}
			if ($form_line[0] == 2) {
				if ($FORM{'sp_cname_kana'} ne '') {
					#_カナチェック
					unless (&strKanaCheck($FORM{'sp_cname_kana'})) {
						my $error_hash = {
							incorrect_error_sp_item_name => '法人名フリガナ',
						};
						push(@SP_INCORRECT_ERROR_LOOP, $error_hash);
						$sp_error_on_flg = 1;
					}
				}
			}
			if ($form_line[0] == 5) {
				if ($FORM{'sp_mail'} ne '' || $FORM{'sp_mail_check'} ne '') {
					#_メールアドレスチェック
					my $mail_check_flg;
					unless ($FORM{'sp_mail'} eq $FORM{'sp_mail_check'}) {
						$sp_email_error_flg++;
						$sp_error_on_flg = 1;
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
				if ($FORM{'sp_pcode_first'} ne '') {
					unless (&strIntCheck($FORM{'sp_pcode_first'})) {
						$error_hash = {
							incorrect_error_sp_item_name => 'ご住所',
						};
					}
				}
				if ($FORM{'sp_pcode_last'} ne '') {
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

sub cartLoopView1 {
	my $flg = $_[0];
	my $cnt = 0;
	my $cart_url;
	if ($flg == 1) {
		$cart_url = sprintf('%s/cgi-bin/order_cart_info.cgi', $_CONFIG_server_ssl_www_root);
	} else {
		$cart_url = './order_cart_info.cgi';
	}
	
	foreach $value (@{$session_cart}) {
		
		$$value{"item_code"} =~ /^(\d{2})(\d{2})(\d{8})(\d{2})(\d{2})/;
		
		my $insert_line;
		
		my $line_cc = $1;
		my $line_gc = $2;
		my $line_ic = $3;
		my $line_vari_v = $4;
		my $line_vari_h = $5;
		
		my $data_file;
		if ($flg == 1) {
			$data_file = sprintf('%s/cgi-bin/search/%02d/%02d.cgi', $_CONFIG_server_ssl_www_root, $line_cc, $line_gc);
		} else {
			$data_file = sprintf('./search/%02d/%02d.cgi', $line_cc, $line_gc);
		}
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
		
		my $val_data_file;
		if ($flg == 1) {
			$val_data_file = sprintf('%s/cgi-bin/search/%02d/%02d_variation.cgi', $_CONFIG_server_ssl_www_root, $line_cc, $line_gc);
		} else {
			$val_data_file = sprintf('./search/%02d/%02d_variation.cgi', $line_cc, $line_gc);
		}
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
				$unit_price   = $item_money_sp_price_tax;
			} else {
				$pretax_price = $item_including_tax_price;
				$unit_price   = $item_including_tax_price;
			}
		} else {
			if ($item_sp_price_flag != 0) {
				$pretax_price = $item_money_sp_price;
				$unit_price   = $item_money_sp_price_tax;
			} else {
				$pretax_price = $item_price;
				$unit_price   = $item_including_tax_price;
			}
		}
		my $hash = "";
		my $amount = $unit_price * $$value{"order_count"};
		
		$subtotal_amount += $amount;
		$vari_yoko_name = $item_vari_h_clm[$line_vari_h];
		$vari_tate_name = $item_vari_v_clm[$line_vari_v];
		$hash = {
			cart_url          => $cart_url,
			main_img_url      => &checkUri(&imgCheck($item_cmd_image_uri_nail, $item_cmd_image_uri_main, 'S'), 1),
			hinmei            => $item_name_articles,
			unit_price        => &convertMoney($unit_price),
			pretax_price      => &convertMoney($pretax_price),
			pretax_flg        => $pretax_flg,
			amount            => &convertMoney($amount) . '円',
			pretax_flg        => $pretax_flg,
			delivery_name     => &deliveryOut($item_deli_type_id),
			cid               => $cnt,
			bpage_para        => $bpage_para,
			order_quantity    => $$value{"order_count"},
			variation_flg     => $item_vari_disp,
			vari_yoko_name    => $vari_yoko_name,
			vari_tate_name    => $vari_tate_name,
			order_quantity_id => $$value{"item_code"},
		};
		push(@LOOP_hash, $hash);
		$cnt = $cnt + 1;
		$deliveryCheck[$item_deli_type_id]++;
		$cart_hit_flg++;
	}
}

sub cartLoopCashDiscount{
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
}

sub cartLoopDelivery {
	my $flg = $_[0];
	my $data_file;
	if ($flg == 1) {
		$data_file = sprintf('%s/cgi-bin/item_delivery.cgi', $_CONFIG_server_ssl_www_root);
	} else {
		$data_file = './item_delivery.cgi';
	}
	open(DATA, $data_file);
	my @data_file = <DATA>;
	close(DATA);
	chomp @data_file;
	
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
			delivery_comment     => $data_line[51],
			delivery_type_flg    => $delivery_type_flg,
			delivery_uniform     => $delivery_uniform,

		};
		push(@LOOP_hash, $hash);
	}
}

sub cartLoopBpage {
	my ($saleItem_id, $pid, $ukeyword, $skeyword, $gkeyword, $ckeyword) = @_;
	my ($bpage_flg, $bpage_u_flg, $bpage_s_flg, $bpage_g_flg, $bpage_c_flg, $send_keyword);
	
	$bpage_flg = 1 if ($FORM{'saleItem_id'} ne '' || $FORM{'pid'} eq '');
	if ($ukeyword) {
		$bpage_u_flg = 1;
		$send_keyword = sprintf('&ukeyword=%s', $FORM{'ukeyword'});
	}
	if ($skeyword) {
		$bpage_s_flg = 1;
		$send_keyword = sprintf('&skeyword=%s', $FORM{'skeyword'});
	}
	if ($gkeyword) {
		$bpage_g_flg = 1;
		$send_keyword = sprintf('&gkeyword=%s', $FORM{'gkeyword'});
	}
	if ($ckeyword) {
		$bpage_c_flg = 1;
		$send_keyword = sprintf('&ckeyword=%s', $FORM{'ckeyword'});
	}
	return ($bpage_flg, $bpage_u_flg, $bpage_s_flg, $bpage_g_flg, $bpage_c_flg, $send_keyword);
}

sub askFormOutput {
	my ($flg, $parts_file) = @_;
	@$parts_file = sort { (split(/\t/,$a))[3] <=> (split(/\t/,$b))[3] } @$parts_file;
	my (@FORM_LOOP, $ask_necessity_check);
	foreach (@$parts_file) {
		my @parts_line = split(/\t/, $_);
		if ($FORM{'pid'} eq $parts_line[1] && $parts_line[11] == 1) {
			my ($form_value, $form_value_1, $form_value_2, @FORM_SUB_LOOP, $form_text_flg, $form_area_flg, $form_radio_flg, $form_check_flg, $form_select_flg, $form_mail_flg, $form_address_flg, $form_date_flg, $form_zen_numeric_flg);
			if ($flg) {
				$form_value = &strBrDouble($FORM{"ask_input_value_$parts_line[0]"});
			}
			
			if ($parts_line[6] eq 'T') {
				$form_text_flg = 1;
			}
			if ($parts_line[6] eq 'A') {
				$form_area_flg = 1;
			}
			if ($parts_line[6] eq 'R') {
				$form_radio_flg = 1;
				$form_sub_value;
				my @option_list = split(/<RETURN>/, $parts_line[9]);
				chomp @option_list;
				my $i = 1;
				foreach (@option_list) {
					my $form_sub_id    = $i;
					my $form_sub_title = $_;
					my $form_sub_value = ' checked' if $FORM{"ask_input_value_$parts_line[0]"} == $i;
					my $sub_hash = {
						form_id         => $parts_line[0],
						form_sub_id     => $form_sub_id,
						form_sub_title  => $form_sub_title,
						form_value      => $form_sub_value,
					};
					push(@FORM_SUB_LOOP, $sub_hash);
					$i++;
				}
			}
			if ($parts_line[6] eq 'C') {
				$form_check_flg = 1;
				my @check_value_list;
				if ($FORM{"ask_input_value_$parts_line[0]"} ne '') {
					@check_value_list = split(/\-/, $FORM{"ask_input_value_$parts_line[0]"});
					foreach (@check_value_list) {
						$FORM{"ask_input_value_$parts_line[0]_$_"} = 1;
					}
				}
				my @option_list = split(/<RETURN>/, $parts_line[9]);
				chomp @option_list;
				my $i = 1;
				foreach (@option_list) {
					my $form_sub_id    = $i;
					my $form_sub_title = $_;
					my $form_sub_value = ' checked' if $FORM{"ask_input_value_$parts_line[0]_$i"};
					my $sub_hash = {
						form_id         => $parts_line[0],
						form_sub_id     => $form_sub_id,
						form_sub_title  => $form_sub_title,
						form_value      => $form_sub_value,
					};
					push(@FORM_SUB_LOOP, $sub_hash);
					$i++;
				}
			}
			if ($parts_line[6] eq 'S') {
				$form_select_flg = 1;
				my @option_list = split(/<RETURN>/, $parts_line[9]);
				chomp @option_list;
				my $i = 1;
				foreach (@option_list) {
					my $form_sub_id    = $i;
					my $form_sub_title = $_;
					my $form_sub_value = ' selected' if $FORM{"ask_input_value_$parts_line[0]"} == $i;
					my $sub_hash = {
						form_sub_id     => $form_sub_id,
						form_sub_title  => $form_sub_title,
						form_value      => $form_sub_value,
					};
					push(@FORM_SUB_LOOP, $sub_hash);
					$i++;
				}
			}
			if ($parts_line[6] eq 'M') {
				$form_mail_flg = 1;
			}
			if ($parts_line[6] eq 'J') {
				$form_address_flg = 1;
				$form_value_1 = &strBrDouble($FORM{"ask_input_value_$parts_line[0]_1"});
				$form_value_2 = &strBrDouble($FORM{"ask_input_value_$parts_line[0]_2"});
				for ($i = 1; $i <= 47; $i++) {
					if ($FORM{"ask_input_value_$parts_line[0]_3"} == $i) {
						$area_flg[$i] = 1;
					} else {
						$area_flg[$i] = 0;
					}
				}
				$form_value_4 = &strBrDouble($FORM{"ask_input_value_$parts_line[0]_4"});
			}
			if ($parts_line[6] eq 'B') {
				$form_date_flg = 1;
				$form_value_1 = &strBrDouble($FORM{"ask_input_value_$parts_line[0]_1"});
				$form_value_2 = &strBrDouble($FORM{"ask_input_value_$parts_line[0]_2"});
				$form_value_3 = &strBrDouble($FORM{"ask_input_value_$parts_line[0]_3"});
			}
			if ($parts_line[6] eq 'N') {
				$form_zen_numeric_flg = 1;
			}
			$parts_line[5] = &checkUri($parts_line[5], 1) if $parts_line[5];
			my $form_hash = {
				form_input_icon    => $parts_line[5],
				form_input_title   => $parts_line[4],
				form_necessity_flg => $parts_line[10],
				form_id            => $parts_line[0],
				form_maxlength     => $parts_line[7],
				form_rows          => $parts_line[8],
				form_value         => MODULE::StringUtil::conversionSpecialChar($form_value),
				form_text_flg      => $form_text_flg,
				form_area_flg      => $form_area_flg,
				form_radio_flg     => $form_radio_flg,
				form_check_flg     => $form_check_flg,
				form_select_flg    => $form_select_flg,
				form_mail_flg      => $form_mail_flg,
				form_address_flg   => $form_address_flg,
				form_date_flg      => $form_date_flg,
				form_zen_numeric_flg => $form_zen_numeric_flg,
				form_value_1       => MODULE::StringUtil::conversionSpecialChar($form_value_1),
				form_value_2       => MODULE::StringUtil::conversionSpecialChar($form_value_2),
				area1_flg          => $area_flg[1],
				area2_flg          => $area_flg[2],
				area3_flg          => $area_flg[3],
				area4_flg          => $area_flg[4],
				area5_flg          => $area_flg[5],
				area6_flg          => $area_flg[6],
				area7_flg          => $area_flg[7],
				area8_flg          => $area_flg[8],
				area9_flg          => $area_flg[9],
				area10_flg         => $area_flg[10],
				area11_flg         => $area_flg[11],
				area12_flg         => $area_flg[12],
				area13_flg         => $area_flg[13],
				area14_flg         => $area_flg[14],
				area15_flg         => $area_flg[15],
				area16_flg         => $area_flg[16],
				area17_flg         => $area_flg[17],
				area18_flg         => $area_flg[18],
				area19_flg         => $area_flg[19],
				area20_flg         => $area_flg[20],
				area21_flg         => $area_flg[21],
				area22_flg         => $area_flg[22],
				area23_flg         => $area_flg[23],
				area24_flg         => $area_flg[24],
				area25_flg         => $area_flg[25],
				area26_flg         => $area_flg[26],
				area27_flg         => $area_flg[27],
				area28_flg         => $area_flg[28],
				area29_flg         => $area_flg[29],
				area30_flg         => $area_flg[30],
				area31_flg         => $area_flg[31],
				area32_flg         => $area_flg[32],
				area33_flg         => $area_flg[33],
				area34_flg         => $area_flg[34],
				area35_flg         => $area_flg[35],
				area36_flg         => $area_flg[36],
				area37_flg         => $area_flg[37],
				area38_flg         => $area_flg[38],
				area39_flg         => $area_flg[39],
				area40_flg         => $area_flg[40],
				area41_flg         => $area_flg[41],
				area42_flg         => $area_flg[42],
				area43_flg         => $area_flg[43],
				area44_flg         => $area_flg[44],
				area45_flg         => $area_flg[45],
				area46_flg         => $area_flg[46],
				area47_flg         => $area_flg[47],
				form_value_3       => MODULE::StringUtil::conversionSpecialChar($form_value_3),
				form_value_4       => MODULE::StringUtil::conversionSpecialChar($form_value_4),
				FORM_SUB_LOOP      => \@FORM_SUB_LOOP,
			};
			push(@FORM_LOOP, $form_hash);
			$ask_necessity_check++ if $parts_line[10];
		}
	}
	return (\@FORM_LOOP, $ask_necessity_check);
}

sub askFormMeta {
	my ($load_file)= @_;
	my @return_line;
	foreach (@$load_file) {
		my ($meta_title, $meta_description, $meta_keywords, $header_addition);
		chomp $_;
		my @load_line = split(/\t/, $_);
		if ($load_line[0] == $FORM{'pid'}) {
			@return_line = @load_line;
			if ($load_line[9] == 1) {
				$meta_title       = $_CONFIG_site_title;
				$meta_description = &strBr($_CONFIG_site_outline_site, 1);
				for (my $i = 1; $i <= 10; $i++) {
					if ($_CONFIG_site_keyword[$i]) {
						$meta_keywords .= $_CONFIG_site_keyword[$i] . ',';
					}
				}
				chop $meta_keywords;
			} else {
				$meta_title       = $load_line[10];
				$meta_description = &strBr($load_line[11], 1);
				for (my $i = 12; $i <= 21; $i++) {
					if ($load_line[$i]) {
						$meta_keywords .= $load_line[$i] . ',';
					}
				}
				chop $meta_keywords;
			}
			if ($load_line[23] == 1) {
				$header_addition = $_CONFIG_site_header_addition;
			} else {
				$header_addition = $load_line[22];
				$header_addition =~ s/<RETURN>/\x0D\x0A/g;
				$header_addition =~ s/<TAB>/\t/g;
			}
			$template->param(
				meta_title          => $meta_title,
				meta_description    => $meta_description,
				meta_keywords       => $meta_keywords,
				header_addition     => $header_addition,
			);
			last;
		}
	}
	return @return_line;
}

sub getTotalStock {
	my ($cc, $gc, $ic, $type) = @_;
	my $stock_count;
	my $alert_count;
	my $stock_file = sprintf('./search/%02d/%02d_stock.cgi', $cc, $gc);
	open(DATA, $stock_file);
	my @stock_file = <DATA>;
	close(DATA);
	
	@stock_file = sort { (split(/\,/,$a))[0] <=> (split(/\,/,$b))[0] } @stock_file;
	foreach (@stock_file) {
		chomp $_;
		my @stock_line = split(/\t/, $_);
		$stock_line[0] =~ /(\d{8})(\d{2})(\d{2})/;
		if (($1 eq $ic) && ($2 eq '00') && ($3 eq '00')) {
			$stock_count = $stock_line[1];
			$alert_count = $stock_line[2];
			last;
		}
	}
	if ($type == 1) {
		return ($stock_count, $alert_count);
	} else {
		return $stock_count;
	}
}


sub httpHeadOutput {
	my ($head)= @_;
	#print "HTTP/1.1 200 OK\n";
	if ($head ne '') {
		print $head;
	}
	#print "Connection: close\n";
	print $_CONFIG_base_head;
}

sub isWhatsNewIcon {
	my $flg = $_[0];
	my $entry_date = $_[1];
	my $term = $_[2];
	my $result = '';
	if ($flg) {
		($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = localtime(time - 60 * 60 * 24 * $term);
		$check_date = sprintf ("%04d%02d%02d", $year + 1900, $mon +1, $mday);
		if ($check_date  >= &editDate($entry_date)) {
			$result = '';
		} else {
			$result = '1';
		}
	} else {
		$result = '';
	}
	
	return $result;
}

sub ceil {
	my $val = shift;
	my $opt = 0;

	$opt = 1 if($val > 0 and $val != int($val));
	return int($val + $opt);
}

sub setOrderCount {
	# 買い物を続けるから戻ってきた場合の処理(数置き換え)
	if ($ENV{'HTTP_REFERER'} =~ /order_cart_info.cgi/) {
	
		$session_name  = 'sessionCart';
		$session_timer = 30;
		
		&getCookie($session_name);
		if ($FORM{'seid'} ne '' && $_CONFIG_server_ssl_use eq '1' && $_CONFIG_page_view_mode ne 'P') {
			$COOKIE{$session_name} = $FORM{'seid'};
		}
		
		&cleanSession;
		our $session      = CGI::Session->new(undef, $COOKIE{$session_name}, {Directory=>"$_CONFIG_server_ssl_www_root/cgi-bin/session"});
		our $session_cart = $session->param($session_name);
		our $session_id   = $session->id;
		
		# エラーフラグ
		my $numeric_err_flg = 0;
		
		CART:foreach $value (@{$session_cart}) {
		
			# 注文数取得
			my $order_quantity = $FORM{'order_quantity_' . $$value{"item_code"}};
			
			# 商品コード取得
			my $item_code      = $$value{"item_code"};
			
			#_注文数値チェック
			if (($order_quantity =~ /[\D]/) || ($order_quantity eq '') || ($order_quantity == 0)) {
				$numeric_err_flg  = 1;
				last CART;
			}
		}
		
		unless ( $numeric_err_flg )
		{
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
}

sub isSessionCartEmpty {
	# セッションチェック
	my $session_cart_num = @{$session_cart};
	if( $session_cart_num <= 0 ) {
		my $top_url;
		if (($_CONFIG_server_ssl_use == 1) && ($_CONFIG_page_view_mode ne 'P')) {
			$top_url = sprintf('%s/', $_CONFIG_server_url);
		} else {
			$top_url = '../';
		}
		&apricationErr($top_url);
	}
}



sub chmodSessionFile {
	my $session_dir = $_[0];
	my $session_file_header = $_[1];
	my $session_id = $_[2];
	my $session_file = $session_dir . $session_file_header . $session_id;

	chmod 0666, $session_file or &outputLog("パーミッション変更エラー :" . $i);

}

sub strZenNumberCheck{
	my $str = $_[0];

	$str = &strZenNumberTrim($str);

	# Shift-JISの文字コードで０～９であることをチェックする
	if ($str =~ /^(?:\x82[\x4F-\x58])+$/ ) {
		return 1;
	} else {
		# 全角数字でなかった場合、0を返す
		return 0;
	}
}

sub strZenNumberTrim{
	my $str = $_[0];
	$str =~ s/^[\s\x81\x40]+//;
	$str =~ s/[\s\x81\x40]+$//;
	return $str;
}


sub isSerachCorrespond{
	my ($serach_line, $keyword) = @_;

	my $correspond_flg = 1;
	my $count = 0;
	foreach (@$keyword) {
		if ($_ ne '') {
			$count++;
			if (substr($_, 0, 1) eq '-') {
				my $minus_keyword = substr($_, 1);
				if (0 <= index(@$serach_line[4],  $minus_keyword) || 0 <= index(@$serach_line[6],  $minus_keyword) || 
					0 <= index(@$serach_line[7],  $minus_keyword) || 0 <= index(@$serach_line[8],  $minus_keyword) || 
					0 <= index(@$serach_line[28], $minus_keyword) || 0 <= index(@$serach_line[29], $minus_keyword) || 
					0 <= index(@$serach_line[30], $minus_keyword) || 0 <= index(@$serach_line[31], $minus_keyword) || 
					0 <= index(@$serach_line[32], $minus_keyword) || 0 <= index(@$serach_line[33], $minus_keyword) || 
					0 <= index(@$serach_line[34], $minus_keyword) || 0 <= index(@$serach_line[35], $minus_keyword)) {
						$correspond_flg = 0;
						last;
				}
			} else {
				unless (0 <= index(@$serach_line[4],  $_) || 0 <= index(@$serach_line[6],  $_) || 
						0 <= index(@$serach_line[7],  $_) || 0 <= index(@$serach_line[8],  $_) || 
						0 <= index(@$serach_line[28], $_) || 0 <= index(@$serach_line[29], $_) || 
						0 <= index(@$serach_line[30], $_) || 0 <= index(@$serach_line[31], $_) || 
						0 <= index(@$serach_line[32], $_) || 0 <= index(@$serach_line[33], $_) || 
						0 <= index(@$serach_line[34], $_) || 0 <= index(@$serach_line[35], $_)) {
							$correspond_flg = 0;
							last;
				}
			}
			if ($count >= 3) {
				last;
			}
		}
	}
	return $correspond_flg;
}

1;
