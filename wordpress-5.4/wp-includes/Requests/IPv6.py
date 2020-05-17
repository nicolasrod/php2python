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
#// Class to validate and to work with IPv6 addresses
#// 
#// @package Requests
#// @subpackage Utilities
#// 
#// 
#// Class to validate and to work with IPv6 addresses
#// 
#// This was originally based on the PEAR class of the same name, but has been
#// entirely rewritten.
#// 
#// @package Requests
#// @subpackage Utilities
#//
class Requests_IPv6():
    #// 
    #// Uncompresses an IPv6 address
    #// 
    #// RFC 4291 allows you to compress consecutive zero pieces in an address to
    #// '::'. This method expects a valid IPv6 address and expands the '::' to
    #// the required number of zero pieces.
    #// 
    #// Example:  FF01::101   ->  FF01:0:0:0:0:0:0:101
    #// ::1         ->  0:0:0:0:0:0:0:1
    #// 
    #// @author Alexander Merz <alexander.merz@web.de>
    #// @author elfrink at introweb dot nl
    #// @author Josh Peck <jmp at joshpeck dot org>
    #// @copyright 2003-2005 The PHP Group
    #// @license http://www.opensource.org/licenses/bsd-license.php
    #// @param string $ip An IPv6 address
    #// @return string The uncompressed IPv6 address
    #//
    @classmethod
    def uncompress(self, ip_=None):
        
        
        if php_substr_count(ip_, "::") != 1:
            return ip_
        # end if
        ip1_, ip2_ = php_explode("::", ip_)
        c1_ = -1 if ip1_ == "" else php_substr_count(ip1_, ":")
        c2_ = -1 if ip2_ == "" else php_substr_count(ip2_, ":")
        if php_strpos(ip2_, ".") != False:
            c2_ += 1
        # end if
        #// ::
        if c1_ == -1 and c2_ == -1:
            ip_ = "0:0:0:0:0:0:0:0"
        else:
            if c1_ == -1:
                fill_ = php_str_repeat("0:", 7 - c2_)
                ip_ = php_str_replace("::", fill_, ip_)
            else:
                if c2_ == -1:
                    fill_ = php_str_repeat(":0", 7 - c1_)
                    ip_ = php_str_replace("::", fill_, ip_)
                else:
                    fill_ = ":" + php_str_repeat("0:", 6 - c2_ - c1_)
                    ip_ = php_str_replace("::", fill_, ip_)
                # end if
            # end if
        # end if
        return ip_
    # end def uncompress
    #// 
    #// Compresses an IPv6 address
    #// 
    #// RFC 4291 allows you to compress consecutive zero pieces in an address to
    #// '::'. This method expects a valid IPv6 address and compresses consecutive
    #// zero pieces to '::'.
    #// 
    #// Example:  FF01:0:0:0:0:0:0:101   ->  FF01::101
    #// 0:0:0:0:0:0:0:1        ->  ::1
    #// 
    #// @see uncompress()
    #// @param string $ip An IPv6 address
    #// @return string The compressed IPv6 address
    #//
    @classmethod
    def compress(self, ip_=None):
        
        
        #// Prepare the IP to be compressed
        ip_ = self.uncompress(ip_)
        ip_parts_ = self.split_v6_v4(ip_)
        #// Replace all leading zeros
        ip_parts_[0] = php_preg_replace("/(^|:)0+([0-9])/", "\\1\\2", ip_parts_[0])
        #// Find bunches of zeros
        if preg_match_all("/(?:^|:)(?:0(?::|$))+/", ip_parts_[0], matches_, PREG_OFFSET_CAPTURE):
            max_ = 0
            pos_ = None
            for match_ in matches_[0]:
                if php_strlen(match_[0]) > max_:
                    max_ = php_strlen(match_[0])
                    pos_ = match_[1]
                # end if
            # end for
            ip_parts_[0] = php_substr_replace(ip_parts_[0], "::", pos_, max_)
        # end if
        if ip_parts_[1] != "":
            return php_implode(":", ip_parts_)
        else:
            return ip_parts_[0]
        # end if
    # end def compress
    #// 
    #// Splits an IPv6 address into the IPv6 and IPv4 representation parts
    #// 
    #// RFC 4291 allows you to represent the last two parts of an IPv6 address
    #// using the standard IPv4 representation
    #// 
    #// Example:  0:0:0:0:0:0:13.1.68.3
    #// 0:0:0:0:0:FFFF:129.144.52.38
    #// 
    #// @param string $ip An IPv6 address
    #// @return string[] [0] contains the IPv6 represented part, and [1] the IPv4 represented part
    #//
    def split_v6_v4(self, ip_=None):
        
        
        if php_strpos(ip_, ".") != False:
            pos_ = php_strrpos(ip_, ":")
            ipv6_part_ = php_substr(ip_, 0, pos_)
            ipv4_part_ = php_substr(ip_, pos_ + 1)
            return Array(ipv6_part_, ipv4_part_)
        else:
            return Array(ip_, "")
        # end if
    # end def split_v6_v4
    #// 
    #// Checks an IPv6 address
    #// 
    #// Checks if the given IP is a valid IPv6 address
    #// 
    #// @param string $ip An IPv6 address
    #// @return bool true if $ip is a valid IPv6 address
    #//
    @classmethod
    def check_ipv6(self, ip_=None):
        
        
        ip_ = self.uncompress(ip_)
        ipv6_, ipv4_ = self.split_v6_v4(ip_)
        ipv6_ = php_explode(":", ipv6_)
        ipv4_ = php_explode(".", ipv4_)
        if php_count(ipv6_) == 8 and php_count(ipv4_) == 1 or php_count(ipv6_) == 6 and php_count(ipv4_) == 4:
            for ipv6_part_ in ipv6_:
                #// The section can't be empty
                if ipv6_part_ == "":
                    return False
                # end if
                #// Nor can it be over four characters
                if php_strlen(ipv6_part_) > 4:
                    return False
                # end if
                #// Remove leading zeros (this is safe because of the above)
                ipv6_part_ = php_ltrim(ipv6_part_, "0")
                if ipv6_part_ == "":
                    ipv6_part_ = "0"
                # end if
                #// Check the value is valid
                value_ = hexdec(ipv6_part_)
                if dechex(value_) != php_strtolower(ipv6_part_) or value_ < 0 or value_ > 65535:
                    return False
                # end if
            # end for
            if php_count(ipv4_) == 4:
                for ipv4_part_ in ipv4_:
                    value_ = php_int(ipv4_part_)
                    if php_str(value_) != ipv4_part_ or value_ < 0 or value_ > 255:
                        return False
                    # end if
                # end for
            # end if
            return True
        else:
            return False
        # end if
    # end def check_ipv6
# end class Requests_IPv6
