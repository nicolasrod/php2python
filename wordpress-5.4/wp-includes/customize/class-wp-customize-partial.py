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
    #// 
    #// Component.
    #// 
    #// @since 4.5.0
    #// @var WP_Customize_Selective_Refresh
    #//
    component = Array()
    #// 
    #// Unique identifier for the partial.
    #// 
    #// If the partial is used to display a single setting, this would generally
    #// be the same as the associated setting's ID.
    #// 
    #// @since 4.5.0
    #// @var string
    #//
    id = Array()
    #// 
    #// Parsed ID.
    #// 
    #// @since 4.5.0
    #// @var array {
    #// @type string $base ID base.
    #// @type array  $keys Keys for multidimensional.
    #// }
    #//
    id_data = Array()
    #// 
    #// Type of this partial.
    #// 
    #// @since 4.5.0
    #// @var string
    #//
    type = "default"
    #// 
    #// The jQuery selector to find the container element for the partial.
    #// 
    #// @since 4.5.0
    #// @var string
    #//
    selector = Array()
    #// 
    #// IDs for settings tied to the partial.
    #// 
    #// @since 4.5.0
    #// @var array
    #//
    settings = Array()
    #// 
    #// The ID for the setting that this partial is primarily responsible for rendering.
    #// 
    #// If not supplied, it will default to the ID of the first setting.
    #// 
    #// @since 4.5.0
    #// @var string
    #//
    primary_setting = Array()
    #// 
    #// Capability required to edit this partial.
    #// 
    #// Normally this is empty and the capability is derived from the capabilities
    #// of the associated `$settings`.
    #// 
    #// @since 4.5.0
    #// @var string
    #//
    capability = Array()
    #// 
    #// Render callback.
    #// 
    #// @since 4.5.0
    #// @see WP_Customize_Partial::render()
    #// @var callable Callback is called with one argument, the instance of
    #// WP_Customize_Partial. The callback can either echo the
    #// partial or return the partial as a string, or return false if error.
    #//
    render_callback = Array()
    #// 
    #// Whether the container element is included in the partial, or if only the contents are rendered.
    #// 
    #// @since 4.5.0
    #// @var bool
    #//
    container_inclusive = False
    #// 
    #// Whether to refresh the entire preview in case a partial cannot be refreshed.
    #// 
    #// A partial render is considered a failure if the render_callback returns false.
    #// 
    #// @since 4.5.0
    #// @var bool
    #//
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
    def __init__(self, component_=None, id_=None, args_=None):
        if args_ is None:
            args_ = Array()
        # end if
        
        keys_ = php_array_keys(get_object_vars(self))
        for key_ in keys_:
            if (php_isset(lambda : args_[key_])):
                self.key_ = args_[key_]
            # end if
        # end for
        self.component = component_
        self.id = id_
        self.id_data["keys"] = php_preg_split("/\\[/", php_str_replace("]", "", self.id))
        self.id_data["base"] = php_array_shift(self.id_data["keys"])
        if php_empty(lambda : self.render_callback):
            self.render_callback = Array(self, "render_callback")
        # end if
        #// Process settings.
        if (not (php_isset(lambda : self.settings))):
            self.settings = Array(id_)
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
    def render(self, container_context_=None):
        if container_context_ is None:
            container_context_ = Array()
        # end if
        
        partial_ = self
        rendered_ = False
        if (not php_empty(lambda : self.render_callback)):
            ob_start()
            return_render_ = php_call_user_func(self.render_callback, self, container_context_)
            ob_render_ = ob_get_clean()
            if None != return_render_ and "" != ob_render_:
                _doing_it_wrong(inspect.currentframe().f_code.co_name, __("Partial render must echo the content or return the content string (or array), but not both."), "4.5.0")
            # end if
            #// 
            #// Note that the string return takes precedence because the $ob_render may just\
#// include PHP warnings or notices.
            #//
            rendered_ = return_render_ if None != return_render_ else ob_render_
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
        rendered_ = apply_filters("customize_partial_render", rendered_, partial_, container_context_)
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
        rendered_ = apply_filters(str("customize_partial_render_") + str(partial_.id), rendered_, partial_, container_context_)
        return rendered_
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
    def render_callback(self, partial_=None, context_=None):
        if context_ is None:
            context_ = Array()
        # end if
        
        partial_ = None
        context_ = None
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
        
        
        exports_ = Array({"settings": self.settings, "primarySetting": self.primary_setting, "selector": self.selector, "type": self.type, "fallbackRefresh": self.fallback_refresh, "containerInclusive": self.container_inclusive})
        return exports_
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
        for setting_id_ in self.settings:
            setting_ = self.component.manager.get_setting(setting_id_)
            if (not setting_) or (not setting_.check_capabilities()):
                return False
            # end if
        # end for
        return True
    # end def check_capabilities
# end class WP_Customize_Partial
