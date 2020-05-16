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
#// WordPress Customize Setting classes
#// 
#// @package WordPress
#// @subpackage Customize
#// @since 3.4.0
#// 
#// 
#// Customize Setting class.
#// 
#// Handles saving and sanitizing of settings.
#// 
#// @since 3.4.0
#// @link https://developer.wordpress.org/themes/customize-api
#// 
#// @see WP_Customize_Manager
#//
class WP_Customize_Setting():
    manager = Array()
    id = Array()
    type = "theme_mod"
    capability = "edit_theme_options"
    theme_supports = ""
    default = ""
    transport = "refresh"
    validate_callback = ""
    sanitize_callback = ""
    sanitize_js_callback = ""
    dirty = False
    id_data = Array()
    is_previewed = False
    aggregated_multidimensionals = Array()
    is_multidimensional_aggregated = False
    #// 
    #// Constructor.
    #// 
    #// Any supplied $args override class property defaults.
    #// 
    #// @since 3.4.0
    #// 
    #// @param WP_Customize_Manager $manager Customizer bootstrap instance.
    #// @param string               $id      A specific ID of the setting.
    #// Can be a theme mod or option name.
    #// @param array                $args    {
    #// Optional. Array of properties for the new Setting object. Default empty array.
    #// 
    #// @type string          $type                 Type of the setting. Default 'theme_mod'.
    #// @type string          $capability           Capability required for the setting. Default 'edit_theme_options'
    #// @type string|string[] $theme_supports       Theme features required to support the panel. Default is none.
    #// @type string          $default              Default value for the setting. Default is empty string.
    #// @type string          $transport            Options for rendering the live preview of changes in Customizer.
    #// Using 'refresh' makes the change visible by reloading the whole preview.
    #// Using 'postMessage' allows a custom JavaScript to handle live changes.
    #// Default is 'refresh'.
    #// @type callable        $validate_callback    Server-side validation callback for the setting's value.
    #// @type callable        $sanitize_callback    Callback to filter a Customize setting value in un-slashed form.
    #// @type callable        $sanitize_js_callback Callback to convert a Customize PHP setting value to a value that is
    #// JSON serializable.
    #// @type bool            $dirty                Whether or not the setting is initially dirty when created.
    #// }
    #//
    def __init__(self, manager=None, id=None, args=Array()):
        
        keys = php_array_keys(get_object_vars(self))
        for key in keys:
            if (php_isset(lambda : args[key])):
                self.key = args[key]
            # end if
        # end for
        self.manager = manager
        self.id = id
        #// Parse the ID for array keys.
        self.id_data["keys"] = php_preg_split("/\\[/", php_str_replace("]", "", self.id))
        self.id_data["base"] = php_array_shift(self.id_data["keys"])
        #// Rebuild the ID.
        self.id = self.id_data["base"]
        if (not php_empty(lambda : self.id_data["keys"])):
            self.id += "[" + php_implode("][", self.id_data["keys"]) + "]"
        # end if
        if self.validate_callback:
            add_filter(str("customize_validate_") + str(self.id), self.validate_callback, 10, 3)
        # end if
        if self.sanitize_callback:
            add_filter(str("customize_sanitize_") + str(self.id), self.sanitize_callback, 10, 2)
        # end if
        if self.sanitize_js_callback:
            add_filter(str("customize_sanitize_js_") + str(self.id), self.sanitize_js_callback, 10, 2)
        # end if
        if "option" == self.type or "theme_mod" == self.type:
            #// Other setting types can opt-in to aggregate multidimensional explicitly.
            self.aggregate_multidimensional()
            #// Allow option settings to indicate whether they should be autoloaded.
            if "option" == self.type and (php_isset(lambda : args["autoload"])):
                self.aggregated_multidimensionals[self.type][self.id_data["base"]]["autoload"] = args["autoload"]
            # end if
        # end if
    # end def __init__
    #// 
    #// Get parsed ID data for multidimensional setting.
    #// 
    #// @since 4.4.0
    #// 
    #// @return array {
    #// ID data for multidimensional setting.
    #// 
    #// @type string $base ID base
    #// @type array  $keys Keys for multidimensional array.
    #// }
    #//
    def id_data(self):
        
        return self.id_data
    # end def id_data
    #// 
    #// Set up the setting for aggregated multidimensional values.
    #// 
    #// When a multidimensional setting gets aggregated, all of its preview and update
    #// calls get combined into one call, greatly improving performance.
    #// 
    #// @since 4.4.0
    #//
    def aggregate_multidimensional(self):
        
        id_base = self.id_data["base"]
        if (not (php_isset(lambda : self.aggregated_multidimensionals[self.type]))):
            self.aggregated_multidimensionals[self.type] = Array()
        # end if
        if (not (php_isset(lambda : self.aggregated_multidimensionals[self.type][id_base]))):
            self.aggregated_multidimensionals[self.type][id_base] = Array({"previewed_instances": Array(), "preview_applied_instances": Array(), "root_value": self.get_root_value(Array())})
        # end if
        if (not php_empty(lambda : self.id_data["keys"])):
            #// Note the preview-applied flag is cleared at priority 9 to ensure it is cleared before a deferred-preview runs.
            add_action(str("customize_post_value_set_") + str(self.id), Array(self, "_clear_aggregated_multidimensional_preview_applied_flag"), 9)
            self.is_multidimensional_aggregated = True
        # end if
    # end def aggregate_multidimensional
    #// 
    #// Reset `$aggregated_multidimensionals` static variable.
    #// 
    #// This is intended only for use by unit tests.
    #// 
    #// @since 4.5.0
    #// @ignore
    #//
    @classmethod
    def reset_aggregated_multidimensionals(self):
        
        self.aggregated_multidimensionals = Array()
    # end def reset_aggregated_multidimensionals
    _previewed_blog_id = Array()
    #// 
    #// Return true if the current site is not the same as the previewed site.
    #// 
    #// @since 4.2.0
    #// 
    #// @return bool If preview() has been called.
    #//
    def is_current_blog_previewed(self):
        
        if (not (php_isset(lambda : self._previewed_blog_id))):
            return False
        # end if
        return get_current_blog_id() == self._previewed_blog_id
    # end def is_current_blog_previewed
    _original_value = Array()
    #// 
    #// Add filters to supply the setting's value when accessed.
    #// 
    #// If the setting already has a pre-existing value and there is no incoming
    #// post value for the setting, then this method will short-circuit since
    #// there is no change to preview.
    #// 
    #// @since 3.4.0
    #// @since 4.4.0 Added boolean return value.
    #// 
    #// @return bool False when preview short-circuits due no change needing to be previewed.
    #//
    def preview(self):
        
        if (not (php_isset(lambda : self._previewed_blog_id))):
            self._previewed_blog_id = get_current_blog_id()
        # end if
        #// Prevent re-previewing an already-previewed setting.
        if self.is_previewed:
            return True
        # end if
        id_base = self.id_data["base"]
        is_multidimensional = (not php_empty(lambda : self.id_data["keys"]))
        multidimensional_filter = Array(self, "_multidimensional_preview_filter")
        #// 
        #// Check if the setting has a pre-existing value (an isset check),
        #// and if doesn't have any incoming post value. If both checks are true,
        #// then the preview short-circuits because there is nothing that needs
        #// to be previewed.
        #//
        undefined = php_new_class("stdClass", lambda : stdClass())
        needs_preview = undefined != self.post_value(undefined)
        value = None
        #// Since no post value was defined, check if we have an initial value set.
        if (not needs_preview):
            if self.is_multidimensional_aggregated:
                root = self.aggregated_multidimensionals[self.type][id_base]["root_value"]
                value = self.multidimensional_get(root, self.id_data["keys"], undefined)
            else:
                default = self.default
                self.default = undefined
                #// Temporarily set default to undefined so we can detect if existing value is set.
                value = self.value()
                self.default = default
            # end if
            needs_preview = undefined == value
            pass
        # end if
        #// If the setting does not need previewing now, defer to when it has a value to preview.
        if (not needs_preview):
            if (not has_action(str("customize_post_value_set_") + str(self.id), Array(self, "preview"))):
                add_action(str("customize_post_value_set_") + str(self.id), Array(self, "preview"))
            # end if
            return False
        # end if
        for case in Switch(self.type):
            if case("theme_mod"):
                if (not is_multidimensional):
                    add_filter(str("theme_mod_") + str(id_base), Array(self, "_preview_filter"))
                else:
                    if php_empty(lambda : self.aggregated_multidimensionals[self.type][id_base]["previewed_instances"]):
                        #// Only add this filter once for this ID base.
                        add_filter(str("theme_mod_") + str(id_base), multidimensional_filter)
                    # end if
                    self.aggregated_multidimensionals[self.type][id_base]["previewed_instances"][self.id] = self
                # end if
                break
            # end if
            if case("option"):
                if (not is_multidimensional):
                    add_filter(str("pre_option_") + str(id_base), Array(self, "_preview_filter"))
                else:
                    if php_empty(lambda : self.aggregated_multidimensionals[self.type][id_base]["previewed_instances"]):
                        #// Only add these filters once for this ID base.
                        add_filter(str("option_") + str(id_base), multidimensional_filter)
                        add_filter(str("default_option_") + str(id_base), multidimensional_filter)
                    # end if
                    self.aggregated_multidimensionals[self.type][id_base]["previewed_instances"][self.id] = self
                # end if
                break
            # end if
            if case():
                #// 
                #// Fires when the WP_Customize_Setting::preview() method is called for settings
                #// not handled as theme_mods or options.
                #// 
                #// The dynamic portion of the hook name, `$this->id`, refers to the setting ID.
                #// 
                #// @since 3.4.0
                #// 
                #// @param WP_Customize_Setting $this WP_Customize_Setting instance.
                #//
                do_action(str("customize_preview_") + str(self.id), self)
                #// 
                #// Fires when the WP_Customize_Setting::preview() method is called for settings
                #// not handled as theme_mods or options.
                #// 
                #// The dynamic portion of the hook name, `$this->type`, refers to the setting type.
                #// 
                #// @since 4.1.0
                #// 
                #// @param WP_Customize_Setting $this WP_Customize_Setting instance.
                #//
                do_action(str("customize_preview_") + str(self.type), self)
            # end if
        # end for
        self.is_previewed = True
        return True
    # end def preview
    #// 
    #// Clear out the previewed-applied flag for a multidimensional-aggregated value whenever its post value is updated.
    #// 
    #// This ensures that the new value will get sanitized and used the next time
    #// that `WP_Customize_Setting::_multidimensional_preview_filter()`
    #// is called for this setting.
    #// 
    #// @since 4.4.0
    #// 
    #// @see WP_Customize_Manager::set_post_value()
    #// @see WP_Customize_Setting::_multidimensional_preview_filter()
    #//
    def _clear_aggregated_multidimensional_preview_applied_flag(self):
        
        self.aggregated_multidimensionals[self.type][self.id_data["base"]]["preview_applied_instances"][self.id] = None
    # end def _clear_aggregated_multidimensional_preview_applied_flag
    #// 
    #// Callback function to filter non-multidimensional theme mods and options.
    #// 
    #// If switch_to_blog() was called after the preview() method, and the current
    #// site is now not the same site, then this method does a no-op and returns
    #// the original value.
    #// 
    #// @since 3.4.0
    #// 
    #// @param mixed $original Old value.
    #// @return mixed New or old value.
    #//
    def _preview_filter(self, original=None):
        
        if (not self.is_current_blog_previewed()):
            return original
        # end if
        undefined = php_new_class("stdClass", lambda : stdClass())
        #// Symbol hack.
        post_value = self.post_value(undefined)
        if undefined != post_value:
            value = post_value
        else:
            #// 
            #// Note that we don't use $original here because preview() will
            #// not add the filter in the first place if it has an initial value
            #// and there is no post value.
            #//
            value = self.default
        # end if
        return value
    # end def _preview_filter
    #// 
    #// Callback function to filter multidimensional theme mods and options.
    #// 
    #// For all multidimensional settings of a given type, the preview filter for
    #// the first setting previewed will be used to apply the values for the others.
    #// 
    #// @since 4.4.0
    #// 
    #// @see WP_Customize_Setting::$aggregated_multidimensionals
    #// @param mixed $original Original root value.
    #// @return mixed New or old value.
    #//
    def _multidimensional_preview_filter(self, original=None):
        
        if (not self.is_current_blog_previewed()):
            return original
        # end if
        id_base = self.id_data["base"]
        #// If no settings have been previewed yet (which should not be the case, since $this is), just pass through the original value.
        if php_empty(lambda : self.aggregated_multidimensionals[self.type][id_base]["previewed_instances"]):
            return original
        # end if
        for previewed_setting in self.aggregated_multidimensionals[self.type][id_base]["previewed_instances"]:
            #// Skip applying previewed value for any settings that have already been applied.
            if (not php_empty(lambda : self.aggregated_multidimensionals[self.type][id_base]["preview_applied_instances"][previewed_setting.id])):
                continue
            # end if
            #// Do the replacements of the posted/default sub value into the root value.
            value = previewed_setting.post_value(previewed_setting.default)
            root = self.aggregated_multidimensionals[previewed_setting.type][id_base]["root_value"]
            root = previewed_setting.multidimensional_replace(root, previewed_setting.id_data["keys"], value)
            self.aggregated_multidimensionals[previewed_setting.type][id_base]["root_value"] = root
            #// Mark this setting having been applied so that it will be skipped when the filter is called again.
            self.aggregated_multidimensionals[previewed_setting.type][id_base]["preview_applied_instances"][previewed_setting.id] = True
        # end for
        return self.aggregated_multidimensionals[self.type][id_base]["root_value"]
    # end def _multidimensional_preview_filter
    #// 
    #// Checks user capabilities and theme supports, and then saves
    #// the value of the setting.
    #// 
    #// @since 3.4.0
    #// 
    #// @return void|false False if cap check fails or value isn't set or is invalid.
    #//
    def save(self):
        
        value = self.post_value()
        if (not self.check_capabilities()) or (not (php_isset(lambda : value))):
            return False
        # end if
        id_base = self.id_data["base"]
        #// 
        #// Fires when the WP_Customize_Setting::save() method is called.
        #// 
        #// The dynamic portion of the hook name, `$id_base` refers to
        #// the base slug of the setting name.
        #// 
        #// @since 3.4.0
        #// 
        #// @param WP_Customize_Setting $this WP_Customize_Setting instance.
        #//
        do_action(str("customize_save_") + str(id_base), self)
        self.update(value)
    # end def save
    #// 
    #// Fetch and sanitize the $_POST value for the setting.
    #// 
    #// During a save request prior to save, post_value() provides the new value while value() does not.
    #// 
    #// @since 3.4.0
    #// 
    #// @param mixed $default A default value which is used as a fallback. Default is null.
    #// @return mixed The default value on failure, otherwise the sanitized and validated value.
    #//
    def post_value(self, default=None):
        
        return self.manager.post_value(self, default)
    # end def post_value
    #// 
    #// Sanitize an input.
    #// 
    #// @since 3.4.0
    #// 
    #// @param string|array $value    The value to sanitize.
    #// @return string|array|null|WP_Error Sanitized value, or `null`/`WP_Error` if invalid.
    #//
    def sanitize(self, value=None):
        
        #// 
        #// Filters a Customize setting value in un-slashed form.
        #// 
        #// @since 3.4.0
        #// 
        #// @param mixed                $value Value of the setting.
        #// @param WP_Customize_Setting $this  WP_Customize_Setting instance.
        #//
        return apply_filters(str("customize_sanitize_") + str(self.id), value, self)
    # end def sanitize
    #// 
    #// Validates an input.
    #// 
    #// @since 4.6.0
    #// 
    #// @see WP_REST_Request::has_valid_params()
    #// 
    #// @param mixed $value Value to validate.
    #// @return true|WP_Error True if the input was validated, otherwise WP_Error.
    #//
    def validate(self, value=None):
        
        if is_wp_error(value):
            return value
        # end if
        if is_null(value):
            return php_new_class("WP_Error", lambda : WP_Error("invalid_value", __("Invalid value.")))
        # end if
        validity = php_new_class("WP_Error", lambda : WP_Error())
        #// 
        #// Validates a Customize setting value.
        #// 
        #// Plugins should amend the `$validity` object via its `WP_Error::add()` method.
        #// 
        #// The dynamic portion of the hook name, `$this->ID`, refers to the setting ID.
        #// 
        #// @since 4.6.0
        #// 
        #// @param WP_Error             $validity Filtered from `true` to `WP_Error` when invalid.
        #// @param mixed                $value    Value of the setting.
        #// @param WP_Customize_Setting $this     WP_Customize_Setting instance.
        #//
        validity = apply_filters(str("customize_validate_") + str(self.id), validity, value, self)
        if is_wp_error(validity) and (not validity.has_errors()):
            validity = True
        # end if
        return validity
    # end def validate
    #// 
    #// Get the root value for a setting, especially for multidimensional ones.
    #// 
    #// @since 4.4.0
    #// 
    #// @param mixed $default Value to return if root does not exist.
    #// @return mixed
    #//
    def get_root_value(self, default=None):
        
        id_base = self.id_data["base"]
        if "option" == self.type:
            return get_option(id_base, default)
        elif "theme_mod" == self.type:
            return get_theme_mod(id_base, default)
        else:
            #// 
            #// Any WP_Customize_Setting subclass implementing aggregate multidimensional
            #// will need to override this method to obtain the data from the appropriate
            #// location.
            #//
            return default
        # end if
    # end def get_root_value
    #// 
    #// Set the root value for a setting, especially for multidimensional ones.
    #// 
    #// @since 4.4.0
    #// 
    #// @param mixed $value Value to set as root of multidimensional setting.
    #// @return bool Whether the multidimensional root was updated successfully.
    #//
    def set_root_value(self, value=None):
        
        id_base = self.id_data["base"]
        if "option" == self.type:
            autoload = True
            if (php_isset(lambda : self.aggregated_multidimensionals[self.type][self.id_data["base"]]["autoload"])):
                autoload = self.aggregated_multidimensionals[self.type][self.id_data["base"]]["autoload"]
            # end if
            return update_option(id_base, value, autoload)
        elif "theme_mod" == self.type:
            set_theme_mod(id_base, value)
            return True
        else:
            #// 
            #// Any WP_Customize_Setting subclass implementing aggregate multidimensional
            #// will need to override this method to obtain the data from the appropriate
            #// location.
            #//
            return False
        # end if
    # end def set_root_value
    #// 
    #// Save the value of the setting, using the related API.
    #// 
    #// @since 3.4.0
    #// 
    #// @param mixed $value The value to update.
    #// @return bool The result of saving the value.
    #//
    def update(self, value=None):
        
        id_base = self.id_data["base"]
        if "option" == self.type or "theme_mod" == self.type:
            if (not self.is_multidimensional_aggregated):
                return self.set_root_value(value)
            else:
                root = self.aggregated_multidimensionals[self.type][id_base]["root_value"]
                root = self.multidimensional_replace(root, self.id_data["keys"], value)
                self.aggregated_multidimensionals[self.type][id_base]["root_value"] = root
                return self.set_root_value(root)
            # end if
        else:
            #// 
            #// Fires when the WP_Customize_Setting::update() method is called for settings
            #// not handled as theme_mods or options.
            #// 
            #// The dynamic portion of the hook name, `$this->type`, refers to the type of setting.
            #// 
            #// @since 3.4.0
            #// 
            #// @param mixed                $value Value of the setting.
            #// @param WP_Customize_Setting $this  WP_Customize_Setting instance.
            #//
            do_action(str("customize_update_") + str(self.type), value, self)
            return has_action(str("customize_update_") + str(self.type))
        # end if
    # end def update
    #// 
    #// Deprecated method.
    #// 
    #// @since 3.4.0
    #// @deprecated 4.4.0 Deprecated in favor of update() method.
    #//
    def _update_theme_mod(self):
        
        _deprecated_function(__METHOD__, "4.4.0", __CLASS__ + "::update()")
    # end def _update_theme_mod
    #// 
    #// Deprecated method.
    #// 
    #// @since 3.4.0
    #// @deprecated 4.4.0 Deprecated in favor of update() method.
    #//
    def _update_option(self):
        
        _deprecated_function(__METHOD__, "4.4.0", __CLASS__ + "::update()")
    # end def _update_option
    #// 
    #// Fetch the value of the setting.
    #// 
    #// @since 3.4.0
    #// 
    #// @return mixed The value.
    #//
    def value(self):
        
        id_base = self.id_data["base"]
        is_core_type = "option" == self.type or "theme_mod" == self.type
        if (not is_core_type) and (not self.is_multidimensional_aggregated):
            #// Use post value if previewed and a post value is present.
            if self.is_previewed:
                value = self.post_value(None)
                if None != value:
                    return value
                # end if
            # end if
            value = self.get_root_value(self.default)
            #// 
            #// Filters a Customize setting value not handled as a theme_mod or option.
            #// 
            #// The dynamic portion of the hook name, `$id_base`, refers to
            #// the base slug of the setting name, initialized from `$this->id_data['base']`.
            #// 
            #// For settings handled as theme_mods or options, see those corresponding
            #// functions for available hooks.
            #// 
            #// @since 3.4.0
            #// @since 4.6.0 Added the `$this` setting instance as the second parameter.
            #// 
            #// @param mixed                $default The setting default value. Default empty.
            #// @param WP_Customize_Setting $this    The setting instance.
            #//
            value = apply_filters(str("customize_value_") + str(id_base), value, self)
        elif self.is_multidimensional_aggregated:
            root_value = self.aggregated_multidimensionals[self.type][id_base]["root_value"]
            value = self.multidimensional_get(root_value, self.id_data["keys"], self.default)
            #// Ensure that the post value is used if the setting is previewed, since preview filters aren't applying on cached $root_value.
            if self.is_previewed:
                value = self.post_value(value)
            # end if
        else:
            value = self.get_root_value(self.default)
        # end if
        return value
    # end def value
    #// 
    #// Sanitize the setting's value for use in JavaScript.
    #// 
    #// @since 3.4.0
    #// 
    #// @return mixed The requested escaped value.
    #//
    def js_value(self):
        
        #// 
        #// Filters a Customize setting value for use in JavaScript.
        #// 
        #// The dynamic portion of the hook name, `$this->id`, refers to the setting ID.
        #// 
        #// @since 3.4.0
        #// 
        #// @param mixed                $value The setting value.
        #// @param WP_Customize_Setting $this  WP_Customize_Setting instance.
        #//
        value = apply_filters(str("customize_sanitize_js_") + str(self.id), self.value(), self)
        if php_is_string(value):
            return html_entity_decode(value, ENT_QUOTES, "UTF-8")
        # end if
        return value
    # end def js_value
    #// 
    #// Retrieves the data to export to the client via JSON.
    #// 
    #// @since 4.6.0
    #// 
    #// @return array Array of parameters passed to JavaScript.
    #//
    def json(self):
        
        return Array({"value": self.js_value(), "transport": self.transport, "dirty": self.dirty, "type": self.type})
    # end def json
    #// 
    #// Validate user capabilities whether the theme supports the setting.
    #// 
    #// @since 3.4.0
    #// 
    #// @return bool False if theme doesn't support the setting or user can't change setting, otherwise true.
    #//
    def check_capabilities(self):
        
        if self.capability and (not current_user_can(self.capability)):
            return False
        # end if
        if self.theme_supports and (not current_theme_supports(self.theme_supports)):
            return False
        # end if
        return True
    # end def check_capabilities
    #// 
    #// Multidimensional helper function.
    #// 
    #// @since 3.4.0
    #// 
    #// @param $root
    #// @param $keys
    #// @param bool $create Default is false.
    #// @return array|void Keys are 'root', 'node', and 'key'.
    #//
    def multidimensional(self, root=None, keys=None, create=False):
        
        if create and php_empty(lambda : root):
            root = Array()
        # end if
        if (not (php_isset(lambda : root))) or php_empty(lambda : keys):
            return
        # end if
        last = php_array_pop(keys)
        node = root
        for key in keys:
            if create and (not (php_isset(lambda : node[key]))):
                node[key] = Array()
            # end if
            if (not php_is_array(node)) or (not (php_isset(lambda : node[key]))):
                return
            # end if
            node = node[key]
        # end for
        if create:
            if (not php_is_array(node)):
                #// Account for an array overriding a string or object value.
                node = Array()
            # end if
            if (not (php_isset(lambda : node[last]))):
                node[last] = Array()
            # end if
        # end if
        if (not (php_isset(lambda : node[last]))):
            return
        # end if
        return Array({"root": root, "node": node, "key": last})
    # end def multidimensional
    #// 
    #// Will attempt to replace a specific value in a multidimensional array.
    #// 
    #// @since 3.4.0
    #// 
    #// @param $root
    #// @param $keys
    #// @param mixed $value The value to update.
    #// @return mixed
    #//
    def multidimensional_replace(self, root=None, keys=None, value=None):
        
        if (not (php_isset(lambda : value))):
            return root
        elif php_empty(lambda : keys):
            #// If there are no keys, we're replacing the root.
            return value
        # end if
        result = self.multidimensional(root, keys, True)
        if (php_isset(lambda : result)):
            result["node"][result["key"]] = value
        # end if
        return root
    # end def multidimensional_replace
    #// 
    #// Will attempt to fetch a specific value from a multidimensional array.
    #// 
    #// @since 3.4.0
    #// 
    #// @param $root
    #// @param $keys
    #// @param mixed $default A default value which is used as a fallback. Default is null.
    #// @return mixed The requested value or the default value.
    #//
    def multidimensional_get(self, root=None, keys=None, default=None):
        
        if php_empty(lambda : keys):
            #// If there are no keys, test the root.
            return root if (php_isset(lambda : root)) else default
        # end if
        result = self.multidimensional(root, keys)
        return result["node"][result["key"]] if (php_isset(lambda : result)) else default
    # end def multidimensional_get
    #// 
    #// Will attempt to check if a specific value in a multidimensional array is set.
    #// 
    #// @since 3.4.0
    #// 
    #// @param $root
    #// @param $keys
    #// @return bool True if value is set, false if not.
    #//
    def multidimensional_isset(self, root=None, keys=None):
        
        result = self.multidimensional_get(root, keys)
        return (php_isset(lambda : result))
    # end def multidimensional_isset
# end class WP_Customize_Setting
#// 
#// WP_Customize_Filter_Setting class.
#//
php_include_file(ABSPATH + WPINC + "/customize/class-wp-customize-filter-setting.php", once=True)
#// 
#// WP_Customize_Header_Image_Setting class.
#//
php_include_file(ABSPATH + WPINC + "/customize/class-wp-customize-header-image-setting.php", once=True)
#// 
#// WP_Customize_Background_Image_Setting class.
#//
php_include_file(ABSPATH + WPINC + "/customize/class-wp-customize-background-image-setting.php", once=True)
#// 
#// WP_Customize_Nav_Menu_Item_Setting class.
#//
php_include_file(ABSPATH + WPINC + "/customize/class-wp-customize-nav-menu-item-setting.php", once=True)
#// 
#// WP_Customize_Nav_Menu_Setting class.
#//
php_include_file(ABSPATH + WPINC + "/customize/class-wp-customize-nav-menu-setting.php", once=True)
