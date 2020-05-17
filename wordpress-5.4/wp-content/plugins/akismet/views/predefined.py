#!/usr/bin/env python3
# coding: utf-8
if '__PHP2PY_LOADED__' not in globals():
    import os
    with open(os.getenv('PHP2PY_COMPAT', 'php_compat.py')) as f:
        exec(compile(f.read(), '<string>', 'exec'))
    # end with
    globals()['__PHP2PY_LOADED__'] = True
# end if
php_print("<div class=\"akismet-box\">\n    <h2>")
esc_html_e("Manual Configuration", "akismet")
php_print("</h2>\n  <p>\n       ")
#// translators: %s is the wp-config.php file
php_print(php_sprintf(esc_html__("An Akismet API key has been defined in the %s file for this site.", "akismet"), "<code>wp-config.php</code>"))
php_print(" </p>\n</div>")
