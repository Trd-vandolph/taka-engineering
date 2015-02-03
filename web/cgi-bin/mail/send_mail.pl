use MIME::Base64;

# メール送信のサブルーチン
sub send_mail_Send {
	(my $send_mail_from, my $send_mail_to, my $send_mail_subject, my $send_mail_message) = @_;
	
	#_動作確認用
	print $send_mail_massage;
	
	# 値をチェック
	unless ($send_mail_from && $send_mail_to && $send_mail_subject && $send_mail_message && $sendmail) {
		$err = 1;
	}
	unless (&send_mail_Check($send_mail_from)) {
		$err = 1;
	}
	unless (&send_mail_Check($send_mail_to)) {
		$err = 1;
	}
	if ($err == 0) {
		
		#サブジェクトをISO-2022-JPでMIMEエンコーディングします
		#utf8::decode($send_mail_subject);
		#$send_mail_subject = &covertInvalidCode($send_mail_subject);
		#utf8::encode($send_mail_subject);
		#$send_mail_subject = Encode::encode('MIME-Header-ISO_2022_JP', $send_mail_subject);
		#Encode::from_to($send_mail_subject, 'utf8', 'iso-2022-jp');
		Encode::from_to($send_mail_subject, 'sjis', 'iso-2022-jp');
		#件名はSJISをJISとBASE64で変換する
		$send_mail_subject = encode_base64($send_mail_subject, '');
		
		#本文をUT-8からISO-2022-JPに変換します。
		#utf8::decode($send_mail_message);
		#$send_mail_message = &covertInvalidCode($send_mail_message);
		#utf8::encode($send_mail_message);
		#Encode::from_to($send_mail_message, 'utf8', 'iso-2022-jp');
		#Encode::from_to($send_mail_message, 'sjis', 'iso-2022-jp');

		#本文はSJISのため、Content-Transfer-Encodingを8bit、charsetをSJISとする
		my $send_mail_head = "From: $send_mail_from" . "\n" . "To: $send_mail_to" . "\n" . "Subject: =?ISO-2022-JP?B?$send_mail_subject?=" . "\n" . "Content-Transfer-Encoding: 8bit" . "\n" . "Content-type: text/plain;charset=\"Shift_JIS\"" . "\n\n";
		
		eval {
			open(MAIL, "|$sendmail -t -i") or $err = 1;
			if ($err == 0) {
				print MAIL $send_mail_head;
				print MAIL $send_mail_message;
#				print MAIL "\n";
#				print MAIL "\n\n" . "." . "\n";
				close(MAIL);
			} else {
				$return_msg = sprintf($_CONFIG_error_msg[9910], $_CONFIG_carriage_contact);
			}
		};
		if ($@) {
			$return_msg = sprintf($_CONFIG_error_msg[9910], $_CONFIG_carriage_contact);
			&outputLog('メール送信エラー:' . $@);
		}
	} else {
		$return_msg = sprintf($_CONFIG_error_msg[9910], $_CONFIG_carriage_contact);
	}
}

# メール形式チェックのサブルーチン
sub send_mail_Check {
	(my $str) = @_;
	# メールの型で無かった場合エラーを返す
	#[0-9a-zA-Z]+\w+\@[0-9a-z]+.[a-z]+|[0-9a-zA-Z]+\w+\@[0-9a-z]+.[a-z]+.[a-z]+|[0-9a-zA-Z]+\w+\@[0-9a-z]+.[a-z]+.[a-z]+.[a-z]+
	if ($str =~ /^([\w-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([\w-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$/ ) {
		return 1;
	} else {
		return 0;
	}
}

sub covertInvalidCode {
	my $str = $_[0];
	#UTF-8からISO-2022-JPに変換する場合に文字化けを起こす文字は
	#コードマップの座標を強制的に変換します。
	#$str =~ s/\x{ff5e}/\x{301c}/g;
	#$str =~ s/\x{2225}/\x{2016}/g;
	#$str =~ s/\x{ff0d}/\x{2212}/g;
	#$str =~ s/\x{ffe0}/\x{00a2}/g;
	#$str =~ s/\x{ffe1}/\x{00a3}/g;
	#$str =~ s/\x{ffe2}/\x{00ac}/g;
	#$str =~ s/\x{00a5}/\x{005c}/g;
	#$str =~ s/\x{2044}/\x{002f}/g;
	return $str;
}

1;
