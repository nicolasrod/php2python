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
#// Build Administration Menu.
#// 
#// @package WordPress
#// @subpackage Administration
#//
if is_network_admin():
    #// 
    #// Fires before the administration menu loads in the Network Admin.
    #// 
    #// The hook fires before menus and sub-menus are removed based on user privileges.
    #// 
    #// @private
    #// @since 3.1.0
    #//
    do_action("_network_admin_menu")
elif is_user_admin():
    #// 
    #// Fires before the administration menu loads in the User Admin.
    #// 
    #// The hook fires before menus and sub-menus are removed based on user privileges.
    #// 
    #// @private
    #// @since 3.1.0
    #//
    do_action("_user_admin_menu")
else:
    #// 
    #// Fires before the administration menu loads in the admin.
    #// 
    #// The hook fires before menus and sub-menus are removed based on user privileges.
    #// 
    #// @private
    #// @since 2.2.0
    #//
    do_action("_admin_menu")
# end if
#// Create list of page plugin hook names.
for menu_page in menu:
    pos = php_strpos(menu_page[2], "?")
    if False != pos:
        #// Handle post_type=post|page|foo pages.
        hook_name = php_substr(menu_page[2], 0, pos)
        hook_args = php_substr(menu_page[2], pos + 1)
        wp_parse_str(hook_args, hook_args)
        #// Set the hook name to be the post type.
        if (php_isset(lambda : hook_args["post_type"])):
            hook_name = hook_args["post_type"]
        else:
            hook_name = php_basename(hook_name, ".php")
        # end if
        hook_args = None
    else:
        hook_name = php_basename(menu_page[2], ".php")
    # end if
    hook_name = sanitize_title(hook_name)
    if (php_isset(lambda : compat[hook_name])):
        hook_name = compat[hook_name]
    elif (not hook_name):
        continue
    # end if
    admin_page_hooks[menu_page[2]] = hook_name
# end for
menu_page = None
compat = None
_wp_submenu_nopriv = Array()
_wp_menu_nopriv = Array()
#// Loop over submenus and remove pages for which the user does not have privs.
for parent,sub in submenu:
    for index,data in sub:
        if (not current_user_can(data[1])):
            submenu[parent][index] = None
            _wp_submenu_nopriv[parent][data[2]] = True
        # end if
    # end for
    index = None
    data = None
    if php_empty(lambda : submenu[parent]):
        submenu[parent] = None
    # end if
# end for
sub = None
parent = None
#// 
#// Loop over the top-level menu.
#// Menus for which the original parent is not accessible due to lack of privileges
#// will have the next submenu in line be assigned as the new menu parent.
#//
for id,data in menu:
    if php_empty(lambda : submenu[data[2]]):
        continue
    # end if
    subs = submenu[data[2]]
    first_sub = reset(subs)
    old_parent = data[2]
    new_parent = first_sub[2]
    #// 
    #// If the first submenu is not the same as the assigned parent,
    #// make the first submenu the new parent.
    #//
    if new_parent != old_parent:
        _wp_real_parent_file[old_parent] = new_parent
        menu[id][2] = new_parent
        for index,data in submenu[old_parent]:
            submenu[new_parent][index] = submenu[old_parent][index]
            submenu[old_parent][index] = None
        # end for
        submenu[old_parent] = None
        index = None
        if (php_isset(lambda : _wp_submenu_nopriv[old_parent])):
            _wp_submenu_nopriv[new_parent] = _wp_submenu_nopriv[old_parent]
        # end if
    # end if
# end for
id = None
data = None
subs = None
first_sub = None
old_parent = None
new_parent = None
if is_network_admin():
    #// 
    #// Fires before the administration menu loads in the Network Admin.
    #// 
    #// @since 3.1.0
    #// 
    #// @param string $context Empty context.
    #//
    do_action("network_admin_menu", "")
elif is_user_admin():
    #// 
    #// Fires before the administration menu loads in the User Admin.
    #// 
    #// @since 3.1.0
    #// 
    #// @param string $context Empty context.
    #//
    do_action("user_admin_menu", "")
else:
    #// 
    #// Fires before the administration menu loads in the admin.
    #// 
    #// @since 1.5.0
    #// 
    #// @param string $context Empty context.
    #//
    do_action("admin_menu", "")
# end if
#// 
#// Remove menus that have no accessible submenus and require privileges
#// that the user does not have. Run re-parent loop again.
#//
for id,data in menu:
    if (not current_user_can(data[1])):
        _wp_menu_nopriv[data[2]] = True
    # end if
    #// 
    #// If there is only one submenu and it is has same destination as the parent,
    #// remove the submenu.
    #//
    if (not php_empty(lambda : submenu[data[2]])) and 1 == php_count(submenu[data[2]]):
        subs = submenu[data[2]]
        first_sub = reset(subs)
        if data[2] == first_sub[2]:
            submenu[data[2]] = None
        # end if
    # end if
    #// If submenu is empty...
    if php_empty(lambda : submenu[data[2]]):
        #// And user doesn't have privs, remove menu.
        if (php_isset(lambda : _wp_menu_nopriv[data[2]])):
            menu[id] = None
        # end if
    # end if
# end for
id = None
data = None
subs = None
first_sub = None
#// 
#// @param string $add
#// @param string $class
#// @return string
#//
def add_cssclass(add=None, class_=None, *args_):
    
    class_ = add if php_empty(lambda : class_) else class_ += " " + add
    return class_
# end def add_cssclass
#// 
#// @param array $menu
#// @return array
#//
def add_menu_classes(menu=None, *args_):
    
    first = False
    lastorder = False
    i = 0
    mc = php_count(menu)
    for order,top in menu:
        i += 1
        if 0 == order:
            #// Dashboard is always shown/single.
            menu[0][4] = add_cssclass("menu-top-first", top[4])
            lastorder = 0
            continue
        # end if
        if 0 == php_strpos(top[2], "separator") and False != lastorder:
            #// If separator.
            first = True
            c = menu[lastorder][4]
            menu[lastorder][4] = add_cssclass("menu-top-last", c)
            continue
        # end if
        if first:
            c = menu[order][4]
            menu[order][4] = add_cssclass("menu-top-first", c)
            first = False
        # end if
        if mc == i:
            #// Last item.
            c = menu[order][4]
            menu[order][4] = add_cssclass("menu-top-last", c)
        # end if
        lastorder = order
    # end for
    #// 
    #// Filters administration menus array with classes added for top-level items.
    #// 
    #// @since 2.7.0
    #// 
    #// @param array $menu Associative array of administration menu items.
    #//
    return apply_filters("add_menu_classes", menu)
# end def add_menu_classes
uksort(menu, "strnatcasecmp")
#// Make it all pretty.
#// 
#// Filters whether to enable custom ordering of the administration menu.
#// 
#// See the {@see 'menu_order'} filter for reordering menu items.
#// 
#// @since 2.8.0
#// 
#// @param bool $custom Whether custom ordering is enabled. Default false.
#//
if apply_filters("custom_menu_order", False):
    menu_order = Array()
    for menu_item in menu:
        menu_order[-1] = menu_item[2]
    # end for
    menu_item = None
    default_menu_order = menu_order
    #// 
    #// Filters the order of administration menu items.
    #// 
    #// A truthy value must first be passed to the {@see 'custom_menu_order'} filter
    #// for this filter to work. Use the following to enable custom menu ordering:
    #// 
    #// add_filter( 'custom_menu_order', '__return_true' );
    #// 
    #// @since 2.8.0
    #// 
    #// @param array $menu_order An ordered array of menu items.
    #//
    menu_order = apply_filters("menu_order", menu_order)
    menu_order = php_array_flip(menu_order)
    default_menu_order = php_array_flip(default_menu_order)
    #// 
    #// @global array $menu_order
    #// @global array $default_menu_order
    #// 
    #// @param array $a
    #// @param array $b
    #// @return int
    #//
    def sort_menu(a=None, b=None, *args_):
        
        global menu_order,default_menu_order
        php_check_if_defined("menu_order","default_menu_order")
        a = a[2]
        b = b[2]
        if (php_isset(lambda : menu_order[a])) and (not (php_isset(lambda : menu_order[b]))):
            return -1
        elif (not (php_isset(lambda : menu_order[a]))) and (php_isset(lambda : menu_order[b])):
            return 1
        elif (php_isset(lambda : menu_order[a])) and (php_isset(lambda : menu_order[b])):
            if menu_order[a] == menu_order[b]:
                return 0
            # end if
            return -1 if menu_order[a] < menu_order[b] else 1
        else:
            return -1 if default_menu_order[a] <= default_menu_order[b] else 1
        # end if
    # end def sort_menu
    usort(menu, "sort_menu")
    menu_order = None
    default_menu_order = None
# end if
#// Prevent adjacent separators.
prev_menu_was_separator = False
for id,data in menu:
    if False == php_stristr(data[4], "wp-menu-separator"):
        #// This item is not a separator, so falsey the toggler and do nothing.
        prev_menu_was_separator = False
    else:
        #// The previous item was a separator, so unset this one.
        if True == prev_menu_was_separator:
            menu[id] = None
        # end if
        #// This item is a separator, so truthy the toggler and move on.
        prev_menu_was_separator = True
    # end if
# end for
id = None
data = None
prev_menu_was_separator = None
#// Remove the last menu item if it is a separator.
last_menu_key = php_array_keys(menu)
last_menu_key = php_array_pop(last_menu_key)
if (not php_empty(lambda : menu)) and "wp-menu-separator" == menu[last_menu_key][4]:
    menu[last_menu_key] = None
# end if
last_menu_key = None
if (not user_can_access_admin_page()):
    #// 
    #// Fires when access to an admin page is denied.
    #// 
    #// @since 2.5.0
    #//
    do_action("admin_page_access_denied")
    wp_die(__("Sorry, you are not allowed to access this page."), 403)
# end if
menu = add_menu_classes(menu)
