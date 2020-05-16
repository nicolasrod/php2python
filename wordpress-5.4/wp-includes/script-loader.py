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
#// WordPress scripts and styles default loader.
#// 
#// Several constants are used to manage the loading, concatenating and compression of scripts and CSS:
#// define('SCRIPT_DEBUG', true); loads the development (non-minified) versions of all scripts and CSS, and disables compression and concatenation,
#// define('CONCATENATE_SCRIPTS', false); disables compression and concatenation of scripts and CSS,
#// define('COMPRESS_SCRIPTS', false); disables compression of scripts,
#// define('COMPRESS_CSS', false); disables compression of CSS,
#// define('ENFORCE_GZIP', true); forces gzip for compression (default is deflate).
#// 
#// The globals $concatenate_scripts, $compress_scripts and $compress_css can be set by plugins
#// to temporarily override the above settings. Also a compression test is run once and the result is saved
#// as option 'can_compress_scripts' (0/1). The test will run again if that option is deleted.
#// 
#// @package WordPress
#// 
#// WordPress Dependency Class
php_include_file(ABSPATH + WPINC + "/class-wp-dependency.php", once=False)
#// WordPress Dependencies Class
php_include_file(ABSPATH + WPINC + "/class.wp-dependencies.php", once=False)
#// WordPress Scripts Class
php_include_file(ABSPATH + WPINC + "/class.wp-scripts.php", once=False)
#// WordPress Scripts Functions
php_include_file(ABSPATH + WPINC + "/functions.wp-scripts.php", once=False)
#// WordPress Styles Class
php_include_file(ABSPATH + WPINC + "/class.wp-styles.php", once=False)
#// WordPress Styles Functions
php_include_file(ABSPATH + WPINC + "/functions.wp-styles.php", once=False)
#// 
#// Registers TinyMCE scripts.
#// 
#// @since 5.0.0
#// 
#// @param WP_Scripts $scripts WP_Scripts object.
#//
def wp_register_tinymce_scripts(scripts=None, force_uncompressed=False, *args_):
    
    global tinymce_version,concatenate_scripts,compress_scripts
    php_check_if_defined("tinymce_version","concatenate_scripts","compress_scripts")
    suffix = wp_scripts_get_suffix()
    dev_suffix = wp_scripts_get_suffix("dev")
    script_concat_settings()
    compressed = compress_scripts and concatenate_scripts and (php_isset(lambda : PHP_SERVER["HTTP_ACCEPT_ENCODING"])) and False != php_stripos(PHP_SERVER["HTTP_ACCEPT_ENCODING"], "gzip") and (not force_uncompressed)
    #// Load tinymce.js when running from /src, otherwise load wp-tinymce.js.gz (in production)
    #// or tinymce.min.js (when SCRIPT_DEBUG is true).
    if compressed:
        scripts.add("wp-tinymce", includes_url("js/tinymce/") + "wp-tinymce.js", Array(), tinymce_version)
    else:
        scripts.add("wp-tinymce-root", includes_url("js/tinymce/") + str("tinymce") + str(dev_suffix) + str(".js"), Array(), tinymce_version)
        scripts.add("wp-tinymce", includes_url("js/tinymce/") + str("plugins/compat3x/plugin") + str(dev_suffix) + str(".js"), Array("wp-tinymce-root"), tinymce_version)
    # end if
    scripts.add("wp-tinymce-lists", includes_url(str("js/tinymce/plugins/lists/plugin") + str(suffix) + str(".js")), Array("wp-tinymce"), tinymce_version)
# end def wp_register_tinymce_scripts
#// 
#// Registers all the WordPress vendor scripts that are in the standardized
#// `js/dist/vendor/` location.
#// 
#// For the order of `$scripts->add` see `wp_default_scripts`.
#// 
#// @since 5.0.0
#// 
#// @param WP_Scripts $scripts WP_Scripts object.
#//
def wp_default_packages_vendor(scripts=None, *args_):
    
    global wp_locale
    php_check_if_defined("wp_locale")
    suffix = wp_scripts_get_suffix()
    vendor_scripts = Array({"react": Array("wp-polyfill"), "react-dom": Array("react")}, "moment", "lodash", "wp-polyfill-fetch", "wp-polyfill-formdata", "wp-polyfill-node-contains", "wp-polyfill-url", "wp-polyfill-dom-rect", "wp-polyfill-element-closest", "wp-polyfill")
    vendor_scripts_versions = Array({"react": "16.9.0", "react-dom": "16.9.0", "moment": "2.22.2", "lodash": "4.17.15", "wp-polyfill-fetch": "3.0.0", "wp-polyfill-formdata": "3.0.12", "wp-polyfill-node-contains": "3.42.0", "wp-polyfill-url": "3.6.4", "wp-polyfill-dom-rect": "3.42.0", "wp-polyfill-element-closest": "2.0.2", "wp-polyfill": "7.4.4"})
    for handle,dependencies in vendor_scripts:
        if php_is_string(dependencies):
            handle = dependencies
            dependencies = Array()
        # end if
        path = str("/wp-includes/js/dist/vendor/") + str(handle) + str(suffix) + str(".js")
        version = vendor_scripts_versions[handle]
        scripts.add(handle, path, dependencies, version, 1)
    # end for
    scripts.add("wp-polyfill", None, Array("wp-polyfill"))
    did_action("init") and scripts.add_inline_script("wp-polyfill", wp_get_script_polyfill(scripts, Array({"'fetch' in window": "wp-polyfill-fetch", "document.contains": "wp-polyfill-node-contains", "window.DOMRect": "wp-polyfill-dom-rect", "window.URL && window.URL.prototype && window.URLSearchParams": "wp-polyfill-url", "window.FormData && window.FormData.prototype.keys": "wp-polyfill-formdata", "Element.prototype.matches && Element.prototype.closest": "wp-polyfill-element-closest"})))
    did_action("init") and scripts.add_inline_script("lodash", "window.lodash = _.noConflict();")
    did_action("init") and scripts.add_inline_script("moment", php_sprintf("moment.locale( '%s', %s );", get_user_locale(), wp_json_encode(Array({"months": php_array_values(wp_locale.month), "monthsShort": php_array_values(wp_locale.month_abbrev), "weekdays": php_array_values(wp_locale.weekday), "weekdaysShort": php_array_values(wp_locale.weekday_abbrev), "week": Array({"dow": php_int(get_option("start_of_week", 0))})}, {"longDateFormat": Array({"LT": get_option("time_format", __("g:i a", "default")), "LTS": None, "L": None, "LL": get_option("date_format", __("F j, Y", "default")), "LLL": __("F j, Y g:i a", "default"), "LLLL": None})}))), "after")
# end def wp_default_packages_vendor
#// 
#// Returns contents of an inline script used in appending polyfill scripts for
#// browsers which fail the provided tests. The provided array is a mapping from
#// a condition to verify feature support to its polyfill script handle.
#// 
#// @since 5.0.0
#// 
#// @param WP_Scripts $scripts WP_Scripts object.
#// @param array      $tests   Features to detect.
#// @return string Conditional polyfill inline script.
#//
def wp_get_script_polyfill(scripts=None, tests=None, *args_):
    
    polyfill = ""
    for test,handle in tests:
        if (not php_array_key_exists(handle, scripts.registered)):
            continue
        # end if
        src = scripts.registered[handle].src
        ver = scripts.registered[handle].ver
        if (not php_preg_match("|^(https?:)?//|", src)) and (not scripts.content_url and 0 == php_strpos(src, scripts.content_url)):
            src = scripts.base_url + src
        # end if
        if (not php_empty(lambda : ver)):
            src = add_query_arg("ver", ver, src)
        # end if
        #// This filter is documented in wp-includes/class.wp-scripts.php
        src = esc_url(apply_filters("script_loader_src", src, handle))
        if (not src):
            continue
        # end if
        polyfill += "( " + test + " ) || " + "document.write( '<script src=\"" + src + "\"></scr' + 'ipt>' );"
    # end for
    return polyfill
# end def wp_get_script_polyfill
#// 
#// Registers all the WordPress packages scripts that are in the standardized
#// `js/dist/` location.
#// 
#// For the order of `$scripts->add` see `wp_default_scripts`.
#// 
#// @since 5.0.0
#// 
#// @param WP_Scripts $scripts WP_Scripts object.
#//
def wp_default_packages_scripts(scripts=None, *args_):
    
    suffix = wp_scripts_get_suffix()
    #// Expects multidimensional array like:
    #// 'a11y.js' => array('dependencies' => array(...), 'version' => '...'),
    #// 'annotations.js' => array('dependencies' => array(...), 'version' => '...'),
    #// 'api-fetch.js' => array(...
    assets = php_include_file(ABSPATH + WPINC + "/assets/script-loader-packages.php", once=False)
    for package_name,package_data in assets:
        basename = php_basename(package_name, ".js")
        handle = "wp-" + basename
        path = str("/wp-includes/js/dist/") + str(basename) + str(suffix) + str(".js")
        if (not php_empty(lambda : package_data["dependencies"])):
            dependencies = package_data["dependencies"]
        else:
            dependencies = Array()
        # end if
        #// Add dependencies that cannot be detected and generated by build tools.
        for case in Switch(handle):
            if case("wp-block-library"):
                php_array_push(dependencies, "editor")
                break
            # end if
            if case("wp-edit-post"):
                php_array_push(dependencies, "media-models", "media-views", "postbox", "wp-dom-ready")
                break
            # end if
        # end for
        scripts.add(handle, path, dependencies, package_data["version"], 1)
        if php_in_array("wp-i18n", dependencies, True):
            scripts.set_translations(handle)
        # end if
    # end for
# end def wp_default_packages_scripts
#// 
#// Adds inline scripts required for the WordPress JavaScript packages.
#// 
#// @since 5.0.0
#// 
#// @param WP_Scripts $scripts WP_Scripts object.
#//
def wp_default_packages_inline_scripts(scripts=None, *args_):
    
    global wp_locale
    php_check_if_defined("wp_locale")
    if (php_isset(lambda : scripts.registered["wp-api-fetch"])):
        scripts.registered["wp-api-fetch"].deps[-1] = "wp-hooks"
    # end if
    scripts.add_inline_script("wp-api-fetch", php_sprintf("wp.apiFetch.use( wp.apiFetch.createRootURLMiddleware( \"%s\" ) );", esc_url_raw(get_rest_url())), "after")
    scripts.add_inline_script("wp-api-fetch", php_implode("\n", Array(php_sprintf("wp.apiFetch.nonceMiddleware = wp.apiFetch.createNonceMiddleware( \"%s\" );", "" if wp_installing() and (not is_multisite()) else wp_create_nonce("wp_rest")), "wp.apiFetch.use( wp.apiFetch.nonceMiddleware );", "wp.apiFetch.use( wp.apiFetch.mediaUploadMiddleware );", php_sprintf("wp.apiFetch.nonceEndpoint = \"%s\";", admin_url("admin-ajax.php?action=rest-nonce")))), "after")
    scripts.add_inline_script("wp-data", php_implode("\n", Array("( function() {", "    var userId = " + get_current_user_ID() + ";", " var storageKey = \"WP_DATA_USER_\" + userId;", "    wp.data", "     .use( wp.data.plugins.persistence, { storageKey: storageKey } );", "    wp.data.plugins.persistence.__unstableMigrate( { storageKey: storageKey } );", "} )();")))
    scripts.add_inline_script("wp-date", php_sprintf("wp.date.setSettings( %s );", wp_json_encode(Array({"l10n": Array({"locale": get_user_locale(), "months": php_array_values(wp_locale.month), "monthsShort": php_array_values(wp_locale.month_abbrev), "weekdays": php_array_values(wp_locale.weekday), "weekdaysShort": php_array_values(wp_locale.weekday_abbrev), "meridiem": wp_locale.meridiem, "relative": Array({"future": __("%s from now"), "past": __("%s ago")})})}, {"formats": Array({"time": get_option("time_format", __("g:i a")), "date": get_option("date_format", __("F j, Y")), "datetime": __("F j, Y g:i a"), "datetimeAbbreviated": __("M j, Y g:i a")})}, {"timezone": Array({"offset": get_option("gmt_offset", 0), "string": get_option("timezone_string", "UTC")})}))), "after")
    #// Loading the old editor and its config to ensure the classic block works as expected.
    scripts.add_inline_script("editor", "window.wp.oldEditor = window.wp.editor;", "after")
# end def wp_default_packages_inline_scripts
#// 
#// Adds inline scripts required for the TinyMCE in the block editor.
#// 
#// These TinyMCE init settings are used to extend and override the default settings
#// from `_WP_Editors::default_settings()` for the Classic block.
#// 
#// @since 5.0.0
#// 
#// @global WP_Scripts $wp_scripts
#//
def wp_tinymce_inline_scripts(*args_):
    
    global wp_scripts
    php_check_if_defined("wp_scripts")
    #// This filter is documented in wp-includes/class-wp-editor.php
    editor_settings = apply_filters("wp_editor_settings", Array({"tinymce": True}), "classic-block")
    tinymce_plugins = Array("charmap", "colorpicker", "hr", "lists", "media", "paste", "tabfocus", "textcolor", "fullscreen", "wordpress", "wpautoresize", "wpeditimage", "wpemoji", "wpgallery", "wplink", "wpdialogs", "wptextpattern", "wpview")
    #// This filter is documented in wp-includes/class-wp-editor.php
    tinymce_plugins = apply_filters("tiny_mce_plugins", tinymce_plugins, "classic-block")
    tinymce_plugins = array_unique(tinymce_plugins)
    disable_captions = False
    #// Runs after `tiny_mce_plugins` but before `mce_buttons`.
    #// This filter is documented in wp-admin/includes/media.php
    if apply_filters("disable_captions", ""):
        disable_captions = True
    # end if
    toolbar1 = Array("formatselect", "bold", "italic", "bullist", "numlist", "blockquote", "alignleft", "aligncenter", "alignright", "link", "unlink", "wp_more", "spellchecker", "wp_add_media", "wp_adv")
    #// This filter is documented in wp-includes/class-wp-editor.php
    toolbar1 = apply_filters("mce_buttons", toolbar1, "classic-block")
    toolbar2 = Array("strikethrough", "hr", "forecolor", "pastetext", "removeformat", "charmap", "outdent", "indent", "undo", "redo", "wp_help")
    #// This filter is documented in wp-includes/class-wp-editor.php
    toolbar2 = apply_filters("mce_buttons_2", toolbar2, "classic-block")
    #// This filter is documented in wp-includes/class-wp-editor.php
    toolbar3 = apply_filters("mce_buttons_3", Array(), "classic-block")
    #// This filter is documented in wp-includes/class-wp-editor.php
    toolbar4 = apply_filters("mce_buttons_4", Array(), "classic-block")
    #// This filter is documented in wp-includes/class-wp-editor.php
    external_plugins = apply_filters("mce_external_plugins", Array(), "classic-block")
    tinymce_settings = Array({"plugins": php_implode(",", tinymce_plugins), "toolbar1": php_implode(",", toolbar1), "toolbar2": php_implode(",", toolbar2), "toolbar3": php_implode(",", toolbar3), "toolbar4": php_implode(",", toolbar4), "external_plugins": wp_json_encode(external_plugins), "classic_block_editor": True})
    if disable_captions:
        tinymce_settings["wpeditimage_disable_captions"] = True
    # end if
    if (not php_empty(lambda : editor_settings["tinymce"])) and php_is_array(editor_settings["tinymce"]):
        php_array_merge(tinymce_settings, editor_settings["tinymce"])
    # end if
    #// This filter is documented in wp-includes/class-wp-editor.php
    tinymce_settings = apply_filters("tiny_mce_before_init", tinymce_settings, "classic-block")
    #// Do "by hand" translation from PHP array to js object.
    #// Prevents breakage in some custom settings.
    init_obj = ""
    for key,value in tinymce_settings:
        if php_is_bool(value):
            val = "true" if value else "false"
            init_obj += key + ":" + val + ","
            continue
        elif (not php_empty(lambda : value)) and php_is_string(value) and "{" == value[0] and "}" == value[php_strlen(value) - 1] or "[" == value[0] and "]" == value[php_strlen(value) - 1] or php_preg_match("/^\\(?function ?\\(/", value):
            init_obj += key + ":" + value + ","
            continue
        # end if
        init_obj += key + ":\"" + value + "\","
    # end for
    init_obj = "{" + php_trim(init_obj, " ,") + "}"
    script = "window.wpEditorL10n = {\n     tinymce: {\n            baseURL: " + wp_json_encode(includes_url("js/tinymce")) + ",\n          suffix: " + "\"\"" if SCRIPT_DEBUG else "\".min\"" + ",\n           settings: " + init_obj + ",\n       }\n }"
    wp_scripts.add_inline_script("wp-block-library", script, "before")
# end def wp_tinymce_inline_scripts
#// 
#// Registers all the WordPress packages scripts.
#// 
#// @since 5.0.0
#// 
#// @param WP_Scripts $scripts WP_Scripts object.
#//
def wp_default_packages(scripts=None, *args_):
    
    wp_default_packages_vendor(scripts)
    wp_register_tinymce_scripts(scripts)
    wp_default_packages_scripts(scripts)
    if did_action("init"):
        wp_default_packages_inline_scripts(scripts)
    # end if
# end def wp_default_packages
#// 
#// Returns the suffix that can be used for the scripts.
#// 
#// There are two suffix types, the normal one and the dev suffix.
#// 
#// @since 5.0.0
#// 
#// @param string $type The type of suffix to retrieve.
#// @return string The script suffix.
#//
def wp_scripts_get_suffix(type="", *args_):
    
    suffixes = None
    if None == suffixes:
        #// Include an unmodified $wp_version.
        php_include_file(ABSPATH + WPINC + "/version.php", once=False)
        develop_src = False != php_strpos(wp_version, "-src")
        if (not php_defined("SCRIPT_DEBUG")):
            php_define("SCRIPT_DEBUG", develop_src)
        # end if
        suffix = "" if SCRIPT_DEBUG else ".min"
        dev_suffix = "" if develop_src else ".min"
        suffixes = Array({"suffix": suffix, "dev_suffix": dev_suffix})
    # end if
    if "dev" == type:
        return suffixes["dev_suffix"]
    # end if
    return suffixes["suffix"]
# end def wp_scripts_get_suffix
#// 
#// Register all WordPress scripts.
#// 
#// Localizes some of them.
#// args order: `$scripts->add( 'handle', 'url', 'dependencies', 'query-string', 1 );`
#// when last arg === 1 queues the script for the footer
#// 
#// @since 2.6.0
#// 
#// @param WP_Scripts $scripts WP_Scripts object.
#//
def wp_default_scripts(scripts=None, *args_):
    
    suffix = wp_scripts_get_suffix()
    dev_suffix = wp_scripts_get_suffix("dev")
    guessurl = site_url()
    if (not guessurl):
        guessed_url = True
        guessurl = wp_guess_url()
    # end if
    scripts.base_url = guessurl
    scripts.content_url = WP_CONTENT_URL if php_defined("WP_CONTENT_URL") else ""
    scripts.default_version = get_bloginfo("version")
    scripts.default_dirs = Array("/wp-admin/js/", "/wp-includes/js/")
    scripts.add("utils", str("/wp-includes/js/utils") + str(suffix) + str(".js"))
    did_action("init") and scripts.localize("utils", "userSettings", Array({"url": php_str(SITECOOKIEPATH), "uid": php_str(get_current_user_id()), "time": php_str(time()), "secure": php_str("https" == php_parse_url(site_url(), PHP_URL_SCHEME))}))
    scripts.add("common", str("/wp-admin/js/common") + str(suffix) + str(".js"), Array("jquery", "hoverIntent", "utils"), False, 1)
    did_action("init") and scripts.localize("common", "commonL10n", Array({"warnDelete": __("You are about to permanently delete these items from your site.\nThis action cannot be undone.\n 'Cancel' to stop, 'OK' to delete."), "dismiss": __("Dismiss this notice."), "collapseMenu": __("Collapse Main menu"), "expandMenu": __("Expand Main menu")}))
    scripts.add("wp-sanitize", str("/wp-includes/js/wp-sanitize") + str(suffix) + str(".js"), Array(), False, 1)
    scripts.add("sack", str("/wp-includes/js/tw-sack") + str(suffix) + str(".js"), Array(), "1.6.1", 1)
    scripts.add("quicktags", str("/wp-includes/js/quicktags") + str(suffix) + str(".js"), Array(), False, 1)
    did_action("init") and scripts.localize("quicktags", "quicktagsL10n", Array({"closeAllOpenTags": __("Close all open tags"), "closeTags": __("close tags"), "enterURL": __("Enter the URL"), "enterImageURL": __("Enter the URL of the image"), "enterImageDescription": __("Enter a description of the image"), "textdirection": __("text direction"), "toggleTextdirection": __("Toggle Editor Text Direction"), "dfw": __("Distraction-free writing mode"), "strong": __("Bold"), "strongClose": __("Close bold tag"), "em": __("Italic"), "emClose": __("Close italic tag"), "link": __("Insert link"), "blockquote": __("Blockquote"), "blockquoteClose": __("Close blockquote tag"), "del": __("Deleted text (strikethrough)"), "delClose": __("Close deleted text tag"), "ins": __("Inserted text"), "insClose": __("Close inserted text tag"), "image": __("Insert image"), "ul": __("Bulleted list"), "ulClose": __("Close bulleted list tag"), "ol": __("Numbered list"), "olClose": __("Close numbered list tag"), "li": __("List item"), "liClose": __("Close list item tag"), "code": __("Code"), "codeClose": __("Close code tag"), "more": __("Insert Read More tag")}))
    scripts.add("colorpicker", str("/wp-includes/js/colorpicker") + str(suffix) + str(".js"), Array("prototype"), "3517m")
    scripts.add("editor", str("/wp-admin/js/editor") + str(suffix) + str(".js"), Array("utils", "jquery"), False, 1)
    scripts.add("clipboard", str("/wp-includes/js/clipboard") + str(suffix) + str(".js"), Array(), False, 1)
    scripts.add("wp-ajax-response", str("/wp-includes/js/wp-ajax-response") + str(suffix) + str(".js"), Array("jquery"), False, 1)
    did_action("init") and scripts.localize("wp-ajax-response", "wpAjax", Array({"noPerm": __("Sorry, you are not allowed to do that."), "broken": __("Something went wrong.")}))
    scripts.add("wp-api-request", str("/wp-includes/js/api-request") + str(suffix) + str(".js"), Array("jquery"), False, 1)
    #// `wpApiSettings` is also used by `wp-api`, which depends on this script.
    did_action("init") and scripts.localize("wp-api-request", "wpApiSettings", Array({"root": esc_url_raw(get_rest_url()), "nonce": "" if wp_installing() and (not is_multisite()) else wp_create_nonce("wp_rest"), "versionString": "wp/v2/"}))
    scripts.add("wp-pointer", str("/wp-includes/js/wp-pointer") + str(suffix) + str(".js"), Array("jquery-ui-widget", "jquery-ui-position"), "20111129a", 1)
    did_action("init") and scripts.localize("wp-pointer", "wpPointerL10n", Array({"dismiss": __("Dismiss")}))
    scripts.add("autosave", str("/wp-includes/js/autosave") + str(suffix) + str(".js"), Array("heartbeat"), False, 1)
    scripts.add("heartbeat", str("/wp-includes/js/heartbeat") + str(suffix) + str(".js"), Array("jquery", "wp-hooks"), False, 1)
    did_action("init") and scripts.localize("heartbeat", "heartbeatSettings", apply_filters("heartbeat_settings", Array()))
    scripts.add("wp-auth-check", str("/wp-includes/js/wp-auth-check") + str(suffix) + str(".js"), Array("heartbeat"), False, 1)
    did_action("init") and scripts.localize("wp-auth-check", "authcheckL10n", Array({"beforeunload": __("Your session has expired. You can log in again from this page or go to the login page."), "interval": apply_filters("wp_auth_check_interval", 3 * MINUTE_IN_SECONDS)}))
    scripts.add("wp-lists", str("/wp-includes/js/wp-lists") + str(suffix) + str(".js"), Array("wp-ajax-response", "jquery-color"), False, 1)
    #// WordPress no longer uses or bundles Prototype or script.aculo.us. These are now pulled from an external source.
    scripts.add("prototype", "https://ajax.googleapis.com/ajax/libs/prototype/1.7.1.0/prototype.js", Array(), "1.7.1")
    scripts.add("scriptaculous-root", "https://ajax.googleapis.com/ajax/libs/scriptaculous/1.9.0/scriptaculous.js", Array("prototype"), "1.9.0")
    scripts.add("scriptaculous-builder", "https://ajax.googleapis.com/ajax/libs/scriptaculous/1.9.0/builder.js", Array("scriptaculous-root"), "1.9.0")
    scripts.add("scriptaculous-dragdrop", "https://ajax.googleapis.com/ajax/libs/scriptaculous/1.9.0/dragdrop.js", Array("scriptaculous-builder", "scriptaculous-effects"), "1.9.0")
    scripts.add("scriptaculous-effects", "https://ajax.googleapis.com/ajax/libs/scriptaculous/1.9.0/effects.js", Array("scriptaculous-root"), "1.9.0")
    scripts.add("scriptaculous-slider", "https://ajax.googleapis.com/ajax/libs/scriptaculous/1.9.0/slider.js", Array("scriptaculous-effects"), "1.9.0")
    scripts.add("scriptaculous-sound", "https://ajax.googleapis.com/ajax/libs/scriptaculous/1.9.0/sound.js", Array("scriptaculous-root"), "1.9.0")
    scripts.add("scriptaculous-controls", "https://ajax.googleapis.com/ajax/libs/scriptaculous/1.9.0/controls.js", Array("scriptaculous-root"), "1.9.0")
    scripts.add("scriptaculous", False, Array("scriptaculous-dragdrop", "scriptaculous-slider", "scriptaculous-controls"))
    #// Not used in core, replaced by Jcrop.js.
    scripts.add("cropper", "/wp-includes/js/crop/cropper.js", Array("scriptaculous-dragdrop"))
    #// jQuery.
    scripts.add("jquery", False, Array("jquery-core", "jquery-migrate"), "1.12.4-wp")
    scripts.add("jquery-core", "/wp-includes/js/jquery/jquery.js", Array(), "1.12.4-wp")
    scripts.add("jquery-migrate", str("/wp-includes/js/jquery/jquery-migrate") + str(suffix) + str(".js"), Array(), "1.4.1")
    #// Full jQuery UI.
    scripts.add("jquery-ui-core", str("/wp-includes/js/jquery/ui/core") + str(dev_suffix) + str(".js"), Array("jquery"), "1.11.4", 1)
    scripts.add("jquery-effects-core", str("/wp-includes/js/jquery/ui/effect") + str(dev_suffix) + str(".js"), Array("jquery"), "1.11.4", 1)
    scripts.add("jquery-effects-blind", str("/wp-includes/js/jquery/ui/effect-blind") + str(dev_suffix) + str(".js"), Array("jquery-effects-core"), "1.11.4", 1)
    scripts.add("jquery-effects-bounce", str("/wp-includes/js/jquery/ui/effect-bounce") + str(dev_suffix) + str(".js"), Array("jquery-effects-core"), "1.11.4", 1)
    scripts.add("jquery-effects-clip", str("/wp-includes/js/jquery/ui/effect-clip") + str(dev_suffix) + str(".js"), Array("jquery-effects-core"), "1.11.4", 1)
    scripts.add("jquery-effects-drop", str("/wp-includes/js/jquery/ui/effect-drop") + str(dev_suffix) + str(".js"), Array("jquery-effects-core"), "1.11.4", 1)
    scripts.add("jquery-effects-explode", str("/wp-includes/js/jquery/ui/effect-explode") + str(dev_suffix) + str(".js"), Array("jquery-effects-core"), "1.11.4", 1)
    scripts.add("jquery-effects-fade", str("/wp-includes/js/jquery/ui/effect-fade") + str(dev_suffix) + str(".js"), Array("jquery-effects-core"), "1.11.4", 1)
    scripts.add("jquery-effects-fold", str("/wp-includes/js/jquery/ui/effect-fold") + str(dev_suffix) + str(".js"), Array("jquery-effects-core"), "1.11.4", 1)
    scripts.add("jquery-effects-highlight", str("/wp-includes/js/jquery/ui/effect-highlight") + str(dev_suffix) + str(".js"), Array("jquery-effects-core"), "1.11.4", 1)
    scripts.add("jquery-effects-puff", str("/wp-includes/js/jquery/ui/effect-puff") + str(dev_suffix) + str(".js"), Array("jquery-effects-core", "jquery-effects-scale"), "1.11.4", 1)
    scripts.add("jquery-effects-pulsate", str("/wp-includes/js/jquery/ui/effect-pulsate") + str(dev_suffix) + str(".js"), Array("jquery-effects-core"), "1.11.4", 1)
    scripts.add("jquery-effects-scale", str("/wp-includes/js/jquery/ui/effect-scale") + str(dev_suffix) + str(".js"), Array("jquery-effects-core", "jquery-effects-size"), "1.11.4", 1)
    scripts.add("jquery-effects-shake", str("/wp-includes/js/jquery/ui/effect-shake") + str(dev_suffix) + str(".js"), Array("jquery-effects-core"), "1.11.4", 1)
    scripts.add("jquery-effects-size", str("/wp-includes/js/jquery/ui/effect-size") + str(dev_suffix) + str(".js"), Array("jquery-effects-core"), "1.11.4", 1)
    scripts.add("jquery-effects-slide", str("/wp-includes/js/jquery/ui/effect-slide") + str(dev_suffix) + str(".js"), Array("jquery-effects-core"), "1.11.4", 1)
    scripts.add("jquery-effects-transfer", str("/wp-includes/js/jquery/ui/effect-transfer") + str(dev_suffix) + str(".js"), Array("jquery-effects-core"), "1.11.4", 1)
    scripts.add("jquery-ui-accordion", str("/wp-includes/js/jquery/ui/accordion") + str(dev_suffix) + str(".js"), Array("jquery-ui-core", "jquery-ui-widget"), "1.11.4", 1)
    scripts.add("jquery-ui-autocomplete", str("/wp-includes/js/jquery/ui/autocomplete") + str(dev_suffix) + str(".js"), Array("jquery-ui-menu", "wp-a11y"), "1.11.4", 1)
    scripts.add("jquery-ui-button", str("/wp-includes/js/jquery/ui/button") + str(dev_suffix) + str(".js"), Array("jquery-ui-core", "jquery-ui-widget"), "1.11.4", 1)
    scripts.add("jquery-ui-datepicker", str("/wp-includes/js/jquery/ui/datepicker") + str(dev_suffix) + str(".js"), Array("jquery-ui-core"), "1.11.4", 1)
    scripts.add("jquery-ui-dialog", str("/wp-includes/js/jquery/ui/dialog") + str(dev_suffix) + str(".js"), Array("jquery-ui-resizable", "jquery-ui-draggable", "jquery-ui-button", "jquery-ui-position"), "1.11.4", 1)
    scripts.add("jquery-ui-draggable", str("/wp-includes/js/jquery/ui/draggable") + str(dev_suffix) + str(".js"), Array("jquery-ui-mouse"), "1.11.4", 1)
    scripts.add("jquery-ui-droppable", str("/wp-includes/js/jquery/ui/droppable") + str(dev_suffix) + str(".js"), Array("jquery-ui-draggable"), "1.11.4", 1)
    scripts.add("jquery-ui-menu", str("/wp-includes/js/jquery/ui/menu") + str(dev_suffix) + str(".js"), Array("jquery-ui-core", "jquery-ui-widget", "jquery-ui-position"), "1.11.4", 1)
    scripts.add("jquery-ui-mouse", str("/wp-includes/js/jquery/ui/mouse") + str(dev_suffix) + str(".js"), Array("jquery-ui-core", "jquery-ui-widget"), "1.11.4", 1)
    scripts.add("jquery-ui-position", str("/wp-includes/js/jquery/ui/position") + str(dev_suffix) + str(".js"), Array("jquery"), "1.11.4", 1)
    scripts.add("jquery-ui-progressbar", str("/wp-includes/js/jquery/ui/progressbar") + str(dev_suffix) + str(".js"), Array("jquery-ui-core", "jquery-ui-widget"), "1.11.4", 1)
    scripts.add("jquery-ui-resizable", str("/wp-includes/js/jquery/ui/resizable") + str(dev_suffix) + str(".js"), Array("jquery-ui-mouse"), "1.11.4", 1)
    scripts.add("jquery-ui-selectable", str("/wp-includes/js/jquery/ui/selectable") + str(dev_suffix) + str(".js"), Array("jquery-ui-mouse"), "1.11.4", 1)
    scripts.add("jquery-ui-selectmenu", str("/wp-includes/js/jquery/ui/selectmenu") + str(dev_suffix) + str(".js"), Array("jquery-ui-menu"), "1.11.4", 1)
    scripts.add("jquery-ui-slider", str("/wp-includes/js/jquery/ui/slider") + str(dev_suffix) + str(".js"), Array("jquery-ui-mouse"), "1.11.4", 1)
    scripts.add("jquery-ui-sortable", str("/wp-includes/js/jquery/ui/sortable") + str(dev_suffix) + str(".js"), Array("jquery-ui-mouse"), "1.11.4", 1)
    scripts.add("jquery-ui-spinner", str("/wp-includes/js/jquery/ui/spinner") + str(dev_suffix) + str(".js"), Array("jquery-ui-button"), "1.11.4", 1)
    scripts.add("jquery-ui-tabs", str("/wp-includes/js/jquery/ui/tabs") + str(dev_suffix) + str(".js"), Array("jquery-ui-core", "jquery-ui-widget"), "1.11.4", 1)
    scripts.add("jquery-ui-tooltip", str("/wp-includes/js/jquery/ui/tooltip") + str(dev_suffix) + str(".js"), Array("jquery-ui-core", "jquery-ui-widget", "jquery-ui-position"), "1.11.4", 1)
    scripts.add("jquery-ui-widget", str("/wp-includes/js/jquery/ui/widget") + str(dev_suffix) + str(".js"), Array("jquery"), "1.11.4", 1)
    #// Strings for 'jquery-ui-autocomplete' live region messages.
    did_action("init") and scripts.localize("jquery-ui-autocomplete", "uiAutocompleteL10n", Array({"noResults": __("No results found."), "oneResult": __("1 result found. Use up and down arrow keys to navigate."), "manyResults": __("%d results found. Use up and down arrow keys to navigate."), "itemSelected": __("Item selected.")}))
    #// Deprecated, not used in core, most functionality is included in jQuery 1.3.
    scripts.add("jquery-form", str("/wp-includes/js/jquery/jquery.form") + str(suffix) + str(".js"), Array("jquery"), "4.2.1", 1)
    #// jQuery plugins.
    scripts.add("jquery-color", "/wp-includes/js/jquery/jquery.color.min.js", Array("jquery"), "2.1.2", 1)
    scripts.add("schedule", "/wp-includes/js/jquery/jquery.schedule.js", Array("jquery"), "20m", 1)
    scripts.add("jquery-query", "/wp-includes/js/jquery/jquery.query.js", Array("jquery"), "2.1.7", 1)
    scripts.add("jquery-serialize-object", "/wp-includes/js/jquery/jquery.serialize-object.js", Array("jquery"), "0.2", 1)
    scripts.add("jquery-hotkeys", str("/wp-includes/js/jquery/jquery.hotkeys") + str(suffix) + str(".js"), Array("jquery"), "0.0.2m", 1)
    scripts.add("jquery-table-hotkeys", str("/wp-includes/js/jquery/jquery.table-hotkeys") + str(suffix) + str(".js"), Array("jquery", "jquery-hotkeys"), False, 1)
    scripts.add("jquery-touch-punch", "/wp-includes/js/jquery/jquery.ui.touch-punch.js", Array("jquery-ui-widget", "jquery-ui-mouse"), "0.2.2", 1)
    #// Not used any more, registered for backward compatibility.
    scripts.add("suggest", str("/wp-includes/js/jquery/suggest") + str(suffix) + str(".js"), Array("jquery"), "1.1-20110113", 1)
    #// Masonry v2 depended on jQuery. v3 does not. The older jquery-masonry handle is a shiv.
    #// It sets jQuery as a dependency, as the theme may have been implicitly loading it this way.
    scripts.add("imagesloaded", "/wp-includes/js/imagesloaded.min.js", Array(), "3.2.0", 1)
    scripts.add("masonry", "/wp-includes/js/masonry.min.js", Array("imagesloaded"), "3.3.2", 1)
    scripts.add("jquery-masonry", str("/wp-includes/js/jquery/jquery.masonry") + str(dev_suffix) + str(".js"), Array("jquery", "masonry"), "3.1.2b", 1)
    scripts.add("thickbox", "/wp-includes/js/thickbox/thickbox.js", Array("jquery"), "3.1-20121105", 1)
    did_action("init") and scripts.localize("thickbox", "thickboxL10n", Array({"next": __("Next &gt;"), "prev": __("&lt; Prev"), "image": __("Image"), "of": __("of"), "close": __("Close"), "noiframes": __("This feature requires inline frames. You have iframes disabled or your browser does not support them."), "loadingAnimation": includes_url("js/thickbox/loadingAnimation.gif")}))
    scripts.add("jcrop", "/wp-includes/js/jcrop/jquery.Jcrop.min.js", Array("jquery"), "0.9.12")
    scripts.add("swfobject", "/wp-includes/js/swfobject.js", Array(), "2.2-20120417")
    #// Error messages for Plupload.
    uploader_l10n = Array({"queue_limit_exceeded": __("You have attempted to queue too many files."), "file_exceeds_size_limit": __("%s exceeds the maximum upload size for this site."), "zero_byte_file": __("This file is empty. Please try another."), "invalid_filetype": __("Sorry, this file type is not permitted for security reasons."), "not_an_image": __("This file is not an image. Please try another."), "image_memory_exceeded": __("Memory exceeded. Please try another smaller file."), "image_dimensions_exceeded": __("This is larger than the maximum size. Please try another."), "default_error": __("An error occurred in the upload. Please try again later."), "missing_upload_url": __("There was a configuration error. Please contact the server administrator."), "upload_limit_exceeded": __("You may only upload 1 file."), "http_error": __("Unexpected response from the server. The file may have been uploaded successfully. Check in the Media Library or reload the page."), "http_error_image": __("Post-processing of the image failed likely because the server is busy or does not have enough resources. Uploading a smaller image may help. Suggested maximum size is 2500 pixels."), "upload_failed": __("Upload failed."), "big_upload_failed": __("Please try uploading this file with the %1$sbrowser uploader%2$s."), "big_upload_queued": __("%s exceeds the maximum upload size for the multi-file uploader when used in your browser."), "io_error": __("IO error."), "security_error": __("Security error."), "file_cancelled": __("File canceled."), "upload_stopped": __("Upload stopped."), "dismiss": __("Dismiss"), "crunching": __("Crunching&hellip;"), "deleted": __("moved to the Trash."), "error_uploading": __("&#8220;%s&#8221; has failed to upload.")})
    scripts.add("moxiejs", str("/wp-includes/js/plupload/moxie") + str(suffix) + str(".js"), Array(), "1.3.5")
    scripts.add("plupload", str("/wp-includes/js/plupload/plupload") + str(suffix) + str(".js"), Array("moxiejs"), "2.1.9")
    #// Back compat handles:
    for handle in Array("all", "html5", "flash", "silverlight", "html4"):
        scripts.add(str("plupload-") + str(handle), False, Array("plupload"), "2.1.1")
    # end for
    scripts.add("plupload-handlers", str("/wp-includes/js/plupload/handlers") + str(suffix) + str(".js"), Array("plupload", "jquery"))
    did_action("init") and scripts.localize("plupload-handlers", "pluploadL10n", uploader_l10n)
    scripts.add("wp-plupload", str("/wp-includes/js/plupload/wp-plupload") + str(suffix) + str(".js"), Array("plupload", "jquery", "json2", "media-models"), False, 1)
    did_action("init") and scripts.localize("wp-plupload", "pluploadL10n", uploader_l10n)
    #// Keep 'swfupload' for back-compat.
    scripts.add("swfupload", "/wp-includes/js/swfupload/swfupload.js", Array(), "2201-20110113")
    scripts.add("swfupload-all", False, Array("swfupload"), "2201")
    scripts.add("swfupload-handlers", str("/wp-includes/js/swfupload/handlers") + str(suffix) + str(".js"), Array("swfupload-all", "jquery"), "2201-20110524")
    did_action("init") and scripts.localize("swfupload-handlers", "swfuploadL10n", uploader_l10n)
    scripts.add("comment-reply", str("/wp-includes/js/comment-reply") + str(suffix) + str(".js"), Array(), False, 1)
    scripts.add("json2", str("/wp-includes/js/json2") + str(suffix) + str(".js"), Array(), "2015-05-03")
    did_action("init") and scripts.add_data("json2", "conditional", "lt IE 8")
    scripts.add("underscore", str("/wp-includes/js/underscore") + str(dev_suffix) + str(".js"), Array(), "1.8.3", 1)
    scripts.add("backbone", str("/wp-includes/js/backbone") + str(dev_suffix) + str(".js"), Array("underscore", "jquery"), "1.4.0", 1)
    scripts.add("wp-util", str("/wp-includes/js/wp-util") + str(suffix) + str(".js"), Array("underscore", "jquery"), False, 1)
    did_action("init") and scripts.localize("wp-util", "_wpUtilSettings", Array({"ajax": Array({"url": admin_url("admin-ajax.php", "relative")})}))
    scripts.add("wp-backbone", str("/wp-includes/js/wp-backbone") + str(suffix) + str(".js"), Array("backbone", "wp-util"), False, 1)
    scripts.add("revisions", str("/wp-admin/js/revisions") + str(suffix) + str(".js"), Array("wp-backbone", "jquery-ui-slider", "hoverIntent"), False, 1)
    scripts.add("imgareaselect", str("/wp-includes/js/imgareaselect/jquery.imgareaselect") + str(suffix) + str(".js"), Array("jquery"), False, 1)
    scripts.add("mediaelement", False, Array("jquery", "mediaelement-core", "mediaelement-migrate"), "4.2.13-9993131", 1)
    scripts.add("mediaelement-core", str("/wp-includes/js/mediaelement/mediaelement-and-player") + str(suffix) + str(".js"), Array(), "4.2.13-9993131", 1)
    scripts.add("mediaelement-migrate", str("/wp-includes/js/mediaelement/mediaelement-migrate") + str(suffix) + str(".js"), Array(), False, 1)
    did_action("init") and scripts.add_inline_script("mediaelement-core", php_sprintf("var mejsL10n = %s;", wp_json_encode(Array({"language": php_strtolower(strtok(determine_locale(), "_-")), "strings": Array({"mejs.download-file": __("Download File"), "mejs.install-flash": __("You are using a browser that does not have Flash player enabled or installed. Please turn on your Flash player plugin or download the latest version from https://get.adobe.com/flashplayer/"), "mejs.fullscreen": __("Fullscreen"), "mejs.play": __("Play"), "mejs.pause": __("Pause"), "mejs.time-slider": __("Time Slider"), "mejs.time-help-text": __("Use Left/Right Arrow keys to advance one second, Up/Down arrows to advance ten seconds."), "mejs.live-broadcast": __("Live Broadcast"), "mejs.volume-help-text": __("Use Up/Down Arrow keys to increase or decrease volume."), "mejs.unmute": __("Unmute"), "mejs.mute": __("Mute"), "mejs.volume-slider": __("Volume Slider"), "mejs.video-player": __("Video Player"), "mejs.audio-player": __("Audio Player"), "mejs.captions-subtitles": __("Captions/Subtitles"), "mejs.captions-chapters": __("Chapters"), "mejs.none": __("None"), "mejs.afrikaans": __("Afrikaans"), "mejs.albanian": __("Albanian"), "mejs.arabic": __("Arabic"), "mejs.belarusian": __("Belarusian"), "mejs.bulgarian": __("Bulgarian"), "mejs.catalan": __("Catalan"), "mejs.chinese": __("Chinese"), "mejs.chinese-simplified": __("Chinese (Simplified)"), "mejs.chinese-traditional": __("Chinese (Traditional)"), "mejs.croatian": __("Croatian"), "mejs.czech": __("Czech"), "mejs.danish": __("Danish"), "mejs.dutch": __("Dutch"), "mejs.english": __("English"), "mejs.estonian": __("Estonian"), "mejs.filipino": __("Filipino"), "mejs.finnish": __("Finnish"), "mejs.french": __("French"), "mejs.galician": __("Galician"), "mejs.german": __("German"), "mejs.greek": __("Greek"), "mejs.haitian-creole": __("Haitian Creole"), "mejs.hebrew": __("Hebrew"), "mejs.hindi": __("Hindi"), "mejs.hungarian": __("Hungarian"), "mejs.icelandic": __("Icelandic"), "mejs.indonesian": __("Indonesian"), "mejs.irish": __("Irish"), "mejs.italian": __("Italian"), "mejs.japanese": __("Japanese"), "mejs.korean": __("Korean"), "mejs.latvian": __("Latvian"), "mejs.lithuanian": __("Lithuanian"), "mejs.macedonian": __("Macedonian"), "mejs.malay": __("Malay"), "mejs.maltese": __("Maltese"), "mejs.norwegian": __("Norwegian"), "mejs.persian": __("Persian"), "mejs.polish": __("Polish"), "mejs.portuguese": __("Portuguese"), "mejs.romanian": __("Romanian"), "mejs.russian": __("Russian"), "mejs.serbian": __("Serbian"), "mejs.slovak": __("Slovak"), "mejs.slovenian": __("Slovenian"), "mejs.spanish": __("Spanish"), "mejs.swahili": __("Swahili"), "mejs.swedish": __("Swedish"), "mejs.tagalog": __("Tagalog"), "mejs.thai": __("Thai"), "mejs.turkish": __("Turkish"), "mejs.ukrainian": __("Ukrainian"), "mejs.vietnamese": __("Vietnamese"), "mejs.welsh": __("Welsh"), "mejs.yiddish": __("Yiddish")})}))), "before")
    scripts.add("mediaelement-vimeo", "/wp-includes/js/mediaelement/renderers/vimeo.min.js", Array("mediaelement"), "4.2.13-9993131", 1)
    scripts.add("wp-mediaelement", str("/wp-includes/js/mediaelement/wp-mediaelement") + str(suffix) + str(".js"), Array("mediaelement"), False, 1)
    mejs_settings = Array({"pluginPath": includes_url("js/mediaelement/", "relative"), "classPrefix": "mejs-", "stretching": "responsive"})
    did_action("init") and scripts.localize("mediaelement", "_wpmejsSettings", apply_filters("mejs_settings", mejs_settings))
    scripts.add("wp-codemirror", "/wp-includes/js/codemirror/codemirror.min.js", Array(), "5.29.1-alpha-ee20357")
    scripts.add("csslint", "/wp-includes/js/codemirror/csslint.js", Array(), "1.0.5")
    scripts.add("esprima", "/wp-includes/js/codemirror/esprima.js", Array(), "4.0.0")
    scripts.add("jshint", "/wp-includes/js/codemirror/fakejshint.js", Array("esprima"), "2.9.5")
    scripts.add("jsonlint", "/wp-includes/js/codemirror/jsonlint.js", Array(), "1.6.2")
    scripts.add("htmlhint", "/wp-includes/js/codemirror/htmlhint.js", Array(), "0.9.14-xwp")
    scripts.add("htmlhint-kses", "/wp-includes/js/codemirror/htmlhint-kses.js", Array("htmlhint"))
    scripts.add("code-editor", str("/wp-admin/js/code-editor") + str(suffix) + str(".js"), Array("jquery", "wp-codemirror", "underscore"))
    scripts.add("wp-theme-plugin-editor", str("/wp-admin/js/theme-plugin-editor") + str(suffix) + str(".js"), Array("wp-util", "wp-sanitize", "jquery", "jquery-ui-core", "wp-a11y", "underscore"))
    did_action("init") and scripts.add_inline_script("wp-theme-plugin-editor", php_sprintf("wp.themePluginEditor.l10n = %s;", wp_json_encode(Array({"saveAlert": __("The changes you made will be lost if you navigate away from this page."), "saveError": __("Something went wrong. Your change may not have been saved. Please try again. There is also a chance that you may need to manually fix and upload the file over FTP."), "lintError": Array({"singular": _n("There is %d error which must be fixed before you can update this file.", "There are %d errors which must be fixed before you can update this file.", 1), "plural": _n("There is %d error which must be fixed before you can update this file.", "There are %d errors which must be fixed before you can update this file.", 2)})}))))
    scripts.add("wp-playlist", str("/wp-includes/js/mediaelement/wp-playlist") + str(suffix) + str(".js"), Array("wp-util", "backbone", "mediaelement"), False, 1)
    scripts.add("zxcvbn-async", str("/wp-includes/js/zxcvbn-async") + str(suffix) + str(".js"), Array(), "1.0")
    did_action("init") and scripts.localize("zxcvbn-async", "_zxcvbnSettings", Array({"src": includes_url("/js/zxcvbn.min.js") if php_empty(lambda : guessed_url) else scripts.base_url + "/wp-includes/js/zxcvbn.min.js"}))
    scripts.add("password-strength-meter", str("/wp-admin/js/password-strength-meter") + str(suffix) + str(".js"), Array("jquery", "zxcvbn-async"), False, 1)
    did_action("init") and scripts.localize("password-strength-meter", "pwsL10n", Array({"unknown": _x("Password strength unknown", "password strength"), "short": _x("Very weak", "password strength"), "bad": _x("Weak", "password strength"), "good": _x("Medium", "password strength"), "strong": _x("Strong", "password strength"), "mismatch": _x("Mismatch", "password mismatch")}))
    scripts.add("user-profile", str("/wp-admin/js/user-profile") + str(suffix) + str(".js"), Array("jquery", "password-strength-meter", "wp-util"), False, 1)
    did_action("init") and scripts.localize("user-profile", "userProfileL10n", Array({"warn": __("Your new password has not been saved."), "warnWeak": __("Confirm use of weak password"), "show": __("Show"), "hide": __("Hide"), "cancel": __("Cancel"), "ariaShow": esc_attr__("Show password"), "ariaHide": esc_attr__("Hide password")}))
    scripts.add("language-chooser", str("/wp-admin/js/language-chooser") + str(suffix) + str(".js"), Array("jquery"), False, 1)
    scripts.add("user-suggest", str("/wp-admin/js/user-suggest") + str(suffix) + str(".js"), Array("jquery-ui-autocomplete"), False, 1)
    scripts.add("admin-bar", str("/wp-includes/js/admin-bar") + str(suffix) + str(".js"), Array("hoverintent-js"), False, 1)
    scripts.add("wplink", str("/wp-includes/js/wplink") + str(suffix) + str(".js"), Array("jquery", "wp-a11y"), False, 1)
    did_action("init") and scripts.localize("wplink", "wpLinkL10n", Array({"title": __("Insert/edit link"), "update": __("Update"), "save": __("Add Link"), "noTitle": __("(no title)"), "noMatchesFound": __("No results found."), "linkSelected": __("Link selected."), "linkInserted": __("Link inserted."), "minInputLength": php_int(_x("3", "minimum input length for searching post links"))}))
    scripts.add("wpdialogs", str("/wp-includes/js/wpdialog") + str(suffix) + str(".js"), Array("jquery-ui-dialog"), False, 1)
    scripts.add("word-count", str("/wp-admin/js/word-count") + str(suffix) + str(".js"), Array(), False, 1)
    scripts.add("media-upload", str("/wp-admin/js/media-upload") + str(suffix) + str(".js"), Array("thickbox", "shortcode"), False, 1)
    scripts.add("hoverIntent", str("/wp-includes/js/hoverIntent") + str(suffix) + str(".js"), Array("jquery"), "1.8.1", 1)
    #// JS-only version of hoverintent (no dependencies).
    scripts.add("hoverintent-js", "/wp-includes/js/hoverintent-js.min.js", Array(), "2.2.1", 1)
    scripts.add("customize-base", str("/wp-includes/js/customize-base") + str(suffix) + str(".js"), Array("jquery", "json2", "underscore"), False, 1)
    scripts.add("customize-loader", str("/wp-includes/js/customize-loader") + str(suffix) + str(".js"), Array("customize-base"), False, 1)
    scripts.add("customize-preview", str("/wp-includes/js/customize-preview") + str(suffix) + str(".js"), Array("wp-a11y", "customize-base"), False, 1)
    scripts.add("customize-models", "/wp-includes/js/customize-models.js", Array("underscore", "backbone"), False, 1)
    scripts.add("customize-views", "/wp-includes/js/customize-views.js", Array("jquery", "underscore", "imgareaselect", "customize-models", "media-editor", "media-views"), False, 1)
    scripts.add("customize-controls", str("/wp-admin/js/customize-controls") + str(suffix) + str(".js"), Array("customize-base", "wp-a11y", "wp-util", "jquery-ui-core"), False, 1)
    did_action("init") and scripts.localize("customize-controls", "_wpCustomizeControlsL10n", Array({"activate": __("Activate &amp; Publish"), "save": __("Save &amp; Publish"), "publish": __("Publish"), "published": __("Published"), "saveDraft": __("Save Draft"), "draftSaved": __("Draft Saved"), "updating": __("Updating"), "schedule": _x("Schedule", "customizer changeset action/button label"), "scheduled": _x("Scheduled", "customizer changeset status"), "invalid": __("Invalid"), "saveBeforeShare": __("Please save your changes in order to share the preview."), "futureDateError": __("You must supply a future date to schedule."), "saveAlert": __("The changes you made will be lost if you navigate away from this page."), "saved": __("Saved"), "cancel": __("Cancel"), "close": __("Close"), "action": __("Action"), "discardChanges": __("Discard changes"), "cheatin": __("Something went wrong."), "notAllowedHeading": __("You need a higher level of permission."), "notAllowed": __("Sorry, you are not allowed to customize this site."), "previewIframeTitle": __("Site Preview"), "loginIframeTitle": __("Session expired"), "collapseSidebar": _x("Hide Controls", "label for hide controls button without length constraints"), "expandSidebar": _x("Show Controls", "label for hide controls button without length constraints"), "untitledBlogName": __("(Untitled)"), "unknownRequestFail": __("Looks like something&#8217;s gone wrong. Wait a couple seconds, and then try again."), "themeDownloading": __("Downloading your new theme&hellip;"), "themePreviewWait": __("Setting up your live preview. This may take a bit."), "revertingChanges": __("Reverting unpublished changes&hellip;"), "trashConfirm": __("Are you sure you want to discard your unpublished changes?"), "takenOverMessage": __("%s has taken over and is currently customizing."), "autosaveNotice": __("There is a more recent autosave of your changes than the one you are previewing. <a href=\"%s\">Restore the autosave</a>"), "videoHeaderNotice": __("This theme doesn&#8217;t support video headers on this page. Navigate to the front page or another page that supports video headers."), "allowedFiles": __("Allowed Files"), "customCssError": Array({"singular": _n("There is %d error which must be fixed before you can save.", "There are %d errors which must be fixed before you can save.", 1), "plural": _n("There is %d error which must be fixed before you can save.", "There are %d errors which must be fixed before you can save.", 2)})}, {"pageOnFrontError": __("Homepage and posts page must be different."), "saveBlockedError": Array({"singular": _n("Unable to save due to %s invalid setting.", "Unable to save due to %s invalid settings.", 1), "plural": _n("Unable to save due to %s invalid setting.", "Unable to save due to %s invalid settings.", 2)})}, {"scheduleDescription": __("Schedule your customization changes to publish (\"go live\") at a future date."), "themePreviewUnavailable": __("Sorry, you can&#8217;t preview new themes when you have changes scheduled or saved as a draft. Please publish your changes, or wait until they publish to preview new themes."), "themeInstallUnavailable": php_sprintf(__("You won&#8217;t be able to install new themes from here yet since your install requires SFTP credentials. For now, please <a href=\"%s\">add themes in the admin</a>."), esc_url(admin_url("theme-install.php"))), "publishSettings": __("Publish Settings"), "invalidDate": __("Invalid date."), "invalidValue": __("Invalid value.")}))
    scripts.add("customize-selective-refresh", str("/wp-includes/js/customize-selective-refresh") + str(suffix) + str(".js"), Array("jquery", "wp-util", "customize-preview"), False, 1)
    scripts.add("customize-widgets", str("/wp-admin/js/customize-widgets") + str(suffix) + str(".js"), Array("jquery", "jquery-ui-sortable", "jquery-ui-droppable", "wp-backbone", "customize-controls"), False, 1)
    scripts.add("customize-preview-widgets", str("/wp-includes/js/customize-preview-widgets") + str(suffix) + str(".js"), Array("jquery", "wp-util", "customize-preview", "customize-selective-refresh"), False, 1)
    scripts.add("customize-nav-menus", str("/wp-admin/js/customize-nav-menus") + str(suffix) + str(".js"), Array("jquery", "wp-backbone", "customize-controls", "accordion", "nav-menu", "wp-sanitize"), False, 1)
    scripts.add("customize-preview-nav-menus", str("/wp-includes/js/customize-preview-nav-menus") + str(suffix) + str(".js"), Array("jquery", "wp-util", "customize-preview", "customize-selective-refresh"), False, 1)
    scripts.add("wp-custom-header", str("/wp-includes/js/wp-custom-header") + str(suffix) + str(".js"), Array("wp-a11y"), False, 1)
    scripts.add("accordion", str("/wp-admin/js/accordion") + str(suffix) + str(".js"), Array("jquery"), False, 1)
    scripts.add("shortcode", str("/wp-includes/js/shortcode") + str(suffix) + str(".js"), Array("underscore"), False, 1)
    scripts.add("media-models", str("/wp-includes/js/media-models") + str(suffix) + str(".js"), Array("wp-backbone"), False, 1)
    did_action("init") and scripts.localize("media-models", "_wpMediaModelsL10n", Array({"settings": Array({"ajaxurl": admin_url("admin-ajax.php", "relative"), "post": Array({"id": 0})})}))
    scripts.add("wp-embed", str("/wp-includes/js/wp-embed") + str(suffix) + str(".js"))
    #// To enqueue media-views or media-editor, call wp_enqueue_media().
    #// Both rely on numerous settings, styles, and templates to operate correctly.
    scripts.add("media-views", str("/wp-includes/js/media-views") + str(suffix) + str(".js"), Array("utils", "media-models", "wp-plupload", "jquery-ui-sortable", "wp-mediaelement", "wp-api-request", "wp-a11y", "wp-i18n"), False, 1)
    scripts.set_translations("media-views")
    scripts.add("media-editor", str("/wp-includes/js/media-editor") + str(suffix) + str(".js"), Array("shortcode", "media-views"), False, 1)
    scripts.add("media-audiovideo", str("/wp-includes/js/media-audiovideo") + str(suffix) + str(".js"), Array("media-editor"), False, 1)
    scripts.add("mce-view", str("/wp-includes/js/mce-view") + str(suffix) + str(".js"), Array("shortcode", "jquery", "media-views", "media-audiovideo"), False, 1)
    scripts.add("wp-api", str("/wp-includes/js/wp-api") + str(suffix) + str(".js"), Array("jquery", "backbone", "underscore", "wp-api-request"), False, 1)
    if is_admin():
        scripts.add("admin-tags", str("/wp-admin/js/tags") + str(suffix) + str(".js"), Array("jquery", "wp-ajax-response"), False, 1)
        did_action("init") and scripts.localize("admin-tags", "tagsl10n", Array({"noPerm": __("Sorry, you are not allowed to do that."), "broken": __("Something went wrong.")}))
        scripts.add("admin-comments", str("/wp-admin/js/edit-comments") + str(suffix) + str(".js"), Array("wp-lists", "quicktags", "jquery-query"), False, 1)
        did_action("init") and scripts.localize("admin-comments", "adminCommentsL10n", Array({"hotkeys_highlight_first": (php_isset(lambda : PHP_REQUEST["hotkeys_highlight_first"])), "hotkeys_highlight_last": (php_isset(lambda : PHP_REQUEST["hotkeys_highlight_last"])), "replyApprove": __("Approve and Reply"), "reply": __("Reply"), "warnQuickEdit": __("Are you sure you want to edit this comment?\nThe changes you made will be lost."), "warnCommentChanges": __("Are you sure you want to do this?\nThe comment changes you made will be lost."), "docTitleComments": __("Comments"), "docTitleCommentsCount": __("Comments (%s)")}))
        scripts.add("xfn", str("/wp-admin/js/xfn") + str(suffix) + str(".js"), Array("jquery"), False, 1)
        scripts.add("postbox", str("/wp-admin/js/postbox") + str(suffix) + str(".js"), Array("jquery-ui-sortable"), False, 1)
        did_action("init") and scripts.localize("postbox", "postBoxL10n", Array({"postBoxEmptyString": __("Drag boxes here")}))
        scripts.add("tags-box", str("/wp-admin/js/tags-box") + str(suffix) + str(".js"), Array("jquery", "tags-suggest"), False, 1)
        scripts.add("tags-suggest", str("/wp-admin/js/tags-suggest") + str(suffix) + str(".js"), Array("jquery-ui-autocomplete", "wp-a11y"), False, 1)
        did_action("init") and scripts.localize("tags-suggest", "tagsSuggestL10n", Array({"tagDelimiter": _x(",", "tag delimiter"), "removeTerm": __("Remove term:"), "termSelected": __("Term selected."), "termAdded": __("Term added."), "termRemoved": __("Term removed.")}))
        scripts.add("post", str("/wp-admin/js/post") + str(suffix) + str(".js"), Array("suggest", "wp-lists", "postbox", "tags-box", "underscore", "word-count", "wp-a11y", "wp-sanitize"), False, 1)
        did_action("init") and scripts.localize("post", "postL10n", Array({"ok": __("OK"), "cancel": __("Cancel"), "publishOn": __("Publish on:"), "publishOnFuture": __("Schedule for:"), "publishOnPast": __("Published on:"), "dateFormat": __("%1$s %2$s, %3$s at %4$s:%5$s"), "showcomm": __("Show more comments"), "endcomm": __("No more comments found."), "publish": __("Publish"), "schedule": _x("Schedule", "post action/button label"), "update": __("Update"), "savePending": __("Save as Pending"), "saveDraft": __("Save Draft"), "private": __("Private"), "public": __("Public"), "publicSticky": __("Public, Sticky"), "password": __("Password Protected"), "privatelyPublished": __("Privately Published"), "published": __("Published"), "saveAlert": __("The changes you made will be lost if you navigate away from this page."), "savingText": __("Saving Draft&#8230;"), "permalinkSaved": __("Permalink saved")}))
        scripts.add("editor-expand", str("/wp-admin/js/editor-expand") + str(suffix) + str(".js"), Array("jquery", "underscore"), False, 1)
        scripts.add("link", str("/wp-admin/js/link") + str(suffix) + str(".js"), Array("wp-lists", "postbox"), False, 1)
        scripts.add("comment", str("/wp-admin/js/comment") + str(suffix) + str(".js"), Array("jquery", "postbox"))
        scripts.add_data("comment", "group", 1)
        did_action("init") and scripts.localize("comment", "commentL10n", Array({"submittedOn": __("Submitted on:"), "dateFormat": __("%1$s %2$s, %3$s at %4$s:%5$s")}))
        scripts.add("admin-gallery", str("/wp-admin/js/gallery") + str(suffix) + str(".js"), Array("jquery-ui-sortable"))
        scripts.add("admin-widgets", str("/wp-admin/js/widgets") + str(suffix) + str(".js"), Array("jquery-ui-sortable", "jquery-ui-draggable", "jquery-ui-droppable", "wp-a11y"), False, 1)
        did_action("init") and scripts.add_inline_script("admin-widgets", php_sprintf("wpWidgets.l10n = %s;", wp_json_encode(Array({"save": __("Save"), "saved": __("Saved"), "saveAlert": __("The changes you made will be lost if you navigate away from this page."), "widgetAdded": __("Widget has been added to the selected sidebar")}))))
        scripts.add("media-widgets", str("/wp-admin/js/widgets/media-widgets") + str(suffix) + str(".js"), Array("jquery", "media-models", "media-views", "wp-api-request"))
        scripts.add_inline_script("media-widgets", "wp.mediaWidgets.init();", "after")
        scripts.add("media-audio-widget", str("/wp-admin/js/widgets/media-audio-widget") + str(suffix) + str(".js"), Array("media-widgets", "media-audiovideo"))
        scripts.add("media-image-widget", str("/wp-admin/js/widgets/media-image-widget") + str(suffix) + str(".js"), Array("media-widgets"))
        scripts.add("media-gallery-widget", str("/wp-admin/js/widgets/media-gallery-widget") + str(suffix) + str(".js"), Array("media-widgets"))
        scripts.add("media-video-widget", str("/wp-admin/js/widgets/media-video-widget") + str(suffix) + str(".js"), Array("media-widgets", "media-audiovideo", "wp-api-request"))
        scripts.add("text-widgets", str("/wp-admin/js/widgets/text-widgets") + str(suffix) + str(".js"), Array("jquery", "backbone", "editor", "wp-util", "wp-a11y"))
        scripts.add("custom-html-widgets", str("/wp-admin/js/widgets/custom-html-widgets") + str(suffix) + str(".js"), Array("jquery", "backbone", "wp-util", "jquery-ui-core", "wp-a11y"))
        scripts.add("theme", str("/wp-admin/js/theme") + str(suffix) + str(".js"), Array("wp-backbone", "wp-a11y", "customize-base"), False, 1)
        scripts.add("inline-edit-post", str("/wp-admin/js/inline-edit-post") + str(suffix) + str(".js"), Array("jquery", "tags-suggest", "wp-a11y"), False, 1)
        did_action("init") and scripts.localize("inline-edit-post", "inlineEditL10n", Array({"error": __("Error while saving the changes."), "ntdeltitle": __("Remove From Bulk Edit"), "notitle": __("(no title)"), "comma": php_trim(_x(",", "tag delimiter")), "saved": __("Changes saved.")}))
        scripts.add("inline-edit-tax", str("/wp-admin/js/inline-edit-tax") + str(suffix) + str(".js"), Array("jquery", "wp-a11y"), False, 1)
        did_action("init") and scripts.localize("inline-edit-tax", "inlineEditL10n", Array({"error": __("Error while saving the changes."), "saved": __("Changes saved.")}))
        scripts.add("plugin-install", str("/wp-admin/js/plugin-install") + str(suffix) + str(".js"), Array("jquery", "jquery-ui-core", "thickbox"), False, 1)
        did_action("init") and scripts.localize("plugin-install", "plugininstallL10n", Array({"plugin_information": __("Plugin:"), "plugin_modal_label": __("Plugin details"), "ays": __("Are you sure you want to install this plugin?")}))
        scripts.add("site-health", str("/wp-admin/js/site-health") + str(suffix) + str(".js"), Array("clipboard", "jquery", "wp-util", "wp-a11y", "wp-i18n"), False, 1)
        scripts.set_translations("site-health")
        scripts.add("privacy-tools", str("/wp-admin/js/privacy-tools") + str(suffix) + str(".js"), Array("jquery"), False, 1)
        did_action("init") and scripts.localize("privacy-tools", "privacyToolsL10n", Array({"noDataFound": __("No personal data was found for this user."), "foundAndRemoved": __("All of the personal data found for this user was erased."), "noneRemoved": __("Personal data was found for this user but was not erased."), "someNotRemoved": __("Personal data was found for this user but some of the personal data found was not erased."), "removalError": __("An error occurred while attempting to find and erase personal data."), "emailSent": __("The personal data export link for this user was sent."), "noExportFile": __("No personal data export file was generated."), "exportError": __("An error occurred while attempting to export personal data.")}))
        scripts.add("updates", str("/wp-admin/js/updates") + str(suffix) + str(".js"), Array("jquery", "wp-util", "wp-a11y", "wp-sanitize"), False, 1)
        did_action("init") and scripts.localize("updates", "_wpUpdatesSettings", Array({"ajax_nonce": wp_create_nonce("updates"), "l10n": Array({"searchResults": __("Search results for &#8220;%s&#8221;"), "searchResultsLabel": __("Search Results"), "noPlugins": __("You do not appear to have any plugins available at this time."), "noItemsSelected": __("Please select at least one item to perform this action on."), "updating": __("Updating..."), "pluginUpdated": _x("Updated!", "plugin"), "themeUpdated": _x("Updated!", "theme"), "update": __("Update"), "updateNow": __("Update Now"), "pluginUpdateNowLabel": _x("Update %s now", "plugin"), "updateFailedShort": __("Update Failed!"), "updateFailed": __("Update Failed: %s"), "pluginUpdatingLabel": _x("Updating %s...", "plugin"), "pluginUpdatedLabel": _x("%s updated!", "plugin"), "pluginUpdateFailedLabel": _x("%s update failed", "plugin"), "updatingMsg": __("Updating... please wait."), "updatedMsg": __("Update completed successfully."), "updateCancel": __("Update canceled."), "beforeunload": __("Updates may not complete if you navigate away from this page."), "installNow": __("Install Now"), "pluginInstallNowLabel": _x("Install %s now", "plugin"), "installing": __("Installing..."), "pluginInstalled": _x("Installed!", "plugin"), "themeInstalled": _x("Installed!", "theme"), "installFailedShort": __("Installation Failed!"), "installFailed": __("Installation failed: %s"), "pluginInstallingLabel": _x("Installing %s...", "plugin"), "themeInstallingLabel": _x("Installing %s...", "theme"), "pluginInstalledLabel": _x("%s installed!", "plugin"), "themeInstalledLabel": _x("%s installed!", "theme"), "pluginInstallFailedLabel": _x("%s installation failed", "plugin"), "themeInstallFailedLabel": _x("%s installation failed", "theme"), "installingMsg": __("Installing... please wait."), "installedMsg": __("Installation completed successfully."), "importerInstalledMsg": __("Importer installed successfully. <a href=\"%s\">Run importer</a>"), "aysDelete": __("Are you sure you want to delete %s?"), "aysDeleteUninstall": __("Are you sure you want to delete %s and its data?"), "aysBulkDelete": __("Are you sure you want to delete the selected plugins and their data?"), "aysBulkDeleteThemes": __("Caution: These themes may be active on other sites in the network. Are you sure you want to proceed?"), "deleting": __("Deleting..."), "deleteFailed": __("Deletion failed: %s"), "pluginDeleted": _x("Deleted!", "plugin"), "themeDeleted": _x("Deleted!", "theme"), "livePreview": __("Live Preview"), "activatePlugin": __("Network Activate") if is_network_admin() else __("Activate"), "activateTheme": __("Network Enable") if is_network_admin() else __("Activate"), "activatePluginLabel": _x("Network Activate %s", "plugin") if is_network_admin() else _x("Activate %s", "plugin"), "activateThemeLabel": _x("Network Activate %s", "theme") if is_network_admin() else _x("Activate %s", "theme"), "activateImporter": __("Run Importer"), "activateImporterLabel": __("Run %s"), "unknownError": __("Something went wrong."), "connectionError": __("Connection lost or the server is busy. Please try again later."), "nonceError": __("An error has occurred. Please reload the page and try again."), "pluginsFound": __("Number of plugins found: %d"), "noPluginsFound": __("No plugins found. Try a different search.")})}))
        scripts.add("farbtastic", "/wp-admin/js/farbtastic.js", Array("jquery"), "1.2")
        scripts.add("iris", "/wp-admin/js/iris.min.js", Array("jquery-ui-draggable", "jquery-ui-slider", "jquery-touch-punch"), "1.0.7", 1)
        scripts.add("wp-color-picker", str("/wp-admin/js/color-picker") + str(suffix) + str(".js"), Array("iris"), False, 1)
        did_action("init") and scripts.localize("wp-color-picker", "wpColorPickerL10n", Array({"clear": __("Clear"), "clearAriaLabel": __("Clear color"), "defaultString": __("Default"), "defaultAriaLabel": __("Select default color"), "pick": __("Select Color"), "defaultLabel": __("Color value")}))
        scripts.add("dashboard", str("/wp-admin/js/dashboard") + str(suffix) + str(".js"), Array("jquery", "admin-comments", "postbox", "wp-util", "wp-a11y"), False, 1)
        scripts.add("list-revisions", str("/wp-includes/js/wp-list-revisions") + str(suffix) + str(".js"))
        scripts.add("media-grid", str("/wp-includes/js/media-grid") + str(suffix) + str(".js"), Array("media-editor"), False, 1)
        scripts.add("media", str("/wp-admin/js/media") + str(suffix) + str(".js"), Array("jquery"), False, 1)
        did_action("init") and scripts.localize("media", "attachMediaBoxL10n", Array({"error": __("An error has occurred. Please reload the page and try again.")}))
        scripts.add("image-edit", str("/wp-admin/js/image-edit") + str(suffix) + str(".js"), Array("jquery", "json2", "imgareaselect"), False, 1)
        did_action("init") and scripts.localize("image-edit", "imageEditL10n", Array({"error": __("Could not load the preview image. Please reload the page and try again.")}))
        scripts.add("set-post-thumbnail", str("/wp-admin/js/set-post-thumbnail") + str(suffix) + str(".js"), Array("jquery"), False, 1)
        did_action("init") and scripts.localize("set-post-thumbnail", "setPostThumbnailL10n", Array({"setThumbnail": __("Use as featured image"), "saving": __("Saving..."), "error": __("Could not set that as the thumbnail image. Try a different attachment."), "done": __("Done")}))
        #// 
        #// Navigation Menus: Adding underscore as a dependency to utilize _.debounce
        #// see https://core.trac.wordpress.org/ticket/42321
        #//
        scripts.add("nav-menu", str("/wp-admin/js/nav-menu") + str(suffix) + str(".js"), Array("jquery-ui-sortable", "jquery-ui-draggable", "jquery-ui-droppable", "wp-lists", "postbox", "json2", "underscore"))
        did_action("init") and scripts.localize("nav-menu", "navMenuL10n", Array({"noResultsFound": __("No results found."), "warnDeleteMenu": __("You are about to permanently delete this menu. \n 'Cancel' to stop, 'OK' to delete."), "saveAlert": __("The changes you made will be lost if you navigate away from this page."), "untitled": _x("(no label)", "missing menu item navigation label")}))
        scripts.add("custom-header", "/wp-admin/js/custom-header.js", Array("jquery-masonry"), False, 1)
        scripts.add("custom-background", str("/wp-admin/js/custom-background") + str(suffix) + str(".js"), Array("wp-color-picker", "media-views"), False, 1)
        scripts.add("media-gallery", str("/wp-admin/js/media-gallery") + str(suffix) + str(".js"), Array("jquery"), False, 1)
        scripts.add("svg-painter", "/wp-admin/js/svg-painter.js", Array("jquery"), False, 1)
    # end if
# end def wp_default_scripts
#// 
#// Assign default styles to $styles object.
#// 
#// Nothing is returned, because the $styles parameter is passed by reference.
#// Meaning that whatever object is passed will be updated without having to
#// reassign the variable that was passed back to the same value. This saves
#// memory.
#// 
#// Adding default styles is not the only task, it also assigns the base_url
#// property, the default version, and text direction for the object.
#// 
#// @since 2.6.0
#// 
#// @param WP_Styles $styles
#//
def wp_default_styles(styles=None, *args_):
    
    #// Include an unmodified $wp_version.
    php_include_file(ABSPATH + WPINC + "/version.php", once=False)
    if (not php_defined("SCRIPT_DEBUG")):
        php_define("SCRIPT_DEBUG", False != php_strpos(wp_version, "-src"))
    # end if
    guessurl = site_url()
    if (not guessurl):
        guessurl = wp_guess_url()
    # end if
    styles.base_url = guessurl
    styles.content_url = WP_CONTENT_URL if php_defined("WP_CONTENT_URL") else ""
    styles.default_version = get_bloginfo("version")
    styles.text_direction = "rtl" if php_function_exists("is_rtl") and is_rtl() else "ltr"
    styles.default_dirs = Array("/wp-admin/", "/wp-includes/css/")
    #// Open Sans is no longer used by core, but may be relied upon by themes and plugins.
    open_sans_font_url = ""
    #// 
    #// translators: If there are characters in your language that are not supported
    #// by Open Sans, translate this to 'off'. Do not translate into your own language.
    #//
    if "off" != _x("on", "Open Sans font: on or off"):
        subsets = "latin,latin-ext"
        #// 
        #// translators: To add an additional Open Sans character subset specific to your language,
        #// translate this to 'greek', 'cyrillic' or 'vietnamese'. Do not translate into your own language.
        #//
        subset = _x("no-subset", "Open Sans font: add new subset (greek, cyrillic, vietnamese)")
        if "cyrillic" == subset:
            subsets += ",cyrillic,cyrillic-ext"
        elif "greek" == subset:
            subsets += ",greek,greek-ext"
        elif "vietnamese" == subset:
            subsets += ",vietnamese"
        # end if
        #// Hotlink Open Sans, for now.
        open_sans_font_url = str("https://fonts.googleapis.com/css?family=Open+Sans:300italic,400italic,600italic,300,400,600&subset=") + str(subsets) + str("&display=fallback")
    # end if
    #// Register a stylesheet for the selected admin color scheme.
    styles.add("colors", True, Array("wp-admin", "buttons"))
    suffix = "" if SCRIPT_DEBUG else ".min"
    #// Admin CSS.
    styles.add("common", str("/wp-admin/css/common") + str(suffix) + str(".css"))
    styles.add("forms", str("/wp-admin/css/forms") + str(suffix) + str(".css"))
    styles.add("admin-menu", str("/wp-admin/css/admin-menu") + str(suffix) + str(".css"))
    styles.add("dashboard", str("/wp-admin/css/dashboard") + str(suffix) + str(".css"))
    styles.add("list-tables", str("/wp-admin/css/list-tables") + str(suffix) + str(".css"))
    styles.add("edit", str("/wp-admin/css/edit") + str(suffix) + str(".css"))
    styles.add("revisions", str("/wp-admin/css/revisions") + str(suffix) + str(".css"))
    styles.add("media", str("/wp-admin/css/media") + str(suffix) + str(".css"))
    styles.add("themes", str("/wp-admin/css/themes") + str(suffix) + str(".css"))
    styles.add("about", str("/wp-admin/css/about") + str(suffix) + str(".css"))
    styles.add("nav-menus", str("/wp-admin/css/nav-menus") + str(suffix) + str(".css"))
    styles.add("widgets", str("/wp-admin/css/widgets") + str(suffix) + str(".css"), Array("wp-pointer"))
    styles.add("site-icon", str("/wp-admin/css/site-icon") + str(suffix) + str(".css"))
    styles.add("l10n", str("/wp-admin/css/l10n") + str(suffix) + str(".css"))
    styles.add("code-editor", str("/wp-admin/css/code-editor") + str(suffix) + str(".css"), Array("wp-codemirror"))
    styles.add("site-health", str("/wp-admin/css/site-health") + str(suffix) + str(".css"))
    styles.add("wp-admin", False, Array("dashicons", "common", "forms", "admin-menu", "dashboard", "list-tables", "edit", "revisions", "media", "themes", "about", "nav-menus", "widgets", "site-icon", "l10n"))
    styles.add("login", str("/wp-admin/css/login") + str(suffix) + str(".css"), Array("dashicons", "buttons", "forms", "l10n"))
    styles.add("install", str("/wp-admin/css/install") + str(suffix) + str(".css"), Array("dashicons", "buttons", "forms", "l10n"))
    styles.add("wp-color-picker", str("/wp-admin/css/color-picker") + str(suffix) + str(".css"))
    styles.add("customize-controls", str("/wp-admin/css/customize-controls") + str(suffix) + str(".css"), Array("wp-admin", "colors", "ie", "imgareaselect"))
    styles.add("customize-widgets", str("/wp-admin/css/customize-widgets") + str(suffix) + str(".css"), Array("wp-admin", "colors"))
    styles.add("customize-nav-menus", str("/wp-admin/css/customize-nav-menus") + str(suffix) + str(".css"), Array("wp-admin", "colors"))
    styles.add("ie", str("/wp-admin/css/ie") + str(suffix) + str(".css"))
    styles.add_data("ie", "conditional", "lte IE 7")
    #// Common dependencies.
    styles.add("buttons", str("/wp-includes/css/buttons") + str(suffix) + str(".css"))
    styles.add("dashicons", str("/wp-includes/css/dashicons") + str(suffix) + str(".css"))
    #// Includes CSS.
    styles.add("admin-bar", str("/wp-includes/css/admin-bar") + str(suffix) + str(".css"), Array("dashicons"))
    styles.add("wp-auth-check", str("/wp-includes/css/wp-auth-check") + str(suffix) + str(".css"), Array("dashicons"))
    styles.add("editor-buttons", str("/wp-includes/css/editor") + str(suffix) + str(".css"), Array("dashicons"))
    styles.add("media-views", str("/wp-includes/css/media-views") + str(suffix) + str(".css"), Array("buttons", "dashicons", "wp-mediaelement"))
    styles.add("wp-pointer", str("/wp-includes/css/wp-pointer") + str(suffix) + str(".css"), Array("dashicons"))
    styles.add("customize-preview", str("/wp-includes/css/customize-preview") + str(suffix) + str(".css"), Array("dashicons"))
    styles.add("wp-embed-template-ie", str("/wp-includes/css/wp-embed-template-ie") + str(suffix) + str(".css"))
    styles.add_data("wp-embed-template-ie", "conditional", "lte IE 8")
    #// External libraries and friends.
    styles.add("imgareaselect", "/wp-includes/js/imgareaselect/imgareaselect.css", Array(), "0.9.8")
    styles.add("wp-jquery-ui-dialog", str("/wp-includes/css/jquery-ui-dialog") + str(suffix) + str(".css"), Array("dashicons"))
    styles.add("mediaelement", "/wp-includes/js/mediaelement/mediaelementplayer-legacy.min.css", Array(), "4.2.13-9993131")
    styles.add("wp-mediaelement", str("/wp-includes/js/mediaelement/wp-mediaelement") + str(suffix) + str(".css"), Array("mediaelement"))
    styles.add("thickbox", "/wp-includes/js/thickbox/thickbox.css", Array("dashicons"))
    styles.add("wp-codemirror", "/wp-includes/js/codemirror/codemirror.min.css", Array(), "5.29.1-alpha-ee20357")
    #// Deprecated CSS.
    styles.add("deprecated-media", str("/wp-admin/css/deprecated-media") + str(suffix) + str(".css"))
    styles.add("farbtastic", str("/wp-admin/css/farbtastic") + str(suffix) + str(".css"), Array(), "1.3u1")
    styles.add("jcrop", "/wp-includes/js/jcrop/jquery.Jcrop.min.css", Array(), "0.9.12")
    styles.add("colors-fresh", False, Array("wp-admin", "buttons"))
    #// Old handle.
    styles.add("open-sans", open_sans_font_url)
    #// No longer used in core as of 4.6.
    #// Packages styles.
    fonts_url = ""
    #// 
    #// translators: Use this to specify the proper Google Font name and variants
    #// to load that is supported by your language. Do not translate.
    #// Set to 'off' to disable loading.
    #//
    font_family = _x("Noto Serif:400,400i,700,700i", "Google Font Name and Variants")
    if "off" != font_family:
        fonts_url = "https://fonts.googleapis.com/css?family=" + urlencode(font_family)
    # end if
    styles.add("wp-editor-font", fonts_url)
    styles.add("wp-block-library-theme", str("/wp-includes/css/dist/block-library/theme") + str(suffix) + str(".css"))
    styles.add("wp-edit-blocks", str("/wp-includes/css/dist/block-library/editor") + str(suffix) + str(".css"), Array("wp-components", "wp-editor", "wp-block-library", "wp-block-library-theme"))
    package_styles = Array({"block-editor": Array("wp-components", "wp-editor-font"), "block-library": Array(), "components": Array(), "edit-post": Array("wp-components", "wp-block-editor", "wp-editor", "wp-edit-blocks", "wp-block-library", "wp-nux"), "editor": Array("wp-components", "wp-block-editor", "wp-nux"), "format-library": Array(), "list-reusable-blocks": Array("wp-components"), "nux": Array("wp-components")})
    for package,dependencies in package_styles:
        handle = "wp-" + package
        path = str("/wp-includes/css/dist/") + str(package) + str("/style") + str(suffix) + str(".css")
        styles.add(handle, path, dependencies)
    # end for
    #// RTL CSS.
    rtl_styles = Array("common", "forms", "admin-menu", "dashboard", "list-tables", "edit", "revisions", "media", "themes", "about", "nav-menus", "widgets", "site-icon", "l10n", "install", "wp-color-picker", "customize-controls", "customize-widgets", "customize-nav-menus", "customize-preview", "ie", "login", "site-health", "buttons", "admin-bar", "wp-auth-check", "editor-buttons", "media-views", "wp-pointer", "wp-jquery-ui-dialog", "wp-block-library-theme", "wp-edit-blocks", "wp-block-editor", "wp-block-library", "wp-components", "wp-edit-post", "wp-editor", "wp-format-library", "wp-list-reusable-blocks", "wp-nux", "deprecated-media", "farbtastic")
    for rtl_style in rtl_styles:
        styles.add_data(rtl_style, "rtl", "replace")
        if suffix:
            styles.add_data(rtl_style, "suffix", suffix)
        # end if
    # end for
# end def wp_default_styles
#// 
#// Reorder JavaScript scripts array to place prototype before jQuery.
#// 
#// @since 2.3.1
#// 
#// @param array $js_array JavaScript scripts array
#// @return array Reordered array, if needed.
#//
def wp_prototype_before_jquery(js_array=None, *args_):
    
    prototype = php_array_search("prototype", js_array, True)
    if False == prototype:
        return js_array
    # end if
    jquery = php_array_search("jquery", js_array, True)
    if False == jquery:
        return js_array
    # end if
    if prototype < jquery:
        return js_array
    # end if
    js_array[prototype] = None
    array_splice(js_array, jquery, 0, "prototype")
    return js_array
# end def wp_prototype_before_jquery
#// 
#// Load localized data on print rather than initialization.
#// 
#// These localizations require information that may not be loaded even by init.
#// 
#// @since 2.5.0
#//
def wp_just_in_time_script_localization(*args_):
    
    wp_localize_script("autosave", "autosaveL10n", Array({"autosaveInterval": AUTOSAVE_INTERVAL, "blog_id": get_current_blog_id()}))
    wp_localize_script("mce-view", "mceViewL10n", Array({"shortcodes": php_array_keys(PHP_GLOBALS["shortcode_tags"]) if (not php_empty(lambda : PHP_GLOBALS["shortcode_tags"])) else Array()}))
    wp_localize_script("word-count", "wordCountL10n", Array({"type": _x("words", "Word count type. Do not translate!"), "shortcodes": php_array_keys(PHP_GLOBALS["shortcode_tags"]) if (not php_empty(lambda : PHP_GLOBALS["shortcode_tags"])) else Array()}))
# end def wp_just_in_time_script_localization
#// 
#// Localizes the jQuery UI datepicker.
#// 
#// @since 4.6.0
#// 
#// @link https://api.jqueryui.com/datepicker/#options
#// 
#// @global WP_Locale $wp_locale WordPress date and time locale object.
#//
def wp_localize_jquery_ui_datepicker(*args_):
    
    global wp_locale
    php_check_if_defined("wp_locale")
    if (not wp_script_is("jquery-ui-datepicker", "enqueued")):
        return
    # end if
    #// Convert the PHP date format into jQuery UI's format.
    datepicker_date_format = php_str_replace(Array("d", "j", "l", "z", "F", "M", "n", "m", "Y", "y"), Array("dd", "d", "DD", "o", "MM", "M", "m", "mm", "yy", "y"), get_option("date_format"))
    datepicker_defaults = wp_json_encode(Array({"closeText": __("Close"), "currentText": __("Today"), "monthNames": php_array_values(wp_locale.month), "monthNamesShort": php_array_values(wp_locale.month_abbrev), "nextText": __("Next"), "prevText": __("Previous"), "dayNames": php_array_values(wp_locale.weekday), "dayNamesShort": php_array_values(wp_locale.weekday_abbrev), "dayNamesMin": php_array_values(wp_locale.weekday_initial), "dateFormat": datepicker_date_format, "firstDay": absint(get_option("start_of_week")), "isRTL": wp_locale.is_rtl()}))
    wp_add_inline_script("jquery-ui-datepicker", str("jQuery(document).ready(function(jQuery){jQuery.datepicker.setDefaults(") + str(datepicker_defaults) + str(");});"))
# end def wp_localize_jquery_ui_datepicker
#// 
#// Localizes community events data that needs to be passed to dashboard.js.
#// 
#// @since 4.8.0
#//
def wp_localize_community_events(*args_):
    
    if (not wp_script_is("dashboard")):
        return
    # end if
    php_include_file(ABSPATH + "wp-admin/includes/class-wp-community-events.php", once=True)
    user_id = get_current_user_id()
    saved_location = get_user_option("community-events-location", user_id)
    saved_ip_address = saved_location["ip"] if (php_isset(lambda : saved_location["ip"])) else False
    current_ip_address = WP_Community_Events.get_unsafe_client_ip()
    #// 
    #// If the user's location is based on their IP address, then update their
    #// location when their IP address changes. This allows them to see events
    #// in their current city when travelling. Otherwise, they would always be
    #// shown events in the city where they were when they first loaded the
    #// Dashboard, which could have been months or years ago.
    #//
    if saved_ip_address and current_ip_address and current_ip_address != saved_ip_address:
        saved_location["ip"] = current_ip_address
        update_user_option(user_id, "community-events-location", saved_location, True)
    # end if
    events_client = php_new_class("WP_Community_Events", lambda : WP_Community_Events(user_id, saved_location))
    wp_localize_script("dashboard", "communityEventsData", Array({"nonce": wp_create_nonce("community_events"), "cache": events_client.get_cached_events(), "l10n": Array({"enter_closest_city": __("Enter your closest city to find nearby events."), "error_occurred_please_try_again": __("An error occurred. Please try again."), "attend_event_near_generic": __("Attend an upcoming event near you."), "could_not_locate_city": __("We couldn&#8217;t locate %s. Please try another nearby city. For example: Kansas City; Springfield; Portland."), "city_updated": __("City updated. Listing events near %s.")})}))
# end def wp_localize_community_events
#// 
#// Administration Screen CSS for changing the styles.
#// 
#// If installing the 'wp-admin/' directory will be replaced with './'.
#// 
#// The $_wp_admin_css_colors global manages the Administration Screens CSS
#// stylesheet that is loaded. The option that is set is 'admin_color' and is the
#// color and key for the array. The value for the color key is an object with
#// a 'url' parameter that has the URL path to the CSS file.
#// 
#// The query from $src parameter will be appended to the URL that is given from
#// the $_wp_admin_css_colors array value URL.
#// 
#// @since 2.6.0
#// @global array $_wp_admin_css_colors
#// 
#// @param string $src    Source URL.
#// @param string $handle Either 'colors' or 'colors-rtl'.
#// @return string|false URL path to CSS stylesheet for Administration Screens.
#//
def wp_style_loader_src(src=None, handle=None, *args_):
    
    global _wp_admin_css_colors
    php_check_if_defined("_wp_admin_css_colors")
    if wp_installing():
        return php_preg_replace("#^wp-admin/#", "./", src)
    # end if
    if "colors" == handle:
        color = get_user_option("admin_color")
        if php_empty(lambda : color) or (not (php_isset(lambda : _wp_admin_css_colors[color]))):
            color = "fresh"
        # end if
        color = _wp_admin_css_colors[color]
        url = color.url
        if (not url):
            return False
        # end if
        parsed = php_parse_url(src)
        if (php_isset(lambda : parsed["query"])) and parsed["query"]:
            wp_parse_str(parsed["query"], qv)
            url = add_query_arg(qv, url)
        # end if
        return url
    # end if
    return src
# end def wp_style_loader_src
#// 
#// Prints the script queue in the HTML head on admin pages.
#// 
#// Postpones the scripts that were queued for the footer.
#// print_footer_scripts() is called in the footer to print these scripts.
#// 
#// @since 2.8.0
#// 
#// @see wp_print_scripts()
#// 
#// @global bool $concatenate_scripts
#// 
#// @return array
#//
def print_head_scripts(*args_):
    
    global concatenate_scripts
    php_check_if_defined("concatenate_scripts")
    if (not did_action("wp_print_scripts")):
        #// This action is documented in wp-includes/functions.wp-scripts.php
        do_action("wp_print_scripts")
    # end if
    wp_scripts = wp_scripts()
    script_concat_settings()
    wp_scripts.do_concat = concatenate_scripts
    wp_scripts.do_head_items()
    #// 
    #// Filters whether to print the head scripts.
    #// 
    #// @since 2.8.0
    #// 
    #// @param bool $print Whether to print the head scripts. Default true.
    #//
    if apply_filters("print_head_scripts", True):
        _print_scripts()
    # end if
    wp_scripts.reset()
    return wp_scripts.done
# end def print_head_scripts
#// 
#// Prints the scripts that were queued for the footer or too late for the HTML head.
#// 
#// @since 2.8.0
#// 
#// @global WP_Scripts $wp_scripts
#// @global bool       $concatenate_scripts
#// 
#// @return array
#//
def print_footer_scripts(*args_):
    
    global wp_scripts,concatenate_scripts
    php_check_if_defined("wp_scripts","concatenate_scripts")
    if (not type(wp_scripts).__name__ == "WP_Scripts"):
        return Array()
        pass
    # end if
    script_concat_settings()
    wp_scripts.do_concat = concatenate_scripts
    wp_scripts.do_footer_items()
    #// 
    #// Filters whether to print the footer scripts.
    #// 
    #// @since 2.8.0
    #// 
    #// @param bool $print Whether to print the footer scripts. Default true.
    #//
    if apply_filters("print_footer_scripts", True):
        _print_scripts()
    # end if
    wp_scripts.reset()
    return wp_scripts.done
# end def print_footer_scripts
#// 
#// Print scripts (internal use only)
#// 
#// @ignore
#// 
#// @global WP_Scripts $wp_scripts
#// @global bool       $compress_scripts
#//
def _print_scripts(*args_):
    
    global wp_scripts,compress_scripts
    php_check_if_defined("wp_scripts","compress_scripts")
    zip = 1 if compress_scripts else 0
    if zip and php_defined("ENFORCE_GZIP") and ENFORCE_GZIP:
        zip = "gzip"
    # end if
    concat = php_trim(wp_scripts.concat, ", ")
    type_attr = "" if current_theme_supports("html5", "script") else " type='text/javascript'"
    if concat:
        if (not php_empty(lambda : wp_scripts.print_code)):
            php_print(str("\n<script") + str(type_attr) + str(">\n"))
            php_print("/* <![CDATA[ */\n")
            #// Not needed in HTML 5.
            php_print(wp_scripts.print_code)
            php_print("/* ]]> */\n")
            php_print("</script>\n")
        # end if
        concat = str_split(concat, 128)
        concatenated = ""
        for key,chunk in concat:
            concatenated += str("&load%5Bchunk_") + str(key) + str("%5D=") + str(chunk)
        # end for
        src = wp_scripts.base_url + str("/wp-admin/load-scripts.php?c=") + str(zip) + concatenated + "&ver=" + wp_scripts.default_version
        php_print(str("<script") + str(type_attr) + str(" src='") + esc_attr(src) + "'></script>\n")
    # end if
    if (not php_empty(lambda : wp_scripts.print_html)):
        php_print(wp_scripts.print_html)
    # end if
# end def _print_scripts
#// 
#// Prints the script queue in the HTML head on the front end.
#// 
#// Postpones the scripts that were queued for the footer.
#// wp_print_footer_scripts() is called in the footer to print these scripts.
#// 
#// @since 2.8.0
#// 
#// @global WP_Scripts $wp_scripts
#// 
#// @return array
#//
def wp_print_head_scripts(*args_):
    
    if (not did_action("wp_print_scripts")):
        #// This action is documented in wp-includes/functions.wp-scripts.php
        do_action("wp_print_scripts")
    # end if
    global wp_scripts
    php_check_if_defined("wp_scripts")
    if (not type(wp_scripts).__name__ == "WP_Scripts"):
        return Array()
        pass
    # end if
    return print_head_scripts()
# end def wp_print_head_scripts
#// 
#// Private, for use in *_footer_scripts hooks
#// 
#// @since 3.3.0
#//
def _wp_footer_scripts(*args_):
    
    print_late_styles()
    print_footer_scripts()
# end def _wp_footer_scripts
#// 
#// Hooks to print the scripts and styles in the footer.
#// 
#// @since 2.8.0
#//
def wp_print_footer_scripts(*args_):
    
    #// 
    #// Fires when footer scripts are printed.
    #// 
    #// @since 2.8.0
    #//
    do_action("wp_print_footer_scripts")
# end def wp_print_footer_scripts
#// 
#// Wrapper for do_action('wp_enqueue_scripts')
#// 
#// Allows plugins to queue scripts for the front end using wp_enqueue_script().
#// Runs first in wp_head() where all is_home(), is_page(), etc. functions are available.
#// 
#// @since 2.8.0
#//
def wp_enqueue_scripts(*args_):
    
    #// 
    #// Fires when scripts and styles are enqueued.
    #// 
    #// @since 2.8.0
    #//
    do_action("wp_enqueue_scripts")
# end def wp_enqueue_scripts
#// 
#// Prints the styles queue in the HTML head on admin pages.
#// 
#// @since 2.8.0
#// 
#// @global bool $concatenate_scripts
#// 
#// @return array
#//
def print_admin_styles(*args_):
    
    global concatenate_scripts
    php_check_if_defined("concatenate_scripts")
    wp_styles = wp_styles()
    script_concat_settings()
    wp_styles.do_concat = concatenate_scripts
    wp_styles.do_items(False)
    #// 
    #// Filters whether to print the admin styles.
    #// 
    #// @since 2.8.0
    #// 
    #// @param bool $print Whether to print the admin styles. Default true.
    #//
    if apply_filters("print_admin_styles", True):
        _print_styles()
    # end if
    wp_styles.reset()
    return wp_styles.done
# end def print_admin_styles
#// 
#// Prints the styles that were queued too late for the HTML head.
#// 
#// @since 3.3.0
#// 
#// @global WP_Styles $wp_styles
#// @global bool      $concatenate_scripts
#// 
#// @return array|void
#//
def print_late_styles(*args_):
    
    global wp_styles,concatenate_scripts
    php_check_if_defined("wp_styles","concatenate_scripts")
    if (not type(wp_styles).__name__ == "WP_Styles"):
        return
    # end if
    script_concat_settings()
    wp_styles.do_concat = concatenate_scripts
    wp_styles.do_footer_items()
    #// 
    #// Filters whether to print the styles queued too late for the HTML head.
    #// 
    #// @since 3.3.0
    #// 
    #// @param bool $print Whether to print the 'late' styles. Default true.
    #//
    if apply_filters("print_late_styles", True):
        _print_styles()
    # end if
    wp_styles.reset()
    return wp_styles.done
# end def print_late_styles
#// 
#// Print styles (internal use only)
#// 
#// @ignore
#// @since 3.3.0
#// 
#// @global bool $compress_css
#//
def _print_styles(*args_):
    
    global compress_css
    php_check_if_defined("compress_css")
    wp_styles = wp_styles()
    zip = 1 if compress_css else 0
    if zip and php_defined("ENFORCE_GZIP") and ENFORCE_GZIP:
        zip = "gzip"
    # end if
    concat = php_trim(wp_styles.concat, ", ")
    type_attr = "" if current_theme_supports("html5", "style") else " type=\"text/css\""
    if concat:
        dir = wp_styles.text_direction
        ver = wp_styles.default_version
        concat = str_split(concat, 128)
        concatenated = ""
        for key,chunk in concat:
            concatenated += str("&load%5Bchunk_") + str(key) + str("%5D=") + str(chunk)
        # end for
        href = wp_styles.base_url + str("/wp-admin/load-styles.php?c=") + str(zip) + str("&dir=") + str(dir) + concatenated + "&ver=" + ver
        php_print("<link rel='stylesheet' href='" + esc_attr(href) + str("'") + str(type_attr) + str(" media='all' />\n"))
        if (not php_empty(lambda : wp_styles.print_code)):
            php_print(str("<style") + str(type_attr) + str(">\n"))
            php_print(wp_styles.print_code)
            php_print("\n</style>\n")
        # end if
    # end if
    if (not php_empty(lambda : wp_styles.print_html)):
        php_print(wp_styles.print_html)
    # end if
# end def _print_styles
#// 
#// Determine the concatenation and compression settings for scripts and styles.
#// 
#// @since 2.8.0
#// 
#// @global bool $concatenate_scripts
#// @global bool $compress_scripts
#// @global bool $compress_css
#//
def script_concat_settings(*args_):
    
    global concatenate_scripts,compress_scripts,compress_css
    php_check_if_defined("concatenate_scripts","compress_scripts","compress_css")
    compressed_output = php_ini_get("zlib.output_compression") or "ob_gzhandler" == php_ini_get("output_handler")
    if (not (php_isset(lambda : concatenate_scripts))):
        concatenate_scripts = CONCATENATE_SCRIPTS if php_defined("CONCATENATE_SCRIPTS") else True
        if (not is_admin()) and (not did_action("login_init")) or php_defined("SCRIPT_DEBUG") and SCRIPT_DEBUG:
            concatenate_scripts = False
        # end if
    # end if
    if (not (php_isset(lambda : compress_scripts))):
        compress_scripts = COMPRESS_SCRIPTS if php_defined("COMPRESS_SCRIPTS") else True
        if compress_scripts and (not get_site_option("can_compress_scripts")) or compressed_output:
            compress_scripts = False
        # end if
    # end if
    if (not (php_isset(lambda : compress_css))):
        compress_css = COMPRESS_CSS if php_defined("COMPRESS_CSS") else True
        if compress_css and (not get_site_option("can_compress_scripts")) or compressed_output:
            compress_css = False
        # end if
    # end if
# end def script_concat_settings
#// 
#// Handles the enqueueing of block scripts and styles that are common to both
#// the editor and the front-end.
#// 
#// @since 5.0.0
#// 
#// @global WP_Screen $current_screen WordPress current screen object.
#//
def wp_common_block_scripts_and_styles(*args_):
    
    global current_screen
    php_check_if_defined("current_screen")
    if is_admin() and type(current_screen).__name__ == "WP_Screen" and (not current_screen.is_block_editor()):
        return
    # end if
    wp_enqueue_style("wp-block-library")
    if current_theme_supports("wp-block-styles"):
        wp_enqueue_style("wp-block-library-theme")
    # end if
    #// 
    #// Fires after enqueuing block assets for both editor and front-end.
    #// 
    #// Call `add_action` on any hook before 'wp_enqueue_scripts'.
    #// 
    #// In the function call you supply, simply use `wp_enqueue_script` and
    #// `wp_enqueue_style` to add your functionality to the Gutenberg editor.
    #// 
    #// @since 5.0.0
    #//
    do_action("enqueue_block_assets")
# end def wp_common_block_scripts_and_styles
#// 
#// Enqueues registered block scripts and styles, depending on current rendered
#// context (only enqueuing editor scripts while in context of the editor).
#// 
#// @since 5.0.0
#// 
#// @global WP_Screen $current_screen WordPress current screen object.
#//
def wp_enqueue_registered_block_scripts_and_styles(*args_):
    
    global current_screen
    php_check_if_defined("current_screen")
    is_editor = type(current_screen).__name__ == "WP_Screen" and current_screen.is_block_editor()
    block_registry = WP_Block_Type_Registry.get_instance()
    for block_name,block_type in block_registry.get_all_registered():
        #// Front-end styles.
        if (not php_empty(lambda : block_type.style)):
            wp_enqueue_style(block_type.style)
        # end if
        #// Front-end script.
        if (not php_empty(lambda : block_type.script)):
            wp_enqueue_script(block_type.script)
        # end if
        #// Editor styles.
        if is_editor and (not php_empty(lambda : block_type.editor_style)):
            wp_enqueue_style(block_type.editor_style)
        # end if
        #// Editor script.
        if is_editor and (not php_empty(lambda : block_type.editor_script)):
            wp_enqueue_script(block_type.editor_script)
        # end if
    # end for
# end def wp_enqueue_registered_block_scripts_and_styles
#// 
#// Function responsible for enqueuing the styles required for block styles functionality on the editor and on the frontend.
#// 
#// @since 5.3.0
#//
def enqueue_block_styles_assets(*args_):
    
    block_styles = WP_Block_Styles_Registry.get_instance().get_all_registered()
    for styles in block_styles:
        for style_properties in styles:
            if (php_isset(lambda : style_properties["style_handle"])):
                wp_enqueue_style(style_properties["style_handle"])
            # end if
            if (php_isset(lambda : style_properties["inline_style"])):
                wp_add_inline_style("wp-block-library", style_properties["inline_style"])
            # end if
        # end for
    # end for
# end def enqueue_block_styles_assets
#// 
#// Function responsible for enqueuing the assets required for block styles functionality on the editor.
#// 
#// @since 5.3.0
#//
def enqueue_editor_block_styles_assets(*args_):
    
    block_styles = WP_Block_Styles_Registry.get_instance().get_all_registered()
    register_script_lines = Array("( function() {")
    for block_name,styles in block_styles:
        for style_properties in styles:
            register_script_lines[-1] = php_sprintf("   wp.blocks.registerBlockStyle( '%s', %s );", block_name, wp_json_encode(Array({"name": style_properties["name"], "label": style_properties["label"]})))
        # end for
    # end for
    register_script_lines[-1] = "} )();"
    inline_script = php_implode("\n", register_script_lines)
    wp_register_script("wp-block-styles", False, Array("wp-blocks"), True, True)
    wp_add_inline_script("wp-block-styles", inline_script)
    wp_enqueue_script("wp-block-styles")
# end def enqueue_editor_block_styles_assets
