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
#// 
#// Credits administration panel.
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// WordPress Administration Bootstrap
php_include_file(__DIR__ + "/admin.php", once=True)
php_include_file(__DIR__ + "/includes/credits.php", once=True)
title = __("Credits")
display_version = php_explode("-", get_bloginfo("version"))
php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
credits = wp_credits()
php_print("""<div class=\"wrap about__container\">
<div class=\"about__header\">
<div class=\"about__header-title\">
<p>
""")
_e("WordPress")
php_print("             <span>")
php_print(display_version)
php_print("""</span>
</p>
</div>
<div class=\"about__header-text\">
<p>
""")
_e("Building more with blocks, faster and easier.")
php_print("""           </p>
</div>
<nav class=\"about__header-navigation nav-tab-wrapper wp-clearfix\" aria-label=\"""")
esc_attr_e("Secondary menu")
php_print("\">\n            <a href=\"about.php\" class=\"nav-tab\">")
_e("What&#8217;s New")
php_print("</a>\n           <a href=\"credits.php\" class=\"nav-tab nav-tab-active\" aria-current=\"page\">")
_e("Credits")
php_print("</a>\n           <a href=\"freedoms.php\" class=\"nav-tab\">")
_e("Freedoms")
php_print("</a>\n           <a href=\"privacy.php\" class=\"nav-tab\">")
_e("Privacy")
php_print("""</a>
</nav>
</div>
<div class=\"about__section is-feature\">
<div class=\"column\">
<h1>""")
_e("Credits")
php_print("</h1>\n\n            ")
if (not credits):
    php_print("\n           <p>\n               ")
    printf(__("WordPress is created by a <a href=\"%1$s\">worldwide team</a> of passionate individuals. <a href=\"%2$s\">Get involved in WordPress</a>."), __("https://wordpress.org/about/"), __("https://make.wordpress.org/"))
    php_print("         </p>\n\n            ")
else:
    php_print("\n           <p>\n               ")
    _e("WordPress is created by a worldwide team of passionate individuals.")
    php_print("         </p>\n          <p>\n               ")
    printf(__("Want to see your name in lights on this page? <a href=\"%s\">Get involved in WordPress</a>."), __("https://make.wordpress.org/"))
    php_print("         </p>\n\n            ")
# end if
php_print("""       </div>
<div class=\"about__image aligncenter\">
<img src=\"data:image/svg+xml;charset=utf8,%3Csvg width='1000' height='300' viewbox='0 0 1000 300' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath fill='%23F3F4F5' d='M0 0h1000v300H0z'/%3E%3Cpath style='mix-blend-mode:multiply' d='M39.6 140.22l931.1 3.36.8 76.5-929.5 6.6-2.4-86.46z' fill='%23216DD2'/%3E%3Cpath style='mix-blend-mode:multiply' d='M963.7 275.14s-.9-59.58-1-64.14c-.1-4.2-932.3 1.74-932.3 1.74L29 268.48v8.4' fill='%237FCDE6'/%3E%3Cpath style='mix-blend-mode:multiply' d='M958 73.32L47.8 70.26l1.2 78.66 907.3 4.26 1.7-79.86z' fill='%23072CF0'/%3E%3Cpath style='mix-blend-mode:multiply' d='M34 91.32l910.4-2.16L939.2 21 33.3 23.82l.7 67.5z' fill='%230188D9'/%3E%3C/svg%3E\" alt=\"\" />
</div>
</div>
""")
if (not credits):
    php_print("</div>")
    php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
    php_exit(0)
# end if
php_print("""
<hr />
<div class=\"about__section\">
<div class=\"column has-subtle-background-color\">
""")
wp_credits_section_title(credits["groups"]["core-developers"])
php_print("         ")
wp_credits_section_list(credits, "core-developers")
php_print("         ")
wp_credits_section_list(credits, "contributing-developers")
php_print("""       </div>
</div>
<hr />
<div class=\"about__section\">
<div class=\"column\">
""")
wp_credits_section_title(credits["groups"]["props"])
php_print("         ")
wp_credits_section_list(credits, "props")
php_print("""       </div>
</div>
<hr />
""")
if (php_isset(lambda : credits["groups"]["translators"])) or (php_isset(lambda : credits["groups"]["validators"])):
    php_print(" <div class=\"about__section\">\n        <div class=\"column\">\n            ")
    wp_credits_section_title(credits["groups"]["validators"])
    php_print("         ")
    wp_credits_section_list(credits, "validators")
    php_print("         ")
    wp_credits_section_list(credits, "translators")
    php_print("""       </div>
    </div>
    <hr />
    """)
# end if
php_print("""
<div class=\"about__section\">
<div class=\"column\">
""")
wp_credits_section_title(credits["groups"]["libraries"])
php_print("         ")
wp_credits_section_list(credits, "libraries")
php_print("""       </div>
</div>
</div>
""")
php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
sys.exit(-1)
#// These are strings returned by the API that we want to be translatable.
__("Project Leaders")
#// translators: %s: The current WordPress version number.
__("Core Contributors to WordPress %s")
__("Noteworthy Contributors")
__("Cofounder, Project Lead")
__("Lead Developer")
__("Release Lead")
__("Release Design Lead")
__("Release Deputy")
__("Core Developer")
__("External Libraries")
