#!/usr/bin/env python3
# coding: utf-8
if '__PHP2PY_LOADED__' not in globals():
    import cgi
    import os
    import os.path
    import copy
    import sys
    from goto import with_goto
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
    def uncompress(self, ip=None):
        
        if php_substr_count(ip, "::") != 1:
            return ip
        # end if
        ip1, ip2 = php_explode("::", ip)
        c1 = -1 if ip1 == "" else php_substr_count(ip1, ":")
        c2 = -1 if ip2 == "" else php_substr_count(ip2, ":")
        if php_strpos(ip2, ".") != False:
            c2 += 1
        # end if
        #// ::
        if c1 == -1 and c2 == -1:
            ip = "0:0:0:0:0:0:0:0"
        else:
            if c1 == -1:
                fill = php_str_repeat("0:", 7 - c2)
                ip = php_str_replace("::", fill, ip)
            else:
                if c2 == -1:
                    fill = php_str_repeat(":0", 7 - c1)
                    ip = php_str_replace("::", fill, ip)
                else:
                    fill = ":" + php_str_repeat("0:", 6 - c2 - c1)
                    ip = php_str_replace("::", fill, ip)
                # end if
            # end if
        # end if
        return ip
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
    def compress(self, ip=None):
        
        #// Prepare the IP to be compressed
        ip = self.uncompress(ip)
        ip_parts = self.split_v6_v4(ip)
        #// Replace all leading zeros
        ip_parts[0] = php_preg_replace("/(^|:)0+([0-9])/", "\\1\\2", ip_parts[0])
        #// Find bunches of zeros
        if preg_match_all("/(?:^|:)(?:0(?::|$))+/", ip_parts[0], matches, PREG_OFFSET_CAPTURE):
            max = 0
            pos = None
            for match in matches[0]:
                if php_strlen(match[0]) > max:
                    max = php_strlen(match[0])
                    pos = match[1]
                # end if
            # end for
            ip_parts[0] = php_substr_replace(ip_parts[0], "::", pos, max)
        # end if
        if ip_parts[1] != "":
            return php_implode(":", ip_parts)
        else:
            return ip_parts[0]
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
    def split_v6_v4(self, ip=None):
        
        if php_strpos(ip, ".") != False:
            pos = php_strrpos(ip, ":")
            ipv6_part = php_substr(ip, 0, pos)
            ipv4_part = php_substr(ip, pos + 1)
            return Array(ipv6_part, ipv4_part)
        else:
            return Array(ip, "")
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
    def check_ipv6(self, ip=None):
        
        ip = self.uncompress(ip)
        ipv6, ipv4 = self.split_v6_v4(ip)
        ipv6 = php_explode(":", ipv6)
        ipv4 = php_explode(".", ipv4)
        if php_count(ipv6) == 8 and php_count(ipv4) == 1 or php_count(ipv6) == 6 and php_count(ipv4) == 4:
            for ipv6_part in ipv6:
                #// The section can't be empty
                if ipv6_part == "":
                    return False
                # end if
                #// Nor can it be over four characters
                if php_strlen(ipv6_part) > 4:
                    return False
                # end if
                #// Remove leading zeros (this is safe because of the above)
                ipv6_part = php_ltrim(ipv6_part, "0")
                if ipv6_part == "":
                    ipv6_part = "0"
                # end if
                #// Check the value is valid
                value = hexdec(ipv6_part)
                if dechex(value) != php_strtolower(ipv6_part) or value < 0 or value > 65535:
                    return False
                # end if
            # end for
            if php_count(ipv4) == 4:
                for ipv4_part in ipv4:
                    value = int(ipv4_part)
                    if str(value) != ipv4_part or value < 0 or value > 255:
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
