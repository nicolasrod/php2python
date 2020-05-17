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
#// Your Rights administration panel.
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// WordPress Administration Bootstrap
php_include_file(__DIR__ + "/admin.php", once=True)
#// This file was used to also display the Privacy tab on the About screen from 4.9.6 until 5.3.0.
if (php_isset(lambda : PHP_REQUEST["privacy-notice"])):
    wp_redirect(admin_url("privacy.php"), 301)
    php_exit(0)
# end if
title_ = __("Freedoms")
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
php_print("</a>\n           <a href=\"freedoms.php\" class=\"nav-tab nav-tab-active\" aria-current=\"page\">")
_e("Freedoms")
php_print("</a>\n           <a href=\"privacy.php\" class=\"nav-tab\">")
_e("Privacy")
php_print("""</a>
</nav>
</div>
<div class=\"about__section has-subtle-background-color is-feature\">
<h1>""")
_e("Freedoms")
php_print("""</h1>
<p class=\"about-description\">
""")
printf(__("WordPress is Free and open source software, built by a distributed community of mostly volunteer developers from around the world. WordPress comes with some awesome, worldview-changing rights courtesy of its <a href=\"%s\">license</a>, the GPL."), __("https://wordpress.org/about/license/"))
php_print("""       </p>
</div>
<hr />
<div class=\"about__section has-4-columns\">
<div class=\"column\">
<div class=\"freedoms-image\"></div>
<h3>""")
_e("The 1st Freedom")
php_print("</h3>\n          <p>")
_e("To run the program for any purpose.")
php_print("""</p>
</div>
<div class=\"column\">
<div class=\"freedoms-image\"></div>
<h3>""")
_e("The 2nd Freedom")
php_print("</h3>\n          <p>")
_e("To study how the program works and change it to make it do what you wish.")
php_print("""</p>
</div>
<div class=\"column\">
<div class=\"freedoms-image\"></div>
<h3>""")
_e("The 3rd Freedom")
php_print("</h3>\n          <p>")
_e("To redistribute.")
php_print("""</p>
</div>
<div class=\"column\">
<div class=\"freedoms-image\"></div>
<h3>""")
_e("The 4th Freedom")
php_print("</h3>\n          <p>")
_e("To distribute copies of your modified versions to others.")
php_print("""</p>
</div>
</div>
<hr />
<div class=\"about__section\">
<div class=\"column\">
<p>
""")
printf(__("WordPress grows when people like you tell their friends about it, and the thousands of businesses and services that are built on and around WordPress share that fact with their users. We&#8217;re flattered every time someone spreads the good word, just make sure to <a href=\"%s\">check out our trademark guidelines</a> first."), "https://wordpressfoundation.org/trademark-policy/")
php_print("""           </p>
<p>
""")
plugins_url_ = admin_url("plugins.php") if current_user_can("activate_plugins") else __("https://wordpress.org/plugins/")
themes_url_ = admin_url("themes.php") if current_user_can("switch_themes") else __("https://wordpress.org/themes/")
printf(__("Every plugin and theme in WordPress.org&#8217;s directory is 100%% GPL or a similarly free and compatible license, so you can feel safe finding <a href=\"%1$s\">plugins</a> and <a href=\"%2$s\">themes</a> there. If you get a plugin or theme from another source, make sure to <a href=\"%3$s\">ask them if it&#8217;s GPL</a> first. If they don&#8217;t respect the WordPress license, we don&#8217;t recommend them."), plugins_url_, themes_url_, __("https://wordpress.org/about/license/"))
php_print("         </p>\n\n            <p>")
_e("Don&#8217;t you wish all software came with these freedoms? So do we! For more information, check out the <a href=\"https://www.fsf.org/\">Free Software Foundation</a>.")
php_print("""</p>
</div>
</div>
</div>
""")
php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
