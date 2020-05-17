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
php_print("<div class=\"site-info\">\n  ")
if php_function_exists("the_privacy_policy_link"):
    the_privacy_policy_link("", "<span role=\"separator\" aria-hidden=\"true\"></span>")
# end if
php_print(" <a href=\"")
php_print(esc_url(__("https://wordpress.org/", "twentyseventeen")))
php_print("\" class=\"imprint\">\n      ")
#// translators: %s: WordPress
printf(__("Proudly powered by %s", "twentyseventeen"), "WordPress")
php_print(" </a>\n</div><!-- .site-info -->\n")
