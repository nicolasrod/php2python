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
#// The searchform.php template.
#// 
#// Used any time that get_search_form() is called.
#// 
#// @link https://developer.wordpress.org/themes/basics/template-hierarchy
#// 
#// @package WordPress
#// @subpackage Twenty_Twenty
#// @since Twenty Twenty 1.0
#// 
#// 
#// Generate a unique ID for each form and a string containing an aria-label
#// if one was passed to get_search_form() in the args array.
#//
twentytwenty_unique_id = twentytwenty_unique_id("search-form-")
twentytwenty_aria_label = "aria-label=\"" + esc_attr(args["label"]) + "\"" if (not php_empty(lambda : args["label"])) else ""
php_print("<form role=\"search\" ")
php_print(twentytwenty_aria_label)
pass
php_print(" method=\"get\" class=\"search-form\" action=\"")
php_print(esc_url(home_url("/")))
php_print("\">\n    <label for=\"")
php_print(esc_attr(twentytwenty_unique_id))
php_print("\">\n        <span class=\"screen-reader-text\">")
_e("Search for:", "twentytwenty")
pass
php_print("</span>\n        <input type=\"search\" id=\"")
php_print(esc_attr(twentytwenty_unique_id))
php_print("\" class=\"search-field\" placeholder=\"")
php_print(esc_attr_x("Search &hellip;", "placeholder", "twentytwenty"))
php_print("\" value=\"")
php_print(get_search_query())
php_print("\" name=\"s\" />\n   </label>\n  <input type=\"submit\" class=\"search-submit\" value=\"")
php_print(esc_attr_x("Search", "submit button", "twentytwenty"))
php_print("\" />\n</form>\n")
