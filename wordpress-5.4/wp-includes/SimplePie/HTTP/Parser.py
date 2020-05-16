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
#// HTTP Response Parser
#// 
#// @package SimplePie
#// @subpackage HTTP
#//
class SimplePie_HTTP_Parser():
    http_version = 0
    status_code = 0
    reason = ""
    headers = Array()
    body = ""
    state = "http_version"
    data = ""
    data_length = 0
    position = 0
    name = ""
    value = ""
    #// 
    #// Create an instance of the class with the input data
    #// 
    #// @param string $data Input data
    #//
    def __init__(self, data=None):
        
        self.data = data
        self.data_length = php_strlen(self.data)
    # end def __init__
    #// 
    #// Parse the input data
    #// 
    #// @return bool true on success, false on failure
    #//
    def parse(self):
        
        while True:
            
            if not (self.state and self.state != "emit" and self.has_data()):
                break
            # end if
            state = self.state
            self.state()
        # end while
        self.data = ""
        if self.state == "emit" or self.state == "body":
            return True
        else:
            self.http_version = ""
            self.status_code = ""
            self.reason = ""
            self.headers = Array()
            self.body = ""
            return False
        # end if
    # end def parse
    #// 
    #// Check whether there is data beyond the pointer
    #// 
    #// @return bool true if there is further data, false if not
    #//
    def has_data(self):
        
        return php_bool(self.position < self.data_length)
    # end def has_data
    #// 
    #// See if the next character is LWS
    #// 
    #// @return bool true if the next character is LWS, false if not
    #//
    def is_linear_whitespace(self):
        
        return php_bool(self.data[self.position] == "   " or self.data[self.position] == " " or self.data[self.position] == "\n" and (php_isset(lambda : self.data[self.position + 1])) and self.data[self.position + 1] == "   " or self.data[self.position + 1] == " ")
    # end def is_linear_whitespace
    #// 
    #// Parse the HTTP version
    #//
    def http_version(self):
        
        if php_strpos(self.data, "\n") != False and php_strtoupper(php_substr(self.data, 0, 5)) == "HTTP/":
            len = strspn(self.data, "0123456789.", 5)
            self.http_version = php_substr(self.data, 5, len)
            self.position += 5 + len
            if php_substr_count(self.http_version, ".") <= 1:
                self.http_version = php_float(self.http_version)
                self.position += strspn(self.data, "     ", self.position)
                self.state = "status"
            else:
                self.state = False
            # end if
        else:
            self.state = False
        # end if
    # end def http_version
    #// 
    #// Parse the status code
    #//
    def status(self):
        
        len = strspn(self.data, "0123456789", self.position)
        if len:
            self.status_code = php_int(php_substr(self.data, self.position, len))
            self.position += len
            self.state = "reason"
        else:
            self.state = False
        # end if
    # end def status
    #// 
    #// Parse the reason phrase
    #//
    def reason(self):
        
        len = strcspn(self.data, "\n", self.position)
        self.reason = php_trim(php_substr(self.data, self.position, len), " \r ")
        self.position += len + 1
        self.state = "new_line"
    # end def reason
    #// 
    #// Deal with a new line, shifting data around as needed
    #//
    def new_line(self):
        
        self.value = php_trim(self.value, "\r ")
        if self.name != "" and self.value != "":
            self.name = php_strtolower(self.name)
            #// We should only use the last Content-Type header. c.f. issue #1
            if (php_isset(lambda : self.headers[self.name])) and self.name != "content-type":
                self.headers[self.name] += ", " + self.value
            else:
                self.headers[self.name] = self.value
            # end if
        # end if
        self.name = ""
        self.value = ""
        if php_substr(self.data[self.position], 0, 2) == "\r\n":
            self.position += 2
            self.state = "body"
        elif self.data[self.position] == "\n":
            self.position += 1
            self.state = "body"
        else:
            self.state = "name"
        # end if
    # end def new_line
    #// 
    #// Parse a header name
    #//
    def name(self):
        
        len = strcspn(self.data, "\n:", self.position)
        if (php_isset(lambda : self.data[self.position + len])):
            if self.data[self.position + len] == "\n":
                self.position += len
                self.state = "new_line"
            else:
                self.name = php_substr(self.data, self.position, len)
                self.position += len + 1
                self.state = "value"
            # end if
        else:
            self.state = False
        # end if
    # end def name
    #// 
    #// Parse LWS, replacing consecutive LWS characters with a single space
    #//
    def linear_whitespace(self):
        
        while True:
            if php_substr(self.data, self.position, 2) == "\r\n":
                self.position += 2
            elif self.data[self.position] == "\n":
                self.position += 1
            # end if
            self.position += strspn(self.data, "     ", self.position)
            
            if self.has_data() and self.is_linear_whitespace():
                break
            # end if
        # end while
        self.value += " "
    # end def linear_whitespace
    #// 
    #// See what state to move to while within non-quoted header values
    #//
    def value(self):
        
        if self.is_linear_whitespace():
            self.linear_whitespace()
        else:
            for case in Switch(self.data[self.position]):
                if case("\""):
                    #// Workaround for ETags: we have to include the quotes as
                    #// part of the tag.
                    if php_strtolower(self.name) == "etag":
                        self.value += "\""
                        self.position += 1
                        self.state = "value_char"
                        break
                    # end if
                    self.position += 1
                    self.state = "quote"
                    break
                # end if
                if case("\n"):
                    self.position += 1
                    self.state = "new_line"
                    break
                # end if
                if case():
                    self.state = "value_char"
                    break
                # end if
            # end for
        # end if
    # end def value
    #// 
    #// Parse a header value while outside quotes
    #//
    def value_char(self):
        
        len = strcspn(self.data, "   \n\"", self.position)
        self.value += php_substr(self.data, self.position, len)
        self.position += len
        self.state = "value"
    # end def value_char
    #// 
    #// See what state to move to while within quoted header values
    #//
    def quote(self):
        
        if self.is_linear_whitespace():
            self.linear_whitespace()
        else:
            for case in Switch(self.data[self.position]):
                if case("\""):
                    self.position += 1
                    self.state = "value"
                    break
                # end if
                if case("\n"):
                    self.position += 1
                    self.state = "new_line"
                    break
                # end if
                if case("\\"):
                    self.position += 1
                    self.state = "quote_escaped"
                    break
                # end if
                if case():
                    self.state = "quote_char"
                    break
                # end if
            # end for
        # end if
    # end def quote
    #// 
    #// Parse a header value while within quotes
    #//
    def quote_char(self):
        
        len = strcspn(self.data, "   \n\"\\", self.position)
        self.value += php_substr(self.data, self.position, len)
        self.position += len
        self.state = "value"
    # end def quote_char
    #// 
    #// Parse an escaped character within quotes
    #//
    def quote_escaped(self):
        
        self.value += self.data[self.position]
        self.position += 1
        self.state = "quote"
    # end def quote_escaped
    #// 
    #// Parse the body
    #//
    def body(self):
        
        self.body = php_substr(self.data, self.position)
        if (not php_empty(lambda : self.headers["transfer-encoding"])):
            self.headers["transfer-encoding"] = None
            self.state = "chunked"
        else:
            self.state = "emit"
        # end if
    # end def body
    #// 
    #// Parsed a "Transfer-Encoding: chunked" body
    #//
    def chunked(self):
        
        if (not php_preg_match("/^([0-9a-f]+)[^\\r\\n]*\\r\\n/i", php_trim(self.body))):
            self.state = "emit"
            return
        # end if
        decoded = ""
        encoded = self.body
        while True:
            
            if not (True):
                break
            # end if
            is_chunked = php_bool(php_preg_match("/^([0-9a-f]+)[^\\r\\n]*\\r\\n/i", encoded, matches))
            if (not is_chunked):
                #// Looks like it's not chunked after all
                self.state = "emit"
                return
            # end if
            length = hexdec(php_trim(matches[1]))
            if length == 0:
                #// Ignore trailer headers
                self.state = "emit"
                self.body = decoded
                return
            # end if
            chunk_length = php_strlen(matches[0])
            decoded += part = php_substr(encoded, chunk_length, length)
            encoded = php_substr(encoded, chunk_length + length + 2)
            if php_trim(encoded) == "0" or php_empty(lambda : encoded):
                self.state = "emit"
                self.body = decoded
                return
            # end if
        # end while
    # end def chunked
# end class SimplePie_HTTP_Parser
