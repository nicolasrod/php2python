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
#// Defines constants and global variables that can be overridden, generally in wp-config.php.
#// 
#// @package WordPress
#// @subpackage Multisite
#// @since 3.0.0
#// 
#// 
#// Defines Multisite upload constants.
#// 
#// Exists for backward compatibility with legacy file-serving through
#// wp-includes/ms-files.php (wp-content/blogs.php in MU).
#// 
#// @since 3.0.0
#//
def ms_upload_constants(*_args_):
    
    
    #// This filter is attached in ms-default-filters.php but that file is not included during SHORTINIT.
    add_filter("default_site_option_ms_files_rewriting", "__return_true")
    if (not get_site_option("ms_files_rewriting")):
        return
    # end if
    #// Base uploads dir relative to ABSPATH.
    if (not php_defined("UPLOADBLOGSDIR")):
        php_define("UPLOADBLOGSDIR", "wp-content/blogs.dir")
    # end if
    #// Note, the main site in a post-MU network uses wp-content/uploads.
    #// This is handled in wp_upload_dir() by ignoring UPLOADS for this case.
    if (not php_defined("UPLOADS")):
        site_id_ = get_current_blog_id()
        php_define("UPLOADS", UPLOADBLOGSDIR + "/" + site_id_ + "/files/")
        #// Uploads dir relative to ABSPATH.
        if "wp-content/blogs.dir" == UPLOADBLOGSDIR and (not php_defined("BLOGUPLOADDIR")):
            php_define("BLOGUPLOADDIR", WP_CONTENT_DIR + "/blogs.dir/" + site_id_ + "/files/")
        # end if
    # end if
# end def ms_upload_constants
#// 
#// Defines Multisite cookie constants.
#// 
#// @since 3.0.0
#//
def ms_cookie_constants(*_args_):
    
    
    current_network_ = get_network()
    #// 
    #// @since 1.2.0
    #//
    if (not php_defined("COOKIEPATH")):
        php_define("COOKIEPATH", current_network_.path)
    # end if
    #// 
    #// @since 1.5.0
    #//
    if (not php_defined("SITECOOKIEPATH")):
        php_define("SITECOOKIEPATH", current_network_.path)
    # end if
    #// 
    #// @since 2.6.0
    #//
    if (not php_defined("ADMIN_COOKIE_PATH")):
        if (not is_subdomain_install()) or php_trim(php_parse_url(get_option("siteurl"), PHP_URL_PATH), "/"):
            php_define("ADMIN_COOKIE_PATH", SITECOOKIEPATH)
        else:
            php_define("ADMIN_COOKIE_PATH", SITECOOKIEPATH + "wp-admin")
        # end if
    # end if
    #// 
    #// @since 2.0.0
    #//
    if (not php_defined("COOKIE_DOMAIN")) and is_subdomain_install():
        if (not php_empty(lambda : current_network_.cookie_domain)):
            php_define("COOKIE_DOMAIN", "." + current_network_.cookie_domain)
        else:
            php_define("COOKIE_DOMAIN", "." + current_network_.domain)
        # end if
    # end if
# end def ms_cookie_constants
#// 
#// Defines Multisite file constants.
#// 
#// Exists for backward compatibility with legacy file-serving through
#// wp-includes/ms-files.php (wp-content/blogs.php in MU).
#// 
#// @since 3.0.0
#//
def ms_file_constants(*_args_):
    
    
    #// 
    #// Optional support for X-Sendfile header
    #// 
    #// @since 3.0.0
    #//
    if (not php_defined("WPMU_SENDFILE")):
        php_define("WPMU_SENDFILE", False)
    # end if
    #// 
    #// Optional support for X-Accel-Redirect header
    #// 
    #// @since 3.0.0
    #//
    if (not php_defined("WPMU_ACCEL_REDIRECT")):
        php_define("WPMU_ACCEL_REDIRECT", False)
    # end if
# end def ms_file_constants
#// 
#// Defines Multisite subdomain constants and handles warnings and notices.
#// 
#// VHOST is deprecated in favor of SUBDOMAIN_INSTALL, which is a bool.
#// 
#// On first call, the constants are checked and defined. On second call,
#// we will have translations loaded and can trigger warnings easily.
#// 
#// @since 3.0.0
#// 
#// @staticvar bool $subdomain_error
#// @staticvar bool $subdomain_error_warn
#//
def ms_subdomain_constants(*_args_):
    
    
    subdomain_error_ = None
    subdomain_error_warn_ = None
    if False == subdomain_error_:
        return
    # end if
    if subdomain_error_:
        vhost_deprecated_ = php_sprintf(__("The constant %1$s <strong>is deprecated</strong>. Use the boolean constant %2$s in %3$s to enable a subdomain configuration. Use %4$s to check whether a subdomain configuration is enabled."), "<code>VHOST</code>", "<code>SUBDOMAIN_INSTALL</code>", "<code>wp-config.php</code>", "<code>is_subdomain_install()</code>")
        if subdomain_error_warn_:
            trigger_error(__("<strong>Conflicting values for the constants VHOST and SUBDOMAIN_INSTALL.</strong> The value of SUBDOMAIN_INSTALL will be assumed to be your subdomain configuration setting.") + " " + vhost_deprecated_, E_USER_WARNING)
        else:
            _deprecated_argument("define()", "3.0.0", vhost_deprecated_)
        # end if
        return
    # end if
    if php_defined("SUBDOMAIN_INSTALL") and php_defined("VHOST"):
        subdomain_error_ = True
        if SUBDOMAIN_INSTALL != "yes" == VHOST:
            subdomain_error_warn_ = True
        # end if
    elif php_defined("SUBDOMAIN_INSTALL"):
        subdomain_error_ = False
        php_define("VHOST", "yes" if SUBDOMAIN_INSTALL else "no")
    elif php_defined("VHOST"):
        subdomain_error_ = True
        php_define("SUBDOMAIN_INSTALL", "yes" == VHOST)
    else:
        subdomain_error_ = False
        php_define("SUBDOMAIN_INSTALL", False)
        php_define("VHOST", "no")
    # end if
# end def ms_subdomain_constants
