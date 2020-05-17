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
#// Press This Display and Handler.
#// 
#// @package WordPress
#// @subpackage Press_This
#//
php_define("IFRAME_REQUEST", True)
#// WordPress Administration Bootstrap
php_include_file(__DIR__ + "/admin.php", once=True)
def wp_load_press_this(*_args_):
    
    
    plugin_slug_ = "press-this"
    plugin_file_ = "press-this/press-this-plugin.php"
    if (not current_user_can("edit_posts")) or (not current_user_can(get_post_type_object("post").cap.create_posts)):
        wp_die(__("Sorry, you are not allowed to create posts as this user."), __("You need a higher level of permission."), 403)
    elif is_plugin_active(plugin_file_):
        php_include_file(WP_PLUGIN_DIR + "/press-this/class-wp-press-this-plugin.php", once=False)
        wp_press_this_ = php_new_class("WP_Press_This_Plugin", lambda : WP_Press_This_Plugin())
        wp_press_this_.html()
    elif current_user_can("activate_plugins"):
        if php_file_exists(WP_PLUGIN_DIR + "/" + plugin_file_):
            url_ = wp_nonce_url(add_query_arg(Array({"action": "activate", "plugin": plugin_file_, "from": "press-this"}), admin_url("plugins.php")), "activate-plugin_" + plugin_file_)
            action_ = php_sprintf("<a href=\"%1$s\" aria-label=\"%2$s\">%2$s</a>", esc_url(url_), __("Activate Press This"))
        else:
            if is_main_site():
                url_ = wp_nonce_url(add_query_arg(Array({"action": "install-plugin", "plugin": plugin_slug_, "from": "press-this"}), self_admin_url("update.php")), "install-plugin_" + plugin_slug_)
                action_ = php_sprintf("<a href=\"%1$s\" class=\"install-now\" data-slug=\"%2$s\" data-name=\"%2$s\" aria-label=\"%3$s\">%3$s</a>", esc_url(url_), esc_attr(plugin_slug_), __("Install Now"))
            else:
                action_ = php_sprintf(__("Press This is not installed. Please install Press This from <a href=\"%s\">the main site</a>."), get_admin_url(get_current_network_id(), "press-this.php"))
            # end if
        # end if
        wp_die(__("The Press This plugin is required.") + "<br />" + action_, __("Installation Required"), 200)
    else:
        wp_die(__("Press This is not available. Please contact your site administrator."), __("Installation Required"), 200)
    # end if
# end def wp_load_press_this
wp_load_press_this()
