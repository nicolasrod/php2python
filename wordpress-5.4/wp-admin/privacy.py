#!/usr/bin/env python3
# coding: utf-8
if '__PHP2PY_LOADED__' not in globals():
    import os
    with open(os.getenv('PHP2PY_COMPAT', 'php_compat.py')) as f:
        exec(compile(f.read(), '<string>', 'exec'))
    # end with
    globals()['__PHP2PY_LOADED__'] = True
# end if
#// 
#// Privacy administration panel.
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// WordPress Administration Bootstrap
php_include_file(__DIR__ + "/admin.php", once=True)
title_ = __("Privacy")
display_version_ = php_explode("-", get_bloginfo("version"))
php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
php_print("""<div class=\"wrap about__container\">
<div class=\"about__header\">
<div class=\"about__header-title\">
<p>
""")
_e("WordPress")
php_print("             <span>")
php_print(display_version_)
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
php_print("</a>\n           <a href=\"credits.php\" class=\"nav-tab\">")
_e("Credits")
php_print("</a>\n           <a href=\"freedoms.php\" class=\"nav-tab\">")
_e("Freedoms")
php_print("</a>\n           <a href=\"privacy.php\" class=\"nav-tab nav-tab-active\" aria-current=\"page\">")
_e("Privacy")
php_print("""</a>
</nav>
</div>
<div class=\"about__section\">
<div class=\"column\">
<h1>""")
_e("Privacy")
php_print("</h1>\n\n            <p>")
_e("From time to time, your WordPress site may send data to WordPress.org &#8212; including, but not limited to &#8212; the version of WordPress you are using, and a list of installed plugins and themes.")
php_print("""</p>
<p>
""")
php_printf(__("This data is used to provide general enhancements to WordPress, which includes helping to protect your site by finding and automatically installing new updates. It is also used to calculate statistics, such as those shown on the <a href=\"%s\">WordPress.org stats page</a>."), __("https://wordpress.org/about/stats/"))
php_print("""           </p>
<p>
""")
php_printf(__("We take privacy and transparency very seriously. To learn more about what data we collect, and how we use it, please visit <a href=\"%s\">WordPress.org/about/privacy</a>."), __("https://wordpress.org/about/privacy/"))
php_print("""           </p>
</div>
</div>
</div>
""")
php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
