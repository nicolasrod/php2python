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
#// Locale API: WP_Locale_Switcher class
#// 
#// @package WordPress
#// @subpackage i18n
#// @since 4.7.0
#// 
#// 
#// Core class used for switching locales.
#// 
#// @since 4.7.0
#//
class WP_Locale_Switcher():
    locales = Array()
    original_locale = Array()
    available_languages = Array()
    #// 
    #// Constructor.
    #// 
    #// Stores the original locale as well as a list of all available languages.
    #// 
    #// @since 4.7.0
    #//
    def __init__(self):
        
        self.original_locale = determine_locale()
        self.available_languages = php_array_merge(Array("en_US"), get_available_languages())
    # end def __init__
    #// 
    #// Initializes the locale switcher.
    #// 
    #// Hooks into the {@see 'locale'} filter to change the locale on the fly.
    #// 
    #// @since 4.7.0
    #//
    def init(self):
        
        add_filter("locale", Array(self, "filter_locale"))
    # end def init
    #// 
    #// Switches the translations according to the given locale.
    #// 
    #// @since 4.7.0
    #// 
    #// @param string $locale The locale to switch to.
    #// @return bool True on success, false on failure.
    #//
    def switch_to_locale(self, locale=None):
        
        current_locale = determine_locale()
        if current_locale == locale:
            return False
        # end if
        if (not php_in_array(locale, self.available_languages, True)):
            return False
        # end if
        self.locales[-1] = locale
        self.change_locale(locale)
        #// 
        #// Fires when the locale is switched.
        #// 
        #// @since 4.7.0
        #// 
        #// @param string $locale The new locale.
        #//
        do_action("switch_locale", locale)
        return True
    # end def switch_to_locale
    #// 
    #// Restores the translations according to the previous locale.
    #// 
    #// @since 4.7.0
    #// 
    #// @return string|false Locale on success, false on failure.
    #//
    def restore_previous_locale(self):
        
        previous_locale = php_array_pop(self.locales)
        if None == previous_locale:
            #// The stack is empty, bail.
            return False
        # end if
        locale = php_end(self.locales)
        if (not locale):
            #// There's nothing left in the stack: go back to the original locale.
            locale = self.original_locale
        # end if
        self.change_locale(locale)
        #// 
        #// Fires when the locale is restored to the previous one.
        #// 
        #// @since 4.7.0
        #// 
        #// @param string $locale          The new locale.
        #// @param string $previous_locale The previous locale.
        #//
        do_action("restore_previous_locale", locale, previous_locale)
        return locale
    # end def restore_previous_locale
    #// 
    #// Restores the translations according to the original locale.
    #// 
    #// @since 4.7.0
    #// 
    #// @return string|false Locale on success, false on failure.
    #//
    def restore_current_locale(self):
        
        if php_empty(lambda : self.locales):
            return False
        # end if
        self.locales = Array(self.original_locale)
        return self.restore_previous_locale()
    # end def restore_current_locale
    #// 
    #// Whether switch_to_locale() is in effect.
    #// 
    #// @since 4.7.0
    #// 
    #// @return bool True if the locale has been switched, false otherwise.
    #//
    def is_switched(self):
        
        return (not php_empty(lambda : self.locales))
    # end def is_switched
    #// 
    #// Filters the locale of the WordPress installation.
    #// 
    #// @since 4.7.0
    #// 
    #// @param string $locale The locale of the WordPress installation.
    #// @return string The locale currently being switched to.
    #//
    def filter_locale(self, locale=None):
        
        switched_locale = php_end(self.locales)
        if switched_locale:
            return switched_locale
        # end if
        return locale
    # end def filter_locale
    #// 
    #// Load translations for a given locale.
    #// 
    #// When switching to a locale, translations for this locale must be loaded from scratch.
    #// 
    #// @since 4.7.0
    #// 
    #// @global Mo[] $l10n An array of all currently loaded text domains.
    #// 
    #// @param string $locale The locale to load translations for.
    #//
    def load_translations(self, locale=None):
        
        global l10n
        php_check_if_defined("l10n")
        domains = php_array_keys(l10n) if l10n else Array()
        load_default_textdomain(locale)
        for domain in domains:
            if "default" == domain:
                continue
            # end if
            unload_textdomain(domain)
            get_translations_for_domain(domain)
        # end for
    # end def load_translations
    #// 
    #// Changes the site's locale to the given one.
    #// 
    #// Loads the translations, changes the global `$wp_locale` object and updates
    #// all post type labels.
    #// 
    #// @since 4.7.0
    #// 
    #// @global WP_Locale $wp_locale WordPress date and time locale object.
    #// 
    #// @param string $locale The locale to change to.
    #//
    def change_locale(self, locale=None):
        global PHP_GLOBALS
        #// Reset translation availability information.
        _get_path_to_translation(None, True)
        self.load_translations(locale)
        PHP_GLOBALS["wp_locale"] = php_new_class("WP_Locale", lambda : WP_Locale())
        #// 
        #// Fires when the locale is switched to or restored.
        #// 
        #// @since 4.7.0
        #// 
        #// @param string $locale The new locale.
        #//
        do_action("change_locale", locale)
    # end def change_locale
# end class WP_Locale_Switcher
