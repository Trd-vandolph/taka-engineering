package Logger::MyLogger;
use vars qw($VERSION);
$VERSION = "1.00";
use strict;

my $filename      = '../log/site_log';
my $extension     = '.log';
my $maxlogsize    = 1000000;
my $maxlogfilenum = 10;

sub new {
	my $param = shift;
	my $class = ref $param || $param;
	my $self  = {};
	$self->{ERROR} = undef;
	bless($self, $class);
	return $self;
}

sub getErr {
	my $self = shift;
	return( $self->{ERROR} );
}

sub appendLog {
	my $self = shift;
	my $msg  = shift || "";
	my $time = Logger::MyLogger->log_time;
	$msg = "$time	$msg\n";
	
	unless( defined($filename . "_1" . $extension) ) {
		$self->{ERROR} = "Undefined log filename";
		print STDERR "Undefined log filename!!\n";
		return 0;
	}
	
	my $lock_file = $filename;
	my $writeFlg = 0;
	unless ( -e ($filename . "_1" . $extension) && $maxlogsize ) {
		for ( my $i = 0; $i < 5; $i++ ) {
			if (!mkdir($lock_file, 0755)) {
				if ( open( LOGFL,">>".$filename . "_1" . $extension  ) ) {
					print LOGFL $msg;
					close(LOGFL);
					$writeFlg = 1;
				}
				rmdir($lock_file);
				last;
			}
		}
		unless ( $writeFlg ) {
			print STDERR "FAILED APPEND LOG!!\n";
			$self->{ERROR} = "FAILED APPEND LOG";
			return 0;
		}
	} else {
		for( my $i = 0; $i < 5; $i++ ) {
			if (!mkdir($lock_file, 0755)) {
				unless( open(LOGFL, ">>" . $filename . "_1" . $extension ) ) {
					$self->{ERROR} = "FAILED OPEN LOG";
					print STDERR "FAILED OPEN LOG!!\n";
					rmdir($lock_file);
					return 0;
				}
				my @logs = <LOGFL>;
				my $file_size = ( -s LOGFL );
				if ( $file_size >= $maxlogsize) {
					close(LOGFL);
					unlink $filename . "_" . ($maxlogfilenum ) . $extension;
					for (my $cnt = $maxlogfilenum; $cnt > 0; $cnt--) {
						my $new_filename = $filename . "_" . ($cnt + 1) . $extension;
						rename $filename . "_$cnt" . $extension , $new_filename;
					}
					unless ( open(LOGFL,">".$filename . "_1" . $extension) ) {
						$self->{ERROR} = "FAILED CREATE LOG";
						print STDERR "FAILED CREATE LOG!!\n";
						rmdir($lock_file);
						return 0;
					}
					print LOGFL $msg;
					close(LOGFL);
					$writeFlg = 1;
				} else {
					foreach ( @logs ) { print LOGFL $_; }
					print LOGFL $msg;
					close(LOGFL);
					$writeFlg = 1;
				}
				rmdir($lock_file);
				last;
			}
		}
	}
	return 1;
}

sub log_time {
	my $times = time();
	my ($sec,$min,$hour,$mday,$month,$year,$wday,$stime) = localtime($times);
	return sprintf("%04d\/%02d\/%02d\ %02d\:%02d:%02d", $year+1900, $month+1, $mday, $hour, $min, $sec);
}

1;
__END__

