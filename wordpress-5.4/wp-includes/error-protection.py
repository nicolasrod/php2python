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
#// Error Protection API: Functions
#// 
#// @package WordPress
#// @since 5.2.0
#// 
#// 
#// Get the instance for storing paused plugins.
#// 
#// @return WP_Paused_Extensions_Storage
#//
def wp_paused_plugins(*_args_):
    
    
    storage_ = None
    if None == storage_:
        storage_ = php_new_class("WP_Paused_Extensions_Storage", lambda : WP_Paused_Extensions_Storage("plugin"))
    # end if
    return storage_
# end def wp_paused_plugins
#// 
#// Get the instance for storing paused extensions.
#// 
#// @return WP_Paused_Extensions_Storage
#//
def wp_paused_themes(*_args_):
    
    
    storage_ = None
    if None == storage_:
        storage_ = php_new_class("WP_Paused_Extensions_Storage", lambda : WP_Paused_Extensions_Storage("theme"))
    # end if
    return storage_
# end def wp_paused_themes
#// 
#// Get a human readable description of an extension's error.
#// 
#// @since 5.2.0
#// 
#// @param array $error Error details {@see error_get_last()}
#// 
#// @return string Formatted error description.
#//
def wp_get_extension_error_description(error_=None, *_args_):
    
    
    constants_ = get_defined_constants(True)
    constants_ = constants_["Core"] if (php_isset(lambda : constants_["Core"])) else constants_["internal"]
    core_errors_ = Array()
    for constant_,value_ in constants_:
        if 0 == php_strpos(constant_, "E_"):
            core_errors_[value_] = constant_
        # end if
    # end for
    if (php_isset(lambda : core_errors_[error_["type"]])):
        error_["type"] = core_errors_[error_["type"]]
    # end if
    #// translators: 1: Error type, 2: Error line number, 3: Error file name, 4: Error message.
    error_message_ = __("An error of type %1$s was caused in line %2$s of the file %3$s. Error message: %4$s")
    return php_sprintf(error_message_, str("<code>") + str(error_["type"]) + str("</code>"), str("<code>") + str(error_["line"]) + str("</code>"), str("<code>") + str(error_["file"]) + str("</code>"), str("<code>") + str(error_["message"]) + str("</code>"))
# end def wp_get_extension_error_description
#// 
#// Registers the shutdown handler for fatal errors.
#// 
#// The handler will only be registered if {@see wp_is_fatal_error_handler_enabled()} returns true.
#// 
#// @since 5.2.0
#//
def wp_register_fatal_error_handler(*_args_):
    
    
    if (not wp_is_fatal_error_handler_enabled()):
        return
    # end if
    handler_ = None
    if php_defined("WP_CONTENT_DIR") and php_is_readable(WP_CONTENT_DIR + "/fatal-error-handler.php"):
        handler_ = php_include_file(WP_CONTENT_DIR + "/fatal-error-handler.php", once=False)
    # end if
    if (not php_is_object(handler_)) or (not php_is_callable(Array(handler_, "handle"))):
        handler_ = php_new_class("WP_Fatal_Error_Handler", lambda : WP_Fatal_Error_Handler())
    # end if
    php_register_shutdown_function(Array(handler_, "handle"))
# end def wp_register_fatal_error_handler
#// 
#// Checks whether the fatal error handler is enabled.
#// 
#// A constant `WP_DISABLE_FATAL_ERROR_HANDLER` can be set in `wp-config.php` to disable it, or alternatively the
#// {@see 'wp_fatal_error_handler_enabled'} filter can be used to modify the return value.
#// 
#// @since 5.2.0
#// 
#// @return bool True if the fatal error handler is enabled, false otherwise.
#//
def wp_is_fatal_error_handler_enabled(*_args_):
    
    
    enabled_ = (not php_defined("WP_DISABLE_FATAL_ERROR_HANDLER")) or (not WP_DISABLE_FATAL_ERROR_HANDLER)
    #// 
    #// Filters whether the fatal error handler is enabled.
    #// 
    #// @since 5.2.0
    #// 
    #// @param bool $enabled True if the fatal error handler is enabled, false otherwise.
    #//
    return apply_filters("wp_fatal_error_handler_enabled", enabled_)
# end def wp_is_fatal_error_handler_enabled
#// 
#// Access the WordPress Recovery Mode instance.
#// 
#// @since 5.2.0
#// 
#// @return WP_Recovery_Mode
#//
def wp_recovery_mode(*_args_):
    
    
    wp_recovery_mode_ = None
    if (not wp_recovery_mode_):
        wp_recovery_mode_ = php_new_class("WP_Recovery_Mode", lambda : WP_Recovery_Mode())
    # end if
    return wp_recovery_mode_
# end def wp_recovery_mode
