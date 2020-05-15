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
#// Displays Administration Menu.
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// 
#// The current page.
#// 
#// @global string $self
#//
self = php_preg_replace("|^.*/wp-admin/network/|i", "", PHP_SERVER["PHP_SELF"])
self = php_preg_replace("|^.*/wp-admin/|i", "", self)
self = php_preg_replace("|^.*/plugins/|i", "", self)
self = php_preg_replace("|^.*/mu-plugins/|i", "", self)
#// 
#// For when admin-header is included from within a function.
#// 
#// @global array  $menu
#// @global array  $submenu
#// @global string $parent_file
#// @global string $submenu_file
#//
global menu,submenu,parent_file,submenu_file
php_check_if_defined("menu","submenu","parent_file","submenu_file")
#// 
#// Filters the parent file of an admin menu sub-menu item.
#// 
#// Allows plugins to move sub-menu items around.
#// 
#// @since MU (3.0.0)
#// 
#// @param string $parent_file The parent file.
#//
parent_file = apply_filters("parent_file", parent_file)
#// 
#// Filters the file of an admin menu sub-menu item.
#// 
#// @since 4.4.0
#// 
#// @param string $submenu_file The submenu file.
#// @param string $parent_file  The submenu item's parent file.
#//
submenu_file = apply_filters("submenu_file", submenu_file, parent_file)
get_admin_page_parent()
#// 
#// Display menu.
#// 
#// @access private
#// @since 2.7.0
#// 
#// @global string $self
#// @global string $parent_file
#// @global string $submenu_file
#// @global string $plugin_page
#// @global string $typenow
#// 
#// @param array $menu
#// @param array $submenu
#// @param bool  $submenu_as_parent
#//
def _wp_menu_output(menu=None, submenu=None, submenu_as_parent=True, *args_):
    
    global self,parent_file,submenu_file,plugin_page,typenow
    php_check_if_defined("self","parent_file","submenu_file","plugin_page","typenow")
    first = True
    #// 0 = menu_title, 1 = capability, 2 = menu_slug, 3 = page_title, 4 = classes, 5 = hookname, 6 = icon_url.
    for key,item in menu:
        admin_is_parent = False
        class_ = Array()
        aria_attributes = ""
        aria_hidden = ""
        is_separator = False
        if first:
            class_[-1] = "wp-first-item"
            first = False
        # end if
        submenu_items = Array()
        if (not php_empty(lambda : submenu[item[2]])):
            class_[-1] = "wp-has-submenu"
            submenu_items = submenu[item[2]]
        # end if
        if parent_file and item[2] == parent_file or php_empty(lambda : typenow) and self == item[2]:
            if (not php_empty(lambda : submenu_items)):
                class_[-1] = "wp-has-current-submenu wp-menu-open"
            else:
                class_[-1] = "current"
                aria_attributes += "aria-current=\"page\""
            # end if
        else:
            class_[-1] = "wp-not-current-submenu"
            if (not php_empty(lambda : submenu_items)):
                aria_attributes += "aria-haspopup=\"true\""
            # end if
        # end if
        if (not php_empty(lambda : item[4])):
            class_[-1] = esc_attr(item[4])
        # end if
        class_ = " class=\"" + join(" ", class_) + "\"" if class_ else ""
        id = " id=\"" + php_preg_replace("|[^a-zA-Z0-9_:.]|", "-", item[5]) + "\"" if (not php_empty(lambda : item[5])) else ""
        img = ""
        img_style = ""
        img_class = " dashicons-before"
        if False != php_strpos(class_, "wp-menu-separator"):
            is_separator = True
        # end if
        #// 
        #// If the string 'none' (previously 'div') is passed instead of a URL, don't output
        #// the default menu image so an icon can be added to div.wp-menu-image as background
        #// with CSS. Dashicons and base64-encoded data:image/svg_xml URIs are also handled
        #// as special cases.
        #//
        if (not php_empty(lambda : item[6])):
            img = "<img src=\"" + item[6] + "\" alt=\"\" />"
            if "none" == item[6] or "div" == item[6]:
                img = "<br />"
            elif 0 == php_strpos(item[6], "data:image/svg+xml;base64,"):
                img = "<br />"
                img_style = " style=\"background-image:url('" + esc_attr(item[6]) + "')\""
                img_class = " svg"
            elif 0 == php_strpos(item[6], "dashicons-"):
                img = "<br />"
                img_class = " dashicons-before " + sanitize_html_class(item[6])
            # end if
        # end if
        arrow = "<div class=\"wp-menu-arrow\"><div></div></div>"
        title = wptexturize(item[0])
        #// Hide separators from screen readers.
        if is_separator:
            aria_hidden = " aria-hidden=\"true\""
        # end if
        php_print(str("\n   <li") + str(class_) + str(id) + str(aria_hidden) + str(">"))
        if is_separator:
            php_print("<div class=\"separator\"></div>")
        elif submenu_as_parent and (not php_empty(lambda : submenu_items)):
            submenu_items = php_array_values(submenu_items)
            #// Re-index.
            menu_hook = get_plugin_page_hook(submenu_items[0][2], item[2])
            menu_file = submenu_items[0][2]
            pos = php_strpos(menu_file, "?")
            if False != pos:
                menu_file = php_substr(menu_file, 0, pos)
            # end if
            if (not php_empty(lambda : menu_hook)) or "index.php" != submenu_items[0][2] and php_file_exists(WP_PLUGIN_DIR + str("/") + str(menu_file)) and (not php_file_exists(ABSPATH + str("/wp-admin/") + str(menu_file))):
                admin_is_parent = True
                php_print(str("<a href='admin.php?page=") + str(submenu_items[0][2]) + str("'") + str(class_) + str(" ") + str(aria_attributes) + str(">") + str(arrow) + str("<div class='wp-menu-image") + str(img_class) + str("'") + str(img_style) + str(">") + str(img) + str("</div><div class='wp-menu-name'>") + str(title) + str("</div></a>"))
            else:
                php_print(str("\n   <a href='") + str(submenu_items[0][2]) + str("'") + str(class_) + str(" ") + str(aria_attributes) + str(">") + str(arrow) + str("<div class='wp-menu-image") + str(img_class) + str("'") + str(img_style) + str(">") + str(img) + str("</div><div class='wp-menu-name'>") + str(title) + str("</div></a>"))
            # end if
        elif (not php_empty(lambda : item[2])) and current_user_can(item[1]):
            menu_hook = get_plugin_page_hook(item[2], "admin.php")
            menu_file = item[2]
            pos = php_strpos(menu_file, "?")
            if False != pos:
                menu_file = php_substr(menu_file, 0, pos)
            # end if
            if (not php_empty(lambda : menu_hook)) or "index.php" != item[2] and php_file_exists(WP_PLUGIN_DIR + str("/") + str(menu_file)) and (not php_file_exists(ABSPATH + str("/wp-admin/") + str(menu_file))):
                admin_is_parent = True
                php_print(str("\n   <a href='admin.php?page=") + str(item[2]) + str("'") + str(class_) + str(" ") + str(aria_attributes) + str(">") + str(arrow) + str("<div class='wp-menu-image") + str(img_class) + str("'") + str(img_style) + str(">") + str(img) + str("</div><div class='wp-menu-name'>") + str(item[0]) + str("</div></a>"))
            else:
                php_print(str("\n   <a href='") + str(item[2]) + str("'") + str(class_) + str(" ") + str(aria_attributes) + str(">") + str(arrow) + str("<div class='wp-menu-image") + str(img_class) + str("'") + str(img_style) + str(">") + str(img) + str("</div><div class='wp-menu-name'>") + str(item[0]) + str("</div></a>"))
            # end if
        # end if
        if (not php_empty(lambda : submenu_items)):
            php_print("\n   <ul class='wp-submenu wp-submenu-wrap'>")
            php_print(str("<li class='wp-submenu-head' aria-hidden='true'>") + str(item[0]) + str("</li>"))
            first = True
            #// 0 = menu_title, 1 = capability, 2 = menu_slug, 3 = page_title, 4 = classes.
            for sub_key,sub_item in submenu_items:
                if (not current_user_can(sub_item[1])):
                    continue
                # end if
                class_ = Array()
                aria_attributes = ""
                if first:
                    class_[-1] = "wp-first-item"
                    first = False
                # end if
                menu_file = item[2]
                pos = php_strpos(menu_file, "?")
                if False != pos:
                    menu_file = php_substr(menu_file, 0, pos)
                # end if
                #// Handle current for post_type=post|page|foo pages, which won't match $self.
                self_type = self + "?post_type=" + typenow if (not php_empty(lambda : typenow)) else "nothing"
                if (php_isset(lambda : submenu_file)):
                    if submenu_file == sub_item[2]:
                        class_[-1] = "current"
                        aria_attributes += " aria-current=\"page\""
                    # end if
                    pass
                elif (not (php_isset(lambda : plugin_page))) and self == sub_item[2] or (php_isset(lambda : plugin_page)) and plugin_page == sub_item[2] and item[2] == self_type or item[2] == self or php_file_exists(menu_file) == False:
                    class_[-1] = "current"
                    aria_attributes += " aria-current=\"page\""
                # end if
                if (not php_empty(lambda : sub_item[4])):
                    class_[-1] = esc_attr(sub_item[4])
                # end if
                class_ = " class=\"" + join(" ", class_) + "\"" if class_ else ""
                menu_hook = get_plugin_page_hook(sub_item[2], item[2])
                sub_file = sub_item[2]
                pos = php_strpos(sub_file, "?")
                if False != pos:
                    sub_file = php_substr(sub_file, 0, pos)
                # end if
                title = wptexturize(sub_item[0])
                if (not php_empty(lambda : menu_hook)) or "index.php" != sub_item[2] and php_file_exists(WP_PLUGIN_DIR + str("/") + str(sub_file)) and (not php_file_exists(ABSPATH + str("/wp-admin/") + str(sub_file))):
                    #// If admin.php is the current page or if the parent exists as a file in the plugins or admin directory.
                    if (not admin_is_parent) and php_file_exists(WP_PLUGIN_DIR + str("/") + str(menu_file)) and (not php_is_dir(WP_PLUGIN_DIR + str("/") + str(item[2]))) or php_file_exists(menu_file):
                        sub_item_url = add_query_arg(Array({"page": sub_item[2]}), item[2])
                    else:
                        sub_item_url = add_query_arg(Array({"page": sub_item[2]}), "admin.php")
                    # end if
                    sub_item_url = esc_url(sub_item_url)
                    php_print(str("<li") + str(class_) + str("><a href='") + str(sub_item_url) + str("'") + str(class_) + str(aria_attributes) + str(">") + str(title) + str("</a></li>"))
                else:
                    php_print(str("<li") + str(class_) + str("><a href='") + str(sub_item[2]) + str("'") + str(class_) + str(aria_attributes) + str(">") + str(title) + str("</a></li>"))
                # end if
            # end for
            php_print("</ul>")
        # end if
        php_print("</li>")
    # end for
    php_print("<li id=\"collapse-menu\" class=\"hide-if-no-js\">" + "<button type=\"button\" id=\"collapse-button\" aria-label=\"" + esc_attr__("Collapse Main menu") + "\" aria-expanded=\"true\">" + "<span class=\"collapse-button-icon\" aria-hidden=\"true\"></span>" + "<span class=\"collapse-button-label\">" + __("Collapse menu") + "</span>" + "</button></li>")
# end def _wp_menu_output
php_print("\n<div id=\"adminmenumain\" role=\"navigation\" aria-label=\"")
esc_attr_e("Main menu")
php_print("\">\n<a href=\"#wpbody-content\" class=\"screen-reader-shortcut\">")
_e("Skip to main content")
php_print("</a>\n<a href=\"#wp-toolbar\" class=\"screen-reader-shortcut\">")
_e("Skip to toolbar")
php_print("""</a>
<div id=\"adminmenuback\"></div>
<div id=\"adminmenuwrap\">
<ul id=\"adminmenu\">
""")
_wp_menu_output(menu, submenu)
#// 
#// Fires after the admin menu has been output.
#// 
#// @since 2.5.0
#//
do_action("adminmenu")
php_print("""</ul>
</div>
</div>
""")
