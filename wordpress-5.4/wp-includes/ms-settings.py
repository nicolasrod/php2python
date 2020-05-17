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
#// the Multisite procedural and class library.
#// 
#// Allows for some configuration in wp-config.php (see ms-default-constants.php)
#// 
#// @package WordPress
#// @subpackage Multisite
#// @since 3.0.0
#// 
#// 
#// Objects representing the current network and current site.
#// 
#// These may be populated through a custom `sunrise.php`. If not, then this
#// file will attempt to populate them based on the current request.
#// 
#// @global WP_Network $current_site The current network.
#// @global object     $current_blog The current site.
#// @global string     $domain       Deprecated. The domain of the site found on load.
#// Use `get_site()->domain` instead.
#// @global string     $path         Deprecated. The path of the site found on load.
#// Use `get_site()->path` instead.
#// @global int        $site_id      Deprecated. The ID of the network found on load.
#// Use `get_current_network_id()` instead.
#// @global bool       $public       Deprecated. Whether the site found on load is public.
#// Use `get_site()->public` instead.
#// 
#// @since 3.0.0
#//
global current_site_
global current_blog_
global domain_
global path_
global site_id_
global public_
php_check_if_defined("current_site_","current_blog_","domain_","path_","site_id_","public_")
#// WP_Network class
php_include_file(ABSPATH + WPINC + "/class-wp-network.php", once=True)
#// WP_Site class
php_include_file(ABSPATH + WPINC + "/class-wp-site.php", once=True)
#// Multisite loader
php_include_file(ABSPATH + WPINC + "/ms-load.php", once=True)
#// Default Multisite constants
php_include_file(ABSPATH + WPINC + "/ms-default-constants.php", once=True)
if php_defined("SUNRISE"):
    php_include_file(WP_CONTENT_DIR + "/sunrise.php", once=False)
# end if
#// Check for and define SUBDOMAIN_INSTALL and the deprecated VHOST constant.
ms_subdomain_constants()
#// This block will process a request if the current network or current site objects
#// have not been populated in the global scope through something like `sunrise.php`.
if (not (php_isset(lambda : current_site_))) or (not (php_isset(lambda : current_blog_))):
    domain_ = php_strtolower(stripslashes(PHP_SERVER["HTTP_HOST"]))
    if php_substr(domain_, -3) == ":80":
        domain_ = php_substr(domain_, 0, -3)
        PHP_SERVER["HTTP_HOST"] = php_substr(PHP_SERVER["HTTP_HOST"], 0, -3)
    elif php_substr(domain_, -4) == ":443":
        domain_ = php_substr(domain_, 0, -4)
        PHP_SERVER["HTTP_HOST"] = php_substr(PHP_SERVER["HTTP_HOST"], 0, -4)
    # end if
    path_ = stripslashes(PHP_SERVER["REQUEST_URI"])
    if is_admin():
        path_ = php_preg_replace("#(.*)/wp-admin/.*#", "$1/", path_)
    # end if
    path_ = php_explode("?", path_)
    bootstrap_result_ = ms_load_current_site_and_network(domain_, path_, is_subdomain_install())
    if True == bootstrap_result_:
        pass
    elif False == bootstrap_result_:
        ms_not_installed(domain_, path_)
    else:
        php_header("Location: " + bootstrap_result_)
        php_exit(0)
    # end if
    bootstrap_result_ = None
    blog_id_ = current_blog_.blog_id
    public_ = current_blog_.public
    if php_empty(lambda : current_blog_.site_id):
        #// This dates to [MU134] and shouldn't be relevant anymore,
        #// but it could be possible for arguments passed to insert_blog() etc.
        current_blog_.site_id = 1
    # end if
    site_id_ = current_blog_.site_id
    wp_load_core_site_options(site_id_)
# end if
wpdb_.set_prefix(table_prefix_, False)
#// $table_prefix can be set in sunrise.php.
wpdb_.set_blog_id(current_blog_.blog_id, current_blog_.site_id)
table_prefix_ = wpdb_.get_blog_prefix()
_wp_switched_stack_ = Array()
switched_ = False
#// Need to init cache again after blog_id is set.
wp_start_object_cache()
if (not type(current_site_).__name__ == "WP_Network"):
    current_site_ = php_new_class("WP_Network", lambda : WP_Network(current_site_))
# end if
if (not type(current_blog_).__name__ == "WP_Site"):
    current_blog_ = php_new_class("WP_Site", lambda : WP_Site(current_blog_))
# end if
#// Define upload directory constants.
ms_upload_constants()
#// 
#// Fires after the current site and network have been detected and loaded
#// in multisite's bootstrap.
#// 
#// @since 4.6.0
#//
do_action("ms_loaded")
