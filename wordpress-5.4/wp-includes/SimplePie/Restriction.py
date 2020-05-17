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
#// Handles `<media:restriction>` as defined in Media RSS
#// 
#// Used by {@see SimplePie_Enclosure::get_restriction()} and {@see SimplePie_Enclosure::get_restrictions()}
#// 
#// This class can be overloaded with {@see SimplePie::set_restriction_class()}
#// 
#// @package SimplePie
#// @subpackage API
#//
class SimplePie_Restriction():
    #// 
    #// Relationship ('allow'/'deny')
    #// 
    #// @var string
    #// @see get_relationship()
    #//
    relationship = Array()
    #// 
    #// Type of restriction
    #// 
    #// @var string
    #// @see get_type()
    #//
    type = Array()
    #// 
    #// Restricted values
    #// 
    #// @var string
    #// @see get_value()
    #//
    value = Array()
    #// 
    #// Constructor, used to input the data
    #// 
    #// For documentation on all the parameters, see the corresponding
    #// properties and their accessors
    #//
    def __init__(self, relationship_=None, type_=None, value_=None):
        if relationship_ is None:
            relationship_ = None
        # end if
        if type_ is None:
            type_ = None
        # end if
        if value_ is None:
            value_ = None
        # end if
        
        self.relationship = relationship_
        self.type = type_
        self.value = value_
    # end def __init__
    #// 
    #// String-ified version
    #// 
    #// @return string
    #//
    def __tostring(self):
        
        
        #// There is no $this->data here
        return php_md5(serialize(self))
    # end def __tostring
    #// 
    #// Get the relationship
    #// 
    #// @return string|null Either 'allow' or 'deny'
    #//
    def get_relationship(self):
        
        
        if self.relationship != None:
            return self.relationship
        else:
            return None
        # end if
    # end def get_relationship
    #// 
    #// Get the type
    #// 
    #// @return string|null
    #//
    def get_type(self):
        
        
        if self.type != None:
            return self.type
        else:
            return None
        # end if
    # end def get_type
    #// 
    #// Get the list of restricted things
    #// 
    #// @return string|null
    #//
    def get_value(self):
        
        
        if self.value != None:
            return self.value
        else:
            return None
        # end if
    # end def get_value
# end class SimplePie_Restriction
