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
</div><!-- #content -->
<footer id=\"colophon\" class=\"site-footer\">
""")
get_template_part("template-parts/footer/footer", "widgets")
php_print("     <div class=\"site-info\">\n         ")
blog_info_ = get_bloginfo("name")
php_print("         ")
if (not php_empty(lambda : blog_info_)):
    php_print("             <a class=\"site-name\" href=\"")
    php_print(esc_url(home_url("/")))
    php_print("\" rel=\"home\">")
    bloginfo("name")
    php_print("</a>,\n          ")
# end if
php_print("         <a href=\"")
php_print(esc_url(__("https://wordpress.org/", "twentynineteen")))
php_print("\" class=\"imprint\">\n              ")
#// translators: %s: WordPress.
php_printf(__("Proudly powered by %s.", "twentynineteen"), "WordPress")
php_print("         </a>\n          ")
if php_function_exists("the_privacy_policy_link"):
    the_privacy_policy_link("", "<span role=\"separator\" aria-hidden=\"true\"></span>")
# end if
php_print("         ")
if has_nav_menu("footer"):
    php_print("             <nav class=\"footer-navigation\" aria-label=\"")
    esc_attr_e("Footer Menu", "twentynineteen")
    php_print("\">\n                    ")
    wp_nav_menu(Array({"theme_location": "footer", "menu_class": "footer-menu", "depth": 1}))
    php_print("             </nav><!-- .footer-navigation -->\n         ")
# end if
php_print("""       </div><!-- .site-info -->
</footer><!-- #colophon -->
</div><!-- #page -->
""")
wp_footer()
php_print("""
</body>
</html>
""")
