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
#// Disable error reporting
#// 
#// Set this to error_reporting( -1 ) for debugging
#//
php_error_reporting(0)
#// Set ABSPATH for execution
if (not php_defined("ABSPATH")):
    php_define("ABSPATH", php_dirname(__DIR__) + "/")
# end if
php_define("WPINC", "wp-includes")
php_include_file(ABSPATH + "wp-admin/includes/noop.php", once=False)
php_include_file(ABSPATH + WPINC + "/script-loader.php", once=False)
php_include_file(ABSPATH + WPINC + "/version.php", once=False)
protocol_ = PHP_SERVER["SERVER_PROTOCOL"]
if (not php_in_array(protocol_, Array("HTTP/1.1", "HTTP/2", "HTTP/2.0"))):
    protocol_ = "HTTP/1.0"
# end if
load_ = PHP_REQUEST["load"]
if php_is_array(load_):
    ksort(load_)
    load_ = php_implode("", load_)
# end if
load_ = php_preg_replace("/[^a-z0-9,_-]+/i", "", load_)
load_ = array_unique(php_explode(",", load_))
if php_empty(lambda : load_):
    php_header(str(protocol_) + str(" 400 Bad Request"))
    php_exit(0)
# end if
rtl_ = (php_isset(lambda : PHP_REQUEST["dir"])) and "rtl" == PHP_REQUEST["dir"]
expires_offset_ = 31536000
#// 1 year.
out_ = ""
wp_styles_ = php_new_class("WP_Styles", lambda : WP_Styles())
wp_default_styles(wp_styles_)
if (php_isset(lambda : PHP_SERVER["HTTP_IF_NONE_MATCH"])) and stripslashes(PHP_SERVER["HTTP_IF_NONE_MATCH"]) == wp_version_:
    php_header(str(protocol_) + str(" 304 Not Modified"))
    php_exit(0)
# end if
for handle_ in load_:
    if (not php_array_key_exists(handle_, wp_styles_.registered)):
        continue
    # end if
    style_ = wp_styles_.registered[handle_]
    if php_empty(lambda : style_.src):
        continue
    # end if
    path_ = ABSPATH + style_.src
    if rtl_ and (not php_empty(lambda : style_.extra["rtl"])):
        #// All default styles have fully independent RTL files.
        path_ = php_str_replace(".min.css", "-rtl.min.css", path_)
    # end if
    content_ = get_file(path_) + "\n"
    if php_strpos(style_.src, "/" + WPINC + "/css/") == 0:
        content_ = php_str_replace("../images/", "../" + WPINC + "/images/", content_)
        content_ = php_str_replace("../js/tinymce/", "../" + WPINC + "/js/tinymce/", content_)
        content_ = php_str_replace("../fonts/", "../" + WPINC + "/fonts/", content_)
        out_ += content_
    else:
        out_ += php_str_replace("../images/", "images/", content_)
    # end if
# end for
php_header(str("Etag: ") + str(wp_version_))
php_header("Content-Type: text/css; charset=UTF-8")
php_header("Expires: " + gmdate("D, d M Y H:i:s", time() + expires_offset_) + " GMT")
php_header(str("Cache-Control: public, max-age=") + str(expires_offset_))
php_print(out_)
php_exit(0)
