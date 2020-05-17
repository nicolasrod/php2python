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
#// Creates common globals for the rest of WordPress
#// 
#// Sets $pagenow global which is the current page. Checks
#// for the browser to set which one is currently being used.
#// 
#// Detects which user environment WordPress is being used on.
#// Only attempts to check for Apache, Nginx and IIS -- three web
#// servers with known pretty permalink capability.
#// 
#// Note: Though Nginx is detected, WordPress does not currently
#// generate rewrite rules for it. See https://wordpress.org/support/article/nginx
#// 
#// @package WordPress
#//
global pagenow_
global is_lynx_
global is_gecko_
global is_winIE_
global is_macIE_
global is_opera_
global is_NS4_
global is_safari_
global is_chrome_
global is_iphone_
global is_IE_
global is_edge_
global is_apache_
global is_IIS_
global is_iis7_
global is_nginx_
php_check_if_defined("pagenow_","is_lynx_","is_gecko_","is_winIE_","is_macIE_","is_opera_","is_NS4_","is_safari_","is_chrome_","is_iphone_","is_IE_","is_edge_","is_apache_","is_IIS_","is_iis7_","is_nginx_")
#// On which page are we?
if is_admin():
    #// wp-admin pages are checked more carefully.
    if is_network_admin():
        php_preg_match("#/wp-admin/network/?(.*?)$#i", PHP_SERVER["PHP_SELF"], self_matches_)
    elif is_user_admin():
        php_preg_match("#/wp-admin/user/?(.*?)$#i", PHP_SERVER["PHP_SELF"], self_matches_)
    else:
        php_preg_match("#/wp-admin/?(.*?)$#i", PHP_SERVER["PHP_SELF"], self_matches_)
    # end if
    pagenow_ = self_matches_[1]
    pagenow_ = php_trim(pagenow_, "/")
    pagenow_ = php_preg_replace("#\\?.*?$#", "", pagenow_)
    if "" == pagenow_ or "index" == pagenow_ or "index.php" == pagenow_:
        pagenow_ = "index.php"
    else:
        php_preg_match("#(.*?)(/|$)#", pagenow_, self_matches_)
        pagenow_ = php_strtolower(self_matches_[1])
        if ".php" != php_substr(pagenow_, -4, 4):
            pagenow_ += ".php"
            pass
        # end if
    # end if
else:
    if php_preg_match("#([^/]+\\.php)([?/].*?)?$#i", PHP_SERVER["PHP_SELF"], self_matches_):
        pagenow_ = php_strtolower(self_matches_[1])
    else:
        pagenow_ = "index.php"
    # end if
# end if
self_matches_ = None
#// Simple browser detection.
is_lynx_ = False
is_gecko_ = False
is_winIE_ = False
is_macIE_ = False
is_opera_ = False
is_NS4_ = False
is_safari_ = False
is_chrome_ = False
is_iphone_ = False
is_edge_ = False
if (php_isset(lambda : PHP_SERVER["HTTP_USER_AGENT"])):
    if php_strpos(PHP_SERVER["HTTP_USER_AGENT"], "Lynx") != False:
        is_lynx_ = True
    elif php_strpos(PHP_SERVER["HTTP_USER_AGENT"], "Edge") != False:
        is_edge_ = True
    elif php_stripos(PHP_SERVER["HTTP_USER_AGENT"], "chrome") != False:
        if php_stripos(PHP_SERVER["HTTP_USER_AGENT"], "chromeframe") != False:
            is_admin_ = is_admin()
            #// 
            #// Filters whether Google Chrome Frame should be used, if available.
            #// 
            #// @since 3.2.0
            #// 
            #// @param bool $is_admin Whether to use the Google Chrome Frame. Default is the value of is_admin().
            #//
            is_chrome_ = apply_filters("use_google_chrome_frame", is_admin_)
            if is_chrome_:
                php_header("X-UA-Compatible: chrome=1")
            # end if
            is_winIE_ = (not is_chrome_)
        else:
            is_chrome_ = True
        # end if
    elif php_stripos(PHP_SERVER["HTTP_USER_AGENT"], "safari") != False:
        is_safari_ = True
    elif php_strpos(PHP_SERVER["HTTP_USER_AGENT"], "MSIE") != False or php_strpos(PHP_SERVER["HTTP_USER_AGENT"], "Trident") != False and php_strpos(PHP_SERVER["HTTP_USER_AGENT"], "Win") != False:
        is_winIE_ = True
    elif php_strpos(PHP_SERVER["HTTP_USER_AGENT"], "MSIE") != False and php_strpos(PHP_SERVER["HTTP_USER_AGENT"], "Mac") != False:
        is_macIE_ = True
    elif php_strpos(PHP_SERVER["HTTP_USER_AGENT"], "Gecko") != False:
        is_gecko_ = True
    elif php_strpos(PHP_SERVER["HTTP_USER_AGENT"], "Opera") != False:
        is_opera_ = True
    elif php_strpos(PHP_SERVER["HTTP_USER_AGENT"], "Nav") != False and php_strpos(PHP_SERVER["HTTP_USER_AGENT"], "Mozilla/4.") != False:
        is_NS4_ = True
    # end if
# end if
if is_safari_ and php_stripos(PHP_SERVER["HTTP_USER_AGENT"], "mobile") != False:
    is_iphone_ = True
# end if
is_IE_ = is_macIE_ or is_winIE_
#// Server detection.
#// 
#// Whether the server software is Apache or something else
#// 
#// @global bool $is_apache
#//
is_apache_ = php_strpos(PHP_SERVER["SERVER_SOFTWARE"], "Apache") != False or php_strpos(PHP_SERVER["SERVER_SOFTWARE"], "LiteSpeed") != False
#// 
#// Whether the server software is Nginx or something else
#// 
#// @global bool $is_nginx
#//
is_nginx_ = php_strpos(PHP_SERVER["SERVER_SOFTWARE"], "nginx") != False
#// 
#// Whether the server software is IIS or something else
#// 
#// @global bool $is_IIS
#//
is_IIS_ = (not is_apache_) and php_strpos(PHP_SERVER["SERVER_SOFTWARE"], "Microsoft-IIS") != False or php_strpos(PHP_SERVER["SERVER_SOFTWARE"], "ExpressionDevServer") != False
#// 
#// Whether the server software is IIS 7.X or greater
#// 
#// @global bool $is_iis7
#//
is_iis7_ = is_IIS_ and php_intval(php_substr(PHP_SERVER["SERVER_SOFTWARE"], php_strpos(PHP_SERVER["SERVER_SOFTWARE"], "Microsoft-IIS/") + 14)) >= 7
#// 
#// Test if the current browser runs on a mobile device (smart phone, tablet, etc.)
#// 
#// @since 3.4.0
#// 
#// @return bool
#//
def wp_is_mobile(*_args_):
    
    
    if php_empty(lambda : PHP_SERVER["HTTP_USER_AGENT"]):
        is_mobile_ = False
    elif php_strpos(PHP_SERVER["HTTP_USER_AGENT"], "Mobile") != False or php_strpos(PHP_SERVER["HTTP_USER_AGENT"], "Android") != False or php_strpos(PHP_SERVER["HTTP_USER_AGENT"], "Silk/") != False or php_strpos(PHP_SERVER["HTTP_USER_AGENT"], "Kindle") != False or php_strpos(PHP_SERVER["HTTP_USER_AGENT"], "BlackBerry") != False or php_strpos(PHP_SERVER["HTTP_USER_AGENT"], "Opera Mini") != False or php_strpos(PHP_SERVER["HTTP_USER_AGENT"], "Opera Mobi") != False:
        is_mobile_ = True
    else:
        is_mobile_ = False
    # end if
    #// 
    #// Filters whether the request should be treated as coming from a mobile device or not.
    #// 
    #// @since 4.9.0
    #// 
    #// @param bool $is_mobile Whether the request is from a mobile device or not.
    #//
    return apply_filters("wp_is_mobile", is_mobile_)
# end def wp_is_mobile
