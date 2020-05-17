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
def translations_api(type_=None, args_=None, *_args_):
    
    
    #// Include an unmodified $wp_version.
    php_include_file(ABSPATH + WPINC + "/version.php", once=False)
    if (not php_in_array(type_, Array("plugins", "themes", "core"))):
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
    res_ = apply_filters("translations_api", False, type_, args_)
    if False == res_:
        url_ = "http://api.wordpress.org/translations/" + type_ + "/1.0/"
        http_url_ = url_
        ssl_ = wp_http_supports(Array("ssl"))
        if ssl_:
            url_ = set_url_scheme(url_, "https")
        # end if
        options_ = Array({"timeout": 3, "body": Array({"wp_version": wp_version_, "locale": get_locale(), "version": args_["version"]})})
        if "core" != type_:
            options_["body"]["slug"] = args_["slug"]
            pass
        # end if
        request_ = wp_remote_post(url_, options_)
        if ssl_ and is_wp_error(request_):
            trigger_error(php_sprintf(__("An unexpected error occurred. Something may be wrong with WordPress.org or this server&#8217;s configuration. If you continue to have problems, please try the <a href=\"%s\">support forums</a>."), __("https://wordpress.org/support/forums/")) + " " + __("(WordPress could not establish a secure connection to WordPress.org. Please contact your server administrator.)"), E_USER_WARNING if php_headers_sent() or WP_DEBUG else E_USER_NOTICE)
            request_ = wp_remote_post(http_url_, options_)
        # end if
        if is_wp_error(request_):
            res_ = php_new_class("WP_Error", lambda : WP_Error("translations_api_failed", php_sprintf(__("An unexpected error occurred. Something may be wrong with WordPress.org or this server&#8217;s configuration. If you continue to have problems, please try the <a href=\"%s\">support forums</a>."), __("https://wordpress.org/support/forums/")), request_.get_error_message()))
        else:
            res_ = php_json_decode(wp_remote_retrieve_body(request_), True)
            if (not php_is_object(res_)) and (not php_is_array(res_)):
                res_ = php_new_class("WP_Error", lambda : WP_Error("translations_api_failed", php_sprintf(__("An unexpected error occurred. Something may be wrong with WordPress.org or this server&#8217;s configuration. If you continue to have problems, please try the <a href=\"%s\">support forums</a>."), __("https://wordpress.org/support/forums/")), wp_remote_retrieve_body(request_)))
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
    return apply_filters("translations_api_result", res_, type_, args_)
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
def wp_get_available_translations(*_args_):
    
    
    if (not wp_installing()):
        translations_ = get_site_transient("available_translations")
        if False != translations_:
            return translations_
        # end if
    # end if
    #// Include an unmodified $wp_version.
    php_include_file(ABSPATH + WPINC + "/version.php", once=False)
    api_ = translations_api("core", Array({"version": wp_version_}))
    if is_wp_error(api_) or php_empty(lambda : api_["translations"]):
        return Array()
    # end if
    translations_ = Array()
    #// Key the array with the language code for now.
    for translation_ in api_["translations"]:
        translations_[translation_["language"]] = translation_
    # end for
    if (not php_defined("WP_INSTALLING")):
        set_site_transient("available_translations", translations_, 3 * HOUR_IN_SECONDS)
    # end if
    return translations_
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
def wp_install_language_form(languages_=None, *_args_):
    
    
    global wp_local_package_
    php_check_if_defined("wp_local_package_")
    installed_languages_ = get_available_languages()
    php_print("<label class='screen-reader-text' for='language'>Select a default language</label>\n")
    php_print("<select size='14' name='language' id='language'>\n")
    php_print("<option value=\"\" lang=\"en\" selected=\"selected\" data-continue=\"Continue\" data-installed=\"1\">English (United States)</option>")
    php_print("\n")
    if (not php_empty(lambda : wp_local_package_)) and (php_isset(lambda : languages_[wp_local_package_])):
        if (php_isset(lambda : languages_[wp_local_package_])):
            language_ = languages_[wp_local_package_]
            printf("<option value=\"%s\" lang=\"%s\" data-continue=\"%s\"%s>%s</option>" + "\n", esc_attr(language_["language"]), esc_attr(current(language_["iso"])), esc_attr(language_["strings"]["continue"] if language_["strings"]["continue"] else "Continue"), " data-installed=\"1\"" if php_in_array(language_["language"], installed_languages_) else "", esc_html(language_["native_name"]))
            languages_[wp_local_package_] = None
        # end if
    # end if
    for language_ in languages_:
        printf("<option value=\"%s\" lang=\"%s\" data-continue=\"%s\"%s>%s</option>" + "\n", esc_attr(language_["language"]), esc_attr(current(language_["iso"])), esc_attr(language_["strings"]["continue"] if language_["strings"]["continue"] else "Continue"), " data-installed=\"1\"" if php_in_array(language_["language"], installed_languages_) else "", esc_html(language_["native_name"]))
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
def wp_download_language_pack(download_=None, *_args_):
    
    
    #// Check if the translation is already installed.
    if php_in_array(download_, get_available_languages()):
        return download_
    # end if
    if (not wp_is_file_mod_allowed("download_language_pack")):
        return False
    # end if
    #// Confirm the translation is one we can download.
    translations_ = wp_get_available_translations()
    if (not translations_):
        return False
    # end if
    for translation_ in translations_:
        if translation_["language"] == download_:
            translation_to_load_ = True
            break
        # end if
    # end for
    if php_empty(lambda : translation_to_load_):
        return False
    # end if
    translation_ = translation_
    php_include_file(ABSPATH + "wp-admin/includes/class-wp-upgrader.php", once=True)
    skin_ = php_new_class("Automatic_Upgrader_Skin", lambda : Automatic_Upgrader_Skin())
    upgrader_ = php_new_class("Language_Pack_Upgrader", lambda : Language_Pack_Upgrader(skin_))
    translation_.type = "core"
    result_ = upgrader_.upgrade(translation_, Array({"clear_update_cache": False}))
    if (not result_) or is_wp_error(result_):
        return False
    # end if
    return translation_.language
# end def wp_download_language_pack
#// 
#// Check if WordPress has access to the filesystem without asking for
#// credentials.
#// 
#// @since 4.0.0
#// 
#// @return bool Returns true on success, false on failure.
#//
def wp_can_install_language_pack(*_args_):
    
    
    if (not wp_is_file_mod_allowed("can_install_language_pack")):
        return False
    # end if
    php_include_file(ABSPATH + "wp-admin/includes/class-wp-upgrader.php", once=True)
    skin_ = php_new_class("Automatic_Upgrader_Skin", lambda : Automatic_Upgrader_Skin())
    upgrader_ = php_new_class("Language_Pack_Upgrader", lambda : Language_Pack_Upgrader(skin_))
    upgrader_.init()
    check_ = upgrader_.fs_connect(Array(WP_CONTENT_DIR, WP_LANG_DIR))
    if (not check_) or is_wp_error(check_):
        return False
    # end if
    return True
# end def wp_can_install_language_pack
