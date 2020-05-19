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
#// Tools Administration Screen.
#// 
#// @package WordPress
#// @subpackage Administration
#//
if (php_isset(lambda : PHP_REQUEST["page"])) and (not php_empty(lambda : PHP_POST)):
    #// Ensure POST-ing to `tools.php?page=export_personal_data` and `tools.php?page=remove_personal_data`
    #// continues to work after creating the new files for exporting and erasing of personal data.
    if "export_personal_data" == PHP_REQUEST["page"]:
        php_include_file(ABSPATH + "wp-admin/export-personal-data.php", once=True)
        sys.exit(-1)
    elif "remove_personal_data" == PHP_REQUEST["page"]:
        php_include_file(ABSPATH + "wp-admin/erase-personal-data.php", once=True)
        sys.exit(-1)
    # end if
# end if
#// The privacy policy guide used to be outputted from here. Since WP 5.3 it is in wp-admin/privacy-policy-guide.php.
if (php_isset(lambda : PHP_REQUEST["wp-privacy-policy-guide"])):
    php_include_file(php_dirname(__DIR__) + "/wp-load.php", once=True)
    wp_redirect(admin_url("privacy-policy-guide.php"), 301)
    php_exit(0)
elif (php_isset(lambda : PHP_REQUEST["page"])):
    #// These were also moved to files in WP 5.3.
    if "export_personal_data" == PHP_REQUEST["page"]:
        php_include_file(php_dirname(__DIR__) + "/wp-load.php", once=True)
        wp_redirect(admin_url("export-personal-data.php"), 301)
        php_exit(0)
    elif "remove_personal_data" == PHP_REQUEST["page"]:
        php_include_file(php_dirname(__DIR__) + "/wp-load.php", once=True)
        wp_redirect(admin_url("erase-personal-data.php"), 301)
        php_exit(0)
    # end if
# end if
#// WordPress Administration Bootstrap
php_include_file(__DIR__ + "/admin.php", once=True)
title_ = __("Tools")
get_current_screen().add_help_tab(Array({"id": "converter", "title": __("Categories and Tags Converter"), "content": "<p>" + __("Categories have hierarchy, meaning that you can nest sub-categories. Tags do not have hierarchy and cannot be nested. Sometimes people start out using one on their posts, then later realize that the other would work better for their content.") + "</p>" + "<p>" + __("The Categories and Tags Converter link on this screen will take you to the Import screen, where that Converter is one of the plugins you can install. Once that plugin is installed, the Activate Plugin &amp; Run Importer link will take you to a screen where you can choose to convert tags into categories or vice versa.") + "</p>"}))
get_current_screen().set_help_sidebar("<p><strong>" + __("For more information:") + "</strong></p>" + "<p>" + __("<a href=\"https://wordpress.org/support/article/tools-screen/\">Documentation on Tools</a>") + "</p>" + "<p>" + __("<a href=\"https://wordpress.org/support/\">Support</a>") + "</p>")
php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
php_print("<div class=\"wrap\">\n<h1>")
php_print(esc_html(title_))
php_print("</h1>\n")
if current_user_can("import"):
    cats_ = get_taxonomy("category")
    tags_ = get_taxonomy("post_tag")
    if current_user_can(cats_.cap.manage_terms) or current_user_can(tags_.cap.manage_terms):
        php_print("     <div class=\"card\">\n          <h2 class=\"title\">")
        _e("Categories and Tags Converter")
        php_print("</h2>\n          <p>\n           ")
        php_printf(__("If you want to convert your categories to tags (or vice versa), use the <a href=\"%s\">Categories and Tags Converter</a> available from the Import screen."), "import.php")
        php_print("         </p>\n      </div>\n        ")
    # end if
# end if
#// 
#// Fires at the end of the Tools Administration screen.
#// 
#// @since 2.8.0
#//
do_action("tool_box")
php_print("</div>\n")
php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
