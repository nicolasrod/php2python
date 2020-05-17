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
#// Feed API: WP_Feed_Cache class
#// 
#// @package WordPress
#// @subpackage Feed
#// @since 4.7.0
#// 
#// 
#// Core class used to implement a feed cache.
#// 
#// @since 2.8.0
#// 
#// @see SimplePie_Cache
#//
class WP_Feed_Cache(SimplePie_Cache):
    #// 
    #// Creates a new SimplePie_Cache object.
    #// 
    #// @since 2.8.0
    #// 
    #// @param string $location  URL location (scheme is used to determine handler).
    #// @param string $filename  Unique identifier for cache object.
    #// @param string $extension 'spi' or 'spc'.
    #// @return WP_Feed_Cache_Transient Feed cache handler object that uses transients.
    #//
    def create(self, location_=None, filename_=None, extension_=None):
        
        
        return php_new_class("WP_Feed_Cache_Transient", lambda : WP_Feed_Cache_Transient(location_, filename_, extension_))
    # end def create
# end class WP_Feed_Cache
