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
#// Twenty Seventeen back compat functionality
#// 
#// Prevents Twenty Seventeen from running on WordPress versions prior to 4.7,
#// since this theme is not meant to be backward compatible beyond that and
#// relies on many newer functions and markup changes introduced in 4.7.
#// 
#// @package WordPress
#// @subpackage Twenty_Seventeen
#// @since Twenty Seventeen 1.0
#// 
#// 
#// Prevent switching to Twenty Seventeen on old versions of WordPress.
#// 
#// Switches to the default theme.
#// 
#// @since Twenty Seventeen 1.0
#//
def twentyseventeen_switch_theme(*_args_):
    
    
    switch_theme(WP_DEFAULT_THEME)
    PHP_REQUEST["activated"] = None
    add_action("admin_notices", "twentyseventeen_upgrade_notice")
# end def twentyseventeen_switch_theme
add_action("after_switch_theme", "twentyseventeen_switch_theme")
#// 
#// Adds a message for unsuccessful theme switch.
#// 
#// Prints an update nag after an unsuccessful attempt to switch to
#// Twenty Seventeen on WordPress versions prior to 4.7.
#// 
#// @since Twenty Seventeen 1.0
#// 
#// @global string $wp_version WordPress version.
#//
def twentyseventeen_upgrade_notice(*_args_):
    
    
    #// translators: %s: The current WordPress version.
    message_ = php_sprintf(__("Twenty Seventeen requires at least WordPress version 4.7. You are running version %s. Please upgrade and try again.", "twentyseventeen"), PHP_GLOBALS["wp_version"])
    php_printf("<div class=\"error\"><p>%s</p></div>", message_)
# end def twentyseventeen_upgrade_notice
#// 
#// Prevents the Customizer from being loaded on WordPress versions prior to 4.7.
#// 
#// @since Twenty Seventeen 1.0
#// 
#// @global string $wp_version WordPress version.
#//
def twentyseventeen_customize(*_args_):
    
    
    wp_die(php_sprintf(__("Twenty Seventeen requires at least WordPress version 4.7. You are running version %s. Please upgrade and try again.", "twentyseventeen"), PHP_GLOBALS["wp_version"]), "", Array({"back_link": True}))
# end def twentyseventeen_customize
add_action("load-customize.php", "twentyseventeen_customize")
#// 
#// Prevents the Theme Preview from being loaded on WordPress versions prior to 4.7.
#// 
#// @since Twenty Seventeen 1.0
#// 
#// @global string $wp_version WordPress version.
#//
def twentyseventeen_preview(*_args_):
    
    
    if (php_isset(lambda : PHP_REQUEST["preview"])):
        #// translators: %s: The current WordPress version.
        wp_die(php_sprintf(__("Twenty Seventeen requires at least WordPress version 4.7. You are running version %s. Please upgrade and try again.", "twentyseventeen"), PHP_GLOBALS["wp_version"]))
    # end if
# end def twentyseventeen_preview
add_action("template_redirect", "twentyseventeen_preview")
