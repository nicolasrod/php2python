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
php_print("<div class=\"akismet-enter-api-key-box centered\">\n <a href=\"#\">")
esc_html_e("Manually enter an API key")
php_print("</a>\n   <div class=\"enter-api-key\">\n     <form action=\"")
php_print(esc_url(Akismet_Admin.get_page_url()))
php_print("\" method=\"post\">\n            ")
wp_nonce_field(Akismet_Admin.NONCE)
php_print("         <input type=\"hidden\" name=\"action\" value=\"enter-key\">\n           <p style=\"width: 100%; display: flex; flex-wrap: nowrap; box-sizing: border-box;\">\n              <input id=\"key\" name=\"key\" type=\"text\" size=\"15\" value=\"\" placeholder=\"")
esc_attr_e("Enter your API key", "akismet")
php_print("\" class=\"regular-text code\" style=\"flex-grow: 1; margin-right: 1rem;\">\n                <input type=\"submit\" name=\"submit\" id=\"submit\" class=\"akismet-button\" value=\"")
esc_attr_e("Connect with API key", "akismet")
php_print("""\">
</p>
</form>
</div>
</div>""")
