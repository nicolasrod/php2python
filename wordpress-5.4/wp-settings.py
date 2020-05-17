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
#// Used to set up and fix common variables and include
#// the WordPress procedural and class library.
#// 
#// Allows for some configuration in wp-config.php (see default-constants.php)
#// 
#// @package WordPress
#// 
#// 
#// Stores the location of the WordPress directory of functions, classes, and core content.
#// 
#// @since 1.0.0
#//
php_define("WPINC", "wp-includes")
#// 
#// Version information for the current WordPress release.
#// 
#// These can't be directly globalized in version.php. When updating,
#// we're including version.php from another installation and don't want
#// these values to be overridden if already set.
#// 
#// @global string $wp_version             The WordPress version string.
#// @global int    $wp_db_version          WordPress database version.
#// @global string $tinymce_version        TinyMCE version.
#// @global string $required_php_version   The required PHP version string.
#// @global string $required_mysql_version The required MySQL version string.
#// @global string $wp_local_package       Locale code of the package.
#//
global wp_version_
global wp_db_version_
global tinymce_version_
global required_php_version_
global required_mysql_version_
global wp_local_package_
php_check_if_defined("wp_version_","wp_db_version_","tinymce_version_","required_php_version_","required_mysql_version_","wp_local_package_")
php_include_file(ABSPATH + WPINC + "/version.php", once=False)
php_include_file(ABSPATH + WPINC + "/load.php", once=False)
#// Check for the required PHP version and for the MySQL extension or a database drop-in.
wp_check_php_mysql_versions()
#// Include files required for initialization.
php_include_file(ABSPATH + WPINC + "/class-wp-paused-extensions-storage.php", once=False)
php_include_file(ABSPATH + WPINC + "/class-wp-fatal-error-handler.php", once=False)
php_include_file(ABSPATH + WPINC + "/class-wp-recovery-mode-cookie-service.php", once=False)
php_include_file(ABSPATH + WPINC + "/class-wp-recovery-mode-key-service.php", once=False)
php_include_file(ABSPATH + WPINC + "/class-wp-recovery-mode-link-service.php", once=False)
php_include_file(ABSPATH + WPINC + "/class-wp-recovery-mode-email-service.php", once=False)
php_include_file(ABSPATH + WPINC + "/class-wp-recovery-mode.php", once=False)
php_include_file(ABSPATH + WPINC + "/error-protection.php", once=False)
php_include_file(ABSPATH + WPINC + "/default-constants.php", once=False)
php_include_file(ABSPATH + WPINC + "/plugin.php", once=True)
#// 
#// If not already configured, `$blog_id` will default to 1 in a single site
#// configuration. In multisite, it will be overridden by default in ms-settings.php.
#// 
#// @global int $blog_id
#// @since 2.0.0
#//
global blog_id_
php_check_if_defined("blog_id_")
#// Set initial default constants including WP_MEMORY_LIMIT, WP_MAX_MEMORY_LIMIT, WP_DEBUG, SCRIPT_DEBUG, WP_CONTENT_DIR and WP_CACHE.
wp_initial_constants()
#// Make sure we register the shutdown handler for fatal errors as soon as possible.
wp_register_fatal_error_handler()
#// WordPress calculates offsets from UTC.
php_date_default_timezone_set("UTC")
#// Turn register_globals off.
wp_unregister_GLOBALS()
#// Standardize $_SERVER variables across setups.
wp_fix_server_vars()
#// Check if we're in maintenance mode.
wp_maintenance()
#// Start loading timer.
timer_start()
#// Check if we're in WP_DEBUG mode.
wp_debug_mode()
#// 
#// Filters whether to enable loading of the advanced-cache.php drop-in.
#// 
#// This filter runs before it can be used by plugins. It is designed for non-web
#// run-times. If false is returned, advanced-cache.php will never be loaded.
#// 
#// @since 4.6.0
#// 
#// @param bool $enable_advanced_cache Whether to enable loading advanced-cache.php (if present).
#// Default true.
#//
if WP_CACHE and apply_filters("enable_loading_advanced_cache_dropin", True) and php_file_exists(WP_CONTENT_DIR + "/advanced-cache.php"):
    #// For an advanced caching plugin to use. Uses a static drop-in because you would only want one.
    php_include_file(WP_CONTENT_DIR + "/advanced-cache.php", once=False)
    #// Re-initialize any hooks added manually by advanced-cache.php.
    if wp_filter_:
        wp_filter_ = WP_Hook.build_preinitialized_hooks(wp_filter_)
    # end if
# end if
#// Define WP_LANG_DIR if not set.
wp_set_lang_dir()
#// Load early WordPress files.
php_include_file(ABSPATH + WPINC + "/compat.php", once=False)
php_include_file(ABSPATH + WPINC + "/class-wp-list-util.php", once=False)
php_include_file(ABSPATH + WPINC + "/formatting.php", once=False)
php_include_file(ABSPATH + WPINC + "/meta.php", once=False)
php_include_file(ABSPATH + WPINC + "/functions.php", once=False)
php_include_file(ABSPATH + WPINC + "/class-wp-meta-query.php", once=False)
php_include_file(ABSPATH + WPINC + "/class-wp-matchesmapregex.php", once=False)
php_include_file(ABSPATH + WPINC + "/class-wp.php", once=False)
php_include_file(ABSPATH + WPINC + "/class-wp-error.php", once=False)
php_include_file(ABSPATH + WPINC + "/pomo/mo.php", once=False)
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// @since 0.71
#//
global wpdb_
php_check_if_defined("wpdb_")
#// Include the wpdb class and, if present, a db.php database drop-in.
require_wp_db()
#// Set the database table prefix and the format specifiers for database table columns.
PHP_GLOBALS["table_prefix"] = table_prefix_
wp_set_wpdb_vars()
#// Start the WordPress object cache, or an external object cache if the drop-in is present.
wp_start_object_cache()
#// Attach the default filters.
php_include_file(ABSPATH + WPINC + "/default-filters.php", once=False)
#// Initialize multisite if enabled.
if is_multisite():
    php_include_file(ABSPATH + WPINC + "/class-wp-site-query.php", once=False)
    php_include_file(ABSPATH + WPINC + "/class-wp-network-query.php", once=False)
    php_include_file(ABSPATH + WPINC + "/ms-blogs.php", once=False)
    php_include_file(ABSPATH + WPINC + "/ms-settings.php", once=False)
elif (not php_defined("MULTISITE")):
    php_define("MULTISITE", False)
# end if
php_register_shutdown_function("shutdown_action_hook")
#// Stop most of WordPress from being loaded if we just want the basics.
if SHORTINIT:
    php_set_include_retval(False)
    sys.exit(-1)
# end if
#// Load the L10n library.
php_include_file(ABSPATH + WPINC + "/l10n.php", once=True)
php_include_file(ABSPATH + WPINC + "/class-wp-locale.php", once=True)
php_include_file(ABSPATH + WPINC + "/class-wp-locale-switcher.php", once=True)
#// Run the installer if WordPress is not installed.
wp_not_installed()
#// Load most of WordPress.
php_include_file(ABSPATH + WPINC + "/class-wp-walker.php", once=False)
php_include_file(ABSPATH + WPINC + "/class-wp-ajax-response.php", once=False)
php_include_file(ABSPATH + WPINC + "/capabilities.php", once=False)
php_include_file(ABSPATH + WPINC + "/class-wp-roles.php", once=False)
php_include_file(ABSPATH + WPINC + "/class-wp-role.php", once=False)
php_include_file(ABSPATH + WPINC + "/class-wp-user.php", once=False)
php_include_file(ABSPATH + WPINC + "/class-wp-query.php", once=False)
php_include_file(ABSPATH + WPINC + "/query.php", once=False)
php_include_file(ABSPATH + WPINC + "/class-wp-date-query.php", once=False)
php_include_file(ABSPATH + WPINC + "/theme.php", once=False)
php_include_file(ABSPATH + WPINC + "/class-wp-theme.php", once=False)
php_include_file(ABSPATH + WPINC + "/template.php", once=False)
php_include_file(ABSPATH + WPINC + "/class-wp-user-request.php", once=False)
php_include_file(ABSPATH + WPINC + "/user.php", once=False)
php_include_file(ABSPATH + WPINC + "/class-wp-user-query.php", once=False)
php_include_file(ABSPATH + WPINC + "/class-wp-session-tokens.php", once=False)
php_include_file(ABSPATH + WPINC + "/class-wp-user-meta-session-tokens.php", once=False)
php_include_file(ABSPATH + WPINC + "/class-wp-metadata-lazyloader.php", once=False)
php_include_file(ABSPATH + WPINC + "/general-template.php", once=False)
php_include_file(ABSPATH + WPINC + "/link-template.php", once=False)
php_include_file(ABSPATH + WPINC + "/author-template.php", once=False)
php_include_file(ABSPATH + WPINC + "/post.php", once=False)
php_include_file(ABSPATH + WPINC + "/class-walker-page.php", once=False)
php_include_file(ABSPATH + WPINC + "/class-walker-page-dropdown.php", once=False)
php_include_file(ABSPATH + WPINC + "/class-wp-post-type.php", once=False)
php_include_file(ABSPATH + WPINC + "/class-wp-post.php", once=False)
php_include_file(ABSPATH + WPINC + "/post-template.php", once=False)
php_include_file(ABSPATH + WPINC + "/revision.php", once=False)
php_include_file(ABSPATH + WPINC + "/post-formats.php", once=False)
php_include_file(ABSPATH + WPINC + "/post-thumbnail-template.php", once=False)
php_include_file(ABSPATH + WPINC + "/category.php", once=False)
php_include_file(ABSPATH + WPINC + "/class-walker-category.php", once=False)
php_include_file(ABSPATH + WPINC + "/class-walker-category-dropdown.php", once=False)
php_include_file(ABSPATH + WPINC + "/category-template.php", once=False)
php_include_file(ABSPATH + WPINC + "/comment.php", once=False)
php_include_file(ABSPATH + WPINC + "/class-wp-comment.php", once=False)
php_include_file(ABSPATH + WPINC + "/class-wp-comment-query.php", once=False)
php_include_file(ABSPATH + WPINC + "/class-walker-comment.php", once=False)
php_include_file(ABSPATH + WPINC + "/comment-template.php", once=False)
php_include_file(ABSPATH + WPINC + "/rewrite.php", once=False)
php_include_file(ABSPATH + WPINC + "/class-wp-rewrite.php", once=False)
php_include_file(ABSPATH + WPINC + "/feed.php", once=False)
php_include_file(ABSPATH + WPINC + "/bookmark.php", once=False)
php_include_file(ABSPATH + WPINC + "/bookmark-template.php", once=False)
php_include_file(ABSPATH + WPINC + "/kses.php", once=False)
php_include_file(ABSPATH + WPINC + "/cron.php", once=False)
php_include_file(ABSPATH + WPINC + "/deprecated.php", once=False)
php_include_file(ABSPATH + WPINC + "/script-loader.php", once=False)
php_include_file(ABSPATH + WPINC + "/taxonomy.php", once=False)
php_include_file(ABSPATH + WPINC + "/class-wp-taxonomy.php", once=False)
php_include_file(ABSPATH + WPINC + "/class-wp-term.php", once=False)
php_include_file(ABSPATH + WPINC + "/class-wp-term-query.php", once=False)
php_include_file(ABSPATH + WPINC + "/class-wp-tax-query.php", once=False)
php_include_file(ABSPATH + WPINC + "/update.php", once=False)
php_include_file(ABSPATH + WPINC + "/canonical.php", once=False)
php_include_file(ABSPATH + WPINC + "/shortcodes.php", once=False)
php_include_file(ABSPATH + WPINC + "/embed.php", once=False)
php_include_file(ABSPATH + WPINC + "/class-wp-embed.php", once=False)
php_include_file(ABSPATH + WPINC + "/class-wp-oembed.php", once=False)
php_include_file(ABSPATH + WPINC + "/class-wp-oembed-controller.php", once=False)
php_include_file(ABSPATH + WPINC + "/media.php", once=False)
php_include_file(ABSPATH + WPINC + "/http.php", once=False)
php_include_file(ABSPATH + WPINC + "/class-http.php", once=False)
php_include_file(ABSPATH + WPINC + "/class-wp-http-streams.php", once=False)
php_include_file(ABSPATH + WPINC + "/class-wp-http-curl.php", once=False)
php_include_file(ABSPATH + WPINC + "/class-wp-http-proxy.php", once=False)
php_include_file(ABSPATH + WPINC + "/class-wp-http-cookie.php", once=False)
php_include_file(ABSPATH + WPINC + "/class-wp-http-encoding.php", once=False)
php_include_file(ABSPATH + WPINC + "/class-wp-http-response.php", once=False)
php_include_file(ABSPATH + WPINC + "/class-wp-http-requests-response.php", once=False)
php_include_file(ABSPATH + WPINC + "/class-wp-http-requests-hooks.php", once=False)
php_include_file(ABSPATH + WPINC + "/widgets.php", once=False)
php_include_file(ABSPATH + WPINC + "/class-wp-widget.php", once=False)
php_include_file(ABSPATH + WPINC + "/class-wp-widget-factory.php", once=False)
php_include_file(ABSPATH + WPINC + "/nav-menu.php", once=False)
php_include_file(ABSPATH + WPINC + "/nav-menu-template.php", once=False)
php_include_file(ABSPATH + WPINC + "/admin-bar.php", once=False)
php_include_file(ABSPATH + WPINC + "/rest-api.php", once=False)
php_include_file(ABSPATH + WPINC + "/rest-api/class-wp-rest-server.php", once=False)
php_include_file(ABSPATH + WPINC + "/rest-api/class-wp-rest-response.php", once=False)
php_include_file(ABSPATH + WPINC + "/rest-api/class-wp-rest-request.php", once=False)
php_include_file(ABSPATH + WPINC + "/rest-api/endpoints/class-wp-rest-controller.php", once=False)
php_include_file(ABSPATH + WPINC + "/rest-api/endpoints/class-wp-rest-posts-controller.php", once=False)
php_include_file(ABSPATH + WPINC + "/rest-api/endpoints/class-wp-rest-attachments-controller.php", once=False)
php_include_file(ABSPATH + WPINC + "/rest-api/endpoints/class-wp-rest-post-types-controller.php", once=False)
php_include_file(ABSPATH + WPINC + "/rest-api/endpoints/class-wp-rest-post-statuses-controller.php", once=False)
php_include_file(ABSPATH + WPINC + "/rest-api/endpoints/class-wp-rest-revisions-controller.php", once=False)
php_include_file(ABSPATH + WPINC + "/rest-api/endpoints/class-wp-rest-autosaves-controller.php", once=False)
php_include_file(ABSPATH + WPINC + "/rest-api/endpoints/class-wp-rest-taxonomies-controller.php", once=False)
php_include_file(ABSPATH + WPINC + "/rest-api/endpoints/class-wp-rest-terms-controller.php", once=False)
php_include_file(ABSPATH + WPINC + "/rest-api/endpoints/class-wp-rest-users-controller.php", once=False)
php_include_file(ABSPATH + WPINC + "/rest-api/endpoints/class-wp-rest-comments-controller.php", once=False)
php_include_file(ABSPATH + WPINC + "/rest-api/endpoints/class-wp-rest-search-controller.php", once=False)
php_include_file(ABSPATH + WPINC + "/rest-api/endpoints/class-wp-rest-blocks-controller.php", once=False)
php_include_file(ABSPATH + WPINC + "/rest-api/endpoints/class-wp-rest-block-renderer-controller.php", once=False)
php_include_file(ABSPATH + WPINC + "/rest-api/endpoints/class-wp-rest-settings-controller.php", once=False)
php_include_file(ABSPATH + WPINC + "/rest-api/endpoints/class-wp-rest-themes-controller.php", once=False)
php_include_file(ABSPATH + WPINC + "/rest-api/fields/class-wp-rest-meta-fields.php", once=False)
php_include_file(ABSPATH + WPINC + "/rest-api/fields/class-wp-rest-comment-meta-fields.php", once=False)
php_include_file(ABSPATH + WPINC + "/rest-api/fields/class-wp-rest-post-meta-fields.php", once=False)
php_include_file(ABSPATH + WPINC + "/rest-api/fields/class-wp-rest-term-meta-fields.php", once=False)
php_include_file(ABSPATH + WPINC + "/rest-api/fields/class-wp-rest-user-meta-fields.php", once=False)
php_include_file(ABSPATH + WPINC + "/rest-api/search/class-wp-rest-search-handler.php", once=False)
php_include_file(ABSPATH + WPINC + "/rest-api/search/class-wp-rest-post-search-handler.php", once=False)
php_include_file(ABSPATH + WPINC + "/class-wp-block-type.php", once=False)
php_include_file(ABSPATH + WPINC + "/class-wp-block-styles-registry.php", once=False)
php_include_file(ABSPATH + WPINC + "/class-wp-block-type-registry.php", once=False)
php_include_file(ABSPATH + WPINC + "/class-wp-block-parser.php", once=False)
php_include_file(ABSPATH + WPINC + "/blocks.php", once=False)
php_include_file(ABSPATH + WPINC + "/blocks/archives.php", once=False)
php_include_file(ABSPATH + WPINC + "/blocks/block.php", once=False)
php_include_file(ABSPATH + WPINC + "/blocks/calendar.php", once=False)
php_include_file(ABSPATH + WPINC + "/blocks/categories.php", once=False)
php_include_file(ABSPATH + WPINC + "/blocks/latest-comments.php", once=False)
php_include_file(ABSPATH + WPINC + "/blocks/latest-posts.php", once=False)
php_include_file(ABSPATH + WPINC + "/blocks/rss.php", once=False)
php_include_file(ABSPATH + WPINC + "/blocks/search.php", once=False)
php_include_file(ABSPATH + WPINC + "/blocks/shortcode.php", once=False)
php_include_file(ABSPATH + WPINC + "/blocks/social-link.php", once=False)
php_include_file(ABSPATH + WPINC + "/blocks/tag-cloud.php", once=False)
PHP_GLOBALS["wp_embed"] = php_new_class("WP_Embed", lambda : WP_Embed())
#// Load multisite-specific files.
if is_multisite():
    php_include_file(ABSPATH + WPINC + "/ms-functions.php", once=False)
    php_include_file(ABSPATH + WPINC + "/ms-default-filters.php", once=False)
    php_include_file(ABSPATH + WPINC + "/ms-deprecated.php", once=False)
# end if
#// Define constants that rely on the API to obtain the default value.
#// Define must-use plugin directory constants, which may be overridden in the sunrise.php drop-in.
wp_plugin_directory_constants()
PHP_GLOBALS["wp_plugin_paths"] = Array()
#// Load must-use plugins.
for mu_plugin_ in wp_get_mu_plugins():
    php_include_file(mu_plugin_, once=False)
    #// 
    #// Fires once a single must-use plugin has loaded.
    #// 
    #// @since 5.1.0
    #// 
    #// @param string $mu_plugin Full path to the plugin's main file.
    #//
    do_action("mu_plugin_loaded", mu_plugin_)
# end for
mu_plugin_ = None
#// Load network activated plugins.
if is_multisite():
    for network_plugin_ in wp_get_active_network_plugins():
        wp_register_plugin_realpath(network_plugin_)
        php_include_file(network_plugin_, once=False)
        #// 
        #// Fires once a single network-activated plugin has loaded.
        #// 
        #// @since 5.1.0
        #// 
        #// @param string $network_plugin Full path to the plugin's main file.
        #//
        do_action("network_plugin_loaded", network_plugin_)
    # end for
    network_plugin_ = None
# end if
#// 
#// Fires once all must-use and network-activated plugins have loaded.
#// 
#// @since 2.8.0
#//
do_action("muplugins_loaded")
if is_multisite():
    ms_cookie_constants()
# end if
#// Define constants after multisite is loaded.
wp_cookie_constants()
#// Define and enforce our SSL constants.
wp_ssl_constants()
#// Create common globals.
php_include_file(ABSPATH + WPINC + "/vars.php", once=False)
#// Make taxonomies and posts available to plugins and themes.
#// @plugin authors: warning: these get registered again on the init hook.
create_initial_taxonomies()
create_initial_post_types()
wp_start_scraping_edited_file_errors()
#// Register the default theme directory root.
register_theme_directory(get_theme_root())
if (not is_multisite()):
    #// Handle users requesting a recovery mode link and initiating recovery mode.
    wp_recovery_mode().initialize()
# end if
#// Create an instance of WP_Site_Health so that Cron events may fire.
if (not php_class_exists("WP_Site_Health")):
    php_include_file(ABSPATH + "wp-admin/includes/class-wp-site-health.php", once=True)
# end if
WP_Site_Health.get_instance()
#// Load active plugins.
for plugin_ in wp_get_active_and_valid_plugins():
    wp_register_plugin_realpath(plugin_)
    php_include_file(plugin_, once=False)
    #// 
    #// Fires once a single activated plugin has loaded.
    #// 
    #// @since 5.1.0
    #// 
    #// @param string $plugin Full path to the plugin's main file.
    #//
    do_action("plugin_loaded", plugin_)
# end for
plugin_ = None
#// Load pluggable functions.
php_include_file(ABSPATH + WPINC + "/pluggable.php", once=False)
php_include_file(ABSPATH + WPINC + "/pluggable-deprecated.php", once=False)
#// Set internal encoding.
wp_set_internal_encoding()
#// Run wp_cache_postload() if object cache is enabled and the function exists.
if WP_CACHE and php_function_exists("wp_cache_postload"):
    wp_cache_postload()
# end if
#// 
#// Fires once activated plugins have loaded.
#// 
#// Pluggable functions are also available at this point in the loading order.
#// 
#// @since 1.5.0
#//
do_action("plugins_loaded")
#// Define constants which affect functionality if not already defined.
wp_functionality_constants()
#// Add magic quotes and set up $_REQUEST ( $_GET + $_POST ).
wp_magic_quotes()
#// 
#// Fires when comment cookies are sanitized.
#// 
#// @since 2.0.11
#//
do_action("sanitize_comment_cookies")
#// 
#// WordPress Query object
#// 
#// @global WP_Query $wp_the_query WordPress Query object.
#// @since 2.0.0
#//
PHP_GLOBALS["wp_the_query"] = php_new_class("WP_Query", lambda : WP_Query())
#// 
#// Holds the reference to @see $wp_the_query
#// Use this global for WordPress queries
#// 
#// @global WP_Query $wp_query WordPress Query object.
#// @since 1.5.0
#//
PHP_GLOBALS["wp_query"] = PHP_GLOBALS["wp_the_query"]
#// 
#// Holds the WordPress Rewrite object for creating pretty URLs
#// 
#// @global WP_Rewrite $wp_rewrite WordPress rewrite component.
#// @since 1.5.0
#//
PHP_GLOBALS["wp_rewrite"] = php_new_class("WP_Rewrite", lambda : WP_Rewrite())
#// 
#// WordPress Object
#// 
#// @global WP $wp Current WordPress environment instance.
#// @since 2.0.0
#//
PHP_GLOBALS["wp"] = php_new_class("WP", lambda : WP())
#// 
#// WordPress Widget Factory Object
#// 
#// @global WP_Widget_Factory $wp_widget_factory
#// @since 2.8.0
#//
PHP_GLOBALS["wp_widget_factory"] = php_new_class("WP_Widget_Factory", lambda : WP_Widget_Factory())
#// 
#// WordPress User Roles
#// 
#// @global WP_Roles $wp_roles WordPress role management object.
#// @since 2.0.0
#//
PHP_GLOBALS["wp_roles"] = php_new_class("WP_Roles", lambda : WP_Roles())
#// 
#// Fires before the theme is loaded.
#// 
#// @since 2.6.0
#//
do_action("setup_theme")
#// Define the template related constants.
wp_templating_constants()
#// Load the default text localization domain.
load_default_textdomain()
locale_ = get_locale()
locale_file_ = WP_LANG_DIR + str("/") + str(locale_) + str(".php")
if 0 == validate_file(locale_) and php_is_readable(locale_file_):
    php_include_file(locale_file_, once=False)
# end if
locale_file_ = None
#// 
#// WordPress Locale object for loading locale domain date and various strings.
#// 
#// @global WP_Locale $wp_locale WordPress date and time locale object.
#// @since 2.1.0
#//
PHP_GLOBALS["wp_locale"] = php_new_class("WP_Locale", lambda : WP_Locale())
#// 
#// WordPress Locale Switcher object for switching locales.
#// 
#// @since 4.7.0
#// 
#// @global WP_Locale_Switcher $wp_locale_switcher WordPress locale switcher object.
#//
PHP_GLOBALS["wp_locale_switcher"] = php_new_class("WP_Locale_Switcher", lambda : WP_Locale_Switcher())
PHP_GLOBALS["wp_locale_switcher"].init()
#// Load the functions for the active theme, for both parent and child theme if applicable.
for theme_ in wp_get_active_and_valid_themes():
    if php_file_exists(theme_ + "/functions.php"):
        php_include_file(theme_ + "/functions.php", once=False)
    # end if
# end for
theme_ = None
#// 
#// Fires after the theme is loaded.
#// 
#// @since 3.0.0
#//
do_action("after_setup_theme")
#// Set up current user.
PHP_GLOBALS["wp"].init()
#// 
#// Fires after WordPress has finished loading but before any headers are sent.
#// 
#// Most of WP is loaded at this stage, and the user is authenticated. WP continues
#// to load on the {@see 'init'} hook that follows (e.g. widgets), and many plugins instantiate
#// themselves on it for all sorts of reasons (e.g. they need a user, a taxonomy, etc.).
#// 
#// If you wish to plug an action once WP is loaded, use the {@see 'wp_loaded'} hook below.
#// 
#// @since 1.5.0
#//
do_action("init")
#// Check site status.
if is_multisite():
    file_ = ms_site_check()
    if True != file_:
        php_include_file(file_, once=False)
        php_exit(0)
    # end if
    file_ = None
# end if
#// 
#// This hook is fired once WP, all plugins, and the theme are fully loaded and instantiated.
#// 
#// Ajax requests should use wp-admin/admin-ajax.php. admin-ajax.php can handle requests for
#// users not logged in.
#// 
#// @link https://codex.wordpress.org/AJAX_in_Plugins
#// 
#// @since 3.0.0
#//
do_action("wp_loaded")
