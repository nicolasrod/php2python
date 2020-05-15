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
php_print("""<div id=\"akismet-plugin-container\">
<div class=\"akismet-masthead\">
<div class=\"akismet-masthead__inside-container\">
<div class=\"akismet-masthead__logo-container\">
<img class=\"akismet-masthead__logo\" src=\"""")
php_print(esc_url(plugins_url("../_inc/img/logo-full-2x.png", __FILE__)))
php_print("""\" alt=\"Akismet\" />
</div>
</div>
</div>
<div class=\"akismet-lower\">
""")
Akismet_Admin.display_status()
php_print("     <div class=\"akismet-boxes\">\n         ")
if Akismet.predefined_api_key():
    Akismet.view("predefined")
elif akismet_user and php_in_array(akismet_user.status, Array("active", "active-dunning", "no-sub", "missing", "cancelled", "suspended")):
    Akismet.view("connect-jp", compact("akismet_user"))
else:
    Akismet.view("activate")
# end if
php_print("     </div>\n    </div>\n</div>")
