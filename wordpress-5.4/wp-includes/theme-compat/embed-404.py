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
php_print("<div class=\"wp-embed\">\n   <p class=\"wp-embed-heading\">")
_e("Oops! That embed can&#8217;t be found.")
php_print("""</p>
<div class=\"wp-embed-excerpt\">
<p>
""")
printf(__("It looks like nothing was found at this location. Maybe try visiting %s directly?"), "<strong><a href=\"" + esc_url(home_url()) + "\">" + esc_html(get_bloginfo("name")) + "</a></strong>")
php_print("""       </p>
</div>
""")
#// This filter is documented in wp-includes/theme-compat/embed-content.php
do_action("embed_content")
php_print("\n   <div class=\"wp-embed-footer\">\n       ")
the_embed_site_title()
php_print(" </div>\n</div>\n")
