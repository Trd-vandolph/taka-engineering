#!/usr/bin/perl -w
package MODULE::StringUtil;

use strict;
use warnings;

sub conversionSpecialChar
{
	my ($txt) = @_;

	if(!defined($txt) || length($txt) < 1 || $txt =~ /^[0-9]+$/)
	{
		return $txt;
	}

	$txt =~ s/</&lt\;/g;
	$txt =~ s/>/&gt\;/g;
	$txt =~ s/\"/&quot\;/g;
	#$txt =~ s/\'/&apos\;/g;
	$txt =~ s/\//&frasl\;/g;

	return $txt;
}

return 1;

__END__
