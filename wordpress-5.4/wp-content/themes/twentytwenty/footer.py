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
php_print("""           <footer id=\"site-footer\" role=\"contentinfo\" class=\"header-footer-group\">
<div class=\"section-inner\">
<div class=\"footer-credits\">
<p class=\"footer-copyright\">&copy;
""")
php_print(date_i18n(_x("Y", "copyright date format", "twentytwenty")))
php_print("                         <a href=\"")
php_print(esc_url(home_url("/")))
php_print("\">")
bloginfo("name")
php_print("""</a>
</p><!-- .footer-copyright -->
<p class=\"powered-by-wordpress\">
<a href=\"""")
php_print(esc_url(__("https://wordpress.org/", "twentytwenty")))
php_print("\">\n                                ")
_e("Powered by WordPress", "twentytwenty")
php_print("""                           </a>
</p><!-- .powered-by-wordpress -->
</div><!-- .footer-credits -->
<a class=\"to-the-top\" href=\"#site-header\">
<span class=\"to-the-top-long\">
""")
#// translators: %s: HTML character for up arrow.
php_printf(__("To the top %s", "twentytwenty"), "<span class=\"arrow\" aria-hidden=\"true\">&uarr;</span>")
php_print("                     </span><!-- .to-the-top-long -->\n                      <span class=\"to-the-top-short\">\n                         ")
#// translators: %s: HTML character for up arrow.
php_printf(__("Up %s", "twentytwenty"), "<span class=\"arrow\" aria-hidden=\"true\">&uarr;</span>")
php_print("""                       </span><!-- .to-the-top-short -->
</a><!-- .to-the-top -->
</div><!-- .section-inner -->
</footer><!-- #site-footer -->
""")
wp_footer()
php_print("""
</body>
</html>
""")
