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
#// Dependencies API: Styles functions
#// 
#// @since 2.6.0
#// 
#// @package WordPress
#// @subpackage Dependencies
#// 
#// 
#// Initialize $wp_styles if it has not been set.
#// 
#// @global WP_Styles $wp_styles
#// 
#// @since 4.2.0
#// 
#// @return WP_Styles WP_Styles instance.
#//
def wp_styles(*args_):
    
    global wp_styles
    php_check_if_defined("wp_styles")
    if (not type(wp_styles).__name__ == "WP_Styles"):
        wp_styles = php_new_class("WP_Styles", lambda : WP_Styles())
    # end if
    return wp_styles
# end def wp_styles
#// 
#// Display styles that are in the $handles queue.
#// 
#// Passing an empty array to $handles prints the queue,
#// passing an array with one string prints that style,
#// and passing an array of strings prints those styles.
#// 
#// @global WP_Styles $wp_styles The WP_Styles object for printing styles.
#// 
#// @since 2.6.0
#// 
#// @param string|bool|array $handles Styles to be printed. Default 'false'.
#// @return string[] On success, an array of handles of processed WP_Dependencies items; otherwise, an empty array.
#//
def wp_print_styles(handles=False, *args_):
    
    if "" == handles:
        #// For 'wp_head'.
        handles = False
    # end if
    if (not handles):
        #// 
        #// Fires before styles in the $handles queue are printed.
        #// 
        #// @since 2.6.0
        #//
        do_action("wp_print_styles")
    # end if
    _wp_scripts_maybe_doing_it_wrong(__FUNCTION__)
    global wp_styles
    php_check_if_defined("wp_styles")
    if (not type(wp_styles).__name__ == "WP_Styles"):
        if (not handles):
            return Array()
            pass
        # end if
    # end if
    return wp_styles().do_items(handles)
# end def wp_print_styles
#// 
#// Add extra CSS styles to a registered stylesheet.
#// 
#// Styles will only be added if the stylesheet is already in the queue.
#// Accepts a string $data containing the CSS. If two or more CSS code blocks
#// are added to the same stylesheet $handle, they will be printed in the order
#// they were added, i.e. the latter added styles can redeclare the previous.
#// 
#// @see WP_Styles::add_inline_style()
#// 
#// @since 3.3.0
#// 
#// @param string $handle Name of the stylesheet to add the extra styles to.
#// @param string $data   String containing the CSS styles to be added.
#// @return bool True on success, false on failure.
#//
def wp_add_inline_style(handle=None, data=None, *args_):
    
    _wp_scripts_maybe_doing_it_wrong(__FUNCTION__)
    if False != php_stripos(data, "</style>"):
        _doing_it_wrong(__FUNCTION__, php_sprintf(__("Do not pass %1$s tags to %2$s."), "<code>&lt;style&gt;</code>", "<code>wp_add_inline_style()</code>"), "3.7.0")
        data = php_trim(php_preg_replace("#<style[^>]*>(.*)</style>#is", "$1", data))
    # end if
    return wp_styles().add_inline_style(handle, data)
# end def wp_add_inline_style
#// 
#// Register a CSS stylesheet.
#// 
#// @see WP_Dependencies::add()
#// @link https://www.w3.org/TR/CSS2/media.html#media-types List of CSS media types.
#// 
#// @since 2.6.0
#// @since 4.3.0 A return value was added.
#// 
#// @param string           $handle Name of the stylesheet. Should be unique.
#// @param string|bool      $src    Full URL of the stylesheet, or path of the stylesheet relative to the WordPress root directory.
#// If source is set to false, stylesheet is an alias of other stylesheets it depends on.
#// @param string[]         $deps   Optional. An array of registered stylesheet handles this stylesheet depends on. Default empty array.
#// @param string|bool|null $ver    Optional. String specifying stylesheet version number, if it has one, which is added to the URL
#// as a query string for cache busting purposes. If version is set to false, a version
#// number is automatically added equal to current installed WordPress version.
#// If set to null, no version is added.
#// @param string           $media  Optional. The media for which this stylesheet has been defined.
#// Default 'all'. Accepts media types like 'all', 'print' and 'screen', or media queries like
#// '(orientation: portrait)' and '(max-width: 640px)'.
#// @return bool Whether the style has been registered. True on success, false on failure.
#//
def wp_register_style(handle=None, src=None, deps=Array(), ver=False, media="all", *args_):
    
    _wp_scripts_maybe_doing_it_wrong(__FUNCTION__)
    return wp_styles().add(handle, src, deps, ver, media)
# end def wp_register_style
#// 
#// Remove a registered stylesheet.
#// 
#// @see WP_Dependencies::remove()
#// 
#// @since 2.1.0
#// 
#// @param string $handle Name of the stylesheet to be removed.
#//
def wp_deregister_style(handle=None, *args_):
    
    _wp_scripts_maybe_doing_it_wrong(__FUNCTION__)
    wp_styles().remove(handle)
# end def wp_deregister_style
#// 
#// Enqueue a CSS stylesheet.
#// 
#// Registers the style if source provided (does NOT overwrite) and enqueues.
#// 
#// @see WP_Dependencies::add()
#// @see WP_Dependencies::enqueue()
#// @link https://www.w3.org/TR/CSS2/media.html#media-types List of CSS media types.
#// 
#// @since 2.6.0
#// 
#// @param string           $handle Name of the stylesheet. Should be unique.
#// @param string           $src    Full URL of the stylesheet, or path of the stylesheet relative to the WordPress root directory.
#// Default empty.
#// @param string[]         $deps   Optional. An array of registered stylesheet handles this stylesheet depends on. Default empty array.
#// @param string|bool|null $ver    Optional. String specifying stylesheet version number, if it has one, which is added to the URL
#// as a query string for cache busting purposes. If version is set to false, a version
#// number is automatically added equal to current installed WordPress version.
#// If set to null, no version is added.
#// @param string           $media  Optional. The media for which this stylesheet has been defined.
#// Default 'all'. Accepts media types like 'all', 'print' and 'screen', or media queries like
#// '(orientation: portrait)' and '(max-width: 640px)'.
#//
def wp_enqueue_style(handle=None, src="", deps=Array(), ver=False, media="all", *args_):
    
    _wp_scripts_maybe_doing_it_wrong(__FUNCTION__)
    wp_styles = wp_styles()
    if src:
        _handle = php_explode("?", handle)
        wp_styles.add(_handle[0], src, deps, ver, media)
    # end if
    wp_styles.enqueue(handle)
# end def wp_enqueue_style
#// 
#// Remove a previously enqueued CSS stylesheet.
#// 
#// @see WP_Dependencies::dequeue()
#// 
#// @since 3.1.0
#// 
#// @param string $handle Name of the stylesheet to be removed.
#//
def wp_dequeue_style(handle=None, *args_):
    
    _wp_scripts_maybe_doing_it_wrong(__FUNCTION__)
    wp_styles().dequeue(handle)
# end def wp_dequeue_style
#// 
#// Check whether a CSS stylesheet has been added to the queue.
#// 
#// @since 2.8.0
#// 
#// @param string $handle Name of the stylesheet.
#// @param string $list   Optional. Status of the stylesheet to check. Default 'enqueued'.
#// Accepts 'enqueued', 'registered', 'queue', 'to_do', and 'done'.
#// @return bool Whether style is queued.
#//
def wp_style_is(handle=None, list="enqueued", *args_):
    
    _wp_scripts_maybe_doing_it_wrong(__FUNCTION__)
    return php_bool(wp_styles().query(handle, list))
# end def wp_style_is
#// 
#// Add metadata to a CSS stylesheet.
#// 
#// Works only if the stylesheet has already been added.
#// 
#// Possible values for $key and $value:
#// 'conditional' string      Comments for IE 6, lte IE 7 etc.
#// 'rtl'         bool|string To declare an RTL stylesheet.
#// 'suffix'      string      Optional suffix, used in combination with RTL.
#// 'alt'         bool        For rel="alternate stylesheet".
#// 'title'       string      For preferred/alternate stylesheets.
#// 
#// @see WP_Dependencies::add_data()
#// 
#// @since 3.6.0
#// 
#// @param string $handle Name of the stylesheet.
#// @param string $key    Name of data point for which we're storing a value.
#// Accepts 'conditional', 'rtl' and 'suffix', 'alt' and 'title'.
#// @param mixed  $value  String containing the CSS data to be added.
#// @return bool True on success, false on failure.
#//
def wp_style_add_data(handle=None, key=None, value=None, *args_):
    
    return wp_styles().add_data(handle, key, value)
# end def wp_style_add_data
