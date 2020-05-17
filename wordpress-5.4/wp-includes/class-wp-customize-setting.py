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
    #// 
    #// Customizer bootstrap instance.
    #// 
    #// @since 3.4.0
    #// @var WP_Customize_Manager
    #//
    manager = Array()
    #// 
    #// Unique string identifier for the setting.
    #// 
    #// @since 3.4.0
    #// @var string
    #//
    id = Array()
    #// 
    #// Type of customize settings.
    #// 
    #// @since 3.4.0
    #// @var string
    #//
    type = "theme_mod"
    #// 
    #// Capability required to edit this setting.
    #// 
    #// @since 3.4.0
    #// @var string|array
    #//
    capability = "edit_theme_options"
    #// 
    #// Theme features required to support the setting.
    #// 
    #// @since 3.4.0
    #// @var string|string[]
    #//
    theme_supports = ""
    #// 
    #// The default value for the setting.
    #// 
    #// @since 3.4.0
    #// @var string
    #//
    default = ""
    #// 
    #// Options for rendering the live preview of changes in Customizer.
    #// 
    #// Set this value to 'postMessage' to enable a custom JavaScript handler to render changes to this setting
    #// as opposed to reloading the whole page.
    #// 
    #// @since 3.4.0
    #// @var string
    #//
    transport = "refresh"
    #// 
    #// Server-side validation callback for the setting's value.
    #// 
    #// @since 4.6.0
    #// @var callable
    #//
    validate_callback = ""
    #// 
    #// Callback to filter a Customize setting value in un-slashed form.
    #// 
    #// @since 3.4.0
    #// @var callable
    #//
    sanitize_callback = ""
    #// 
    #// Callback to convert a Customize PHP setting value to a value that is JSON serializable.
    #// 
    #// @since 3.4.0
    #// @var string
    #//
    sanitize_js_callback = ""
    #// 
    #// Whether or not the setting is initially dirty when created.
    #// 
    #// This is used to ensure that a setting will be sent from the pane to the
    #// preview when loading the Customizer. Normally a setting only is synced to
    #// the preview if it has been changed. This allows the setting to be sent
    #// from the start.
    #// 
    #// @since 4.2.0
    #// @var bool
    #//
    dirty = False
    #// 
    #// ID Data.
    #// 
    #// @since 3.4.0
    #// @var array
    #//
    id_data = Array()
    #// 
    #// Whether or not preview() was called.
    #// 
    #// @since 4.4.0
    #// @var bool
    #//
    is_previewed = False
    #// 
    #// Cache of multidimensional values to improve performance.
    #// 
    #// @since 4.4.0
    #// @var array
    #//
    aggregated_multidimensionals = Array()
    #// 
    #// Whether the multidimensional setting is aggregated.
    #// 
    #// @since 4.4.0
    #// @var bool
    #//
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
    def __init__(self, manager_=None, id_=None, args_=None):
        if args_ is None:
            args_ = Array()
        # end if
        
        keys_ = php_array_keys(get_object_vars(self))
        for key_ in keys_:
            if (php_isset(lambda : args_[key_])):
                self.key_ = args_[key_]
            # end if
        # end for
        self.manager = manager_
        self.id = id_
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
            if "option" == self.type and (php_isset(lambda : args_["autoload"])):
                self.aggregated_multidimensionals[self.type][self.id_data["base"]]["autoload"] = args_["autoload"]
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
        
        
        id_base_ = self.id_data["base"]
        if (not (php_isset(lambda : self.aggregated_multidimensionals[self.type]))):
            self.aggregated_multidimensionals[self.type] = Array()
        # end if
        if (not (php_isset(lambda : self.aggregated_multidimensionals[self.type][id_base_]))):
            self.aggregated_multidimensionals[self.type][id_base_] = Array({"previewed_instances": Array(), "preview_applied_instances": Array(), "root_value": self.get_root_value(Array())})
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
    #// 
    #// The ID for the current site when the preview() method was called.
    #// 
    #// @since 4.2.0
    #// @var int
    #//
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
    #// 
    #// Original non-previewed value stored by the preview method.
    #// 
    #// @see WP_Customize_Setting::preview()
    #// @since 4.1.1
    #// @var mixed
    #//
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
        id_base_ = self.id_data["base"]
        is_multidimensional_ = (not php_empty(lambda : self.id_data["keys"]))
        multidimensional_filter_ = Array(self, "_multidimensional_preview_filter")
        #// 
        #// Check if the setting has a pre-existing value (an isset check),
        #// and if doesn't have any incoming post value. If both checks are true,
        #// then the preview short-circuits because there is nothing that needs
        #// to be previewed.
        #//
        undefined_ = php_new_class("stdClass", lambda : stdClass())
        needs_preview_ = undefined_ != self.post_value(undefined_)
        value_ = None
        #// Since no post value was defined, check if we have an initial value set.
        if (not needs_preview_):
            if self.is_multidimensional_aggregated:
                root_ = self.aggregated_multidimensionals[self.type][id_base_]["root_value"]
                value_ = self.multidimensional_get(root_, self.id_data["keys"], undefined_)
            else:
                default_ = self.default
                self.default = undefined_
                #// Temporarily set default to undefined so we can detect if existing value is set.
                value_ = self.value()
                self.default = default_
            # end if
            needs_preview_ = undefined_ == value_
            pass
        # end if
        #// If the setting does not need previewing now, defer to when it has a value to preview.
        if (not needs_preview_):
            if (not has_action(str("customize_post_value_set_") + str(self.id), Array(self, "preview"))):
                add_action(str("customize_post_value_set_") + str(self.id), Array(self, "preview"))
            # end if
            return False
        # end if
        for case in Switch(self.type):
            if case("theme_mod"):
                if (not is_multidimensional_):
                    add_filter(str("theme_mod_") + str(id_base_), Array(self, "_preview_filter"))
                else:
                    if php_empty(lambda : self.aggregated_multidimensionals[self.type][id_base_]["previewed_instances"]):
                        #// Only add this filter once for this ID base.
                        add_filter(str("theme_mod_") + str(id_base_), multidimensional_filter_)
                    # end if
                    self.aggregated_multidimensionals[self.type][id_base_]["previewed_instances"][self.id] = self
                # end if
                break
            # end if
            if case("option"):
                if (not is_multidimensional_):
                    add_filter(str("pre_option_") + str(id_base_), Array(self, "_preview_filter"))
                else:
                    if php_empty(lambda : self.aggregated_multidimensionals[self.type][id_base_]["previewed_instances"]):
                        #// Only add these filters once for this ID base.
                        add_filter(str("option_") + str(id_base_), multidimensional_filter_)
                        add_filter(str("default_option_") + str(id_base_), multidimensional_filter_)
                    # end if
                    self.aggregated_multidimensionals[self.type][id_base_]["previewed_instances"][self.id] = self
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
    def _preview_filter(self, original_=None):
        
        
        if (not self.is_current_blog_previewed()):
            return original_
        # end if
        undefined_ = php_new_class("stdClass", lambda : stdClass())
        #// Symbol hack.
        post_value_ = self.post_value(undefined_)
        if undefined_ != post_value_:
            value_ = post_value_
        else:
            #// 
            #// Note that we don't use $original here because preview() will
            #// not add the filter in the first place if it has an initial value
            #// and there is no post value.
            #//
            value_ = self.default
        # end if
        return value_
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
    def _multidimensional_preview_filter(self, original_=None):
        
        
        if (not self.is_current_blog_previewed()):
            return original_
        # end if
        id_base_ = self.id_data["base"]
        #// If no settings have been previewed yet (which should not be the case, since $this is), just pass through the original value.
        if php_empty(lambda : self.aggregated_multidimensionals[self.type][id_base_]["previewed_instances"]):
            return original_
        # end if
        for previewed_setting_ in self.aggregated_multidimensionals[self.type][id_base_]["previewed_instances"]:
            #// Skip applying previewed value for any settings that have already been applied.
            if (not php_empty(lambda : self.aggregated_multidimensionals[self.type][id_base_]["preview_applied_instances"][previewed_setting_.id])):
                continue
            # end if
            #// Do the replacements of the posted/default sub value into the root value.
            value_ = previewed_setting_.post_value(previewed_setting_.default)
            root_ = self.aggregated_multidimensionals[previewed_setting_.type][id_base_]["root_value"]
            root_ = previewed_setting_.multidimensional_replace(root_, previewed_setting_.id_data["keys"], value_)
            self.aggregated_multidimensionals[previewed_setting_.type][id_base_]["root_value"] = root_
            #// Mark this setting having been applied so that it will be skipped when the filter is called again.
            self.aggregated_multidimensionals[previewed_setting_.type][id_base_]["preview_applied_instances"][previewed_setting_.id] = True
        # end for
        return self.aggregated_multidimensionals[self.type][id_base_]["root_value"]
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
        
        
        value_ = self.post_value()
        if (not self.check_capabilities()) or (not (php_isset(lambda : value_))):
            return False
        # end if
        id_base_ = self.id_data["base"]
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
        do_action(str("customize_save_") + str(id_base_), self)
        self.update(value_)
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
    def post_value(self, default_=None):
        if default_ is None:
            default_ = None
        # end if
        
        return self.manager.post_value(self, default_)
    # end def post_value
    #// 
    #// Sanitize an input.
    #// 
    #// @since 3.4.0
    #// 
    #// @param string|array $value    The value to sanitize.
    #// @return string|array|null|WP_Error Sanitized value, or `null`/`WP_Error` if invalid.
    #//
    def sanitize(self, value_=None):
        
        
        #// 
        #// Filters a Customize setting value in un-slashed form.
        #// 
        #// @since 3.4.0
        #// 
        #// @param mixed                $value Value of the setting.
        #// @param WP_Customize_Setting $this  WP_Customize_Setting instance.
        #//
        return apply_filters(str("customize_sanitize_") + str(self.id), value_, self)
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
    def validate(self, value_=None):
        
        
        if is_wp_error(value_):
            return value_
        # end if
        if php_is_null(value_):
            return php_new_class("WP_Error", lambda : WP_Error("invalid_value", __("Invalid value.")))
        # end if
        validity_ = php_new_class("WP_Error", lambda : WP_Error())
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
        validity_ = apply_filters(str("customize_validate_") + str(self.id), validity_, value_, self)
        if is_wp_error(validity_) and (not validity_.has_errors()):
            validity_ = True
        # end if
        return validity_
    # end def validate
    #// 
    #// Get the root value for a setting, especially for multidimensional ones.
    #// 
    #// @since 4.4.0
    #// 
    #// @param mixed $default Value to return if root does not exist.
    #// @return mixed
    #//
    def get_root_value(self, default_=None):
        if default_ is None:
            default_ = None
        # end if
        
        id_base_ = self.id_data["base"]
        if "option" == self.type:
            return get_option(id_base_, default_)
        elif "theme_mod" == self.type:
            return get_theme_mod(id_base_, default_)
        else:
            #// 
            #// Any WP_Customize_Setting subclass implementing aggregate multidimensional
            #// will need to override this method to obtain the data from the appropriate
            #// location.
            #//
            return default_
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
    def set_root_value(self, value_=None):
        
        
        id_base_ = self.id_data["base"]
        if "option" == self.type:
            autoload_ = True
            if (php_isset(lambda : self.aggregated_multidimensionals[self.type][self.id_data["base"]]["autoload"])):
                autoload_ = self.aggregated_multidimensionals[self.type][self.id_data["base"]]["autoload"]
            # end if
            return update_option(id_base_, value_, autoload_)
        elif "theme_mod" == self.type:
            set_theme_mod(id_base_, value_)
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
    def update(self, value_=None):
        
        
        id_base_ = self.id_data["base"]
        if "option" == self.type or "theme_mod" == self.type:
            if (not self.is_multidimensional_aggregated):
                return self.set_root_value(value_)
            else:
                root_ = self.aggregated_multidimensionals[self.type][id_base_]["root_value"]
                root_ = self.multidimensional_replace(root_, self.id_data["keys"], value_)
                self.aggregated_multidimensionals[self.type][id_base_]["root_value"] = root_
                return self.set_root_value(root_)
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
            do_action(str("customize_update_") + str(self.type), value_, self)
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
        
        
        id_base_ = self.id_data["base"]
        is_core_type_ = "option" == self.type or "theme_mod" == self.type
        if (not is_core_type_) and (not self.is_multidimensional_aggregated):
            #// Use post value if previewed and a post value is present.
            if self.is_previewed:
                value_ = self.post_value(None)
                if None != value_:
                    return value_
                # end if
            # end if
            value_ = self.get_root_value(self.default)
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
            value_ = apply_filters(str("customize_value_") + str(id_base_), value_, self)
        elif self.is_multidimensional_aggregated:
            root_value_ = self.aggregated_multidimensionals[self.type][id_base_]["root_value"]
            value_ = self.multidimensional_get(root_value_, self.id_data["keys"], self.default)
            #// Ensure that the post value is used if the setting is previewed, since preview filters aren't applying on cached $root_value.
            if self.is_previewed:
                value_ = self.post_value(value_)
            # end if
        else:
            value_ = self.get_root_value(self.default)
        # end if
        return value_
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
        value_ = apply_filters(str("customize_sanitize_js_") + str(self.id), self.value(), self)
        if php_is_string(value_):
            return html_entity_decode(value_, ENT_QUOTES, "UTF-8")
        # end if
        return value_
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
    def multidimensional(self, root_=None, keys_=None, create_=None):
        if create_ is None:
            create_ = False
        # end if
        
        if create_ and php_empty(lambda : root_):
            root_ = Array()
        # end if
        if (not (php_isset(lambda : root_))) or php_empty(lambda : keys_):
            return
        # end if
        last_ = php_array_pop(keys_)
        node_ = root_
        for key_ in keys_:
            if create_ and (not (php_isset(lambda : node_[key_]))):
                node_[key_] = Array()
            # end if
            if (not php_is_array(node_)) or (not (php_isset(lambda : node_[key_]))):
                return
            # end if
            node_ = node_[key_]
        # end for
        if create_:
            if (not php_is_array(node_)):
                #// Account for an array overriding a string or object value.
                node_ = Array()
            # end if
            if (not (php_isset(lambda : node_[last_]))):
                node_[last_] = Array()
            # end if
        # end if
        if (not (php_isset(lambda : node_[last_]))):
            return
        # end if
        return Array({"root": root_, "node": node_, "key": last_})
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
    def multidimensional_replace(self, root_=None, keys_=None, value_=None):
        
        
        if (not (php_isset(lambda : value_))):
            return root_
        elif php_empty(lambda : keys_):
            #// If there are no keys, we're replacing the root.
            return value_
        # end if
        result_ = self.multidimensional(root_, keys_, True)
        if (php_isset(lambda : result_)):
            result_["node"][result_["key"]] = value_
        # end if
        return root_
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
    def multidimensional_get(self, root_=None, keys_=None, default_=None):
        if default_ is None:
            default_ = None
        # end if
        
        if php_empty(lambda : keys_):
            #// If there are no keys, test the root.
            return root_ if (php_isset(lambda : root_)) else default_
        # end if
        result_ = self.multidimensional(root_, keys_)
        return result_["node"][result_["key"]] if (php_isset(lambda : result_)) else default_
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
    def multidimensional_isset(self, root_=None, keys_=None):
        
        
        result_ = self.multidimensional_get(root_, keys_)
        return (php_isset(lambda : result_))
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
