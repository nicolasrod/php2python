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
php_print("""<div class=\"custom-header\">
<div class=\"custom-header-media\">
""")
the_custom_header_markup()
php_print("     </div>\n\n  ")
get_template_part("template-parts/header/site", "branding")
php_print("\n</div><!-- .custom-header -->\n")
