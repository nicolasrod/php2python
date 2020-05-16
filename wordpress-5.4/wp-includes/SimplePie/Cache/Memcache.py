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
#// Caches data to memcache
#// 
#// Registered for URLs with the "memcache" protocol
#// 
#// For example, `memcache://localhost:11211/?timeout=3600&prefix=sp_` will
#// connect to memcache on `localhost` on port 11211. All tables will be
#// prefixed with `sp_` and data will expire after 3600 seconds
#// 
#// @package SimplePie
#// @subpackage Caching
#// @uses Memcache
#//
class SimplePie_Cache_Memcache(SimplePie_Cache_Base):
    cache = Array()
    options = Array()
    name = Array()
    #// 
    #// Create a new cache object
    #// 
    #// @param string $location Location string (from SimplePie::$cache_location)
    #// @param string $name Unique ID for the cache
    #// @param string $type Either TYPE_FEED for SimplePie data, or TYPE_IMAGE for image data
    #//
    def __init__(self, location=None, name=None, type=None):
        
        self.options = Array({"host": "127.0.0.1", "port": 11211, "extras": Array({"timeout": 3600, "prefix": "simplepie_"})})
        parsed = SimplePie_Cache.parse_url(location)
        self.options["host"] = self.options["host"] if php_empty(lambda : parsed["host"]) else parsed["host"]
        self.options["port"] = self.options["port"] if php_empty(lambda : parsed["port"]) else parsed["port"]
        self.options["extras"] = php_array_merge(self.options["extras"], parsed["extras"])
        self.name = self.options["extras"]["prefix"] + php_md5(str(name) + str(":") + str(type))
        self.cache = php_new_class("Memcache", lambda : Memcache())
        self.cache.addserver(self.options["host"], php_int(self.options["port"]))
    # end def __init__
    #// 
    #// Save data to the cache
    #// 
    #// @param array|SimplePie $data Data to store in the cache. If passed a SimplePie object, only cache the $data property
    #// @return bool Successfulness
    #//
    def save(self, data=None):
        
        if type(data).__name__ == "SimplePie":
            data = data.data
        # end if
        return self.cache.set(self.name, serialize(data), MEMCACHE_COMPRESSED, php_int(self.options["extras"]["timeout"]))
    # end def save
    #// 
    #// Retrieve the data saved to the cache
    #// 
    #// @return array Data for SimplePie::$data
    #//
    def load(self):
        
        data = self.cache.get(self.name)
        if data != False:
            return unserialize(data)
        # end if
        return False
    # end def load
    #// 
    #// Retrieve the last modified time for the cache
    #// 
    #// @return int Timestamp
    #//
    def mtime(self):
        
        data = self.cache.get(self.name)
        if data != False:
            #// essentially ignore the mtime because Memcache expires on it's own
            return time()
        # end if
        return False
    # end def mtime
    #// 
    #// Set the last modified time to the current time
    #// 
    #// @return bool Success status
    #//
    def touch(self):
        
        data = self.cache.get(self.name)
        if data != False:
            return self.cache.set(self.name, data, MEMCACHE_COMPRESSED, php_int(self.duration))
        # end if
        return False
    # end def touch
    #// 
    #// Remove the cache
    #// 
    #// @return bool Success status
    #//
    def unlink(self):
        
        return self.cache.delete(self.name, 0)
    # end def unlink
# end class SimplePie_Cache_Memcache
