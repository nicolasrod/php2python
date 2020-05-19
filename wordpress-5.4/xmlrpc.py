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
#// XML-RPC protocol support for WordPress
#// 
#// @package WordPress
#// 
#// 
#// Whether this is an XML-RPC Request
#// 
#// @var bool
#//
php_define("XMLRPC_REQUEST", True)
#// Some browser-embedded clients send cookies. We don't want them.
PHP_COOKIE = Array()
#// A bug in PHP < 5.2.2 makes $HTTP_RAW_POST_DATA not set by default,
#// but we can do it ourself.
if (not (php_isset(lambda : HTTP_RAW_POST_DATA_))):
    HTTP_RAW_POST_DATA_ = php_file_get_contents("php://input")
# end if
#// Fix for mozBlog and other cases where '<?xml' isn't on the very first line.
if (php_isset(lambda : HTTP_RAW_POST_DATA_)):
    HTTP_RAW_POST_DATA_ = php_trim(HTTP_RAW_POST_DATA_)
# end if
#// Include the bootstrap for setting up WordPress environment
php_include_file(__DIR__ + "/wp-load.php", once=True)
if (php_isset(lambda : PHP_REQUEST["rsd"])):
    #// http://cyber.law.harvard.edu/blogs/gems/tech/rsd.html
    php_header("Content-Type: text/xml; charset=" + get_option("blog_charset"), True)
    php_print("<?xml version=\"1.0\" encoding=\"" + get_option("blog_charset") + "\"?" + ">")
    php_print("""<rsd version=\"1.0\" xmlns=\"http://archipelago.phrasewise.com/rsd\">
    <service>
    <engineName>WordPress</engineName>
    <engineLink>https://wordpress.org/</engineLink>
    <homePageLink>""")
    bloginfo_rss("url")
    php_print("</homePageLink>\n        <apis>\n            <api name=\"WordPress\" blogID=\"1\" preferred=\"true\" apiLink=\"")
    php_print(site_url("xmlrpc.php", "rpc"))
    php_print("\" />\n          <api name=\"Movable Type\" blogID=\"1\" preferred=\"false\" apiLink=\"")
    php_print(site_url("xmlrpc.php", "rpc"))
    php_print("\" />\n          <api name=\"MetaWeblog\" blogID=\"1\" preferred=\"false\" apiLink=\"")
    php_print(site_url("xmlrpc.php", "rpc"))
    php_print("\" />\n          <api name=\"Blogger\" blogID=\"1\" preferred=\"false\" apiLink=\"")
    php_print(site_url("xmlrpc.php", "rpc"))
    php_print("\" />\n          ")
    #// 
    #// Add additional APIs to the Really Simple Discovery (RSD) endpoint.
    #// 
    #// @link http://cyber.law.harvard.edu/blogs/gems/tech/rsd.html
    #// 
    #// @since 3.5.0
    #//
    do_action("xmlrpc_rsd_apis")
    php_print("""       </apis>
    </service>
    </rsd>
    """)
    php_exit(0)
# end if
php_include_file(ABSPATH + "wp-admin/includes/admin.php", once=True)
php_include_file(ABSPATH + WPINC + "/class-IXR.php", once=True)
php_include_file(ABSPATH + WPINC + "/class-wp-xmlrpc-server.php", once=True)
#// 
#// Posts submitted via the XML-RPC interface get that title
#// 
#// @name post_default_title
#// @var string
#//
post_default_title_ = ""
#// 
#// Filters the class used for handling XML-RPC requests.
#// 
#// @since 3.1.0
#// 
#// @param string $class The name of the XML-RPC server class.
#//
wp_xmlrpc_server_class_ = apply_filters("wp_xmlrpc_server_class", "wp_xmlrpc_server")
wp_xmlrpc_server_ = php_new_class(wp_xmlrpc_server_class_, lambda : {**locals(), **globals()}[wp_xmlrpc_server_class_]())
#// Fire off the request.
wp_xmlrpc_server_.serve_request()
php_exit(0)
#// 
#// logIO() - Writes logging info to a file.
#// 
#// @deprecated 3.4.0 Use error_log()
#// @see error_log()
#// 
#// @param string $io Whether input or output
#// @param string $msg Information describing logging reason.
#//
def logIO(io_=None, msg_=None, *_args_):
    
    
    #// phpcs:ignore WordPress.NamingConventions.ValidFunctionName.FunctionNameInvalid
    _deprecated_function(inspect.currentframe().f_code.co_name, "3.4.0", "error_log()")
    if (not php_empty(lambda : PHP_GLOBALS["xmlrpc_logging"])):
        php_error_log(io_ + " - " + msg_)
    # end if
# end def logIO
