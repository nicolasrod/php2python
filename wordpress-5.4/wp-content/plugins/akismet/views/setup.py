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
php_print("<div class=\"akismet-setup-instructions\">\n <p>")
esc_html_e("Set up your Akismet account to enable spam filtering on this site.", "akismet")
php_print("</p>\n   ")
Akismet.view("get", Array({"text": __("Set up your Akismet account", "akismet"), "classes": Array("akismet-button", "akismet-is-primary")}))
php_print("</div>\n")
