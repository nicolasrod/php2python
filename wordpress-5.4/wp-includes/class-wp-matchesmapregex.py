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
#// WP_MatchesMapRegex helper class
#// 
#// @package WordPress
#// @since 4.7.0
#// 
#// 
#// Helper class to remove the need to use eval to replace $matches[] in query strings.
#// 
#// @since 2.9.0
#//
class WP_MatchesMapRegex():
    _matches = Array()
    output = Array()
    _subject = Array()
    _pattern = "(\\$matches\\[[1-9]+[0-9]*\\])"
    #// Magic number.
    #// 
    #// constructor
    #// 
    #// @param string $subject subject if regex
    #// @param array  $matches data to use in map
    #//
    def __init__(self, subject=None, matches=None):
        
        self._subject = subject
        self._matches = matches
        self.output = self._map()
    # end def __init__
    #// 
    #// Substitute substring matches in subject.
    #// 
    #// static helper function to ease use
    #// 
    #// @param string $subject subject
    #// @param array  $matches data used for substitution
    #// @return string
    #//
    @classmethod
    def apply(self, subject=None, matches=None):
        
        oSelf = php_new_class("WP_MatchesMapRegex", lambda : WP_MatchesMapRegex(subject, matches))
        return oSelf.output
    # end def apply
    #// 
    #// do the actual mapping
    #// 
    #// @return string
    #//
    def _map(self):
        
        callback = Array(self, "callback")
        return preg_replace_callback(self._pattern, callback, self._subject)
    # end def _map
    #// 
    #// preg_replace_callback hook
    #// 
    #// @param  array $matches preg_replace regexp matches
    #// @return string
    #//
    def callback(self, matches=None):
        
        index = php_intval(php_substr(matches[0], 9, -1))
        return urlencode(self._matches[index]) if (php_isset(lambda : self._matches[index])) else ""
    # end def callback
# end class WP_MatchesMapRegex
