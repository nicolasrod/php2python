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
#// WordPress Administration Screen API.
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// 
#// Get the column headers for a screen
#// 
#// @since 2.7.0
#// 
#// @staticvar array $column_headers
#// 
#// @param string|WP_Screen $screen The screen you want the headers for
#// @return string[] The column header labels keyed by column ID.
#//
def get_column_headers(screen=None, *args_):
    
    if php_is_string(screen):
        screen = convert_to_screen(screen)
    # end if
    get_column_headers.column_headers = Array()
    if (not (php_isset(lambda : get_column_headers.column_headers[screen.id]))):
        #// 
        #// Filters the column headers for a list table on a specific screen.
        #// 
        #// The dynamic portion of the hook name, `$screen->id`, refers to the
        #// ID of a specific screen. For example, the screen ID for the Posts
        #// list table is edit-post, so the filter for that screen would be
        #// manage_edit-post_columns.
        #// 
        #// @since 3.0.0
        #// 
        #// @param string[] $columns The column header labels keyed by column ID.
        #//
        get_column_headers.column_headers[screen.id] = apply_filters(str("manage_") + str(screen.id) + str("_columns"), Array())
    # end if
    return get_column_headers.column_headers[screen.id]
# end def get_column_headers
#// 
#// Get a list of hidden columns.
#// 
#// @since 2.7.0
#// 
#// @param string|WP_Screen $screen The screen you want the hidden columns for
#// @return string[] Array of IDs of hidden columns.
#//
def get_hidden_columns(screen=None, *args_):
    
    if php_is_string(screen):
        screen = convert_to_screen(screen)
    # end if
    hidden = get_user_option("manage" + screen.id + "columnshidden")
    use_defaults = (not php_is_array(hidden))
    if use_defaults:
        hidden = Array()
        #// 
        #// Filters the default list of hidden columns.
        #// 
        #// @since 4.4.0
        #// 
        #// @param string[]  $hidden Array of IDs of columns hidden by default.
        #// @param WP_Screen $screen WP_Screen object of the current screen.
        #//
        hidden = apply_filters("default_hidden_columns", hidden, screen)
    # end if
    #// 
    #// Filters the list of hidden columns.
    #// 
    #// @since 4.4.0
    #// @since 4.4.1 Added the `use_defaults` parameter.
    #// 
    #// @param string[]  $hidden       Array of IDs of hidden columns.
    #// @param WP_Screen $screen       WP_Screen object of the current screen.
    #// @param bool      $use_defaults Whether to show the default columns.
    #//
    return apply_filters("hidden_columns", hidden, screen, use_defaults)
# end def get_hidden_columns
#// 
#// Prints the meta box preferences for screen meta.
#// 
#// @since 2.7.0
#// 
#// @global array $wp_meta_boxes
#// 
#// @param WP_Screen $screen
#//
def meta_box_prefs(screen=None, *args_):
    
    global wp_meta_boxes
    php_check_if_defined("wp_meta_boxes")
    if php_is_string(screen):
        screen = convert_to_screen(screen)
    # end if
    if php_empty(lambda : wp_meta_boxes[screen.id]):
        return
    # end if
    hidden = get_hidden_meta_boxes(screen)
    for context in php_array_keys(wp_meta_boxes[screen.id]):
        for priority in Array("high", "core", "default", "low"):
            if (not (php_isset(lambda : wp_meta_boxes[screen.id][context][priority]))):
                continue
            # end if
            for box in wp_meta_boxes[screen.id][context][priority]:
                if False == box or (not box["title"]):
                    continue
                # end if
                #// Submit box cannot be hidden.
                if "submitdiv" == box["id"] or "linksubmitdiv" == box["id"]:
                    continue
                # end if
                widget_title = box["title"]
                if php_is_array(box["args"]) and (php_isset(lambda : box["args"]["__widget_basename"])):
                    widget_title = box["args"]["__widget_basename"]
                # end if
                printf("<label for=\"%1$s-hide\"><input class=\"hide-postbox-tog\" name=\"%1$s-hide\" type=\"checkbox\" id=\"%1$s-hide\" value=\"%1$s\" %2$s />%3$s</label>", esc_attr(box["id"]), checked(php_in_array(box["id"], hidden), False, False), widget_title)
            # end for
        # end for
    # end for
# end def meta_box_prefs
#// 
#// Gets an array of IDs of hidden meta boxes.
#// 
#// @since 2.7.0
#// 
#// @param string|WP_Screen $screen Screen identifier
#// @return string[] IDs of hidden meta boxes.
#//
def get_hidden_meta_boxes(screen=None, *args_):
    
    if php_is_string(screen):
        screen = convert_to_screen(screen)
    # end if
    hidden = get_user_option(str("metaboxhidden_") + str(screen.id))
    use_defaults = (not php_is_array(hidden))
    #// Hide slug boxes by default.
    if use_defaults:
        hidden = Array()
        if "post" == screen.base:
            if "post" == screen.post_type or "page" == screen.post_type or "attachment" == screen.post_type:
                hidden = Array("slugdiv", "trackbacksdiv", "postcustom", "postexcerpt", "commentstatusdiv", "commentsdiv", "authordiv", "revisionsdiv")
            else:
                hidden = Array("slugdiv")
            # end if
        # end if
        #// 
        #// Filters the default list of hidden meta boxes.
        #// 
        #// @since 3.1.0
        #// 
        #// @param string[]  $hidden An array of IDs of meta boxes hidden by default.
        #// @param WP_Screen $screen WP_Screen object of the current screen.
        #//
        hidden = apply_filters("default_hidden_meta_boxes", hidden, screen)
    # end if
    #// 
    #// Filters the list of hidden meta boxes.
    #// 
    #// @since 3.3.0
    #// 
    #// @param string[]  $hidden       An array of IDs of hidden meta boxes.
    #// @param WP_Screen $screen       WP_Screen object of the current screen.
    #// @param bool      $use_defaults Whether to show the default meta boxes.
    #// Default true.
    #//
    return apply_filters("hidden_meta_boxes", hidden, screen, use_defaults)
# end def get_hidden_meta_boxes
#// 
#// Register and configure an admin screen option
#// 
#// @since 3.1.0
#// 
#// @param string $option An option name.
#// @param mixed $args Option-dependent arguments.
#//
def add_screen_option(option=None, args=Array(), *args_):
    
    current_screen = get_current_screen()
    if (not current_screen):
        return
    # end if
    current_screen.add_option(option, args)
# end def add_screen_option
#// 
#// Get the current screen object
#// 
#// @since 3.1.0
#// 
#// @global WP_Screen $current_screen WordPress current screen object.
#// 
#// @return WP_Screen|null Current screen object or null when screen not defined.
#//
def get_current_screen(*args_):
    
    global current_screen
    php_check_if_defined("current_screen")
    if (not (php_isset(lambda : current_screen))):
        return None
    # end if
    return current_screen
# end def get_current_screen
#// 
#// Set the current screen object
#// 
#// @since 3.0.0
#// 
#// @param string|WP_Screen $hook_name Optional. The hook name (also known as the hook suffix) used to determine the screen,
#// or an existing screen object.
#//
def set_current_screen(hook_name="", *args_):
    
    WP_Screen.get(hook_name).set_current_screen()
# end def set_current_screen
