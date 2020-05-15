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
php_print("""<div id=\"akismet-plugin-container\">
<div class=\"akismet-masthead\">
<div class=\"akismet-masthead__inside-container\">
<a href=\"""")
php_print(esc_url(Akismet_Admin.get_page_url()))
php_print("\" class=\"akismet-right\">")
esc_html_e("Akismet Settings", "akismet")
php_print("</a>\n           <div class=\"akismet-masthead__logo-container\">\n              <img class=\"akismet-masthead__logo\" src=\"")
php_print(esc_url(plugins_url("../_inc/img/logo-full-2x.png", __FILE__)))
php_print("""\" alt=\"Akismet\" />
</div>
</div>
</div>
<iframe src=\"""")
php_print(esc_url(php_sprintf("//akismet.com/web/1.0/user-stats.php?blog=%s&api_key=%s&locale=%s", urlencode(get_option("home")), Akismet.get_api_key(), get_locale())))
php_print("\" width=\"100%\" height=\"2500px\" frameborder=\"0\"></iframe>\n</div>")
