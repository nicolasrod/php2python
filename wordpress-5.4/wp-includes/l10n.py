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
#// Core Translation API
#// 
#// @package WordPress
#// @subpackage i18n
#// @since 1.2.0
#// 
#// 
#// Retrieves the current locale.
#// 
#// If the locale is set, then it will filter the locale in the {@see 'locale'}
#// filter hook and return the value.
#// 
#// If the locale is not set already, then the WPLANG constant is used if it is
#// defined. Then it is filtered through the {@see 'locale'} filter hook and
#// the value for the locale global set and the locale is returned.
#// 
#// The process to get the locale should only be done once, but the locale will
#// always be filtered using the {@see 'locale'} hook.
#// 
#// @since 1.5.0
#// 
#// @global string $locale           The current locale.
#// @global string $wp_local_package Locale code of the package.
#// 
#// @return string The locale of the blog or from the {@see 'locale'} hook.
#//
def get_locale(*_args_):
    
    
    global locale_
    global wp_local_package_
    php_check_if_defined("locale_","wp_local_package_")
    if (php_isset(lambda : locale_)):
        #// 
        #// Filters the locale ID of the WordPress installation.
        #// 
        #// @since 1.5.0
        #// 
        #// @param string $locale The locale ID.
        #//
        return apply_filters("locale", locale_)
    # end if
    if (php_isset(lambda : wp_local_package_)):
        locale_ = wp_local_package_
    # end if
    #// WPLANG was defined in wp-config.
    if php_defined("WPLANG"):
        locale_ = WPLANG
    # end if
    #// If multisite, check options.
    if is_multisite():
        #// Don't check blog option when installing.
        if wp_installing():
            ms_locale_ = get_site_option("WPLANG")
        else:
            ms_locale_ = get_option("WPLANG")
            if False == ms_locale_:
                ms_locale_ = get_site_option("WPLANG")
            # end if
        # end if
        if False != ms_locale_:
            locale_ = ms_locale_
        # end if
    else:
        db_locale_ = get_option("WPLANG")
        if False != db_locale_:
            locale_ = db_locale_
        # end if
    # end if
    if php_empty(lambda : locale_):
        locale_ = "en_US"
    # end if
    #// This filter is documented in wp-includes/l10n.php
    return apply_filters("locale", locale_)
# end def get_locale
#// 
#// Retrieves the locale of a user.
#// 
#// If the user has a locale set to a non-empty string then it will be
#// returned. Otherwise it returns the locale of get_locale().
#// 
#// @since 4.7.0
#// 
#// @param int|WP_User $user_id User's ID or a WP_User object. Defaults to current user.
#// @return string The locale of the user.
#//
def get_user_locale(user_id_=0, *_args_):
    
    
    user_ = False
    if 0 == user_id_ and php_function_exists("wp_get_current_user"):
        user_ = wp_get_current_user()
    elif type(user_id_).__name__ == "WP_User":
        user_ = user_id_
    elif user_id_ and php_is_numeric(user_id_):
        user_ = get_user_by("id", user_id_)
    # end if
    if (not user_):
        return get_locale()
    # end if
    locale_ = user_.locale
    return locale_ if locale_ else get_locale()
# end def get_user_locale
#// 
#// Determine the current locale desired for the request.
#// 
#// @since 5.0.0
#// 
#// @global string $pagenow
#// 
#// @return string The determined locale.
#//
def determine_locale(*_args_):
    
    
    #// 
    #// Filters the locale for the current request prior to the default determination process.
    #// 
    #// Using this filter allows to override the default logic, effectively short-circuiting the function.
    #// 
    #// @since 5.0.0
    #// 
    #// @param string|null $locale The locale to return and short-circuit. Default null.
    #//
    determined_locale_ = apply_filters("pre_determine_locale", None)
    if (not php_empty(lambda : determined_locale_)) and php_is_string(determined_locale_):
        return determined_locale_
    # end if
    determined_locale_ = get_locale()
    if is_admin():
        determined_locale_ = get_user_locale()
    # end if
    if (php_isset(lambda : PHP_REQUEST["_locale"])) and "user" == PHP_REQUEST["_locale"] and wp_is_json_request():
        determined_locale_ = get_user_locale()
    # end if
    if (not php_empty(lambda : PHP_REQUEST["wp_lang"])) and (not php_empty(lambda : PHP_GLOBALS["pagenow"])) and "wp-login.php" == PHP_GLOBALS["pagenow"]:
        determined_locale_ = sanitize_text_field(PHP_REQUEST["wp_lang"])
    # end if
    #// 
    #// Filters the locale for the current request.
    #// 
    #// @since 5.0.0
    #// 
    #// @param string $locale The locale.
    #//
    return apply_filters("determine_locale", determined_locale_)
# end def determine_locale
#// 
#// Retrieve the translation of $text.
#// 
#// If there is no translation, or the text domain isn't loaded, the original text is returned.
#// 
#// Note:* Don't use translate() directly, use __() or related functions.
#// 
#// @since 2.2.0
#// 
#// @param string $text   Text to translate.
#// @param string $domain Optional. Text domain. Unique identifier for retrieving translated strings.
#// Default 'default'.
#// @return string Translated text.
#//
def translate(text_=None, domain_="default", *_args_):
    
    
    translations_ = get_translations_for_domain(domain_)
    translation_ = translations_.translate(text_)
    #// 
    #// Filters text with its translation.
    #// 
    #// @since 2.0.11
    #// 
    #// @param string $translation  Translated text.
    #// @param string $text         Text to translate.
    #// @param string $domain       Text domain. Unique identifier for retrieving translated strings.
    #//
    return apply_filters("gettext", translation_, text_, domain_)
# end def translate
#// 
#// Remove last item on a pipe-delimited string.
#// 
#// Meant for removing the last item in a string, such as 'Role name|User role'. The original
#// string will be returned if no pipe '|' characters are found in the string.
#// 
#// @since 2.8.0
#// 
#// @param string $string A pipe-delimited string.
#// @return string Either $string or everything before the last pipe.
#//
def before_last_bar(string_=None, *_args_):
    
    
    last_bar_ = php_strrpos(string_, "|")
    if False == last_bar_:
        return string_
    else:
        return php_substr(string_, 0, last_bar_)
    # end if
# end def before_last_bar
#// 
#// Retrieve the translation of $text in the context defined in $context.
#// 
#// If there is no translation, or the text domain isn't loaded, the original text is returned.
#// 
#// Note:* Don't use translate_with_gettext_context() directly, use _x() or related functions.
#// 
#// @since 2.8.0
#// 
#// @param string $text    Text to translate.
#// @param string $context Context information for the translators.
#// @param string $domain  Optional. Text domain. Unique identifier for retrieving translated strings.
#// Default 'default'.
#// @return string Translated text on success, original text on failure.
#//
def translate_with_gettext_context(text_=None, context_=None, domain_="default", *_args_):
    
    
    translations_ = get_translations_for_domain(domain_)
    translation_ = translations_.translate(text_, context_)
    #// 
    #// Filters text with its translation based on context information.
    #// 
    #// @since 2.8.0
    #// 
    #// @param string $translation  Translated text.
    #// @param string $text         Text to translate.
    #// @param string $context      Context information for the translators.
    #// @param string $domain       Text domain. Unique identifier for retrieving translated strings.
    #//
    return apply_filters("gettext_with_context", translation_, text_, context_, domain_)
# end def translate_with_gettext_context
#// 
#// Retrieve the translation of $text.
#// 
#// If there is no translation, or the text domain isn't loaded, the original text is returned.
#// 
#// @since 2.1.0
#// 
#// @param string $text   Text to translate.
#// @param string $domain Optional. Text domain. Unique identifier for retrieving translated strings.
#// Default 'default'.
#// @return string Translated text.
#//
def __(text_=None, domain_="default", *_args_):
    
    
    return translate(text_, domain_)
# end def __
#// 
#// Retrieve the translation of $text and escapes it for safe use in an attribute.
#// 
#// If there is no translation, or the text domain isn't loaded, the original text is returned.
#// 
#// @since 2.8.0
#// 
#// @param string $text   Text to translate.
#// @param string $domain Optional. Text domain. Unique identifier for retrieving translated strings.
#// Default 'default'.
#// @return string Translated text on success, original text on failure.
#//
def esc_attr__(text_=None, domain_="default", *_args_):
    
    
    return esc_attr(translate(text_, domain_))
# end def esc_attr__
#// 
#// Retrieve the translation of $text and escapes it for safe use in HTML output.
#// 
#// If there is no translation, or the text domain isn't loaded, the original text
#// is escaped and returned.
#// 
#// @since 2.8.0
#// 
#// @param string $text   Text to translate.
#// @param string $domain Optional. Text domain. Unique identifier for retrieving translated strings.
#// Default 'default'.
#// @return string Translated text.
#//
def esc_html__(text_=None, domain_="default", *_args_):
    
    
    return esc_html(translate(text_, domain_))
# end def esc_html__
#// 
#// Display translated text.
#// 
#// @since 1.2.0
#// 
#// @param string $text   Text to translate.
#// @param string $domain Optional. Text domain. Unique identifier for retrieving translated strings.
#// Default 'default'.
#//
def _e(text_=None, domain_="default", *_args_):
    
    
    php_print(translate(text_, domain_))
# end def _e
#// 
#// Display translated text that has been escaped for safe use in an attribute.
#// 
#// Encodes `< > & " '` (less than, greater than, ampersand, double quote, single quote).
#// Will never double encode entities.
#// 
#// If you need the value for use in PHP, use esc_attr__().
#// 
#// @since 2.8.0
#// 
#// @param string $text   Text to translate.
#// @param string $domain Optional. Text domain. Unique identifier for retrieving translated strings.
#// Default 'default'.
#//
def esc_attr_e(text_=None, domain_="default", *_args_):
    
    
    php_print(esc_attr(translate(text_, domain_)))
# end def esc_attr_e
#// 
#// Display translated text that has been escaped for safe use in HTML output.
#// 
#// If there is no translation, or the text domain isn't loaded, the original text
#// is escaped and displayed.
#// 
#// If you need the value for use in PHP, use esc_html__().
#// 
#// @since 2.8.0
#// 
#// @param string $text   Text to translate.
#// @param string $domain Optional. Text domain. Unique identifier for retrieving translated strings.
#// Default 'default'.
#//
def esc_html_e(text_=None, domain_="default", *_args_):
    
    
    php_print(esc_html(translate(text_, domain_)))
# end def esc_html_e
#// 
#// Retrieve translated string with gettext context.
#// 
#// Quite a few times, there will be collisions with similar translatable text
#// found in more than two places, but with different translated context.
#// 
#// By including the context in the pot file, translators can translate the two
#// strings differently.
#// 
#// @since 2.8.0
#// 
#// @param string $text    Text to translate.
#// @param string $context Context information for the translators.
#// @param string $domain  Optional. Text domain. Unique identifier for retrieving translated strings.
#// Default 'default'.
#// @return string Translated context string without pipe.
#//
def _x(text_=None, context_=None, domain_="default", *_args_):
    
    
    return translate_with_gettext_context(text_, context_, domain_)
# end def _x
#// 
#// Display translated string with gettext context.
#// 
#// @since 3.0.0
#// 
#// @param string $text    Text to translate.
#// @param string $context Context information for the translators.
#// @param string $domain  Optional. Text domain. Unique identifier for retrieving translated strings.
#// Default 'default'.
#// @return string Translated context string without pipe.
#//
def _ex(text_=None, context_=None, domain_="default", *_args_):
    
    
    php_print(_x(text_, context_, domain_))
# end def _ex
#// 
#// Translate string with gettext context, and escapes it for safe use in an attribute.
#// 
#// If there is no translation, or the text domain isn't loaded, the original text
#// is escaped and returned.
#// 
#// @since 2.8.0
#// 
#// @param string $text    Text to translate.
#// @param string $context Context information for the translators.
#// @param string $domain  Optional. Text domain. Unique identifier for retrieving translated strings.
#// Default 'default'.
#// @return string Translated text.
#//
def esc_attr_x(text_=None, context_=None, domain_="default", *_args_):
    
    
    return esc_attr(translate_with_gettext_context(text_, context_, domain_))
# end def esc_attr_x
#// 
#// Translate string with gettext context, and escapes it for safe use in HTML output.
#// 
#// If there is no translation, or the text domain isn't loaded, the original text
#// is escaped and returned.
#// 
#// @since 2.9.0
#// 
#// @param string $text    Text to translate.
#// @param string $context Context information for the translators.
#// @param string $domain  Optional. Text domain. Unique identifier for retrieving translated strings.
#// Default 'default'.
#// @return string Translated text.
#//
def esc_html_x(text_=None, context_=None, domain_="default", *_args_):
    
    
    return esc_html(translate_with_gettext_context(text_, context_, domain_))
# end def esc_html_x
#// 
#// Translates and retrieves the singular or plural form based on the supplied number.
#// 
#// Used when you want to use the appropriate form of a string based on whether a
#// number is singular or plural.
#// 
#// Example:
#// 
#// printf( _n( '%s person', '%s people', $count, 'text-domain' ), number_format_i18n( $count ) );
#// 
#// @since 2.8.0
#// 
#// @param string $single The text to be used if the number is singular.
#// @param string $plural The text to be used if the number is plural.
#// @param int    $number The number to compare against to use either the singular or plural form.
#// @param string $domain Optional. Text domain. Unique identifier for retrieving translated strings.
#// Default 'default'.
#// @return string The translated singular or plural form.
#//
def _n(single_=None, plural_=None, number_=None, domain_="default", *_args_):
    
    
    translations_ = get_translations_for_domain(domain_)
    translation_ = translations_.translate_plural(single_, plural_, number_)
    #// 
    #// Filters the singular or plural form of a string.
    #// 
    #// @since 2.2.0
    #// 
    #// @param string $translation Translated text.
    #// @param string $single      The text to be used if the number is singular.
    #// @param string $plural      The text to be used if the number is plural.
    #// @param string $number      The number to compare against to use either the singular or plural form.
    #// @param string $domain      Text domain. Unique identifier for retrieving translated strings.
    #//
    return apply_filters("ngettext", translation_, single_, plural_, number_, domain_)
# end def _n
#// 
#// Translates and retrieves the singular or plural form based on the supplied number, with gettext context.
#// 
#// This is a hybrid of _n() and _x(). It supports context and plurals.
#// 
#// Used when you want to use the appropriate form of a string with context based on whether a
#// number is singular or plural.
#// 
#// Example of a generic phrase which is disambiguated via the context parameter:
#// 
#// printf( _nx( '%s group', '%s groups', $people, 'group of people', 'text-domain' ), number_format_i18n( $people ) );
#// printf( _nx( '%s group', '%s groups', $animals, 'group of animals', 'text-domain' ), number_format_i18n( $animals ) );
#// 
#// @since 2.8.0
#// 
#// @param string $single  The text to be used if the number is singular.
#// @param string $plural  The text to be used if the number is plural.
#// @param int    $number  The number to compare against to use either the singular or plural form.
#// @param string $context Context information for the translators.
#// @param string $domain  Optional. Text domain. Unique identifier for retrieving translated strings.
#// Default 'default'.
#// @return string The translated singular or plural form.
#//
def _nx(single_=None, plural_=None, number_=None, context_=None, domain_="default", *_args_):
    
    
    translations_ = get_translations_for_domain(domain_)
    translation_ = translations_.translate_plural(single_, plural_, number_, context_)
    #// 
    #// Filters the singular or plural form of a string with gettext context.
    #// 
    #// @since 2.8.0
    #// 
    #// @param string $translation Translated text.
    #// @param string $single      The text to be used if the number is singular.
    #// @param string $plural      The text to be used if the number is plural.
    #// @param string $number      The number to compare against to use either the singular or plural form.
    #// @param string $context     Context information for the translators.
    #// @param string $domain      Text domain. Unique identifier for retrieving translated strings.
    #//
    return apply_filters("ngettext_with_context", translation_, single_, plural_, number_, context_, domain_)
# end def _nx
#// 
#// Registers plural strings in POT file, but does not translate them.
#// 
#// Used when you want to keep structures with translatable plural
#// strings and use them later when the number is known.
#// 
#// Example:
#// 
#// $message = _n_noop( '%s post', '%s posts', 'text-domain' );
#// ...
#// printf( translate_nooped_plural( $message, $count, 'text-domain' ), number_format_i18n( $count ) );
#// 
#// @since 2.5.0
#// 
#// @param string $singular Singular form to be localized.
#// @param string $plural   Plural form to be localized.
#// @param string $domain   Optional. Text domain. Unique identifier for retrieving translated strings.
#// Default null.
#// @return array {
#// Array of translation information for the strings.
#// 
#// @type string $0        Singular form to be localized. No longer used.
#// @type string $1        Plural form to be localized. No longer used.
#// @type string $singular Singular form to be localized.
#// @type string $plural   Plural form to be localized.
#// @type null   $context  Context information for the translators.
#// @type string $domain   Text domain.
#// }
#//
def _n_noop(singular_=None, plural_=None, domain_=None, *_args_):
    if domain_ is None:
        domain_ = None
    # end if
    
    return Array({0: singular_, 1: plural_, "singular": singular_, "plural": plural_, "context": None, "domain": domain_})
# end def _n_noop
#// 
#// Registers plural strings with gettext context in POT file, but does not translate them.
#// 
#// Used when you want to keep structures with translatable plural
#// strings and use them later when the number is known.
#// 
#// Example of a generic phrase which is disambiguated via the context parameter:
#// 
#// $messages = array(
#// 'people'  => _nx_noop( '%s group', '%s groups', 'people', 'text-domain' ),
#// 'animals' => _nx_noop( '%s group', '%s groups', 'animals', 'text-domain' ),
#// );
#// ...
#// $message = $messages[ $type ];
#// printf( translate_nooped_plural( $message, $count, 'text-domain' ), number_format_i18n( $count ) );
#// 
#// @since 2.8.0
#// 
#// @param string $singular Singular form to be localized.
#// @param string $plural   Plural form to be localized.
#// @param string $context  Context information for the translators.
#// @param string $domain   Optional. Text domain. Unique identifier for retrieving translated strings.
#// Default null.
#// @return array {
#// Array of translation information for the strings.
#// 
#// @type string $0        Singular form to be localized. No longer used.
#// @type string $1        Plural form to be localized. No longer used.
#// @type string $2        Context information for the translators. No longer used.
#// @type string $singular Singular form to be localized.
#// @type string $plural   Plural form to be localized.
#// @type string $context  Context information for the translators.
#// @type string $domain   Text domain.
#// }
#//
def _nx_noop(singular_=None, plural_=None, context_=None, domain_=None, *_args_):
    if domain_ is None:
        domain_ = None
    # end if
    
    return Array({0: singular_, 1: plural_, 2: context_, "singular": singular_, "plural": plural_, "context": context_, "domain": domain_})
# end def _nx_noop
#// 
#// Translates and retrieves the singular or plural form of a string that's been registered
#// with _n_noop() or _nx_noop().
#// 
#// Used when you want to use a translatable plural string once the number is known.
#// 
#// Example:
#// 
#// $message = _n_noop( '%s post', '%s posts', 'text-domain' );
#// ...
#// printf( translate_nooped_plural( $message, $count, 'text-domain' ), number_format_i18n( $count ) );
#// 
#// @since 3.1.0
#// 
#// @param array  $nooped_plural Array with singular, plural, and context keys, usually the result of _n_noop() or _nx_noop().
#// @param int    $count         Number of objects.
#// @param string $domain        Optional. Text domain. Unique identifier for retrieving translated strings. If $nooped_plural contains
#// a text domain passed to _n_noop() or _nx_noop(), it will override this value. Default 'default'.
#// @return string Either $single or $plural translated text.
#//
def translate_nooped_plural(nooped_plural_=None, count_=None, domain_="default", *_args_):
    
    
    if nooped_plural_["domain"]:
        domain_ = nooped_plural_["domain"]
    # end if
    if nooped_plural_["context"]:
        return _nx(nooped_plural_["singular"], nooped_plural_["plural"], count_, nooped_plural_["context"], domain_)
    else:
        return _n(nooped_plural_["singular"], nooped_plural_["plural"], count_, domain_)
    # end if
# end def translate_nooped_plural
#// 
#// Load a .mo file into the text domain $domain.
#// 
#// If the text domain already exists, the translations will be merged. If both
#// sets have the same string, the translation from the original value will be taken.
#// 
#// On success, the .mo file will be placed in the $l10n global by $domain
#// and will be a MO object.
#// 
#// @since 1.5.0
#// 
#// @global MO[] $l10n          An array of all currently loaded text domains.
#// @global MO[] $l10n_unloaded An array of all text domains that have been unloaded again.
#// 
#// @param string $domain Text domain. Unique identifier for retrieving translated strings.
#// @param string $mofile Path to the .mo file.
#// @return bool True on success, false on failure.
#//
def load_textdomain(domain_=None, mofile_=None, *_args_):
    
    
    global l10n_
    global l10n_unloaded_
    php_check_if_defined("l10n_","l10n_unloaded_")
    l10n_unloaded_ = l10n_unloaded_
    #// 
    #// Filters whether to override the .mo file loading.
    #// 
    #// @since 2.9.0
    #// 
    #// @param bool   $override Whether to override the .mo file loading. Default false.
    #// @param string $domain   Text domain. Unique identifier for retrieving translated strings.
    #// @param string $mofile   Path to the MO file.
    #//
    plugin_override_ = apply_filters("override_load_textdomain", False, domain_, mofile_)
    if True == plugin_override_:
        l10n_unloaded_[domain_] = None
        return True
    # end if
    #// 
    #// Fires before the MO translation file is loaded.
    #// 
    #// @since 2.9.0
    #// 
    #// @param string $domain Text domain. Unique identifier for retrieving translated strings.
    #// @param string $mofile Path to the .mo file.
    #//
    do_action("load_textdomain", domain_, mofile_)
    #// 
    #// Filters MO file path for loading translations for a specific text domain.
    #// 
    #// @since 2.9.0
    #// 
    #// @param string $mofile Path to the MO file.
    #// @param string $domain Text domain. Unique identifier for retrieving translated strings.
    #//
    mofile_ = apply_filters("load_textdomain_mofile", mofile_, domain_)
    if (not php_is_readable(mofile_)):
        return False
    # end if
    mo_ = php_new_class("MO", lambda : MO())
    if (not mo_.import_from_file(mofile_)):
        return False
    # end if
    if (php_isset(lambda : l10n_[domain_])):
        mo_.merge_with(l10n_[domain_])
    # end if
    l10n_unloaded_[domain_] = None
    l10n_[domain_] = mo_
    return True
# end def load_textdomain
#// 
#// Unload translations for a text domain.
#// 
#// @since 3.0.0
#// 
#// @global MO[] $l10n          An array of all currently loaded text domains.
#// @global MO[] $l10n_unloaded An array of all text domains that have been unloaded again.
#// 
#// @param string $domain Text domain. Unique identifier for retrieving translated strings.
#// @return bool Whether textdomain was unloaded.
#//
def unload_textdomain(domain_=None, *_args_):
    
    
    global l10n_
    global l10n_unloaded_
    php_check_if_defined("l10n_","l10n_unloaded_")
    l10n_unloaded_ = l10n_unloaded_
    #// 
    #// Filters whether to override the text domain unloading.
    #// 
    #// @since 3.0.0
    #// 
    #// @param bool   $override Whether to override the text domain unloading. Default false.
    #// @param string $domain   Text domain. Unique identifier for retrieving translated strings.
    #//
    plugin_override_ = apply_filters("override_unload_textdomain", False, domain_)
    if plugin_override_:
        l10n_unloaded_[domain_] = True
        return True
    # end if
    #// 
    #// Fires before the text domain is unloaded.
    #// 
    #// @since 3.0.0
    #// 
    #// @param string $domain Text domain. Unique identifier for retrieving translated strings.
    #//
    do_action("unload_textdomain", domain_)
    if (php_isset(lambda : l10n_[domain_])):
        l10n_[domain_] = None
        l10n_unloaded_[domain_] = True
        return True
    # end if
    return False
# end def unload_textdomain
#// 
#// Load default translated strings based on locale.
#// 
#// Loads the .mo file in WP_LANG_DIR constant path from WordPress root.
#// The translated (.mo) file is named based on the locale.
#// 
#// @see load_textdomain()
#// 
#// @since 1.5.0
#// 
#// @param string $locale Optional. Locale to load. Default is the value of get_locale().
#// @return bool Whether the textdomain was loaded.
#//
def load_default_textdomain(locale_=None, *_args_):
    if locale_ is None:
        locale_ = None
    # end if
    
    if None == locale_:
        locale_ = determine_locale()
    # end if
    #// Unload previously loaded strings so we can switch translations.
    unload_textdomain("default")
    return_ = load_textdomain("default", WP_LANG_DIR + str("/") + str(locale_) + str(".mo"))
    if is_multisite() or php_defined("WP_INSTALLING_NETWORK") and WP_INSTALLING_NETWORK and (not php_file_exists(WP_LANG_DIR + str("/admin-") + str(locale_) + str(".mo"))):
        load_textdomain("default", WP_LANG_DIR + str("/ms-") + str(locale_) + str(".mo"))
        return return_
    # end if
    if is_admin() or wp_installing() or php_defined("WP_REPAIRING") and WP_REPAIRING:
        load_textdomain("default", WP_LANG_DIR + str("/admin-") + str(locale_) + str(".mo"))
    # end if
    if is_network_admin() or php_defined("WP_INSTALLING_NETWORK") and WP_INSTALLING_NETWORK:
        load_textdomain("default", WP_LANG_DIR + str("/admin-network-") + str(locale_) + str(".mo"))
    # end if
    return return_
# end def load_default_textdomain
#// 
#// Loads a plugin's translated strings.
#// 
#// If the path is not given then it will be the root of the plugin directory.
#// 
#// The .mo file should be named based on the text domain with a dash, and then the locale exactly.
#// 
#// @since 1.5.0
#// @since 4.6.0 The function now tries to load the .mo file from the languages directory first.
#// 
#// @param string       $domain          Unique identifier for retrieving translated strings
#// @param string|false $deprecated      Optional. Deprecated. Use the $plugin_rel_path parameter instead.
#// Default false.
#// @param string|false $plugin_rel_path Optional. Relative path to WP_PLUGIN_DIR where the .mo file resides.
#// Default false.
#// @return bool True when textdomain is successfully loaded, false otherwise.
#//
def load_plugin_textdomain(domain_=None, deprecated_=None, plugin_rel_path_=None, *_args_):
    if deprecated_ is None:
        deprecated_ = False
    # end if
    if plugin_rel_path_ is None:
        plugin_rel_path_ = False
    # end if
    
    #// 
    #// Filters a plugin's locale.
    #// 
    #// @since 3.0.0
    #// 
    #// @param string $locale The plugin's current locale.
    #// @param string $domain Text domain. Unique identifier for retrieving translated strings.
    #//
    locale_ = apply_filters("plugin_locale", determine_locale(), domain_)
    mofile_ = domain_ + "-" + locale_ + ".mo"
    #// Try to load from the languages directory first.
    if load_textdomain(domain_, WP_LANG_DIR + "/plugins/" + mofile_):
        return True
    # end if
    if False != plugin_rel_path_:
        path_ = WP_PLUGIN_DIR + "/" + php_trim(plugin_rel_path_, "/")
    elif False != deprecated_:
        _deprecated_argument(inspect.currentframe().f_code.co_name, "2.7.0")
        path_ = ABSPATH + php_trim(deprecated_, "/")
    else:
        path_ = WP_PLUGIN_DIR
    # end if
    return load_textdomain(domain_, path_ + "/" + mofile_)
# end def load_plugin_textdomain
#// 
#// Load the translated strings for a plugin residing in the mu-plugins directory.
#// 
#// @since 3.0.0
#// @since 4.6.0 The function now tries to load the .mo file from the languages directory first.
#// 
#// @param string $domain             Text domain. Unique identifier for retrieving translated strings.
#// @param string $mu_plugin_rel_path Optional. Relative to `WPMU_PLUGIN_DIR` directory in which the .mo
#// file resides. Default empty string.
#// @return bool True when textdomain is successfully loaded, false otherwise.
#//
def load_muplugin_textdomain(domain_=None, mu_plugin_rel_path_="", *_args_):
    
    
    #// This filter is documented in wp-includes/l10n.php
    locale_ = apply_filters("plugin_locale", determine_locale(), domain_)
    mofile_ = domain_ + "-" + locale_ + ".mo"
    #// Try to load from the languages directory first.
    if load_textdomain(domain_, WP_LANG_DIR + "/plugins/" + mofile_):
        return True
    # end if
    path_ = WPMU_PLUGIN_DIR + "/" + php_ltrim(mu_plugin_rel_path_, "/")
    return load_textdomain(domain_, path_ + "/" + mofile_)
# end def load_muplugin_textdomain
#// 
#// Load the theme's translated strings.
#// 
#// If the current locale exists as a .mo file in the theme's root directory, it
#// will be included in the translated strings by the $domain.
#// 
#// The .mo files must be named based on the locale exactly.
#// 
#// @since 1.5.0
#// @since 4.6.0 The function now tries to load the .mo file from the languages directory first.
#// 
#// @param string $domain Text domain. Unique identifier for retrieving translated strings.
#// @param string $path   Optional. Path to the directory containing the .mo file.
#// Default false.
#// @return bool True when textdomain is successfully loaded, false otherwise.
#//
def load_theme_textdomain(domain_=None, path_=None, *_args_):
    if path_ is None:
        path_ = False
    # end if
    
    #// 
    #// Filters a theme's locale.
    #// 
    #// @since 3.0.0
    #// 
    #// @param string $locale The theme's current locale.
    #// @param string $domain Text domain. Unique identifier for retrieving translated strings.
    #//
    locale_ = apply_filters("theme_locale", determine_locale(), domain_)
    mofile_ = domain_ + "-" + locale_ + ".mo"
    #// Try to load from the languages directory first.
    if load_textdomain(domain_, WP_LANG_DIR + "/themes/" + mofile_):
        return True
    # end if
    if (not path_):
        path_ = get_template_directory()
    # end if
    return load_textdomain(domain_, path_ + "/" + locale_ + ".mo")
# end def load_theme_textdomain
#// 
#// Load the child themes translated strings.
#// 
#// If the current locale exists as a .mo file in the child themes
#// root directory, it will be included in the translated strings by the $domain.
#// 
#// The .mo files must be named based on the locale exactly.
#// 
#// @since 2.9.0
#// 
#// @param string $domain Text domain. Unique identifier for retrieving translated strings.
#// @param string $path   Optional. Path to the directory containing the .mo file.
#// Default false.
#// @return bool True when the theme textdomain is successfully loaded, false otherwise.
#//
def load_child_theme_textdomain(domain_=None, path_=None, *_args_):
    if path_ is None:
        path_ = False
    # end if
    
    if (not path_):
        path_ = get_stylesheet_directory()
    # end if
    return load_theme_textdomain(domain_, path_)
# end def load_child_theme_textdomain
#// 
#// Loads the script translated strings.
#// 
#// @since 5.0.0
#// @since 5.0.2 Uses load_script_translations() to load translation data.
#// @since 5.1.0 The `$domain` parameter was made optional.
#// 
#// @see WP_Scripts::set_translations()
#// 
#// @param string $handle Name of the script to register a translation domain to.
#// @param string $domain Optional. Text domain. Default 'default'.
#// @param string $path   Optional. The full file path to the directory containing translation files.
#// @return string|false False if the script textdomain could not be loaded, the translated strings
#// in JSON encoding otherwise.
#//
def load_script_textdomain(handle_=None, domain_="default", path_=None, *_args_):
    if path_ is None:
        path_ = None
    # end if
    
    wp_scripts_ = wp_scripts()
    if (not (php_isset(lambda : wp_scripts_.registered[handle_]))):
        return False
    # end if
    path_ = untrailingslashit(path_)
    locale_ = determine_locale()
    #// If a path was given and the handle file exists simply return it.
    file_base_ = locale_ if "default" == domain_ else domain_ + "-" + locale_
    handle_filename_ = file_base_ + "-" + handle_ + ".json"
    if path_:
        translations_ = load_script_translations(path_ + "/" + handle_filename_, handle_, domain_)
        if translations_:
            return translations_
        # end if
    # end if
    src_ = wp_scripts_.registered[handle_].src
    if (not php_preg_match("|^(https?:)?//|", src_)) and (not wp_scripts_.content_url and 0 == php_strpos(src_, wp_scripts_.content_url)):
        src_ = wp_scripts_.base_url + src_
    # end if
    relative_ = False
    languages_path_ = WP_LANG_DIR
    src_url_ = wp_parse_url(src_)
    content_url_ = wp_parse_url(content_url())
    plugins_url_ = wp_parse_url(plugins_url())
    site_url_ = wp_parse_url(site_url())
    #// If the host is the same or it's a relative URL.
    if (not (php_isset(lambda : content_url_["path"]))) or php_strpos(src_url_["path"], content_url_["path"]) == 0 and (not (php_isset(lambda : src_url_["host"]))) or src_url_["host"] == content_url_["host"]:
        #// Make the src relative the specific plugin or theme.
        if (php_isset(lambda : content_url_["path"])):
            relative_ = php_substr(src_url_["path"], php_strlen(content_url_["path"]))
        else:
            relative_ = src_url_["path"]
        # end if
        relative_ = php_trim(relative_, "/")
        relative_ = php_explode("/", relative_)
        languages_path_ = WP_LANG_DIR + "/" + relative_[0]
        relative_ = php_array_slice(relative_, 2)
        #// Remove plugins/<plugin name> or themes/<theme name>.
        relative_ = php_implode("/", relative_)
    elif (not (php_isset(lambda : plugins_url_["path"]))) or php_strpos(src_url_["path"], plugins_url_["path"]) == 0 and (not (php_isset(lambda : src_url_["host"]))) or src_url_["host"] == plugins_url_["host"]:
        #// Make the src relative the specific plugin.
        if (php_isset(lambda : plugins_url_["path"])):
            relative_ = php_substr(src_url_["path"], php_strlen(plugins_url_["path"]))
        else:
            relative_ = src_url_["path"]
        # end if
        relative_ = php_trim(relative_, "/")
        relative_ = php_explode("/", relative_)
        languages_path_ = WP_LANG_DIR + "/plugins"
        relative_ = php_array_slice(relative_, 1)
        #// Remove <plugin name>.
        relative_ = php_implode("/", relative_)
    elif (not (php_isset(lambda : src_url_["host"]))) or src_url_["host"] == site_url_["host"]:
        if (not (php_isset(lambda : site_url_["path"]))):
            relative_ = php_trim(src_url_["path"], "/")
        elif php_strpos(src_url_["path"], trailingslashit(site_url_["path"])) == 0:
            #// Make the src relative to the WP root.
            relative_ = php_substr(src_url_["path"], php_strlen(site_url_["path"]))
            relative_ = php_trim(relative_, "/")
        # end if
    # end if
    #// 
    #// Filters the relative path of scripts used for finding translation files.
    #// 
    #// @since 5.0.2
    #// 
    #// @param string|false $relative The relative path of the script. False if it could not be determined.
    #// @param string       $src      The full source URL of the script.
    #//
    relative_ = apply_filters("load_script_textdomain_relative_path", relative_, src_)
    #// If the source is not from WP.
    if False == relative_:
        return load_script_translations(False, handle_, domain_)
    # end if
    #// Translations are always based on the unminified filename.
    if php_substr(relative_, -7) == ".min.js":
        relative_ = php_substr(relative_, 0, -7) + ".js"
    # end if
    md5_filename_ = file_base_ + "-" + php_md5(relative_) + ".json"
    if path_:
        translations_ = load_script_translations(path_ + "/" + md5_filename_, handle_, domain_)
        if translations_:
            return translations_
        # end if
    # end if
    translations_ = load_script_translations(languages_path_ + "/" + md5_filename_, handle_, domain_)
    if translations_:
        return translations_
    # end if
    return load_script_translations(False, handle_, domain_)
# end def load_script_textdomain
#// 
#// Loads the translation data for the given script handle and text domain.
#// 
#// @since 5.0.2
#// 
#// @param string|false $file   Path to the translation file to load. False if there isn't one.
#// @param string       $handle Name of the script to register a translation domain to.
#// @param string       $domain The text domain.
#// @return string|false The JSON-encoded translated strings for the given script handle and text domain. False if there are none.
#//
def load_script_translations(file_=None, handle_=None, domain_=None, *_args_):
    
    
    #// 
    #// Pre-filters script translations for the given file, script handle and text domain.
    #// 
    #// Returning a non-null value allows to override the default logic, effectively short-circuiting the function.
    #// 
    #// @since 5.0.2
    #// 
    #// @param string|false|null $translations JSON-encoded translation data. Default null.
    #// @param string|false      $file         Path to the translation file to load. False if there isn't one.
    #// @param string            $handle       Name of the script to register a translation domain to.
    #// @param string            $domain       The text domain.
    #//
    translations_ = apply_filters("pre_load_script_translations", None, file_, handle_, domain_)
    if None != translations_:
        return translations_
    # end if
    #// 
    #// Filters the file path for loading script translations for the given script handle and text domain.
    #// 
    #// @since 5.0.2
    #// 
    #// @param string|false $file   Path to the translation file to load. False if there isn't one.
    #// @param string       $handle Name of the script to register a translation domain to.
    #// @param string       $domain The text domain.
    #//
    file_ = apply_filters("load_script_translation_file", file_, handle_, domain_)
    if (not file_) or (not php_is_readable(file_)):
        return False
    # end if
    translations_ = php_file_get_contents(file_)
    #// 
    #// Filters script translations for the given file, script handle and text domain.
    #// 
    #// @since 5.0.2
    #// 
    #// @param string $translations JSON-encoded translation data.
    #// @param string $file         Path to the translation file that was loaded.
    #// @param string $handle       Name of the script to register a translation domain to.
    #// @param string $domain       The text domain.
    #//
    return apply_filters("load_script_translations", translations_, file_, handle_, domain_)
# end def load_script_translations
#// 
#// Loads plugin and theme textdomains just-in-time.
#// 
#// When a textdomain is encountered for the first time, we try to load
#// the translation file from `wp-content/languages`, removing the need
#// to call load_plugin_texdomain() or load_theme_texdomain().
#// 
#// @since 4.6.0
#// @access private
#// 
#// @see get_translations_for_domain()
#// @global MO[] $l10n_unloaded An array of all text domains that have been unloaded again.
#// 
#// @param string $domain Text domain. Unique identifier for retrieving translated strings.
#// @return bool True when the textdomain is successfully loaded, false otherwise.
#//
def _load_textdomain_just_in_time(domain_=None, *_args_):
    
    
    global l10n_unloaded_
    php_check_if_defined("l10n_unloaded_")
    l10n_unloaded_ = l10n_unloaded_
    #// Short-circuit if domain is 'default' which is reserved for core.
    if "default" == domain_ or (php_isset(lambda : l10n_unloaded_[domain_])):
        return False
    # end if
    translation_path_ = _get_path_to_translation(domain_)
    if False == translation_path_:
        return False
    # end if
    return load_textdomain(domain_, translation_path_)
# end def _load_textdomain_just_in_time
#// 
#// Gets the path to a translation file for loading a textdomain just in time.
#// 
#// Caches the retrieved results internally.
#// 
#// @since 4.7.0
#// @access private
#// 
#// @see _load_textdomain_just_in_time()
#// @staticvar array $available_translations
#// 
#// @param string $domain Text domain. Unique identifier for retrieving translated strings.
#// @param bool   $reset  Whether to reset the internal cache. Used by the switch to locale functionality.
#// @return string|false The path to the translation file or false if no translation file was found.
#//
def _get_path_to_translation(domain_=None, reset_=None, *_args_):
    if reset_ is None:
        reset_ = False
    # end if
    
    available_translations_ = Array()
    if True == reset_:
        available_translations_ = Array()
    # end if
    if (not (php_isset(lambda : available_translations_[domain_]))):
        available_translations_[domain_] = _get_path_to_translation_from_lang_dir(domain_)
    # end if
    return available_translations_[domain_]
# end def _get_path_to_translation
#// 
#// Gets the path to a translation file in the languages directory for the current locale.
#// 
#// Holds a cached list of available .mo files to improve performance.
#// 
#// @since 4.7.0
#// @access private
#// 
#// @see _get_path_to_translation()
#// @staticvar array $cached_mofiles
#// 
#// @param string $domain Text domain. Unique identifier for retrieving translated strings.
#// @return string|false The path to the translation file or false if no translation file was found.
#//
def _get_path_to_translation_from_lang_dir(domain_=None, *_args_):
    
    
    cached_mofiles_ = None
    if None == cached_mofiles_:
        cached_mofiles_ = Array()
        locations_ = Array(WP_LANG_DIR + "/plugins", WP_LANG_DIR + "/themes")
        for location_ in locations_:
            mofiles_ = glob(location_ + "/*.mo")
            if mofiles_:
                cached_mofiles_ = php_array_merge(cached_mofiles_, mofiles_)
            # end if
        # end for
    # end if
    locale_ = determine_locale()
    mofile_ = str(domain_) + str("-") + str(locale_) + str(".mo")
    path_ = WP_LANG_DIR + "/plugins/" + mofile_
    if php_in_array(path_, cached_mofiles_):
        return path_
    # end if
    path_ = WP_LANG_DIR + "/themes/" + mofile_
    if php_in_array(path_, cached_mofiles_):
        return path_
    # end if
    return False
# end def _get_path_to_translation_from_lang_dir
#// 
#// Return the Translations instance for a text domain.
#// 
#// If there isn't one, returns empty Translations instance.
#// 
#// @since 2.8.0
#// 
#// @global MO[] $l10n
#// @staticvar NOOP_Translations $noop_translations
#// 
#// @param string $domain Text domain. Unique identifier for retrieving translated strings.
#// @return Translations|NOOP_Translations A Translations instance.
#//
def get_translations_for_domain(domain_=None, *_args_):
    
    
    global l10n_
    php_check_if_defined("l10n_")
    if (php_isset(lambda : l10n_[domain_])) or _load_textdomain_just_in_time(domain_) and (php_isset(lambda : l10n_[domain_])):
        return l10n_[domain_]
    # end if
    noop_translations_ = None
    if None == noop_translations_:
        noop_translations_ = php_new_class("NOOP_Translations", lambda : NOOP_Translations())
    # end if
    return noop_translations_
# end def get_translations_for_domain
#// 
#// Whether there are translations for the text domain.
#// 
#// @since 3.0.0
#// 
#// @global MO[] $l10n
#// 
#// @param string $domain Text domain. Unique identifier for retrieving translated strings.
#// @return bool Whether there are translations.
#//
def is_textdomain_loaded(domain_=None, *_args_):
    
    
    global l10n_
    php_check_if_defined("l10n_")
    return (php_isset(lambda : l10n_[domain_]))
# end def is_textdomain_loaded
#// 
#// Translates role name.
#// 
#// Since the role names are in the database and not in the source there
#// are dummy gettext calls to get them into the POT file and this function
#// properly translates them back.
#// 
#// The before_last_bar() call is needed, because older installations keep the roles
#// using the old context format: 'Role name|User role' and just skipping the
#// content after the last bar is easier than fixing them in the DB. New installations
#// won't suffer from that problem.
#// 
#// @since 2.8.0
#// @since 5.2.0 Added the `$domain` parameter.
#// 
#// @param string $name   The role name.
#// @param string $domain Optional. Text domain. Unique identifier for retrieving translated strings.
#// Default 'default'.
#// @return string Translated role name on success, original name on failure.
#//
def translate_user_role(name_=None, domain_="default", *_args_):
    
    
    return translate_with_gettext_context(before_last_bar(name_), "User role", domain_)
# end def translate_user_role
#// 
#// Get all available languages based on the presence of *.mo files in a given directory.
#// 
#// The default directory is WP_LANG_DIR.
#// 
#// @since 3.0.0
#// @since 4.7.0 The results are now filterable with the {@see 'get_available_languages'} filter.
#// 
#// @param string $dir A directory to search for language files.
#// Default WP_LANG_DIR.
#// @return string[] An array of language codes or an empty array if no languages are present. Language codes are formed by stripping the .mo extension from the language file names.
#//
def get_available_languages(dir_=None, *_args_):
    if dir_ is None:
        dir_ = None
    # end if
    
    languages_ = Array()
    lang_files_ = glob(WP_LANG_DIR if php_is_null(dir_) else dir_ + "/*.mo")
    if lang_files_:
        for lang_file_ in lang_files_:
            lang_file_ = php_basename(lang_file_, ".mo")
            if 0 != php_strpos(lang_file_, "continents-cities") and 0 != php_strpos(lang_file_, "ms-") and 0 != php_strpos(lang_file_, "admin-"):
                languages_[-1] = lang_file_
            # end if
        # end for
    # end if
    #// 
    #// Filters the list of available language codes.
    #// 
    #// @since 4.7.0
    #// 
    #// @param string[] $languages An array of available language codes.
    #// @param string   $dir       The directory where the language files were found.
    #//
    return apply_filters("get_available_languages", languages_, dir_)
# end def get_available_languages
#// 
#// Get installed translations.
#// 
#// Looks in the wp-content/languages directory for translations of
#// plugins or themes.
#// 
#// @since 3.7.0
#// 
#// @param string $type What to search for. Accepts 'plugins', 'themes', 'core'.
#// @return array Array of language data.
#//
def wp_get_installed_translations(type_=None, *_args_):
    
    
    if "themes" != type_ and "plugins" != type_ and "core" != type_:
        return Array()
    # end if
    dir_ = "" if "core" == type_ else str("/") + str(type_)
    if (not php_is_dir(WP_LANG_DIR)):
        return Array()
    # end if
    if dir_ and (not php_is_dir(WP_LANG_DIR + dir_)):
        return Array()
    # end if
    files_ = scandir(WP_LANG_DIR + dir_)
    if (not files_):
        return Array()
    # end if
    language_data_ = Array()
    for file_ in files_:
        if "." == file_[0] or php_is_dir(WP_LANG_DIR + str(dir_) + str("/") + str(file_)):
            continue
        # end if
        if php_substr(file_, -3) != ".po":
            continue
        # end if
        if (not php_preg_match("/(?:(.+)-)?([a-z]{2,3}(?:_[A-Z]{2})?(?:_[a-z0-9]+)?).po/", file_, match_)):
            continue
        # end if
        if (not php_in_array(php_substr(file_, 0, -3) + ".mo", files_)):
            continue
        # end if
        textdomain_, language_ = match_
        if "" == textdomain_:
            textdomain_ = "default"
        # end if
        language_data_[textdomain_][language_] = wp_get_pomo_file_data(WP_LANG_DIR + str(dir_) + str("/") + str(file_))
    # end for
    return language_data_
# end def wp_get_installed_translations
#// 
#// Extract headers from a PO file.
#// 
#// @since 3.7.0
#// 
#// @param string $po_file Path to PO file.
#// @return string[] Array of PO file header values keyed by header name.
#//
def wp_get_pomo_file_data(po_file_=None, *_args_):
    
    
    headers_ = get_file_data(po_file_, Array({"POT-Creation-Date": "\"POT-Creation-Date", "PO-Revision-Date": "\"PO-Revision-Date", "Project-Id-Version": "\"Project-Id-Version", "X-Generator": "\"X-Generator"}))
    for header_,value_ in headers_.items():
        #// Remove possible contextual '\n' and closing double quote.
        headers_[header_] = php_preg_replace("~(\\\\n)?\"$~", "", value_)
    # end for
    return headers_
# end def wp_get_pomo_file_data
#// 
#// Language selector.
#// 
#// @since 4.0.0
#// @since 4.3.0 Introduced the `echo` argument.
#// @since 4.7.0 Introduced the `show_option_site_default` argument.
#// @since 5.1.0 Introduced the `show_option_en_us` argument.
#// 
#// @see get_available_languages()
#// @see wp_get_available_translations()
#// 
#// @param string|array $args {
#// Optional. Array or string of arguments for outputting the language selector.
#// 
#// @type string   $id                           ID attribute of the select element. Default 'locale'.
#// @type string   $name                         Name attribute of the select element. Default 'locale'.
#// @type array    $languages                    List of installed languages, contain only the locales.
#// Default empty array.
#// @type array    $translations                 List of available translations. Default result of
#// wp_get_available_translations().
#// @type string   $selected                     Language which should be selected. Default empty.
#// @type bool|int $echo                         Whether to echo the generated markup. Accepts 0, 1, or their
#// boolean equivalents. Default 1.
#// @type bool     $show_available_translations  Whether to show available translations. Default true.
#// @type bool     $show_option_site_default     Whether to show an option to fall back to the site's locale. Default false.
#// @type bool     $show_option_en_us            Whether to show an option for English (United States). Default true.
#// }
#// @return string HTML dropdown list of languages.
#//
def wp_dropdown_languages(args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    parsed_args_ = wp_parse_args(args_, Array({"id": "locale", "name": "locale", "languages": Array(), "translations": Array(), "selected": "", "echo": 1, "show_available_translations": True, "show_option_site_default": False, "show_option_en_us": True}))
    #// Bail if no ID or no name.
    if (not parsed_args_["id"]) or (not parsed_args_["name"]):
        return
    # end if
    #// English (United States) uses an empty string for the value attribute.
    if "en_US" == parsed_args_["selected"]:
        parsed_args_["selected"] = ""
    # end if
    translations_ = parsed_args_["translations"]
    if php_empty(lambda : translations_):
        php_include_file(ABSPATH + "wp-admin/includes/translation-install.php", once=True)
        translations_ = wp_get_available_translations()
    # end if
    #// 
    #// $parsed_args['languages'] should only contain the locales. Find the locale in
    #// $translations to get the native name. Fall back to locale.
    #//
    languages_ = Array()
    for locale_ in parsed_args_["languages"]:
        if (php_isset(lambda : translations_[locale_])):
            translation_ = translations_[locale_]
            languages_[-1] = Array({"language": translation_["language"], "native_name": translation_["native_name"], "lang": current(translation_["iso"])})
            translations_[locale_] = None
        else:
            languages_[-1] = Array({"language": locale_, "native_name": locale_, "lang": ""})
        # end if
    # end for
    translations_available_ = (not php_empty(lambda : translations_)) and parsed_args_["show_available_translations"]
    #// Holds the HTML markup.
    structure_ = Array()
    #// List installed languages.
    if translations_available_:
        structure_[-1] = "<optgroup label=\"" + esc_attr_x("Installed", "translations") + "\">"
    # end if
    #// Site default.
    if parsed_args_["show_option_site_default"]:
        structure_[-1] = php_sprintf("<option value=\"site-default\" data-installed=\"1\"%s>%s</option>", selected("site-default", parsed_args_["selected"], False), _x("Site Default", "default site language"))
    # end if
    if parsed_args_["show_option_en_us"]:
        structure_[-1] = php_sprintf("<option value=\"\" lang=\"en\" data-installed=\"1\"%s>English (United States)</option>", selected("", parsed_args_["selected"], False))
    # end if
    #// List installed languages.
    for language_ in languages_:
        structure_[-1] = php_sprintf("<option value=\"%s\" lang=\"%s\"%s data-installed=\"1\">%s</option>", esc_attr(language_["language"]), esc_attr(language_["lang"]), selected(language_["language"], parsed_args_["selected"], False), esc_html(language_["native_name"]))
    # end for
    if translations_available_:
        structure_[-1] = "</optgroup>"
    # end if
    #// List available translations.
    if translations_available_:
        structure_[-1] = "<optgroup label=\"" + esc_attr_x("Available", "translations") + "\">"
        for translation_ in translations_:
            structure_[-1] = php_sprintf("<option value=\"%s\" lang=\"%s\"%s>%s</option>", esc_attr(translation_["language"]), esc_attr(current(translation_["iso"])), selected(translation_["language"], parsed_args_["selected"], False), esc_html(translation_["native_name"]))
        # end for
        structure_[-1] = "</optgroup>"
    # end if
    #// Combine the output string.
    output_ = php_sprintf("<select name=\"%s\" id=\"%s\">", esc_attr(parsed_args_["name"]), esc_attr(parsed_args_["id"]))
    output_ += php_join("\n", structure_)
    output_ += "</select>"
    if parsed_args_["echo"]:
        php_print(output_)
    # end if
    return output_
# end def wp_dropdown_languages
#// 
#// Determines whether the current locale is right-to-left (RTL).
#// 
#// For more information on this and similar theme functions, check out
#// the {@link https://developer.wordpress.org/themes/basics/conditional-tags
#// Conditional Tags} article in the Theme Developer Handbook.
#// 
#// @since 3.0.0
#// 
#// @global WP_Locale $wp_locale WordPress date and time locale object.
#// 
#// @return bool Whether locale is RTL.
#//
def is_rtl(*_args_):
    
    
    global wp_locale_
    php_check_if_defined("wp_locale_")
    if (not type(wp_locale_).__name__ == "WP_Locale"):
        return False
    # end if
    return wp_locale_.is_rtl()
# end def is_rtl
#// 
#// Switches the translations according to the given locale.
#// 
#// @since 4.7.0
#// 
#// @global WP_Locale_Switcher $wp_locale_switcher WordPress locale switcher object.
#// 
#// @param string $locale The locale.
#// @return bool True on success, false on failure.
#//
def switch_to_locale(locale_=None, *_args_):
    
    
    #// @var WP_Locale_Switcher $wp_locale_switcher
    global wp_locale_switcher_
    php_check_if_defined("wp_locale_switcher_")
    return wp_locale_switcher_.switch_to_locale(locale_)
# end def switch_to_locale
#// 
#// Restores the translations according to the previous locale.
#// 
#// @since 4.7.0
#// 
#// @global WP_Locale_Switcher $wp_locale_switcher WordPress locale switcher object.
#// 
#// @return string|false Locale on success, false on error.
#//
def restore_previous_locale(*_args_):
    
    
    #// @var WP_Locale_Switcher $wp_locale_switcher
    global wp_locale_switcher_
    php_check_if_defined("wp_locale_switcher_")
    return wp_locale_switcher_.restore_previous_locale()
# end def restore_previous_locale
#// 
#// Restores the translations according to the original locale.
#// 
#// @since 4.7.0
#// 
#// @global WP_Locale_Switcher $wp_locale_switcher WordPress locale switcher object.
#// 
#// @return string|false Locale on success, false on error.
#//
def restore_current_locale(*_args_):
    
    
    #// @var WP_Locale_Switcher $wp_locale_switcher
    global wp_locale_switcher_
    php_check_if_defined("wp_locale_switcher_")
    return wp_locale_switcher_.restore_current_locale()
# end def restore_current_locale
#// 
#// Whether switch_to_locale() is in effect.
#// 
#// @since 4.7.0
#// 
#// @global WP_Locale_Switcher $wp_locale_switcher WordPress locale switcher object.
#// 
#// @return bool True if the locale has been switched, false otherwise.
#//
def is_locale_switched(*_args_):
    
    
    #// @var WP_Locale_Switcher $wp_locale_switcher
    global wp_locale_switcher_
    php_check_if_defined("wp_locale_switcher_")
    return wp_locale_switcher_.is_switched()
# end def is_locale_switched
