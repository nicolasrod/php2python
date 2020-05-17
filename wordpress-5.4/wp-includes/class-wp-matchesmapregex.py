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
    #// 
    #// store for matches
    #// 
    #// @var array
    #//
    _matches = Array()
    #// 
    #// store for mapping result
    #// 
    #// @var string
    #//
    output = Array()
    #// 
    #// subject to perform mapping on (query string containing $matches[] references
    #// 
    #// @var string
    #//
    _subject = Array()
    #// 
    #// regexp pattern to match $matches[] references
    #// 
    #// @var string
    #//
    _pattern = "(\\$matches\\[[1-9]+[0-9]*\\])"
    #// Magic number.
    #// 
    #// constructor
    #// 
    #// @param string $subject subject if regex
    #// @param array  $matches data to use in map
    #//
    def __init__(self, subject_=None, matches_=None):
        
        
        self._subject = subject_
        self._matches = matches_
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
    def apply(self, subject_=None, matches_=None):
        
        
        oSelf_ = php_new_class("WP_MatchesMapRegex", lambda : WP_MatchesMapRegex(subject_, matches_))
        return oSelf_.output
    # end def apply
    #// 
    #// do the actual mapping
    #// 
    #// @return string
    #//
    def _map(self):
        
        
        callback_ = Array(self, "callback")
        return preg_replace_callback(self._pattern, callback_, self._subject)
    # end def _map
    #// 
    #// preg_replace_callback hook
    #// 
    #// @param  array $matches preg_replace regexp matches
    #// @return string
    #//
    def callback(self, matches_=None):
        
        
        index_ = php_intval(php_substr(matches_[0], 9, -1))
        return urlencode(self._matches[index_]) if (php_isset(lambda : self._matches[index_])) else ""
    # end def callback
# end class WP_MatchesMapRegex
