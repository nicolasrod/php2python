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
#// Edit links form for inclusion in administration panels.
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// Don't load directly.
if (not php_defined("ABSPATH")):
    php_print("-1")
    php_exit()
# end if
if (not php_empty(lambda : link_id)):
    #// translators: %s: URL to Links screen.
    heading = php_sprintf(__("<a href=\"%s\">Links</a> / Edit Link"), "link-manager.php")
    submit_text = __("Update Link")
    form_name = "editlink"
    nonce_action = "update-bookmark_" + link_id
else:
    #// translators: %s: URL to Links screen.
    heading = php_sprintf(__("<a href=\"%s\">Links</a> / Add New Link"), "link-manager.php")
    submit_text = __("Add Link")
    form_name = "addlink"
    nonce_action = "add-bookmark"
# end if
php_include_file(ABSPATH + "wp-admin/includes/meta-boxes.php", once=True)
add_meta_box("linksubmitdiv", __("Save"), "link_submit_meta_box", None, "side", "core")
add_meta_box("linkcategorydiv", __("Categories"), "link_categories_meta_box", None, "normal", "core")
add_meta_box("linktargetdiv", __("Target"), "link_target_meta_box", None, "normal", "core")
add_meta_box("linkxfndiv", __("Link Relationship (XFN)"), "link_xfn_meta_box", None, "normal", "core")
add_meta_box("linkadvanceddiv", __("Advanced"), "link_advanced_meta_box", None, "normal", "core")
#// This action is documented in wp-admin/includes/meta-boxes.php
do_action("add_meta_boxes", "link", link)
#// 
#// Fires when link-specific meta boxes are added.
#// 
#// @since 3.0.0
#// 
#// @param object $link Link object.
#//
do_action("add_meta_boxes_link", link)
#// This action is documented in wp-admin/includes/meta-boxes.php
do_action("do_meta_boxes", "link", "normal", link)
#// This action is documented in wp-admin/includes/meta-boxes.php
do_action("do_meta_boxes", "link", "advanced", link)
#// This action is documented in wp-admin/includes/meta-boxes.php
do_action("do_meta_boxes", "link", "side", link)
add_screen_option("layout_columns", Array({"max": 2, "default": 2}))
get_current_screen().add_help_tab(Array({"id": "overview", "title": __("Overview"), "content": "<p>" + __("You can add or edit links on this screen by entering information in each of the boxes. Only the link&#8217;s web address and name (the text you want to display on your site as the link) are required fields.") + "</p>" + "<p>" + __("The boxes for link name, web address, and description have fixed positions, while the others may be repositioned using drag and drop. You can also hide boxes you don&#8217;t use in the Screen Options tab, or minimize boxes by clicking on the title bar of the box.") + "</p>" + "<p>" + __("XFN stands for <a href=\"http://gmpg.org/xfn/\">XHTML Friends Network</a>, which is optional. WordPress allows the generation of XFN attributes to show how you are related to the authors/owners of the site to which you are linking.") + "</p>"}))
get_current_screen().set_help_sidebar("<p><strong>" + __("For more information:") + "</strong></p>" + "<p>" + __("<a href=\"https://codex.wordpress.org/Links_Add_New_Screen\">Documentation on Creating Links</a>") + "</p>" + "<p>" + __("<a href=\"https://wordpress.org/support/\">Support</a>") + "</p>")
php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
php_print("""
<div class=\"wrap\">
<h1 class=\"wp-heading-inline\">
""")
php_print(esc_html(title))
php_print("</h1>\n\n<a href=\"link-add.php\" class=\"page-title-action\">")
php_print(esc_html_x("Add New", "link"))
php_print("""</a>
<hr class=\"wp-header-end\">
""")
if (php_isset(lambda : PHP_REQUEST["added"])):
    php_print("<div id=\"message\" class=\"updated notice is-dismissible\"><p>")
    _e("Link added.")
    php_print("</p></div>\n")
# end if
php_print("\n<form name=\"")
php_print(esc_attr(form_name))
php_print("\" id=\"")
php_print(esc_attr(form_name))
php_print("\" method=\"post\" action=\"link.php\">\n")
if (not php_empty(lambda : link_added)):
    php_print(link_added)
# end if
wp_nonce_field(nonce_action)
wp_nonce_field("closedpostboxes", "closedpostboxesnonce", False)
wp_nonce_field("meta-box-order", "meta-box-order-nonce", False)
php_print("""
<div id=\"poststuff\">
<div id=\"post-body\" class=\"metabox-holder columns-""")
php_print("1" if 1 == get_current_screen().get_columns() else "2")
php_print("""\">
<div id=\"post-body-content\">
<div id=\"namediv\" class=\"stuffbox\">
<h2><label for=\"link_name\">""")
_ex("Name", "link name")
php_print("</label></h2>\n<div class=\"inside\">\n  <input type=\"text\" name=\"link_name\" size=\"30\" maxlength=\"255\" value=\"")
php_print(esc_attr(link.link_name))
php_print("\" id=\"link_name\" />\n <p>")
_e("Example: Nifty blogging software")
php_print("""</p>
</div>
</div>
<div id=\"addressdiv\" class=\"stuffbox\">
<h2><label for=\"link_url\">""")
_e("Web Address")
php_print("</label></h2>\n<div class=\"inside\">\n  <input type=\"text\" name=\"link_url\" size=\"30\" maxlength=\"255\" class=\"code\" value=\"")
php_print(esc_attr(link.link_url))
php_print("\" id=\"link_url\" />\n  <p>")
_e("Example: <code>http://wordpress.org/</code> &#8212; don&#8217;t forget the <code>http://</code>")
php_print("""</p>
</div>
</div>
<div id=\"descriptiondiv\" class=\"stuffbox\">
<h2><label for=\"link_description\">""")
_e("Description")
php_print("</label></h2>\n<div class=\"inside\">\n  <input type=\"text\" name=\"link_description\" size=\"30\" maxlength=\"255\" value=\"")
php_print(esc_attr(link.link_description) if (php_isset(lambda : link.link_description)) else "")
php_print("\" id=\"link_description\" />\n  <p>")
_e("This will be shown when someone hovers over the link in the blogroll, or optionally below the link.")
php_print("""</p>
</div>
</div>
</div><!-- /post-body-content -->
<div id=\"postbox-container-1\" class=\"postbox-container\">
""")
#// This action is documented in wp-admin/includes/meta-boxes.php
do_action("submitlink_box")
side_meta_boxes = do_meta_boxes("link", "side", link)
php_print("</div>\n<div id=\"postbox-container-2\" class=\"postbox-container\">\n")
do_meta_boxes(None, "normal", link)
do_meta_boxes(None, "advanced", link)
php_print("</div>\n")
if link_id:
    php_print("<input type=\"hidden\" name=\"action\" value=\"save\" />\n<input type=\"hidden\" name=\"link_id\" value=\"")
    php_print(php_int(link_id))
    php_print("\" />\n<input type=\"hidden\" name=\"cat_id\" value=\"")
    php_print(php_int(cat_id))
    php_print("\" />\n")
else:
    php_print("<input type=\"hidden\" name=\"action\" value=\"add\" />\n")
# end if
php_print("""
</div>
</div>
</form>
</div>
""")
