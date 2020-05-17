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
#// Core Widgets API
#// 
#// This API is used for creating dynamic sidebar without hardcoding functionality into
#// themes
#// 
#// Includes both internal WordPress routines and theme-use routines.
#// 
#// This functionality was found in a plugin before the WordPress 2.2 release, which
#// included it in the core from that point on.
#// 
#// @link https://wordpress.org/support/article/wordpress-widgets
#// @link https://developer.wordpress.org/themes/functionality/widgets
#// 
#// @package WordPress
#// @subpackage Widgets
#// @since 2.2.0
#// 
#// 
#// Global Variables.
#// 
#// @ignore
global wp_registered_sidebars_
global wp_registered_widgets_
global wp_registered_widget_controls_
global wp_registered_widget_updates_
php_check_if_defined("wp_registered_sidebars_","wp_registered_widgets_","wp_registered_widget_controls_","wp_registered_widget_updates_")
#// 
#// Stores the sidebars, since many themes can have more than one.
#// 
#// @global array $wp_registered_sidebars Registered sidebars.
#// @since 2.2.0
#//
wp_registered_sidebars_ = Array()
#// 
#// Stores the registered widgets.
#// 
#// @global array $wp_registered_widgets
#// @since 2.2.0
#//
wp_registered_widgets_ = Array()
#// 
#// Stores the registered widget control (options).
#// 
#// @global array $wp_registered_widget_controls
#// @since 2.2.0
#//
wp_registered_widget_controls_ = Array()
#// 
#// @global array $wp_registered_widget_updates
#//
wp_registered_widget_updates_ = Array()
#// 
#// Private
#// 
#// @global array $_wp_sidebars_widgets
#//
_wp_sidebars_widgets_ = Array()
#// 
#// Private
#// 
#// @global array $_wp_deprecated_widgets_callbacks
#//
PHP_GLOBALS["_wp_deprecated_widgets_callbacks"] = Array("wp_widget_pages", "wp_widget_pages_control", "wp_widget_calendar", "wp_widget_calendar_control", "wp_widget_archives", "wp_widget_archives_control", "wp_widget_links", "wp_widget_meta", "wp_widget_meta_control", "wp_widget_search", "wp_widget_recent_entries", "wp_widget_recent_entries_control", "wp_widget_tag_cloud", "wp_widget_tag_cloud_control", "wp_widget_categories", "wp_widget_categories_control", "wp_widget_text", "wp_widget_text_control", "wp_widget_rss", "wp_widget_rss_control", "wp_widget_recent_comments", "wp_widget_recent_comments_control")
#// 
#// Template tags & API functions.
#// 
#// 
#// Register a widget
#// 
#// Registers a WP_Widget widget
#// 
#// @since 2.8.0
#// @since 4.6.0 Updated the `$widget` parameter to also accept a WP_Widget instance object
#// instead of simply a `WP_Widget` subclass name.
#// 
#// @see WP_Widget
#// 
#// @global WP_Widget_Factory $wp_widget_factory
#// 
#// @param string|WP_Widget $widget Either the name of a `WP_Widget` subclass or an instance of a `WP_Widget` subclass.
#//
def register_widget(widget_=None, *_args_):
    
    
    global wp_widget_factory_
    php_check_if_defined("wp_widget_factory_")
    wp_widget_factory_.register(widget_)
# end def register_widget
#// 
#// Unregisters a widget.
#// 
#// Unregisters a WP_Widget widget. Useful for un-registering default widgets.
#// Run within a function hooked to the {@see 'widgets_init'} action.
#// 
#// @since 2.8.0
#// @since 4.6.0 Updated the `$widget` parameter to also accept a WP_Widget instance object
#// instead of simply a `WP_Widget` subclass name.
#// 
#// @see WP_Widget
#// 
#// @global WP_Widget_Factory $wp_widget_factory
#// 
#// @param string|WP_Widget $widget Either the name of a `WP_Widget` subclass or an instance of a `WP_Widget` subclass.
#//
def unregister_widget(widget_=None, *_args_):
    
    
    global wp_widget_factory_
    php_check_if_defined("wp_widget_factory_")
    wp_widget_factory_.unregister(widget_)
# end def unregister_widget
#// 
#// Creates multiple sidebars.
#// 
#// If you wanted to quickly create multiple sidebars for a theme or internally.
#// This function will allow you to do so. If you don't pass the 'name' and/or
#// 'id' in `$args`, then they will be built for you.
#// 
#// @since 2.2.0
#// 
#// @see register_sidebar() The second parameter is documented by register_sidebar() and is the same here.
#// 
#// @global array $wp_registered_sidebars The new sidebars are stored in this array by sidebar ID.
#// 
#// @param int          $number Optional. Number of sidebars to create. Default 1.
#// @param array|string $args {
#// Optional. Array or string of arguments for building a sidebar.
#// 
#// @type string $id   The base string of the unique identifier for each sidebar. If provided, and multiple
#// sidebars are being defined, the id will have "-2" appended, and so on.
#// Default 'sidebar-' followed by the number the sidebar creation is currently at.
#// @type string $name The name or title for the sidebars displayed in the admin dashboard. If registering
#// more than one sidebar, include '%d' in the string as a placeholder for the uniquely
#// assigned number for each sidebar.
#// Default 'Sidebar' for the first sidebar, otherwise 'Sidebar %d'.
#// }
#//
def register_sidebars(number_=1, args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    global wp_registered_sidebars_
    php_check_if_defined("wp_registered_sidebars_")
    number_ = php_int(number_)
    if php_is_string(args_):
        parse_str(args_, args_)
    # end if
    i_ = 1
    while i_ <= number_:
        
        _args_ = args_
        if number_ > 1:
            if (php_isset(lambda : args_["name"])):
                _args_["name"] = php_sprintf(args_["name"], i_)
            else:
                #// translators: %d: Sidebar number.
                _args_["name"] = php_sprintf(__("Sidebar %d"), i_)
            # end if
        else:
            _args_["name"] = args_["name"] if (php_isset(lambda : args_["name"])) else __("Sidebar")
        # end if
        #// Custom specified ID's are suffixed if they exist already.
        #// Automatically generated sidebar names need to be suffixed regardless starting at -0.
        if (php_isset(lambda : args_["id"])):
            _args_["id"] = args_["id"]
            n_ = 2
            #// Start at -2 for conflicting custom IDs.
            while True:
                
                if not (is_registered_sidebar(_args_["id"])):
                    break
                # end if
                _args_["id"] = args_["id"] + "-" + n_
                n_ += 1
                n_ += 1
            # end while
        else:
            n_ = php_count(wp_registered_sidebars_)
            while True:
                n_ += 1
                n_ += 1
                _args_["id"] = "sidebar-" + n_
                
                if is_registered_sidebar(_args_["id"]):
                    break
                # end if
            # end while
        # end if
        register_sidebar(_args_)
        i_ += 1
    # end while
# end def register_sidebars
#// 
#// Builds the definition for a single sidebar and returns the ID.
#// 
#// Accepts either a string or an array and then parses that against a set
#// of default arguments for the new sidebar. WordPress will automatically
#// generate a sidebar ID and name based on the current number of registered
#// sidebars if those arguments are not included.
#// 
#// When allowing for automatic generation of the name and ID parameters, keep
#// in mind that the incrementor for your sidebar can change over time depending
#// on what other plugins and themes are installed.
#// 
#// If theme support for 'widgets' has not yet been added when this function is
#// called, it will be automatically enabled through the use of add_theme_support()
#// 
#// @since 2.2.0
#// 
#// @global array $wp_registered_sidebars Stores the new sidebar in this array by sidebar ID.
#// 
#// @param array|string $args {
#// Optional. Array or string of arguments for the sidebar being registered.
#// 
#// @type string $name          The name or title of the sidebar displayed in the Widgets
#// interface. Default 'Sidebar $instance'.
#// @type string $id            The unique identifier by which the sidebar will be called.
#// Default 'sidebar-$instance'.
#// @type string $description   Description of the sidebar, displayed in the Widgets interface.
#// Default empty string.
#// @type string $class         Extra CSS class to assign to the sidebar in the Widgets interface.
#// Default empty.
#// @type string $before_widget HTML content to prepend to each widget's HTML output when
#// assigned to this sidebar. Default is an opening list item element.
#// @type string $after_widget  HTML content to append to each widget's HTML output when
#// assigned to this sidebar. Default is a closing list item element.
#// @type string $before_title  HTML content to prepend to the sidebar title when displayed.
#// Default is an opening h2 element.
#// @type string $after_title   HTML content to append to the sidebar title when displayed.
#// Default is a closing h2 element.
#// }
#// @return string Sidebar ID added to $wp_registered_sidebars global.
#//
def register_sidebar(args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    global wp_registered_sidebars_
    php_check_if_defined("wp_registered_sidebars_")
    i_ = php_count(wp_registered_sidebars_) + 1
    id_is_empty_ = php_empty(lambda : args_["id"])
    defaults_ = Array({"name": php_sprintf(__("Sidebar %d"), i_), "id": str("sidebar-") + str(i_), "description": "", "class": "", "before_widget": "<li id=\"%1$s\" class=\"widget %2$s\">", "after_widget": "</li>\n", "before_title": "<h2 class=\"widgettitle\">", "after_title": "</h2>\n"})
    #// 
    #// Filters the sidebar default arguments.
    #// 
    #// @since 5.3.0
    #// 
    #// @see register_sidebar()
    #// 
    #// @param array $defaults The default sidebar arguments.
    #//
    sidebar_ = wp_parse_args(args_, apply_filters("register_sidebar_defaults", defaults_))
    if id_is_empty_:
        _doing_it_wrong(__FUNCTION__, php_sprintf(__("No %1$s was set in the arguments array for the \"%2$s\" sidebar. Defaulting to \"%3$s\". Manually set the %1$s to \"%3$s\" to silence this notice and keep existing sidebar content."), "<code>id</code>", sidebar_["name"], sidebar_["id"]), "4.2.0")
    # end if
    wp_registered_sidebars_[sidebar_["id"]] = sidebar_
    add_theme_support("widgets")
    #// 
    #// Fires once a sidebar has been registered.
    #// 
    #// @since 3.0.0
    #// 
    #// @param array $sidebar Parsed arguments for the registered sidebar.
    #//
    do_action("register_sidebar", sidebar_)
    return sidebar_["id"]
# end def register_sidebar
#// 
#// Removes a sidebar from the list.
#// 
#// @since 2.2.0
#// 
#// @global array $wp_registered_sidebars Removes the sidebar from this array by sidebar ID.
#// 
#// @param string|int $sidebar_id The ID of the sidebar when it was registered.
#//
def unregister_sidebar(sidebar_id_=None, *_args_):
    
    
    global wp_registered_sidebars_
    php_check_if_defined("wp_registered_sidebars_")
    wp_registered_sidebars_[sidebar_id_] = None
# end def unregister_sidebar
#// 
#// Checks if a sidebar is registered.
#// 
#// @since 4.4.0
#// 
#// @global array $wp_registered_sidebars Registered sidebars.
#// 
#// @param string|int $sidebar_id The ID of the sidebar when it was registered.
#// @return bool True if the sidebar is registered, false otherwise.
#//
def is_registered_sidebar(sidebar_id_=None, *_args_):
    
    
    global wp_registered_sidebars_
    php_check_if_defined("wp_registered_sidebars_")
    return (php_isset(lambda : wp_registered_sidebars_[sidebar_id_]))
# end def is_registered_sidebar
#// 
#// Register an instance of a widget.
#// 
#// The default widget option is 'classname' that can be overridden.
#// 
#// The function can also be used to un-register widgets when `$output_callback`
#// parameter is an empty string.
#// 
#// @since 2.2.0
#// @since 5.3.0 Formalized the existing and already documented `...$params` parameter
#// by adding it to the function signature.
#// 
#// @global array $wp_registered_widgets            Uses stored registered widgets.
#// @global array $wp_registered_widget_controls    Stores the registered widget controls (options).
#// @global array $wp_registered_widget_updates
#// @global array $_wp_deprecated_widgets_callbacks
#// 
#// @param int|string $id              Widget ID.
#// @param string     $name            Widget display title.
#// @param callable   $output_callback Run when widget is called.
#// @param array      $options {
#// Optional. An array of supplementary widget options for the instance.
#// 
#// @type string $classname   Class name for the widget's HTML container. Default is a shortened
#// version of the output callback name.
#// @type string $description Widget description for display in the widget administration
#// panel and/or theme.
#// }
#// @param mixed      ...$params       Optional additional parameters to pass to the callback function when it's called.
#//
def wp_register_sidebar_widget(id_=None, name_=None, output_callback_=None, options_=None, *params_):
    if options_ is None:
        options_ = Array()
    # end if
    
    global wp_registered_widgets_
    global wp_registered_widget_controls_
    global wp_registered_widget_updates_
    global _wp_deprecated_widgets_callbacks_
    php_check_if_defined("wp_registered_widgets_","wp_registered_widget_controls_","wp_registered_widget_updates_","_wp_deprecated_widgets_callbacks_")
    id_ = php_strtolower(id_)
    if php_empty(lambda : output_callback_):
        wp_registered_widgets_[id_] = None
        return
    # end if
    id_base_ = _get_widget_id_base(id_)
    if php_in_array(output_callback_, _wp_deprecated_widgets_callbacks_, True) and (not php_is_callable(output_callback_)):
        wp_registered_widget_controls_[id_] = None
        wp_registered_widget_updates_[id_base_] = None
        return
    # end if
    defaults_ = Array({"classname": output_callback_})
    options_ = wp_parse_args(options_, defaults_)
    widget_ = Array({"name": name_, "id": id_, "callback": output_callback_, "params": params_})
    widget_ = php_array_merge(widget_, options_)
    if php_is_callable(output_callback_) and (not (php_isset(lambda : wp_registered_widgets_[id_]))) or did_action("widgets_init"):
        #// 
        #// Fires once for each registered widget.
        #// 
        #// @since 3.0.0
        #// 
        #// @param array $widget An array of default widget arguments.
        #//
        do_action("wp_register_sidebar_widget", widget_)
        wp_registered_widgets_[id_] = widget_
    # end if
# end def wp_register_sidebar_widget
#// 
#// Retrieve description for widget.
#// 
#// When registering widgets, the options can also include 'description' that
#// describes the widget for display on the widget administration panel or
#// in the theme.
#// 
#// @since 2.5.0
#// 
#// @global array $wp_registered_widgets
#// 
#// @param int|string $id Widget ID.
#// @return string|void Widget description, if available.
#//
def wp_widget_description(id_=None, *_args_):
    
    
    if (not is_scalar(id_)):
        return
    # end if
    global wp_registered_widgets_
    php_check_if_defined("wp_registered_widgets_")
    if (php_isset(lambda : wp_registered_widgets_[id_]["description"])):
        return esc_html(wp_registered_widgets_[id_]["description"])
    # end if
# end def wp_widget_description
#// 
#// Retrieve description for a sidebar.
#// 
#// When registering sidebars a 'description' parameter can be included that
#// describes the sidebar for display on the widget administration panel.
#// 
#// @since 2.9.0
#// 
#// @global array $wp_registered_sidebars Registered sidebars.
#// 
#// @param string $id sidebar ID.
#// @return string|void Sidebar description, if available.
#//
def wp_sidebar_description(id_=None, *_args_):
    
    
    if (not is_scalar(id_)):
        return
    # end if
    global wp_registered_sidebars_
    php_check_if_defined("wp_registered_sidebars_")
    if (php_isset(lambda : wp_registered_sidebars_[id_]["description"])):
        return wp_kses(wp_registered_sidebars_[id_]["description"], "sidebar_description")
    # end if
# end def wp_sidebar_description
#// 
#// Remove widget from sidebar.
#// 
#// @since 2.2.0
#// 
#// @param int|string $id Widget ID.
#//
def wp_unregister_sidebar_widget(id_=None, *_args_):
    
    
    #// 
    #// Fires just before a widget is removed from a sidebar.
    #// 
    #// @since 3.0.0
    #// 
    #// @param int $id The widget ID.
    #//
    do_action("wp_unregister_sidebar_widget", id_)
    wp_register_sidebar_widget(id_, "", "")
    wp_unregister_widget_control(id_)
# end def wp_unregister_sidebar_widget
#// 
#// Registers widget control callback for customizing options.
#// 
#// @since 2.2.0
#// @since 5.3.0 Formalized the existing and already documented `...$params` parameter
#// by adding it to the function signature.
#// 
#// @global array $wp_registered_widget_controls
#// @global array $wp_registered_widget_updates
#// @global array $wp_registered_widgets
#// @global array $_wp_deprecated_widgets_callbacks
#// 
#// @param int|string $id               Sidebar ID.
#// @param string     $name             Sidebar display name.
#// @param callable   $control_callback Run when sidebar is displayed.
#// @param array      $options {
#// Optional. Array or string of control options. Default empty array.
#// 
#// @type int        $height  Never used. Default 200.
#// @type int        $width   Width of the fully expanded control form (but try hard to use the default width).
#// Default 250.
#// @type int|string $id_base Required for multi-widgets, i.e widgets that allow multiple instances such as the
#// text widget. The widget id will end up looking like `{$id_base}-{$unique_number}`.
#// }
#// @param mixed      ...$params        Optional additional parameters to pass to the callback function when it's called.
#//
def wp_register_widget_control(id_=None, name_=None, control_callback_=None, options_=None, *params_):
    if options_ is None:
        options_ = Array()
    # end if
    
    global wp_registered_widget_controls_
    global wp_registered_widget_updates_
    global wp_registered_widgets_
    global _wp_deprecated_widgets_callbacks_
    php_check_if_defined("wp_registered_widget_controls_","wp_registered_widget_updates_","wp_registered_widgets_","_wp_deprecated_widgets_callbacks_")
    id_ = php_strtolower(id_)
    id_base_ = _get_widget_id_base(id_)
    if php_empty(lambda : control_callback_):
        wp_registered_widget_controls_[id_] = None
        wp_registered_widget_updates_[id_base_] = None
        return
    # end if
    if php_in_array(control_callback_, _wp_deprecated_widgets_callbacks_, True) and (not php_is_callable(control_callback_)):
        wp_registered_widgets_[id_] = None
        return
    # end if
    if (php_isset(lambda : wp_registered_widget_controls_[id_])) and (not did_action("widgets_init")):
        return
    # end if
    defaults_ = Array({"width": 250, "height": 200})
    #// Height is never used.
    options_ = wp_parse_args(options_, defaults_)
    options_["width"] = php_int(options_["width"])
    options_["height"] = php_int(options_["height"])
    widget_ = Array({"name": name_, "id": id_, "callback": control_callback_, "params": params_})
    widget_ = php_array_merge(widget_, options_)
    wp_registered_widget_controls_[id_] = widget_
    if (php_isset(lambda : wp_registered_widget_updates_[id_base_])):
        return
    # end if
    if (php_isset(lambda : widget_["params"][0]["number"])):
        widget_["params"][0]["number"] = -1
    # end if
    widget_["width"] = None
    widget_["height"] = None
    widget_["name"] = None
    widget_["id"] = None
    wp_registered_widget_updates_[id_base_] = widget_
# end def wp_register_widget_control
#// 
#// Registers the update callback for a widget.
#// 
#// @since 2.8.0
#// @since 5.3.0 Formalized the existing and already documented `...$params` parameter
#// by adding it to the function signature.
#// 
#// @global array $wp_registered_widget_updates
#// 
#// @param string   $id_base         The base ID of a widget created by extending WP_Widget.
#// @param callable $update_callback Update callback method for the widget.
#// @param array    $options         Optional. Widget control options. See wp_register_widget_control().
#// Default empty array.
#// @param mixed    ...$params       Optional additional parameters to pass to the callback function when it's called.
#//
def _register_widget_update_callback(id_base_=None, update_callback_=None, options_=None, *params_):
    if options_ is None:
        options_ = Array()
    # end if
    
    global wp_registered_widget_updates_
    php_check_if_defined("wp_registered_widget_updates_")
    if (php_isset(lambda : wp_registered_widget_updates_[id_base_])):
        if php_empty(lambda : update_callback_):
            wp_registered_widget_updates_[id_base_] = None
        # end if
        return
    # end if
    widget_ = Array({"callback": update_callback_, "params": params_})
    widget_ = php_array_merge(widget_, options_)
    wp_registered_widget_updates_[id_base_] = widget_
# end def _register_widget_update_callback
#// 
#// Registers the form callback for a widget.
#// 
#// @since 2.8.0
#// @since 5.3.0 Formalized the existing and already documented `...$params` parameter
#// by adding it to the function signature.
#// 
#// @global array $wp_registered_widget_controls
#// 
#// @param int|string $id            Widget ID.
#// @param string     $name          Name attribute for the widget.
#// @param callable   $form_callback Form callback.
#// @param array      $options       Optional. Widget control options. See wp_register_widget_control().
#// Default empty array.
#// @param mixed      ...$params     Optional additional parameters to pass to the callback function when it's called.
#//
def _register_widget_form_callback(id_=None, name_=None, form_callback_=None, options_=None, *params_):
    if options_ is None:
        options_ = Array()
    # end if
    
    global wp_registered_widget_controls_
    php_check_if_defined("wp_registered_widget_controls_")
    id_ = php_strtolower(id_)
    if php_empty(lambda : form_callback_):
        wp_registered_widget_controls_[id_] = None
        return
    # end if
    if (php_isset(lambda : wp_registered_widget_controls_[id_])) and (not did_action("widgets_init")):
        return
    # end if
    defaults_ = Array({"width": 250, "height": 200})
    options_ = wp_parse_args(options_, defaults_)
    options_["width"] = php_int(options_["width"])
    options_["height"] = php_int(options_["height"])
    widget_ = Array({"name": name_, "id": id_, "callback": form_callback_, "params": params_})
    widget_ = php_array_merge(widget_, options_)
    wp_registered_widget_controls_[id_] = widget_
# end def _register_widget_form_callback
#// 
#// Remove control callback for widget.
#// 
#// @since 2.2.0
#// 
#// @param int|string $id Widget ID.
#//
def wp_unregister_widget_control(id_=None, *_args_):
    
    
    wp_register_widget_control(id_, "", "")
# end def wp_unregister_widget_control
#// 
#// Display dynamic sidebar.
#// 
#// By default this displays the default sidebar or 'sidebar-1'. If your theme specifies the 'id' or
#// 'name' parameter for its registered sidebars you can pass an id or name as the $index parameter.
#// Otherwise, you can pass in a numerical index to display the sidebar at that index.
#// 
#// @since 2.2.0
#// 
#// @global array $wp_registered_sidebars Registered sidebars.
#// @global array $wp_registered_widgets
#// 
#// @param int|string $index Optional, default is 1. Index, name or ID of dynamic sidebar.
#// @return bool True, if widget sidebar was found and called. False if not found or not called.
#//
def dynamic_sidebar(index_=1, *_args_):
    
    
    global wp_registered_sidebars_
    global wp_registered_widgets_
    php_check_if_defined("wp_registered_sidebars_","wp_registered_widgets_")
    if php_is_int(index_):
        index_ = str("sidebar-") + str(index_)
    else:
        index_ = sanitize_title(index_)
        for key_,value_ in wp_registered_sidebars_:
            if sanitize_title(value_["name"]) == index_:
                index_ = key_
                break
            # end if
        # end for
    # end if
    sidebars_widgets_ = wp_get_sidebars_widgets()
    if php_empty(lambda : wp_registered_sidebars_[index_]) or php_empty(lambda : sidebars_widgets_[index_]) or (not php_is_array(sidebars_widgets_[index_])):
        #// This action is documented in wp-includes/widget.php
        do_action("dynamic_sidebar_before", index_, False)
        #// This action is documented in wp-includes/widget.php
        do_action("dynamic_sidebar_after", index_, False)
        #// This filter is documented in wp-includes/widget.php
        return apply_filters("dynamic_sidebar_has_widgets", False, index_)
    # end if
    #// 
    #// Fires before widgets are rendered in a dynamic sidebar.
    #// 
    #// Note: The action also fires for empty sidebars, and on both the front end
    #// and back end, including the Inactive Widgets sidebar on the Widgets screen.
    #// 
    #// @since 3.9.0
    #// 
    #// @param int|string $index       Index, name, or ID of the dynamic sidebar.
    #// @param bool       $has_widgets Whether the sidebar is populated with widgets.
    #// Default true.
    #//
    do_action("dynamic_sidebar_before", index_, True)
    sidebar_ = wp_registered_sidebars_[index_]
    did_one_ = False
    for id_ in sidebars_widgets_[index_]:
        if (not (php_isset(lambda : wp_registered_widgets_[id_]))):
            continue
        # end if
        params_ = php_array_merge(Array(php_array_merge(sidebar_, Array({"widget_id": id_, "widget_name": wp_registered_widgets_[id_]["name"]}))), wp_registered_widgets_[id_]["params"])
        #// Substitute HTML `id` and `class` attributes into `before_widget`.
        classname__ = ""
        for cn_ in wp_registered_widgets_[id_]["classname"]:
            if php_is_string(cn_):
                classname__ += "_" + cn_
            elif php_is_object(cn_):
                classname__ += "_" + get_class(cn_)
            # end if
        # end for
        classname__ = php_ltrim(classname__, "_")
        params_[0]["before_widget"] = php_sprintf(params_[0]["before_widget"], id_, classname__)
        #// 
        #// Filters the parameters passed to a widget's display callback.
        #// 
        #// Note: The filter is evaluated on both the front end and back end,
        #// including for the Inactive Widgets sidebar on the Widgets screen.
        #// 
        #// @since 2.5.0
        #// 
        #// @see register_sidebar()
        #// 
        #// @param array $params {
        #// @type array $args  {
        #// An array of widget display arguments.
        #// 
        #// @type string $name          Name of the sidebar the widget is assigned to.
        #// @type string $id            ID of the sidebar the widget is assigned to.
        #// @type string $description   The sidebar description.
        #// @type string $class         CSS class applied to the sidebar container.
        #// @type string $before_widget HTML markup to prepend to each widget in the sidebar.
        #// @type string $after_widget  HTML markup to append to each widget in the sidebar.
        #// @type string $before_title  HTML markup to prepend to the widget title when displayed.
        #// @type string $after_title   HTML markup to append to the widget title when displayed.
        #// @type string $widget_id     ID of the widget.
        #// @type string $widget_name   Name of the widget.
        #// }
        #// @type array $widget_args {
        #// An array of multi-widget arguments.
        #// 
        #// @type int $number Number increment used for multiples of the same widget.
        #// }
        #// }
        #//
        params_ = apply_filters("dynamic_sidebar_params", params_)
        callback_ = wp_registered_widgets_[id_]["callback"]
        #// 
        #// Fires before a widget's display callback is called.
        #// 
        #// Note: The action fires on both the front end and back end, including
        #// for widgets in the Inactive Widgets sidebar on the Widgets screen.
        #// 
        #// The action is not fired for empty sidebars.
        #// 
        #// @since 3.0.0
        #// 
        #// @param array $widget_id {
        #// An associative array of widget arguments.
        #// 
        #// @type string $name                Name of the widget.
        #// @type string $id                  Widget ID.
        #// @type array|callable $callback    When the hook is fired on the front end, $callback is an array
        #// containing the widget object. Fired on the back end, $callback
        #// is 'wp_widget_control', see $_callback.
        #// @type array          $params      An associative array of multi-widget arguments.
        #// @type string         $classname   CSS class applied to the widget container.
        #// @type string         $description The widget description.
        #// @type array          $_callback   When the hook is fired on the back end, $_callback is populated
        #// with an array containing the widget object, see $callback.
        #// }
        #//
        do_action("dynamic_sidebar", wp_registered_widgets_[id_])
        if php_is_callable(callback_):
            call_user_func_array(callback_, params_)
            did_one_ = True
        # end if
    # end for
    #// 
    #// Fires after widgets are rendered in a dynamic sidebar.
    #// 
    #// Note: The action also fires for empty sidebars, and on both the front end
    #// and back end, including the Inactive Widgets sidebar on the Widgets screen.
    #// 
    #// @since 3.9.0
    #// 
    #// @param int|string $index       Index, name, or ID of the dynamic sidebar.
    #// @param bool       $has_widgets Whether the sidebar is populated with widgets.
    #// Default true.
    #//
    do_action("dynamic_sidebar_after", index_, True)
    #// 
    #// Filters whether a sidebar has widgets.
    #// 
    #// Note: The filter is also evaluated for empty sidebars, and on both the front end
    #// and back end, including the Inactive Widgets sidebar on the Widgets screen.
    #// 
    #// @since 3.9.0
    #// 
    #// @param bool       $did_one Whether at least one widget was rendered in the sidebar.
    #// Default false.
    #// @param int|string $index   Index, name, or ID of the dynamic sidebar.
    #//
    return apply_filters("dynamic_sidebar_has_widgets", did_one_, index_)
# end def dynamic_sidebar
#// 
#// Determines whether a given widget is displayed on the front end.
#// 
#// Either $callback or $id_base can be used
#// $id_base is the first argument when extending WP_Widget class
#// Without the optional $widget_id parameter, returns the ID of the first sidebar
#// in which the first instance of the widget with the given callback or $id_base is found.
#// With the $widget_id parameter, returns the ID of the sidebar where
#// the widget with that callback/$id_base AND that ID is found.
#// 
#// NOTE: $widget_id and $id_base are the same for single widgets. To be effective
#// this function has to run after widgets have initialized, at action {@see 'init'} or later.
#// 
#// For more information on this and similar theme functions, check out
#// the {@link https://developer.wordpress.org/themes/basics/conditional-tags
#// Conditional Tags} article in the Theme Developer Handbook.
#// 
#// @since 2.2.0
#// 
#// @global array $wp_registered_widgets
#// 
#// @param string|false $callback      Optional, Widget callback to check. Default false.
#// @param int|false    $widget_id     Optional. Widget ID. Optional, but needed for checking. Default false.
#// @param string|false $id_base       Optional. The base ID of a widget created by extending WP_Widget. Default false.
#// @param bool         $skip_inactive Optional. Whether to check in 'wp_inactive_widgets'. Default true.
#// @return string|false False if widget is not active or id of sidebar in which the widget is active.
#//
def is_active_widget(callback_=None, widget_id_=None, id_base_=None, skip_inactive_=None, *_args_):
    if callback_ is None:
        callback_ = False
    # end if
    if widget_id_ is None:
        widget_id_ = False
    # end if
    if id_base_ is None:
        id_base_ = False
    # end if
    if skip_inactive_ is None:
        skip_inactive_ = True
    # end if
    
    global wp_registered_widgets_
    php_check_if_defined("wp_registered_widgets_")
    sidebars_widgets_ = wp_get_sidebars_widgets()
    if php_is_array(sidebars_widgets_):
        for sidebar_,widgets_ in sidebars_widgets_:
            if skip_inactive_ and "wp_inactive_widgets" == sidebar_ or "orphaned_widgets" == php_substr(sidebar_, 0, 16):
                continue
            # end if
            if php_is_array(widgets_):
                for widget_ in widgets_:
                    if callback_ and (php_isset(lambda : wp_registered_widgets_[widget_]["callback"])) and wp_registered_widgets_[widget_]["callback"] == callback_ or id_base_ and _get_widget_id_base(widget_) == id_base_:
                        if (not widget_id_) or widget_id_ == wp_registered_widgets_[widget_]["id"]:
                            return sidebar_
                        # end if
                    # end if
                # end for
            # end if
        # end for
    # end if
    return False
# end def is_active_widget
#// 
#// Determines whether the dynamic sidebar is enabled and used by the theme.
#// 
#// For more information on this and similar theme functions, check out
#// the {@link https://developer.wordpress.org/themes/basics/conditional-tags
#// Conditional Tags} article in the Theme Developer Handbook.
#// 
#// @since 2.2.0
#// 
#// @global array $wp_registered_widgets
#// @global array $wp_registered_sidebars Registered sidebars.
#// 
#// @return bool True, if using widgets. False, if not using widgets.
#//
def is_dynamic_sidebar(*_args_):
    
    
    global wp_registered_widgets_
    global wp_registered_sidebars_
    php_check_if_defined("wp_registered_widgets_","wp_registered_sidebars_")
    sidebars_widgets_ = get_option("sidebars_widgets")
    for index_,sidebar_ in wp_registered_sidebars_:
        if (not php_empty(lambda : sidebars_widgets_[index_])):
            for widget_ in sidebars_widgets_[index_]:
                if php_array_key_exists(widget_, wp_registered_widgets_):
                    return True
                # end if
            # end for
        # end if
    # end for
    return False
# end def is_dynamic_sidebar
#// 
#// Determines whether a sidebar is in use.
#// 
#// For more information on this and similar theme functions, check out
#// the {@link https://developer.wordpress.org/themes/basics/conditional-tags
#// Conditional Tags} article in the Theme Developer Handbook.
#// 
#// @since 2.8.0
#// 
#// @param string|int $index Sidebar name, id or number to check.
#// @return bool true if the sidebar is in use, false otherwise.
#//
def is_active_sidebar(index_=None, *_args_):
    
    
    index_ = str("sidebar-") + str(index_) if php_is_int(index_) else sanitize_title(index_)
    sidebars_widgets_ = wp_get_sidebars_widgets()
    is_active_sidebar_ = (not php_empty(lambda : sidebars_widgets_[index_]))
    #// 
    #// Filters whether a dynamic sidebar is considered "active".
    #// 
    #// @since 3.9.0
    #// 
    #// @param bool       $is_active_sidebar Whether or not the sidebar should be considered "active".
    #// In other words, whether the sidebar contains any widgets.
    #// @param int|string $index             Index, name, or ID of the dynamic sidebar.
    #//
    return apply_filters("is_active_sidebar", is_active_sidebar_, index_)
# end def is_active_sidebar
#// 
#// Internal Functions.
#// 
#// 
#// Retrieve full list of sidebars and their widget instance IDs.
#// 
#// Will upgrade sidebar widget list, if needed. Will also save updated list, if
#// needed.
#// 
#// @since 2.2.0
#// @access private
#// 
#// @global array $_wp_sidebars_widgets
#// @global array $sidebars_widgets
#// 
#// @param bool $deprecated Not used (argument deprecated).
#// @return array Upgraded list of widgets to version 3 array format when called from the admin.
#//
def wp_get_sidebars_widgets(deprecated_=None, *_args_):
    if deprecated_ is None:
        deprecated_ = True
    # end if
    
    if True != deprecated_:
        _deprecated_argument(__FUNCTION__, "2.8.1")
    # end if
    global _wp_sidebars_widgets_
    global sidebars_widgets_
    php_check_if_defined("_wp_sidebars_widgets_","sidebars_widgets_")
    #// If loading from front page, consult $_wp_sidebars_widgets rather than options
    #// to see if wp_convert_widget_settings() has made manipulations in memory.
    if (not is_admin()):
        if php_empty(lambda : _wp_sidebars_widgets_):
            _wp_sidebars_widgets_ = get_option("sidebars_widgets", Array())
        # end if
        sidebars_widgets_ = _wp_sidebars_widgets_
    else:
        sidebars_widgets_ = get_option("sidebars_widgets", Array())
    # end if
    if php_is_array(sidebars_widgets_) and (php_isset(lambda : sidebars_widgets_["array_version"])):
        sidebars_widgets_["array_version"] = None
    # end if
    #// 
    #// Filters the list of sidebars and their widgets.
    #// 
    #// @since 2.7.0
    #// 
    #// @param array $sidebars_widgets An associative array of sidebars and their widgets.
    #//
    return apply_filters("sidebars_widgets", sidebars_widgets_)
# end def wp_get_sidebars_widgets
#// 
#// Set the sidebar widget option to update sidebars.
#// 
#// @since 2.2.0
#// @access private
#// 
#// @global array $_wp_sidebars_widgets
#// @param array $sidebars_widgets Sidebar widgets and their settings.
#//
def wp_set_sidebars_widgets(sidebars_widgets_=None, *_args_):
    
    
    global _wp_sidebars_widgets_
    php_check_if_defined("_wp_sidebars_widgets_")
    #// Clear cached value used in wp_get_sidebars_widgets().
    _wp_sidebars_widgets_ = None
    if (not (php_isset(lambda : sidebars_widgets_["array_version"]))):
        sidebars_widgets_["array_version"] = 3
    # end if
    update_option("sidebars_widgets", sidebars_widgets_)
# end def wp_set_sidebars_widgets
#// 
#// Retrieve default registered sidebars list.
#// 
#// @since 2.2.0
#// @access private
#// 
#// @global array $wp_registered_sidebars Registered sidebars.
#// 
#// @return array
#//
def wp_get_widget_defaults(*_args_):
    
    
    global wp_registered_sidebars_
    php_check_if_defined("wp_registered_sidebars_")
    defaults_ = Array()
    for index_,sidebar_ in wp_registered_sidebars_:
        defaults_[index_] = Array()
    # end for
    return defaults_
# end def wp_get_widget_defaults
#// 
#// Convert the widget settings from single to multi-widget format.
#// 
#// @since 2.8.0
#// 
#// @global array $_wp_sidebars_widgets
#// 
#// @param string $base_name
#// @param string $option_name
#// @param array  $settings
#// @return array
#//
def wp_convert_widget_settings(base_name_=None, option_name_=None, settings_=None, *_args_):
    
    global PHP_GLOBALS
    #// This test may need expanding.
    single_ = False
    changed_ = False
    if php_empty(lambda : settings_):
        single_ = True
    else:
        for number_ in php_array_keys(settings_):
            if "number" == number_:
                continue
            # end if
            if (not php_is_numeric(number_)):
                single_ = True
                break
            # end if
        # end for
    # end if
    if single_:
        settings_ = Array({2: settings_})
        #// If loading from the front page, update sidebar in memory but don't save to options.
        if is_admin():
            sidebars_widgets_ = get_option("sidebars_widgets")
        else:
            if php_empty(lambda : PHP_GLOBALS["_wp_sidebars_widgets"]):
                PHP_GLOBALS["_wp_sidebars_widgets"] = get_option("sidebars_widgets", Array())
            # end if
            sidebars_widgets_ = PHP_GLOBALS["_wp_sidebars_widgets"]
        # end if
        for index_,sidebar_ in sidebars_widgets_:
            if php_is_array(sidebar_):
                for i_,name_ in sidebar_:
                    if base_name_ == name_:
                        sidebars_widgets_[index_][i_] = str(name_) + str("-2")
                        changed_ = True
                        break
                    # end if
                # end for
            # end if
        # end for
        if is_admin() and changed_:
            update_option("sidebars_widgets", sidebars_widgets_)
        # end if
    # end if
    settings_["_multiwidget"] = 1
    if is_admin():
        update_option(option_name_, settings_)
    # end if
    return settings_
# end def wp_convert_widget_settings
#// 
#// Output an arbitrary widget as a template tag.
#// 
#// @since 2.8.0
#// 
#// @global WP_Widget_Factory $wp_widget_factory
#// 
#// @param string $widget   The widget's PHP class name (see class-wp-widget.php).
#// @param array  $instance Optional. The widget's instance settings. Default empty array.
#// @param array  $args {
#// Optional. Array of arguments to configure the display of the widget.
#// 
#// @type string $before_widget HTML content that will be prepended to the widget's HTML output.
#// Default `<div class="widget %s">`, where `%s` is the widget's class name.
#// @type string $after_widget  HTML content that will be appended to the widget's HTML output.
#// Default `</div>`.
#// @type string $before_title  HTML content that will be prepended to the widget's title when displayed.
#// Default `<h2 class="widgettitle">`.
#// @type string $after_title   HTML content that will be appended to the widget's title when displayed.
#// Default `</h2>`.
#// }
#//
def the_widget(widget_=None, instance_=None, args_=None, *_args_):
    if instance_ is None:
        instance_ = Array()
    # end if
    if args_ is None:
        args_ = Array()
    # end if
    
    global wp_widget_factory_
    php_check_if_defined("wp_widget_factory_")
    if (not (php_isset(lambda : wp_widget_factory_.widgets[widget_]))):
        _doing_it_wrong(__FUNCTION__, php_sprintf(__("Widgets need to be registered using %s, before they can be displayed."), "<code>register_widget()</code>"), "4.9.0")
        return
    # end if
    widget_obj_ = wp_widget_factory_.widgets[widget_]
    if (not type(widget_obj_).__name__ == "WP_Widget"):
        return
    # end if
    default_args_ = Array({"before_widget": "<div class=\"widget %s\">", "after_widget": "</div>", "before_title": "<h2 class=\"widgettitle\">", "after_title": "</h2>"})
    args_ = wp_parse_args(args_, default_args_)
    args_["before_widget"] = php_sprintf(args_["before_widget"], widget_obj_.widget_options["classname"])
    instance_ = wp_parse_args(instance_)
    #// This filter is documented in wp-includes/class-wp-widget.php
    instance_ = apply_filters("widget_display_callback", instance_, widget_obj_, args_)
    if False == instance_:
        return
    # end if
    #// 
    #// Fires before rendering the requested widget.
    #// 
    #// @since 3.0.0
    #// 
    #// @param string $widget   The widget's class name.
    #// @param array  $instance The current widget instance's settings.
    #// @param array  $args     An array of the widget's sidebar arguments.
    #//
    do_action("the_widget", widget_, instance_, args_)
    widget_obj_._set(-1)
    widget_obj_.widget(args_, instance_)
# end def the_widget
#// 
#// Retrieves the widget ID base value.
#// 
#// @since 2.8.0
#// 
#// @param string $id Widget ID.
#// @return string Widget ID base.
#//
def _get_widget_id_base(id_=None, *_args_):
    
    
    return php_preg_replace("/-[0-9]+$/", "", id_)
# end def _get_widget_id_base
#// 
#// Handle sidebars config after theme change
#// 
#// @access private
#// @since 3.3.0
#// 
#// @global array $sidebars_widgets
#//
def _wp_sidebars_changed(*_args_):
    
    
    global sidebars_widgets_
    php_check_if_defined("sidebars_widgets_")
    if (not php_is_array(sidebars_widgets_)):
        sidebars_widgets_ = wp_get_sidebars_widgets()
    # end if
    retrieve_widgets(True)
# end def _wp_sidebars_changed
#// 
#// Look for "lost" widgets, this has to run at least on each theme change.
#// 
#// @since 2.8.0
#// 
#// @global array $wp_registered_sidebars Registered sidebars.
#// @global array $sidebars_widgets
#// @global array $wp_registered_widgets
#// 
#// @param string|bool $theme_changed Whether the theme was changed as a boolean. A value
#// of 'customize' defers updates for the Customizer.
#// @return array Updated sidebars widgets.
#//
def retrieve_widgets(theme_changed_=None, *_args_):
    if theme_changed_ is None:
        theme_changed_ = False
    # end if
    
    global wp_registered_sidebars_
    global sidebars_widgets_
    global wp_registered_widgets_
    php_check_if_defined("wp_registered_sidebars_","sidebars_widgets_","wp_registered_widgets_")
    registered_sidebars_keys_ = php_array_keys(wp_registered_sidebars_)
    registered_widgets_ids_ = php_array_keys(wp_registered_widgets_)
    if (not php_is_array(get_theme_mod("sidebars_widgets"))):
        if php_empty(lambda : sidebars_widgets_):
            return Array()
        # end if
        sidebars_widgets_["array_version"] = None
        sidebars_widgets_keys_ = php_array_keys(sidebars_widgets_)
        sort(sidebars_widgets_keys_)
        sort(registered_sidebars_keys_)
        if sidebars_widgets_keys_ == registered_sidebars_keys_:
            sidebars_widgets_ = _wp_remove_unregistered_widgets(sidebars_widgets_, registered_widgets_ids_)
            return sidebars_widgets_
        # end if
    # end if
    #// Discard invalid, theme-specific widgets from sidebars.
    sidebars_widgets_ = _wp_remove_unregistered_widgets(sidebars_widgets_, registered_widgets_ids_)
    sidebars_widgets_ = wp_map_sidebars_widgets(sidebars_widgets_)
    #// Find hidden/lost multi-widget instances.
    shown_widgets_ = call_user_func_array("array_merge", sidebars_widgets_)
    lost_widgets_ = php_array_diff(registered_widgets_ids_, shown_widgets_)
    for key_,widget_id_ in lost_widgets_:
        number_ = php_preg_replace("/.+?-([0-9]+)$/", "$1", widget_id_)
        #// Only keep active and default widgets.
        if php_is_numeric(number_) and php_int(number_) < 2:
            lost_widgets_[key_] = None
        # end if
    # end for
    sidebars_widgets_["wp_inactive_widgets"] = php_array_merge(lost_widgets_, sidebars_widgets_["wp_inactive_widgets"])
    if "customize" != theme_changed_:
        wp_set_sidebars_widgets(sidebars_widgets_)
    # end if
    return sidebars_widgets_
# end def retrieve_widgets
#// 
#// Compares a list of sidebars with their widgets against a whitelist.
#// 
#// @since 4.9.0
#// @since 4.9.2 Always tries to restore widget assignments from previous data, not just if sidebars needed mapping.
#// 
#// @param array $existing_sidebars_widgets List of sidebars and their widget instance IDs.
#// @return array Mapped sidebars widgets.
#//
def wp_map_sidebars_widgets(existing_sidebars_widgets_=None, *_args_):
    
    
    global wp_registered_sidebars_
    php_check_if_defined("wp_registered_sidebars_")
    new_sidebars_widgets_ = Array({"wp_inactive_widgets": Array()})
    #// Short-circuit if there are no sidebars to map.
    if (not php_is_array(existing_sidebars_widgets_)) or php_empty(lambda : existing_sidebars_widgets_):
        return new_sidebars_widgets_
    # end if
    for sidebar_,widgets_ in existing_sidebars_widgets_:
        if "wp_inactive_widgets" == sidebar_ or "orphaned_widgets" == php_substr(sidebar_, 0, 16):
            new_sidebars_widgets_["wp_inactive_widgets"] = php_array_merge(new_sidebars_widgets_["wp_inactive_widgets"], widgets_)
            existing_sidebars_widgets_[sidebar_] = None
        # end if
    # end for
    #// If old and new theme have just one sidebar, map it and we're done.
    if 1 == php_count(existing_sidebars_widgets_) and 1 == php_count(wp_registered_sidebars_):
        new_sidebars_widgets_[key(wp_registered_sidebars_)] = php_array_pop(existing_sidebars_widgets_)
        return new_sidebars_widgets_
    # end if
    #// Map locations with the same slug.
    existing_sidebars_ = php_array_keys(existing_sidebars_widgets_)
    for sidebar_,name_ in wp_registered_sidebars_:
        if php_in_array(sidebar_, existing_sidebars_, True):
            new_sidebars_widgets_[sidebar_] = existing_sidebars_widgets_[sidebar_]
            existing_sidebars_widgets_[sidebar_] = None
        elif (not php_array_key_exists(sidebar_, new_sidebars_widgets_)):
            new_sidebars_widgets_[sidebar_] = Array()
        # end if
    # end for
    #// If there are more sidebars, try to map them.
    if (not php_empty(lambda : existing_sidebars_widgets_)):
        #// 
        #// If old and new theme both have sidebars that contain phrases
        #// from within the same group, make an educated guess and map it.
        #//
        common_slug_groups_ = Array(Array("sidebar", "primary", "main", "right"), Array("second", "left"), Array("sidebar-2", "footer", "bottom"), Array("header", "top"))
        #// Go through each group...
        for slug_group_ in common_slug_groups_:
            #// ...and see if any of these slugs...
            for slug_ in slug_group_:
                #// ...and any of the new sidebars...
                for new_sidebar_,args_ in wp_registered_sidebars_:
                    #// ...actually match!
                    if False == php_stripos(new_sidebar_, slug_) and False == php_stripos(slug_, new_sidebar_):
                        continue
                    # end if
                    #// Then see if any of the existing sidebars...
                    for sidebar_,widgets_ in existing_sidebars_widgets_:
                        #// ...and any slug in the same group...
                        for slug_ in slug_group_:
                            #// ... have a match as well.
                            if False == php_stripos(sidebar_, slug_) and False == php_stripos(slug_, sidebar_):
                                continue
                            # end if
                            #// Make sure this sidebar wasn't mapped and removed previously.
                            if (not php_empty(lambda : existing_sidebars_widgets_[sidebar_])):
                                #// We have a match that can be mapped!
                                new_sidebars_widgets_[new_sidebar_] = php_array_merge(new_sidebars_widgets_[new_sidebar_], existing_sidebars_widgets_[sidebar_])
                                existing_sidebars_widgets_[sidebar_] = None
                                continue
                            # end if
                        # end for
                        pass
                    # end for
                    pass
                # end for
                pass
            # end for
            pass
        # end for
        pass
    # end if
    #// Move any left over widgets to inactive sidebar.
    for widgets_ in existing_sidebars_widgets_:
        if php_is_array(widgets_) and (not php_empty(lambda : widgets_)):
            new_sidebars_widgets_["wp_inactive_widgets"] = php_array_merge(new_sidebars_widgets_["wp_inactive_widgets"], widgets_)
        # end if
    # end for
    #// Sidebars_widgets settings from when this theme was previously active.
    old_sidebars_widgets_ = get_theme_mod("sidebars_widgets")
    old_sidebars_widgets_ = old_sidebars_widgets_["data"] if (php_isset(lambda : old_sidebars_widgets_["data"])) else False
    if php_is_array(old_sidebars_widgets_):
        #// Remove empty sidebars, no need to map those.
        old_sidebars_widgets_ = php_array_filter(old_sidebars_widgets_)
        #// Only check sidebars that are empty or have not been mapped to yet.
        for new_sidebar_,new_widgets_ in new_sidebars_widgets_:
            if php_array_key_exists(new_sidebar_, old_sidebars_widgets_) and (not php_empty(lambda : new_widgets_)):
                old_sidebars_widgets_[new_sidebar_] = None
            # end if
        # end for
        #// Remove orphaned widgets, we're only interested in previously active sidebars.
        for sidebar_,widgets_ in old_sidebars_widgets_:
            if "orphaned_widgets" == php_substr(sidebar_, 0, 16):
                old_sidebars_widgets_[sidebar_] = None
            # end if
        # end for
        old_sidebars_widgets_ = _wp_remove_unregistered_widgets(old_sidebars_widgets_)
        if (not php_empty(lambda : old_sidebars_widgets_)):
            #// Go through each remaining sidebar...
            for old_sidebar_,old_widgets_ in old_sidebars_widgets_:
                #// ...and check every new sidebar...
                for new_sidebar_,new_widgets_ in new_sidebars_widgets_:
                    #// ...for every widget we're trying to revive.
                    for key_,widget_id_ in old_widgets_:
                        active_key_ = php_array_search(widget_id_, new_widgets_, True)
                        #// If the widget is used elsewhere...
                        if False != active_key_:
                            #// ...and that elsewhere is inactive widgets...
                            if "wp_inactive_widgets" == new_sidebar_:
                                new_sidebars_widgets_["wp_inactive_widgets"][active_key_] = None
                            else:
                                old_sidebars_widgets_[old_sidebar_][key_] = None
                            # end if
                        # end if
                        pass
                    # end for
                    pass
                # end for
                pass
            # end for
            pass
        # end if
        #// End if ( ! empty( $old_sidebars_widgets ) ).
        #// Restore widget settings from when theme was previously active.
        new_sidebars_widgets_ = php_array_merge(new_sidebars_widgets_, old_sidebars_widgets_)
    # end if
    return new_sidebars_widgets_
# end def wp_map_sidebars_widgets
#// 
#// Compares a list of sidebars with their widgets against a whitelist.
#// 
#// @since 4.9.0
#// 
#// @param array $sidebars_widgets List of sidebars and their widget instance IDs.
#// @param array $whitelist        Optional. List of widget IDs to compare against. Default: Registered widgets.
#// @return array Sidebars with whitelisted widgets.
#//
def _wp_remove_unregistered_widgets(sidebars_widgets_=None, whitelist_=None, *_args_):
    if whitelist_ is None:
        whitelist_ = Array()
    # end if
    
    if php_empty(lambda : whitelist_):
        whitelist_ = php_array_keys(PHP_GLOBALS["wp_registered_widgets"])
    # end if
    for sidebar_,widgets_ in sidebars_widgets_:
        if php_is_array(widgets_):
            sidebars_widgets_[sidebar_] = php_array_intersect(widgets_, whitelist_)
        # end if
    # end for
    return sidebars_widgets_
# end def _wp_remove_unregistered_widgets
#// 
#// Display the RSS entries in a list.
#// 
#// @since 2.5.0
#// 
#// @param string|array|object $rss RSS url.
#// @param array $args Widget arguments.
#//
def wp_widget_rss_output(rss_=None, args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    if php_is_string(rss_):
        rss_ = fetch_feed(rss_)
    elif php_is_array(rss_) and (php_isset(lambda : rss_["url"])):
        args_ = rss_
        rss_ = fetch_feed(rss_["url"])
    elif (not php_is_object(rss_)):
        return
    # end if
    if is_wp_error(rss_):
        if is_admin() or current_user_can("manage_options"):
            php_print("<p><strong>" + __("RSS Error:") + "</strong> " + rss_.get_error_message() + "</p>")
        # end if
        return
    # end if
    default_args_ = Array({"show_author": 0, "show_date": 0, "show_summary": 0, "items": 0})
    args_ = wp_parse_args(args_, default_args_)
    items_ = php_int(args_["items"])
    if items_ < 1 or 20 < items_:
        items_ = 10
    # end if
    show_summary_ = php_int(args_["show_summary"])
    show_author_ = php_int(args_["show_author"])
    show_date_ = php_int(args_["show_date"])
    if (not rss_.get_item_quantity()):
        php_print("<ul><li>" + __("An error has occurred, which probably means the feed is down. Try again later.") + "</li></ul>")
        rss_.__del__()
        rss_ = None
        return
    # end if
    php_print("<ul>")
    for item_ in rss_.get_items(0, items_):
        link_ = item_.get_link()
        while True:
            
            if not (php_stristr(link_, "http") != link_):
                break
            # end if
            link_ = php_substr(link_, 1)
        # end while
        link_ = esc_url(strip_tags(link_))
        title_ = esc_html(php_trim(strip_tags(item_.get_title())))
        if php_empty(lambda : title_):
            title_ = __("Untitled")
        # end if
        desc_ = html_entity_decode(item_.get_description(), ENT_QUOTES, get_option("blog_charset"))
        desc_ = esc_attr(wp_trim_words(desc_, 55, " [&hellip;]"))
        summary_ = ""
        if show_summary_:
            summary_ = desc_
            #// Change existing [...] to [&hellip;].
            if "[...]" == php_substr(summary_, -5):
                summary_ = php_substr(summary_, 0, -5) + "[&hellip;]"
            # end if
            summary_ = "<div class=\"rssSummary\">" + esc_html(summary_) + "</div>"
        # end if
        date_ = ""
        if show_date_:
            date_ = item_.get_date("U")
            if date_:
                date_ = " <span class=\"rss-date\">" + date_i18n(get_option("date_format"), date_) + "</span>"
            # end if
        # end if
        author_ = ""
        if show_author_:
            author_ = item_.get_author()
            if php_is_object(author_):
                author_ = author_.get_name()
                author_ = " <cite>" + esc_html(strip_tags(author_)) + "</cite>"
            # end if
        # end if
        if "" == link_:
            php_print(str("<li>") + str(title_) + str(date_) + str(summary_) + str(author_) + str("</li>"))
        elif show_summary_:
            php_print(str("<li><a class='rsswidget' href='") + str(link_) + str("'>") + str(title_) + str("</a>") + str(date_) + str(summary_) + str(author_) + str("</li>"))
        else:
            php_print(str("<li><a class='rsswidget' href='") + str(link_) + str("'>") + str(title_) + str("</a>") + str(date_) + str(author_) + str("</li>"))
        # end if
    # end for
    php_print("</ul>")
    rss_.__del__()
    rss_ = None
# end def wp_widget_rss_output
#// 
#// Display RSS widget options form.
#// 
#// The options for what fields are displayed for the RSS form are all booleans
#// and are as follows: 'url', 'title', 'items', 'show_summary', 'show_author',
#// 'show_date'.
#// 
#// @since 2.5.0
#// 
#// @param array|string $args Values for input fields.
#// @param array $inputs Override default display options.
#//
def wp_widget_rss_form(args_=None, inputs_=None, *_args_):
    
    
    default_inputs_ = Array({"url": True, "title": True, "items": True, "show_summary": True, "show_author": True, "show_date": True})
    inputs_ = wp_parse_args(inputs_, default_inputs_)
    args_["title"] = args_["title"] if (php_isset(lambda : args_["title"])) else ""
    args_["url"] = args_["url"] if (php_isset(lambda : args_["url"])) else ""
    args_["items"] = php_int(args_["items"]) if (php_isset(lambda : args_["items"])) else 0
    if args_["items"] < 1 or 20 < args_["items"]:
        args_["items"] = 10
    # end if
    args_["show_summary"] = php_int(args_["show_summary"]) if (php_isset(lambda : args_["show_summary"])) else php_int(inputs_["show_summary"])
    args_["show_author"] = php_int(args_["show_author"]) if (php_isset(lambda : args_["show_author"])) else php_int(inputs_["show_author"])
    args_["show_date"] = php_int(args_["show_date"]) if (php_isset(lambda : args_["show_date"])) else php_int(inputs_["show_date"])
    if (not php_empty(lambda : args_["error"])):
        php_print("<p class=\"widget-error\"><strong>" + __("RSS Error:") + "</strong> " + args_["error"] + "</p>")
    # end if
    esc_number_ = esc_attr(args_["number"])
    if inputs_["url"]:
        php_print(" <p><label for=\"rss-url-")
        php_print(esc_number_)
        php_print("\">")
        _e("Enter the RSS feed URL here:")
        php_print("</label>\n   <input class=\"widefat\" id=\"rss-url-")
        php_print(esc_number_)
        php_print("\" name=\"widget-rss[")
        php_print(esc_number_)
        php_print("][url]\" type=\"text\" value=\"")
        php_print(esc_url(args_["url"]))
        php_print("\" /></p>\n")
    # end if
    if inputs_["title"]:
        php_print(" <p><label for=\"rss-title-")
        php_print(esc_number_)
        php_print("\">")
        _e("Give the feed a title (optional):")
        php_print("</label>\n   <input class=\"widefat\" id=\"rss-title-")
        php_print(esc_number_)
        php_print("\" name=\"widget-rss[")
        php_print(esc_number_)
        php_print("][title]\" type=\"text\" value=\"")
        php_print(esc_attr(args_["title"]))
        php_print("\" /></p>\n")
    # end if
    if inputs_["items"]:
        php_print(" <p><label for=\"rss-items-")
        php_print(esc_number_)
        php_print("\">")
        _e("How many items would you like to display?")
        php_print("</label>\n   <select id=\"rss-items-")
        php_print(esc_number_)
        php_print("\" name=\"widget-rss[")
        php_print(esc_number_)
        php_print("][items]\">\n    ")
        i_ = 1
        while i_ <= 20:
            
            php_print(str("<option value='") + str(i_) + str("' ") + selected(args_["items"], i_, False) + str(">") + str(i_) + str("</option>"))
            i_ += 1
        # end while
        php_print(" </select></p>\n")
    # end if
    if inputs_["show_summary"]:
        php_print(" <p><input id=\"rss-show-summary-")
        php_print(esc_number_)
        php_print("\" name=\"widget-rss[")
        php_print(esc_number_)
        php_print("][show_summary]\" type=\"checkbox\" value=\"1\" ")
        checked(args_["show_summary"])
        php_print(" />\n    <label for=\"rss-show-summary-")
        php_print(esc_number_)
        php_print("\">")
        _e("Display item content?")
        php_print("</label></p>\n")
    # end if
    if inputs_["show_author"]:
        php_print(" <p><input id=\"rss-show-author-")
        php_print(esc_number_)
        php_print("\" name=\"widget-rss[")
        php_print(esc_number_)
        php_print("][show_author]\" type=\"checkbox\" value=\"1\" ")
        checked(args_["show_author"])
        php_print(" />\n    <label for=\"rss-show-author-")
        php_print(esc_number_)
        php_print("\">")
        _e("Display item author if available?")
        php_print("</label></p>\n")
    # end if
    if inputs_["show_date"]:
        php_print(" <p><input id=\"rss-show-date-")
        php_print(esc_number_)
        php_print("\" name=\"widget-rss[")
        php_print(esc_number_)
        php_print("][show_date]\" type=\"checkbox\" value=\"1\" ")
        checked(args_["show_date"])
        php_print("/>\n <label for=\"rss-show-date-")
        php_print(esc_number_)
        php_print("\">")
        _e("Display item date?")
        php_print("</label></p>\n   ")
    # end if
    for input_ in php_array_keys(default_inputs_):
        if "hidden" == inputs_[input_]:
            id_ = php_str_replace("_", "-", input_)
            php_print("<input type=\"hidden\" id=\"rss-")
            php_print(esc_attr(id_))
            php_print("-")
            php_print(esc_number_)
            php_print("\" name=\"widget-rss[")
            php_print(esc_number_)
            php_print("][")
            php_print(esc_attr(input_))
            php_print("]\" value=\"")
            php_print(esc_attr(args_[input_]))
            php_print("\" />\n      ")
        # end if
    # end for
# end def wp_widget_rss_form
#// 
#// Process RSS feed widget data and optionally retrieve feed items.
#// 
#// The feed widget can not have more than 20 items or it will reset back to the
#// default, which is 10.
#// 
#// The resulting array has the feed title, feed url, feed link (from channel),
#// feed items, error (if any), and whether to show summary, author, and date.
#// All respectively in the order of the array elements.
#// 
#// @since 2.5.0
#// 
#// @param array $widget_rss RSS widget feed data. Expects unescaped data.
#// @param bool $check_feed Optional, default is true. Whether to check feed for errors.
#// @return array
#//
def wp_widget_rss_process(widget_rss_=None, check_feed_=None, *_args_):
    if check_feed_ is None:
        check_feed_ = True
    # end if
    
    items_ = php_int(widget_rss_["items"])
    if items_ < 1 or 20 < items_:
        items_ = 10
    # end if
    url_ = esc_url_raw(strip_tags(widget_rss_["url"]))
    title_ = php_trim(strip_tags(widget_rss_["title"])) if (php_isset(lambda : widget_rss_["title"])) else ""
    show_summary_ = php_int(widget_rss_["show_summary"]) if (php_isset(lambda : widget_rss_["show_summary"])) else 0
    show_author_ = php_int(widget_rss_["show_author"]) if (php_isset(lambda : widget_rss_["show_author"])) else 0
    show_date_ = php_int(widget_rss_["show_date"]) if (php_isset(lambda : widget_rss_["show_date"])) else 0
    if check_feed_:
        rss_ = fetch_feed(url_)
        error_ = False
        link_ = ""
        if is_wp_error(rss_):
            error_ = rss_.get_error_message()
        else:
            link_ = esc_url(strip_tags(rss_.get_permalink()))
            while True:
                
                if not (php_stristr(link_, "http") != link_):
                    break
                # end if
                link_ = php_substr(link_, 1)
            # end while
            rss_.__del__()
            rss_ = None
        # end if
    # end if
    return php_compact("title", "url", "link", "items", "error", "show_summary", "show_author", "show_date")
# end def wp_widget_rss_process
#// 
#// Registers all of the default WordPress widgets on startup.
#// 
#// Calls {@see 'widgets_init'} action after all of the WordPress widgets have been registered.
#// 
#// @since 2.2.0
#//
def wp_widgets_init(*_args_):
    
    
    if (not is_blog_installed()):
        return
    # end if
    register_widget("WP_Widget_Pages")
    register_widget("WP_Widget_Calendar")
    register_widget("WP_Widget_Archives")
    if get_option("link_manager_enabled"):
        register_widget("WP_Widget_Links")
    # end if
    register_widget("WP_Widget_Media_Audio")
    register_widget("WP_Widget_Media_Image")
    register_widget("WP_Widget_Media_Gallery")
    register_widget("WP_Widget_Media_Video")
    register_widget("WP_Widget_Meta")
    register_widget("WP_Widget_Search")
    register_widget("WP_Widget_Text")
    register_widget("WP_Widget_Categories")
    register_widget("WP_Widget_Recent_Posts")
    register_widget("WP_Widget_Recent_Comments")
    register_widget("WP_Widget_RSS")
    register_widget("WP_Widget_Tag_Cloud")
    register_widget("WP_Nav_Menu_Widget")
    register_widget("WP_Widget_Custom_HTML")
    #// 
    #// Fires after all default WordPress widgets have been registered.
    #// 
    #// @since 2.2.0
    #//
    do_action("widgets_init")
# end def wp_widgets_init
