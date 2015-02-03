package ORDERNUMBER;

sub setSIG {
    $SIG{HUP} = $SIG{INT} = $SIG{PIPE} = $SIG{QUIT} = $SIG{TERM} = \&unlock;
}

sub setLock(@) {
	my (@lock_file) = @_;
	$lock_fileNum = @lock_file;
	for ( $i=0; $i<$lock_fileNum; $i++) {
		$retry = 20;
		while (!mkdir(@lock_file[$i], 0755)) {
			if (--$retry <= 0) {
				$lock_file_2 = @lock_file[$i] . "_2";
				if (mkdir($lock_file_2, 0755)) {

					my @tmp = stat(@lock_file[$i]);
					$lastUp = @tmp[9];
					$newSec = time();
					if($lastUp + ( 60 * 10 ) < $newSec) {
						if (rename($lock_file_2, @lock_file[$i]) == 0){
							#error;
						}
						last;
					} else {
						rmdir($lock_file_2);
					}

#					if ((-M @lock_file[$i]) * 86400 > 600) {
#						if (rename($lock_file_2, @lock_file[$i]) == 0){
#							#error;
#						}
#						last;
#					} else {
#						rmdir($lock_file_2);
#					}
				}
				for ($j = $i - 1; $j >= 0; $j--) {
					rmdir(@lock_file[$j]);
				}
				return 0;
			}
			select( undef, undef, undef, 0.25 );
		}
		return 1;
	}
}

sub getNumber {
	$_CONFIG_server_ssl_www_root = $_[0];
	$num_file  = "$_CONFIG_server_ssl_www_root/cgi-bin/order/order_number.cgi";
	$maker2[0] = "$_CONFIG_server_ssl_www_root/cgi-bin/order/number";
	if (ORDERNUMBER::setLock(@maker2) == 0) {
		$str = 'sippai';
		#error;
	} else {
		if (!open(TXT, "+< ./$num_file")) {
			if (!open(TXT, "+> ./$num_file")) {
		$str = 'sippai';
				#error;
			} else {
				close(TXT);
				$str = ORDERNUMBER::outputNumber;
			}
		} else {
			$time = "";
			$cnt  = 0;
			my @logs = <TXT>;
			close(TXT);
			$str = ORDERNUMBER::outputNumber(@logs);
		}
	}
	ORDERNUMBER::delLock(@maker2);
	return $str;
}

sub getTime {
	my $times = time();
	my ($sec, $min, $hour, $mday, $month, $year, $wday, $stime) = localtime($times);
	my @weekly = ('Sun', 'Mon', 'Tue', 'Wed', 'Thr', 'Fri', 'Sut');    #© •\Ž¦‚µ‚½‚¢—j“ú•¶Žš
	return sprintf("%04d%02d%02d%02d%02d%02d", $year+1900,$month+1,$mday,$hour,$min,$sec);
}

sub outputNumber {
	if (!open(TXT, ">> ./$num_file")) {
		#error;
	}
	foreach (@_) {
		$time = substr($_ , 0, 14);
		$cnt  = substr($_, 15, 9);
		$cnt  = $cnt - 0;
	}
	
	if($time eq ORDERNUMBER::getTime) {
		$cnt = $cnt + 1;
		if ($cnt > 999999999) {
			$cnt = 0;
		}
	} else {
		$time = ORDERNUMBER::getTime;
		$cnt  = 0;
	}
	$str = $time . sprintf("%09d", $cnt);
	truncate (TXT, 0);
	print TXT "$str\n";
	close(TXT);
	return $str;
}

sub delLock(@) {
	my (@lock_file) = @_;
	$lock_fileNum = @lock_file;
	for ( $i=0; $i<$lock_fileNum; $i++) {
		rmdir(@lock_file[$i]);
	}
}

sub unlock {
	for ( $i=0; $i<$lock_fileNum; $i++) {
		if(0 == -M @lock_file[$i]) {
			rmdir(@lock_file[$i]);
		}
	}
}

1;