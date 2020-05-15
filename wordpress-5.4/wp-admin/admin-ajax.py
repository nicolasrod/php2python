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
#// WordPress Ajax Process Execution
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// @link https://codex.wordpress.org/AJAX_in_Plugins
#// 
#// 
#// Executing Ajax process.
#// 
#// @since 2.1.0
#//
php_define("DOING_AJAX", True)
if (not php_defined("WP_ADMIN")):
    php_define("WP_ADMIN", True)
# end if
#// Load WordPress Bootstrap
php_include_file(php_dirname(__DIR__) + "/wp-load.php", once=True)
#// Allow for cross-domain requests (from the front end).
send_origin_headers()
php_header("Content-Type: text/html; charset=" + get_option("blog_charset"))
php_header("X-Robots-Tag: noindex")
#// Require an action parameter.
if php_empty(lambda : PHP_REQUEST["action"]):
    wp_die("0", 400)
# end if
#// Load WordPress Administration APIs
php_include_file(ABSPATH + "wp-admin/includes/admin.php", once=True)
#// Load Ajax Handlers for WordPress Core
php_include_file(ABSPATH + "wp-admin/includes/ajax-actions.php", once=True)
send_nosniff_header()
nocache_headers()
#// This action is documented in wp-admin/admin.php
do_action("admin_init")
core_actions_get = Array("fetch-list", "ajax-tag-search", "wp-compression-test", "imgedit-preview", "oembed-cache", "autocomplete-user", "dashboard-widgets", "logged-in", "rest-nonce")
core_actions_post = Array("oembed-cache", "image-editor", "delete-comment", "delete-tag", "delete-link", "delete-meta", "delete-post", "trash-post", "untrash-post", "delete-page", "dim-comment", "add-link-category", "add-tag", "get-tagcloud", "get-comments", "replyto-comment", "edit-comment", "add-menu-item", "add-meta", "add-user", "closed-postboxes", "hidden-columns", "update-welcome-panel", "menu-get-metabox", "wp-link-ajax", "menu-locations-save", "menu-quick-search", "meta-box-order", "get-permalink", "sample-permalink", "inline-save", "inline-save-tax", "find_posts", "widgets-order", "save-widget", "delete-inactive-widgets", "set-post-thumbnail", "date_format", "time_format", "wp-remove-post-lock", "dismiss-wp-pointer", "upload-attachment", "get-attachment", "query-attachments", "save-attachment", "save-attachment-compat", "send-link-to-editor", "send-attachment-to-editor", "save-attachment-order", "media-create-image-subsizes", "heartbeat", "get-revision-diffs", "save-user-color-scheme", "update-widget", "query-themes", "parse-embed", "set-attachment-thumbnail", "parse-media-shortcode", "destroy-sessions", "install-plugin", "update-plugin", "crop-image", "generate-password", "save-wporg-username", "delete-plugin", "search-plugins", "search-install-plugins", "activate-plugin", "update-theme", "delete-theme", "install-theme", "get-post-thumbnail-html", "get-community-events", "edit-theme-plugin-file", "wp-privacy-export-personal-data", "wp-privacy-erase-personal-data", "health-check-site-status-result", "health-check-dotorg-communication", "health-check-is-in-debug-mode", "health-check-background-updates", "health-check-loopback-requests", "health-check-get-sizes")
#// Deprecated.
core_actions_post_deprecated = Array("wp-fullscreen-save-post", "press-this-save-post", "press-this-add-category")
core_actions_post = php_array_merge(core_actions_post, core_actions_post_deprecated)
#// Register core Ajax calls.
if (not php_empty(lambda : PHP_REQUEST["action"])) and php_in_array(PHP_REQUEST["action"], core_actions_get):
    add_action("wp_ajax_" + PHP_REQUEST["action"], "wp_ajax_" + php_str_replace("-", "_", PHP_REQUEST["action"]), 1)
# end if
if (not php_empty(lambda : PHP_POST["action"])) and php_in_array(PHP_POST["action"], core_actions_post):
    add_action("wp_ajax_" + PHP_POST["action"], "wp_ajax_" + php_str_replace("-", "_", PHP_POST["action"]), 1)
# end if
add_action("wp_ajax_nopriv_heartbeat", "wp_ajax_nopriv_heartbeat", 1)
action = PHP_REQUEST["action"] if (php_isset(lambda : PHP_REQUEST["action"])) else ""
if is_user_logged_in():
    #// If no action is registered, return a Bad Request response.
    if (not has_action(str("wp_ajax_") + str(action))):
        wp_die("0", 400)
    # end if
    #// 
    #// Fires authenticated Ajax actions for logged-in users.
    #// 
    #// The dynamic portion of the hook name, `$action`, refers
    #// to the name of the Ajax action callback being fired.
    #// 
    #// @since 2.1.0
    #//
    do_action(str("wp_ajax_") + str(action))
else:
    #// If no action is registered, return a Bad Request response.
    if (not has_action(str("wp_ajax_nopriv_") + str(action))):
        wp_die("0", 400)
    # end if
    #// 
    #// Fires non-authenticated Ajax actions for logged-out users.
    #// 
    #// The dynamic portion of the hook name, `$action`, refers
    #// to the name of the Ajax action callback being fired.
    #// 
    #// @since 2.8.0
    #//
    do_action(str("wp_ajax_nopriv_") + str(action))
# end if
#// Default status.
wp_die("0")
