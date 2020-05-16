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
#// Parses the XML Declaration
#// 
#// @package SimplePie
#// @subpackage Parsing
#//
class SimplePie_XML_Declaration_Parser():
    version = "1.0"
    encoding = "UTF-8"
    standalone = False
    state = "before_version_name"
    data = ""
    data_length = 0
    position = 0
    #// 
    #// Create an instance of the class with the input data
    #// 
    #// @access public
    #// @param string $data Input data
    #//
    def __init__(self, data=None):
        
        self.data = data
        self.data_length = php_strlen(self.data)
    # end def __init__
    #// 
    #// Parse the input data
    #// 
    #// @access public
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
        if self.state == "emit":
            return True
        else:
            self.version = ""
            self.encoding = ""
            self.standalone = ""
            return False
        # end if
    # end def parse
    #// 
    #// Check whether there is data beyond the pointer
    #// 
    #// @access private
    #// @return bool true if there is further data, false if not
    #//
    def has_data(self):
        
        return php_bool(self.position < self.data_length)
    # end def has_data
    #// 
    #// Advance past any whitespace
    #// 
    #// @return int Number of whitespace characters passed
    #//
    def skip_whitespace(self):
        
        whitespace = strspn(self.data, "    \n\r ", self.position)
        self.position += whitespace
        return whitespace
    # end def skip_whitespace
    #// 
    #// Read value
    #//
    def get_value(self):
        
        quote = php_substr(self.data, self.position, 1)
        if quote == "\"" or quote == "'":
            self.position += 1
            len = strcspn(self.data, quote, self.position)
            if self.has_data():
                value = php_substr(self.data, self.position, len)
                self.position += len + 1
                return value
            # end if
        # end if
        return False
    # end def get_value
    def before_version_name(self):
        
        if self.skip_whitespace():
            self.state = "version_name"
        else:
            self.state = False
        # end if
    # end def before_version_name
    def version_name(self):
        
        if php_substr(self.data, self.position, 7) == "version":
            self.position += 7
            self.skip_whitespace()
            self.state = "version_equals"
        else:
            self.state = False
        # end if
    # end def version_name
    def version_equals(self):
        
        if php_substr(self.data, self.position, 1) == "=":
            self.position += 1
            self.skip_whitespace()
            self.state = "version_value"
        else:
            self.state = False
        # end if
    # end def version_equals
    def version_value(self):
        
        self.version = self.get_value()
        if self.version:
            self.skip_whitespace()
            if self.has_data():
                self.state = "encoding_name"
            else:
                self.state = "emit"
            # end if
        else:
            self.state = False
        # end if
    # end def version_value
    def encoding_name(self):
        
        if php_substr(self.data, self.position, 8) == "encoding":
            self.position += 8
            self.skip_whitespace()
            self.state = "encoding_equals"
        else:
            self.state = "standalone_name"
        # end if
    # end def encoding_name
    def encoding_equals(self):
        
        if php_substr(self.data, self.position, 1) == "=":
            self.position += 1
            self.skip_whitespace()
            self.state = "encoding_value"
        else:
            self.state = False
        # end if
    # end def encoding_equals
    def encoding_value(self):
        
        self.encoding = self.get_value()
        if self.encoding:
            self.skip_whitespace()
            if self.has_data():
                self.state = "standalone_name"
            else:
                self.state = "emit"
            # end if
        else:
            self.state = False
        # end if
    # end def encoding_value
    def standalone_name(self):
        
        if php_substr(self.data, self.position, 10) == "standalone":
            self.position += 10
            self.skip_whitespace()
            self.state = "standalone_equals"
        else:
            self.state = False
        # end if
    # end def standalone_name
    def standalone_equals(self):
        
        if php_substr(self.data, self.position, 1) == "=":
            self.position += 1
            self.skip_whitespace()
            self.state = "standalone_value"
        else:
            self.state = False
        # end if
    # end def standalone_equals
    def standalone_value(self):
        
        standalone = self.get_value()
        if standalone:
            for case in Switch(standalone):
                if case("yes"):
                    self.standalone = True
                    break
                # end if
                if case("no"):
                    self.standalone = False
                    break
                # end if
                if case():
                    self.state = False
                    return
                # end if
            # end for
            self.skip_whitespace()
            if self.has_data():
                self.state = False
            else:
                self.state = "emit"
            # end if
        else:
            self.state = False
        # end if
    # end def standalone_value
# end class SimplePie_XML_Declaration_Parser
