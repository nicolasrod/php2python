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
#// Multisite: Deprecated admin functions from past versions and WordPress MU
#// 
#// These functions should not be used and will be removed in a later version.
#// It is suggested to use for the alternatives instead when available.
#// 
#// @package WordPress
#// @subpackage Deprecated
#// @since 3.0.0
#// 
#// 
#// Outputs the WPMU menu.
#// 
#// @deprecated 3.0.0
#//
def wpmu_menu(*args_):
    
    _deprecated_function(__FUNCTION__, "3.0.0")
    pass
# end def wpmu_menu
#// 
#// Determines if the available space defined by the admin has been exceeded by the user.
#// 
#// @deprecated 3.0.0 Use is_upload_space_available()
#// @see is_upload_space_available()
#//
def wpmu_checkAvailableSpace(*args_):
    
    _deprecated_function(__FUNCTION__, "3.0.0", "is_upload_space_available()")
    if (not is_upload_space_available()):
        wp_die(php_sprintf(__("Sorry, you have used your space allocation of %s. Please delete some files to upload more files."), size_format(get_space_allowed() * MB_IN_BYTES)))
    # end if
# end def wpmu_checkAvailableSpace
#// 
#// WPMU options.
#// 
#// @deprecated 3.0.0
#//
def mu_options(options=None, *args_):
    
    _deprecated_function(__FUNCTION__, "3.0.0")
    return options
# end def mu_options
#// 
#// Deprecated functionality for activating a network-only plugin.
#// 
#// @deprecated 3.0.0 Use activate_plugin()
#// @see activate_plugin()
#//
def activate_sitewide_plugin(*args_):
    
    _deprecated_function(__FUNCTION__, "3.0.0", "activate_plugin()")
    return False
# end def activate_sitewide_plugin
#// 
#// Deprecated functionality for deactivating a network-only plugin.
#// 
#// @deprecated 3.0.0 Use deactivate_plugin()
#// @see deactivate_plugin()
#//
def deactivate_sitewide_plugin(plugin=False, *args_):
    
    _deprecated_function(__FUNCTION__, "3.0.0", "deactivate_plugin()")
# end def deactivate_sitewide_plugin
#// 
#// Deprecated functionality for determining if the current plugin is network-only.
#// 
#// @deprecated 3.0.0 Use is_network_only_plugin()
#// @see is_network_only_plugin()
#//
def is_wpmu_sitewide_plugin(file=None, *args_):
    
    _deprecated_function(__FUNCTION__, "3.0.0", "is_network_only_plugin()")
    return is_network_only_plugin(file)
# end def is_wpmu_sitewide_plugin
#// 
#// Deprecated functionality for getting themes network-enabled themes.
#// 
#// @deprecated 3.4.0 Use WP_Theme::get_allowed_on_network()
#// @see WP_Theme::get_allowed_on_network()
#//
def get_site_allowed_themes(*args_):
    
    _deprecated_function(__FUNCTION__, "3.4.0", "WP_Theme::get_allowed_on_network()")
    return php_array_map("intval", WP_Theme.get_allowed_on_network())
# end def get_site_allowed_themes
#// 
#// Deprecated functionality for getting themes allowed on a specific site.
#// 
#// @deprecated 3.4.0 Use WP_Theme::get_allowed_on_site()
#// @see WP_Theme::get_allowed_on_site()
#//
def wpmu_get_blog_allowedthemes(blog_id=0, *args_):
    
    _deprecated_function(__FUNCTION__, "3.4.0", "WP_Theme::get_allowed_on_site()")
    return php_array_map("intval", WP_Theme.get_allowed_on_site(blog_id))
# end def wpmu_get_blog_allowedthemes
#// 
#// Deprecated functionality for determining whether a file is deprecated.
#// 
#// @deprecated 3.5.0
#//
def ms_deprecated_blogs_file(*args_):
    
    pass
# end def ms_deprecated_blogs_file
