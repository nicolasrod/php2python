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
php_print("""
<section class=\"no-results not-found\">
<header class=\"page-header\">
<h1 class=\"page-title\">""")
_e("Nothing Found", "twentynineteen")
php_print("""</h1>
</header><!-- .page-header -->
<div class=\"page-content\">
""")
if is_home() and current_user_can("publish_posts"):
    printf("<p>" + wp_kses(__("Ready to publish your first post? <a href=\"%1$s\">Get started here</a>.", "twentynineteen"), Array({"a": Array({"href": Array()})})) + "</p>", esc_url(admin_url("post-new.php")))
elif is_search():
    php_print("\n           <p>")
    _e("Sorry, but nothing matched your search terms. Please try again with some different keywords.", "twentynineteen")
    php_print("</p>\n           ")
    get_search_form()
else:
    php_print("\n           <p>")
    _e("It seems we can&rsquo;t find what you&rsquo;re looking for. Perhaps searching can help.", "twentynineteen")
    php_print("</p>\n           ")
    get_search_form()
# end if
php_print(" </div><!-- .page-content -->\n</section><!-- .no-results -->\n")
