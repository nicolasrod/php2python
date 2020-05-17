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
#// Noop functions for load-scripts.php and load-styles.php.
#// 
#// @package WordPress
#// @subpackage Administration
#// @since 4.4.0
#// 
#// 
#// @ignore
#//
def __(*_args_):
    
    
    pass
# end def __
#// 
#// @ignore
#//
def _x(*_args_):
    
    
    pass
# end def _x
#// 
#// @ignore
#//
def add_filter(*_args_):
    
    
    pass
# end def add_filter
#// 
#// @ignore
#//
def esc_attr(*_args_):
    
    
    pass
# end def esc_attr
#// 
#// @ignore
#//
def apply_filters(*_args_):
    
    
    pass
# end def apply_filters
#// 
#// @ignore
#//
def get_option(*_args_):
    
    
    pass
# end def get_option
#// 
#// @ignore
#//
def is_lighttpd_before_150(*_args_):
    
    
    pass
# end def is_lighttpd_before_150
#// 
#// @ignore
#//
def add_action(*_args_):
    
    
    pass
# end def add_action
#// 
#// @ignore
#//
def did_action(*_args_):
    
    
    pass
# end def did_action
#// 
#// @ignore
#//
def do_action_ref_array(*_args_):
    
    
    pass
# end def do_action_ref_array
#// 
#// @ignore
#//
def get_bloginfo(*_args_):
    
    
    pass
# end def get_bloginfo
#// 
#// @ignore
#//
def is_admin(*_args_):
    
    
    return True
# end def is_admin
#// 
#// @ignore
#//
def site_url(*_args_):
    
    
    pass
# end def site_url
#// 
#// @ignore
#//
def admin_url(*_args_):
    
    
    pass
# end def admin_url
#// 
#// @ignore
#//
def home_url(*_args_):
    
    
    pass
# end def home_url
#// 
#// @ignore
#//
def includes_url(*_args_):
    
    
    pass
# end def includes_url
#// 
#// @ignore
#//
def wp_guess_url(*_args_):
    
    
    pass
# end def wp_guess_url
def get_file(path_=None, *_args_):
    
    
    path_ = php_realpath(path_)
    if (not path_) or (not php_no_error(lambda: php_is_file(path_))):
        return ""
    # end if
    return php_no_error(lambda: php_file_get_contents(path_))
# end def get_file
