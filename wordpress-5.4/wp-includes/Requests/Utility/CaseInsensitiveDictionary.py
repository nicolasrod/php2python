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
#// Case-insensitive dictionary, suitable for HTTP headers
#// 
#// @package Requests
#// @subpackage Utilities
#// 
#// 
#// Case-insensitive dictionary, suitable for HTTP headers
#// 
#// @package Requests
#// @subpackage Utilities
#//
class Requests_Utility_CaseInsensitiveDictionary(ArrayAccessIteratorAggregate):
    #// 
    #// Actual item data
    #// 
    #// @var array
    #//
    data = Array()
    #// 
    #// Creates a case insensitive dictionary.
    #// 
    #// @param array $data Dictionary/map to convert to case-insensitive
    #//
    def __init__(self, data_=None):
        if data_ is None:
            data_ = Array()
        # end if
        
        for key_,value_ in data_:
            self.offsetset(key_, value_)
        # end for
    # end def __init__
    #// 
    #// Check if the given item exists
    #// 
    #// @param string $key Item key
    #// @return boolean Does the item exist?
    #//
    def offsetexists(self, key_=None):
        
        
        key_ = php_strtolower(key_)
        return (php_isset(lambda : self.data[key_]))
    # end def offsetexists
    #// 
    #// Get the value for the item
    #// 
    #// @param string $key Item key
    #// @return string Item value
    #//
    def offsetget(self, key_=None):
        
        
        key_ = php_strtolower(key_)
        if (not (php_isset(lambda : self.data[key_]))):
            return None
        # end if
        return self.data[key_]
    # end def offsetget
    #// 
    #// Set the given item
    #// 
    #// @throws Requests_Exception On attempting to use dictionary as list (`invalidset`)
    #// 
    #// @param string $key Item name
    #// @param string $value Item value
    #//
    def offsetset(self, key_=None, value_=None):
        
        
        if key_ == None:
            raise php_new_class("Requests_Exception", lambda : Requests_Exception("Object is a dictionary, not a list", "invalidset"))
        # end if
        key_ = php_strtolower(key_)
        self.data[key_] = value_
    # end def offsetset
    #// 
    #// Unset the given header
    #// 
    #// @param string $key
    #//
    def offsetunset(self, key_=None):
        
        
        self.data[php_strtolower(key_)] = None
    # end def offsetunset
    #// 
    #// Get an iterator for the data
    #// 
    #// @return ArrayIterator
    #//
    def getiterator(self):
        
        
        return php_new_class("ArrayIterator", lambda : ArrayIterator(self.data))
    # end def getiterator
    #// 
    #// Get the headers as an array
    #// 
    #// @return array Header data
    #//
    def getall(self):
        
        
        return self.data
    # end def getall
# end class Requests_Utility_CaseInsensitiveDictionary
