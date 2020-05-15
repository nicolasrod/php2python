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
#// Theme, template, and stylesheet functions.
#// 
#// @package WordPress
#// @subpackage Theme
#// 
#// 
#// Returns an array of WP_Theme objects based on the arguments.
#// 
#// Despite advances over get_themes(), this function is quite expensive, and grows
#// linearly with additional themes. Stick to wp_get_theme() if possible.
#// 
#// @since 3.4.0
#// 
#// @global array $wp_theme_directories
#// @staticvar array $_themes
#// 
#// @param array $args {
#// Optional. The search arguments.
#// 
#// @type mixed $errors  True to return themes with errors, false to return themes without errors, null to return all themes.
#// Defaults to false.
#// @type mixed $allowed (Multisite) True to return only allowed themes for a site. False to return only disallowed themes for a site.
#// 'site' to return only site-allowed themes. 'network' to return only network-allowed themes.
#// Null to return all themes. Defaults to null.
#// @type int   $blog_id (Multisite) The blog ID used to calculate which themes are allowed.
#// Defaults to 0, synonymous for the current blog.
#// }
#// @return WP_Theme[] Array of WP_Theme objects.
#//
def wp_get_themes(args=Array(), *args_):
    
    global wp_theme_directories
    php_check_if_defined("wp_theme_directories")
    defaults = Array({"errors": False, "allowed": None, "blog_id": 0})
    args = wp_parse_args(args, defaults)
    theme_directories = search_theme_directories()
    if php_is_array(wp_theme_directories) and php_count(wp_theme_directories) > 1:
        #// Make sure the current theme wins out, in case search_theme_directories() picks the wrong
        #// one in the case of a conflict. (Normally, last registered theme root wins.)
        current_theme = get_stylesheet()
        if (php_isset(lambda : theme_directories[current_theme])):
            root_of_current_theme = get_raw_theme_root(current_theme)
            if (not php_in_array(root_of_current_theme, wp_theme_directories)):
                root_of_current_theme = WP_CONTENT_DIR + root_of_current_theme
            # end if
            theme_directories[current_theme]["theme_root"] = root_of_current_theme
        # end if
    # end if
    if php_empty(lambda : theme_directories):
        return Array()
    # end if
    if is_multisite() and None != args["allowed"]:
        allowed = args["allowed"]
        if "network" == allowed:
            theme_directories = php_array_intersect_key(theme_directories, WP_Theme.get_allowed_on_network())
        elif "site" == allowed:
            theme_directories = php_array_intersect_key(theme_directories, WP_Theme.get_allowed_on_site(args["blog_id"]))
        elif allowed:
            theme_directories = php_array_intersect_key(theme_directories, WP_Theme.get_allowed(args["blog_id"]))
        else:
            theme_directories = php_array_diff_key(theme_directories, WP_Theme.get_allowed(args["blog_id"]))
        # end if
    # end if
    themes = Array()
    _themes = Array()
    for theme,theme_root in theme_directories:
        if (php_isset(lambda : _themes[theme_root["theme_root"] + "/" + theme])):
            themes[theme] = _themes[theme_root["theme_root"] + "/" + theme]
        else:
            themes[theme] = php_new_class("WP_Theme", lambda : WP_Theme(theme, theme_root["theme_root"]))
            _themes[theme_root["theme_root"] + "/" + theme] = themes[theme]
        # end if
    # end for
    if None != args["errors"]:
        for theme,wp_theme in themes:
            if wp_theme.errors() != args["errors"]:
                themes[theme] = None
            # end if
        # end for
    # end if
    return themes
# end def wp_get_themes
#// 
#// Gets a WP_Theme object for a theme.
#// 
#// @since 3.4.0
#// 
#// @global array $wp_theme_directories
#// 
#// @param string $stylesheet Directory name for the theme. Optional. Defaults to current theme.
#// @param string $theme_root Absolute path of the theme root to look in. Optional. If not specified, get_raw_theme_root()
#// is used to calculate the theme root for the $stylesheet provided (or current theme).
#// @return WP_Theme Theme object. Be sure to check the object's exists() method if you need to confirm the theme's existence.
#//
def wp_get_theme(stylesheet="", theme_root="", *args_):
    
    global wp_theme_directories
    php_check_if_defined("wp_theme_directories")
    if php_empty(lambda : stylesheet):
        stylesheet = get_stylesheet()
    # end if
    if php_empty(lambda : theme_root):
        theme_root = get_raw_theme_root(stylesheet)
        if False == theme_root:
            theme_root = WP_CONTENT_DIR + "/themes"
        elif (not php_in_array(theme_root, wp_theme_directories)):
            theme_root = WP_CONTENT_DIR + theme_root
        # end if
    # end if
    return php_new_class("WP_Theme", lambda : WP_Theme(stylesheet, theme_root))
# end def wp_get_theme
#// 
#// Clears the cache held by get_theme_roots() and WP_Theme.
#// 
#// @since 3.5.0
#// @param bool $clear_update_cache Whether to clear the Theme updates cache
#//
def wp_clean_themes_cache(clear_update_cache=True, *args_):
    
    if clear_update_cache:
        delete_site_transient("update_themes")
    # end if
    search_theme_directories(True)
    for theme in wp_get_themes(Array({"errors": None})):
        theme.cache_delete()
    # end for
# end def wp_clean_themes_cache
#// 
#// Whether a child theme is in use.
#// 
#// @since 3.0.0
#// 
#// @return bool true if a child theme is in use, false otherwise.
#//
def is_child_theme(*args_):
    
    return TEMPLATEPATH != STYLESHEETPATH
# end def is_child_theme
#// 
#// Retrieve name of the current stylesheet.
#// 
#// The theme name that the administrator has currently set the front end theme
#// as.
#// 
#// For all intents and purposes, the template name and the stylesheet name are
#// going to be the same for most cases.
#// 
#// @since 1.5.0
#// 
#// @return string Stylesheet name.
#//
def get_stylesheet(*args_):
    
    #// 
    #// Filters the name of current stylesheet.
    #// 
    #// @since 1.5.0
    #// 
    #// @param string $stylesheet Name of the current stylesheet.
    #//
    return apply_filters("stylesheet", get_option("stylesheet"))
# end def get_stylesheet
#// 
#// Retrieve stylesheet directory path for current theme.
#// 
#// @since 1.5.0
#// 
#// @return string Path to current theme directory.
#//
def get_stylesheet_directory(*args_):
    
    stylesheet = get_stylesheet()
    theme_root = get_theme_root(stylesheet)
    stylesheet_dir = str(theme_root) + str("/") + str(stylesheet)
    #// 
    #// Filters the stylesheet directory path for current theme.
    #// 
    #// @since 1.5.0
    #// 
    #// @param string $stylesheet_dir Absolute path to the current theme.
    #// @param string $stylesheet     Directory name of the current theme.
    #// @param string $theme_root     Absolute path to themes directory.
    #//
    return apply_filters("stylesheet_directory", stylesheet_dir, stylesheet, theme_root)
# end def get_stylesheet_directory
#// 
#// Retrieve stylesheet directory URI.
#// 
#// @since 1.5.0
#// 
#// @return string
#//
def get_stylesheet_directory_uri(*args_):
    
    stylesheet = php_str_replace("%2F", "/", rawurlencode(get_stylesheet()))
    theme_root_uri = get_theme_root_uri(stylesheet)
    stylesheet_dir_uri = str(theme_root_uri) + str("/") + str(stylesheet)
    #// 
    #// Filters the stylesheet directory URI.
    #// 
    #// @since 1.5.0
    #// 
    #// @param string $stylesheet_dir_uri Stylesheet directory URI.
    #// @param string $stylesheet         Name of the activated theme's directory.
    #// @param string $theme_root_uri     Themes root URI.
    #//
    return apply_filters("stylesheet_directory_uri", stylesheet_dir_uri, stylesheet, theme_root_uri)
# end def get_stylesheet_directory_uri
#// 
#// Retrieves the URI of current theme stylesheet.
#// 
#// The stylesheet file name is 'style.css' which is appended to the stylesheet directory URI path.
#// See get_stylesheet_directory_uri().
#// 
#// @since 1.5.0
#// 
#// @return string
#//
def get_stylesheet_uri(*args_):
    
    stylesheet_dir_uri = get_stylesheet_directory_uri()
    stylesheet_uri = stylesheet_dir_uri + "/style.css"
    #// 
    #// Filters the URI of the current theme stylesheet.
    #// 
    #// @since 1.5.0
    #// 
    #// @param string $stylesheet_uri     Stylesheet URI for the current theme/child theme.
    #// @param string $stylesheet_dir_uri Stylesheet directory URI for the current theme/child theme.
    #//
    return apply_filters("stylesheet_uri", stylesheet_uri, stylesheet_dir_uri)
# end def get_stylesheet_uri
#// 
#// Retrieves the localized stylesheet URI.
#// 
#// The stylesheet directory for the localized stylesheet files are located, by
#// default, in the base theme directory. The name of the locale file will be the
#// locale followed by '.css'. If that does not exist, then the text direction
#// stylesheet will be checked for existence, for example 'ltr.css'.
#// 
#// The theme may change the location of the stylesheet directory by either using
#// the {@see 'stylesheet_directory_uri'} or {@see 'locale_stylesheet_uri'} filters.
#// 
#// If you want to change the location of the stylesheet files for the entire
#// WordPress workflow, then change the former. If you just have the locale in a
#// separate folder, then change the latter.
#// 
#// @since 2.1.0
#// 
#// @global WP_Locale $wp_locale WordPress date and time locale object.
#// 
#// @return string
#//
def get_locale_stylesheet_uri(*args_):
    
    global wp_locale
    php_check_if_defined("wp_locale")
    stylesheet_dir_uri = get_stylesheet_directory_uri()
    dir = get_stylesheet_directory()
    locale = get_locale()
    if php_file_exists(str(dir) + str("/") + str(locale) + str(".css")):
        stylesheet_uri = str(stylesheet_dir_uri) + str("/") + str(locale) + str(".css")
    elif (not php_empty(lambda : wp_locale.text_direction)) and php_file_exists(str(dir) + str("/") + str(wp_locale.text_direction) + str(".css")):
        stylesheet_uri = str(stylesheet_dir_uri) + str("/") + str(wp_locale.text_direction) + str(".css")
    else:
        stylesheet_uri = ""
    # end if
    #// 
    #// Filters the localized stylesheet URI.
    #// 
    #// @since 2.1.0
    #// 
    #// @param string $stylesheet_uri     Localized stylesheet URI.
    #// @param string $stylesheet_dir_uri Stylesheet directory URI.
    #//
    return apply_filters("locale_stylesheet_uri", stylesheet_uri, stylesheet_dir_uri)
# end def get_locale_stylesheet_uri
#// 
#// Retrieve name of the current theme.
#// 
#// @since 1.5.0
#// 
#// @return string Template name.
#//
def get_template(*args_):
    
    #// 
    #// Filters the name of the current theme.
    #// 
    #// @since 1.5.0
    #// 
    #// @param string $template Current theme's directory name.
    #//
    return apply_filters("template", get_option("template"))
# end def get_template
#// 
#// Retrieve current theme directory.
#// 
#// @since 1.5.0
#// 
#// @return string Template directory path.
#//
def get_template_directory(*args_):
    
    template = get_template()
    theme_root = get_theme_root(template)
    template_dir = str(theme_root) + str("/") + str(template)
    #// 
    #// Filters the current theme directory path.
    #// 
    #// @since 1.5.0
    #// 
    #// @param string $template_dir The URI of the current theme directory.
    #// @param string $template     Directory name of the current theme.
    #// @param string $theme_root   Absolute path to the themes directory.
    #//
    return apply_filters("template_directory", template_dir, template, theme_root)
# end def get_template_directory
#// 
#// Retrieve theme directory URI.
#// 
#// @since 1.5.0
#// 
#// @return string Template directory URI.
#//
def get_template_directory_uri(*args_):
    
    template = php_str_replace("%2F", "/", rawurlencode(get_template()))
    theme_root_uri = get_theme_root_uri(template)
    template_dir_uri = str(theme_root_uri) + str("/") + str(template)
    #// 
    #// Filters the current theme directory URI.
    #// 
    #// @since 1.5.0
    #// 
    #// @param string $template_dir_uri The URI of the current theme directory.
    #// @param string $template         Directory name of the current theme.
    #// @param string $theme_root_uri   The themes root URI.
    #//
    return apply_filters("template_directory_uri", template_dir_uri, template, theme_root_uri)
# end def get_template_directory_uri
#// 
#// Retrieve theme roots.
#// 
#// @since 2.9.0
#// 
#// @global array $wp_theme_directories
#// 
#// @return array|string An array of theme roots keyed by template/stylesheet or a single theme root if all themes have the same root.
#//
def get_theme_roots(*args_):
    
    global wp_theme_directories
    php_check_if_defined("wp_theme_directories")
    if (not php_is_array(wp_theme_directories)) or php_count(wp_theme_directories) <= 1:
        return "/themes"
    # end if
    theme_roots = get_site_transient("theme_roots")
    if False == theme_roots:
        search_theme_directories(True)
        #// Regenerate the transient.
        theme_roots = get_site_transient("theme_roots")
    # end if
    return theme_roots
# end def get_theme_roots
#// 
#// Register a directory that contains themes.
#// 
#// @since 2.9.0
#// 
#// @global array $wp_theme_directories
#// 
#// @param string $directory Either the full filesystem path to a theme folder or a folder within WP_CONTENT_DIR
#// @return bool
#//
def register_theme_directory(directory=None, *args_):
    
    global wp_theme_directories
    php_check_if_defined("wp_theme_directories")
    if (not php_file_exists(directory)):
        #// Try prepending as the theme directory could be relative to the content directory.
        directory = WP_CONTENT_DIR + "/" + directory
        #// If this directory does not exist, return and do not register.
        if (not php_file_exists(directory)):
            return False
        # end if
    # end if
    if (not php_is_array(wp_theme_directories)):
        wp_theme_directories = Array()
    # end if
    untrailed = untrailingslashit(directory)
    if (not php_empty(lambda : untrailed)) and (not php_in_array(untrailed, wp_theme_directories)):
        wp_theme_directories[-1] = untrailed
    # end if
    return True
# end def register_theme_directory
#// 
#// Search all registered theme directories for complete and valid themes.
#// 
#// @since 2.9.0
#// 
#// @global array $wp_theme_directories
#// @staticvar array $found_themes
#// 
#// @param bool $force Optional. Whether to force a new directory scan. Defaults to false.
#// @return array|false Valid themes found
#//
def search_theme_directories(force=False, *args_):
    
    global wp_theme_directories
    php_check_if_defined("wp_theme_directories")
    found_themes = None
    if php_empty(lambda : wp_theme_directories):
        return False
    # end if
    if (not force) and (php_isset(lambda : found_themes)):
        return found_themes
    # end if
    found_themes = Array()
    wp_theme_directories = wp_theme_directories
    relative_theme_roots = Array()
    #// 
    #// Set up maybe-relative, maybe-absolute array of theme directories.
    #// We always want to return absolute, but we need to cache relative
    #// to use in get_theme_root().
    #//
    for theme_root in wp_theme_directories:
        if 0 == php_strpos(theme_root, WP_CONTENT_DIR):
            relative_theme_roots[php_str_replace(WP_CONTENT_DIR, "", theme_root)] = theme_root
        else:
            relative_theme_roots[theme_root] = theme_root
        # end if
    # end for
    #// 
    #// Filters whether to get the cache of the registered theme directories.
    #// 
    #// @since 3.4.0
    #// 
    #// @param bool   $cache_expiration Whether to get the cache of the theme directories. Default false.
    #// @param string $cache_directory  Directory to be searched for the cache.
    #//
    cache_expiration = apply_filters("wp_cache_themes_persistently", False, "search_theme_directories")
    if cache_expiration:
        cached_roots = get_site_transient("theme_roots")
        if php_is_array(cached_roots):
            for theme_dir,theme_root in cached_roots:
                #// A cached theme root is no longer around, so skip it.
                if (not (php_isset(lambda : relative_theme_roots[theme_root]))):
                    continue
                # end if
                found_themes[theme_dir] = Array({"theme_file": theme_dir + "/style.css", "theme_root": relative_theme_roots[theme_root]})
            # end for
            return found_themes
        # end if
        if (not php_is_int(cache_expiration)):
            cache_expiration = 30 * MINUTE_IN_SECONDS
        # end if
    else:
        cache_expiration = 30 * MINUTE_IN_SECONDS
    # end if
    #// Loop the registered theme directories and extract all themes
    for theme_root in wp_theme_directories:
        #// Start with directories in the root of the current theme directory.
        dirs = php_no_error(lambda: scandir(theme_root))
        if (not dirs):
            trigger_error(str(theme_root) + str(" is not readable"), E_USER_NOTICE)
            continue
        # end if
        for dir in dirs:
            if (not php_is_dir(theme_root + "/" + dir)) or "." == dir[0] or "CVS" == dir:
                continue
            # end if
            if php_file_exists(theme_root + "/" + dir + "/style.css"):
                #// wp-content/themes/a-single-theme
                #// wp-content/themes is $theme_root, a-single-theme is $dir.
                found_themes[dir] = Array({"theme_file": dir + "/style.css", "theme_root": theme_root})
            else:
                found_theme = False
                #// wp-content/themes/a-folder-of-themes
                #// wp-content/themes is $theme_root, a-folder-of-themes is $dir, then themes are $sub_dirs.
                sub_dirs = php_no_error(lambda: scandir(theme_root + "/" + dir))
                if (not sub_dirs):
                    trigger_error(str(theme_root) + str("/") + str(dir) + str(" is not readable"), E_USER_NOTICE)
                    continue
                # end if
                for sub_dir in sub_dirs:
                    if (not php_is_dir(theme_root + "/" + dir + "/" + sub_dir)) or "." == dir[0] or "CVS" == dir:
                        continue
                    # end if
                    if (not php_file_exists(theme_root + "/" + dir + "/" + sub_dir + "/style.css")):
                        continue
                    # end if
                    found_themes[dir + "/" + sub_dir] = Array({"theme_file": dir + "/" + sub_dir + "/style.css", "theme_root": theme_root})
                    found_theme = True
                # end for
                #// Never mind the above, it's just a theme missing a style.css.
                #// Return it; WP_Theme will catch the error.
                if (not found_theme):
                    found_themes[dir] = Array({"theme_file": dir + "/style.css", "theme_root": theme_root})
                # end if
            # end if
        # end for
    # end for
    asort(found_themes)
    theme_roots = Array()
    relative_theme_roots = php_array_flip(relative_theme_roots)
    for theme_dir,theme_data in found_themes:
        theme_roots[theme_dir] = relative_theme_roots[theme_data["theme_root"]]
        pass
    # end for
    if get_site_transient("theme_roots") != theme_roots:
        set_site_transient("theme_roots", theme_roots, cache_expiration)
    # end if
    return found_themes
# end def search_theme_directories
#// 
#// Retrieve path to themes directory.
#// 
#// Does not have trailing slash.
#// 
#// @since 1.5.0
#// 
#// @global array $wp_theme_directories
#// 
#// @param string $stylesheet_or_template Optional. The stylesheet or template name of the theme.
#// Default is to leverage the main theme root.
#// @return string Themes directory path.
#//
def get_theme_root(stylesheet_or_template="", *args_):
    
    global wp_theme_directories
    php_check_if_defined("wp_theme_directories")
    theme_root = ""
    if stylesheet_or_template:
        theme_root = get_raw_theme_root(stylesheet_or_template)
        if theme_root:
            #// Always prepend WP_CONTENT_DIR unless the root currently registered as a theme directory.
            #// This gives relative theme roots the benefit of the doubt when things go haywire.
            if (not php_in_array(theme_root, wp_theme_directories)):
                theme_root = WP_CONTENT_DIR + theme_root
            # end if
        # end if
    # end if
    if (not theme_root):
        theme_root = WP_CONTENT_DIR + "/themes"
    # end if
    #// 
    #// Filters the absolute path to the themes directory.
    #// 
    #// @since 1.5.0
    #// 
    #// @param string $theme_root Absolute path to themes directory.
    #//
    return apply_filters("theme_root", theme_root)
# end def get_theme_root
#// 
#// Retrieve URI for themes directory.
#// 
#// Does not have trailing slash.
#// 
#// @since 1.5.0
#// 
#// @global array $wp_theme_directories
#// 
#// @param string $stylesheet_or_template Optional. The stylesheet or template name of the theme.
#// Default is to leverage the main theme root.
#// @param string $theme_root             Optional. The theme root for which calculations will be based,
#// preventing the need for a get_raw_theme_root() call. Default empty.
#// @return string Themes directory URI.
#//
def get_theme_root_uri(stylesheet_or_template="", theme_root="", *args_):
    
    global wp_theme_directories
    php_check_if_defined("wp_theme_directories")
    if stylesheet_or_template and (not theme_root):
        theme_root = get_raw_theme_root(stylesheet_or_template)
    # end if
    if stylesheet_or_template and theme_root:
        if php_in_array(theme_root, wp_theme_directories):
            #// Absolute path. Make an educated guess. YMMV -- but note the filter below.
            if 0 == php_strpos(theme_root, WP_CONTENT_DIR):
                theme_root_uri = content_url(php_str_replace(WP_CONTENT_DIR, "", theme_root))
            elif 0 == php_strpos(theme_root, ABSPATH):
                theme_root_uri = site_url(php_str_replace(ABSPATH, "", theme_root))
            elif 0 == php_strpos(theme_root, WP_PLUGIN_DIR) or 0 == php_strpos(theme_root, WPMU_PLUGIN_DIR):
                theme_root_uri = plugins_url(php_basename(theme_root), theme_root)
            else:
                theme_root_uri = theme_root
            # end if
        else:
            theme_root_uri = content_url(theme_root)
        # end if
    else:
        theme_root_uri = content_url("themes")
    # end if
    #// 
    #// Filters the URI for themes directory.
    #// 
    #// @since 1.5.0
    #// 
    #// @param string $theme_root_uri         The URI for themes directory.
    #// @param string $siteurl                WordPress web address which is set in General Options.
    #// @param string $stylesheet_or_template The stylesheet or template name of the theme.
    #//
    return apply_filters("theme_root_uri", theme_root_uri, get_option("siteurl"), stylesheet_or_template)
# end def get_theme_root_uri
#// 
#// Get the raw theme root relative to the content directory with no filters applied.
#// 
#// @since 3.1.0
#// 
#// @global array $wp_theme_directories
#// 
#// @param string $stylesheet_or_template The stylesheet or template name of the theme.
#// @param bool   $skip_cache             Optional. Whether to skip the cache.
#// Defaults to false, meaning the cache is used.
#// @return string Theme root.
#//
def get_raw_theme_root(stylesheet_or_template=None, skip_cache=False, *args_):
    
    global wp_theme_directories
    php_check_if_defined("wp_theme_directories")
    if (not php_is_array(wp_theme_directories)) or php_count(wp_theme_directories) <= 1:
        return "/themes"
    # end if
    theme_root = False
    #// If requesting the root for the current theme, consult options to avoid calling get_theme_roots().
    if (not skip_cache):
        if get_option("stylesheet") == stylesheet_or_template:
            theme_root = get_option("stylesheet_root")
        elif get_option("template") == stylesheet_or_template:
            theme_root = get_option("template_root")
        # end if
    # end if
    if php_empty(lambda : theme_root):
        theme_roots = get_theme_roots()
        if (not php_empty(lambda : theme_roots[stylesheet_or_template])):
            theme_root = theme_roots[stylesheet_or_template]
        # end if
    # end if
    return theme_root
# end def get_raw_theme_root
#// 
#// Display localized stylesheet link element.
#// 
#// @since 2.1.0
#//
def locale_stylesheet(*args_):
    
    stylesheet = get_locale_stylesheet_uri()
    if php_empty(lambda : stylesheet):
        return
    # end if
    type_attr = "" if current_theme_supports("html5", "style") else " type=\"text/css\""
    printf("<link rel=\"stylesheet\" href=\"%s\"%s media=\"screen\" />", stylesheet, type_attr)
# end def locale_stylesheet
#// 
#// Switches the theme.
#// 
#// Accepts one argument: $stylesheet of the theme. It also accepts an additional function signature
#// of two arguments: $template then $stylesheet. This is for backward compatibility.
#// 
#// @since 2.5.0
#// 
#// @global array                $wp_theme_directories
#// @global WP_Customize_Manager $wp_customize
#// @global array                $sidebars_widgets
#// 
#// @param string $stylesheet Stylesheet name
#//
def switch_theme(stylesheet=None, *args_):
    
    global wp_theme_directories,wp_customize,sidebars_widgets
    php_check_if_defined("wp_theme_directories","wp_customize","sidebars_widgets")
    _sidebars_widgets = None
    if "wp_ajax_customize_save" == current_action():
        old_sidebars_widgets_data_setting = wp_customize.get_setting("old_sidebars_widgets_data")
        if old_sidebars_widgets_data_setting:
            _sidebars_widgets = wp_customize.post_value(old_sidebars_widgets_data_setting)
        # end if
    elif php_is_array(sidebars_widgets):
        _sidebars_widgets = sidebars_widgets
    # end if
    if php_is_array(_sidebars_widgets):
        set_theme_mod("sidebars_widgets", Array({"time": time(), "data": _sidebars_widgets}))
    # end if
    nav_menu_locations = get_theme_mod("nav_menu_locations")
    update_option("theme_switch_menu_locations", nav_menu_locations)
    if php_func_num_args() > 1:
        stylesheet = php_func_get_arg(1)
    # end if
    old_theme = wp_get_theme()
    new_theme = wp_get_theme(stylesheet)
    template = new_theme.get_template()
    if wp_is_recovery_mode():
        paused_themes = wp_paused_themes()
        paused_themes.delete(old_theme.get_stylesheet())
        paused_themes.delete(old_theme.get_template())
    # end if
    update_option("template", template)
    update_option("stylesheet", stylesheet)
    if php_count(wp_theme_directories) > 1:
        update_option("template_root", get_raw_theme_root(template, True))
        update_option("stylesheet_root", get_raw_theme_root(stylesheet, True))
    else:
        delete_option("template_root")
        delete_option("stylesheet_root")
    # end if
    new_name = new_theme.get("Name")
    update_option("current_theme", new_name)
    #// Migrate from the old mods_{name} option to theme_mods_{slug}.
    if is_admin() and False == get_option("theme_mods_" + stylesheet):
        default_theme_mods = get_option("mods_" + new_name)
        if (not php_empty(lambda : nav_menu_locations)) and php_empty(lambda : default_theme_mods["nav_menu_locations"]):
            default_theme_mods["nav_menu_locations"] = nav_menu_locations
        # end if
        add_option(str("theme_mods_") + str(stylesheet), default_theme_mods)
    else:
        #// 
        #// Since retrieve_widgets() is called when initializing a theme in the Customizer,
        #// we need to remove the theme mods to avoid overwriting changes made via
        #// the Customizer when accessing wp-admin/widgets.php.
        #//
        if "wp_ajax_customize_save" == current_action():
            remove_theme_mod("sidebars_widgets")
        # end if
    # end if
    update_option("theme_switched", old_theme.get_stylesheet())
    #// 
    #// Fires after the theme is switched.
    #// 
    #// @since 1.5.0
    #// @since 4.5.0 Introduced the `$old_theme` parameter.
    #// 
    #// @param string   $new_name  Name of the new theme.
    #// @param WP_Theme $new_theme WP_Theme instance of the new theme.
    #// @param WP_Theme $old_theme WP_Theme instance of the old theme.
    #//
    do_action("switch_theme", new_name, new_theme, old_theme)
# end def switch_theme
#// 
#// Checks that current theme files 'index.php' and 'style.css' exists.
#// 
#// Does not initially check the default theme, which is the fallback and should always exist.
#// But if it doesn't exist, it'll fall back to the latest core default theme that does exist.
#// Will switch theme to the fallback theme if current theme does not validate.
#// 
#// You can use the {@see 'validate_current_theme'} filter to return false to
#// disable this functionality.
#// 
#// @since 1.5.0
#// @see WP_DEFAULT_THEME
#// 
#// @return bool
#//
def validate_current_theme(*args_):
    
    #// 
    #// Filters whether to validate the current theme.
    #// 
    #// @since 2.7.0
    #// 
    #// @param bool $validate Whether to validate the current theme. Default true.
    #//
    if wp_installing() or (not apply_filters("validate_current_theme", True)):
        return True
    # end if
    if (not php_file_exists(get_template_directory() + "/index.php")):
        pass
    elif (not php_file_exists(get_template_directory() + "/style.css")):
        pass
    elif is_child_theme() and (not php_file_exists(get_stylesheet_directory() + "/style.css")):
        pass
    else:
        #// Valid.
        return True
    # end if
    default = wp_get_theme(WP_DEFAULT_THEME)
    if default.exists():
        switch_theme(WP_DEFAULT_THEME)
        return False
    # end if
    #// 
    #// If we're in an invalid state but WP_DEFAULT_THEME doesn't exist,
    #// switch to the latest core default theme that's installed.
    #// If it turns out that this latest core default theme is our current
    #// theme, then there's nothing we can do about that, so we have to bail,
    #// rather than going into an infinite loop. (This is why there are
    #// checks against WP_DEFAULT_THEME above, also.) We also can't do anything
    #// if it turns out there is no default theme installed. (That's `false`.)
    #//
    default = WP_Theme.get_core_default_theme()
    if False == default or get_stylesheet() == default.get_stylesheet():
        return True
    # end if
    switch_theme(default.get_stylesheet())
    return False
# end def validate_current_theme
#// 
#// Retrieve all theme modifications.
#// 
#// @since 3.1.0
#// 
#// @return array|void Theme modifications.
#//
def get_theme_mods(*args_):
    
    theme_slug = get_option("stylesheet")
    mods = get_option(str("theme_mods_") + str(theme_slug))
    if False == mods:
        theme_name = get_option("current_theme")
        if False == theme_name:
            theme_name = wp_get_theme().get("Name")
        # end if
        mods = get_option(str("mods_") + str(theme_name))
        #// Deprecated location.
        if is_admin() and False != mods:
            update_option(str("theme_mods_") + str(theme_slug), mods)
            delete_option(str("mods_") + str(theme_name))
        # end if
    # end if
    return mods
# end def get_theme_mods
#// 
#// Retrieve theme modification value for the current theme.
#// 
#// If the modification name does not exist, then the $default will be passed
#// through {@link https://www.php.net/sprintf sprintf()} PHP function with
#// the template directory URI as the first string and the stylesheet directory URI
#// as the second string.
#// 
#// @since 2.1.0
#// 
#// @param string       $name    Theme modification name.
#// @param string|false $default Optional. Theme modification default value. Default false.
#// @return mixed Theme modification value.
#//
def get_theme_mod(name=None, default=False, *args_):
    
    mods = get_theme_mods()
    if (php_isset(lambda : mods[name])):
        #// 
        #// Filters the theme modification, or 'theme_mod', value.
        #// 
        #// The dynamic portion of the hook name, `$name`, refers to the key name
        #// of the modification array. For example, 'header_textcolor', 'header_image',
        #// and so on depending on the theme options.
        #// 
        #// @since 2.2.0
        #// 
        #// @param string $current_mod The value of the current theme modification.
        #//
        return apply_filters(str("theme_mod_") + str(name), mods[name])
    # end if
    if php_is_string(default):
        #// Only run the replacement if an sprintf() string format pattern was found.
        if php_preg_match("#(?<!%)%(?:\\d+\\$?)?s#", default):
            default = php_sprintf(default, get_template_directory_uri(), get_stylesheet_directory_uri())
        # end if
    # end if
    #// This filter is documented in wp-includes/theme.php
    return apply_filters(str("theme_mod_") + str(name), default)
# end def get_theme_mod
#// 
#// Update theme modification value for the current theme.
#// 
#// @since 2.1.0
#// 
#// @param string $name  Theme modification name.
#// @param mixed  $value Theme modification value.
#//
def set_theme_mod(name=None, value=None, *args_):
    
    mods = get_theme_mods()
    old_value = mods[name] if (php_isset(lambda : mods[name])) else False
    #// 
    #// Filters the theme modification, or 'theme_mod', value on save.
    #// 
    #// The dynamic portion of the hook name, `$name`, refers to the key name
    #// of the modification array. For example, 'header_textcolor', 'header_image',
    #// and so on depending on the theme options.
    #// 
    #// @since 3.9.0
    #// 
    #// @param string $value     The new value of the theme modification.
    #// @param string $old_value The current value of the theme modification.
    #//
    mods[name] = apply_filters(str("pre_set_theme_mod_") + str(name), value, old_value)
    theme = get_option("stylesheet")
    update_option(str("theme_mods_") + str(theme), mods)
# end def set_theme_mod
#// 
#// Remove theme modification name from current theme list.
#// 
#// If removing the name also removes all elements, then the entire option will
#// be removed.
#// 
#// @since 2.1.0
#// 
#// @param string $name Theme modification name.
#//
def remove_theme_mod(name=None, *args_):
    
    mods = get_theme_mods()
    if (not (php_isset(lambda : mods[name]))):
        return
    # end if
    mods[name] = None
    if php_empty(lambda : mods):
        remove_theme_mods()
        return
    # end if
    theme = get_option("stylesheet")
    update_option(str("theme_mods_") + str(theme), mods)
# end def remove_theme_mod
#// 
#// Remove theme modifications option for current theme.
#// 
#// @since 2.1.0
#//
def remove_theme_mods(*args_):
    
    delete_option("theme_mods_" + get_option("stylesheet"))
    #// Old style.
    theme_name = get_option("current_theme")
    if False == theme_name:
        theme_name = wp_get_theme().get("Name")
    # end if
    delete_option("mods_" + theme_name)
# end def remove_theme_mods
#// 
#// Retrieves the custom header text color in 3- or 6-digit hexadecimal form.
#// 
#// @since 2.1.0
#// 
#// @return string Header text color in 3- or 6-digit hexadecimal form (minus the hash symbol).
#//
def get_header_textcolor(*args_):
    
    return get_theme_mod("header_textcolor", get_theme_support("custom-header", "default-text-color"))
# end def get_header_textcolor
#// 
#// Displays the custom header text color in 3- or 6-digit hexadecimal form (minus the hash symbol).
#// 
#// @since 2.1.0
#//
def header_textcolor(*args_):
    
    php_print(get_header_textcolor())
# end def header_textcolor
#// 
#// Whether to display the header text.
#// 
#// @since 3.4.0
#// 
#// @return bool
#//
def display_header_text(*args_):
    
    if (not current_theme_supports("custom-header", "header-text")):
        return False
    # end if
    text_color = get_theme_mod("header_textcolor", get_theme_support("custom-header", "default-text-color"))
    return "blank" != text_color
# end def display_header_text
#// 
#// Check whether a header image is set or not.
#// 
#// @since 4.2.0
#// 
#// @see get_header_image()
#// 
#// @return bool Whether a header image is set or not.
#//
def has_header_image(*args_):
    
    return bool(get_header_image())
# end def has_header_image
#// 
#// Retrieve header image for custom header.
#// 
#// @since 2.1.0
#// 
#// @return string|false
#//
def get_header_image(*args_):
    
    url = get_theme_mod("header_image", get_theme_support("custom-header", "default-image"))
    if "remove-header" == url:
        return False
    # end if
    if is_random_header_image():
        url = get_random_header_image()
    # end if
    return esc_url_raw(set_url_scheme(url))
# end def get_header_image
#// 
#// Create image tag markup for a custom header image.
#// 
#// @since 4.4.0
#// 
#// @param array $attr Optional. Additional attributes for the image tag. Can be used
#// to override the default attributes. Default empty.
#// @return string HTML image element markup or empty string on failure.
#//
def get_header_image_tag(attr=Array(), *args_):
    
    header = get_custom_header()
    header.url = get_header_image()
    if (not header.url):
        return ""
    # end if
    width = absint(header.width)
    height = absint(header.height)
    attr = wp_parse_args(attr, Array({"src": header.url, "width": width, "height": height, "alt": get_bloginfo("name")}))
    #// Generate 'srcset' and 'sizes' if not already present.
    if php_empty(lambda : attr["srcset"]) and (not php_empty(lambda : header.attachment_id)):
        image_meta = get_post_meta(header.attachment_id, "_wp_attachment_metadata", True)
        size_array = Array(width, height)
        if php_is_array(image_meta):
            srcset = wp_calculate_image_srcset(size_array, header.url, image_meta, header.attachment_id)
            sizes = attr["sizes"] if (not php_empty(lambda : attr["sizes"])) else wp_calculate_image_sizes(size_array, header.url, image_meta, header.attachment_id)
            if srcset and sizes:
                attr["srcset"] = srcset
                attr["sizes"] = sizes
            # end if
        # end if
    # end if
    attr = php_array_map("esc_attr", attr)
    html = "<img"
    for name,value in attr:
        html += " " + name + "=\"" + value + "\""
    # end for
    html += " />"
    #// 
    #// Filters the markup of header images.
    #// 
    #// @since 4.4.0
    #// 
    #// @param string $html   The HTML image tag markup being filtered.
    #// @param object $header The custom header object returned by 'get_custom_header()'.
    #// @param array  $attr   Array of the attributes for the image tag.
    #//
    return apply_filters("get_header_image_tag", html, header, attr)
# end def get_header_image_tag
#// 
#// Display the image markup for a custom header image.
#// 
#// @since 4.4.0
#// 
#// @param array $attr Optional. Attributes for the image markup. Default empty.
#//
def the_header_image_tag(attr=Array(), *args_):
    
    php_print(get_header_image_tag(attr))
# end def the_header_image_tag
#// 
#// Get random header image data from registered images in theme.
#// 
#// @since 3.4.0
#// 
#// @access private
#// 
#// @global array  $_wp_default_headers
#// @staticvar object $_wp_random_header
#// 
#// @return object
#//
def _get_random_header_data(*args_):
    
    _wp_random_header = None
    if php_empty(lambda : _wp_random_header):
        global _wp_default_headers
        php_check_if_defined("_wp_default_headers")
        header_image_mod = get_theme_mod("header_image", "")
        headers = Array()
        if "random-uploaded-image" == header_image_mod:
            headers = get_uploaded_header_images()
        elif (not php_empty(lambda : _wp_default_headers)):
            if "random-default-image" == header_image_mod:
                headers = _wp_default_headers
            else:
                if current_theme_supports("custom-header", "random-default"):
                    headers = _wp_default_headers
                # end if
            # end if
        # end if
        if php_empty(lambda : headers):
            return php_new_class("stdClass", lambda : stdClass())
        # end if
        _wp_random_header = headers[php_array_rand(headers)]
        _wp_random_header.url = php_sprintf(_wp_random_header.url, get_template_directory_uri(), get_stylesheet_directory_uri())
        _wp_random_header.thumbnail_url = php_sprintf(_wp_random_header.thumbnail_url, get_template_directory_uri(), get_stylesheet_directory_uri())
    # end if
    return _wp_random_header
# end def _get_random_header_data
#// 
#// Get random header image url from registered images in theme.
#// 
#// @since 3.2.0
#// 
#// @return string Path to header image
#//
def get_random_header_image(*args_):
    
    random_image = _get_random_header_data()
    if php_empty(lambda : random_image.url):
        return ""
    # end if
    return random_image.url
# end def get_random_header_image
#// 
#// Check if random header image is in use.
#// 
#// Always true if user expressly chooses the option in Appearance > Header.
#// Also true if theme has multiple header images registered, no specific header image
#// is chosen, and theme turns on random headers with add_theme_support().
#// 
#// @since 3.2.0
#// 
#// @param string $type The random pool to use. any|default|uploaded
#// @return bool
#//
def is_random_header_image(type="any", *args_):
    
    header_image_mod = get_theme_mod("header_image", get_theme_support("custom-header", "default-image"))
    if "any" == type:
        if "random-default-image" == header_image_mod or "random-uploaded-image" == header_image_mod or "" != get_random_header_image() and php_empty(lambda : header_image_mod):
            return True
        # end if
    else:
        if str("random-") + str(type) + str("-image") == header_image_mod:
            return True
        elif "default" == type and php_empty(lambda : header_image_mod) and "" != get_random_header_image():
            return True
        # end if
    # end if
    return False
# end def is_random_header_image
#// 
#// Display header image URL.
#// 
#// @since 2.1.0
#//
def header_image(*args_):
    
    image = get_header_image()
    if image:
        php_print(esc_url(image))
    # end if
# end def header_image
#// 
#// Get the header images uploaded for the current theme.
#// 
#// @since 3.2.0
#// 
#// @return array
#//
def get_uploaded_header_images(*args_):
    
    header_images = Array()
    #// @todo Caching.
    headers = get_posts(Array({"post_type": "attachment", "meta_key": "_wp_attachment_is_custom_header", "meta_value": get_option("stylesheet"), "orderby": "none", "nopaging": True}))
    if php_empty(lambda : headers):
        return Array()
    # end if
    for header in headers:
        url = esc_url_raw(wp_get_attachment_url(header.ID))
        header_data = wp_get_attachment_metadata(header.ID)
        header_index = header.ID
        header_images[header_index] = Array()
        header_images[header_index]["attachment_id"] = header.ID
        header_images[header_index]["url"] = url
        header_images[header_index]["thumbnail_url"] = url
        header_images[header_index]["alt_text"] = get_post_meta(header.ID, "_wp_attachment_image_alt", True)
        header_images[header_index]["attachment_parent"] = header_data["attachment_parent"] if (php_isset(lambda : header_data["attachment_parent"])) else ""
        if (php_isset(lambda : header_data["width"])):
            header_images[header_index]["width"] = header_data["width"]
        # end if
        if (php_isset(lambda : header_data["height"])):
            header_images[header_index]["height"] = header_data["height"]
        # end if
    # end for
    return header_images
# end def get_uploaded_header_images
#// 
#// Get the header image data.
#// 
#// @since 3.4.0
#// 
#// @global array $_wp_default_headers
#// 
#// @return object
#//
def get_custom_header(*args_):
    
    global _wp_default_headers
    php_check_if_defined("_wp_default_headers")
    if is_random_header_image():
        data = _get_random_header_data()
    else:
        data = get_theme_mod("header_image_data")
        if (not data) and current_theme_supports("custom-header", "default-image"):
            directory_args = Array(get_template_directory_uri(), get_stylesheet_directory_uri())
            data = Array()
            data["url"] = vsprintf(get_theme_support("custom-header", "default-image"), directory_args)
            data["thumbnail_url"] = data["url"]
            if (not php_empty(lambda : _wp_default_headers)):
                for default_header in _wp_default_headers:
                    url = vsprintf(default_header["url"], directory_args)
                    if data["url"] == url:
                        data = default_header
                        data["url"] = url
                        data["thumbnail_url"] = vsprintf(data["thumbnail_url"], directory_args)
                        break
                    # end if
                # end for
            # end if
        # end if
    # end if
    default = Array({"url": "", "thumbnail_url": "", "width": get_theme_support("custom-header", "width"), "height": get_theme_support("custom-header", "height"), "video": get_theme_support("custom-header", "video")})
    return wp_parse_args(data, default)
# end def get_custom_header
#// 
#// Register a selection of default headers to be displayed by the custom header admin UI.
#// 
#// @since 3.0.0
#// 
#// @global array $_wp_default_headers
#// 
#// @param array $headers Array of headers keyed by a string id. The ids point to arrays containing 'url', 'thumbnail_url', and 'description' keys.
#//
def register_default_headers(headers=None, *args_):
    
    global _wp_default_headers
    php_check_if_defined("_wp_default_headers")
    _wp_default_headers = php_array_merge(_wp_default_headers, headers)
# end def register_default_headers
#// 
#// Unregister default headers.
#// 
#// This function must be called after register_default_headers() has already added the
#// header you want to remove.
#// 
#// @see register_default_headers()
#// @since 3.0.0
#// 
#// @global array $_wp_default_headers
#// 
#// @param string|array $header The header string id (key of array) to remove, or an array thereof.
#// @return bool|void A single header returns true on success, false on failure.
#// There is currently no return value for multiple headers.
#//
def unregister_default_headers(header=None, *args_):
    
    global _wp_default_headers
    php_check_if_defined("_wp_default_headers")
    if php_is_array(header):
        php_array_map("unregister_default_headers", header)
    elif (php_isset(lambda : _wp_default_headers[header])):
        _wp_default_headers[header] = None
        return True
    else:
        return False
    # end if
# end def unregister_default_headers
#// 
#// Check whether a header video is set or not.
#// 
#// @since 4.7.0
#// 
#// @see get_header_video_url()
#// 
#// @return bool Whether a header video is set or not.
#//
def has_header_video(*args_):
    
    return bool(get_header_video_url())
# end def has_header_video
#// 
#// Retrieve header video URL for custom header.
#// 
#// Uses a local video if present, or falls back to an external video.
#// 
#// @since 4.7.0
#// 
#// @return string|false Header video URL or false if there is no video.
#//
def get_header_video_url(*args_):
    
    id = absint(get_theme_mod("header_video"))
    if id:
        #// Get the file URL from the attachment ID.
        url = wp_get_attachment_url(id)
    else:
        url = get_theme_mod("external_header_video")
    # end if
    #// 
    #// Filters the header video URL.
    #// 
    #// @since 4.7.3
    #// 
    #// @param string $url Header video URL, if available.
    #//
    url = apply_filters("get_header_video_url", url)
    if (not id) and (not url):
        return False
    # end if
    return esc_url_raw(set_url_scheme(url))
# end def get_header_video_url
#// 
#// Display header video URL.
#// 
#// @since 4.7.0
#//
def the_header_video_url(*args_):
    
    video = get_header_video_url()
    if video:
        php_print(esc_url(video))
    # end if
# end def the_header_video_url
#// 
#// Retrieve header video settings.
#// 
#// @since 4.7.0
#// 
#// @return array
#//
def get_header_video_settings(*args_):
    
    header = get_custom_header()
    video_url = get_header_video_url()
    video_type = wp_check_filetype(video_url, wp_get_mime_types())
    settings = Array({"mimeType": "", "posterUrl": get_header_image(), "videoUrl": video_url, "width": absint(header.width), "height": absint(header.height), "minWidth": 900, "minHeight": 500, "l10n": Array({"pause": __("Pause"), "play": __("Play"), "pauseSpeak": __("Video is paused."), "playSpeak": __("Video is playing.")})})
    if php_preg_match("#^https?://(?:www\\.)?(?:youtube\\.com/watch|youtu\\.be/)#", video_url):
        settings["mimeType"] = "video/x-youtube"
    elif (not php_empty(lambda : video_type["type"])):
        settings["mimeType"] = video_type["type"]
    # end if
    #// 
    #// Filters header video settings.
    #// 
    #// @since 4.7.0
    #// 
    #// @param array $settings An array of header video settings.
    #//
    return apply_filters("header_video_settings", settings)
# end def get_header_video_settings
#// 
#// Check whether a custom header is set or not.
#// 
#// @since 4.7.0
#// 
#// @return bool True if a custom header is set. False if not.
#//
def has_custom_header(*args_):
    
    if has_header_image() or has_header_video() and is_header_video_active():
        return True
    # end if
    return False
# end def has_custom_header
#// 
#// Checks whether the custom header video is eligible to show on the current page.
#// 
#// @since 4.7.0
#// 
#// @return bool True if the custom header video should be shown. False if not.
#//
def is_header_video_active(*args_):
    
    if (not get_theme_support("custom-header", "video")):
        return False
    # end if
    video_active_cb = get_theme_support("custom-header", "video-active-callback")
    if php_empty(lambda : video_active_cb) or (not php_is_callable(video_active_cb)):
        show_video = True
    else:
        show_video = php_call_user_func(video_active_cb)
    # end if
    #// 
    #// Modify whether the custom header video is eligible to show on the current page.
    #// 
    #// @since 4.7.0
    #// 
    #// @param bool $show_video Whether the custom header video should be shown. Returns the value
    #// of the theme setting for the `custom-header`'s `video-active-callback`.
    #// If no callback is set, the default value is that of `is_front_page()`.
    #//
    return apply_filters("is_header_video_active", show_video)
# end def is_header_video_active
#// 
#// Retrieve the markup for a custom header.
#// 
#// The container div will always be returned in the Customizer preview.
#// 
#// @since 4.7.0
#// 
#// @return string The markup for a custom header on success.
#//
def get_custom_header_markup(*args_):
    
    if (not has_custom_header()) and (not is_customize_preview()):
        return ""
    # end if
    return php_sprintf("<div id=\"wp-custom-header\" class=\"wp-custom-header\">%s</div>", get_header_image_tag())
# end def get_custom_header_markup
#// 
#// Print the markup for a custom header.
#// 
#// A container div will always be printed in the Customizer preview.
#// 
#// @since 4.7.0
#//
def the_custom_header_markup(*args_):
    
    custom_header = get_custom_header_markup()
    if php_empty(lambda : custom_header):
        return
    # end if
    php_print(custom_header)
    if is_header_video_active() and has_header_video() or is_customize_preview():
        wp_enqueue_script("wp-custom-header")
        wp_localize_script("wp-custom-header", "_wpCustomHeaderSettings", get_header_video_settings())
    # end if
# end def the_custom_header_markup
#// 
#// Retrieve background image for custom background.
#// 
#// @since 3.0.0
#// 
#// @return string
#//
def get_background_image(*args_):
    
    return get_theme_mod("background_image", get_theme_support("custom-background", "default-image"))
# end def get_background_image
#// 
#// Display background image path.
#// 
#// @since 3.0.0
#//
def background_image(*args_):
    
    php_print(get_background_image())
# end def background_image
#// 
#// Retrieve value for custom background color.
#// 
#// @since 3.0.0
#// 
#// @return string
#//
def get_background_color(*args_):
    
    return get_theme_mod("background_color", get_theme_support("custom-background", "default-color"))
# end def get_background_color
#// 
#// Display background color value.
#// 
#// @since 3.0.0
#//
def background_color(*args_):
    
    php_print(get_background_color())
# end def background_color
#// 
#// Default custom background callback.
#// 
#// @since 3.0.0
#//
def _custom_background_cb(*args_):
    
    #// $background is the saved custom image, or the default image.
    background = set_url_scheme(get_background_image())
    #// $color is the saved custom color.
    #// A default has to be specified in style.css. It will not be printed here.
    color = get_background_color()
    if get_theme_support("custom-background", "default-color") == color:
        color = False
    # end if
    type_attr = "" if current_theme_supports("html5", "style") else " type=\"text/css\""
    if (not background) and (not color):
        if is_customize_preview():
            printf("<style%s id=\"custom-background-css\"></style>", type_attr)
        # end if
        return
    # end if
    style = str("background-color: #") + str(color) + str(";") if color else ""
    if background:
        image = " background-image: url(\"" + esc_url_raw(background) + "\");"
        #// Background Position.
        position_x = get_theme_mod("background_position_x", get_theme_support("custom-background", "default-position-x"))
        position_y = get_theme_mod("background_position_y", get_theme_support("custom-background", "default-position-y"))
        if (not php_in_array(position_x, Array("left", "center", "right"), True)):
            position_x = "left"
        # end if
        if (not php_in_array(position_y, Array("top", "center", "bottom"), True)):
            position_y = "top"
        # end if
        position = str(" background-position: ") + str(position_x) + str(" ") + str(position_y) + str(";")
        #// Background Size.
        size = get_theme_mod("background_size", get_theme_support("custom-background", "default-size"))
        if (not php_in_array(size, Array("auto", "contain", "cover"), True)):
            size = "auto"
        # end if
        size = str(" background-size: ") + str(size) + str(";")
        #// Background Repeat.
        repeat = get_theme_mod("background_repeat", get_theme_support("custom-background", "default-repeat"))
        if (not php_in_array(repeat, Array("repeat-x", "repeat-y", "repeat", "no-repeat"), True)):
            repeat = "repeat"
        # end if
        repeat = str(" background-repeat: ") + str(repeat) + str(";")
        #// Background Scroll.
        attachment = get_theme_mod("background_attachment", get_theme_support("custom-background", "default-attachment"))
        if "fixed" != attachment:
            attachment = "scroll"
        # end if
        attachment = str(" background-attachment: ") + str(attachment) + str(";")
        style += image + position + size + repeat + attachment
    # end if
    php_print("<style")
    php_print(type_attr)
    php_print(" id=\"custom-background-css\">\nbody.custom-background { ")
    php_print(php_trim(style))
    php_print(" }\n</style>\n   ")
# end def _custom_background_cb
#// 
#// Render the Custom CSS style element.
#// 
#// @since 4.7.0
#//
def wp_custom_css_cb(*args_):
    
    styles = wp_get_custom_css()
    if styles or is_customize_preview():
        type_attr = "" if current_theme_supports("html5", "style") else " type=\"text/css\""
        php_print("     <style")
        php_print(type_attr)
        php_print(" id=\"wp-custom-css\">\n         ")
        php_print(strip_tags(styles))
        pass
        php_print("     </style>\n      ")
    # end if
# end def wp_custom_css_cb
#// 
#// Fetch the `custom_css` post for a given theme.
#// 
#// @since 4.7.0
#// 
#// @param string $stylesheet Optional. A theme object stylesheet name. Defaults to the current theme.
#// @return WP_Post|null The custom_css post or null if none exists.
#//
def wp_get_custom_css_post(stylesheet="", *args_):
    
    if php_empty(lambda : stylesheet):
        stylesheet = get_stylesheet()
    # end if
    custom_css_query_vars = Array({"post_type": "custom_css", "post_status": get_post_stati(), "name": sanitize_title(stylesheet), "posts_per_page": 1, "no_found_rows": True, "cache_results": True, "update_post_meta_cache": False, "update_post_term_cache": False, "lazy_load_term_meta": False})
    post = None
    if get_stylesheet() == stylesheet:
        post_id = get_theme_mod("custom_css_post_id")
        if post_id > 0 and get_post(post_id):
            post = get_post(post_id)
        # end if
        #// `-1` indicates no post exists; no query necessary.
        if (not post) and -1 != post_id:
            query = php_new_class("WP_Query", lambda : WP_Query(custom_css_query_vars))
            post = query.post
            #// 
            #// Cache the lookup. See wp_update_custom_css_post().
            #// @todo This should get cleared if a custom_css post is added/removed.
            #//
            set_theme_mod("custom_css_post_id", post.ID if post else -1)
        # end if
    else:
        query = php_new_class("WP_Query", lambda : WP_Query(custom_css_query_vars))
        post = query.post
    # end if
    return post
# end def wp_get_custom_css_post
#// 
#// Fetch the saved Custom CSS content for rendering.
#// 
#// @since 4.7.0
#// 
#// @param string $stylesheet Optional. A theme object stylesheet name. Defaults to the current theme.
#// @return string The Custom CSS Post content.
#//
def wp_get_custom_css(stylesheet="", *args_):
    
    css = ""
    if php_empty(lambda : stylesheet):
        stylesheet = get_stylesheet()
    # end if
    post = wp_get_custom_css_post(stylesheet)
    if post:
        css = post.post_content
    # end if
    #// 
    #// Filters the Custom CSS Output into the <head>.
    #// 
    #// @since 4.7.0
    #// 
    #// @param string $css        CSS pulled in from the Custom CSS CPT.
    #// @param string $stylesheet The theme stylesheet name.
    #//
    css = apply_filters("wp_get_custom_css", css, stylesheet)
    return css
# end def wp_get_custom_css
#// 
#// Update the `custom_css` post for a given theme.
#// 
#// Inserts a `custom_css` post when one doesn't yet exist.
#// 
#// @since 4.7.0
#// 
#// @param string $css CSS, stored in `post_content`.
#// @param array  $args {
#// Args.
#// 
#// @type string $preprocessed Pre-processed CSS, stored in `post_content_filtered`. Normally empty string. Optional.
#// @type string $stylesheet   Stylesheet (child theme) to update. Optional, defaults to current theme/stylesheet.
#// }
#// @return WP_Post|WP_Error Post on success, error on failure.
#//
def wp_update_custom_css_post(css=None, args=Array(), *args_):
    
    args = wp_parse_args(args, Array({"preprocessed": "", "stylesheet": get_stylesheet()}))
    data = Array({"css": css, "preprocessed": args["preprocessed"]})
    #// 
    #// Filters the `css` (`post_content`) and `preprocessed` (`post_content_filtered`) args for a `custom_css` post being updated.
    #// 
    #// This filter can be used by plugin that offer CSS pre-processors, to store the original
    #// pre-processed CSS in `post_content_filtered` and then store processed CSS in `post_content`.
    #// When used in this way, the `post_content_filtered` should be supplied as the setting value
    #// instead of `post_content` via a the `customize_value_custom_css` filter, for example:
    #// 
    #// <code>
    #// add_filter( 'customize_value_custom_css', function( $value, $setting ) {
    #// $post = wp_get_custom_css_post( $setting->stylesheet );
    #// if ( $post && ! empty( $post->post_content_filtered ) ) {
    #// $css = $post->post_content_filtered;
    #// }
    #// return $css;
    #// }, 10, 2 );
    #// </code>
    #// 
    #// @since 4.7.0
    #// @param array $data {
    #// Custom CSS data.
    #// 
    #// @type string $css          CSS stored in `post_content`.
    #// @type string $preprocessed Pre-processed CSS stored in `post_content_filtered`. Normally empty string.
    #// }
    #// @param array $args {
    #// The args passed into `wp_update_custom_css_post()` merged with defaults.
    #// 
    #// @type string $css          The original CSS passed in to be updated.
    #// @type string $preprocessed The original preprocessed CSS passed in to be updated.
    #// @type string $stylesheet   The stylesheet (theme) being updated.
    #// }
    #//
    data = apply_filters("update_custom_css_data", data, php_array_merge(args, compact("css")))
    post_data = Array({"post_title": args["stylesheet"], "post_name": sanitize_title(args["stylesheet"]), "post_type": "custom_css", "post_status": "publish", "post_content": data["css"], "post_content_filtered": data["preprocessed"]})
    #// Update post if it already exists, otherwise create a new one.
    post = wp_get_custom_css_post(args["stylesheet"])
    if post:
        post_data["ID"] = post.ID
        r = wp_update_post(wp_slash(post_data), True)
    else:
        r = wp_insert_post(wp_slash(post_data), True)
        if (not is_wp_error(r)):
            if get_stylesheet() == args["stylesheet"]:
                set_theme_mod("custom_css_post_id", r)
            # end if
            #// Trigger creation of a revision. This should be removed once #30854 is resolved.
            if 0 == php_count(wp_get_post_revisions(r)):
                wp_save_post_revision(r)
            # end if
        # end if
    # end if
    if is_wp_error(r):
        return r
    # end if
    return get_post(r)
# end def wp_update_custom_css_post
#// 
#// Add callback for custom TinyMCE editor stylesheets.
#// 
#// The parameter $stylesheet is the name of the stylesheet, relative to
#// the theme root. It also accepts an array of stylesheets.
#// It is optional and defaults to 'editor-style.css'.
#// 
#// This function automatically adds another stylesheet with -rtl prefix, e.g. editor-style-rtl.css.
#// If that file doesn't exist, it is removed before adding the stylesheet(s) to TinyMCE.
#// If an array of stylesheets is passed to add_editor_style(),
#// RTL is only added for the first stylesheet.
#// 
#// Since version 3.4 the TinyMCE body has .rtl CSS class.
#// It is a better option to use that class and add any RTL styles to the main stylesheet.
#// 
#// @since 3.0.0
#// 
#// @global array $editor_styles
#// 
#// @param array|string $stylesheet Optional. Stylesheet name or array thereof, relative to theme root.
#// Defaults to 'editor-style.css'
#//
def add_editor_style(stylesheet="editor-style.css", *args_):
    
    global editor_styles
    php_check_if_defined("editor_styles")
    add_theme_support("editor-style")
    editor_styles = editor_styles
    stylesheet = stylesheet
    if is_rtl():
        rtl_stylesheet = php_str_replace(".css", "-rtl.css", stylesheet[0])
        stylesheet[-1] = rtl_stylesheet
    # end if
    editor_styles = php_array_merge(editor_styles, stylesheet)
# end def add_editor_style
#// 
#// Removes all visual editor stylesheets.
#// 
#// @since 3.1.0
#// 
#// @global array $editor_styles
#// 
#// @return bool True on success, false if there were no stylesheets to remove.
#//
def remove_editor_styles(*args_):
    global PHP_GLOBALS
    if (not current_theme_supports("editor-style")):
        return False
    # end if
    _remove_theme_support("editor-style")
    if is_admin():
        PHP_GLOBALS["editor_styles"] = Array()
    # end if
    return True
# end def remove_editor_styles
#// 
#// Retrieve any registered editor stylesheet URLs.
#// 
#// @since 4.0.0
#// 
#// @global array $editor_styles Registered editor stylesheets
#// 
#// @return string[] If registered, a list of editor stylesheet URLs.
#//
def get_editor_stylesheets(*args_):
    
    stylesheets = Array()
    #// Load editor_style.css if the current theme supports it.
    if (not php_empty(lambda : PHP_GLOBALS["editor_styles"])) and php_is_array(PHP_GLOBALS["editor_styles"]):
        editor_styles = PHP_GLOBALS["editor_styles"]
        editor_styles = array_unique(php_array_filter(editor_styles))
        style_uri = get_stylesheet_directory_uri()
        style_dir = get_stylesheet_directory()
        #// Support externally referenced styles (like, say, fonts).
        for key,file in editor_styles:
            if php_preg_match("~^(https?:)?//~", file):
                stylesheets[-1] = esc_url_raw(file)
                editor_styles[key] = None
            # end if
        # end for
        #// Look in a parent theme first, that way child theme CSS overrides.
        if is_child_theme():
            template_uri = get_template_directory_uri()
            template_dir = get_template_directory()
            for key,file in editor_styles:
                if file and php_file_exists(str(template_dir) + str("/") + str(file)):
                    stylesheets[-1] = str(template_uri) + str("/") + str(file)
                # end if
            # end for
        # end if
        for file in editor_styles:
            if file and php_file_exists(str(style_dir) + str("/") + str(file)):
                stylesheets[-1] = str(style_uri) + str("/") + str(file)
            # end if
        # end for
    # end if
    #// 
    #// Filters the array of URLs of stylesheets applied to the editor.
    #// 
    #// @since 4.3.0
    #// 
    #// @param string[] $stylesheets Array of URLs of stylesheets to be applied to the editor.
    #//
    return apply_filters("editor_stylesheets", stylesheets)
# end def get_editor_stylesheets
#// 
#// Expand a theme's starter content configuration using core-provided data.
#// 
#// @since 4.7.0
#// 
#// @return array Array of starter content.
#//
def get_theme_starter_content(*args_):
    
    theme_support = get_theme_support("starter-content")
    if php_is_array(theme_support) and (not php_empty(lambda : theme_support[0])) and php_is_array(theme_support[0]):
        config = theme_support[0]
    else:
        config = Array()
    # end if
    core_content = Array({"widgets": Array({"text_business_info": Array("text", Array({"title": _x("Find Us", "Theme starter content"), "text": join("", Array("<strong>" + _x("Address", "Theme starter content") + "</strong>\n", _x("123 Main Street", "Theme starter content") + "\n" + _x("New York, NY 10001", "Theme starter content") + "\n\n", "<strong>" + _x("Hours", "Theme starter content") + "</strong>\n", _x("Monday&ndash;Friday: 9:00AM&ndash;5:00PM", "Theme starter content") + "\n" + _x("Saturday &amp; Sunday: 11:00AM&ndash;3:00PM", "Theme starter content"))), "filter": True, "visual": True}))}, {"text_about": Array("text", Array({"title": _x("About This Site", "Theme starter content"), "text": _x("This may be a good place to introduce yourself and your site or include some credits.", "Theme starter content"), "filter": True, "visual": True}))}, {"archives": Array("archives", Array({"title": _x("Archives", "Theme starter content")}))}, {"calendar": Array("calendar", Array({"title": _x("Calendar", "Theme starter content")}))}, {"categories": Array("categories", Array({"title": _x("Categories", "Theme starter content")}))}, {"meta": Array("meta", Array({"title": _x("Meta", "Theme starter content")}))}, {"recent-comments": Array("recent-comments", Array({"title": _x("Recent Comments", "Theme starter content")}))}, {"recent-posts": Array("recent-posts", Array({"title": _x("Recent Posts", "Theme starter content")}))}, {"search": Array("search", Array({"title": _x("Search", "Theme starter content")}))})}, {"nav_menus": Array({"link_home": Array({"type": "custom", "title": _x("Home", "Theme starter content"), "url": home_url("/")})}, {"page_home": Array({"type": "post_type", "object": "page", "object_id": "{{home}}"})}, {"page_about": Array({"type": "post_type", "object": "page", "object_id": "{{about}}"})}, {"page_blog": Array({"type": "post_type", "object": "page", "object_id": "{{blog}}"})}, {"page_news": Array({"type": "post_type", "object": "page", "object_id": "{{news}}"})}, {"page_contact": Array({"type": "post_type", "object": "page", "object_id": "{{contact}}"})}, {"link_email": Array({"title": _x("Email", "Theme starter content"), "url": "mailto:wordpress@example.com"})}, {"link_facebook": Array({"title": _x("Facebook", "Theme starter content"), "url": "https://www.facebook.com/wordpress"})}, {"link_foursquare": Array({"title": _x("Foursquare", "Theme starter content"), "url": "https://foursquare.com/"})}, {"link_github": Array({"title": _x("GitHub", "Theme starter content"), "url": "https://github.com/wordpress/"})}, {"link_instagram": Array({"title": _x("Instagram", "Theme starter content"), "url": "https://www.instagram.com/explore/tags/wordcamp/"})}, {"link_linkedin": Array({"title": _x("LinkedIn", "Theme starter content"), "url": "https://www.linkedin.com/company/1089783"})}, {"link_pinterest": Array({"title": _x("Pinterest", "Theme starter content"), "url": "https://www.pinterest.com/"})}, {"link_twitter": Array({"title": _x("Twitter", "Theme starter content"), "url": "https://twitter.com/wordpress"})}, {"link_yelp": Array({"title": _x("Yelp", "Theme starter content"), "url": "https://www.yelp.com"})}, {"link_youtube": Array({"title": _x("YouTube", "Theme starter content"), "url": "https://www.youtube.com/channel/UCdof4Ju7amm1chz1gi1T2ZA"})})}, {"posts": Array({"home": Array({"post_type": "page", "post_title": _x("Home", "Theme starter content"), "post_content": php_sprintf("<!-- wp:paragraph -->\n<p>%s</p>\n<!-- /wp:paragraph -->", _x("Welcome to your site! This is your homepage, which is what most visitors will see when they come to your site for the first time.", "Theme starter content"))})}, {"about": Array({"post_type": "page", "post_title": _x("About", "Theme starter content"), "post_content": php_sprintf("<!-- wp:paragraph -->\n<p>%s</p>\n<!-- /wp:paragraph -->", _x("You might be an artist who would like to introduce yourself and your work here or maybe you&rsquo;re a business with a mission to describe.", "Theme starter content"))})}, {"contact": Array({"post_type": "page", "post_title": _x("Contact", "Theme starter content"), "post_content": php_sprintf("<!-- wp:paragraph -->\n<p>%s</p>\n<!-- /wp:paragraph -->", _x("This is a page with some basic contact information, such as an address and phone number. You might also try a plugin to add a contact form.", "Theme starter content"))})}, {"blog": Array({"post_type": "page", "post_title": _x("Blog", "Theme starter content")})}, {"news": Array({"post_type": "page", "post_title": _x("News", "Theme starter content")})}, {"homepage-section": Array({"post_type": "page", "post_title": _x("A homepage section", "Theme starter content"), "post_content": php_sprintf("<!-- wp:paragraph -->\n<p>%s</p>\n<!-- /wp:paragraph -->", _x("This is an example of a homepage section. Homepage sections can be any page other than the homepage itself, including the page that shows your latest blog posts.", "Theme starter content"))})})})
    content = Array()
    for type,args in config:
        for case in Switch(type):
            if case("options"):
                pass
            # end if
            if case("theme_mods"):
                content[type] = config[type]
                break
            # end if
            if case("widgets"):
                for sidebar_id,widgets in config[type]:
                    for id,widget in widgets:
                        if php_is_array(widget):
                            #// Item extends core content.
                            if (not php_empty(lambda : core_content[type][id])):
                                widget = Array(core_content[type][id][0], php_array_merge(core_content[type][id][1], widget))
                            # end if
                            content[type][sidebar_id][-1] = widget
                        elif php_is_string(widget) and (not php_empty(lambda : core_content[type])) and (not php_empty(lambda : core_content[type][widget])):
                            content[type][sidebar_id][-1] = core_content[type][widget]
                        # end if
                    # end for
                # end for
                break
            # end if
            if case("nav_menus"):
                for nav_menu_location,nav_menu in config[type]:
                    #// Ensure nav menus get a name.
                    if php_empty(lambda : nav_menu["name"]):
                        nav_menu["name"] = nav_menu_location
                    # end if
                    content[type][nav_menu_location]["name"] = nav_menu["name"]
                    for id,nav_menu_item in nav_menu["items"]:
                        if php_is_array(nav_menu_item):
                            #// Item extends core content.
                            if (not php_empty(lambda : core_content[type][id])):
                                nav_menu_item = php_array_merge(core_content[type][id], nav_menu_item)
                            # end if
                            content[type][nav_menu_location]["items"][-1] = nav_menu_item
                        elif php_is_string(nav_menu_item) and (not php_empty(lambda : core_content[type])) and (not php_empty(lambda : core_content[type][nav_menu_item])):
                            content[type][nav_menu_location]["items"][-1] = core_content[type][nav_menu_item]
                        # end if
                    # end for
                # end for
                break
            # end if
            if case("attachments"):
                for id,item in config[type]:
                    if (not php_empty(lambda : item["file"])):
                        content[type][id] = item
                    # end if
                # end for
                break
            # end if
            if case("posts"):
                for id,item in config[type]:
                    if php_is_array(item):
                        #// Item extends core content.
                        if (not php_empty(lambda : core_content[type][id])):
                            item = php_array_merge(core_content[type][id], item)
                        # end if
                        #// Enforce a subset of fields.
                        content[type][id] = wp_array_slice_assoc(item, Array("post_type", "post_title", "post_excerpt", "post_name", "post_content", "menu_order", "comment_status", "thumbnail", "template"))
                    elif php_is_string(item) and (not php_empty(lambda : core_content[type][item])):
                        content[type][item] = core_content[type][item]
                    # end if
                # end for
                break
            # end if
        # end for
    # end for
    #// 
    #// Filters the expanded array of starter content.
    #// 
    #// @since 4.7.0
    #// 
    #// @param array $content Array of starter content.
    #// @param array $config  Array of theme-specific starter content configuration.
    #//
    return apply_filters("get_theme_starter_content", content, config)
# end def get_theme_starter_content
#// 
#// Registers theme support for a given feature.
#// 
#// Must be called in the theme's functions.php file to work.
#// If attached to a hook, it must be {@see 'after_setup_theme'}.
#// The {@see 'init'} hook may be too late for some features.
#// 
#// Example usage:
#// 
#// add_theme_support( 'title-tag' );
#// add_theme_support( 'custom-logo', array(
#// 'height' => 480,
#// 'width'  => 720,
#// ) );
#// 
#// @since 2.9.0
#// @since 3.6.0 The `html5` feature was added.
#// @since 3.9.0 The `html5` feature now also accepts 'gallery' and 'caption'.
#// @since 4.1.0 The `title-tag` feature was added.
#// @since 4.5.0 The `customize-selective-refresh-widgets` feature was added.
#// @since 4.7.0 The `starter-content` feature was added.
#// @since 5.0.0 The `responsive-embeds`, `align-wide`, `dark-editor-style`, `disable-custom-colors`,
#// `disable-custom-font-sizes`, `editor-color-palette`, `editor-font-sizes`,
#// `editor-styles`, and `wp-block-styles` features were added.
#// @since 5.3.0 The `html5` feature now also accepts 'script' and 'style'.
#// @since 5.3.0 Formalized the existing and already documented `...$args` parameter
#// by adding it to the function signature.
#// 
#// @global array $_wp_theme_features
#// 
#// @param string $feature The feature being added. Likely core values include 'post-formats',
#// 'post-thumbnails', 'html5', 'custom-logo', 'custom-header-uploads',
#// 'custom-header', 'custom-background', 'title-tag', 'starter-content',
#// 'responsive-embeds', etc.
#// @param mixed  ...$args Optional extra arguments to pass along with certain features.
#// @return void|bool False on failure, void otherwise.
#//
def add_theme_support(feature=None, *args):
    
    global _wp_theme_features
    php_check_if_defined("_wp_theme_features")
    if (not args):
        args = True
    # end if
    for case in Switch(feature):
        if case("post-thumbnails"):
            #// All post types are already supported.
            if True == get_theme_support("post-thumbnails"):
                return
            # end if
            #// 
            #// Merge post types with any that already declared their support
            #// for post thumbnails.
            #//
            if (php_isset(lambda : args[0])) and php_is_array(args[0]) and (php_isset(lambda : _wp_theme_features["post-thumbnails"])):
                args[0] = array_unique(php_array_merge(_wp_theme_features["post-thumbnails"][0], args[0]))
            # end if
            break
        # end if
        if case("post-formats"):
            if (php_isset(lambda : args[0])) and php_is_array(args[0]):
                post_formats = get_post_format_slugs()
                post_formats["standard"] = None
                args[0] = php_array_intersect(args[0], php_array_keys(post_formats))
            # end if
            break
        # end if
        if case("html5"):
            #// You can't just pass 'html5', you need to pass an array of types.
            if php_empty(lambda : args[0]):
                #// Build an array of types for back-compat.
                args = Array({0: Array("comment-list", "comment-form", "search-form")})
            elif (not (php_isset(lambda : args[0]))) or (not php_is_array(args[0])):
                _doing_it_wrong("add_theme_support( 'html5' )", __("You need to pass an array of types."), "3.6.1")
                return False
            # end if
            #// Calling 'html5' again merges, rather than overwrites.
            if (php_isset(lambda : _wp_theme_features["html5"])):
                args[0] = php_array_merge(_wp_theme_features["html5"][0], args[0])
            # end if
            break
        # end if
        if case("custom-logo"):
            if True == args:
                args = Array({0: Array()})
            # end if
            defaults = Array({"width": None, "height": None, "flex-width": False, "flex-height": False, "header-text": ""})
            args[0] = wp_parse_args(php_array_intersect_key(args[0], defaults), defaults)
            #// Allow full flexibility if no size is specified.
            if php_is_null(args[0]["width"]) and php_is_null(args[0]["height"]):
                args[0]["flex-width"] = True
                args[0]["flex-height"] = True
            # end if
            break
        # end if
        if case("custom-header-uploads"):
            return add_theme_support("custom-header", Array({"uploads": True}))
        # end if
        if case("custom-header"):
            if True == args:
                args = Array({0: Array()})
            # end if
            defaults = Array({"default-image": "", "random-default": False, "width": 0, "height": 0, "flex-height": False, "flex-width": False, "default-text-color": "", "header-text": True, "uploads": True, "wp-head-callback": "", "admin-head-callback": "", "admin-preview-callback": "", "video": False, "video-active-callback": "is_front_page"})
            jit = (php_isset(lambda : args[0]["__jit"]))
            args[0]["__jit"] = None
            #// Merge in data from previous add_theme_support() calls.
            #// The first value registered wins. (A child theme is set up first.)
            if (php_isset(lambda : _wp_theme_features["custom-header"])):
                args[0] = wp_parse_args(_wp_theme_features["custom-header"][0], args[0])
            # end if
            #// Load in the defaults at the end, as we need to insure first one wins.
            #// This will cause all constants to be defined, as each arg will then be set to the default.
            if jit:
                args[0] = wp_parse_args(args[0], defaults)
            # end if
            #// 
            #// If a constant was defined, use that value. Otherwise, define the constant to ensure
            #// the constant is always accurate (and is not defined later,  overriding our value).
            #// As stated above, the first value wins.
            #// Once we get to wp_loaded (just-in-time), define any constants we haven't already.
            #// Constants are lame. Don't reference them. This is just for backward compatibility.
            #//
            if php_defined("NO_HEADER_TEXT"):
                args[0]["header-text"] = (not NO_HEADER_TEXT)
            elif (php_isset(lambda : args[0]["header-text"])):
                php_define("NO_HEADER_TEXT", php_empty(lambda : args[0]["header-text"]))
            # end if
            if php_defined("HEADER_IMAGE_WIDTH"):
                args[0]["width"] = int(HEADER_IMAGE_WIDTH)
            elif (php_isset(lambda : args[0]["width"])):
                php_define("HEADER_IMAGE_WIDTH", int(args[0]["width"]))
            # end if
            if php_defined("HEADER_IMAGE_HEIGHT"):
                args[0]["height"] = int(HEADER_IMAGE_HEIGHT)
            elif (php_isset(lambda : args[0]["height"])):
                php_define("HEADER_IMAGE_HEIGHT", int(args[0]["height"]))
            # end if
            if php_defined("HEADER_TEXTCOLOR"):
                args[0]["default-text-color"] = HEADER_TEXTCOLOR
            elif (php_isset(lambda : args[0]["default-text-color"])):
                php_define("HEADER_TEXTCOLOR", args[0]["default-text-color"])
            # end if
            if php_defined("HEADER_IMAGE"):
                args[0]["default-image"] = HEADER_IMAGE
            elif (php_isset(lambda : args[0]["default-image"])):
                php_define("HEADER_IMAGE", args[0]["default-image"])
            # end if
            if jit and (not php_empty(lambda : args[0]["default-image"])):
                args[0]["random-default"] = False
            # end if
            #// If headers are supported, and we still don't have a defined width or height,
            #// we have implicit flex sizes.
            if jit:
                if php_empty(lambda : args[0]["width"]) and php_empty(lambda : args[0]["flex-width"]):
                    args[0]["flex-width"] = True
                # end if
                if php_empty(lambda : args[0]["height"]) and php_empty(lambda : args[0]["flex-height"]):
                    args[0]["flex-height"] = True
                # end if
            # end if
            break
        # end if
        if case("custom-background"):
            if True == args:
                args = Array({0: Array()})
            # end if
            defaults = Array({"default-image": "", "default-preset": "default", "default-position-x": "left", "default-position-y": "top", "default-size": "auto", "default-repeat": "repeat", "default-attachment": "scroll", "default-color": "", "wp-head-callback": "_custom_background_cb", "admin-head-callback": "", "admin-preview-callback": ""})
            jit = (php_isset(lambda : args[0]["__jit"]))
            args[0]["__jit"] = None
            #// Merge in data from previous add_theme_support() calls. The first value registered wins.
            if (php_isset(lambda : _wp_theme_features["custom-background"])):
                args[0] = wp_parse_args(_wp_theme_features["custom-background"][0], args[0])
            # end if
            if jit:
                args[0] = wp_parse_args(args[0], defaults)
            # end if
            if php_defined("BACKGROUND_COLOR"):
                args[0]["default-color"] = BACKGROUND_COLOR
            elif (php_isset(lambda : args[0]["default-color"])) or jit:
                php_define("BACKGROUND_COLOR", args[0]["default-color"])
            # end if
            if php_defined("BACKGROUND_IMAGE"):
                args[0]["default-image"] = BACKGROUND_IMAGE
            elif (php_isset(lambda : args[0]["default-image"])) or jit:
                php_define("BACKGROUND_IMAGE", args[0]["default-image"])
            # end if
            break
        # end if
        if case("title-tag"):
            #// Can be called in functions.php but must happen before wp_loaded, i.e. not in header.php.
            if did_action("wp_loaded"):
                _doing_it_wrong("add_theme_support( 'title-tag' )", php_sprintf(__("Theme support for %1$s should be registered before the %2$s hook."), "<code>title-tag</code>", "<code>wp_loaded</code>"), "4.1.0")
                return False
            # end if
        # end if
    # end for
    _wp_theme_features[feature] = args
# end def add_theme_support
#// 
#// Registers the internal custom header and background routines.
#// 
#// @since 3.4.0
#// @access private
#// 
#// @global Custom_Image_Header $custom_image_header
#// @global Custom_Background   $custom_background
#//
def _custom_header_background_just_in_time(*args_):
    
    global custom_image_header,custom_background
    php_check_if_defined("custom_image_header","custom_background")
    if current_theme_supports("custom-header"):
        #// In case any constants were defined after an add_custom_image_header() call, re-run.
        add_theme_support("custom-header", Array({"__jit": True}))
        args = get_theme_support("custom-header")
        if args[0]["wp-head-callback"]:
            add_action("wp_head", args[0]["wp-head-callback"])
        # end if
        if is_admin():
            php_include_file(ABSPATH + "wp-admin/includes/class-custom-image-header.php", once=True)
            custom_image_header = php_new_class("Custom_Image_Header", lambda : Custom_Image_Header(args[0]["admin-head-callback"], args[0]["admin-preview-callback"]))
        # end if
    # end if
    if current_theme_supports("custom-background"):
        #// In case any constants were defined after an add_custom_background() call, re-run.
        add_theme_support("custom-background", Array({"__jit": True}))
        args = get_theme_support("custom-background")
        add_action("wp_head", args[0]["wp-head-callback"])
        if is_admin():
            php_include_file(ABSPATH + "wp-admin/includes/class-custom-background.php", once=True)
            custom_background = php_new_class("Custom_Background", lambda : Custom_Background(args[0]["admin-head-callback"], args[0]["admin-preview-callback"]))
        # end if
    # end if
# end def _custom_header_background_just_in_time
#// 
#// Adds CSS to hide header text for custom logo, based on Customizer setting.
#// 
#// @since 4.5.0
#// @access private
#//
def _custom_logo_header_styles(*args_):
    
    if (not current_theme_supports("custom-header", "header-text")) and get_theme_support("custom-logo", "header-text") and (not get_theme_mod("header_text", True)):
        classes = get_theme_support("custom-logo", "header-text")
        classes = php_array_map("sanitize_html_class", classes)
        classes = "." + php_implode(", .", classes)
        type_attr = "" if current_theme_supports("html5", "style") else " type=\"text/css\""
        php_print("     <!-- Custom Logo: hide header text -->\n        <style id=\"custom-logo-css\"")
        php_print(type_attr)
        php_print(">\n          ")
        php_print(classes)
        php_print(""" {
        position: absolute;
        clip: rect(1px, 1px, 1px, 1px);
        }
        </style>
        """)
    # end if
# end def _custom_logo_header_styles
#// 
#// Gets the theme support arguments passed when registering that support
#// 
#// Example usage:
#// 
#// get_theme_support( 'custom-logo' );
#// get_theme_support( 'custom-header', 'width' );
#// 
#// @since 3.1.0
#// @since 5.3.0 Formalized the existing and already documented `...$args` parameter
#// by adding it to the function signature.
#// 
#// @global array $_wp_theme_features
#// 
#// @param string $feature The feature to check.
#// @param mixed  ...$args Optional extra arguments to be checked against certain features.
#// @return mixed The array of extra arguments or the value for the registered feature.
#//
def get_theme_support(feature=None, *args):
    
    global _wp_theme_features
    php_check_if_defined("_wp_theme_features")
    if (not (php_isset(lambda : _wp_theme_features[feature]))):
        return False
    # end if
    if (not args):
        return _wp_theme_features[feature]
    # end if
    for case in Switch(feature):
        if case("custom-logo"):
            pass
        # end if
        if case("custom-header"):
            pass
        # end if
        if case("custom-background"):
            if (php_isset(lambda : _wp_theme_features[feature][0][args[0]])):
                return _wp_theme_features[feature][0][args[0]]
            # end if
            return False
        # end if
        if case():
            return _wp_theme_features[feature]
        # end if
    # end for
# end def get_theme_support
#// 
#// Allows a theme to de-register its support of a certain feature
#// 
#// Should be called in the theme's functions.php file. Generally would
#// be used for child themes to override support from the parent theme.
#// 
#// @since 3.0.0
#// @see add_theme_support()
#// @param string $feature The feature being removed.
#// @return bool|void Whether feature was removed.
#//
def remove_theme_support(feature=None, *args_):
    
    #// Blacklist: for internal registrations not used directly by themes.
    if php_in_array(feature, Array("editor-style", "widgets", "menus")):
        return False
    # end if
    return _remove_theme_support(feature)
# end def remove_theme_support
#// 
#// Do not use. Removes theme support internally, ignorant of the blacklist.
#// 
#// @access private
#// @since 3.1.0
#// 
#// @global array               $_wp_theme_features
#// @global Custom_Image_Header $custom_image_header
#// @global Custom_Background   $custom_background
#// 
#// @param string $feature
#//
def _remove_theme_support(feature=None, *args_):
    
    global _wp_theme_features
    php_check_if_defined("_wp_theme_features")
    for case in Switch(feature):
        if case("custom-header-uploads"):
            if (not (php_isset(lambda : _wp_theme_features["custom-header"]))):
                return False
            # end if
            add_theme_support("custom-header", Array({"uploads": False}))
            return
        # end if
    # end for
    if (not (php_isset(lambda : _wp_theme_features[feature]))):
        return False
    # end if
    for case in Switch(feature):
        if case("custom-header"):
            if (not did_action("wp_loaded")):
                break
            # end if
            support = get_theme_support("custom-header")
            if (php_isset(lambda : support[0]["wp-head-callback"])):
                remove_action("wp_head", support[0]["wp-head-callback"])
            # end if
            if (php_isset(lambda : PHP_GLOBALS["custom_image_header"])):
                remove_action("admin_menu", Array(PHP_GLOBALS["custom_image_header"], "init"))
                PHP_GLOBALS["custom_image_header"] = None
            # end if
            break
        # end if
        if case("custom-background"):
            if (not did_action("wp_loaded")):
                break
            # end if
            support = get_theme_support("custom-background")
            if (php_isset(lambda : support[0]["wp-head-callback"])):
                remove_action("wp_head", support[0]["wp-head-callback"])
            # end if
            remove_action("admin_menu", Array(PHP_GLOBALS["custom_background"], "init"))
            PHP_GLOBALS["custom_background"] = None
            break
        # end if
    # end for
    _wp_theme_features[feature] = None
    return True
# end def _remove_theme_support
#// 
#// Checks a theme's support for a given feature.
#// 
#// Example usage:
#// 
#// current_theme_supports( 'custom-logo' );
#// current_theme_supports( 'html5', 'comment-form' );
#// 
#// @since 2.9.0
#// @since 5.3.0 Formalized the existing and already documented `...$args` parameter
#// by adding it to the function signature.
#// 
#// @global array $_wp_theme_features
#// 
#// @param string $feature The feature being checked.
#// @param mixed  ...$args Optional extra arguments to be checked against certain features.
#// @return bool True if the current theme supports the feature, false otherwise.
#//
def current_theme_supports(feature=None, *args):
    
    global _wp_theme_features
    php_check_if_defined("_wp_theme_features")
    if "custom-header-uploads" == feature:
        return current_theme_supports("custom-header", "uploads")
    # end if
    if (not (php_isset(lambda : _wp_theme_features[feature]))):
        return False
    # end if
    #// If no args passed then no extra checks need be performed.
    if (not args):
        return True
    # end if
    for case in Switch(feature):
        if case("post-thumbnails"):
            #// 
            #// post-thumbnails can be registered for only certain content/post types
            #// by passing an array of types to add_theme_support().
            #// If no array was passed, then any type is accepted.
            #//
            if True == _wp_theme_features[feature]:
                #// Registered for all types
                return True
            # end if
            content_type = args[0]
            return php_in_array(content_type, _wp_theme_features[feature][0])
        # end if
        if case("html5"):
            pass
        # end if
        if case("post-formats"):
            #// 
            #// Specific post formats can be registered by passing an array of types
            #// to add_theme_support().
            #// 
            #// Specific areas of HTML5 support *must* be passed via an array to add_theme_support().
            #//
            type = args[0]
            return php_in_array(type, _wp_theme_features[feature][0])
        # end if
        if case("custom-logo"):
            pass
        # end if
        if case("custom-header"):
            pass
        # end if
        if case("custom-background"):
            #// Specific capabilities can be registered by passing an array to add_theme_support().
            return (php_isset(lambda : _wp_theme_features[feature][0][args[0]])) and _wp_theme_features[feature][0][args[0]]
        # end if
    # end for
    #// 
    #// Filters whether the current theme supports a specific feature.
    #// 
    #// The dynamic portion of the hook name, `$feature`, refers to the specific theme
    #// feature. Possible values include 'post-formats', 'post-thumbnails', 'custom-background',
    #// 'custom-header', 'menus', 'automatic-feed-links', 'html5',
    #// 'starter-content', and 'customize-selective-refresh-widgets'.
    #// 
    #// @since 3.4.0
    #// 
    #// @param bool   $supports Whether the current theme supports the given feature. Default true.
    #// @param array  $args     Array of arguments for the feature.
    #// @param string $feature  The theme feature.
    #//
    return apply_filters(str("current_theme_supports-") + str(feature), True, args, _wp_theme_features[feature])
    pass
# end def current_theme_supports
#// 
#// Checks a theme's support for a given feature before loading the functions which implement it.
#// 
#// @since 2.9.0
#// 
#// @param string $feature The feature being checked.
#// @param string $include Path to the file.
#// @return bool True if the current theme supports the supplied feature, false otherwise.
#//
def require_if_theme_supports(feature=None, include=None, *args_):
    
    if current_theme_supports(feature):
        php_include_file(include, once=False)
        return True
    # end if
    return False
# end def require_if_theme_supports
#// 
#// Checks an attachment being deleted to see if it's a header or background image.
#// 
#// If true it removes the theme modification which would be pointing at the deleted
#// attachment.
#// 
#// @access private
#// @since 3.0.0
#// @since 4.3.0 Also removes `header_image_data`.
#// @since 4.5.0 Also removes custom logo theme mods.
#// 
#// @param int $id The attachment id.
#//
def _delete_attachment_theme_mod(id=None, *args_):
    
    attachment_image = wp_get_attachment_url(id)
    header_image = get_header_image()
    background_image = get_background_image()
    custom_logo_id = get_theme_mod("custom_logo")
    if custom_logo_id and custom_logo_id == id:
        remove_theme_mod("custom_logo")
        remove_theme_mod("header_text")
    # end if
    if header_image and header_image == attachment_image:
        remove_theme_mod("header_image")
        remove_theme_mod("header_image_data")
    # end if
    if background_image and background_image == attachment_image:
        remove_theme_mod("background_image")
    # end if
# end def _delete_attachment_theme_mod
#// 
#// Checks if a theme has been changed and runs 'after_switch_theme' hook on the next WP load.
#// 
#// See {@see 'after_switch_theme'}.
#// 
#// @since 3.3.0
#//
def check_theme_switched(*args_):
    
    stylesheet = get_option("theme_switched")
    if stylesheet:
        old_theme = wp_get_theme(stylesheet)
        #// Prevent widget & menu mapping from running since Customizer already called it up front.
        if get_option("theme_switched_via_customizer"):
            remove_action("after_switch_theme", "_wp_menus_changed")
            remove_action("after_switch_theme", "_wp_sidebars_changed")
            update_option("theme_switched_via_customizer", False)
        # end if
        if old_theme.exists():
            #// 
            #// Fires on the first WP load after a theme switch if the old theme still exists.
            #// 
            #// This action fires multiple times and the parameters differs
            #// according to the context, if the old theme exists or not.
            #// If the old theme is missing, the parameter will be the slug
            #// of the old theme.
            #// 
            #// @since 3.3.0
            #// 
            #// @param string   $old_name  Old theme name.
            #// @param WP_Theme $old_theme WP_Theme instance of the old theme.
            #//
            do_action("after_switch_theme", old_theme.get("Name"), old_theme)
        else:
            #// This action is documented in wp-includes/theme.php
            do_action("after_switch_theme", stylesheet, old_theme)
        # end if
        flush_rewrite_rules()
        update_option("theme_switched", False)
    # end if
# end def check_theme_switched
#// 
#// Includes and instantiates the WP_Customize_Manager class.
#// 
#// Loads the Customizer at plugins_loaded when accessing the customize.php admin
#// page or when any request includes a wp_customize=on param or a customize_changeset
#// param (a UUID). This param is a signal for whether to bootstrap the Customizer when
#// WordPress is loading, especially in the Customizer preview
#// or when making Customizer Ajax requests for widgets or menus.
#// 
#// @since 3.4.0
#// 
#// @global WP_Customize_Manager $wp_customize
#//
def _wp_customize_include(*args_):
    global PHP_GLOBALS
    is_customize_admin_page = is_admin() and "customize.php" == php_basename(PHP_SERVER["PHP_SELF"])
    should_include = is_customize_admin_page or (php_isset(lambda : PHP_REQUEST["wp_customize"])) and "on" == PHP_REQUEST["wp_customize"] or (not php_empty(lambda : PHP_REQUEST["customize_changeset_uuid"])) or (not php_empty(lambda : PHP_POST["customize_changeset_uuid"]))
    if (not should_include):
        return
    # end if
    #// 
    #// Note that wp_unslash() is not being used on the input vars because it is
    #// called before wp_magic_quotes() gets called. Besides this fact, none of
    #// the values should contain any characters needing slashes anyway.
    #//
    keys = Array("changeset_uuid", "customize_changeset_uuid", "customize_theme", "theme", "customize_messenger_channel", "customize_autosaved")
    input_vars = php_array_merge(wp_array_slice_assoc(PHP_REQUEST, keys), wp_array_slice_assoc(PHP_POST, keys))
    theme = None
    autosaved = None
    messenger_channel = None
    #// Value false indicates UUID should be determined after_setup_theme
    #// to either re-use existing saved changeset or else generate a new UUID if none exists.
    changeset_uuid = False
    #// Set initially fo false since defaults to true for back-compat;
    #// can be overridden via the customize_changeset_branching filter.
    branching = False
    if is_customize_admin_page and (php_isset(lambda : input_vars["changeset_uuid"])):
        changeset_uuid = sanitize_key(input_vars["changeset_uuid"])
    elif (not php_empty(lambda : input_vars["customize_changeset_uuid"])):
        changeset_uuid = sanitize_key(input_vars["customize_changeset_uuid"])
    # end if
    #// Note that theme will be sanitized via WP_Theme.
    if is_customize_admin_page and (php_isset(lambda : input_vars["theme"])):
        theme = input_vars["theme"]
    elif (php_isset(lambda : input_vars["customize_theme"])):
        theme = input_vars["customize_theme"]
    # end if
    if (not php_empty(lambda : input_vars["customize_autosaved"])):
        autosaved = True
    # end if
    if (php_isset(lambda : input_vars["customize_messenger_channel"])):
        messenger_channel = sanitize_key(input_vars["customize_messenger_channel"])
    # end if
    #// 
    #// Note that settings must be previewed even outside the customizer preview
    #// and also in the customizer pane itself. This is to enable loading an existing
    #// changeset into the customizer. Previewing the settings only has to be prevented
    #// here in the case of a customize_save action because this will cause WP to think
    #// there is nothing changed that needs to be saved.
    #//
    is_customize_save_action = wp_doing_ajax() and (php_isset(lambda : PHP_REQUEST["action"])) and "customize_save" == wp_unslash(PHP_REQUEST["action"])
    settings_previewed = (not is_customize_save_action)
    php_include_file(ABSPATH + WPINC + "/class-wp-customize-manager.php", once=True)
    PHP_GLOBALS["wp_customize"] = php_new_class("WP_Customize_Manager", lambda : WP_Customize_Manager(compact("changeset_uuid", "theme", "messenger_channel", "settings_previewed", "autosaved", "branching")))
# end def _wp_customize_include
#// 
#// Publishes a snapshot's changes.
#// 
#// @since 4.7.0
#// @access private
#// 
#// @global wpdb                 $wpdb         WordPress database abstraction object.
#// @global WP_Customize_Manager $wp_customize Customizer instance.
#// 
#// @param string  $new_status     New post status.
#// @param string  $old_status     Old post status.
#// @param WP_Post $changeset_post Changeset post object.
#//
def _wp_customize_publish_changeset(new_status=None, old_status=None, changeset_post=None, *args_):
    
    global wp_customize,wpdb
    php_check_if_defined("wp_customize","wpdb")
    is_publishing_changeset = "customize_changeset" == changeset_post.post_type and "publish" == new_status and "publish" != old_status
    if (not is_publishing_changeset):
        return
    # end if
    if php_empty(lambda : wp_customize):
        php_include_file(ABSPATH + WPINC + "/class-wp-customize-manager.php", once=True)
        wp_customize = php_new_class("WP_Customize_Manager", lambda : WP_Customize_Manager(Array({"changeset_uuid": changeset_post.post_name, "settings_previewed": False})))
    # end if
    if (not did_action("customize_register")):
        #// 
        #// When running from CLI or Cron, the customize_register action will need
        #// to be triggered in order for core, themes, and plugins to register their
        #// settings. Normally core will add_action( 'customize_register' ) at
        #// priority 10 to register the core settings, and if any themes/plugins
        #// also add_action( 'customize_register' ) at the same priority, they
        #// will have a $wp_customize with those settings registered since they
        #// call add_action() afterward, normally. However, when manually doing
        #// the customize_register action after the setup_theme, then the order
        #// will be reversed for two actions added at priority 10, resulting in
        #// the core settings no longer being available as expected to themes/plugins.
        #// So the following manually calls the method that registers the core
        #// settings up front before doing the action.
        #//
        remove_action("customize_register", Array(wp_customize, "register_controls"))
        wp_customize.register_controls()
        #// This filter is documented in /wp-includes/class-wp-customize-manager.php
        do_action("customize_register", wp_customize)
    # end if
    wp_customize._publish_changeset_values(changeset_post.ID)
    #// 
    #// Trash the changeset post if revisions are not enabled. Unpublished
    #// changesets by default get garbage collected due to the auto-draft status.
    #// When a changeset post is published, however, it would no longer get cleaned
    #// out. This is a problem when the changeset posts are never displayed anywhere,
    #// since they would just be endlessly piling up. So here we use the revisions
    #// feature to indicate whether or not a published changeset should get trashed
    #// and thus garbage collected.
    #//
    if (not wp_revisions_enabled(changeset_post)):
        wp_customize.trash_changeset_post(changeset_post.ID)
    # end if
# end def _wp_customize_publish_changeset
#// 
#// Filters changeset post data upon insert to ensure post_name is intact.
#// 
#// This is needed to prevent the post_name from being dropped when the post is
#// transitioned into pending status by a contributor.
#// 
#// @since 4.7.0
#// @see wp_insert_post()
#// 
#// @param array $post_data          An array of slashed post data.
#// @param array $supplied_post_data An array of sanitized, but otherwise unmodified post data.
#// @return array Filtered data.
#//
def _wp_customize_changeset_filter_insert_post_data(post_data=None, supplied_post_data=None, *args_):
    
    if (php_isset(lambda : post_data["post_type"])) and "customize_changeset" == post_data["post_type"]:
        #// Prevent post_name from being dropped, such as when contributor saves a changeset post as pending.
        if php_empty(lambda : post_data["post_name"]) and (not php_empty(lambda : supplied_post_data["post_name"])):
            post_data["post_name"] = supplied_post_data["post_name"]
        # end if
    # end if
    return post_data
# end def _wp_customize_changeset_filter_insert_post_data
#// 
#// Adds settings for the customize-loader script.
#// 
#// @since 3.4.0
#//
def _wp_customize_loader_settings(*args_):
    
    admin_origin = php_parse_url(admin_url())
    home_origin = php_parse_url(home_url())
    cross_domain = php_strtolower(admin_origin["host"]) != php_strtolower(home_origin["host"])
    browser = Array({"mobile": wp_is_mobile(), "ios": wp_is_mobile() and php_preg_match("/iPad|iPod|iPhone/", PHP_SERVER["HTTP_USER_AGENT"])})
    settings = Array({"url": esc_url(admin_url("customize.php")), "isCrossDomain": cross_domain, "browser": browser, "l10n": Array({"saveAlert": __("The changes you made will be lost if you navigate away from this page."), "mainIframeTitle": __("Customizer")})})
    script = "var _wpCustomizeLoaderSettings = " + wp_json_encode(settings) + ";"
    wp_scripts = wp_scripts()
    data = wp_scripts.get_data("customize-loader", "data")
    if data:
        script = str(data) + str("\n") + str(script)
    # end if
    wp_scripts.add_data("customize-loader", "data", script)
# end def _wp_customize_loader_settings
#// 
#// Returns a URL to load the Customizer.
#// 
#// @since 3.4.0
#// 
#// @param string $stylesheet Optional. Theme to customize. Defaults to current theme.
#// The theme's stylesheet will be urlencoded if necessary.
#// @return string
#//
def wp_customize_url(stylesheet="", *args_):
    
    url = admin_url("customize.php")
    if stylesheet:
        url += "?theme=" + urlencode(stylesheet)
    # end if
    return esc_url(url)
# end def wp_customize_url
#// 
#// Prints a script to check whether or not the Customizer is supported,
#// and apply either the no-customize-support or customize-support class
#// to the body.
#// 
#// This function MUST be called inside the body tag.
#// 
#// Ideally, call this function immediately after the body tag is opened.
#// This prevents a flash of unstyled content.
#// 
#// It is also recommended that you add the "no-customize-support" class
#// to the body tag by default.
#// 
#// @since 3.4.0
#// @since 4.7.0 Support for IE8 and below is explicitly removed via conditional comments.
#//
def wp_customize_support_script(*args_):
    
    admin_origin = php_parse_url(admin_url())
    home_origin = php_parse_url(home_url())
    cross_domain = php_strtolower(admin_origin["host"]) != php_strtolower(home_origin["host"])
    type_attr = "" if current_theme_supports("html5", "script") else " type=\"text/javascript\""
    php_print(" <!--[if lte IE 8]>\n        <script")
    php_print(type_attr)
    php_print(""">
    document.body.className = document.body.className.replace( /(^|\\s)(no-)?customize-support(?=\\s|$)/, '' ) + ' no-customize-support';
    </script>
    <![endif]-->
    <!--[if gte IE 9]><!-->
    <script""")
    php_print(type_attr)
    php_print(""">
    (function() {
    var request, b = document.body, c = 'className', cs = 'customize-support', rcs = new RegExp('(^|\\\\s+)(no-)?'+cs+'(\\\\s+|$)');
    """)
    if cross_domain:
        php_print("             request = (function(){ var xhr = new XMLHttpRequest(); return ('withCredentials' in xhr); })();\n       ")
    else:
        php_print("             request = true;\n       ")
    # end if
    php_print("""
    b[c] = b[c].replace( rcs, ' ' );
    // The customizer requires postMessage and CORS (if the site is cross domain).
    b[c] += ( window.postMessage && request ? ' ' : ' no-' ) + cs;
    }());
    </script>
    <!--<![endif]-->
    """)
# end def wp_customize_support_script
#// 
#// Whether the site is being previewed in the Customizer.
#// 
#// @since 4.0.0
#// 
#// @global WP_Customize_Manager $wp_customize Customizer instance.
#// 
#// @return bool True if the site is being previewed in the Customizer, false otherwise.
#//
def is_customize_preview(*args_):
    
    global wp_customize
    php_check_if_defined("wp_customize")
    return type(wp_customize).__name__ == "WP_Customize_Manager" and wp_customize.is_preview()
# end def is_customize_preview
#// 
#// Make sure that auto-draft posts get their post_date bumped or status changed to draft to prevent premature garbage-collection.
#// 
#// When a changeset is updated but remains an auto-draft, ensure the post_date
#// for the auto-draft posts remains the same so that it will be
#// garbage-collected at the same time by `wp_delete_auto_drafts()`. Otherwise,
#// if the changeset is updated to be a draft then update the posts
#// to have a far-future post_date so that they will never be garbage collected
#// unless the changeset post itself is deleted.
#// 
#// When a changeset is updated to be a persistent draft or to be scheduled for
#// publishing, then transition any dependent auto-drafts to a draft status so
#// that they likewise will not be garbage-collected but also so that they can
#// be edited in the admin before publishing since there is not yet a post/page
#// editing flow in the Customizer. See #39752.
#// 
#// @link https://core.trac.wordpress.org/ticket/39752
#// 
#// @since 4.8.0
#// @access private
#// @see wp_delete_auto_drafts()
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param string   $new_status Transition to this post status.
#// @param string   $old_status Previous post status.
#// @param \WP_Post $post       Post data.
#//
def _wp_keep_alive_customize_changeset_dependent_auto_drafts(new_status=None, old_status=None, post=None, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    old_status = None
    #// Short-circuit if not a changeset or if the changeset was published.
    if "customize_changeset" != post.post_type or "publish" == new_status:
        return
    # end if
    data = php_json_decode(post.post_content, True)
    if php_empty(lambda : data["nav_menus_created_posts"]["value"]):
        return
    # end if
    #// 
    #// Actually, in lieu of keeping alive, trash any customization drafts here if the changeset itself is
    #// getting trashed. This is needed because when a changeset transitions to a draft, then any of the
    #// dependent auto-draft post/page stubs will also get transitioned to customization drafts which
    #// are then visible in the WP Admin. We cannot wait for the deletion of the changeset in which
    #// _wp_delete_customize_changeset_dependent_auto_drafts() will be called, since they need to be
    #// trashed to remove from visibility immediately.
    #//
    if "trash" == new_status:
        for post_id in data["nav_menus_created_posts"]["value"]:
            if (not php_empty(lambda : post_id)) and "draft" == get_post_status(post_id):
                wp_trash_post(post_id)
            # end if
        # end for
        return
    # end if
    post_args = Array()
    if "auto-draft" == new_status:
        #// 
        #// Keep the post date for the post matching the changeset
        #// so that it will not be garbage-collected before the changeset.
        #//
        post_args["post_date"] = post.post_date
        pass
    else:
        #// 
        #// Since the changeset no longer has an auto-draft (and it is not published)
        #// it is now a persistent changeset, a long-lived draft, and so any
        #// associated auto-draft posts should likewise transition into having a draft
        #// status. These drafts will be treated differently than regular drafts in
        #// that they will be tied to the given changeset. The publish meta box is
        #// replaced with a notice about how the post is part of a set of customized changes
        #// which will be published when the changeset is published.
        #//
        post_args["post_status"] = "draft"
    # end if
    for post_id in data["nav_menus_created_posts"]["value"]:
        if php_empty(lambda : post_id) or "auto-draft" != get_post_status(post_id):
            continue
        # end if
        wpdb.update(wpdb.posts, post_args, Array({"ID": post_id}))
        clean_post_cache(post_id)
    # end for
# end def _wp_keep_alive_customize_changeset_dependent_auto_drafts