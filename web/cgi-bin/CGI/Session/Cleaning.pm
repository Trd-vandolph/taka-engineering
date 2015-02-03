package CGI::Session::Cleaning;
require Exporter;
use Cwd;
our @ISA = qw(Exporter);
our %EXPORT_TAGS = ( 'all' => [ qw(
    
) ] );
our @EXPORT_OK = ( @{ $EXPORT_TAGS{'all'} } );
our @EXPORT = qw(
    
);
our $error_mess = "";
our $VERSION = '0.01';
sub new {
	my $class   = shift;
	$class      = ref( $class ) || $class;
	my @api_3;
	
	if ( defined $_[0] ) {
		@api_3  =
			map { uc( $_->[0] ) => $_->[1] } 
			map { [ /^(.+):(.+)$/ ] } 
						split /;/, $_[0] ;
	}
	
	my $self = {
		_OPTIONS    => [ @_ ], 
		_API_3      => {
			DRIVER      => 'File', 
			SERIALIZER  => 'Default', 
			ID          => 'MD5', 
			@api_3
		}
	};
	$class .= "::$self->{_API_3}->{DRIVER}";
	return bless( $self, $class );
}
sub sweep {
		my $self        = shift;
		my %sessions    = %{ $self->_scan_sessions() };
		my @args;
		
		$args[0, 2]     = @{ $self->{_OPTIONS} }[0, 1];
		
		my $str = "";
		while ( my( $id, $val ) = each %sessions ) {
			next unless( $id );
			$val = "./session/" . $val;
			$str = $str . "Åu" . $val . "ÅvÅ@" . "[" . ((-M $val) * 86400) . "] <br>";

			my @tmp = stat($val);
			my $lastUp = @tmp[9];
			my $newSec = time();

			if($lastUp + ( 60 * 60 ) < $newSec) {
				unlink $val;
			}
		}
		$str = $str;
	return $str;
}

sub _scan_sessions { return {} }
package CGI::Session::Cleaning::Item;
use CGI::Session;
our @ISA = qw(CGI::Session);
sub new {
	my $class   = shift;
	$class      = ref( $class ) || $class;
	
	my $self    = CGI::Session->new( @_ );
	
	return bless( $self, $class );
	
}
sub _init_old_session {
	my ($self, $claimed_id) = @_;
	$error_mess = $error_mess . "1";
	my $options = $self->{_OPTIONS} || [];
	my $data = $self->retrieve($claimed_id, $options);
	
	$error_mess = $error_mess . "2";
	if ( defined $data ) {
	$error_mess = $error_mess . " data = $data ";
		$self->{_DATA} = $data;
		if ( $self->_is_expired() ) {
			$self->delete();
			$self->flush();
		}
		return 1;
	}
	return 0;
}

package CGI::Session::Cleaning::File;
our @ISA    = qw(CGI::Session::Cleaning);

sub _scan_sessions {
	
	my $self    = shift;
	my $dir     = $self->{_OPTIONS}[1]{Directory} || '.';
	my $pat     = sprintf( $CGI::Session::File::FileName, '(.+)' );
	
	opendir( DIRH, $dir ) or croak( "can't open directory" );
	
	my %sessions = 
		map { $_->[1] => $_->[0] }
		map { [ /^($pat)/ ] }
								readdir( DIRH );
	closedir( DIRH );
	
	return \%sessions;
	
}


1;