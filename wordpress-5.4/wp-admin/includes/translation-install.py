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
#// WordPress Translation Installation Administration API
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// 
#// Retrieve translations from WordPress Translation API.
#// 
#// @since 4.0.0
#// 
#// @param string       $type Type of translations. Accepts 'plugins', 'themes', 'core'.
#// @param array|object $args Translation API arguments. Optional.
#// @return object|WP_Error On success an object of translations, WP_Error on failure.
#//
def translations_api(type=None, args=None, *args_):
    
    #// Include an unmodified $wp_version.
    php_include_file(ABSPATH + WPINC + "/version.php", once=False)
    if (not php_in_array(type, Array("plugins", "themes", "core"))):
        return php_new_class("WP_Error", lambda : WP_Error("invalid_type", __("Invalid translation type.")))
    # end if
    #// 
    #// Allows a plugin to override the WordPress.org Translation Installation API entirely.
    #// 
    #// @since 4.0.0
    #// 
    #// @param bool|array  $result The result object. Default false.
    #// @param string      $type   The type of translations being requested.
    #// @param object      $args   Translation API arguments.
    #//
    res = apply_filters("translations_api", False, type, args)
    if False == res:
        url = "http://api.wordpress.org/translations/" + type + "/1.0/"
        http_url = url
        ssl = wp_http_supports(Array("ssl"))
        if ssl:
            url = set_url_scheme(url, "https")
        # end if
        options = Array({"timeout": 3, "body": Array({"wp_version": wp_version, "locale": get_locale(), "version": args["version"]})})
        if "core" != type:
            options["body"]["slug"] = args["slug"]
            pass
        # end if
        request = wp_remote_post(url, options)
        if ssl and is_wp_error(request):
            trigger_error(php_sprintf(__("An unexpected error occurred. Something may be wrong with WordPress.org or this server&#8217;s configuration. If you continue to have problems, please try the <a href=\"%s\">support forums</a>."), __("https://wordpress.org/support/forums/")) + " " + __("(WordPress could not establish a secure connection to WordPress.org. Please contact your server administrator.)"), E_USER_WARNING if php_headers_sent() or WP_DEBUG else E_USER_NOTICE)
            request = wp_remote_post(http_url, options)
        # end if
        if is_wp_error(request):
            res = php_new_class("WP_Error", lambda : WP_Error("translations_api_failed", php_sprintf(__("An unexpected error occurred. Something may be wrong with WordPress.org or this server&#8217;s configuration. If you continue to have problems, please try the <a href=\"%s\">support forums</a>."), __("https://wordpress.org/support/forums/")), request.get_error_message()))
        else:
            res = php_json_decode(wp_remote_retrieve_body(request), True)
            if (not php_is_object(res)) and (not php_is_array(res)):
                res = php_new_class("WP_Error", lambda : WP_Error("translations_api_failed", php_sprintf(__("An unexpected error occurred. Something may be wrong with WordPress.org or this server&#8217;s configuration. If you continue to have problems, please try the <a href=\"%s\">support forums</a>."), __("https://wordpress.org/support/forums/")), wp_remote_retrieve_body(request)))
            # end if
        # end if
    # end if
    #// 
    #// Filters the Translation Installation API response results.
    #// 
    #// @since 4.0.0
    #// 
    #// @param object|WP_Error $res  Response object or WP_Error.
    #// @param string          $type The type of translations being requested.
    #// @param object          $args Translation API arguments.
    #//
    return apply_filters("translations_api_result", res, type, args)
# end def translations_api
#// 
#// Get available translations from the WordPress.org API.
#// 
#// @since 4.0.0
#// 
#// @see translations_api()
#// 
#// @return array[] Array of translations, each an array of data, keyed by the language. If the API response results
#// in an error, an empty array will be returned.
#//
def wp_get_available_translations(*args_):
    
    if (not wp_installing()):
        translations = get_site_transient("available_translations")
        if False != translations:
            return translations
        # end if
    # end if
    #// Include an unmodified $wp_version.
    php_include_file(ABSPATH + WPINC + "/version.php", once=False)
    api = translations_api("core", Array({"version": wp_version}))
    if is_wp_error(api) or php_empty(lambda : api["translations"]):
        return Array()
    # end if
    translations = Array()
    #// Key the array with the language code for now.
    for translation in api["translations"]:
        translations[translation["language"]] = translation
    # end for
    if (not php_defined("WP_INSTALLING")):
        set_site_transient("available_translations", translations, 3 * HOUR_IN_SECONDS)
    # end if
    return translations
# end def wp_get_available_translations
#// 
#// Output the select form for the language selection on the installation screen.
#// 
#// @since 4.0.0
#// 
#// @global string $wp_local_package Locale code of the package.
#// 
#// @param array[] $languages Array of available languages (populated via the Translation API).
#//
def wp_install_language_form(languages=None, *args_):
    
    global wp_local_package
    php_check_if_defined("wp_local_package")
    installed_languages = get_available_languages()
    php_print("<label class='screen-reader-text' for='language'>Select a default language</label>\n")
    php_print("<select size='14' name='language' id='language'>\n")
    php_print("<option value=\"\" lang=\"en\" selected=\"selected\" data-continue=\"Continue\" data-installed=\"1\">English (United States)</option>")
    php_print("\n")
    if (not php_empty(lambda : wp_local_package)) and (php_isset(lambda : languages[wp_local_package])):
        if (php_isset(lambda : languages[wp_local_package])):
            language = languages[wp_local_package]
            printf("<option value=\"%s\" lang=\"%s\" data-continue=\"%s\"%s>%s</option>" + "\n", esc_attr(language["language"]), esc_attr(current(language["iso"])), esc_attr(language["strings"]["continue"] if language["strings"]["continue"] else "Continue"), " data-installed=\"1\"" if php_in_array(language["language"], installed_languages) else "", esc_html(language["native_name"]))
            languages[wp_local_package] = None
        # end if
    # end if
    for language in languages:
        printf("<option value=\"%s\" lang=\"%s\" data-continue=\"%s\"%s>%s</option>" + "\n", esc_attr(language["language"]), esc_attr(current(language["iso"])), esc_attr(language["strings"]["continue"] if language["strings"]["continue"] else "Continue"), " data-installed=\"1\"" if php_in_array(language["language"], installed_languages) else "", esc_html(language["native_name"]))
    # end for
    php_print("</select>\n")
    php_print("<p class=\"step\"><span class=\"spinner\"></span><input id=\"language-continue\" type=\"submit\" class=\"button button-primary button-large\" value=\"Continue\" /></p>")
# end def wp_install_language_form
#// 
#// Download a language pack.
#// 
#// @since 4.0.0
#// 
#// @see wp_get_available_translations()
#// 
#// @param string $download Language code to download.
#// @return string|bool Returns the language code if successfully downloaded
#// (or already installed), or false on failure.
#//
def wp_download_language_pack(download=None, *args_):
    
    #// Check if the translation is already installed.
    if php_in_array(download, get_available_languages()):
        return download
    # end if
    if (not wp_is_file_mod_allowed("download_language_pack")):
        return False
    # end if
    #// Confirm the translation is one we can download.
    translations = wp_get_available_translations()
    if (not translations):
        return False
    # end if
    for translation in translations:
        if translation["language"] == download:
            translation_to_load = True
            break
        # end if
    # end for
    if php_empty(lambda : translation_to_load):
        return False
    # end if
    translation = translation
    php_include_file(ABSPATH + "wp-admin/includes/class-wp-upgrader.php", once=True)
    skin = php_new_class("Automatic_Upgrader_Skin", lambda : Automatic_Upgrader_Skin())
    upgrader = php_new_class("Language_Pack_Upgrader", lambda : Language_Pack_Upgrader(skin))
    translation.type = "core"
    result = upgrader.upgrade(translation, Array({"clear_update_cache": False}))
    if (not result) or is_wp_error(result):
        return False
    # end if
    return translation.language
# end def wp_download_language_pack
#// 
#// Check if WordPress has access to the filesystem without asking for
#// credentials.
#// 
#// @since 4.0.0
#// 
#// @return bool Returns true on success, false on failure.
#//
def wp_can_install_language_pack(*args_):
    
    if (not wp_is_file_mod_allowed("can_install_language_pack")):
        return False
    # end if
    php_include_file(ABSPATH + "wp-admin/includes/class-wp-upgrader.php", once=True)
    skin = php_new_class("Automatic_Upgrader_Skin", lambda : Automatic_Upgrader_Skin())
    upgrader = php_new_class("Language_Pack_Upgrader", lambda : Language_Pack_Upgrader(skin))
    upgrader.init()
    check = upgrader.fs_connect(Array(WP_CONTENT_DIR, WP_LANG_DIR))
    if (not check) or is_wp_error(check):
        return False
    # end if
    return True
# end def wp_can_install_language_pack
