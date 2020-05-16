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
#// IRI parser/serialiser/normaliser
#// 
#// @package Requests
#// @subpackage Utilities
#// 
#// 
#// IRI parser/serialiser/normaliser
#// 
#// Copyright (c) 2007-2010, Geoffrey Sneddon and Steve Minutillo.
#// All rights reserved.
#// 
#// Redistribution and use in source and binary forms, with or without
#// modification, are permitted provided that the following conditions are met:
#// 
#// Redistributions of source code must retain the above copyright notice,
#// this list of conditions and the following disclaimer.
#// 
#// Redistributions in binary form must reproduce the above copyright notice,
#// this list of conditions and the following disclaimer in the documentation
#// and/or other materials provided with the distribution.
#// 
#// Neither the name of the SimplePie Team nor the names of its contributors
#// may be used to endorse or promote products derived from this software
#// without specific prior written permission.
#// 
#// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#// AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#// IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
#// ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDERS AND CONTRIBUTORS BE
#// LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
#// CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
#// SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
#// INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
#// CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
#// ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
#// POSSIBILITY OF SUCH DAMAGE.
#// 
#// @package Requests
#// @subpackage Utilities
#// @author Geoffrey Sneddon
#// @author Steve Minutillo
#// @copyright 2007-2009 Geoffrey Sneddon and Steve Minutillo
#// @license http://www.opensource.org/licenses/bsd-license.php
#// @link http://hg.gsnedders.com/iri
#// 
#// @property string $iri IRI we're working with
#// @property-read string $uri IRI in URI form, {@see to_uri}
#// @property string $scheme Scheme part of the IRI
#// @property string $authority Authority part, formatted for a URI (userinfo + host + port)
#// @property string $iauthority Authority part of the IRI (userinfo + host + port)
#// @property string $userinfo Userinfo part, formatted for a URI (after '://' and before '@')
#// @property string $iuserinfo Userinfo part of the IRI (after '://' and before '@')
#// @property string $host Host part, formatted for a URI
#// @property string $ihost Host part of the IRI
#// @property string $port Port part of the IRI (after ':')
#// @property string $path Path part, formatted for a URI (after first '/')
#// @property string $ipath Path part of the IRI (after first '/')
#// @property string $query Query part, formatted for a URI (after '?')
#// @property string $iquery Query part of the IRI (after '?')
#// @property string $fragment Fragment, formatted for a URI (after '#')
#// @property string $ifragment Fragment part of the IRI (after '#')
#//
class Requests_IRI():
    scheme = None
    iuserinfo = None
    ihost = None
    port = None
    ipath = ""
    iquery = None
    ifragment = None
    normalization = Array({"acap": Array({"port": 674})}, {"dict": Array({"port": 2628})}, {"file": Array({"ihost": "localhost"})}, {"http": Array({"port": 80})}, {"https": Array({"port": 443})})
    #// 
    #// Return the entire IRI when you try and read the object as a string
    #// 
    #// @return string
    #//
    def __tostring(self):
        
        return self.get_iri()
    # end def __tostring
    #// 
    #// Overload __set() to provide access via properties
    #// 
    #// @param string $name Property name
    #// @param mixed $value Property value
    #//
    def __set(self, name=None, value=None):
        
        if php_method_exists(self, "set_" + name):
            php_call_user_func(Array(self, "set_" + name), value)
        elif name == "iauthority" or name == "iuserinfo" or name == "ihost" or name == "ipath" or name == "iquery" or name == "ifragment":
            php_call_user_func(Array(self, "set_" + php_substr(name, 1)), value)
        # end if
    # end def __set
    #// 
    #// Overload __get() to provide access via properties
    #// 
    #// @param string $name Property name
    #// @return mixed
    #//
    def __get(self, name=None):
        
        #// isset() returns false for null, we don't want to do that
        #// Also why we use array_key_exists below instead of isset()
        props = get_object_vars(self)
        if name == "iri" or name == "uri" or name == "iauthority" or name == "authority":
            method = "get_" + name
            return_ = self.method()
        elif php_array_key_exists(name, props):
            return_ = self.name
            #// host -> ihost
        elif "i" + name and php_array_key_exists(prop, props):
            prop = "i" + name
            name = prop
            return_ = self.prop
            #// ischeme -> scheme
        elif php_substr(name, 1) and php_array_key_exists(prop, props):
            prop = php_substr(name, 1)
            name = prop
            return_ = self.prop
        else:
            trigger_error("Undefined property: " + get_class(self) + "::" + name, E_USER_NOTICE)
            return_ = None
        # end if
        if return_ == None and (php_isset(lambda : self.normalization[self.scheme][name])):
            return self.normalization[self.scheme][name]
        else:
            return return_
        # end if
    # end def __get
    #// 
    #// Overload __isset() to provide access via properties
    #// 
    #// @param string $name Property name
    #// @return bool
    #//
    def __isset(self, name=None):
        
        return php_method_exists(self, "get_" + name) or (php_isset(lambda : self.name))
    # end def __isset
    #// 
    #// Overload __unset() to provide access via properties
    #// 
    #// @param string $name Property name
    #//
    def __unset(self, name=None):
        
        if php_method_exists(self, "set_" + name):
            php_call_user_func(Array(self, "set_" + name), "")
        # end if
    # end def __unset
    #// 
    #// Create a new IRI object, from a specified string
    #// 
    #// @param string|null $iri
    #//
    def __init__(self, iri=None):
        
        self.set_iri(iri)
    # end def __init__
    #// 
    #// Create a new IRI object by resolving a relative IRI
    #// 
    #// Returns false if $base is not absolute, otherwise an IRI.
    #// 
    #// @param IRI|string $base (Absolute) Base IRI
    #// @param IRI|string $relative Relative IRI
    #// @return IRI|false
    #//
    @classmethod
    def absolutize(self, base=None, relative=None):
        
        if (not type(relative).__name__ == "Requests_IRI"):
            relative = php_new_class("Requests_IRI", lambda : Requests_IRI(relative))
        # end if
        if (not relative.is_valid()):
            return False
        elif relative.scheme != None:
            return copy.deepcopy(relative)
        # end if
        if (not type(base).__name__ == "Requests_IRI"):
            base = php_new_class("Requests_IRI", lambda : Requests_IRI(base))
        # end if
        if base.scheme == None or (not base.is_valid()):
            return False
        # end if
        if relative.get_iri() != "":
            if relative.iuserinfo != None or relative.ihost != None or relative.port != None:
                target = copy.deepcopy(relative)
                target.scheme = base.scheme
            else:
                target = php_new_class("Requests_IRI", lambda : Requests_IRI())
                target.scheme = base.scheme
                target.iuserinfo = base.iuserinfo
                target.ihost = base.ihost
                target.port = base.port
                if relative.ipath != "":
                    if relative.ipath[0] == "/":
                        target.ipath = relative.ipath
                    elif base.iuserinfo != None or base.ihost != None or base.port != None and base.ipath == "":
                        target.ipath = "/" + relative.ipath
                    elif php_strrpos(base.ipath, "/") != False:
                        last_segment = php_strrpos(base.ipath, "/")
                        target.ipath = php_substr(base.ipath, 0, last_segment + 1) + relative.ipath
                    else:
                        target.ipath = relative.ipath
                    # end if
                    target.ipath = target.remove_dot_segments(target.ipath)
                    target.iquery = relative.iquery
                else:
                    target.ipath = base.ipath
                    if relative.iquery != None:
                        target.iquery = relative.iquery
                    elif base.iquery != None:
                        target.iquery = base.iquery
                    # end if
                # end if
                target.ifragment = relative.ifragment
            # end if
        else:
            target = copy.deepcopy(base)
            target.ifragment = None
        # end if
        target.scheme_normalization()
        return target
    # end def absolutize
    #// 
    #// Parse an IRI into scheme/authority/path/query/fragment segments
    #// 
    #// @param string $iri
    #// @return array
    #//
    def parse_iri(self, iri=None):
        
        iri = php_trim(iri, "   \n\r")
        has_match = php_preg_match("/^((?P<scheme>[^:\\/?#]+):)?(\\/\\/(?P<authority>[^\\/?#]*))?(?P<path>[^?#]*)(\\?(?P<query>[^#]*))?(#(?P<fragment>.*))?$/", iri, match)
        if (not has_match):
            raise php_new_class("Requests_Exception", lambda : Requests_Exception("Cannot parse supplied IRI", "iri.cannot_parse", iri))
        # end if
        if match[1] == "":
            match["scheme"] = None
        # end if
        if (not (php_isset(lambda : match[3]))) or match[3] == "":
            match["authority"] = None
        # end if
        if (not (php_isset(lambda : match[5]))):
            match["path"] = ""
        # end if
        if (not (php_isset(lambda : match[6]))) or match[6] == "":
            match["query"] = None
        # end if
        if (not (php_isset(lambda : match[8]))) or match[8] == "":
            match["fragment"] = None
        # end if
        return match
    # end def parse_iri
    #// 
    #// Remove dot segments from a path
    #// 
    #// @param string $input
    #// @return string
    #//
    def remove_dot_segments(self, input=None):
        
        output = ""
        while True:
            
            if not (php_strpos(input, "./") != False or php_strpos(input, "/.") != False or input == "." or input == ".."):
                break
            # end if
            #// A: If the input buffer begins with a prefix of "../" or "./",
            #// then remove that prefix from the input buffer; otherwise,
            if php_strpos(input, "../") == 0:
                input = php_substr(input, 3)
            elif php_strpos(input, "./") == 0:
                input = php_substr(input, 2)
                #// B: if the input buffer begins with a prefix of "/./" or "/.",
                #// where "." is a complete path segment, then replace that prefix
                #// with "/" in the input buffer; otherwise,
            elif php_strpos(input, "/./") == 0:
                input = php_substr(input, 2)
            elif input == "/.":
                input = "/"
                #// C: if the input buffer begins with a prefix of "/../" or "/..",
                #// where ".." is a complete path segment, then replace that prefix
                #// with "/" in the input buffer and remove the last segment and its
                #// preceding "/" (if any) from the output buffer; otherwise,
            elif php_strpos(input, "/../") == 0:
                input = php_substr(input, 3)
                output = php_substr_replace(output, "", php_strrpos(output, "/"))
            elif input == "/..":
                input = "/"
                output = php_substr_replace(output, "", php_strrpos(output, "/"))
                #// D: if the input buffer consists only of "." or "..", then remove
                #// that from the input buffer; otherwise,
            elif input == "." or input == "..":
                input = ""
                #// E: move the first path segment in the input buffer to the end of
                #// the output buffer, including the initial "/" character (if any)
                #// and any subsequent characters up to, but not including, the next
                #// "/" character or the end of the input buffer
            elif php_strpos(input, "/", 1) != False:
                pos = php_strpos(input, "/", 1)
                output += php_substr(input, 0, pos)
                input = php_substr_replace(input, "", 0, pos)
            else:
                output += input
                input = ""
            # end if
        # end while
        return output + input
    # end def remove_dot_segments
    #// 
    #// Replace invalid character with percent encoding
    #// 
    #// @param string $string Input string
    #// @param string $extra_chars Valid characters not in iunreserved or
    #// iprivate (this is ASCII-only)
    #// @param bool $iprivate Allow iprivate
    #// @return string
    #//
    def replace_invalid_with_pct_encoding(self, string=None, extra_chars=None, iprivate=False):
        
        #// Normalize as many pct-encoded sections as possible
        string = preg_replace_callback("/(?:%[A-Fa-f0-9]{2})+/", Array(self, "remove_iunreserved_percent_encoded"), string)
        #// Replace invalid percent characters
        string = php_preg_replace("/%(?![A-Fa-f0-9]{2})/", "%25", string)
        #// Add unreserved and % to $extra_chars (the latter is safe because all
        #// pct-encoded sections are now valid).
        extra_chars += "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~%"
        #// Now replace any bytes that aren't allowed with their pct-encoded versions
        position = 0
        strlen = php_strlen(string)
        while True:
            
            if not (position += strspn(string, extra_chars, position) < strlen):
                break
            # end if
            value = php_ord(string[position])
            #// Start position
            start = position
            #// By default we are valid
            valid = True
            #// No one byte sequences are valid due to the while.
            #// Two byte sequence:
            if value & 224 == 192:
                character = value & 31 << 6
                length = 2
                remaining = 1
                #// Three byte sequence:
            elif value & 240 == 224:
                character = value & 15 << 12
                length = 3
                remaining = 2
                #// Four byte sequence:
            elif value & 248 == 240:
                character = value & 7 << 18
                length = 4
                remaining = 3
            else:
                valid = False
                length = 1
                remaining = 0
            # end if
            if remaining:
                if position + length <= strlen:
                    position += 1
                    while remaining:
                        
                        value = php_ord(string[position])
                        #// Check that the byte is valid, then add it to the character:
                        if value & 192 == 128:
                            remaining -= 1
                            character |= value & 63 << remaining * 6
                        else:
                            valid = False
                            position -= 1
                            break
                        # end if
                        position += 1
                    # end while
                else:
                    position = strlen - 1
                    valid = False
                # end if
            # end if
            #// Percent encode anything invalid or not in ucschar
            if (not valid) or length > 1 and character <= 127 or length > 2 and character <= 2047 or length > 3 and character <= 65535 or character & 65534 == 65534 or character >= 64976 and character <= 65007 or character > 55295 and character < 63744 or character < 160 or character > 983037 and (not iprivate) or character < 57344 or character > 1114109:
                #// If we were a character, pretend we weren't, but rather an error.
                if valid:
                    position -= 1
                # end if
                j = start
                while j <= position:
                    
                    string = php_substr_replace(string, php_sprintf("%%%02X", php_ord(string[j])), j, 1)
                    j += 2
                    position += 2
                    strlen += 2
                    j += 1
                # end while
            # end if
        # end while
        return string
    # end def replace_invalid_with_pct_encoding
    #// 
    #// Callback function for preg_replace_callback.
    #// 
    #// Removes sequences of percent encoded bytes that represent UTF-8
    #// encoded characters in iunreserved
    #// 
    #// @param array $match PCRE match
    #// @return string Replacement
    #//
    def remove_iunreserved_percent_encoded(self, match=None):
        
        #// As we just have valid percent encoded sequences we can just explode
        #// and ignore the first member of the returned array (an empty string).
        bytes = php_explode("%", match[0])
        #// Initialize the new string (this is what will be returned) and that
        #// there are no bytes remaining in the current sequence (unsurprising
        #// at the first byte!).
        string = ""
        remaining = 0
        #// Loop over each and every byte, and set $value to its value
        i = 1
        len = php_count(bytes)
        while i < len:
            
            value = hexdec(bytes[i])
            #// If we're the first byte of sequence:
            if (not remaining):
                #// Start position
                start = i
                #// By default we are valid
                valid = True
                #// One byte sequence:
                if value <= 127:
                    character = value
                    length = 1
                    #// Two byte sequence:
                elif value & 224 == 192:
                    character = value & 31 << 6
                    length = 2
                    remaining = 1
                    #// Three byte sequence:
                elif value & 240 == 224:
                    character = value & 15 << 12
                    length = 3
                    remaining = 2
                    #// Four byte sequence:
                elif value & 248 == 240:
                    character = value & 7 << 18
                    length = 4
                    remaining = 3
                else:
                    valid = False
                    remaining = 0
                # end if
            else:
                #// Check that the byte is valid, then add it to the character:
                if value & 192 == 128:
                    remaining -= 1
                    character |= value & 63 << remaining * 6
                else:
                    valid = False
                    remaining = 0
                    i -= 1
                # end if
            # end if
            #// If we've reached the end of the current byte sequence, append it to Unicode::$data
            if (not remaining):
                #// Percent encode anything invalid or not in iunreserved
                if (not valid) or length > 1 and character <= 127 or length > 2 and character <= 2047 or length > 3 and character <= 65535 or character < 45 or character > 983037 or character & 65534 == 65534 or character >= 64976 and character <= 65007 or character == 47 or character > 57 and character < 65 or character > 90 and character < 97 or character > 122 and character < 126 or character > 126 and character < 160 or character > 55295 and character < 63744:
                    j = start
                    while j <= i:
                        
                        string += "%" + php_strtoupper(bytes[j])
                        j += 1
                    # end while
                else:
                    j = start
                    while j <= i:
                        
                        string += chr(hexdec(bytes[j]))
                        j += 1
                    # end while
                # end if
            # end if
            i += 1
        # end while
        #// If we have any bytes left over they are invalid (i.e., we are
        #// mid-way through a multi-byte sequence)
        if remaining:
            j = start
            while j < len:
                
                string += "%" + php_strtoupper(bytes[j])
                j += 1
            # end while
        # end if
        return string
    # end def remove_iunreserved_percent_encoded
    def scheme_normalization(self):
        
        if (php_isset(lambda : self.normalization[self.scheme]["iuserinfo"])) and self.iuserinfo == self.normalization[self.scheme]["iuserinfo"]:
            self.iuserinfo = None
        # end if
        if (php_isset(lambda : self.normalization[self.scheme]["ihost"])) and self.ihost == self.normalization[self.scheme]["ihost"]:
            self.ihost = None
        # end if
        if (php_isset(lambda : self.normalization[self.scheme]["port"])) and self.port == self.normalization[self.scheme]["port"]:
            self.port = None
        # end if
        if (php_isset(lambda : self.normalization[self.scheme]["ipath"])) and self.ipath == self.normalization[self.scheme]["ipath"]:
            self.ipath = ""
        # end if
        if (php_isset(lambda : self.ihost)) and php_empty(lambda : self.ipath):
            self.ipath = "/"
        # end if
        if (php_isset(lambda : self.normalization[self.scheme]["iquery"])) and self.iquery == self.normalization[self.scheme]["iquery"]:
            self.iquery = None
        # end if
        if (php_isset(lambda : self.normalization[self.scheme]["ifragment"])) and self.ifragment == self.normalization[self.scheme]["ifragment"]:
            self.ifragment = None
        # end if
    # end def scheme_normalization
    #// 
    #// Check if the object represents a valid IRI. This needs to be done on each
    #// call as some things change depending on another part of the IRI.
    #// 
    #// @return bool
    #//
    def is_valid(self):
        
        isauthority = self.iuserinfo != None or self.ihost != None or self.port != None
        if self.ipath != "" and isauthority and self.ipath[0] != "/" or self.scheme == None and (not isauthority) and php_strpos(self.ipath, ":") != False and True if php_strpos(self.ipath, "/") == False else php_strpos(self.ipath, ":") < php_strpos(self.ipath, "/"):
            return False
        # end if
        return True
    # end def is_valid
    #// 
    #// Set the entire IRI. Returns true on success, false on failure (if there
    #// are any invalid characters).
    #// 
    #// @param string $iri
    #// @return bool
    #//
    def set_iri(self, iri=None):
        
        set_iri.cache = None
        if (not set_iri.cache):
            set_iri.cache = Array()
        # end if
        if iri == None:
            return True
        # end if
        if (php_isset(lambda : set_iri.cache[iri])):
            self.scheme, self.iuserinfo, self.ihost, self.port, self.ipath, self.iquery, self.ifragment, return_ = set_iri.cache[iri]
            return return_
        # end if
        parsed = self.parse_iri(php_str(iri))
        return_ = self.set_scheme(parsed["scheme"]) and self.set_authority(parsed["authority"]) and self.set_path(parsed["path"]) and self.set_query(parsed["query"]) and self.set_fragment(parsed["fragment"])
        set_iri.cache[iri] = Array(self.scheme, self.iuserinfo, self.ihost, self.port, self.ipath, self.iquery, self.ifragment, return_)
        return return_
    # end def set_iri
    #// 
    #// Set the scheme. Returns true on success, false on failure (if there are
    #// any invalid characters).
    #// 
    #// @param string $scheme
    #// @return bool
    #//
    def set_scheme(self, scheme=None):
        
        if scheme == None:
            self.scheme = None
        elif (not php_preg_match("/^[A-Za-z][0-9A-Za-z+\\-.]*$/", scheme)):
            self.scheme = None
            return False
        else:
            self.scheme = php_strtolower(scheme)
        # end if
        return True
    # end def set_scheme
    #// 
    #// Set the authority. Returns true on success, false on failure (if there are
    #// any invalid characters).
    #// 
    #// @param string $authority
    #// @return bool
    #//
    def set_authority(self, authority=None):
        
        set_authority.cache = None
        if (not set_authority.cache):
            set_authority.cache = Array()
        # end if
        if authority == None:
            self.iuserinfo = None
            self.ihost = None
            self.port = None
            return True
        # end if
        if (php_isset(lambda : set_authority.cache[authority])):
            self.iuserinfo, self.ihost, self.port, return_ = set_authority.cache[authority]
            return return_
        # end if
        remaining = authority
        iuserinfo_end = php_strrpos(remaining, "@")
        if iuserinfo_end != False:
            iuserinfo = php_substr(remaining, 0, iuserinfo_end)
            remaining = php_substr(remaining, iuserinfo_end + 1)
        else:
            iuserinfo = None
        # end if
        port_start = php_strpos(remaining, ":", php_strpos(remaining, "]"))
        if port_start != False:
            port = php_substr(remaining, port_start + 1)
            if port == False or port == "":
                port = None
            # end if
            remaining = php_substr(remaining, 0, port_start)
        else:
            port = None
        # end if
        return_ = self.set_userinfo(iuserinfo) and self.set_host(remaining) and self.set_port(port)
        set_authority.cache[authority] = Array(self.iuserinfo, self.ihost, self.port, return_)
        return return_
    # end def set_authority
    #// 
    #// Set the iuserinfo.
    #// 
    #// @param string $iuserinfo
    #// @return bool
    #//
    def set_userinfo(self, iuserinfo=None):
        
        if iuserinfo == None:
            self.iuserinfo = None
        else:
            self.iuserinfo = self.replace_invalid_with_pct_encoding(iuserinfo, "!$&'()*+,;=:")
            self.scheme_normalization()
        # end if
        return True
    # end def set_userinfo
    #// 
    #// Set the ihost. Returns true on success, false on failure (if there are
    #// any invalid characters).
    #// 
    #// @param string $ihost
    #// @return bool
    #//
    def set_host(self, ihost=None):
        
        if ihost == None:
            self.ihost = None
            return True
        # end if
        if php_substr(ihost, 0, 1) == "[" and php_substr(ihost, -1) == "]":
            if Requests_IPv6.check_ipv6(php_substr(ihost, 1, -1)):
                self.ihost = "[" + Requests_IPv6.compress(php_substr(ihost, 1, -1)) + "]"
            else:
                self.ihost = None
                return False
            # end if
        else:
            ihost = self.replace_invalid_with_pct_encoding(ihost, "!$&'()*+,;=")
            #// Lowercase, but ignore pct-encoded sections (as they should
            #// remain uppercase). This must be done after the previous step
            #// as that can add unescaped characters.
            position = 0
            strlen = php_strlen(ihost)
            while True:
                
                if not (position += strcspn(ihost, "ABCDEFGHIJKLMNOPQRSTUVWXYZ%", position) < strlen):
                    break
                # end if
                if ihost[position] == "%":
                    position += 3
                else:
                    ihost[position] = php_strtolower(ihost[position])
                    position += 1
                # end if
            # end while
            self.ihost = ihost
        # end if
        self.scheme_normalization()
        return True
    # end def set_host
    #// 
    #// Set the port. Returns true on success, false on failure (if there are
    #// any invalid characters).
    #// 
    #// @param string $port
    #// @return bool
    #//
    def set_port(self, port=None):
        
        if port == None:
            self.port = None
            return True
        # end if
        if strspn(port, "0123456789") == php_strlen(port):
            self.port = php_int(port)
            self.scheme_normalization()
            return True
        # end if
        self.port = None
        return False
    # end def set_port
    #// 
    #// Set the ipath.
    #// 
    #// @param string $ipath
    #// @return bool
    #//
    def set_path(self, ipath=None):
        
        set_path.cache = None
        if (not set_path.cache):
            set_path.cache = Array()
        # end if
        ipath = php_str(ipath)
        if (php_isset(lambda : set_path.cache[ipath])):
            self.ipath = set_path.cache[ipath][php_int(self.scheme != None)]
        else:
            valid = self.replace_invalid_with_pct_encoding(ipath, "!$&'()*+,;=@:/")
            removed = self.remove_dot_segments(valid)
            set_path.cache[ipath] = Array(valid, removed)
            self.ipath = removed if self.scheme != None else valid
        # end if
        self.scheme_normalization()
        return True
    # end def set_path
    #// 
    #// Set the iquery.
    #// 
    #// @param string $iquery
    #// @return bool
    #//
    def set_query(self, iquery=None):
        
        if iquery == None:
            self.iquery = None
        else:
            self.iquery = self.replace_invalid_with_pct_encoding(iquery, "!$&'()*+,;=:@/?", True)
            self.scheme_normalization()
        # end if
        return True
    # end def set_query
    #// 
    #// Set the ifragment.
    #// 
    #// @param string $ifragment
    #// @return bool
    #//
    def set_fragment(self, ifragment=None):
        
        if ifragment == None:
            self.ifragment = None
        else:
            self.ifragment = self.replace_invalid_with_pct_encoding(ifragment, "!$&'()*+,;=:@/?")
            self.scheme_normalization()
        # end if
        return True
    # end def set_fragment
    #// 
    #// Convert an IRI to a URI (or parts thereof)
    #// 
    #// @param string|bool IRI to convert (or false from {@see get_iri})
    #// @return string|false URI if IRI is valid, false otherwise.
    #//
    def to_uri(self, string=None):
        
        if (not php_is_string(string)):
            return False
        # end if
        to_uri.non_ascii = None
        if (not to_uri.non_ascii):
            to_uri.non_ascii = php_implode("", range("", "ÿ"))
        # end if
        position = 0
        strlen = php_strlen(string)
        while True:
            
            if not (position += strcspn(string, to_uri.non_ascii, position) < strlen):
                break
            # end if
            string = php_substr_replace(string, php_sprintf("%%%02X", php_ord(string[position])), position, 1)
            position += 3
            strlen += 2
        # end while
        return string
    # end def to_uri
    #// 
    #// Get the complete IRI
    #// 
    #// @return string
    #//
    def get_iri(self):
        
        if (not self.is_valid()):
            return False
        # end if
        iri = ""
        if self.scheme != None:
            iri += self.scheme + ":"
        # end if
        iauthority = self.get_iauthority()
        if iauthority != None:
            iri += "//" + iauthority
        # end if
        iri += self.ipath
        if self.iquery != None:
            iri += "?" + self.iquery
        # end if
        if self.ifragment != None:
            iri += "#" + self.ifragment
        # end if
        return iri
    # end def get_iri
    #// 
    #// Get the complete URI
    #// 
    #// @return string
    #//
    def get_uri(self):
        
        return self.to_uri(self.get_iri())
    # end def get_uri
    #// 
    #// Get the complete iauthority
    #// 
    #// @return string
    #//
    def get_iauthority(self):
        
        if self.iuserinfo == None and self.ihost == None and self.port == None:
            return None
        # end if
        iauthority = ""
        if self.iuserinfo != None:
            iauthority += self.iuserinfo + "@"
        # end if
        if self.ihost != None:
            iauthority += self.ihost
        # end if
        if self.port != None:
            iauthority += ":" + self.port
        # end if
        return iauthority
    # end def get_iauthority
    #// 
    #// Get the complete authority
    #// 
    #// @return string
    #//
    def get_authority(self):
        
        iauthority = self.get_iauthority()
        if php_is_string(iauthority):
            return self.to_uri(iauthority)
        else:
            return iauthority
        # end if
    # end def get_authority
# end class Requests_IRI
