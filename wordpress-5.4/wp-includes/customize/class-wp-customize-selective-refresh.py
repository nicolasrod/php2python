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
    #// 
    #// Customize manager.
    #// 
    #// @since 4.5.0
    #// @var WP_Customize_Manager
    #//
    manager = Array()
    #// 
    #// Registered instances of WP_Customize_Partial.
    #// 
    #// @since 4.5.0
    #// @var WP_Customize_Partial[]
    #//
    partials = Array()
    #// 
    #// Log of errors triggered when partials are rendered.
    #// 
    #// @since 4.5.0
    #// @var array
    #//
    triggered_errors = Array()
    #// 
    #// Keep track of the current partial being rendered.
    #// 
    #// @since 4.5.0
    #// @var string|null
    #//
    current_partial_id = Array()
    #// 
    #// Plugin bootstrap for Partial Refresh functionality.
    #// 
    #// @since 4.5.0
    #// 
    #// @param WP_Customize_Manager $manager Customizer bootstrap instance.
    #//
    def __init__(self, manager_=None):
        
        
        self.manager = manager_
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
    def add_partial(self, id_=None, args_=None):
        if args_ is None:
            args_ = Array()
        # end if
        
        if type(id_).__name__ == "WP_Customize_Partial":
            partial_ = id_
        else:
            class_ = "WP_Customize_Partial"
            #// This filter is documented in wp-includes/customize/class-wp-customize-selective-refresh.php
            args_ = apply_filters("customize_dynamic_partial_args", args_, id_)
            #// This filter is documented in wp-includes/customize/class-wp-customize-selective-refresh.php
            class_ = apply_filters("customize_dynamic_partial_class", class_, id_, args_)
            partial_ = php_new_class(class_, lambda : {**locals(), **globals()}[class_](self, id_, args_))
        # end if
        self.partials[partial_.id] = partial_
        return partial_
    # end def add_partial
    #// 
    #// Retrieves a partial.
    #// 
    #// @since 4.5.0
    #// 
    #// @param string $id Customize Partial ID.
    #// @return WP_Customize_Partial|null The partial, if set. Otherwise null.
    #//
    def get_partial(self, id_=None):
        
        
        if (php_isset(lambda : self.partials[id_])):
            return self.partials[id_]
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
    def remove_partial(self, id_=None):
        
        
        self.partials[id_] = None
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
        
        
        partials_ = Array()
        for partial_ in self.partials():
            if partial_.check_capabilities():
                partials_[partial_.id] = partial_.json()
            # end if
        # end for
        switched_locale_ = switch_to_locale(get_user_locale())
        l10n_ = Array({"shiftClickToEdit": __("Shift-click to edit this element."), "clickEditMenu": __("Click to edit this menu."), "clickEditWidget": __("Click to edit this widget."), "clickEditTitle": __("Click to edit the site title."), "clickEditMisc": __("Click to edit this element."), "badDocumentWrite": php_sprintf(__("%s is forbidden"), "document.write()")})
        if switched_locale_:
            restore_previous_locale()
        # end if
        exports_ = Array({"partials": partials_, "renderQueryVar": self.RENDER_QUERY_VAR, "l10n": l10n_})
        #// Export data to JS.
        php_print(php_sprintf("<script>var _customizePartialRefreshExports = %s;</script>", wp_json_encode(exports_)))
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
    def add_dynamic_partials(self, partial_ids_=None):
        
        
        new_partials_ = Array()
        for partial_id_ in partial_ids_:
            #// Skip partials already created.
            partial_ = self.get_partial(partial_id_)
            if partial_:
                continue
            # end if
            partial_args_ = False
            partial_class_ = "WP_Customize_Partial"
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
            partial_args_ = apply_filters("customize_dynamic_partial_args", partial_args_, partial_id_)
            if False == partial_args_:
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
            partial_class_ = apply_filters("customize_dynamic_partial_class", partial_class_, partial_id_, partial_args_)
            partial_ = php_new_class(partial_class_, lambda : {**locals(), **globals()}[partial_class_](self, partial_id_, partial_args_))
            self.add_partial(partial_)
            new_partials_[-1] = partial_
        # end for
        return new_partials_
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
    def handle_error(self, errno_=None, errstr_=None, errfile_=None, errline_=None):
        if errfile_ is None:
            errfile_ = None
        # end if
        if errline_ is None:
            errline_ = None
        # end if
        
        self.triggered_errors[-1] = Array({"partial": self.current_partial_id, "error_number": errno_, "error_string": errstr_, "error_file": errfile_, "error_line": errline_})
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
        partials_ = php_json_decode(wp_unslash(PHP_POST["partials"]), True)
        if (not php_is_array(partials_)):
            wp_send_json_error("malformed_partials")
        # end if
        self.add_dynamic_partials(php_array_keys(partials_))
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
        do_action("customize_render_partials_before", self, partials_)
        set_error_handler(Array(self, "handle_error"), php_error_reporting())
        contents_ = Array()
        for partial_id_,container_contexts_ in partials_.items():
            self.current_partial_id = partial_id_
            if (not php_is_array(container_contexts_)):
                wp_send_json_error("malformed_container_contexts")
            # end if
            partial_ = self.get_partial(partial_id_)
            if (not partial_) or (not partial_.check_capabilities()):
                contents_[partial_id_] = None
                continue
            # end if
            contents_[partial_id_] = Array()
            #// @todo The array should include not only the contents, but also whether the container is included?
            if php_empty(lambda : container_contexts_):
                #// Since there are no container contexts, render just once.
                contents_[partial_id_][-1] = partial_.render(None)
            else:
                for container_context_ in container_contexts_:
                    contents_[partial_id_][-1] = partial_.render(container_context_)
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
        do_action("customize_render_partials_after", self, partials_)
        response_ = Array({"contents": contents_})
        if php_defined("WP_DEBUG_DISPLAY") and WP_DEBUG_DISPLAY:
            response_["errors"] = self.triggered_errors
        # end if
        setting_validities_ = self.manager.validate_setting_values(self.manager.unsanitized_post_values())
        exported_setting_validities_ = php_array_map(Array(self.manager, "prepare_setting_validity_for_js"), setting_validities_)
        response_["setting_validities"] = exported_setting_validities_
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
        response_ = apply_filters("customize_render_partials_response", response_, self, partials_)
        wp_send_json_success(response_)
    # end def handle_render_partials_request
# end class WP_Customize_Selective_Refresh
