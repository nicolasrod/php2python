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
#// Customize API: WP_Customize_Partial class
#// 
#// @package WordPress
#// @subpackage Customize
#// @since 4.5.0
#// 
#// 
#// Core Customizer class for implementing selective refresh partials.
#// 
#// Representation of a rendered region in the previewed page that gets
#// selectively refreshed when an associated setting is changed.
#// This class is analogous of WP_Customize_Control.
#// 
#// @since 4.5.0
#//
class WP_Customize_Partial():
    component = Array()
    id = Array()
    id_data = Array()
    type = "default"
    selector = Array()
    settings = Array()
    primary_setting = Array()
    capability = Array()
    render_callback = Array()
    container_inclusive = False
    fallback_refresh = True
    #// 
    #// Constructor.
    #// 
    #// Supplied `$args` override class property defaults.
    #// 
    #// If `$args['settings']` is not defined, use the $id as the setting ID.
    #// 
    #// @since 4.5.0
    #// 
    #// @param WP_Customize_Selective_Refresh $component Customize Partial Refresh plugin instance.
    #// @param string                         $id        Control ID.
    #// @param array                          $args      {
    #// Optional. Arguments to override class property defaults.
    #// 
    #// @type array|string $settings All settings IDs tied to the partial. If undefined, `$id` will be used.
    #// }
    #//
    def __init__(self, component=None, id=None, args=Array()):
        
        keys = php_array_keys(get_object_vars(self))
        for key in keys:
            if (php_isset(lambda : args[key])):
                self.key = args[key]
            # end if
        # end for
        self.component = component
        self.id = id
        self.id_data["keys"] = php_preg_split("/\\[/", php_str_replace("]", "", self.id))
        self.id_data["base"] = php_array_shift(self.id_data["keys"])
        if php_empty(lambda : self.render_callback):
            self.render_callback = Array(self, "render_callback")
        # end if
        #// Process settings.
        if (not (php_isset(lambda : self.settings))):
            self.settings = Array(id)
        elif php_is_string(self.settings):
            self.settings = Array(self.settings)
        # end if
        if php_empty(lambda : self.primary_setting):
            self.primary_setting = current(self.settings)
        # end if
    # end def __init__
    #// 
    #// Retrieves parsed ID data for multidimensional setting.
    #// 
    #// @since 4.5.0
    #// 
    #// @return array {
    #// ID data for multidimensional partial.
    #// 
    #// @type string $base ID base.
    #// @type array  $keys Keys for multidimensional array.
    #// }
    #//
    def id_data(self):
        
        return self.id_data
    # end def id_data
    #// 
    #// Renders the template partial involving the associated settings.
    #// 
    #// @since 4.5.0
    #// 
    #// @param array $container_context Optional. Array of context data associated with the target container (placement).
    #// Default empty array.
    #// @return string|array|false The rendered partial as a string, raw data array (for client-side JS template),
    #// or false if no render applied.
    #//
    def render(self, container_context=Array()):
        
        partial = self
        rendered = False
        if (not php_empty(lambda : self.render_callback)):
            ob_start()
            return_render = php_call_user_func(self.render_callback, self, container_context)
            ob_render = ob_get_clean()
            if None != return_render and "" != ob_render:
                _doing_it_wrong(__FUNCTION__, __("Partial render must echo the content or return the content string (or array), but not both."), "4.5.0")
            # end if
            #// 
            #// Note that the string return takes precedence because the $ob_render may just\
#// include PHP warnings or notices.
            #//
            rendered = return_render if None != return_render else ob_render
        # end if
        #// 
        #// Filters partial rendering.
        #// 
        #// @since 4.5.0
        #// 
        #// @param string|array|false   $rendered          The partial value. Default false.
        #// @param WP_Customize_Partial $partial           WP_Customize_Setting instance.
        #// @param array                $container_context Optional array of context data associated with
        #// the target container.
        #//
        rendered = apply_filters("customize_partial_render", rendered, partial, container_context)
        #// 
        #// Filters partial rendering for a specific partial.
        #// 
        #// The dynamic portion of the hook name, `$partial->ID` refers to the partial ID.
        #// 
        #// @since 4.5.0
        #// 
        #// @param string|array|false   $rendered          The partial value. Default false.
        #// @param WP_Customize_Partial $partial           WP_Customize_Setting instance.
        #// @param array                $container_context Optional array of context data associated with
        #// the target container.
        #//
        rendered = apply_filters(str("customize_partial_render_") + str(partial.id), rendered, partial, container_context)
        return rendered
    # end def render
    #// 
    #// Default callback used when invoking WP_Customize_Control::render().
    #// 
    #// Note that this method may echo the partial *or* return the partial as
    #// a string or array, but not both. Output buffering is performed when this
    #// is called. Subclasses can override this with their specific logic, or they
    #// may provide an 'render_callback' argument to the constructor.
    #// 
    #// This method may return an HTML string for straight DOM injection, or it
    #// may return an array for supporting Partial JS subclasses to render by
    #// applying to client-side templating.
    #// 
    #// @since 4.5.0
    #// 
    #// @param WP_Customize_Partial $partial Partial.
    #// @param array                $context Context.
    #// @return string|array|false
    #//
    def render_callback(self, partial=None, context=Array()):
        
        partial = None
        context = None
        return False
    # end def render_callback
    #// 
    #// Retrieves the data to export to the client via JSON.
    #// 
    #// @since 4.5.0
    #// 
    #// @return array Array of parameters passed to the JavaScript.
    #//
    def json(self):
        
        exports = Array({"settings": self.settings, "primarySetting": self.primary_setting, "selector": self.selector, "type": self.type, "fallbackRefresh": self.fallback_refresh, "containerInclusive": self.container_inclusive})
        return exports
    # end def json
    #// 
    #// Checks if the user can refresh this partial.
    #// 
    #// Returns false if the user cannot manipulate one of the associated settings,
    #// or if one of the associated settings does not exist.
    #// 
    #// @since 4.5.0
    #// 
    #// @return bool False if user can't edit one of the related settings,
    #// or if one of the associated settings does not exist.
    #//
    def check_capabilities(self):
        
        if (not php_empty(lambda : self.capability)) and (not current_user_can(self.capability)):
            return False
        # end if
        for setting_id in self.settings:
            setting = self.component.manager.get_setting(setting_id)
            if (not setting) or (not setting.check_capabilities()):
                return False
            # end if
        # end for
        return True
    # end def check_capabilities
# end class WP_Customize_Partial
