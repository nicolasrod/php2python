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
#// Disable error reporting
#// 
#// Set this to error_reporting( -1 ) for debugging.
#//
php_error_reporting(0)
#// Set ABSPATH for execution
if (not php_defined("ABSPATH")):
    php_define("ABSPATH", php_dirname(__DIR__) + "/")
# end if
php_define("WPINC", "wp-includes")
protocol = PHP_SERVER["SERVER_PROTOCOL"]
if (not php_in_array(protocol, Array("HTTP/1.1", "HTTP/2", "HTTP/2.0"))):
    protocol = "HTTP/1.0"
# end if
load = PHP_REQUEST["load"]
if php_is_array(load):
    ksort(load)
    load = php_implode("", load)
# end if
load = php_preg_replace("/[^a-z0-9,_-]+/i", "", load)
load = array_unique(php_explode(",", load))
if php_empty(lambda : load):
    php_header(str(protocol) + str(" 400 Bad Request"))
    php_exit(0)
# end if
php_include_file(ABSPATH + "wp-admin/includes/noop.php", once=False)
php_include_file(ABSPATH + WPINC + "/script-loader.php", once=False)
php_include_file(ABSPATH + WPINC + "/version.php", once=False)
expires_offset = 31536000
#// 1 year.
out = ""
wp_scripts = php_new_class("WP_Scripts", lambda : WP_Scripts())
wp_default_scripts(wp_scripts)
wp_default_packages_vendor(wp_scripts)
wp_default_packages_scripts(wp_scripts)
if (php_isset(lambda : PHP_SERVER["HTTP_IF_NONE_MATCH"])) and stripslashes(PHP_SERVER["HTTP_IF_NONE_MATCH"]) == wp_version:
    php_header(str(protocol) + str(" 304 Not Modified"))
    php_exit(0)
# end if
for handle in load:
    if (not php_array_key_exists(handle, wp_scripts.registered)):
        continue
    # end if
    path = ABSPATH + wp_scripts.registered[handle].src
    out += get_file(path) + "\n"
# end for
php_header(str("Etag: ") + str(wp_version))
php_header("Content-Type: application/javascript; charset=UTF-8")
php_header("Expires: " + gmdate("D, d M Y H:i:s", time() + expires_offset) + " GMT")
php_header(str("Cache-Control: public, max-age=") + str(expires_offset))
php_print(out)
php_exit(0)
