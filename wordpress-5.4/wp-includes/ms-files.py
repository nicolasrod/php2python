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
#// Multisite upload handler.
#// 
#// @since 3.0.0
#// 
#// @package WordPress
#// @subpackage Multisite
#//
php_define("SHORTINIT", True)
php_include_file(php_dirname(__DIR__) + "/wp-load.php", once=True)
if (not is_multisite()):
    php_print("Multisite support not enabled")
    php_exit()
# end if
ms_file_constants()
php_error_reporting(0)
if "1" == current_blog_.archived or "1" == current_blog_.spam or "1" == current_blog_.deleted:
    status_header(404)
    php_print("404 &#8212; File not found.")
    php_exit()
# end if
file_ = php_rtrim(BLOGUPLOADDIR, "/") + "/" + php_str_replace("..", "", PHP_REQUEST["file"])
if (not php_is_file(file_)):
    status_header(404)
    php_print("404 &#8212; File not found.")
    php_exit()
# end if
mime_ = wp_check_filetype(file_)
if False == mime_["type"] and php_function_exists("mime_content_type"):
    mime_["type"] = mime_content_type(file_)
# end if
if mime_["type"]:
    mimetype_ = mime_["type"]
else:
    mimetype_ = "image/" + php_substr(file_, php_strrpos(file_, ".") + 1)
# end if
php_header("Content-Type: " + mimetype_)
#// Always send this.
if False == php_strpos(PHP_SERVER["SERVER_SOFTWARE"], "Microsoft-IIS"):
    php_header("Content-Length: " + filesize(file_))
# end if
#// Optional support for X-Sendfile and X-Accel-Redirect.
if WPMU_ACCEL_REDIRECT:
    php_header("X-Accel-Redirect: " + php_str_replace(WP_CONTENT_DIR, "", file_))
    php_exit(0)
elif WPMU_SENDFILE:
    php_header("X-Sendfile: " + file_)
    php_exit(0)
# end if
last_modified_ = gmdate("D, d M Y H:i:s", filemtime(file_))
etag_ = "\"" + php_md5(last_modified_) + "\""
php_header(str("Last-Modified: ") + str(last_modified_) + str(" GMT"))
php_header("ETag: " + etag_)
php_header("Expires: " + gmdate("D, d M Y H:i:s", time() + 100000000) + " GMT")
#// Support for conditional GET - use stripslashes() to avoid formatting.php dependency.
client_etag_ = stripslashes(PHP_SERVER["HTTP_IF_NONE_MATCH"]) if (php_isset(lambda : PHP_SERVER["HTTP_IF_NONE_MATCH"])) else False
if (not (php_isset(lambda : PHP_SERVER["HTTP_IF_MODIFIED_SINCE"]))):
    PHP_SERVER["HTTP_IF_MODIFIED_SINCE"] = False
# end if
client_last_modified_ = php_trim(PHP_SERVER["HTTP_IF_MODIFIED_SINCE"])
#// If string is empty, return 0. If not, attempt to parse into a timestamp.
client_modified_timestamp_ = strtotime(client_last_modified_) if client_last_modified_ else 0
#// Make a timestamp for our most recent modification...
modified_timestamp_ = strtotime(last_modified_)
if client_modified_timestamp_ >= modified_timestamp_ and client_etag_ == etag_ if client_last_modified_ and client_etag_ else client_modified_timestamp_ >= modified_timestamp_ or client_etag_ == etag_:
    status_header(304)
    php_exit(0)
# end if
#// If we made it this far, just serve the file.
readfile(file_)
flush()
