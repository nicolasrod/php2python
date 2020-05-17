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
#// Widget API: WP_Widget_Factory class
#// 
#// @package WordPress
#// @subpackage Widgets
#// @since 4.4.0
#// 
#// 
#// Singleton that registers and instantiates WP_Widget classes.
#// 
#// @since 2.8.0
#// @since 4.4.0 Moved to its own file from wp-includes/widgets.php
#//
class WP_Widget_Factory():
    #// 
    #// Widgets array.
    #// 
    #// @since 2.8.0
    #// @var array
    #//
    widgets = Array()
    #// 
    #// PHP5 constructor.
    #// 
    #// @since 4.3.0
    #//
    def __init__(self):
        
        
        add_action("widgets_init", Array(self, "_register_widgets"), 100)
    # end def __init__
    #// 
    #// PHP4 constructor.
    #// 
    #// @since 2.8.0
    #// @deprecated 4.3.0 Use __construct() instead.
    #// 
    #// @see WP_Widget_Factory::__construct()
    #//
    def wp_widget_factory(self):
        
        
        _deprecated_constructor("WP_Widget_Factory", "4.3.0")
        self.__init__()
    # end def wp_widget_factory
    #// 
    #// Registers a widget subclass.
    #// 
    #// @since 2.8.0
    #// @since 4.6.0 Updated the `$widget` parameter to also accept a WP_Widget instance object
    #// instead of simply a `WP_Widget` subclass name.
    #// 
    #// @param string|WP_Widget $widget Either the name of a `WP_Widget` subclass or an instance of a `WP_Widget` subclass.
    #//
    def register(self, widget_=None):
        
        
        if type(widget_).__name__ == "WP_Widget":
            self.widgets[spl_object_hash(widget_)] = widget_
        else:
            self.widgets[widget_] = php_new_class(widget_, lambda : {**locals(), **globals()}[widget_]())
        # end if
    # end def register
    #// 
    #// Un-registers a widget subclass.
    #// 
    #// @since 2.8.0
    #// @since 4.6.0 Updated the `$widget` parameter to also accept a WP_Widget instance object
    #// instead of simply a `WP_Widget` subclass name.
    #// 
    #// @param string|WP_Widget $widget Either the name of a `WP_Widget` subclass or an instance of a `WP_Widget` subclass.
    #//
    def unregister(self, widget_=None):
        
        
        if type(widget_).__name__ == "WP_Widget":
            self.widgets[spl_object_hash(widget_)] = None
        else:
            self.widgets[widget_] = None
        # end if
    # end def unregister
    #// 
    #// Serves as a utility method for adding widgets to the registered widgets global.
    #// 
    #// @since 2.8.0
    #// 
    #// @global array $wp_registered_widgets
    #//
    def _register_widgets(self):
        
        
        global wp_registered_widgets_
        php_check_if_defined("wp_registered_widgets_")
        keys_ = php_array_keys(self.widgets)
        registered_ = php_array_keys(wp_registered_widgets_)
        registered_ = php_array_map("_get_widget_id_base", registered_)
        for key_ in keys_:
            #// Don't register new widget if old widget with the same id is already registered.
            if php_in_array(self.widgets[key_].id_base, registered_, True):
                self.widgets[key_] = None
                continue
            # end if
            self.widgets[key_]._register()
        # end for
    # end def _register_widgets
# end class WP_Widget_Factory
