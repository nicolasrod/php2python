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
#// Base class for database-based caches
#// 
#// @package SimplePie
#// @subpackage Caching
#//
class SimplePie_Cache_DB(SimplePie_Cache_Base):
    #// 
    #// Helper for database conversion
    #// 
    #// Converts a given {@see SimplePie} object into data to be stored
    #// 
    #// @param SimplePie $data
    #// @return array First item is the serialized data for storage, second item is the unique ID for this item
    #//
    def prepare_simplepie_object_for_cache(self, data=None):
        
        items = data.get_items()
        items_by_id = Array()
        if (not php_empty(lambda : items)):
            for item in items:
                items_by_id[item.get_id()] = item
            # end for
            if php_count(items_by_id) != php_count(items):
                items_by_id = Array()
                for item in items:
                    items_by_id[item.get_id(True)] = item
                # end for
            # end if
            if (php_isset(lambda : data.data["child"][SIMPLEPIE_NAMESPACE_ATOM_10]["feed"][0])):
                channel = data.data["child"][SIMPLEPIE_NAMESPACE_ATOM_10]["feed"][0]
            elif (php_isset(lambda : data.data["child"][SIMPLEPIE_NAMESPACE_ATOM_03]["feed"][0])):
                channel = data.data["child"][SIMPLEPIE_NAMESPACE_ATOM_03]["feed"][0]
            elif (php_isset(lambda : data.data["child"][SIMPLEPIE_NAMESPACE_RDF]["RDF"][0])):
                channel = data.data["child"][SIMPLEPIE_NAMESPACE_RDF]["RDF"][0]
            elif (php_isset(lambda : data.data["child"][SIMPLEPIE_NAMESPACE_RSS_20]["rss"][0]["child"][SIMPLEPIE_NAMESPACE_RSS_20]["channel"][0])):
                channel = data.data["child"][SIMPLEPIE_NAMESPACE_RSS_20]["rss"][0]["child"][SIMPLEPIE_NAMESPACE_RSS_20]["channel"][0]
            else:
                channel = None
            # end if
            if channel != None:
                if (php_isset(lambda : channel["child"][SIMPLEPIE_NAMESPACE_ATOM_10]["entry"])):
                    channel["child"][SIMPLEPIE_NAMESPACE_ATOM_10]["entry"] = None
                # end if
                if (php_isset(lambda : channel["child"][SIMPLEPIE_NAMESPACE_ATOM_03]["entry"])):
                    channel["child"][SIMPLEPIE_NAMESPACE_ATOM_03]["entry"] = None
                # end if
                if (php_isset(lambda : channel["child"][SIMPLEPIE_NAMESPACE_RSS_10]["item"])):
                    channel["child"][SIMPLEPIE_NAMESPACE_RSS_10]["item"] = None
                # end if
                if (php_isset(lambda : channel["child"][SIMPLEPIE_NAMESPACE_RSS_090]["item"])):
                    channel["child"][SIMPLEPIE_NAMESPACE_RSS_090]["item"] = None
                # end if
                if (php_isset(lambda : channel["child"][SIMPLEPIE_NAMESPACE_RSS_20]["item"])):
                    channel["child"][SIMPLEPIE_NAMESPACE_RSS_20]["item"] = None
                # end if
            # end if
            if (php_isset(lambda : data.data["items"])):
                data.data["items"] = None
            # end if
            if (php_isset(lambda : data.data["ordered_items"])):
                data.data["ordered_items"] = None
            # end if
        # end if
        return Array(serialize(data.data), items_by_id)
    # end def prepare_simplepie_object_for_cache
# end class SimplePie_Cache_DB