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
#// SimplePie
#// 
#// A PHP-Based RSS and Atom Feed Framework.
#// Takes the hard work out of managing a complete RSS/Atom solution.
#// 
#// Copyright (c) 2004-2012, Ryan Parman, Geoffrey Sneddon, Ryan McCue, and contributors
#// All rights reserved.
#// 
#// Redistribution and use in source and binary forms, with or without modification, are
#// permitted provided that the following conditions are met:
#// 
#// Redistributions of source code must retain the above copyright notice, this list of
#// conditions and the following disclaimer.
#// 
#// Redistributions in binary form must reproduce the above copyright notice, this list
#// of conditions and the following disclaimer in the documentation and/or other materials
#// provided with the distribution.
#// 
#// Neither the name of the SimplePie Team nor the names of its contributors may be used
#// to endorse or promote products derived from this software without specific prior
#// written permission.
#// 
#// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS
#// OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY
#// AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDERS
#// AND CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
#// CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#// SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#// THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
#// OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
#// POSSIBILITY OF SUCH DAMAGE.
#// 
#// @package SimplePie
#// @version 1.3.1
#// @copyright 2004-2012 Ryan Parman, Geoffrey Sneddon, Ryan McCue
#// @author Ryan Parman
#// @author Geoffrey Sneddon
#// @author Ryan McCue
#// @link http://simplepie.org/ SimplePie
#// @license http://www.opensource.org/licenses/bsd-license.php BSD License
#// 
#// 
#// IRI parser/serialiser/normaliser
#// 
#// @package SimplePie
#// @subpackage HTTP
#// @author Geoffrey Sneddon
#// @author Steve Minutillo
#// @author Ryan McCue
#// @copyright 2007-2012 Geoffrey Sneddon, Steve Minutillo, Ryan McCue
#// @license http://www.opensource.org/licenses/bsd-license.php
#//
class SimplePie_IRI():
    #// 
    #// Scheme
    #// 
    #// @var string
    #//
    scheme = None
    #// 
    #// User Information
    #// 
    #// @var string
    #//
    iuserinfo = None
    #// 
    #// ihost
    #// 
    #// @var string
    #//
    ihost = None
    #// 
    #// Port
    #// 
    #// @var string
    #//
    port = None
    #// 
    #// ipath
    #// 
    #// @var string
    #//
    ipath = ""
    #// 
    #// iquery
    #// 
    #// @var string
    #//
    iquery = None
    #// 
    #// ifragment
    #// 
    #// @var string
    #//
    ifragment = None
    #// 
    #// Normalization database
    #// 
    #// Each key is the scheme, each value is an array with each key as the IRI
    #// part and value as the default value for that part.
    #//
    normalization = Array({"acap": Array({"port": 674})}, {"dict": Array({"port": 2628})}, {"file": Array({"ihost": "localhost"})}, {"http": Array({"port": 80, "ipath": "/"})}, {"https": Array({"port": 443, "ipath": "/"})})
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
    def __set(self, name_=None, value_=None):
        
        
        if php_method_exists(self, "set_" + name_):
            php_call_user_func(Array(self, "set_" + name_), value_)
        elif name_ == "iauthority" or name_ == "iuserinfo" or name_ == "ihost" or name_ == "ipath" or name_ == "iquery" or name_ == "ifragment":
            php_call_user_func(Array(self, "set_" + php_substr(name_, 1)), value_)
        # end if
    # end def __set
    #// 
    #// Overload __get() to provide access via properties
    #// 
    #// @param string $name Property name
    #// @return mixed
    #//
    def __get(self, name_=None):
        
        
        #// isset() returns false for null, we don't want to do that
        #// Also why we use array_key_exists below instead of isset()
        props_ = get_object_vars(self)
        if name_ == "iri" or name_ == "uri" or name_ == "iauthority" or name_ == "authority":
            return_ = self.str("get_") + str(name_)()
        elif php_array_key_exists(name_, props_):
            return_ = self.name_
            #// host -> ihost
        elif "i" + name_ and php_array_key_exists(prop_, props_):
            prop_ = "i" + name_
            name_ = prop_
            return_ = self.prop_
            #// ischeme -> scheme
        elif php_substr(name_, 1) and php_array_key_exists(prop_, props_):
            prop_ = php_substr(name_, 1)
            name_ = prop_
            return_ = self.prop_
        else:
            trigger_error("Undefined property: " + get_class(self) + "::" + name_, E_USER_NOTICE)
            return_ = None
        # end if
        if return_ == None and (php_isset(lambda : self.normalization[self.scheme][name_])):
            return self.normalization[self.scheme][name_]
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
    def __isset(self, name_=None):
        
        
        if php_method_exists(self, "get_" + name_) or (php_isset(lambda : self.name_)):
            return True
        else:
            return False
        # end if
    # end def __isset
    #// 
    #// Overload __unset() to provide access via properties
    #// 
    #// @param string $name Property name
    #//
    def __unset(self, name_=None):
        
        
        if php_method_exists(self, "set_" + name_):
            php_call_user_func(Array(self, "set_" + name_), "")
        # end if
    # end def __unset
    #// 
    #// Create a new IRI object, from a specified string
    #// 
    #// @param string $iri
    #//
    def __init__(self, iri_=None):
        
        
        self.set_iri(iri_)
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
    def absolutize(self, base_=None, relative_=None):
        
        
        if (not type(relative_).__name__ == "SimplePie_IRI"):
            relative_ = php_new_class("SimplePie_IRI", lambda : SimplePie_IRI(relative_))
        # end if
        if (not relative_.is_valid()):
            return False
        elif relative_.scheme != None:
            return copy.deepcopy(relative_)
        else:
            if (not type(base_).__name__ == "SimplePie_IRI"):
                base_ = php_new_class("SimplePie_IRI", lambda : SimplePie_IRI(base_))
            # end if
            if base_.scheme != None and base_.is_valid():
                if relative_.get_iri() != "":
                    if relative_.iuserinfo != None or relative_.ihost != None or relative_.port != None:
                        target_ = copy.deepcopy(relative_)
                        target_.scheme = base_.scheme
                    else:
                        target_ = php_new_class("SimplePie_IRI", lambda : SimplePie_IRI())
                        target_.scheme = base_.scheme
                        target_.iuserinfo = base_.iuserinfo
                        target_.ihost = base_.ihost
                        target_.port = base_.port
                        if relative_.ipath != "":
                            if relative_.ipath[0] == "/":
                                target_.ipath = relative_.ipath
                            elif base_.iuserinfo != None or base_.ihost != None or base_.port != None and base_.ipath == "":
                                target_.ipath = "/" + relative_.ipath
                            elif php_strrpos(base_.ipath, "/") != False:
                                last_segment_ = php_strrpos(base_.ipath, "/")
                                target_.ipath = php_substr(base_.ipath, 0, last_segment_ + 1) + relative_.ipath
                            else:
                                target_.ipath = relative_.ipath
                            # end if
                            target_.ipath = target_.remove_dot_segments(target_.ipath)
                            target_.iquery = relative_.iquery
                        else:
                            target_.ipath = base_.ipath
                            if relative_.iquery != None:
                                target_.iquery = relative_.iquery
                            elif base_.iquery != None:
                                target_.iquery = base_.iquery
                            # end if
                        # end if
                        target_.ifragment = relative_.ifragment
                    # end if
                else:
                    target_ = copy.deepcopy(base_)
                    target_.ifragment = None
                # end if
                target_.scheme_normalization()
                return target_
            else:
                return False
            # end if
        # end if
    # end def absolutize
    #// 
    #// Parse an IRI into scheme/authority/path/query/fragment segments
    #// 
    #// @param string $iri
    #// @return array
    #//
    def parse_iri(self, iri_=None):
        
        
        iri_ = php_trim(iri_, "     \n\r")
        if php_preg_match("/^((?P<scheme>[^:\\/?#]+):)?(\\/\\/(?P<authority>[^\\/?#]*))?(?P<path>[^?#]*)(\\?(?P<query>[^#]*))?(#(?P<fragment>.*))?$/", iri_, match_):
            if match_[1] == "":
                match_["scheme"] = None
            # end if
            if (not (php_isset(lambda : match_[3]))) or match_[3] == "":
                match_["authority"] = None
            # end if
            if (not (php_isset(lambda : match_[5]))):
                match_["path"] = ""
            # end if
            if (not (php_isset(lambda : match_[6]))) or match_[6] == "":
                match_["query"] = None
            # end if
            if (not (php_isset(lambda : match_[8]))) or match_[8] == "":
                match_["fragment"] = None
            # end if
            return match_
        else:
            #// This can occur when a paragraph is accidentally parsed as a URI
            return False
        # end if
    # end def parse_iri
    #// 
    #// Remove dot segments from a path
    #// 
    #// @param string $input
    #// @return string
    #//
    def remove_dot_segments(self, input_=None):
        
        
        output_ = ""
        while True:
            
            if not (php_strpos(input_, "./") != False or php_strpos(input_, "/.") != False or input_ == "." or input_ == ".."):
                break
            # end if
            #// A: If the input buffer begins with a prefix of "../" or "./", then remove that prefix from the input buffer; otherwise,
            if php_strpos(input_, "../") == 0:
                input_ = php_substr(input_, 3)
            elif php_strpos(input_, "./") == 0:
                input_ = php_substr(input_, 2)
                #// B: if the input buffer begins with a prefix of "/./" or "/.", where "." is a complete path segment, then replace that prefix with "/" in the input buffer; otherwise,
            elif php_strpos(input_, "/./") == 0:
                input_ = php_substr(input_, 2)
            elif input_ == "/.":
                input_ = "/"
                #// C: if the input buffer begins with a prefix of "/../" or "/..", where ".." is a complete path segment, then replace that prefix with "/" in the input buffer and remove the last segment and its preceding "/" (if any) from the output buffer; otherwise,
            elif php_strpos(input_, "/../") == 0:
                input_ = php_substr(input_, 3)
                output_ = php_substr_replace(output_, "", php_strrpos(output_, "/"))
            elif input_ == "/..":
                input_ = "/"
                output_ = php_substr_replace(output_, "", php_strrpos(output_, "/"))
                #// D: if the input buffer consists only of "." or "..", then remove that from the input buffer; otherwise,
            elif input_ == "." or input_ == "..":
                input_ = ""
                #// E: move the first path segment in the input buffer to the end of the output buffer, including the initial "/" character (if any) and any subsequent characters up to, but not including, the next "/" character or the end of the input buffer
            elif php_strpos(input_, "/", 1) != False:
                pos_ = php_strpos(input_, "/", 1)
                output_ += php_substr(input_, 0, pos_)
                input_ = php_substr_replace(input_, "", 0, pos_)
            else:
                output_ += input_
                input_ = ""
            # end if
        # end while
        return output_ + input_
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
    def replace_invalid_with_pct_encoding(self, string_=None, extra_chars_=None, iprivate_=None):
        if iprivate_ is None:
            iprivate_ = False
        # end if
        
        #// Normalize as many pct-encoded sections as possible
        string_ = preg_replace_callback("/(?:%[A-Fa-f0-9]{2})+/", Array(self, "remove_iunreserved_percent_encoded"), string_)
        #// Replace invalid percent characters
        string_ = php_preg_replace("/%(?![A-Fa-f0-9]{2})/", "%25", string_)
        #// Add unreserved and % to $extra_chars (the latter is safe because all
        #// pct-encoded sections are now valid).
        extra_chars_ += "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~%"
        #// Now replace any bytes that aren't allowed with their pct-encoded versions
        position_ = 0
        strlen_ = php_strlen(string_)
        while True:
            
            if not (position_ += strspn(string_, extra_chars_, position_) < strlen_):
                break
            # end if
            value_ = php_ord(string_[position_])
            #// Start position
            start_ = position_
            #// By default we are valid
            valid_ = True
            #// No one byte sequences are valid due to the while.
            #// Two byte sequence:
            if value_ & 224 == 192:
                character_ = value_ & 31 << 6
                length_ = 2
                remaining_ = 1
                #// Three byte sequence:
            elif value_ & 240 == 224:
                character_ = value_ & 15 << 12
                length_ = 3
                remaining_ = 2
                #// Four byte sequence:
            elif value_ & 248 == 240:
                character_ = value_ & 7 << 18
                length_ = 4
                remaining_ = 3
            else:
                valid_ = False
                length_ = 1
                remaining_ = 0
            # end if
            if remaining_:
                if position_ + length_ <= strlen_:
                    position_ += 1
                    while remaining_:
                        
                        value_ = php_ord(string_[position_])
                        #// Check that the byte is valid, then add it to the character:
                        if value_ & 192 == 128:
                            remaining_ -= 1
                            character_ |= value_ & 63 << remaining_ * 6
                        else:
                            valid_ = False
                            position_ -= 1
                            break
                        # end if
                        position_ += 1
                    # end while
                else:
                    position_ = strlen_ - 1
                    valid_ = False
                # end if
            # end if
            #// Percent encode anything invalid or not in ucschar
            if (not valid_) or length_ > 1 and character_ <= 127 or length_ > 2 and character_ <= 2047 or length_ > 3 and character_ <= 65535 or character_ & 65534 == 65534 or character_ >= 64976 and character_ <= 65007 or character_ > 55295 and character_ < 63744 or character_ < 160 or character_ > 983037 and (not iprivate_) or character_ < 57344 or character_ > 1114109:
                #// If we were a character, pretend we weren't, but rather an error.
                if valid_:
                    position_ -= 1
                # end if
                j_ = start_
                while j_ <= position_:
                    
                    string_ = php_substr_replace(string_, php_sprintf("%%%02X", php_ord(string_[j_])), j_, 1)
                    j_ += 2
                    position_ += 2
                    strlen_ += 2
                    j_ += 1
                # end while
            # end if
        # end while
        return string_
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
    def remove_iunreserved_percent_encoded(self, match_=None):
        
        
        #// As we just have valid percent encoded sequences we can just explode
        #// and ignore the first member of the returned array (an empty string).
        bytes_ = php_explode("%", match_[0])
        #// Initialize the new string (this is what will be returned) and that
        #// there are no bytes remaining in the current sequence (unsurprising
        #// at the first byte!).
        string_ = ""
        remaining_ = 0
        #// Loop over each and every byte, and set $value to its value
        i_ = 1
        len_ = php_count(bytes_)
        while i_ < len_:
            
            value_ = hexdec(bytes_[i_])
            #// If we're the first byte of sequence:
            if (not remaining_):
                #// Start position
                start_ = i_
                #// By default we are valid
                valid_ = True
                #// One byte sequence:
                if value_ <= 127:
                    character_ = value_
                    length_ = 1
                    #// Two byte sequence:
                elif value_ & 224 == 192:
                    character_ = value_ & 31 << 6
                    length_ = 2
                    remaining_ = 1
                    #// Three byte sequence:
                elif value_ & 240 == 224:
                    character_ = value_ & 15 << 12
                    length_ = 3
                    remaining_ = 2
                    #// Four byte sequence:
                elif value_ & 248 == 240:
                    character_ = value_ & 7 << 18
                    length_ = 4
                    remaining_ = 3
                else:
                    valid_ = False
                    remaining_ = 0
                # end if
            else:
                #// Check that the byte is valid, then add it to the character:
                if value_ & 192 == 128:
                    remaining_ -= 1
                    character_ |= value_ & 63 << remaining_ * 6
                else:
                    valid_ = False
                    remaining_ = 0
                    i_ -= 1
                # end if
            # end if
            #// If we've reached the end of the current byte sequence, append it to Unicode::$data
            if (not remaining_):
                #// Percent encode anything invalid or not in iunreserved
                if (not valid_) or length_ > 1 and character_ <= 127 or length_ > 2 and character_ <= 2047 or length_ > 3 and character_ <= 65535 or character_ < 45 or character_ > 983037 or character_ & 65534 == 65534 or character_ >= 64976 and character_ <= 65007 or character_ == 47 or character_ > 57 and character_ < 65 or character_ > 90 and character_ < 97 or character_ > 122 and character_ < 126 or character_ > 126 and character_ < 160 or character_ > 55295 and character_ < 63744:
                    j_ = start_
                    while j_ <= i_:
                        
                        string_ += "%" + php_strtoupper(bytes_[j_])
                        j_ += 1
                    # end while
                else:
                    j_ = start_
                    while j_ <= i_:
                        
                        string_ += chr(hexdec(bytes_[j_]))
                        j_ += 1
                    # end while
                # end if
            # end if
            i_ += 1
        # end while
        #// If we have any bytes left over they are invalid (i.e., we are
        #// mid-way through a multi-byte sequence)
        if remaining_:
            j_ = start_
            while j_ < len_:
                
                string_ += "%" + php_strtoupper(bytes_[j_])
                j_ += 1
            # end while
        # end if
        return string_
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
        
        
        isauthority_ = self.iuserinfo != None or self.ihost != None or self.port != None
        if self.ipath != "" and isauthority_ and self.ipath[0] != "/" or php_substr(self.ipath, 0, 2) == "//" or self.scheme == None and (not isauthority_) and php_strpos(self.ipath, ":") != False and True if php_strpos(self.ipath, "/") == False else php_strpos(self.ipath, ":") < php_strpos(self.ipath, "/"):
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
    def set_iri(self, iri_=None):
        
        
        cache_ = None
        if (not cache_):
            cache_ = Array()
        # end if
        if iri_ == None:
            return True
        elif (php_isset(lambda : cache_[iri_])):
            self.scheme, self.iuserinfo, self.ihost, self.port, self.ipath, self.iquery, self.ifragment, return_ = cache_[iri_]
            return return_
        else:
            parsed_ = self.parse_iri(php_str(iri_))
            if (not parsed_):
                return False
            # end if
            return_ = self.set_scheme(parsed_["scheme"]) and self.set_authority(parsed_["authority"]) and self.set_path(parsed_["path"]) and self.set_query(parsed_["query"]) and self.set_fragment(parsed_["fragment"])
            cache_[iri_] = Array(self.scheme, self.iuserinfo, self.ihost, self.port, self.ipath, self.iquery, self.ifragment, return_)
            return return_
        # end if
    # end def set_iri
    #// 
    #// Set the scheme. Returns true on success, false on failure (if there are
    #// any invalid characters).
    #// 
    #// @param string $scheme
    #// @return bool
    #//
    def set_scheme(self, scheme_=None):
        
        
        if scheme_ == None:
            self.scheme = None
        elif (not php_preg_match("/^[A-Za-z][0-9A-Za-z+\\-.]*$/", scheme_)):
            self.scheme = None
            return False
        else:
            self.scheme = php_strtolower(scheme_)
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
    def set_authority(self, authority_=None):
        
        
        cache_ = None
        if (not cache_):
            cache_ = Array()
        # end if
        if authority_ == None:
            self.iuserinfo = None
            self.ihost = None
            self.port = None
            return True
        elif (php_isset(lambda : cache_[authority_])):
            self.iuserinfo, self.ihost, self.port, return_ = cache_[authority_]
            return return_
        else:
            remaining_ = authority_
            iuserinfo_end_ = php_strrpos(remaining_, "@")
            if iuserinfo_end_ != False:
                iuserinfo_ = php_substr(remaining_, 0, iuserinfo_end_)
                remaining_ = php_substr(remaining_, iuserinfo_end_ + 1)
            else:
                iuserinfo_ = None
            # end if
            port_start_ = php_strpos(remaining_, ":", php_strpos(remaining_, "]"))
            if port_start_ != False:
                port_ = php_substr(remaining_, port_start_ + 1)
                if port_ == False:
                    port_ = None
                # end if
                remaining_ = php_substr(remaining_, 0, port_start_)
            else:
                port_ = None
            # end if
            return_ = self.set_userinfo(iuserinfo_) and self.set_host(remaining_) and self.set_port(port_)
            cache_[authority_] = Array(self.iuserinfo, self.ihost, self.port, return_)
            return return_
        # end if
    # end def set_authority
    #// 
    #// Set the iuserinfo.
    #// 
    #// @param string $iuserinfo
    #// @return bool
    #//
    def set_userinfo(self, iuserinfo_=None):
        
        
        if iuserinfo_ == None:
            self.iuserinfo = None
        else:
            self.iuserinfo = self.replace_invalid_with_pct_encoding(iuserinfo_, "!$&'()*+,;=:")
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
    def set_host(self, ihost_=None):
        
        
        if ihost_ == None:
            self.ihost = None
            return True
        elif php_substr(ihost_, 0, 1) == "[" and php_substr(ihost_, -1) == "]":
            if SimplePie_Net_IPv6.check_ipv6(php_substr(ihost_, 1, -1)):
                self.ihost = "[" + SimplePie_Net_IPv6.compress(php_substr(ihost_, 1, -1)) + "]"
            else:
                self.ihost = None
                return False
            # end if
        else:
            ihost_ = self.replace_invalid_with_pct_encoding(ihost_, "!$&'()*+,;=")
            #// Lowercase, but ignore pct-encoded sections (as they should
            #// remain uppercase). This must be done after the previous step
            #// as that can add unescaped characters.
            position_ = 0
            strlen_ = php_strlen(ihost_)
            while True:
                
                if not (position_ += strcspn(ihost_, "ABCDEFGHIJKLMNOPQRSTUVWXYZ%", position_) < strlen_):
                    break
                # end if
                if ihost_[position_] == "%":
                    position_ += 3
                else:
                    ihost_[position_] = php_strtolower(ihost_[position_])
                    position_ += 1
                # end if
            # end while
            self.ihost = ihost_
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
    def set_port(self, port_=None):
        
        
        if port_ == None:
            self.port = None
            return True
        elif strspn(port_, "0123456789") == php_strlen(port_):
            self.port = php_int(port_)
            self.scheme_normalization()
            return True
        else:
            self.port = None
            return False
        # end if
    # end def set_port
    #// 
    #// Set the ipath.
    #// 
    #// @param string $ipath
    #// @return bool
    #//
    def set_path(self, ipath_=None):
        
        
        cache_ = None
        if (not cache_):
            cache_ = Array()
        # end if
        ipath_ = php_str(ipath_)
        if (php_isset(lambda : cache_[ipath_])):
            self.ipath = cache_[ipath_][php_int(self.scheme != None)]
        else:
            valid_ = self.replace_invalid_with_pct_encoding(ipath_, "!$&'()*+,;=@:/")
            removed_ = self.remove_dot_segments(valid_)
            cache_[ipath_] = Array(valid_, removed_)
            self.ipath = removed_ if self.scheme != None else valid_
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
    def set_query(self, iquery_=None):
        
        
        if iquery_ == None:
            self.iquery = None
        else:
            self.iquery = self.replace_invalid_with_pct_encoding(iquery_, "!$&'()*+,;=:@/?", True)
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
    def set_fragment(self, ifragment_=None):
        
        
        if ifragment_ == None:
            self.ifragment = None
        else:
            self.ifragment = self.replace_invalid_with_pct_encoding(ifragment_, "!$&'()*+,;=:@/?")
            self.scheme_normalization()
        # end if
        return True
    # end def set_fragment
    #// 
    #// Convert an IRI to a URI (or parts thereof)
    #// 
    #// @return string
    #//
    def to_uri(self, string_=None):
        
        
        non_ascii_ = None
        if (not non_ascii_):
            non_ascii_ = php_implode("", range("", "ÿ"))
        # end if
        position_ = 0
        strlen_ = php_strlen(string_)
        while True:
            
            if not (position_ += strcspn(string_, non_ascii_, position_) < strlen_):
                break
            # end if
            string_ = php_substr_replace(string_, php_sprintf("%%%02X", php_ord(string_[position_])), position_, 1)
            position_ += 3
            strlen_ += 2
        # end while
        return string_
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
        iri_ = ""
        if self.scheme != None:
            iri_ += self.scheme + ":"
        # end if
        iauthority_ = self.get_iauthority()
        if iauthority_ != None:
            iri_ += "//" + iauthority_
        # end if
        if self.ipath != "":
            iri_ += self.ipath
        elif (not php_empty(lambda : self.normalization[self.scheme]["ipath"])) and iauthority_ != None and iauthority_ != "":
            iri_ += self.normalization[self.scheme]["ipath"]
        # end if
        if self.iquery != None:
            iri_ += "?" + self.iquery
        # end if
        if self.ifragment != None:
            iri_ += "#" + self.ifragment
        # end if
        return iri_
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
        
        
        if self.iuserinfo != None or self.ihost != None or self.port != None:
            iauthority_ = ""
            if self.iuserinfo != None:
                iauthority_ += self.iuserinfo + "@"
            # end if
            if self.ihost != None:
                iauthority_ += self.ihost
            # end if
            if self.port != None:
                iauthority_ += ":" + self.port
            # end if
            return iauthority_
        else:
            return None
        # end if
    # end def get_iauthority
    #// 
    #// Get the complete authority
    #// 
    #// @return string
    #//
    def get_authority(self):
        
        
        iauthority_ = self.get_iauthority()
        if php_is_string(iauthority_):
            return self.to_uri(iauthority_)
        else:
            return iauthority_
        # end if
    # end def get_authority
# end class SimplePie_IRI
