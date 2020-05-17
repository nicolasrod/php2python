#!/usr/bin/env python3
# coding: utf-8
if '__PHP2PY_LOADED__' not in globals():
    import os
    with open(os.getenv('PHP2PY_COMPAT', 'php_compat.py')) as f:
        exec(compile(f.read(), '<string>', 'exec'))
    # end with
    globals()['__PHP2PY_LOADED__'] = True
# end if
#// 
#// SSL utilities for Requests
#// 
#// @package Requests
#// @subpackage Utilities
#// 
#// 
#// SSL utilities for Requests
#// 
#// Collection of utilities for working with and verifying SSL certificates.
#// 
#// @package Requests
#// @subpackage Utilities
#//
class Requests_SSL():
    #// 
    #// Verify the certificate against common name and subject alternative names
    #// 
    #// Unfortunately, PHP doesn't check the certificate against the alternative
    #// names, leading things like 'https://www.github.com/' to be invalid.
    #// Instead
    #// 
    #// @see https://tools.ietf.org/html/rfc2818#section-3.1 RFC2818, Section 3.1
    #// 
    #// @throws Requests_Exception On not obtaining a match for the host (`fsockopen.ssl.no_match`)
    #// @param string $host Host name to verify against
    #// @param array $cert Certificate data from openssl_x509_parse()
    #// @return bool
    #//
    @classmethod
    def verify_certificate(self, host_=None, cert_=None):
        
        
        #// Calculate the valid wildcard match if the host is not an IP address
        parts_ = php_explode(".", host_)
        if ip2long(host_) == False:
            parts_[0] = "*"
        # end if
        wildcard_ = php_implode(".", parts_)
        has_dns_alt_ = False
        #// Check the subjectAltName
        if (not php_empty(lambda : cert_["extensions"])) and (not php_empty(lambda : cert_["extensions"]["subjectAltName"])):
            altnames_ = php_explode(",", cert_["extensions"]["subjectAltName"])
            for altname_ in altnames_:
                altname_ = php_trim(altname_)
                if php_strpos(altname_, "DNS:") != 0:
                    continue
                # end if
                has_dns_alt_ = True
                #// Strip the 'DNS:' prefix and trim whitespace
                altname_ = php_trim(php_substr(altname_, 4))
                #// Check for a match
                if self.match_domain(host_, altname_) == True:
                    return True
                # end if
            # end for
        # end if
        #// Fall back to checking the common name if we didn't get any dNSName
        #// alt names, as per RFC2818
        if (not has_dns_alt_) and (not php_empty(lambda : cert_["subject"]["CN"])):
            #// Check for a match
            if self.match_domain(host_, cert_["subject"]["CN"]) == True:
                return True
            # end if
        # end if
        return False
    # end def verify_certificate
    #// 
    #// Verify that a reference name is valid
    #// 
    #// Verifies a dNSName for HTTPS usage, (almost) as per Firefox's rules:
    #// - Wildcards can only occur in a name with more than 3 components
    #// - Wildcards can only occur as the last character in the first
    #// component
    #// - Wildcards may be preceded by additional characters
    #// 
    #// We modify these rules to be a bit stricter and only allow the wildcard
    #// character to be the full first component; that is, with the exclusion of
    #// the third rule.
    #// 
    #// @param string $reference Reference dNSName
    #// @return boolean Is the name valid?
    #//
    @classmethod
    def verify_reference_name(self, reference_=None):
        
        
        parts_ = php_explode(".", reference_)
        #// Check the first part of the name
        first_ = php_array_shift(parts_)
        if php_strpos(first_, "*") != False:
            #// Check that the wildcard is the full part
            if first_ != "*":
                return False
            # end if
            #// Check that we have at least 3 components (including first)
            if php_count(parts_) < 2:
                return False
            # end if
        # end if
        #// Check the remaining parts
        for part_ in parts_:
            if php_strpos(part_, "*") != False:
                return False
            # end if
        # end for
        #// Nothing found, verified!
        return True
    # end def verify_reference_name
    #// 
    #// Match a hostname against a dNSName reference
    #// 
    #// @param string $host Requested host
    #// @param string $reference dNSName to match against
    #// @return boolean Does the domain match?
    #//
    @classmethod
    def match_domain(self, host_=None, reference_=None):
        
        
        #// Check if the reference is blacklisted first
        if self.verify_reference_name(reference_) != True:
            return False
        # end if
        #// Check for a direct match
        if host_ == reference_:
            return True
        # end if
        #// Calculate the valid wildcard match if the host is not an IP address
        #// Also validates that the host has 3 parts or more, as per Firefox's
        #// ruleset.
        if ip2long(host_) == False:
            parts_ = php_explode(".", host_)
            parts_[0] = "*"
            wildcard_ = php_implode(".", parts_)
            if wildcard_ == reference_:
                return True
            # end if
        # end if
        return False
    # end def match_domain
# end class Requests_SSL
