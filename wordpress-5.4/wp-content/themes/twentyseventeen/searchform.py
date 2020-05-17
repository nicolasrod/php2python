#!/usr/bin/env python3
# coding: utf-8
if '__PHP2PY_LOADED__' not in globals():
    import os
    with open(os.getenv('PHP2PY_COMPAT', 'php_compat.py')) as f:
        exec(compile(f.read(), '<string>', 'exec'))
    # end with
    globals()['__PHP2PY_LOADED__'] = True
# end if
pass
php_print("\n")
unique_id_ = esc_attr(twentyseventeen_unique_id("search-form-"))
php_print("\n<form role=\"search\" method=\"get\" class=\"search-form\" action=\"")
php_print(esc_url(home_url("/")))
php_print("\">\n    <label for=\"")
php_print(unique_id_)
php_print("\">\n        <span class=\"screen-reader-text\">")
php_print(_x("Search for:", "label", "twentyseventeen"))
php_print("</span>\n    </label>\n  <input type=\"search\" id=\"")
php_print(unique_id_)
php_print("\" class=\"search-field\" placeholder=\"")
php_print(esc_attr_x("Search &hellip;", "placeholder", "twentyseventeen"))
php_print("\" value=\"")
php_print(get_search_query())
php_print("\" name=\"s\" />\n   <button type=\"submit\" class=\"search-submit\">")
php_print(twentyseventeen_get_svg(Array({"icon": "search"})))
php_print("<span class=\"screen-reader-text\">")
php_print(_x("Search", "submit button", "twentyseventeen"))
php_print("</span></button>\n</form>\n")
