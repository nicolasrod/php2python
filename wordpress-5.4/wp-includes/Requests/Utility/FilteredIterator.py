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
#// Iterator for arrays requiring filtered values
#// 
#// @package Requests
#// @subpackage Utilities
#// 
#// 
#// Iterator for arrays requiring filtered values
#// 
#// @package Requests
#// @subpackage Utilities
#//
class Requests_Utility_FilteredIterator(ArrayIterator):
    #// 
    #// Callback to run as a filter
    #// 
    #// @var callable
    #//
    callback = Array()
    #// 
    #// Create a new iterator
    #// 
    #// @param array $data
    #// @param callable $callback Callback to be called on each value
    #//
    def __init__(self, data_=None, callback_=None):
        
        
        super().__init__(data_)
        self.callback = callback_
    # end def __init__
    #// 
    #// Get the current item's value after filtering
    #// 
    #// @return string
    #//
    def current(self):
        
        
        value_ = super().current()
        value_ = php_call_user_func(self.callback, value_)
        return value_
    # end def current
# end class Requests_Utility_FilteredIterator
