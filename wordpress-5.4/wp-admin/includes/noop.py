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
#// Noop functions for load-scripts.php and load-styles.php.
#// 
#// @package WordPress
#// @subpackage Administration
#// @since 4.4.0
#// 
#// 
#// @ignore
#//
def __(*args_):
    
    pass
# end def __
#// 
#// @ignore
#//
def _x(*args_):
    
    pass
# end def _x
#// 
#// @ignore
#//
def add_filter(*args_):
    
    pass
# end def add_filter
#// 
#// @ignore
#//
def esc_attr(*args_):
    
    pass
# end def esc_attr
#// 
#// @ignore
#//
def apply_filters(*args_):
    
    pass
# end def apply_filters
#// 
#// @ignore
#//
def get_option(*args_):
    
    pass
# end def get_option
#// 
#// @ignore
#//
def is_lighttpd_before_150(*args_):
    
    pass
# end def is_lighttpd_before_150
#// 
#// @ignore
#//
def add_action(*args_):
    
    pass
# end def add_action
#// 
#// @ignore
#//
def did_action(*args_):
    
    pass
# end def did_action
#// 
#// @ignore
#//
def do_action_ref_array(*args_):
    
    pass
# end def do_action_ref_array
#// 
#// @ignore
#//
def get_bloginfo(*args_):
    
    pass
# end def get_bloginfo
#// 
#// @ignore
#//
def is_admin(*args_):
    
    return True
# end def is_admin
#// 
#// @ignore
#//
def site_url(*args_):
    
    pass
# end def site_url
#// 
#// @ignore
#//
def admin_url(*args_):
    
    pass
# end def admin_url
#// 
#// @ignore
#//
def home_url(*args_):
    
    pass
# end def home_url
#// 
#// @ignore
#//
def includes_url(*args_):
    
    pass
# end def includes_url
#// 
#// @ignore
#//
def wp_guess_url(*args_):
    
    pass
# end def wp_guess_url
def get_file(path=None, *args_):
    
    path = php_realpath(path)
    if (not path) or (not php_no_error(lambda: php_is_file(path))):
        return ""
    # end if
    return php_no_error(lambda: php_file_get_contents(path))
# end def get_file
