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
#// Caches data to the filesystem
#// 
#// @package SimplePie
#// @subpackage Caching
#//
class SimplePie_Cache_File(SimplePie_Cache_Base):
    #// 
    #// Location string
    #// 
    #// @see SimplePie::$cache_location
    #// @var string
    #//
    location = Array()
    #// 
    #// Filename
    #// 
    #// @var string
    #//
    filename = Array()
    #// 
    #// File extension
    #// 
    #// @var string
    #//
    extension = Array()
    #// 
    #// File path
    #// 
    #// @var string
    #//
    name = Array()
    #// 
    #// Create a new cache object
    #// 
    #// @param string $location Location string (from SimplePie::$cache_location)
    #// @param string $name Unique ID for the cache
    #// @param string $type Either TYPE_FEED for SimplePie data, or TYPE_IMAGE for image data
    #//
    def __init__(self, location_=None, name_=None, type_=None):
        
        
        self.location = location_
        self.filename = name_
        self.extension = type_
        self.name = str(self.location) + str("/") + str(self.filename) + str(".") + str(self.extension)
    # end def __init__
    #// 
    #// Save data to the cache
    #// 
    #// @param array|SimplePie $data Data to store in the cache. If passed a SimplePie object, only cache the $data property
    #// @return bool Successfulness
    #//
    def save(self, data_=None):
        
        
        if php_file_exists(self.name) and is_writeable(self.name) or php_file_exists(self.location) and is_writeable(self.location):
            if type(data_).__name__ == "SimplePie":
                data_ = data_.data
            # end if
            data_ = serialize(data_)
            return php_bool(file_put_contents(self.name, data_))
        # end if
        return False
    # end def save
    #// 
    #// Retrieve the data saved to the cache
    #// 
    #// @return array Data for SimplePie::$data
    #//
    def load(self):
        
        
        if php_file_exists(self.name) and php_is_readable(self.name):
            return unserialize(php_file_get_contents(self.name))
        # end if
        return False
    # end def load
    #// 
    #// Retrieve the last modified time for the cache
    #// 
    #// @return int Timestamp
    #//
    def mtime(self):
        
        
        if php_file_exists(self.name):
            return filemtime(self.name)
        # end if
        return False
    # end def mtime
    #// 
    #// Set the last modified time to the current time
    #// 
    #// @return bool Success status
    #//
    def touch(self):
        
        
        if php_file_exists(self.name):
            return touch(self.name)
        # end if
        return False
    # end def touch
    #// 
    #// Remove the cache
    #// 
    #// @return bool Success status
    #//
    def unlink(self):
        
        
        if php_file_exists(self.name):
            return unlink(self.name)
        # end if
        return False
    # end def unlink
# end class SimplePie_Cache_File
