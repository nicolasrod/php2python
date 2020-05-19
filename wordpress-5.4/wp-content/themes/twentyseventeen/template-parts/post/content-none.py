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
php_print("""
<section class=\"no-results not-found\">
<header class=\"page-header\">
<h1 class=\"page-title\">""")
_e("Nothing Found", "twentyseventeen")
php_print("""</h1>
</header>
<div class=\"page-content\">
""")
if is_home() and current_user_can("publish_posts"):
    php_print("\n           <p>\n           ")
    #// translators: %s: Post editor URL.
    php_printf(__("Ready to publish your first post? <a href=\"%s\">Get started here</a>.", "twentyseventeen"), esc_url(admin_url("post-new.php")))
    php_print("         </p>\n\n        ")
else:
    php_print("\n           <p>")
    _e("It seems we can&rsquo;t find what you&rsquo;re looking for. Perhaps searching can help.", "twentyseventeen")
    php_print("</p>\n           ")
    get_search_form()
# end if
php_print(" </div><!-- .page-content -->\n</section><!-- .no-results -->\n")
