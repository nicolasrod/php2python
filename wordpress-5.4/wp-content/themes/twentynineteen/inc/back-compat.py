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
#// Twenty Nineteen back compat functionality
#// 
#// Prevents Twenty Nineteen from running on WordPress versions prior to 4.7,
#// since this theme is not meant to be backward compatible beyond that and
#// relies on many newer functions and markup changes introduced in 4.7.
#// 
#// @package WordPress
#// @subpackage Twenty_Nineteen
#// @since Twenty Nineteen 1.0.0
#// 
#// 
#// Prevent switching to Twenty Nineteen on old versions of WordPress.
#// 
#// Switches to the default theme.
#// 
#// @since Twenty Nineteen 1.0.0
#//
def twentynineteen_switch_theme(*args_):
    
    switch_theme(WP_DEFAULT_THEME)
    PHP_REQUEST["activated"] = None
    add_action("admin_notices", "twentynineteen_upgrade_notice")
# end def twentynineteen_switch_theme
add_action("after_switch_theme", "twentynineteen_switch_theme")
#// 
#// Adds a message for unsuccessful theme switch.
#// 
#// Prints an update nag after an unsuccessful attempt to switch to
#// Twenty Nineteen on WordPress versions prior to 4.7.
#// 
#// @since Twenty Nineteen 1.0.0
#// 
#// @global string $wp_version WordPress version.
#//
def twentynineteen_upgrade_notice(*args_):
    
    #// translators: %s: WordPress version.
    message = php_sprintf(__("Twenty Nineteen requires at least WordPress version 4.7. You are running version %s. Please upgrade and try again.", "twentynineteen"), PHP_GLOBALS["wp_version"])
    printf("<div class=\"error\"><p>%s</p></div>", message)
# end def twentynineteen_upgrade_notice
#// 
#// Prevents the Customizer from being loaded on WordPress versions prior to 4.7.
#// 
#// @since Twenty Nineteen 1.0.0
#// 
#// @global string $wp_version WordPress version.
#//
def twentynineteen_customize(*args_):
    
    wp_die(php_sprintf(__("Twenty Nineteen requires at least WordPress version 4.7. You are running version %s. Please upgrade and try again.", "twentynineteen"), PHP_GLOBALS["wp_version"]), "", Array({"back_link": True}))
# end def twentynineteen_customize
add_action("load-customize.php", "twentynineteen_customize")
#// 
#// Prevents the Theme Preview from being loaded on WordPress versions prior to 4.7.
#// 
#// @since Twenty Nineteen 1.0.0
#// 
#// @global string $wp_version WordPress version.
#//
def twentynineteen_preview(*args_):
    
    if (php_isset(lambda : PHP_REQUEST["preview"])):
        #// translators: %s: WordPress version.
        wp_die(php_sprintf(__("Twenty Nineteen requires at least WordPress version 4.7. You are running version %s. Please upgrade and try again.", "twentynineteen"), PHP_GLOBALS["wp_version"]))
    # end if
# end def twentynineteen_preview
add_action("template_redirect", "twentynineteen_preview")
