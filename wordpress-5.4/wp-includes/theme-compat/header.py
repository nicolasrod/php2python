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
#// @package WordPress
#// @subpackage Theme_Compat
#// @deprecated 3.0.0
#// 
#// This file is here for backward compatibility with old themes and will be removed in a future version.
#//
_deprecated_file(php_sprintf(__("Theme without %s"), php_basename(__FILE__)), "3.0.0", None, php_sprintf(__("Please include a %s template in your theme."), php_basename(__FILE__)))
php_print("<!DOCTYPE html>\n<html xmlns=\"http://www.w3.org/1999/xhtml\" ")
language_attributes()
php_print(""">
<head>
<link rel=\"profile\" href=\"http://gmpg.org/xfn/11\" />
<meta http-equiv=\"Content-Type\" content=\"""")
bloginfo("html_type")
php_print("; charset=")
bloginfo("charset")
php_print("\" />\n\n<title>")
php_print(wp_get_document_title())
php_print("</title>\n\n<link rel=\"stylesheet\" href=\"")
bloginfo("stylesheet_url")
php_print("\" type=\"text/css\" media=\"screen\" />\n<link rel=\"pingback\" href=\"")
bloginfo("pingback_url")
php_print("\" />\n\n")
if php_file_exists(get_stylesheet_directory() + "/images/kubrickbgwide.jpg"):
    php_print("<style type=\"text/css\" media=\"screen\">\n\n   ")
    #// Checks to see whether it needs a sidebar.
    if php_empty(lambda : withcomments) and (not is_single()):
        php_print(" #page { background: url(\"")
        bloginfo("stylesheet_directory")
        php_print("/images/kubrickbg-")
        bloginfo("text_direction")
        php_print(".jpg\") repeat-y top; border: none; }\n")
    else:
        pass
        php_print(" #page { background: url(\"")
        bloginfo("stylesheet_directory")
        php_print("/images/kubrickbgwide.jpg\") repeat-y top; border: none; }\n")
    # end if
    php_print("\n</style>\n")
# end if
php_print("\n")
if is_singular():
    wp_enqueue_script("comment-reply")
# end if
php_print("\n")
wp_head()
php_print("</head>\n<body ")
body_class()
php_print(""">
<div id=\"page\">
<div id=\"header\" role=\"banner\">
<div id=\"headerimg\">
<h1><a href=\"""")
php_print(home_url())
php_print("/\">")
bloginfo("name")
php_print("</a></h1>\n      <div class=\"description\">")
bloginfo("description")
php_print("""</div>
</div>
</div>
<hr />
""")
