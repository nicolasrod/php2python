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
pass
php_print("<form name=\"akismet_activate\" action=\"https://akismet.com/get/\" method=\"POST\" target=\"_blank\">\n <input type=\"hidden\" name=\"passback_url\" value=\"")
php_print(esc_url(Akismet_Admin.get_page_url()))
php_print("\"/>\n   <input type=\"hidden\" name=\"blog\" value=\"")
php_print(esc_url(get_option("home")))
php_print("\"/>\n   <input type=\"hidden\" name=\"redirect\" value=\"")
php_print(redirect if (php_isset(lambda : redirect)) else "plugin-signup")
php_print("\"/>\n   <input type=\"submit\" class=\"")
php_print(php_implode(" ", classes) if (php_isset(lambda : classes)) and php_count(classes) > 0 else "akismet-button")
php_print("\" value=\"")
php_print(esc_attr(text))
php_print("\"/>\n</form>")
