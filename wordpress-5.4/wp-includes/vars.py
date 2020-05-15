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
global pagenow,is_lynx,is_gecko,is_winIE,is_macIE,is_opera,is_NS4,is_safari,is_chrome,is_iphone,is_IE,is_edge,is_apache,is_IIS,is_iis7,is_nginx
php_check_if_defined("pagenow","is_lynx","is_gecko","is_winIE","is_macIE","is_opera","is_NS4","is_safari","is_chrome","is_iphone","is_IE","is_edge","is_apache","is_IIS","is_iis7","is_nginx")
#// On which page are we?
if is_admin():
    #// wp-admin pages are checked more carefully.
    if is_network_admin():
        php_preg_match("#/wp-admin/network/?(.*?)$#i", PHP_SERVER["PHP_SELF"], self_matches)
    elif is_user_admin():
        php_preg_match("#/wp-admin/user/?(.*?)$#i", PHP_SERVER["PHP_SELF"], self_matches)
    else:
        php_preg_match("#/wp-admin/?(.*?)$#i", PHP_SERVER["PHP_SELF"], self_matches)
    # end if
    pagenow = self_matches[1]
    pagenow = php_trim(pagenow, "/")
    pagenow = php_preg_replace("#\\?.*?$#", "", pagenow)
    if "" == pagenow or "index" == pagenow or "index.php" == pagenow:
        pagenow = "index.php"
    else:
        php_preg_match("#(.*?)(/|$)#", pagenow, self_matches)
        pagenow = php_strtolower(self_matches[1])
        if ".php" != php_substr(pagenow, -4, 4):
            pagenow += ".php"
            pass
        # end if
    # end if
else:
    if php_preg_match("#([^/]+\\.php)([?/].*?)?$#i", PHP_SERVER["PHP_SELF"], self_matches):
        pagenow = php_strtolower(self_matches[1])
    else:
        pagenow = "index.php"
    # end if
# end if
self_matches = None
#// Simple browser detection.
is_lynx = False
is_gecko = False
is_winIE = False
is_macIE = False
is_opera = False
is_NS4 = False
is_safari = False
is_chrome = False
is_iphone = False
is_edge = False
if (php_isset(lambda : PHP_SERVER["HTTP_USER_AGENT"])):
    if php_strpos(PHP_SERVER["HTTP_USER_AGENT"], "Lynx") != False:
        is_lynx = True
    elif php_strpos(PHP_SERVER["HTTP_USER_AGENT"], "Edge") != False:
        is_edge = True
    elif php_stripos(PHP_SERVER["HTTP_USER_AGENT"], "chrome") != False:
        if php_stripos(PHP_SERVER["HTTP_USER_AGENT"], "chromeframe") != False:
            is_admin = is_admin()
            #// 
            #// Filters whether Google Chrome Frame should be used, if available.
            #// 
            #// @since 3.2.0
            #// 
            #// @param bool $is_admin Whether to use the Google Chrome Frame. Default is the value of is_admin().
            #//
            is_chrome = apply_filters("use_google_chrome_frame", is_admin)
            if is_chrome:
                php_header("X-UA-Compatible: chrome=1")
            # end if
            is_winIE = (not is_chrome)
        else:
            is_chrome = True
        # end if
    elif php_stripos(PHP_SERVER["HTTP_USER_AGENT"], "safari") != False:
        is_safari = True
    elif php_strpos(PHP_SERVER["HTTP_USER_AGENT"], "MSIE") != False or php_strpos(PHP_SERVER["HTTP_USER_AGENT"], "Trident") != False and php_strpos(PHP_SERVER["HTTP_USER_AGENT"], "Win") != False:
        is_winIE = True
    elif php_strpos(PHP_SERVER["HTTP_USER_AGENT"], "MSIE") != False and php_strpos(PHP_SERVER["HTTP_USER_AGENT"], "Mac") != False:
        is_macIE = True
    elif php_strpos(PHP_SERVER["HTTP_USER_AGENT"], "Gecko") != False:
        is_gecko = True
    elif php_strpos(PHP_SERVER["HTTP_USER_AGENT"], "Opera") != False:
        is_opera = True
    elif php_strpos(PHP_SERVER["HTTP_USER_AGENT"], "Nav") != False and php_strpos(PHP_SERVER["HTTP_USER_AGENT"], "Mozilla/4.") != False:
        is_NS4 = True
    # end if
# end if
if is_safari and php_stripos(PHP_SERVER["HTTP_USER_AGENT"], "mobile") != False:
    is_iphone = True
# end if
is_IE = is_macIE or is_winIE
#// Server detection.
#// 
#// Whether the server software is Apache or something else
#// 
#// @global bool $is_apache
#//
is_apache = php_strpos(PHP_SERVER["SERVER_SOFTWARE"], "Apache") != False or php_strpos(PHP_SERVER["SERVER_SOFTWARE"], "LiteSpeed") != False
#// 
#// Whether the server software is Nginx or something else
#// 
#// @global bool $is_nginx
#//
is_nginx = php_strpos(PHP_SERVER["SERVER_SOFTWARE"], "nginx") != False
#// 
#// Whether the server software is IIS or something else
#// 
#// @global bool $is_IIS
#//
is_IIS = (not is_apache) and php_strpos(PHP_SERVER["SERVER_SOFTWARE"], "Microsoft-IIS") != False or php_strpos(PHP_SERVER["SERVER_SOFTWARE"], "ExpressionDevServer") != False
#// 
#// Whether the server software is IIS 7.X or greater
#// 
#// @global bool $is_iis7
#//
is_iis7 = is_IIS and php_intval(php_substr(PHP_SERVER["SERVER_SOFTWARE"], php_strpos(PHP_SERVER["SERVER_SOFTWARE"], "Microsoft-IIS/") + 14)) >= 7
#// 
#// Test if the current browser runs on a mobile device (smart phone, tablet, etc.)
#// 
#// @since 3.4.0
#// 
#// @return bool
#//
def wp_is_mobile(*args_):
    
    if php_empty(lambda : PHP_SERVER["HTTP_USER_AGENT"]):
        is_mobile = False
    elif php_strpos(PHP_SERVER["HTTP_USER_AGENT"], "Mobile") != False or php_strpos(PHP_SERVER["HTTP_USER_AGENT"], "Android") != False or php_strpos(PHP_SERVER["HTTP_USER_AGENT"], "Silk/") != False or php_strpos(PHP_SERVER["HTTP_USER_AGENT"], "Kindle") != False or php_strpos(PHP_SERVER["HTTP_USER_AGENT"], "BlackBerry") != False or php_strpos(PHP_SERVER["HTTP_USER_AGENT"], "Opera Mini") != False or php_strpos(PHP_SERVER["HTTP_USER_AGENT"], "Opera Mobi") != False:
        is_mobile = True
    else:
        is_mobile = False
    # end if
    #// 
    #// Filters whether the request should be treated as coming from a mobile device or not.
    #// 
    #// @since 4.9.0
    #// 
    #// @param bool $is_mobile Whether the request is from a mobile device or not.
    #//
    return apply_filters("wp_is_mobile", is_mobile)
# end def wp_is_mobile
