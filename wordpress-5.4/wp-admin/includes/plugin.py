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
#// WordPress Plugin Administration API
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// 
#// Parses the plugin contents to retrieve plugin's metadata.
#// 
#// All plugin headers must be on their own line. Plugin description must not have
#// any newlines, otherwise only parts of the description will be displayed.
#// The below is formatted for printing.
#// 
#// 
#// Plugin Name: Name of the plugin.
#// Plugin URI: The home page of the plugin.
#// Description: Plugin description.
#// Author: Plugin author's name.
#// Author URI: Link to the author's website.
#// Version: Plugin version.
#// Text Domain: Optional. Unique identifier, should be same as the one used in
#// load_plugin_textdomain().
#// Domain Path: Optional. Only useful if the translations are located in a
#// folder above the plugin's base path. For example, if .mo files are
#// located in the locale folder then Domain Path will be "/locale/" and
#// must have the first slash. Defaults to the base folder the plugin is
#// located in.
#// Network: Optional. Specify "Network: true" to require that a plugin is activated
#// across all sites in an installation. This will prevent a plugin from being
#// activated on a single site when Multisite is enabled.
#// Requires at least: Optional. Specify the minimum required WordPress version.
#// Requires PHP: Optional. Specify the minimum required PHP version.
#// # Remove the space to close comment.
#// 
#// The first 8 KB of the file will be pulled in and if the plugin data is not
#// within that first 8 KB, then the plugin author should correct their plugin
#// and move the plugin data headers to the top.
#// 
#// The plugin file is assumed to have permissions to allow for scripts to read
#// the file. This is not checked however and the file is only opened for
#// reading.
#// 
#// @since 1.5.0
#// @since 5.3.0 Added support for `Requires at least` and `Requires PHP` headers.
#// 
#// @param string $plugin_file Absolute path to the main plugin file.
#// @param bool   $markup      Optional. If the returned data should have HTML markup applied.
#// Default true.
#// @param bool   $translate   Optional. If the returned data should be translated. Default true.
#// @return array {
#// Plugin data. Values will be empty if not supplied by the plugin.
#// 
#// @type string $Name        Name of the plugin. Should be unique.
#// @type string $Title       Title of the plugin and link to the plugin's site (if set).
#// @type string $Description Plugin description.
#// @type string $Author      Author's name.
#// @type string $AuthorURI   Author's website address (if set).
#// @type string $Version     Plugin version.
#// @type string $TextDomain  Plugin textdomain.
#// @type string $DomainPath  Plugins relative directory path to .mo files.
#// @type bool   $Network     Whether the plugin can only be activated network-wide.
#// @type string $RequiresWP  Minimum required version of WordPress.
#// @type string $RequiresPHP Minimum required version of PHP.
#// }
#//
def get_plugin_data(plugin_file_=None, markup_=None, translate_=None, *_args_):
    if markup_ is None:
        markup_ = True
    # end if
    if translate_ is None:
        translate_ = True
    # end if
    
    default_headers_ = Array({"Name": "Plugin Name", "PluginURI": "Plugin URI", "Version": "Version", "Description": "Description", "Author": "Author", "AuthorURI": "Author URI", "TextDomain": "Text Domain", "DomainPath": "Domain Path", "Network": "Network", "RequiresWP": "Requires at least", "RequiresPHP": "Requires PHP", "_sitewide": "Site Wide Only"})
    plugin_data_ = get_file_data(plugin_file_, default_headers_, "plugin")
    #// Site Wide Only is the old header for Network.
    if (not plugin_data_["Network"]) and plugin_data_["_sitewide"]:
        #// translators: 1: Site Wide Only: true, 2: Network: true
        _deprecated_argument(__FUNCTION__, "3.0.0", php_sprintf(__("The %1$s plugin header is deprecated. Use %2$s instead."), "<code>Site Wide Only: true</code>", "<code>Network: true</code>"))
        plugin_data_["Network"] = plugin_data_["_sitewide"]
    # end if
    plugin_data_["Network"] = "true" == php_strtolower(plugin_data_["Network"])
    plugin_data_["_sitewide"] = None
    #// If no text domain is defined fall back to the plugin slug.
    if (not plugin_data_["TextDomain"]):
        plugin_slug_ = php_dirname(plugin_basename(plugin_file_))
        if "." != plugin_slug_ and False == php_strpos(plugin_slug_, "/"):
            plugin_data_["TextDomain"] = plugin_slug_
        # end if
    # end if
    if markup_ or translate_:
        plugin_data_ = _get_plugin_data_markup_translate(plugin_file_, plugin_data_, markup_, translate_)
    else:
        plugin_data_["Title"] = plugin_data_["Name"]
        plugin_data_["AuthorName"] = plugin_data_["Author"]
    # end if
    return plugin_data_
# end def get_plugin_data
#// 
#// Sanitizes plugin data, optionally adds markup, optionally translates.
#// 
#// @since 2.7.0
#// 
#// @see get_plugin_data()
#// 
#// @access private
#// 
#// @param string $plugin_file Path to the main plugin file.
#// @param array  $plugin_data An array of plugin data. See `get_plugin_data()`.
#// @param bool   $markup      Optional. If the returned data should have HTML markup applied.
#// Default true.
#// @param bool   $translate   Optional. If the returned data should be translated. Default true.
#// @return array {
#// Plugin data. Values will be empty if not supplied by the plugin.
#// 
#// @type string $Name        Name of the plugin. Should be unique.
#// @type string $Title       Title of the plugin and link to the plugin's site (if set).
#// @type string $Description Plugin description.
#// @type string $Author      Author's name.
#// @type string $AuthorURI   Author's website address (if set).
#// @type string $Version     Plugin version.
#// @type string $TextDomain  Plugin textdomain.
#// @type string $DomainPath  Plugins relative directory path to .mo files.
#// @type bool   $Network     Whether the plugin can only be activated network-wide.
#// }
#//
def _get_plugin_data_markup_translate(plugin_file_=None, plugin_data_=None, markup_=None, translate_=None, *_args_):
    if markup_ is None:
        markup_ = True
    # end if
    if translate_ is None:
        translate_ = True
    # end if
    
    #// Sanitize the plugin filename to a WP_PLUGIN_DIR relative path.
    plugin_file_ = plugin_basename(plugin_file_)
    #// Translate fields.
    if translate_:
        textdomain_ = plugin_data_["TextDomain"]
        if textdomain_:
            if (not is_textdomain_loaded(textdomain_)):
                if plugin_data_["DomainPath"]:
                    load_plugin_textdomain(textdomain_, False, php_dirname(plugin_file_) + plugin_data_["DomainPath"])
                else:
                    load_plugin_textdomain(textdomain_, False, php_dirname(plugin_file_))
                # end if
            # end if
        elif "hello.php" == php_basename(plugin_file_):
            textdomain_ = "default"
        # end if
        if textdomain_:
            for field_ in Array("Name", "PluginURI", "Description", "Author", "AuthorURI", "Version"):
                #// phpcs:ignore WordPress.WP.I18n.LowLevelTranslationFunction,WordPress.WP.I18n.NonSingularStringLiteralText,WordPress.WP.I18n.NonSingularStringLiteralDomain
                plugin_data_[field_] = translate(plugin_data_[field_], textdomain_)
            # end for
        # end if
    # end if
    #// Sanitize fields.
    allowed_tags_in_links_ = Array({"abbr": Array({"title": True})}, {"acronym": Array({"title": True})}, {"code": True, "em": True, "strong": True})
    allowed_tags_ = allowed_tags_in_links_
    allowed_tags_["a"] = Array({"href": True, "title": True})
    #// Name is marked up inside <a> tags. Don't allow these.
    #// Author is too, but some plugins have used <a> here (omitting Author URI).
    plugin_data_["Name"] = wp_kses(plugin_data_["Name"], allowed_tags_in_links_)
    plugin_data_["Author"] = wp_kses(plugin_data_["Author"], allowed_tags_)
    plugin_data_["Description"] = wp_kses(plugin_data_["Description"], allowed_tags_)
    plugin_data_["Version"] = wp_kses(plugin_data_["Version"], allowed_tags_)
    plugin_data_["PluginURI"] = esc_url(plugin_data_["PluginURI"])
    plugin_data_["AuthorURI"] = esc_url(plugin_data_["AuthorURI"])
    plugin_data_["Title"] = plugin_data_["Name"]
    plugin_data_["AuthorName"] = plugin_data_["Author"]
    #// Apply markup.
    if markup_:
        if plugin_data_["PluginURI"] and plugin_data_["Name"]:
            plugin_data_["Title"] = "<a href=\"" + plugin_data_["PluginURI"] + "\">" + plugin_data_["Name"] + "</a>"
        # end if
        if plugin_data_["AuthorURI"] and plugin_data_["Author"]:
            plugin_data_["Author"] = "<a href=\"" + plugin_data_["AuthorURI"] + "\">" + plugin_data_["Author"] + "</a>"
        # end if
        plugin_data_["Description"] = wptexturize(plugin_data_["Description"])
        if plugin_data_["Author"]:
            plugin_data_["Description"] += php_sprintf(" <cite>" + __("By %s.") + "</cite>", plugin_data_["Author"])
        # end if
    # end if
    return plugin_data_
# end def _get_plugin_data_markup_translate
#// 
#// Get a list of a plugin's files.
#// 
#// @since 2.8.0
#// 
#// @param string $plugin Path to the plugin file relative to the plugins directory.
#// @return string[] Array of file names relative to the plugin root.
#//
def get_plugin_files(plugin_=None, *_args_):
    
    
    plugin_file_ = WP_PLUGIN_DIR + "/" + plugin_
    dir_ = php_dirname(plugin_file_)
    plugin_files_ = Array(plugin_basename(plugin_file_))
    if php_is_dir(dir_) and WP_PLUGIN_DIR != dir_:
        #// 
        #// Filters the array of excluded directories and files while scanning the folder.
        #// 
        #// @since 4.9.0
        #// 
        #// @param string[] $exclusions Array of excluded directories and files.
        #//
        exclusions_ = apply_filters("plugin_files_exclusions", Array("CVS", "node_modules", "vendor", "bower_components"))
        list_files_ = list_files(dir_, 100, exclusions_)
        list_files_ = php_array_map("plugin_basename", list_files_)
        plugin_files_ = php_array_merge(plugin_files_, list_files_)
        plugin_files_ = php_array_values(array_unique(plugin_files_))
    # end if
    return plugin_files_
# end def get_plugin_files
#// 
#// Check the plugins directory and retrieve all plugin files with plugin data.
#// 
#// WordPress only supports plugin files in the base plugins directory
#// (wp-content/plugins) and in one directory above the plugins directory
#// (wp-content/plugins/my-plugin). The file it looks for has the plugin data
#// and must be found in those two locations. It is recommended to keep your
#// plugin files in their own directories.
#// 
#// The file with the plugin data is the file that will be included and therefore
#// needs to have the main execution for the plugin. This does not mean
#// everything must be contained in the file and it is recommended that the file
#// be split for maintainability. Keep everything in one file for extreme
#// optimization purposes.
#// 
#// @since 1.5.0
#// 
#// @param string $plugin_folder Optional. Relative path to single plugin folder.
#// @return array[] Array of arrays of plugin data, keyed by plugin file name. See `get_plugin_data()`.
#//
def get_plugins(plugin_folder_="", *_args_):
    
    
    cache_plugins_ = wp_cache_get("plugins", "plugins")
    if (not cache_plugins_):
        cache_plugins_ = Array()
    # end if
    if (php_isset(lambda : cache_plugins_[plugin_folder_])):
        return cache_plugins_[plugin_folder_]
    # end if
    wp_plugins_ = Array()
    plugin_root_ = WP_PLUGIN_DIR
    if (not php_empty(lambda : plugin_folder_)):
        plugin_root_ += plugin_folder_
    # end if
    #// Files in wp-content/plugins directory.
    plugins_dir_ = php_no_error(lambda: php_opendir(plugin_root_))
    plugin_files_ = Array()
    if plugins_dir_:
        while True:
            file_ = php_readdir(plugins_dir_)
            if not (file_ != False):
                break
            # end if
            if php_substr(file_, 0, 1) == ".":
                continue
            # end if
            if php_is_dir(plugin_root_ + "/" + file_):
                plugins_subdir_ = php_no_error(lambda: php_opendir(plugin_root_ + "/" + file_))
                if plugins_subdir_:
                    while True:
                        subfile_ = php_readdir(plugins_subdir_)
                        if not (subfile_ != False):
                            break
                        # end if
                        if php_substr(subfile_, 0, 1) == ".":
                            continue
                        # end if
                        if php_substr(subfile_, -4) == ".php":
                            plugin_files_[-1] = str(file_) + str("/") + str(subfile_)
                        # end if
                    # end while
                    php_closedir(plugins_subdir_)
                # end if
            else:
                if php_substr(file_, -4) == ".php":
                    plugin_files_[-1] = file_
                # end if
            # end if
        # end while
        php_closedir(plugins_dir_)
    # end if
    if php_empty(lambda : plugin_files_):
        return wp_plugins_
    # end if
    for plugin_file_ in plugin_files_:
        if (not php_is_readable(str(plugin_root_) + str("/") + str(plugin_file_))):
            continue
        # end if
        #// Do not apply markup/translate as it will be cached.
        plugin_data_ = get_plugin_data(str(plugin_root_) + str("/") + str(plugin_file_), False, False)
        if php_empty(lambda : plugin_data_["Name"]):
            continue
        # end if
        wp_plugins_[plugin_basename(plugin_file_)] = plugin_data_
    # end for
    uasort(wp_plugins_, "_sort_uname_callback")
    cache_plugins_[plugin_folder_] = wp_plugins_
    wp_cache_set("plugins", cache_plugins_, "plugins")
    return wp_plugins_
# end def get_plugins
#// 
#// Check the mu-plugins directory and retrieve all mu-plugin files with any plugin data.
#// 
#// WordPress only includes mu-plugin files in the base mu-plugins directory (wp-content/mu-plugins).
#// 
#// @since 3.0.0
#// @return array[] Array of arrays of mu-plugin data, keyed by plugin file name. See `get_plugin_data()`.
#//
def get_mu_plugins(*_args_):
    
    
    wp_plugins_ = Array()
    plugin_files_ = Array()
    if (not php_is_dir(WPMU_PLUGIN_DIR)):
        return wp_plugins_
    # end if
    #// Files in wp-content/mu-plugins directory.
    plugins_dir_ = php_no_error(lambda: php_opendir(WPMU_PLUGIN_DIR))
    if plugins_dir_:
        while True:
            file_ = php_readdir(plugins_dir_)
            if not (file_ != False):
                break
            # end if
            if php_substr(file_, -4) == ".php":
                plugin_files_[-1] = file_
            # end if
        # end while
    else:
        return wp_plugins_
    # end if
    php_closedir(plugins_dir_)
    if php_empty(lambda : plugin_files_):
        return wp_plugins_
    # end if
    for plugin_file_ in plugin_files_:
        if (not php_is_readable(WPMU_PLUGIN_DIR + str("/") + str(plugin_file_))):
            continue
        # end if
        #// Do not apply markup/translate as it will be cached.
        plugin_data_ = get_plugin_data(WPMU_PLUGIN_DIR + str("/") + str(plugin_file_), False, False)
        if php_empty(lambda : plugin_data_["Name"]):
            plugin_data_["Name"] = plugin_file_
        # end if
        wp_plugins_[plugin_file_] = plugin_data_
    # end for
    if (php_isset(lambda : wp_plugins_["index.php"])) and filesize(WPMU_PLUGIN_DIR + "/index.php") <= 30:
        wp_plugins_["index.php"] = None
    # end if
    uasort(wp_plugins_, "_sort_uname_callback")
    return wp_plugins_
# end def get_mu_plugins
#// 
#// Callback to sort array by a 'Name' key.
#// 
#// @since 3.1.0
#// 
#// @access private
#// 
#// @param array $a array with 'Name' key.
#// @param array $b array with 'Name' key.
#// @return int Return 0 or 1 based on two string comparison.
#//
def _sort_uname_callback(a_=None, b_=None, *_args_):
    
    
    return strnatcasecmp(a_["Name"], b_["Name"])
# end def _sort_uname_callback
#// 
#// Check the wp-content directory and retrieve all drop-ins with any plugin data.
#// 
#// @since 3.0.0
#// @return array[] Array of arrays of dropin plugin data, keyed by plugin file name. See `get_plugin_data()`.
#//
def get_dropins(*_args_):
    
    
    dropins_ = Array()
    plugin_files_ = Array()
    _dropins_ = _get_dropins()
    #// Files in wp-content directory.
    plugins_dir_ = php_no_error(lambda: php_opendir(WP_CONTENT_DIR))
    if plugins_dir_:
        while True:
            file_ = php_readdir(plugins_dir_)
            if not (file_ != False):
                break
            # end if
            if (php_isset(lambda : _dropins_[file_])):
                plugin_files_[-1] = file_
            # end if
        # end while
    else:
        return dropins_
    # end if
    php_closedir(plugins_dir_)
    if php_empty(lambda : plugin_files_):
        return dropins_
    # end if
    for plugin_file_ in plugin_files_:
        if (not php_is_readable(WP_CONTENT_DIR + str("/") + str(plugin_file_))):
            continue
        # end if
        #// Do not apply markup/translate as it will be cached.
        plugin_data_ = get_plugin_data(WP_CONTENT_DIR + str("/") + str(plugin_file_), False, False)
        if php_empty(lambda : plugin_data_["Name"]):
            plugin_data_["Name"] = plugin_file_
        # end if
        dropins_[plugin_file_] = plugin_data_
    # end for
    uksort(dropins_, "strnatcasecmp")
    return dropins_
# end def get_dropins
#// 
#// Returns drop-ins that WordPress uses.
#// 
#// Includes Multisite drop-ins only when is_multisite()
#// 
#// @since 3.0.0
#// @return array[] Key is file name. The value is an array, with the first value the
#// purpose of the drop-in and the second value the name of the constant that must be
#// true for the drop-in to be used, or true if no constant is required.
#//
def _get_dropins(*_args_):
    
    
    dropins_ = Array({"advanced-cache.php": Array(__("Advanced caching plugin."), "WP_CACHE"), "db.php": Array(__("Custom database class."), True), "db-error.php": Array(__("Custom database error message."), True), "install.php": Array(__("Custom installation script."), True), "maintenance.php": Array(__("Custom maintenance message."), True), "object-cache.php": Array(__("External object cache."), True), "php-error.php": Array(__("Custom PHP error message."), True), "fatal-error-handler.php": Array(__("Custom PHP fatal error handler."), True)})
    if is_multisite():
        dropins_["sunrise.php"] = Array(__("Executed before Multisite is loaded."), "SUNRISE")
        #// SUNRISE
        dropins_["blog-deleted.php"] = Array(__("Custom site deleted message."), True)
        #// Auto on deleted blog.
        dropins_["blog-inactive.php"] = Array(__("Custom site inactive message."), True)
        #// Auto on inactive blog.
        dropins_["blog-suspended.php"] = Array(__("Custom site suspended message."), True)
        pass
    # end if
    return dropins_
# end def _get_dropins
#// 
#// Determines whether a plugin is active.
#// 
#// Only plugins installed in the plugins/ folder can be active.
#// 
#// Plugins in the mu-plugins/ folder can't be "activated," so this function will
#// return false for those plugins.
#// 
#// For more information on this and similar theme functions, check out
#// the {@link https://developer.wordpress.org/themes/basics/conditional-tags
#// Conditional Tags} article in the Theme Developer Handbook.
#// 
#// @since 2.5.0
#// 
#// @param string $plugin Path to the plugin file relative to the plugins directory.
#// @return bool True, if in the active plugins list. False, not in the list.
#//
def is_plugin_active(plugin_=None, *_args_):
    
    
    return php_in_array(plugin_, get_option("active_plugins", Array())) or is_plugin_active_for_network(plugin_)
# end def is_plugin_active
#// 
#// Determines whether the plugin is inactive.
#// 
#// Reverse of is_plugin_active(). Used as a callback.
#// 
#// For more information on this and similar theme functions, check out
#// the {@link https://developer.wordpress.org/themes/basics/conditional-tags
#// Conditional Tags} article in the Theme Developer Handbook.
#// 
#// @since 3.1.0
#// @see is_plugin_active()
#// 
#// @param string $plugin Path to the plugin file relative to the plugins directory.
#// @return bool True if inactive. False if active.
#//
def is_plugin_inactive(plugin_=None, *_args_):
    
    
    return (not is_plugin_active(plugin_))
# end def is_plugin_inactive
#// 
#// Determines whether the plugin is active for the entire network.
#// 
#// Only plugins installed in the plugins/ folder can be active.
#// 
#// Plugins in the mu-plugins/ folder can't be "activated," so this function will
#// return false for those plugins.
#// 
#// For more information on this and similar theme functions, check out
#// the {@link https://developer.wordpress.org/themes/basics/conditional-tags
#// Conditional Tags} article in the Theme Developer Handbook.
#// 
#// @since 3.0.0
#// 
#// @param string $plugin Path to the plugin file relative to the plugins directory.
#// @return bool True if active for the network, otherwise false.
#//
def is_plugin_active_for_network(plugin_=None, *_args_):
    
    
    if (not is_multisite()):
        return False
    # end if
    plugins_ = get_site_option("active_sitewide_plugins")
    if (php_isset(lambda : plugins_[plugin_])):
        return True
    # end if
    return False
# end def is_plugin_active_for_network
#// 
#// Checks for "Network: true" in the plugin header to see if this should
#// be activated only as a network wide plugin. The plugin would also work
#// when Multisite is not enabled.
#// 
#// Checks for "Site Wide Only: true" for backward compatibility.
#// 
#// @since 3.0.0
#// 
#// @param string $plugin Path to the plugin file relative to the plugins directory.
#// @return bool True if plugin is network only, false otherwise.
#//
def is_network_only_plugin(plugin_=None, *_args_):
    
    
    plugin_data_ = get_plugin_data(WP_PLUGIN_DIR + "/" + plugin_)
    if plugin_data_:
        return plugin_data_["Network"]
    # end if
    return False
# end def is_network_only_plugin
#// 
#// Attempts activation of plugin in a "sandbox" and redirects on success.
#// 
#// A plugin that is already activated will not attempt to be activated again.
#// 
#// The way it works is by setting the redirection to the error before trying to
#// include the plugin file. If the plugin fails, then the redirection will not
#// be overwritten with the success message. Also, the options will not be
#// updated and the activation hook will not be called on plugin error.
#// 
#// It should be noted that in no way the below code will actually prevent errors
#// within the file. The code should not be used elsewhere to replicate the
#// "sandbox", which uses redirection to work.
#// {@source 13 1}
#// 
#// If any errors are found or text is outputted, then it will be captured to
#// ensure that the success redirection will update the error redirection.
#// 
#// @since 2.5.0
#// @since 5.2.0 Test for WordPress version and PHP version compatibility.
#// 
#// @param string $plugin       Path to the plugin file relative to the plugins directory.
#// @param string $redirect     Optional. URL to redirect to.
#// @param bool   $network_wide Optional. Whether to enable the plugin for all sites in the network
#// or just the current site. Multisite only. Default false.
#// @param bool   $silent       Optional. Whether to prevent calling activation hooks. Default false.
#// @return null|WP_Error Null on success, WP_Error on invalid file.
#//
def activate_plugin(plugin_=None, redirect_="", network_wide_=None, silent_=None, *_args_):
    if network_wide_ is None:
        network_wide_ = False
    # end if
    if silent_ is None:
        silent_ = False
    # end if
    global PHP_REQUEST
    plugin_ = plugin_basename(php_trim(plugin_))
    if is_multisite() and network_wide_ or is_network_only_plugin(plugin_):
        network_wide_ = True
        current_ = get_site_option("active_sitewide_plugins", Array())
        PHP_REQUEST["networkwide"] = 1
        pass
    else:
        current_ = get_option("active_plugins", Array())
    # end if
    valid_ = validate_plugin(plugin_)
    if is_wp_error(valid_):
        return valid_
    # end if
    requirements_ = validate_plugin_requirements(plugin_)
    if is_wp_error(requirements_):
        return requirements_
    # end if
    if network_wide_ and (not (php_isset(lambda : current_[plugin_]))) or (not network_wide_) and (not php_in_array(plugin_, current_)):
        if (not php_empty(lambda : redirect_)):
            #// We'll override this later if the plugin can be included without fatal error.
            wp_redirect(add_query_arg("_error_nonce", wp_create_nonce("plugin-activation-error_" + plugin_), redirect_))
        # end if
        ob_start()
        wp_register_plugin_realpath(WP_PLUGIN_DIR + "/" + plugin_)
        _wp_plugin_file_ = plugin_
        if (not php_defined("WP_SANDBOX_SCRAPING")):
            php_define("WP_SANDBOX_SCRAPING", True)
        # end if
        php_include_file(WP_PLUGIN_DIR + "/" + plugin_, once=False)
        plugin_ = _wp_plugin_file_
        #// Avoid stomping of the $plugin variable in a plugin.
        if (not silent_):
            #// 
            #// Fires before a plugin is activated.
            #// 
            #// If a plugin is silently activated (such as during an update),
            #// this hook does not fire.
            #// 
            #// @since 2.9.0
            #// 
            #// @param string $plugin       Path to the plugin file relative to the plugins directory.
            #// @param bool   $network_wide Whether to enable the plugin for all sites in the network
            #// or just the current site. Multisite only. Default is false.
            #//
            do_action("activate_plugin", plugin_, network_wide_)
            #// 
            #// Fires as a specific plugin is being activated.
            #// 
            #// This hook is the "activation" hook used internally by register_activation_hook().
            #// The dynamic portion of the hook name, `$plugin`, refers to the plugin basename.
            #// 
            #// If a plugin is silently activated (such as during an update), this hook does not fire.
            #// 
            #// @since 2.0.0
            #// 
            #// @param bool $network_wide Whether to enable the plugin for all sites in the network
            #// or just the current site. Multisite only. Default is false.
            #//
            do_action(str("activate_") + str(plugin_), network_wide_)
        # end if
        if network_wide_:
            current_ = get_site_option("active_sitewide_plugins", Array())
            current_[plugin_] = time()
            update_site_option("active_sitewide_plugins", current_)
        else:
            current_ = get_option("active_plugins", Array())
            current_[-1] = plugin_
            sort(current_)
            update_option("active_plugins", current_)
        # end if
        if (not silent_):
            #// 
            #// Fires after a plugin has been activated.
            #// 
            #// If a plugin is silently activated (such as during an update),
            #// this hook does not fire.
            #// 
            #// @since 2.9.0
            #// 
            #// @param string $plugin       Path to the plugin file relative to the plugins directory.
            #// @param bool   $network_wide Whether to enable the plugin for all sites in the network
            #// or just the current site. Multisite only. Default is false.
            #//
            do_action("activated_plugin", plugin_, network_wide_)
        # end if
        if ob_get_length() > 0:
            output_ = ob_get_clean()
            return php_new_class("WP_Error", lambda : WP_Error("unexpected_output", __("The plugin generated unexpected output."), output_))
        # end if
        ob_end_clean()
    # end if
    return None
# end def activate_plugin
#// 
#// Deactivate a single plugin or multiple plugins.
#// 
#// The deactivation hook is disabled by the plugin upgrader by using the $silent
#// parameter.
#// 
#// @since 2.5.0
#// 
#// @param string|string[] $plugins      Single plugin or list of plugins to deactivate.
#// @param bool            $silent       Prevent calling deactivation hooks. Default false.
#// @param bool|null       $network_wide Whether to deactivate the plugin for all sites in the network.
#// A value of null will deactivate plugins for both the network
#// and the current site. Multisite only. Default null.
#//
def deactivate_plugins(plugins_=None, silent_=None, network_wide_=None, *_args_):
    if silent_ is None:
        silent_ = False
    # end if
    if network_wide_ is None:
        network_wide_ = None
    # end if
    
    if is_multisite():
        network_current_ = get_site_option("active_sitewide_plugins", Array())
    # end if
    current_ = get_option("active_plugins", Array())
    do_blog_ = False
    do_network_ = False
    for plugin_ in plugins_:
        plugin_ = plugin_basename(php_trim(plugin_))
        if (not is_plugin_active(plugin_)):
            continue
        # end if
        network_deactivating_ = False != network_wide_ and is_plugin_active_for_network(plugin_)
        if (not silent_):
            #// 
            #// Fires before a plugin is deactivated.
            #// 
            #// If a plugin is silently deactivated (such as during an update),
            #// this hook does not fire.
            #// 
            #// @since 2.9.0
            #// 
            #// @param string $plugin               Path to the plugin file relative to the plugins directory.
            #// @param bool   $network_deactivating Whether the plugin is deactivated for all sites in the network
            #// or just the current site. Multisite only. Default false.
            #//
            do_action("deactivate_plugin", plugin_, network_deactivating_)
        # end if
        if False != network_wide_:
            if is_plugin_active_for_network(plugin_):
                do_network_ = True
                network_current_[plugin_] = None
            elif network_wide_:
                continue
            # end if
        # end if
        if True != network_wide_:
            key_ = php_array_search(plugin_, current_)
            if False != key_:
                do_blog_ = True
                current_[key_] = None
            # end if
        # end if
        if do_blog_ and wp_is_recovery_mode():
            extension_ = php_explode("/", plugin_)
            wp_paused_plugins().delete(extension_)
        # end if
        if (not silent_):
            #// 
            #// Fires as a specific plugin is being deactivated.
            #// 
            #// This hook is the "deactivation" hook used internally by register_deactivation_hook().
            #// The dynamic portion of the hook name, `$plugin`, refers to the plugin basename.
            #// 
            #// If a plugin is silently deactivated (such as during an update), this hook does not fire.
            #// 
            #// @since 2.0.0
            #// 
            #// @param bool $network_deactivating Whether the plugin is deactivated for all sites in the network
            #// or just the current site. Multisite only. Default false.
            #//
            do_action(str("deactivate_") + str(plugin_), network_deactivating_)
            #// 
            #// Fires after a plugin is deactivated.
            #// 
            #// If a plugin is silently deactivated (such as during an update),
            #// this hook does not fire.
            #// 
            #// @since 2.9.0
            #// 
            #// @param string $plugin               Path to the plugin file relative to the plugins directory.
            #// @param bool   $network_deactivating Whether the plugin is deactivated for all sites in the network
            #// or just the current site. Multisite only. Default false.
            #//
            do_action("deactivated_plugin", plugin_, network_deactivating_)
        # end if
    # end for
    if do_blog_:
        update_option("active_plugins", current_)
    # end if
    if do_network_:
        update_site_option("active_sitewide_plugins", network_current_)
    # end if
# end def deactivate_plugins
#// 
#// Activate multiple plugins.
#// 
#// When WP_Error is returned, it does not mean that one of the plugins had
#// errors. It means that one or more of the plugin file paths were invalid.
#// 
#// The execution will be halted as soon as one of the plugins has an error.
#// 
#// @since 2.6.0
#// 
#// @param string|string[] $plugins      Single plugin or list of plugins to activate.
#// @param string          $redirect     Redirect to page after successful activation.
#// @param bool            $network_wide Whether to enable the plugin for all sites in the network.
#// Default false.
#// @param bool $silent                  Prevent calling activation hooks. Default false.
#// @return bool|WP_Error True when finished or WP_Error if there were errors during a plugin activation.
#//
def activate_plugins(plugins_=None, redirect_="", network_wide_=None, silent_=None, *_args_):
    if network_wide_ is None:
        network_wide_ = False
    # end if
    if silent_ is None:
        silent_ = False
    # end if
    
    if (not php_is_array(plugins_)):
        plugins_ = Array(plugins_)
    # end if
    errors_ = Array()
    for plugin_ in plugins_:
        if (not php_empty(lambda : redirect_)):
            redirect_ = add_query_arg("plugin", plugin_, redirect_)
        # end if
        result_ = activate_plugin(plugin_, redirect_, network_wide_, silent_)
        if is_wp_error(result_):
            errors_[plugin_] = result_
        # end if
    # end for
    if (not php_empty(lambda : errors_)):
        return php_new_class("WP_Error", lambda : WP_Error("plugins_invalid", __("One of the plugins is invalid."), errors_))
    # end if
    return True
# end def activate_plugins
#// 
#// Remove directory and files of a plugin for a list of plugins.
#// 
#// @since 2.6.0
#// 
#// @global WP_Filesystem_Base $wp_filesystem WordPress filesystem subclass.
#// 
#// @param string[] $plugins    List of plugin paths to delete, relative to the plugins directory.
#// @param string   $deprecated Not used.
#// @return bool|null|WP_Error True on success, false if `$plugins` is empty, `WP_Error` on failure.
#// `null` if filesystem credentials are required to proceed.
#//
def delete_plugins(plugins_=None, deprecated_="", *_args_):
    
    
    global wp_filesystem_
    php_check_if_defined("wp_filesystem_")
    if php_empty(lambda : plugins_):
        return False
    # end if
    checked_ = Array()
    for plugin_ in plugins_:
        checked_[-1] = "checked[]=" + plugin_
    # end for
    url_ = wp_nonce_url("plugins.php?action=delete-selected&verify-delete=1&" + php_implode("&", checked_), "bulk-plugins")
    ob_start()
    credentials_ = request_filesystem_credentials(url_)
    data_ = ob_get_clean()
    if False == credentials_:
        if (not php_empty(lambda : data_)):
            php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
            php_print(data_)
            php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
            php_exit(0)
        # end if
        return
    # end if
    if (not WP_Filesystem(credentials_)):
        ob_start()
        #// Failed to connect. Error and request again.
        request_filesystem_credentials(url_, "", True)
        data_ = ob_get_clean()
        if (not php_empty(lambda : data_)):
            php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
            php_print(data_)
            php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
            php_exit(0)
        # end if
        return
    # end if
    if (not php_is_object(wp_filesystem_)):
        return php_new_class("WP_Error", lambda : WP_Error("fs_unavailable", __("Could not access filesystem.")))
    # end if
    if is_wp_error(wp_filesystem_.errors) and wp_filesystem_.errors.has_errors():
        return php_new_class("WP_Error", lambda : WP_Error("fs_error", __("Filesystem error."), wp_filesystem_.errors))
    # end if
    #// Get the base plugin folder.
    plugins_dir_ = wp_filesystem_.wp_plugins_dir()
    if php_empty(lambda : plugins_dir_):
        return php_new_class("WP_Error", lambda : WP_Error("fs_no_plugins_dir", __("Unable to locate WordPress plugin directory.")))
    # end if
    plugins_dir_ = trailingslashit(plugins_dir_)
    plugin_translations_ = wp_get_installed_translations("plugins")
    errors_ = Array()
    for plugin_file_ in plugins_:
        #// Run Uninstall hook.
        if is_uninstallable_plugin(plugin_file_):
            uninstall_plugin(plugin_file_)
        # end if
        #// 
        #// Fires immediately before a plugin deletion attempt.
        #// 
        #// @since 4.4.0
        #// 
        #// @param string $plugin_file Path to the plugin file relative to the plugins directory.
        #//
        do_action("delete_plugin", plugin_file_)
        this_plugin_dir_ = trailingslashit(php_dirname(plugins_dir_ + plugin_file_))
        #// If plugin is in its own directory, recursively delete the directory.
        #// Base check on if plugin includes directory separator AND that it's not the root plugin folder.
        if php_strpos(plugin_file_, "/") and this_plugin_dir_ != plugins_dir_:
            deleted_ = wp_filesystem_.delete(this_plugin_dir_, True)
        else:
            deleted_ = wp_filesystem_.delete(plugins_dir_ + plugin_file_)
        # end if
        #// 
        #// Fires immediately after a plugin deletion attempt.
        #// 
        #// @since 4.4.0
        #// 
        #// @param string $plugin_file Path to the plugin file relative to the plugins directory.
        #// @param bool   $deleted     Whether the plugin deletion was successful.
        #//
        do_action("deleted_plugin", plugin_file_, deleted_)
        if (not deleted_):
            errors_[-1] = plugin_file_
            continue
        # end if
        #// Remove language files, silently.
        plugin_slug_ = php_dirname(plugin_file_)
        if "." != plugin_slug_ and (not php_empty(lambda : plugin_translations_[plugin_slug_])):
            translations_ = plugin_translations_[plugin_slug_]
            for translation_,data_ in translations_.items():
                wp_filesystem_.delete(WP_LANG_DIR + "/plugins/" + plugin_slug_ + "-" + translation_ + ".po")
                wp_filesystem_.delete(WP_LANG_DIR + "/plugins/" + plugin_slug_ + "-" + translation_ + ".mo")
                json_translation_files_ = glob(WP_LANG_DIR + "/plugins/" + plugin_slug_ + "-" + translation_ + "-*.json")
                if json_translation_files_:
                    php_array_map(Array(wp_filesystem_, "delete"), json_translation_files_)
                # end if
            # end for
        # end if
    # end for
    #// Remove deleted plugins from the plugin updates list.
    current_ = get_site_transient("update_plugins")
    if current_:
        #// Don't remove the plugins that weren't deleted.
        deleted_ = php_array_diff(plugins_, errors_)
        for plugin_file_ in deleted_:
            current_.response[plugin_file_] = None
        # end for
        set_site_transient("update_plugins", current_)
    # end if
    if (not php_empty(lambda : errors_)):
        if 1 == php_count(errors_):
            #// translators: %s: Plugin filename.
            message_ = __("Could not fully remove the plugin %s.")
        else:
            #// translators: %s: Comma-separated list of plugin filenames.
            message_ = __("Could not fully remove the plugins %s.")
        # end if
        return php_new_class("WP_Error", lambda : WP_Error("could_not_remove_plugin", php_sprintf(message_, php_implode(", ", errors_))))
    # end if
    return True
# end def delete_plugins
#// 
#// Validate active plugins
#// 
#// Validate all active plugins, deactivates invalid and
#// returns an array of deactivated ones.
#// 
#// @since 2.5.0
#// @return WP_Error[] Array of plugin errors keyed by plugin file name.
#//
def validate_active_plugins(*_args_):
    
    
    plugins_ = get_option("active_plugins", Array())
    #// Validate vartype: array.
    if (not php_is_array(plugins_)):
        update_option("active_plugins", Array())
        plugins_ = Array()
    # end if
    if is_multisite() and current_user_can("manage_network_plugins"):
        network_plugins_ = get_site_option("active_sitewide_plugins", Array())
        plugins_ = php_array_merge(plugins_, php_array_keys(network_plugins_))
    # end if
    if php_empty(lambda : plugins_):
        return Array()
    # end if
    invalid_ = Array()
    #// Invalid plugins get deactivated.
    for plugin_ in plugins_:
        result_ = validate_plugin(plugin_)
        if is_wp_error(result_):
            invalid_[plugin_] = result_
            deactivate_plugins(plugin_, True)
        # end if
    # end for
    return invalid_
# end def validate_active_plugins
#// 
#// Validate the plugin path.
#// 
#// Checks that the main plugin file exists and is a valid plugin. See validate_file().
#// 
#// @since 2.5.0
#// 
#// @param string $plugin Path to the plugin file relative to the plugins directory.
#// @return int|WP_Error 0 on success, WP_Error on failure.
#//
def validate_plugin(plugin_=None, *_args_):
    
    
    if validate_file(plugin_):
        return php_new_class("WP_Error", lambda : WP_Error("plugin_invalid", __("Invalid plugin path.")))
    # end if
    if (not php_file_exists(WP_PLUGIN_DIR + "/" + plugin_)):
        return php_new_class("WP_Error", lambda : WP_Error("plugin_not_found", __("Plugin file does not exist.")))
    # end if
    installed_plugins_ = get_plugins()
    if (not (php_isset(lambda : installed_plugins_[plugin_]))):
        return php_new_class("WP_Error", lambda : WP_Error("no_plugin_header", __("The plugin does not have a valid header.")))
    # end if
    return 0
# end def validate_plugin
#// 
#// Validate the plugin requirements for WP version and PHP version.
#// 
#// @since 5.2.0
#// 
#// @param string $plugin Path to the plugin file relative to the plugins directory.
#// @return true|WP_Error True if requirements are met, WP_Error on failure.
#//
def validate_plugin_requirements(plugin_=None, *_args_):
    
    
    readme_file_ = WP_PLUGIN_DIR + "/" + php_dirname(plugin_) + "/readme.txt"
    plugin_data_ = Array({"requires": "", "requires_php": ""})
    if php_file_exists(readme_file_):
        plugin_data_ = get_file_data(readme_file_, Array({"requires": "Requires at least", "requires_php": "Requires PHP"}), "plugin")
    # end if
    plugin_data_ = php_array_merge(plugin_data_, get_plugin_data(WP_PLUGIN_DIR + "/" + plugin_))
    #// Check for headers in the plugin's PHP file, give precedence to the plugin headers.
    plugin_data_["requires"] = plugin_data_["RequiresWP"] if (not php_empty(lambda : plugin_data_["RequiresWP"])) else plugin_data_["requires"]
    plugin_data_["requires_php"] = plugin_data_["RequiresPHP"] if (not php_empty(lambda : plugin_data_["RequiresPHP"])) else plugin_data_["requires_php"]
    plugin_data_["wp_compatible"] = is_wp_version_compatible(plugin_data_["requires"])
    plugin_data_["php_compatible"] = is_php_version_compatible(plugin_data_["requires_php"])
    if (not plugin_data_["wp_compatible"]) and (not plugin_data_["php_compatible"]):
        return php_new_class("WP_Error", lambda : WP_Error("plugin_wp_php_incompatible", php_sprintf(__("<strong>Error:</strong> Current WordPress and PHP versions do not meet minimum requirements for %s."), plugin_data_["Name"])))
    elif (not plugin_data_["php_compatible"]):
        return php_new_class("WP_Error", lambda : WP_Error("plugin_php_incompatible", php_sprintf(__("<strong>Error:</strong> Current PHP version does not meet minimum requirements for %s."), plugin_data_["Name"])))
    elif (not plugin_data_["wp_compatible"]):
        return php_new_class("WP_Error", lambda : WP_Error("plugin_wp_incompatible", php_sprintf(__("<strong>Error:</strong> Current WordPress version does not meet minimum requirements for %s."), plugin_data_["Name"])))
    # end if
    return True
# end def validate_plugin_requirements
#// 
#// Whether the plugin can be uninstalled.
#// 
#// @since 2.7.0
#// 
#// @param string $plugin Path to the plugin file relative to the plugins directory.
#// @return bool Whether plugin can be uninstalled.
#//
def is_uninstallable_plugin(plugin_=None, *_args_):
    
    
    file_ = plugin_basename(plugin_)
    uninstallable_plugins_ = get_option("uninstall_plugins")
    if (php_isset(lambda : uninstallable_plugins_[file_])) or php_file_exists(WP_PLUGIN_DIR + "/" + php_dirname(file_) + "/uninstall.php"):
        return True
    # end if
    return False
# end def is_uninstallable_plugin
#// 
#// Uninstall a single plugin.
#// 
#// Calls the uninstall hook, if it is available.
#// 
#// @since 2.7.0
#// 
#// @param string $plugin Path to the plugin file relative to the plugins directory.
#// @return true True if a plugin's uninstall.php file has been found and included.
#//
def uninstall_plugin(plugin_=None, *_args_):
    
    
    file_ = plugin_basename(plugin_)
    uninstallable_plugins_ = get_option("uninstall_plugins")
    #// 
    #// Fires in uninstall_plugin() immediately before the plugin is uninstalled.
    #// 
    #// @since 4.5.0
    #// 
    #// @param string $plugin                Path to the plugin file relative to the plugins directory.
    #// @param array  $uninstallable_plugins Uninstallable plugins.
    #//
    do_action("pre_uninstall_plugin", plugin_, uninstallable_plugins_)
    if php_file_exists(WP_PLUGIN_DIR + "/" + php_dirname(file_) + "/uninstall.php"):
        if (php_isset(lambda : uninstallable_plugins_[file_])):
            uninstallable_plugins_[file_] = None
            update_option("uninstall_plugins", uninstallable_plugins_)
        # end if
        uninstallable_plugins_ = None
        php_define("WP_UNINSTALL_PLUGIN", file_)
        wp_register_plugin_realpath(WP_PLUGIN_DIR + "/" + file_)
        php_include_file(WP_PLUGIN_DIR + "/" + php_dirname(file_) + "/uninstall.php", once=False)
        return True
    # end if
    if (php_isset(lambda : uninstallable_plugins_[file_])):
        callable_ = uninstallable_plugins_[file_]
        uninstallable_plugins_[file_] = None
        update_option("uninstall_plugins", uninstallable_plugins_)
        uninstallable_plugins_ = None
        wp_register_plugin_realpath(WP_PLUGIN_DIR + "/" + file_)
        php_include_file(WP_PLUGIN_DIR + "/" + file_, once=False)
        add_action(str("uninstall_") + str(file_), callable_)
        #// 
        #// Fires in uninstall_plugin() once the plugin has been uninstalled.
        #// 
        #// The action concatenates the 'uninstall_' prefix with the basename of the
        #// plugin passed to uninstall_plugin() to create a dynamically-named action.
        #// 
        #// @since 2.7.0
        #//
        do_action(str("uninstall_") + str(file_))
    # end if
# end def uninstall_plugin
#// 
#// Menu.
#// 
#// 
#// Add a top-level menu page.
#// 
#// This function takes a capability which will be used to determine whether
#// or not a page is included in the menu.
#// 
#// The function which is hooked in to handle the output of the page must check
#// that the user has the required capability as well.
#// 
#// @since 1.5.0
#// 
#// @global array $menu
#// @global array $admin_page_hooks
#// @global array $_registered_pages
#// @global array $_parent_pages
#// 
#// @param string   $page_title The text to be displayed in the title tags of the page when the menu is selected.
#// @param string   $menu_title The text to be used for the menu.
#// @param string   $capability The capability required for this menu to be displayed to the user.
#// @param string   $menu_slug  The slug name to refer to this menu by. Should be unique for this menu page and only
#// include lowercase alphanumeric, dashes, and underscores characters to be compatible
#// with sanitize_key().
#// @param callable $function   The function to be called to output the content for this page.
#// @param string   $icon_url   The URL to the icon to be used for this menu.
#// Pass a base64-encoded SVG using a data URI, which will be colored to match
#// the color scheme. This should begin with 'data:image/svg+xml;base64,'.
#// Pass the name of a Dashicons helper class to use a font icon,
#// e.g. 'dashicons-chart-pie'.
#// Pass 'none' to leave div.wp-menu-image empty so an icon can be added via CSS.
#// @param int      $position   The position in the menu order this item should appear.
#// @return string The resulting page's hook_suffix.
#//
def add_menu_page(page_title_=None, menu_title_=None, capability_=None, menu_slug_=None, function_="", icon_url_="", position_=None, *_args_):
    if position_ is None:
        position_ = None
    # end if
    
    global menu_
    global admin_page_hooks_
    global _registered_pages_
    global _parent_pages_
    php_check_if_defined("menu_","admin_page_hooks_","_registered_pages_","_parent_pages_")
    menu_slug_ = plugin_basename(menu_slug_)
    admin_page_hooks_[menu_slug_] = sanitize_title(menu_title_)
    hookname_ = get_plugin_page_hookname(menu_slug_, "")
    if (not php_empty(lambda : function_)) and (not php_empty(lambda : hookname_)) and current_user_can(capability_):
        add_action(hookname_, function_)
    # end if
    if php_empty(lambda : icon_url_):
        icon_url_ = "dashicons-admin-generic"
        icon_class_ = "menu-icon-generic "
    else:
        icon_url_ = set_url_scheme(icon_url_)
        icon_class_ = ""
    # end if
    new_menu_ = Array(menu_title_, capability_, menu_slug_, page_title_, "menu-top " + icon_class_ + hookname_, hookname_, icon_url_)
    if None == position_:
        menu_[-1] = new_menu_
    elif (php_isset(lambda : menu_[str(position_)])):
        position_ = position_ + php_substr(base_convert(php_md5(menu_slug_ + menu_title_), 16, 10), -5) * 1e-05
        menu_[str(position_)] = new_menu_
    else:
        menu_[position_] = new_menu_
    # end if
    _registered_pages_[hookname_] = True
    #// No parent as top level.
    _parent_pages_[menu_slug_] = False
    return hookname_
# end def add_menu_page
#// 
#// Add a submenu page.
#// 
#// This function takes a capability which will be used to determine whether
#// or not a page is included in the menu.
#// 
#// The function which is hooked in to handle the output of the page must check
#// that the user has the required capability as well.
#// 
#// @since 1.5.0
#// @since 5.3.0 Added the `$position` parameter.
#// 
#// @global array $submenu
#// @global array $menu
#// @global array $_wp_real_parent_file
#// @global bool  $_wp_submenu_nopriv
#// @global array $_registered_pages
#// @global array $_parent_pages
#// 
#// @param string   $parent_slug The slug name for the parent menu (or the file name of a standard
#// WordPress admin page).
#// @param string   $page_title  The text to be displayed in the title tags of the page when the menu
#// is selected.
#// @param string   $menu_title  The text to be used for the menu.
#// @param string   $capability  The capability required for this menu to be displayed to the user.
#// @param string   $menu_slug   The slug name to refer to this menu by. Should be unique for this menu
#// and only include lowercase alphanumeric, dashes, and underscores characters
#// to be compatible with sanitize_key().
#// @param callable $function    The function to be called to output the content for this page.
#// @param int      $position    The position in the menu order this item should appear.
#// @return string|false The resulting page's hook_suffix, or false if the user does not have the capability required.
#//
def add_submenu_page(parent_slug_=None, page_title_=None, menu_title_=None, capability_=None, menu_slug_=None, function_="", position_=None, *_args_):
    if position_ is None:
        position_ = None
    # end if
    
    global submenu_
    global menu_
    global _wp_real_parent_file_
    global _wp_submenu_nopriv_
    global _registered_pages_
    global _parent_pages_
    php_check_if_defined("submenu_","menu_","_wp_real_parent_file_","_wp_submenu_nopriv_","_registered_pages_","_parent_pages_")
    menu_slug_ = plugin_basename(menu_slug_)
    parent_slug_ = plugin_basename(parent_slug_)
    if (php_isset(lambda : _wp_real_parent_file_[parent_slug_])):
        parent_slug_ = _wp_real_parent_file_[parent_slug_]
    # end if
    if (not current_user_can(capability_)):
        _wp_submenu_nopriv_[parent_slug_][menu_slug_] = True
        return False
    # end if
    #// 
    #// If the parent doesn't already have a submenu, add a link to the parent
    #// as the first item in the submenu. If the submenu file is the same as the
    #// parent file someone is trying to link back to the parent manually. In
    #// this case, don't automatically add a link back to avoid duplication.
    #//
    if (not (php_isset(lambda : submenu_[parent_slug_]))) and menu_slug_ != parent_slug_:
        for parent_menu_ in menu_:
            if parent_menu_[2] == parent_slug_ and current_user_can(parent_menu_[1]):
                submenu_[parent_slug_][-1] = php_array_slice(parent_menu_, 0, 4)
            # end if
        # end for
    # end if
    new_sub_menu_ = Array(menu_title_, capability_, menu_slug_, page_title_)
    if (not php_is_int(position_)):
        if None != position_:
            _doing_it_wrong(__FUNCTION__, php_sprintf(__("The seventh parameter passed to %s should be an integer representing menu position."), "<code>add_submenu_page()</code>"), "5.3.0")
        # end if
        submenu_[parent_slug_][-1] = new_sub_menu_
    else:
        #// Append the submenu if the parent item is not present in the submenu,
        #// or if position is equal or higher than the number of items in the array.
        if (not (php_isset(lambda : submenu_[parent_slug_]))) or position_ >= php_count(submenu_[parent_slug_]):
            submenu_[parent_slug_][-1] = new_sub_menu_
        else:
            #// Test for a negative position.
            position_ = php_max(position_, 0)
            if 0 == position_:
                #// For negative or `0` positions, prepend the submenu.
                array_unshift(submenu_[parent_slug_], new_sub_menu_)
            else:
                #// Grab all of the items before the insertion point.
                before_items_ = php_array_slice(submenu_[parent_slug_], 0, position_, True)
                #// Grab all of the items after the insertion point.
                after_items_ = php_array_slice(submenu_[parent_slug_], position_, None, True)
                #// Add the new item.
                before_items_[-1] = new_sub_menu_
                #// Merge the items.
                submenu_[parent_slug_] = php_array_merge(before_items_, after_items_)
            # end if
        # end if
    # end if
    #// Sort the parent array.
    php_ksort(submenu_[parent_slug_])
    hookname_ = get_plugin_page_hookname(menu_slug_, parent_slug_)
    if (not php_empty(lambda : function_)) and (not php_empty(lambda : hookname_)):
        add_action(hookname_, function_)
    # end if
    _registered_pages_[hookname_] = True
    #// 
    #// Backward-compatibility for plugins using add_management_page().
    #// See wp-admin/admin.php for redirect from edit.php to tools.php.
    #//
    if "tools.php" == parent_slug_:
        _registered_pages_[get_plugin_page_hookname(menu_slug_, "edit.php")] = True
    # end if
    #// No parent as top level.
    _parent_pages_[menu_slug_] = parent_slug_
    return hookname_
# end def add_submenu_page
#// 
#// Add submenu page to the Tools main menu.
#// 
#// This function takes a capability which will be used to determine whether
#// or not a page is included in the menu.
#// 
#// The function which is hooked in to handle the output of the page must check
#// that the user has the required capability as well.
#// 
#// @since 1.5.0
#// @since 5.3.0 Added the `$position` parameter.
#// 
#// @param string   $page_title The text to be displayed in the title tags of the page when the menu is selected.
#// @param string   $menu_title The text to be used for the menu.
#// @param string   $capability The capability required for this menu to be displayed to the user.
#// @param string   $menu_slug  The slug name to refer to this menu by (should be unique for this menu).
#// @param callable $function   The function to be called to output the content for this page.
#// @param int      $position   The position in the menu order this item should appear.
#// @return string|false The resulting page's hook_suffix, or false if the user does not have the capability required.
#//
def add_management_page(page_title_=None, menu_title_=None, capability_=None, menu_slug_=None, function_="", position_=None, *_args_):
    if position_ is None:
        position_ = None
    # end if
    
    return add_submenu_page("tools.php", page_title_, menu_title_, capability_, menu_slug_, function_, position_)
# end def add_management_page
#// 
#// Add submenu page to the Settings main menu.
#// 
#// This function takes a capability which will be used to determine whether
#// or not a page is included in the menu.
#// 
#// The function which is hooked in to handle the output of the page must check
#// that the user has the required capability as well.
#// 
#// @since 1.5.0
#// @since 5.3.0 Added the `$position` parameter.
#// 
#// @param string   $page_title The text to be displayed in the title tags of the page when the menu is selected.
#// @param string   $menu_title The text to be used for the menu.
#// @param string   $capability The capability required for this menu to be displayed to the user.
#// @param string   $menu_slug  The slug name to refer to this menu by (should be unique for this menu).
#// @param callable $function   The function to be called to output the content for this page.
#// @param int      $position   The position in the menu order this item should appear.
#// @return string|false The resulting page's hook_suffix, or false if the user does not have the capability required.
#//
def add_options_page(page_title_=None, menu_title_=None, capability_=None, menu_slug_=None, function_="", position_=None, *_args_):
    if position_ is None:
        position_ = None
    # end if
    
    return add_submenu_page("options-general.php", page_title_, menu_title_, capability_, menu_slug_, function_, position_)
# end def add_options_page
#// 
#// Add submenu page to the Appearance main menu.
#// 
#// This function takes a capability which will be used to determine whether
#// or not a page is included in the menu.
#// 
#// The function which is hooked in to handle the output of the page must check
#// that the user has the required capability as well.
#// 
#// @since 2.0.0
#// @since 5.3.0 Added the `$position` parameter.
#// 
#// @param string   $page_title The text to be displayed in the title tags of the page when the menu is selected.
#// @param string   $menu_title The text to be used for the menu.
#// @param string   $capability The capability required for this menu to be displayed to the user.
#// @param string   $menu_slug  The slug name to refer to this menu by (should be unique for this menu).
#// @param callable $function   The function to be called to output the content for this page.
#// @param int      $position   The position in the menu order this item should appear.
#// @return string|false The resulting page's hook_suffix, or false if the user does not have the capability required.
#//
def add_theme_page(page_title_=None, menu_title_=None, capability_=None, menu_slug_=None, function_="", position_=None, *_args_):
    if position_ is None:
        position_ = None
    # end if
    
    return add_submenu_page("themes.php", page_title_, menu_title_, capability_, menu_slug_, function_, position_)
# end def add_theme_page
#// 
#// Add submenu page to the Plugins main menu.
#// 
#// This function takes a capability which will be used to determine whether
#// or not a page is included in the menu.
#// 
#// The function which is hooked in to handle the output of the page must check
#// that the user has the required capability as well.
#// 
#// @since 3.0.0
#// @since 5.3.0 Added the `$position` parameter.
#// 
#// @param string   $page_title The text to be displayed in the title tags of the page when the menu is selected.
#// @param string   $menu_title The text to be used for the menu.
#// @param string   $capability The capability required for this menu to be displayed to the user.
#// @param string   $menu_slug  The slug name to refer to this menu by (should be unique for this menu).
#// @param callable $function   The function to be called to output the content for this page.
#// @param int      $position   The position in the menu order this item should appear.
#// @return string|false The resulting page's hook_suffix, or false if the user does not have the capability required.
#//
def add_plugins_page(page_title_=None, menu_title_=None, capability_=None, menu_slug_=None, function_="", position_=None, *_args_):
    if position_ is None:
        position_ = None
    # end if
    
    return add_submenu_page("plugins.php", page_title_, menu_title_, capability_, menu_slug_, function_, position_)
# end def add_plugins_page
#// 
#// Add submenu page to the Users/Profile main menu.
#// 
#// This function takes a capability which will be used to determine whether
#// or not a page is included in the menu.
#// 
#// The function which is hooked in to handle the output of the page must check
#// that the user has the required capability as well.
#// 
#// @since 2.1.3
#// @since 5.3.0 Added the `$position` parameter.
#// 
#// @param string   $page_title The text to be displayed in the title tags of the page when the menu is selected.
#// @param string   $menu_title The text to be used for the menu.
#// @param string   $capability The capability required for this menu to be displayed to the user.
#// @param string   $menu_slug  The slug name to refer to this menu by (should be unique for this menu).
#// @param callable $function   The function to be called to output the content for this page.
#// @param int      $position   The position in the menu order this item should appear.
#// @return string|false The resulting page's hook_suffix, or false if the user does not have the capability required.
#//
def add_users_page(page_title_=None, menu_title_=None, capability_=None, menu_slug_=None, function_="", position_=None, *_args_):
    if position_ is None:
        position_ = None
    # end if
    
    if current_user_can("edit_users"):
        parent_ = "users.php"
    else:
        parent_ = "profile.php"
    # end if
    return add_submenu_page(parent_, page_title_, menu_title_, capability_, menu_slug_, function_, position_)
# end def add_users_page
#// 
#// Add submenu page to the Dashboard main menu.
#// 
#// This function takes a capability which will be used to determine whether
#// or not a page is included in the menu.
#// 
#// The function which is hooked in to handle the output of the page must check
#// that the user has the required capability as well.
#// 
#// @since 2.7.0
#// @since 5.3.0 Added the `$position` parameter.
#// 
#// @param string   $page_title The text to be displayed in the title tags of the page when the menu is selected.
#// @param string   $menu_title The text to be used for the menu.
#// @param string   $capability The capability required for this menu to be displayed to the user.
#// @param string   $menu_slug  The slug name to refer to this menu by (should be unique for this menu).
#// @param callable $function   The function to be called to output the content for this page.
#// @param int      $position   The position in the menu order this item should appear.
#// @return string|false The resulting page's hook_suffix, or false if the user does not have the capability required.
#//
def add_dashboard_page(page_title_=None, menu_title_=None, capability_=None, menu_slug_=None, function_="", position_=None, *_args_):
    if position_ is None:
        position_ = None
    # end if
    
    return add_submenu_page("index.php", page_title_, menu_title_, capability_, menu_slug_, function_, position_)
# end def add_dashboard_page
#// 
#// Add submenu page to the Posts main menu.
#// 
#// This function takes a capability which will be used to determine whether
#// or not a page is included in the menu.
#// 
#// The function which is hooked in to handle the output of the page must check
#// that the user has the required capability as well.
#// 
#// @since 2.7.0
#// @since 5.3.0 Added the `$position` parameter.
#// 
#// @param string   $page_title The text to be displayed in the title tags of the page when the menu is selected.
#// @param string   $menu_title The text to be used for the menu.
#// @param string   $capability The capability required for this menu to be displayed to the user.
#// @param string   $menu_slug  The slug name to refer to this menu by (should be unique for this menu).
#// @param callable $function   The function to be called to output the content for this page.
#// @param int      $position   The position in the menu order this item should appear.
#// @return string|false The resulting page's hook_suffix, or false if the user does not have the capability required.
#//
def add_posts_page(page_title_=None, menu_title_=None, capability_=None, menu_slug_=None, function_="", position_=None, *_args_):
    if position_ is None:
        position_ = None
    # end if
    
    return add_submenu_page("edit.php", page_title_, menu_title_, capability_, menu_slug_, function_, position_)
# end def add_posts_page
#// 
#// Add submenu page to the Media main menu.
#// 
#// This function takes a capability which will be used to determine whether
#// or not a page is included in the menu.
#// 
#// The function which is hooked in to handle the output of the page must check
#// that the user has the required capability as well.
#// 
#// @since 2.7.0
#// @since 5.3.0 Added the `$position` parameter.
#// 
#// @param string   $page_title The text to be displayed in the title tags of the page when the menu is selected.
#// @param string   $menu_title The text to be used for the menu.
#// @param string   $capability The capability required for this menu to be displayed to the user.
#// @param string   $menu_slug  The slug name to refer to this menu by (should be unique for this menu).
#// @param callable $function   The function to be called to output the content for this page.
#// @param int      $position   The position in the menu order this item should appear.
#// @return string|false The resulting page's hook_suffix, or false if the user does not have the capability required.
#//
def add_media_page(page_title_=None, menu_title_=None, capability_=None, menu_slug_=None, function_="", position_=None, *_args_):
    if position_ is None:
        position_ = None
    # end if
    
    return add_submenu_page("upload.php", page_title_, menu_title_, capability_, menu_slug_, function_, position_)
# end def add_media_page
#// 
#// Add submenu page to the Links main menu.
#// 
#// This function takes a capability which will be used to determine whether
#// or not a page is included in the menu.
#// 
#// The function which is hooked in to handle the output of the page must check
#// that the user has the required capability as well.
#// 
#// @since 2.7.0
#// @since 5.3.0 Added the `$position` parameter.
#// 
#// @param string   $page_title The text to be displayed in the title tags of the page when the menu is selected.
#// @param string   $menu_title The text to be used for the menu.
#// @param string   $capability The capability required for this menu to be displayed to the user.
#// @param string   $menu_slug  The slug name to refer to this menu by (should be unique for this menu).
#// @param callable $function   The function to be called to output the content for this page.
#// @param int      $position   The position in the menu order this item should appear.
#// @return string|false The resulting page's hook_suffix, or false if the user does not have the capability required.
#//
def add_links_page(page_title_=None, menu_title_=None, capability_=None, menu_slug_=None, function_="", position_=None, *_args_):
    if position_ is None:
        position_ = None
    # end if
    
    return add_submenu_page("link-manager.php", page_title_, menu_title_, capability_, menu_slug_, function_, position_)
# end def add_links_page
#// 
#// Add submenu page to the Pages main menu.
#// 
#// This function takes a capability which will be used to determine whether
#// or not a page is included in the menu.
#// 
#// The function which is hooked in to handle the output of the page must check
#// that the user has the required capability as well.
#// 
#// @since 2.7.0
#// @since 5.3.0 Added the `$position` parameter.
#// 
#// @param string   $page_title The text to be displayed in the title tags of the page when the menu is selected.
#// @param string   $menu_title The text to be used for the menu.
#// @param string   $capability The capability required for this menu to be displayed to the user.
#// @param string   $menu_slug  The slug name to refer to this menu by (should be unique for this menu).
#// @param callable $function   The function to be called to output the content for this page.
#// @param int      $position   The position in the menu order this item should appear.
#// @return string|false The resulting page's hook_suffix, or false if the user does not have the capability required.
#//
def add_pages_page(page_title_=None, menu_title_=None, capability_=None, menu_slug_=None, function_="", position_=None, *_args_):
    if position_ is None:
        position_ = None
    # end if
    
    return add_submenu_page("edit.php?post_type=page", page_title_, menu_title_, capability_, menu_slug_, function_, position_)
# end def add_pages_page
#// 
#// Add submenu page to the Comments main menu.
#// 
#// This function takes a capability which will be used to determine whether
#// or not a page is included in the menu.
#// 
#// The function which is hooked in to handle the output of the page must check
#// that the user has the required capability as well.
#// 
#// @since 2.7.0
#// @since 5.3.0 Added the `$position` parameter.
#// 
#// @param string   $page_title The text to be displayed in the title tags of the page when the menu is selected.
#// @param string   $menu_title The text to be used for the menu.
#// @param string   $capability The capability required for this menu to be displayed to the user.
#// @param string   $menu_slug  The slug name to refer to this menu by (should be unique for this menu).
#// @param callable $function   The function to be called to output the content for this page.
#// @param int      $position   The position in the menu order this item should appear.
#// @return string|false The resulting page's hook_suffix, or false if the user does not have the capability required.
#//
def add_comments_page(page_title_=None, menu_title_=None, capability_=None, menu_slug_=None, function_="", position_=None, *_args_):
    if position_ is None:
        position_ = None
    # end if
    
    return add_submenu_page("edit-comments.php", page_title_, menu_title_, capability_, menu_slug_, function_, position_)
# end def add_comments_page
#// 
#// Remove a top-level admin menu.
#// 
#// @since 3.1.0
#// 
#// @global array $menu
#// 
#// @param string $menu_slug The slug of the menu.
#// @return array|bool The removed menu on success, false if not found.
#//
def remove_menu_page(menu_slug_=None, *_args_):
    
    
    global menu_
    php_check_if_defined("menu_")
    for i_,item_ in menu_.items():
        if menu_slug_ == item_[2]:
            menu_[i_] = None
            return item_
        # end if
    # end for
    return False
# end def remove_menu_page
#// 
#// Remove an admin submenu.
#// 
#// @since 3.1.0
#// 
#// @global array $submenu
#// 
#// @param string $menu_slug    The slug for the parent menu.
#// @param string $submenu_slug The slug of the submenu.
#// @return array|bool The removed submenu on success, false if not found.
#//
def remove_submenu_page(menu_slug_=None, submenu_slug_=None, *_args_):
    
    
    global submenu_
    php_check_if_defined("submenu_")
    if (not (php_isset(lambda : submenu_[menu_slug_]))):
        return False
    # end if
    for i_,item_ in submenu_[menu_slug_].items():
        if submenu_slug_ == item_[2]:
            submenu_[menu_slug_][i_] = None
            return item_
        # end if
    # end for
    return False
# end def remove_submenu_page
#// 
#// Get the URL to access a particular menu page based on the slug it was registered with.
#// 
#// If the slug hasn't been registered properly, no URL will be returned.
#// 
#// @since 3.0.0
#// 
#// @global array $_parent_pages
#// 
#// @param string $menu_slug The slug name to refer to this menu by (should be unique for this menu).
#// @param bool   $echo      Whether or not to echo the URL. Default true.
#// @return string The menu page URL.
#//
def menu_page_url(menu_slug_=None, echo_=None, *_args_):
    if echo_ is None:
        echo_ = True
    # end if
    
    global _parent_pages_
    php_check_if_defined("_parent_pages_")
    if (php_isset(lambda : _parent_pages_[menu_slug_])):
        parent_slug_ = _parent_pages_[menu_slug_]
        if parent_slug_ and (not (php_isset(lambda : _parent_pages_[parent_slug_]))):
            url_ = admin_url(add_query_arg("page", menu_slug_, parent_slug_))
        else:
            url_ = admin_url("admin.php?page=" + menu_slug_)
        # end if
    else:
        url_ = ""
    # end if
    url_ = esc_url(url_)
    if echo_:
        php_print(url_)
    # end if
    return url_
# end def menu_page_url
#// 
#// Pluggable Menu Support -- Private.
#// 
#// 
#// Gets the parent file of the current admin page.
#// 
#// @since 1.5.0
#// 
#// @global string $parent_file
#// @global array $menu
#// @global array $submenu
#// @global string $pagenow
#// @global string $typenow
#// @global string $plugin_page
#// @global array $_wp_real_parent_file
#// @global array $_wp_menu_nopriv
#// @global array $_wp_submenu_nopriv
#// 
#// @return string The parent file of the current admin page.
#//
def get_admin_page_parent(parent_="", *_args_):
    
    
    global parent_file_
    global menu_
    global submenu_
    global pagenow_
    global typenow_
    global plugin_page_
    global _wp_real_parent_file_
    global _wp_menu_nopriv_
    global _wp_submenu_nopriv_
    php_check_if_defined("parent_file_","menu_","submenu_","pagenow_","typenow_","plugin_page_","_wp_real_parent_file_","_wp_menu_nopriv_","_wp_submenu_nopriv_")
    if (not php_empty(lambda : parent_)) and "admin.php" != parent_:
        if (php_isset(lambda : _wp_real_parent_file_[parent_])):
            parent_ = _wp_real_parent_file_[parent_]
        # end if
        return parent_
    # end if
    if "admin.php" == pagenow_ and (php_isset(lambda : plugin_page_)):
        for parent_menu_ in menu_:
            if parent_menu_[2] == plugin_page_:
                parent_file_ = plugin_page_
                if (php_isset(lambda : _wp_real_parent_file_[parent_file_])):
                    parent_file_ = _wp_real_parent_file_[parent_file_]
                # end if
                return parent_file_
            # end if
        # end for
        if (php_isset(lambda : _wp_menu_nopriv_[plugin_page_])):
            parent_file_ = plugin_page_
            if (php_isset(lambda : _wp_real_parent_file_[parent_file_])):
                parent_file_ = _wp_real_parent_file_[parent_file_]
            # end if
            return parent_file_
        # end if
    # end if
    if (php_isset(lambda : plugin_page_)) and (php_isset(lambda : _wp_submenu_nopriv_[pagenow_][plugin_page_])):
        parent_file_ = pagenow_
        if (php_isset(lambda : _wp_real_parent_file_[parent_file_])):
            parent_file_ = _wp_real_parent_file_[parent_file_]
        # end if
        return parent_file_
    # end if
    for parent_ in php_array_keys(submenu_):
        for submenu_array_ in submenu_[parent_]:
            if (php_isset(lambda : _wp_real_parent_file_[parent_])):
                parent_ = _wp_real_parent_file_[parent_]
            # end if
            if (not php_empty(lambda : typenow_)) and str(pagenow_) + str("?post_type=") + str(typenow_) == submenu_array_[2]:
                parent_file_ = parent_
                return parent_
            elif submenu_array_[2] == pagenow_ and php_empty(lambda : typenow_) and php_empty(lambda : parent_file_) or False == php_strpos(parent_file_, "?"):
                parent_file_ = parent_
                return parent_
            elif (php_isset(lambda : plugin_page_)) and plugin_page_ == submenu_array_[2]:
                parent_file_ = parent_
                return parent_
            # end if
        # end for
    # end for
    if php_empty(lambda : parent_file_):
        parent_file_ = ""
    # end if
    return ""
# end def get_admin_page_parent
#// 
#// Gets the title of the current admin page.
#// 
#// @since 1.5.0
#// 
#// @global string $title
#// @global array $menu
#// @global array $submenu
#// @global string $pagenow
#// @global string $plugin_page
#// @global string $typenow
#// 
#// @return string The title of the current admin page.
#//
def get_admin_page_title(*_args_):
    
    
    global title_
    global menu_
    global submenu_
    global pagenow_
    global plugin_page_
    global typenow_
    php_check_if_defined("title_","menu_","submenu_","pagenow_","plugin_page_","typenow_")
    if (not php_empty(lambda : title_)):
        return title_
    # end if
    hook_ = get_plugin_page_hook(plugin_page_, pagenow_)
    parent_ = get_admin_page_parent()
    parent1_ = parent_
    if php_empty(lambda : parent_):
        for menu_array_ in menu_:
            if (php_isset(lambda : menu_array_[3])):
                if menu_array_[2] == pagenow_:
                    title_ = menu_array_[3]
                    return menu_array_[3]
                elif (php_isset(lambda : plugin_page_)) and plugin_page_ == menu_array_[2] and hook_ == menu_array_[3]:
                    title_ = menu_array_[3]
                    return menu_array_[3]
                # end if
            else:
                title_ = menu_array_[0]
                return title_
            # end if
        # end for
    else:
        for parent_ in php_array_keys(submenu_):
            for submenu_array_ in submenu_[parent_]:
                if (php_isset(lambda : plugin_page_)) and plugin_page_ == submenu_array_[2] and parent_ == pagenow_ or parent_ == plugin_page_ or plugin_page_ == hook_ or "admin.php" == pagenow_ and parent1_ != submenu_array_[2] or (not php_empty(lambda : typenow_)) and parent_ == pagenow_ + "?post_type=" + typenow_:
                    title_ = submenu_array_[3]
                    return submenu_array_[3]
                # end if
                if submenu_array_[2] != pagenow_ or (php_isset(lambda : PHP_REQUEST["page"])):
                    continue
                # end if
                if (php_isset(lambda : submenu_array_[3])):
                    title_ = submenu_array_[3]
                    return submenu_array_[3]
                else:
                    title_ = submenu_array_[0]
                    return title_
                # end if
            # end for
        # end for
        if php_empty(lambda : title_):
            for menu_array_ in menu_:
                if (php_isset(lambda : plugin_page_)) and plugin_page_ == menu_array_[2] and "admin.php" == pagenow_ and parent1_ == menu_array_[2]:
                    title_ = menu_array_[3]
                    return menu_array_[3]
                # end if
            # end for
        # end if
    # end if
    return title_
# end def get_admin_page_title
#// 
#// Gets the hook attached to the administrative page of a plugin.
#// 
#// @since 1.5.0
#// 
#// @param string $plugin_page The slug name of the plugin page.
#// @param string $parent_page The slug name for the parent menu (or the file name of a standard
#// WordPress admin page).
#// @return string|null Hook attached to the plugin page, null otherwise.
#//
def get_plugin_page_hook(plugin_page_=None, parent_page_=None, *_args_):
    
    
    hook_ = get_plugin_page_hookname(plugin_page_, parent_page_)
    if has_action(hook_):
        return hook_
    else:
        return None
    # end if
# end def get_plugin_page_hook
#// 
#// Gets the hook name for the administrative page of a plugin.
#// 
#// @since 1.5.0
#// 
#// @global array $admin_page_hooks
#// 
#// @param string $plugin_page The slug name of the plugin page.
#// @param string $parent_page The slug name for the parent menu (or the file name of a standard
#// WordPress admin page).
#// @return string Hook name for the plugin page.
#//
def get_plugin_page_hookname(plugin_page_=None, parent_page_=None, *_args_):
    
    
    global admin_page_hooks_
    php_check_if_defined("admin_page_hooks_")
    parent_ = get_admin_page_parent(parent_page_)
    page_type_ = "admin"
    if php_empty(lambda : parent_page_) or "admin.php" == parent_page_ or (php_isset(lambda : admin_page_hooks_[plugin_page_])):
        if (php_isset(lambda : admin_page_hooks_[plugin_page_])):
            page_type_ = "toplevel"
        elif (php_isset(lambda : admin_page_hooks_[parent_])):
            page_type_ = admin_page_hooks_[parent_]
        # end if
    elif (php_isset(lambda : admin_page_hooks_[parent_])):
        page_type_ = admin_page_hooks_[parent_]
    # end if
    plugin_name_ = php_preg_replace("!\\.php!", "", plugin_page_)
    return page_type_ + "_page_" + plugin_name_
# end def get_plugin_page_hookname
#// 
#// Determines whether the current user can access the current admin page.
#// 
#// @since 1.5.0
#// 
#// @global string $pagenow
#// @global array  $menu
#// @global array  $submenu
#// @global array  $_wp_menu_nopriv
#// @global array  $_wp_submenu_nopriv
#// @global string $plugin_page
#// @global array  $_registered_pages
#// 
#// @return bool True if the current user can access the admin page, false otherwise.
#//
def user_can_access_admin_page(*_args_):
    
    
    global pagenow_
    global menu_
    global submenu_
    global _wp_menu_nopriv_
    global _wp_submenu_nopriv_
    global plugin_page_
    global _registered_pages_
    php_check_if_defined("pagenow_","menu_","submenu_","_wp_menu_nopriv_","_wp_submenu_nopriv_","plugin_page_","_registered_pages_")
    parent_ = get_admin_page_parent()
    if (not (php_isset(lambda : plugin_page_))) and (php_isset(lambda : _wp_submenu_nopriv_[parent_][pagenow_])):
        return False
    # end if
    if (php_isset(lambda : plugin_page_)):
        if (php_isset(lambda : _wp_submenu_nopriv_[parent_][plugin_page_])):
            return False
        # end if
        hookname_ = get_plugin_page_hookname(plugin_page_, parent_)
        if (not (php_isset(lambda : _registered_pages_[hookname_]))):
            return False
        # end if
    # end if
    if php_empty(lambda : parent_):
        if (php_isset(lambda : _wp_menu_nopriv_[pagenow_])):
            return False
        # end if
        if (php_isset(lambda : _wp_submenu_nopriv_[pagenow_][pagenow_])):
            return False
        # end if
        if (php_isset(lambda : plugin_page_)) and (php_isset(lambda : _wp_submenu_nopriv_[pagenow_][plugin_page_])):
            return False
        # end if
        if (php_isset(lambda : plugin_page_)) and (php_isset(lambda : _wp_menu_nopriv_[plugin_page_])):
            return False
        # end if
        for key_ in php_array_keys(_wp_submenu_nopriv_):
            if (php_isset(lambda : _wp_submenu_nopriv_[key_][pagenow_])):
                return False
            # end if
            if (php_isset(lambda : plugin_page_)) and (php_isset(lambda : _wp_submenu_nopriv_[key_][plugin_page_])):
                return False
            # end if
        # end for
        return True
    # end if
    if (php_isset(lambda : plugin_page_)) and plugin_page_ == parent_ and (php_isset(lambda : _wp_menu_nopriv_[plugin_page_])):
        return False
    # end if
    if (php_isset(lambda : submenu_[parent_])):
        for submenu_array_ in submenu_[parent_]:
            if (php_isset(lambda : plugin_page_)) and submenu_array_[2] == plugin_page_:
                if current_user_can(submenu_array_[1]):
                    return True
                else:
                    return False
                # end if
            elif submenu_array_[2] == pagenow_:
                if current_user_can(submenu_array_[1]):
                    return True
                else:
                    return False
                # end if
            # end if
        # end for
    # end if
    for menu_array_ in menu_:
        if menu_array_[2] == parent_:
            if current_user_can(menu_array_[1]):
                return True
            else:
                return False
            # end if
        # end if
    # end for
    return True
# end def user_can_access_admin_page
#// Whitelist functions
#// 
#// Refreshes the value of the options whitelist available via the 'whitelist_options' hook.
#// 
#// See the {@see 'whitelist_options'} filter.
#// 
#// @since 2.7.0
#// 
#// @global array $new_whitelist_options
#// 
#// @param array $options
#// @return array
#//
def option_update_filter(options_=None, *_args_):
    
    
    global new_whitelist_options_
    php_check_if_defined("new_whitelist_options_")
    if php_is_array(new_whitelist_options_):
        options_ = add_option_whitelist(new_whitelist_options_, options_)
    # end if
    return options_
# end def option_update_filter
#// 
#// Adds an array of options to the options whitelist.
#// 
#// @since 2.7.0
#// 
#// @global array $whitelist_options
#// 
#// @param array        $new_options
#// @param string|array $options
#// @return array
#//
def add_option_whitelist(new_options_=None, options_="", *_args_):
    
    
    if "" == options_:
        global whitelist_options_
        php_check_if_defined("whitelist_options_")
    else:
        whitelist_options_ = options_
    # end if
    for page_,keys_ in new_options_.items():
        for key_ in keys_:
            if (not (php_isset(lambda : whitelist_options_[page_]))) or (not php_is_array(whitelist_options_[page_])):
                whitelist_options_[page_] = Array()
                whitelist_options_[page_][-1] = key_
            else:
                pos_ = php_array_search(key_, whitelist_options_[page_])
                if False == pos_:
                    whitelist_options_[page_][-1] = key_
                # end if
            # end if
        # end for
    # end for
    return whitelist_options_
# end def add_option_whitelist
#// 
#// Removes a list of options from the options whitelist.
#// 
#// @since 2.7.0
#// 
#// @global array $whitelist_options
#// 
#// @param array        $del_options
#// @param string|array $options
#// @return array
#//
def remove_option_whitelist(del_options_=None, options_="", *_args_):
    
    
    if "" == options_:
        global whitelist_options_
        php_check_if_defined("whitelist_options_")
    else:
        whitelist_options_ = options_
    # end if
    for page_,keys_ in del_options_.items():
        for key_ in keys_:
            if (php_isset(lambda : whitelist_options_[page_])) and php_is_array(whitelist_options_[page_]):
                pos_ = php_array_search(key_, whitelist_options_[page_])
                if False != pos_:
                    whitelist_options_[page_][pos_] = None
                # end if
            # end if
        # end for
    # end for
    return whitelist_options_
# end def remove_option_whitelist
#// 
#// Output nonce, action, and option_page fields for a settings page.
#// 
#// @since 2.7.0
#// 
#// @param string $option_group A settings group name. This should match the group name
#// used in register_setting().
#//
def settings_fields(option_group_=None, *_args_):
    
    
    php_print("<input type='hidden' name='option_page' value='" + esc_attr(option_group_) + "' />")
    php_print("<input type=\"hidden\" name=\"action\" value=\"update\" />")
    wp_nonce_field(str(option_group_) + str("-options"))
# end def settings_fields
#// 
#// Clears the plugins cache used by get_plugins() and by default, the plugin updates cache.
#// 
#// @since 3.7.0
#// 
#// @param bool $clear_update_cache Whether to clear the plugin updates cache. Default true.
#//
def wp_clean_plugins_cache(clear_update_cache_=None, *_args_):
    if clear_update_cache_ is None:
        clear_update_cache_ = True
    # end if
    
    if clear_update_cache_:
        delete_site_transient("update_plugins")
    # end if
    wp_cache_delete("plugins", "plugins")
# end def wp_clean_plugins_cache
#// 
#// Load a given plugin attempt to generate errors.
#// 
#// @since 3.0.0
#// @since 4.4.0 Function was moved into the `wp-admin/includes/plugin.php` file.
#// 
#// @param string $plugin Path to the plugin file relative to the plugins directory.
#//
def plugin_sandbox_scrape(plugin_=None, *_args_):
    
    
    if (not php_defined("WP_SANDBOX_SCRAPING")):
        php_define("WP_SANDBOX_SCRAPING", True)
    # end if
    wp_register_plugin_realpath(WP_PLUGIN_DIR + "/" + plugin_)
    php_include_file(WP_PLUGIN_DIR + "/" + plugin_, once=False)
# end def plugin_sandbox_scrape
#// 
#// Helper function for adding content to the Privacy Policy Guide.
#// 
#// Plugins and themes should suggest text for inclusion in the site's privacy policy.
#// The suggested text should contain information about any functionality that affects user privacy,
#// and will be shown on the Privacy Policy Guide screen.
#// 
#// A plugin or theme can use this function multiple times as long as it will help to better present
#// the suggested policy content. For example modular plugins such as WooCommerse or Jetpack
#// can add or remove suggested content depending on the modules/extensions that are enabled.
#// For more information see the Plugin Handbook:
#// https://developer.wordpress.org/plugins/privacy/suggesting-text-for-the-site-privacy-policy/.
#// 
#// The HTML contents of the `$policy_text` supports use of a specialized `.privacy-policy-tutorial`
#// CSS class which can be used to provide supplemental information. Any content contained within
#// HTML elements that have the `.privacy-policy-tutorial` CSS class applied will be omitted
#// from the clipboard when the section content is copied.
#// 
#// Intended for use with the `'admin_init'` action.
#// 
#// @since 4.9.6
#// 
#// @param string $plugin_name The name of the plugin or theme that is suggesting content
#// for the site's privacy policy.
#// @param string $policy_text The suggested content for inclusion in the policy.
#//
def wp_add_privacy_policy_content(plugin_name_=None, policy_text_=None, *_args_):
    
    
    if (not is_admin()):
        _doing_it_wrong(__FUNCTION__, php_sprintf(__("The suggested privacy policy content should be added only in wp-admin by using the %s (or later) action."), "<code>admin_init</code>"), "4.9.7")
        return
    elif (not doing_action("admin_init")) and (not did_action("admin_init")):
        _doing_it_wrong(__FUNCTION__, php_sprintf(__("The suggested privacy policy content should be added by using the %s (or later) action. Please see the inline documentation."), "<code>admin_init</code>"), "4.9.7")
        return
    # end if
    if (not php_class_exists("WP_Privacy_Policy_Content")):
        php_include_file(ABSPATH + "wp-admin/includes/class-wp-privacy-policy-content.php", once=True)
    # end if
    WP_Privacy_Policy_Content.add(plugin_name_, policy_text_)
# end def wp_add_privacy_policy_content
#// 
#// Determines whether a plugin is technically active but was paused while
#// loading.
#// 
#// For more information on this and similar theme functions, check out
#// the {@link https://developer.wordpress.org/themes/basics/conditional-tags
#// Conditional Tags} article in the Theme Developer Handbook.
#// 
#// @since 5.2.0
#// 
#// @param string $plugin Path to the plugin file relative to the plugins directory.
#// @return bool True, if in the list of paused plugins. False, if not in the list.
#//
def is_plugin_paused(plugin_=None, *_args_):
    
    
    if (not (php_isset(lambda : PHP_GLOBALS["_paused_plugins"]))):
        return False
    # end if
    if (not is_plugin_active(plugin_)):
        return False
    # end if
    plugin_ = php_explode("/", plugin_)
    return php_array_key_exists(plugin_, PHP_GLOBALS["_paused_plugins"])
# end def is_plugin_paused
#// 
#// Gets the error that was recorded for a paused plugin.
#// 
#// @since 5.2.0
#// 
#// @param string $plugin Path to the plugin file relative to the plugins directory.
#// @return array|false Array of error information as returned by `error_get_last()`,
#// or false if none was recorded.
#//
def wp_get_plugin_error(plugin_=None, *_args_):
    
    
    if (not (php_isset(lambda : PHP_GLOBALS["_paused_plugins"]))):
        return False
    # end if
    plugin_ = php_explode("/", plugin_)
    if (not php_array_key_exists(plugin_, PHP_GLOBALS["_paused_plugins"])):
        return False
    # end if
    return PHP_GLOBALS["_paused_plugins"][plugin_]
# end def wp_get_plugin_error
#// 
#// Tries to resume a single plugin.
#// 
#// If a redirect was provided, we first ensure the plugin does not throw fatal
#// errors anymore.
#// 
#// The way it works is by setting the redirection to the error before trying to
#// include the plugin file. If the plugin fails, then the redirection will not
#// be overwritten with the success message and the plugin will not be resumed.
#// 
#// @since 5.2.0
#// 
#// @param string $plugin   Single plugin to resume.
#// @param string $redirect Optional. URL to redirect to. Default empty string.
#// @return bool|WP_Error True on success, false if `$plugin` was not paused,
#// `WP_Error` on failure.
#//
def resume_plugin(plugin_=None, redirect_="", *_args_):
    
    
    #// 
    #// We'll override this later if the plugin could be resumed without
    #// creating a fatal error.
    #//
    if (not php_empty(lambda : redirect_)):
        wp_redirect(add_query_arg("_error_nonce", wp_create_nonce("plugin-resume-error_" + plugin_), redirect_))
        #// Load the plugin to test whether it throws a fatal error.
        ob_start()
        plugin_sandbox_scrape(plugin_)
        ob_clean()
    # end if
    extension_ = php_explode("/", plugin_)
    result_ = wp_paused_plugins().delete(extension_)
    if (not result_):
        return php_new_class("WP_Error", lambda : WP_Error("could_not_resume_plugin", __("Could not resume the plugin.")))
    # end if
    return True
# end def resume_plugin
#// 
#// Renders an admin notice in case some plugins have been paused due to errors.
#// 
#// @since 5.2.0
#//
def paused_plugins_notice(*_args_):
    
    
    if "plugins.php" == PHP_GLOBALS["pagenow"]:
        return
    # end if
    if (not current_user_can("resume_plugins")):
        return
    # end if
    if (not (php_isset(lambda : PHP_GLOBALS["_paused_plugins"]))) or php_empty(lambda : PHP_GLOBALS["_paused_plugins"]):
        return
    # end if
    printf("<div class=\"notice notice-error\"><p><strong>%s</strong><br>%s</p><p><a href=\"%s\">%s</a></p></div>", __("One or more plugins failed to load properly."), __("You can find more details and make changes on the Plugins screen."), esc_url(admin_url("plugins.php?plugin_status=paused")), __("Go to the Plugins screen"))
# end def paused_plugins_notice
