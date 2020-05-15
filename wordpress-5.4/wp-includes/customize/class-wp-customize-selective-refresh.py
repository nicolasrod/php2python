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
#// Customize API: WP_Customize_Selective_Refresh class
#// 
#// @package WordPress
#// @subpackage Customize
#// @since 4.5.0
#// 
#// 
#// Core Customizer class for implementing selective refresh.
#// 
#// @since 4.5.0
#//
class WP_Customize_Selective_Refresh():
    RENDER_QUERY_VAR = "wp_customize_render_partials"
    manager = Array()
    partials = Array()
    triggered_errors = Array()
    current_partial_id = Array()
    #// 
    #// Plugin bootstrap for Partial Refresh functionality.
    #// 
    #// @since 4.5.0
    #// 
    #// @param WP_Customize_Manager $manager Customizer bootstrap instance.
    #//
    def __init__(self, manager=None):
        
        self.manager = manager
        php_include_file(ABSPATH + WPINC + "/customize/class-wp-customize-partial.php", once=True)
        add_action("customize_preview_init", Array(self, "init_preview"))
    # end def __init__
    #// 
    #// Retrieves the registered partials.
    #// 
    #// @since 4.5.0
    #// 
    #// @return array Partials.
    #//
    def partials(self):
        
        return self.partials
    # end def partials
    #// 
    #// Adds a partial.
    #// 
    #// @since 4.5.0
    #// 
    #// @param WP_Customize_Partial|string $id   Customize Partial object, or Panel ID.
    #// @param array                       $args {
    #// Optional. Array of properties for the new Partials object. Default empty array.
    #// 
    #// @type string   $type                  Type of the partial to be created.
    #// @type string   $selector              The jQuery selector to find the container element for the partial, that is, a partial's placement.
    #// @type array    $settings              IDs for settings tied to the partial.
    #// @type string   $primary_setting       The ID for the setting that this partial is primarily responsible for
    #// rendering. If not supplied, it will default to the ID of the first setting.
    #// @type string   $capability            Capability required to edit this partial.
    #// Normally this is empty and the capability is derived from the capabilities
    #// of the associated `$settings`.
    #// @type callable $render_callback       Render callback.
    #// Callback is called with one argument, the instance of WP_Customize_Partial.
    #// The callback can either echo the partial or return the partial as a string,
    #// or return false if error.
    #// @type bool     $container_inclusive   Whether the container element is included in the partial, or if only
    #// the contents are rendered.
    #// @type bool     $fallback_refresh      Whether to refresh the entire preview in case a partial cannot be refreshed.
    #// A partial render is considered a failure if the render_callback returns
    #// false.
    #// }
    #// @return WP_Customize_Partial             The instance of the panel that was added.
    #//
    def add_partial(self, id=None, args=Array()):
        
        if type(id).__name__ == "WP_Customize_Partial":
            partial = id
        else:
            class_ = "WP_Customize_Partial"
            #// This filter is documented in wp-includes/customize/class-wp-customize-selective-refresh.php
            args = apply_filters("customize_dynamic_partial_args", args, id)
            #// This filter is documented in wp-includes/customize/class-wp-customize-selective-refresh.php
            class_ = apply_filters("customize_dynamic_partial_class", class_, id, args)
            partial = php_new_class(class_, lambda : {**locals(), **globals()}[class_](self, id, args))
        # end if
        self.partials[partial.id] = partial
        return partial
    # end def add_partial
    #// 
    #// Retrieves a partial.
    #// 
    #// @since 4.5.0
    #// 
    #// @param string $id Customize Partial ID.
    #// @return WP_Customize_Partial|null The partial, if set. Otherwise null.
    #//
    def get_partial(self, id=None):
        
        if (php_isset(lambda : self.partials[id])):
            return self.partials[id]
        else:
            return None
        # end if
    # end def get_partial
    #// 
    #// Removes a partial.
    #// 
    #// @since 4.5.0
    #// 
    #// @param string $id Customize Partial ID.
    #//
    def remove_partial(self, id=None):
        
        self.partials[id] = None
    # end def remove_partial
    #// 
    #// Initializes the Customizer preview.
    #// 
    #// @since 4.5.0
    #//
    def init_preview(self):
        
        add_action("template_redirect", Array(self, "handle_render_partials_request"))
        add_action("wp_enqueue_scripts", Array(self, "enqueue_preview_scripts"))
    # end def init_preview
    #// 
    #// Enqueues preview scripts.
    #// 
    #// @since 4.5.0
    #//
    def enqueue_preview_scripts(self):
        
        wp_enqueue_script("customize-selective-refresh")
        add_action("wp_footer", Array(self, "export_preview_data"), 1000)
    # end def enqueue_preview_scripts
    #// 
    #// Exports data in preview after it has finished rendering so that partials can be added at runtime.
    #// 
    #// @since 4.5.0
    #//
    def export_preview_data(self):
        
        partials = Array()
        for partial in self.partials():
            if partial.check_capabilities():
                partials[partial.id] = partial.json()
            # end if
        # end for
        switched_locale = switch_to_locale(get_user_locale())
        l10n = Array({"shiftClickToEdit": __("Shift-click to edit this element."), "clickEditMenu": __("Click to edit this menu."), "clickEditWidget": __("Click to edit this widget."), "clickEditTitle": __("Click to edit the site title."), "clickEditMisc": __("Click to edit this element."), "badDocumentWrite": php_sprintf(__("%s is forbidden"), "document.write()")})
        if switched_locale:
            restore_previous_locale()
        # end if
        exports = Array({"partials": partials, "renderQueryVar": self.RENDER_QUERY_VAR, "l10n": l10n})
        #// Export data to JS.
        php_print(php_sprintf("<script>var _customizePartialRefreshExports = %s;</script>", wp_json_encode(exports)))
    # end def export_preview_data
    #// 
    #// Registers dynamically-created partials.
    #// 
    #// @since 4.5.0
    #// 
    #// @see WP_Customize_Manager::add_dynamic_settings()
    #// 
    #// @param string[] $partial_ids Array of the partial IDs to add.
    #// @return WP_Customize_Partial[] Array of added WP_Customize_Partial instances.
    #//
    def add_dynamic_partials(self, partial_ids=None):
        
        new_partials = Array()
        for partial_id in partial_ids:
            #// Skip partials already created.
            partial = self.get_partial(partial_id)
            if partial:
                continue
            # end if
            partial_args = False
            partial_class = "WP_Customize_Partial"
            #// 
            #// Filters a dynamic partial's constructor arguments.
            #// 
            #// For a dynamic partial to be registered, this filter must be employed
            #// to override the default false value with an array of args to pass to
            #// the WP_Customize_Partial constructor.
            #// 
            #// @since 4.5.0
            #// 
            #// @param false|array $partial_args The arguments to the WP_Customize_Partial constructor.
            #// @param string      $partial_id   ID for dynamic partial.
            #//
            partial_args = apply_filters("customize_dynamic_partial_args", partial_args, partial_id)
            if False == partial_args:
                continue
            # end if
            #// 
            #// Filters the class used to construct partials.
            #// 
            #// Allow non-statically created partials to be constructed with custom WP_Customize_Partial subclass.
            #// 
            #// @since 4.5.0
            #// 
            #// @param string $partial_class WP_Customize_Partial or a subclass.
            #// @param string $partial_id    ID for dynamic partial.
            #// @param array  $partial_args  The arguments to the WP_Customize_Partial constructor.
            #//
            partial_class = apply_filters("customize_dynamic_partial_class", partial_class, partial_id, partial_args)
            partial = php_new_class(partial_class, lambda : {**locals(), **globals()}[partial_class](self, partial_id, partial_args))
            self.add_partial(partial)
            new_partials[-1] = partial
        # end for
        return new_partials
    # end def add_dynamic_partials
    #// 
    #// Checks whether the request is for rendering partials.
    #// 
    #// Note that this will not consider whether the request is authorized or valid,
    #// just that essentially the route is a match.
    #// 
    #// @since 4.5.0
    #// 
    #// @return bool Whether the request is for rendering partials.
    #//
    def is_render_partials_request(self):
        
        return (not php_empty(lambda : PHP_POST[self.RENDER_QUERY_VAR]))
    # end def is_render_partials_request
    #// 
    #// Handles PHP errors triggered during rendering the partials.
    #// 
    #// These errors will be relayed back to the client in the Ajax response.
    #// 
    #// @since 4.5.0
    #// 
    #// @param int    $errno   Error number.
    #// @param string $errstr  Error string.
    #// @param string $errfile Error file.
    #// @param string $errline Error line.
    #// @return true Always true.
    #//
    def handle_error(self, errno=None, errstr=None, errfile=None, errline=None):
        
        self.triggered_errors[-1] = Array({"partial": self.current_partial_id, "error_number": errno, "error_string": errstr, "error_file": errfile, "error_line": errline})
        return True
    # end def handle_error
    #// 
    #// Handles the Ajax request to return the rendered partials for the requested placements.
    #// 
    #// @since 4.5.0
    #//
    def handle_render_partials_request(self):
        
        if (not self.is_render_partials_request()):
            return
        # end if
        #// 
        #// Note that is_customize_preview() returning true will entail that the
        #// user passed the 'customize' capability check and the nonce check, since
        #// WP_Customize_Manager::setup_theme() is where the previewing flag is set.
        #//
        if (not is_customize_preview()):
            wp_send_json_error("expected_customize_preview", 403)
        elif (not (php_isset(lambda : PHP_POST["partials"]))):
            wp_send_json_error("missing_partials", 400)
        # end if
        #// Ensure that doing selective refresh on 404 template doesn't result in fallback rendering behavior (full refreshes).
        status_header(200)
        partials = php_json_decode(wp_unslash(PHP_POST["partials"]), True)
        if (not php_is_array(partials)):
            wp_send_json_error("malformed_partials")
        # end if
        self.add_dynamic_partials(php_array_keys(partials))
        #// 
        #// Fires immediately before partials are rendered.
        #// 
        #// Plugins may do things like call wp_enqueue_scripts() and gather a list of the scripts
        #// and styles which may get enqueued in the response.
        #// 
        #// @since 4.5.0
        #// 
        #// @param WP_Customize_Selective_Refresh $this     Selective refresh component.
        #// @param array                          $partials Placements' context data for the partials rendered in the request.
        #// The array is keyed by partial ID, with each item being an array of
        #// the placements' context data.
        #//
        do_action("customize_render_partials_before", self, partials)
        set_error_handler(Array(self, "handle_error"), php_error_reporting())
        contents = Array()
        for partial_id,container_contexts in partials:
            self.current_partial_id = partial_id
            if (not php_is_array(container_contexts)):
                wp_send_json_error("malformed_container_contexts")
            # end if
            partial = self.get_partial(partial_id)
            if (not partial) or (not partial.check_capabilities()):
                contents[partial_id] = None
                continue
            # end if
            contents[partial_id] = Array()
            #// @todo The array should include not only the contents, but also whether the container is included?
            if php_empty(lambda : container_contexts):
                #// Since there are no container contexts, render just once.
                contents[partial_id][-1] = partial.render(None)
            else:
                for container_context in container_contexts:
                    contents[partial_id][-1] = partial.render(container_context)
                # end for
            # end if
        # end for
        self.current_partial_id = None
        restore_error_handler()
        #// 
        #// Fires immediately after partials are rendered.
        #// 
        #// Plugins may do things like call wp_footer() to scrape scripts output and return them
        #// via the {@see 'customize_render_partials_response'} filter.
        #// 
        #// @since 4.5.0
        #// 
        #// @param WP_Customize_Selective_Refresh $this     Selective refresh component.
        #// @param array                          $partials Placements' context data for the partials rendered in the request.
        #// The array is keyed by partial ID, with each item being an array of
        #// the placements' context data.
        #//
        do_action("customize_render_partials_after", self, partials)
        response = Array({"contents": contents})
        if php_defined("WP_DEBUG_DISPLAY") and WP_DEBUG_DISPLAY:
            response["errors"] = self.triggered_errors
        # end if
        setting_validities = self.manager.validate_setting_values(self.manager.unsanitized_post_values())
        exported_setting_validities = php_array_map(Array(self.manager, "prepare_setting_validity_for_js"), setting_validities)
        response["setting_validities"] = exported_setting_validities
        #// 
        #// Filters the response from rendering the partials.
        #// 
        #// Plugins may use this filter to inject `$scripts` and `$styles`, which are dependencies
        #// for the partials being rendered. The response data will be available to the client via
        #// the `render-partials-response` JS event, so the client can then inject the scripts and
        #// styles into the DOM if they have not already been enqueued there.
        #// 
        #// If plugins do this, they'll need to take care for any scripts that do `document.write()`
        #// and make sure that these are not injected, or else to override the function to no-op,
        #// or else the page will be destroyed.
        #// 
        #// Plugins should be aware that `$scripts` and `$styles` may eventually be included by
        #// default in the response.
        #// 
        #// @since 4.5.0
        #// 
        #// @param array $response {
        #// Response.
        #// 
        #// @type array $contents Associative array mapping a partial ID its corresponding array of contents
        #// for the containers requested.
        #// @type array $errors   List of errors triggered during rendering of partials, if `WP_DEBUG_DISPLAY`
        #// is enabled.
        #// }
        #// @param WP_Customize_Selective_Refresh $this     Selective refresh component.
        #// @param array                          $partials Placements' context data for the partials rendered in the request.
        #// The array is keyed by partial ID, with each item being an array of
        #// the placements' context data.
        #//
        response = apply_filters("customize_render_partials_response", response, self, partials)
        wp_send_json_success(response)
    # end def handle_render_partials_request
# end class WP_Customize_Selective_Refresh
