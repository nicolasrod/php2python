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
self_ = php_preg_replace("|^.*/wp-admin/network/|i", "", PHP_SERVER["PHP_SELF"])
self_ = php_preg_replace("|^.*/wp-admin/|i", "", self_)
self_ = php_preg_replace("|^.*/plugins/|i", "", self_)
self_ = php_preg_replace("|^.*/mu-plugins/|i", "", self_)
#// 
#// For when admin-header is included from within a function.
#// 
#// @global array  $menu
#// @global array  $submenu
#// @global string $parent_file
#// @global string $submenu_file
#//
global menu_
global submenu_
global parent_file_
global submenu_file_
php_check_if_defined("menu_","submenu_","parent_file_","submenu_file_")
#// 
#// Filters the parent file of an admin menu sub-menu item.
#// 
#// Allows plugins to move sub-menu items around.
#// 
#// @since MU (3.0.0)
#// 
#// @param string $parent_file The parent file.
#//
parent_file_ = apply_filters("parent_file", parent_file_)
#// 
#// Filters the file of an admin menu sub-menu item.
#// 
#// @since 4.4.0
#// 
#// @param string $submenu_file The submenu file.
#// @param string $parent_file  The submenu item's parent file.
#//
submenu_file_ = apply_filters("submenu_file", submenu_file_, parent_file_)
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
def _wp_menu_output(menu_=None, submenu_=None, submenu_as_parent_=None, *_args_):
    if submenu_as_parent_ is None:
        submenu_as_parent_ = True
    # end if
    
    global self_
    global parent_file_
    global submenu_file_
    global plugin_page_
    global typenow_
    php_check_if_defined("self_","parent_file_","submenu_file_","plugin_page_","typenow_")
    first_ = True
    #// 0 = menu_title, 1 = capability, 2 = menu_slug, 3 = page_title, 4 = classes, 5 = hookname, 6 = icon_url.
    for key_,item_ in menu_:
        admin_is_parent_ = False
        class_ = Array()
        aria_attributes_ = ""
        aria_hidden_ = ""
        is_separator_ = False
        if first_:
            class_[-1] = "wp-first-item"
            first_ = False
        # end if
        submenu_items_ = Array()
        if (not php_empty(lambda : submenu_[item_[2]])):
            class_[-1] = "wp-has-submenu"
            submenu_items_ = submenu_[item_[2]]
        # end if
        if parent_file_ and item_[2] == parent_file_ or php_empty(lambda : typenow_) and self_ == item_[2]:
            if (not php_empty(lambda : submenu_items_)):
                class_[-1] = "wp-has-current-submenu wp-menu-open"
            else:
                class_[-1] = "current"
                aria_attributes_ += "aria-current=\"page\""
            # end if
        else:
            class_[-1] = "wp-not-current-submenu"
            if (not php_empty(lambda : submenu_items_)):
                aria_attributes_ += "aria-haspopup=\"true\""
            # end if
        # end if
        if (not php_empty(lambda : item_[4])):
            class_[-1] = esc_attr(item_[4])
        # end if
        class_ = " class=\"" + join(" ", class_) + "\"" if class_ else ""
        id_ = " id=\"" + php_preg_replace("|[^a-zA-Z0-9_:.]|", "-", item_[5]) + "\"" if (not php_empty(lambda : item_[5])) else ""
        img_ = ""
        img_style_ = ""
        img_class_ = " dashicons-before"
        if False != php_strpos(class_, "wp-menu-separator"):
            is_separator_ = True
        # end if
        #// 
        #// If the string 'none' (previously 'div') is passed instead of a URL, don't output
        #// the default menu image so an icon can be added to div.wp-menu-image as background
        #// with CSS. Dashicons and base64-encoded data:image/svg_xml URIs are also handled
        #// as special cases.
        #//
        if (not php_empty(lambda : item_[6])):
            img_ = "<img src=\"" + item_[6] + "\" alt=\"\" />"
            if "none" == item_[6] or "div" == item_[6]:
                img_ = "<br />"
            elif 0 == php_strpos(item_[6], "data:image/svg+xml;base64,"):
                img_ = "<br />"
                img_style_ = " style=\"background-image:url('" + esc_attr(item_[6]) + "')\""
                img_class_ = " svg"
            elif 0 == php_strpos(item_[6], "dashicons-"):
                img_ = "<br />"
                img_class_ = " dashicons-before " + sanitize_html_class(item_[6])
            # end if
        # end if
        arrow_ = "<div class=\"wp-menu-arrow\"><div></div></div>"
        title_ = wptexturize(item_[0])
        #// Hide separators from screen readers.
        if is_separator_:
            aria_hidden_ = " aria-hidden=\"true\""
        # end if
        php_print(str("\n   <li") + str(class_) + str(id_) + str(aria_hidden_) + str(">"))
        if is_separator_:
            php_print("<div class=\"separator\"></div>")
        elif submenu_as_parent_ and (not php_empty(lambda : submenu_items_)):
            submenu_items_ = php_array_values(submenu_items_)
            #// Re-index.
            menu_hook_ = get_plugin_page_hook(submenu_items_[0][2], item_[2])
            menu_file_ = submenu_items_[0][2]
            pos_ = php_strpos(menu_file_, "?")
            if False != pos_:
                menu_file_ = php_substr(menu_file_, 0, pos_)
            # end if
            if (not php_empty(lambda : menu_hook_)) or "index.php" != submenu_items_[0][2] and php_file_exists(WP_PLUGIN_DIR + str("/") + str(menu_file_)) and (not php_file_exists(ABSPATH + str("/wp-admin/") + str(menu_file_))):
                admin_is_parent_ = True
                php_print(str("<a href='admin.php?page=") + str(submenu_items_[0][2]) + str("'") + str(class_) + str(" ") + str(aria_attributes_) + str(">") + str(arrow_) + str("<div class='wp-menu-image") + str(img_class_) + str("'") + str(img_style_) + str(">") + str(img_) + str("</div><div class='wp-menu-name'>") + str(title_) + str("</div></a>"))
            else:
                php_print(str("\n   <a href='") + str(submenu_items_[0][2]) + str("'") + str(class_) + str(" ") + str(aria_attributes_) + str(">") + str(arrow_) + str("<div class='wp-menu-image") + str(img_class_) + str("'") + str(img_style_) + str(">") + str(img_) + str("</div><div class='wp-menu-name'>") + str(title_) + str("</div></a>"))
            # end if
        elif (not php_empty(lambda : item_[2])) and current_user_can(item_[1]):
            menu_hook_ = get_plugin_page_hook(item_[2], "admin.php")
            menu_file_ = item_[2]
            pos_ = php_strpos(menu_file_, "?")
            if False != pos_:
                menu_file_ = php_substr(menu_file_, 0, pos_)
            # end if
            if (not php_empty(lambda : menu_hook_)) or "index.php" != item_[2] and php_file_exists(WP_PLUGIN_DIR + str("/") + str(menu_file_)) and (not php_file_exists(ABSPATH + str("/wp-admin/") + str(menu_file_))):
                admin_is_parent_ = True
                php_print(str("\n   <a href='admin.php?page=") + str(item_[2]) + str("'") + str(class_) + str(" ") + str(aria_attributes_) + str(">") + str(arrow_) + str("<div class='wp-menu-image") + str(img_class_) + str("'") + str(img_style_) + str(">") + str(img_) + str("</div><div class='wp-menu-name'>") + str(item_[0]) + str("</div></a>"))
            else:
                php_print(str("\n   <a href='") + str(item_[2]) + str("'") + str(class_) + str(" ") + str(aria_attributes_) + str(">") + str(arrow_) + str("<div class='wp-menu-image") + str(img_class_) + str("'") + str(img_style_) + str(">") + str(img_) + str("</div><div class='wp-menu-name'>") + str(item_[0]) + str("</div></a>"))
            # end if
        # end if
        if (not php_empty(lambda : submenu_items_)):
            php_print("\n   <ul class='wp-submenu wp-submenu-wrap'>")
            php_print(str("<li class='wp-submenu-head' aria-hidden='true'>") + str(item_[0]) + str("</li>"))
            first_ = True
            #// 0 = menu_title, 1 = capability, 2 = menu_slug, 3 = page_title, 4 = classes.
            for sub_key_,sub_item_ in submenu_items_:
                if (not current_user_can(sub_item_[1])):
                    continue
                # end if
                class_ = Array()
                aria_attributes_ = ""
                if first_:
                    class_[-1] = "wp-first-item"
                    first_ = False
                # end if
                menu_file_ = item_[2]
                pos_ = php_strpos(menu_file_, "?")
                if False != pos_:
                    menu_file_ = php_substr(menu_file_, 0, pos_)
                # end if
                #// Handle current for post_type=post|page|foo pages, which won't match $self.
                self_type_ = self_ + "?post_type=" + typenow_ if (not php_empty(lambda : typenow_)) else "nothing"
                if (php_isset(lambda : submenu_file_)):
                    if submenu_file_ == sub_item_[2]:
                        class_[-1] = "current"
                        aria_attributes_ += " aria-current=\"page\""
                    # end if
                    pass
                elif (not (php_isset(lambda : plugin_page_))) and self_ == sub_item_[2] or (php_isset(lambda : plugin_page_)) and plugin_page_ == sub_item_[2] and item_[2] == self_type_ or item_[2] == self_ or php_file_exists(menu_file_) == False:
                    class_[-1] = "current"
                    aria_attributes_ += " aria-current=\"page\""
                # end if
                if (not php_empty(lambda : sub_item_[4])):
                    class_[-1] = esc_attr(sub_item_[4])
                # end if
                class_ = " class=\"" + join(" ", class_) + "\"" if class_ else ""
                menu_hook_ = get_plugin_page_hook(sub_item_[2], item_[2])
                sub_file_ = sub_item_[2]
                pos_ = php_strpos(sub_file_, "?")
                if False != pos_:
                    sub_file_ = php_substr(sub_file_, 0, pos_)
                # end if
                title_ = wptexturize(sub_item_[0])
                if (not php_empty(lambda : menu_hook_)) or "index.php" != sub_item_[2] and php_file_exists(WP_PLUGIN_DIR + str("/") + str(sub_file_)) and (not php_file_exists(ABSPATH + str("/wp-admin/") + str(sub_file_))):
                    #// If admin.php is the current page or if the parent exists as a file in the plugins or admin directory.
                    if (not admin_is_parent_) and php_file_exists(WP_PLUGIN_DIR + str("/") + str(menu_file_)) and (not php_is_dir(WP_PLUGIN_DIR + str("/") + str(item_[2]))) or php_file_exists(menu_file_):
                        sub_item_url_ = add_query_arg(Array({"page": sub_item_[2]}), item_[2])
                    else:
                        sub_item_url_ = add_query_arg(Array({"page": sub_item_[2]}), "admin.php")
                    # end if
                    sub_item_url_ = esc_url(sub_item_url_)
                    php_print(str("<li") + str(class_) + str("><a href='") + str(sub_item_url_) + str("'") + str(class_) + str(aria_attributes_) + str(">") + str(title_) + str("</a></li>"))
                else:
                    php_print(str("<li") + str(class_) + str("><a href='") + str(sub_item_[2]) + str("'") + str(class_) + str(aria_attributes_) + str(">") + str(title_) + str("</a></li>"))
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
_wp_menu_output(menu_, submenu_)
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
