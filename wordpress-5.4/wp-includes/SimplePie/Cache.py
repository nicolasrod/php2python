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
#// Used to create cache objects
#// 
#// This class can be overloaded with {@see SimplePie::set_cache_class()},
#// although the preferred way is to create your own handler
#// via {@see register()}
#// 
#// @package SimplePie
#// @subpackage Caching
#//
class SimplePie_Cache():
    #// 
    #// Cache handler classes
    #// 
    #// These receive 3 parameters to their constructor, as documented in
    #// {@see register()}
    #// @var array
    #//
    handlers = Array({"mysql": "SimplePie_Cache_MySQL", "memcache": "SimplePie_Cache_Memcache"})
    #// 
    #// Don't call the constructor. Please.
    #//
    def __init__(self):
        
        
        pass
    # end def __init__
    #// 
    #// Create a new SimplePie_Cache object
    #// 
    #// @param string $location URL location (scheme is used to determine handler)
    #// @param string $filename Unique identifier for cache object
    #// @param string $extension 'spi' or 'spc'
    #// @return SimplePie_Cache_Base Type of object depends on scheme of `$location`
    #//
    @classmethod
    def get_handler(self, location_=None, filename_=None, extension_=None):
        
        
        type_ = php_explode(":", location_, 2)
        type_ = type_[0]
        if (not php_empty(lambda : self.handlers[type_])):
            class_ = self.handlers[type_]
            return php_new_class(class_, lambda : {**locals(), **globals()}[class_](location_, filename_, extension_))
        # end if
        return php_new_class("SimplePie_Cache_File", lambda : SimplePie_Cache_File(location_, filename_, extension_))
    # end def get_handler
    #// 
    #// Create a new SimplePie_Cache object
    #// 
    #// @deprecated Use {@see get_handler} instead
    #//
    def create(self, location_=None, filename_=None, extension_=None):
        
        
        trigger_error("Cache::create() has been replaced with Cache::get_handler(). Switch to the registry system to use this.", E_USER_DEPRECATED)
        return self.get_handler(location_, filename_, extension_)
    # end def create
    #// 
    #// Register a handler
    #// 
    #// @param string $type DSN type to register for
    #// @param string $class Name of handler class. Must implement SimplePie_Cache_Base
    #//
    @classmethod
    def register(self, type_=None, class_=None):
        
        
        self.handlers[type_] = class_
    # end def register
    #// 
    #// Parse a URL into an array
    #// 
    #// @param string $url
    #// @return array
    #//
    @classmethod
    def parse_url(self, url_=None):
        
        
        params_ = php_parse_url(url_)
        params_["extras"] = Array()
        if (php_isset(lambda : params_["query"])):
            parse_str(params_["query"], params_["extras"])
        # end if
        return params_
    # end def parse_url
# end class SimplePie_Cache
