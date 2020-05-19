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
for menu_page_ in menu_:
    pos_ = php_strpos(menu_page_[2], "?")
    if False != pos_:
        #// Handle post_type=post|page|foo pages.
        hook_name_ = php_substr(menu_page_[2], 0, pos_)
        hook_args_ = php_substr(menu_page_[2], pos_ + 1)
        wp_parse_str(hook_args_, hook_args_)
        #// Set the hook name to be the post type.
        if (php_isset(lambda : hook_args_["post_type"])):
            hook_name_ = hook_args_["post_type"]
        else:
            hook_name_ = php_basename(hook_name_, ".php")
        # end if
        hook_args_ = None
    else:
        hook_name_ = php_basename(menu_page_[2], ".php")
    # end if
    hook_name_ = sanitize_title(hook_name_)
    if (php_isset(lambda : compat_[hook_name_])):
        hook_name_ = compat_[hook_name_]
    elif (not hook_name_):
        continue
    # end if
    admin_page_hooks_[menu_page_[2]] = hook_name_
# end for
menu_page_ = None
compat_ = None
_wp_submenu_nopriv_ = Array()
_wp_menu_nopriv_ = Array()
#// Loop over submenus and remove pages for which the user does not have privs.
for parent_,sub_ in submenu_.items():
    for index_,data_ in sub_.items():
        if (not current_user_can(data_[1])):
            submenu_[parent_][index_] = None
            _wp_submenu_nopriv_[parent_][data_[2]] = True
        # end if
    # end for
    index_ = None
    data_ = None
    if php_empty(lambda : submenu_[parent_]):
        submenu_[parent_] = None
    # end if
# end for
sub_ = None
parent_ = None
#// 
#// Loop over the top-level menu.
#// Menus for which the original parent is not accessible due to lack of privileges
#// will have the next submenu in line be assigned as the new menu parent.
#//
for id_,data_ in menu_.items():
    if php_empty(lambda : submenu_[data_[2]]):
        continue
    # end if
    subs_ = submenu_[data_[2]]
    first_sub_ = reset(subs_)
    old_parent_ = data_[2]
    new_parent_ = first_sub_[2]
    #// 
    #// If the first submenu is not the same as the assigned parent,
    #// make the first submenu the new parent.
    #//
    if new_parent_ != old_parent_:
        _wp_real_parent_file_[old_parent_] = new_parent_
        menu_[id_][2] = new_parent_
        for index_,data_ in submenu_[old_parent_].items():
            submenu_[new_parent_][index_] = submenu_[old_parent_][index_]
            submenu_[old_parent_][index_] = None
        # end for
        submenu_[old_parent_] = None
        index_ = None
        if (php_isset(lambda : _wp_submenu_nopriv_[old_parent_])):
            _wp_submenu_nopriv_[new_parent_] = _wp_submenu_nopriv_[old_parent_]
        # end if
    # end if
# end for
id_ = None
data_ = None
subs_ = None
first_sub_ = None
old_parent_ = None
new_parent_ = None
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
for id_,data_ in menu_.items():
    if (not current_user_can(data_[1])):
        _wp_menu_nopriv_[data_[2]] = True
    # end if
    #// 
    #// If there is only one submenu and it is has same destination as the parent,
    #// remove the submenu.
    #//
    if (not php_empty(lambda : submenu_[data_[2]])) and 1 == php_count(submenu_[data_[2]]):
        subs_ = submenu_[data_[2]]
        first_sub_ = reset(subs_)
        if data_[2] == first_sub_[2]:
            submenu_[data_[2]] = None
        # end if
    # end if
    #// If submenu is empty...
    if php_empty(lambda : submenu_[data_[2]]):
        #// And user doesn't have privs, remove menu.
        if (php_isset(lambda : _wp_menu_nopriv_[data_[2]])):
            menu_[id_] = None
        # end if
    # end if
# end for
id_ = None
data_ = None
subs_ = None
first_sub_ = None
#// 
#// @param string $add
#// @param string $class
#// @return string
#//
def add_cssclass(add_=None, class_=None, *_args_):
    
    
    class_ = add_ if php_empty(lambda : class_) else class_ += " " + add_
    return class_
# end def add_cssclass
#// 
#// @param array $menu
#// @return array
#//
def add_menu_classes(menu_=None, *_args_):
    
    
    first_ = False
    lastorder_ = False
    i_ = 0
    mc_ = php_count(menu_)
    for order_,top_ in menu_.items():
        i_ += 1
        if 0 == order_:
            #// Dashboard is always shown/single.
            menu_[0][4] = add_cssclass("menu-top-first", top_[4])
            lastorder_ = 0
            continue
        # end if
        if 0 == php_strpos(top_[2], "separator") and False != lastorder_:
            #// If separator.
            first_ = True
            c_ = menu_[lastorder_][4]
            menu_[lastorder_][4] = add_cssclass("menu-top-last", c_)
            continue
        # end if
        if first_:
            c_ = menu_[order_][4]
            menu_[order_][4] = add_cssclass("menu-top-first", c_)
            first_ = False
        # end if
        if mc_ == i_:
            #// Last item.
            c_ = menu_[order_][4]
            menu_[order_][4] = add_cssclass("menu-top-last", c_)
        # end if
        lastorder_ = order_
    # end for
    #// 
    #// Filters administration menus array with classes added for top-level items.
    #// 
    #// @since 2.7.0
    #// 
    #// @param array $menu Associative array of administration menu items.
    #//
    return apply_filters("add_menu_classes", menu_)
# end def add_menu_classes
uksort(menu_, "strnatcasecmp")
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
    menu_order_ = Array()
    for menu_item_ in menu_:
        menu_order_[-1] = menu_item_[2]
    # end for
    menu_item_ = None
    default_menu_order_ = menu_order_
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
    menu_order_ = apply_filters("menu_order", menu_order_)
    menu_order_ = php_array_flip(menu_order_)
    default_menu_order_ = php_array_flip(default_menu_order_)
    #// 
    #// @global array $menu_order
    #// @global array $default_menu_order
    #// 
    #// @param array $a
    #// @param array $b
    #// @return int
    #//
    def sort_menu(a_=None, b_=None, *_args_):
        
        
        global menu_order_
        global default_menu_order_
        php_check_if_defined("menu_order_","default_menu_order_")
        a_ = a_[2]
        b_ = b_[2]
        if (php_isset(lambda : menu_order_[a_])) and (not (php_isset(lambda : menu_order_[b_]))):
            return -1
        elif (not (php_isset(lambda : menu_order_[a_]))) and (php_isset(lambda : menu_order_[b_])):
            return 1
        elif (php_isset(lambda : menu_order_[a_])) and (php_isset(lambda : menu_order_[b_])):
            if menu_order_[a_] == menu_order_[b_]:
                return 0
            # end if
            return -1 if menu_order_[a_] < menu_order_[b_] else 1
        else:
            return -1 if default_menu_order_[a_] <= default_menu_order_[b_] else 1
        # end if
    # end def sort_menu
    usort(menu_, "sort_menu")
    menu_order_ = None
    default_menu_order_ = None
# end if
#// Prevent adjacent separators.
prev_menu_was_separator_ = False
for id_,data_ in menu_.items():
    if False == php_stristr(data_[4], "wp-menu-separator"):
        #// This item is not a separator, so falsey the toggler and do nothing.
        prev_menu_was_separator_ = False
    else:
        #// The previous item was a separator, so unset this one.
        if True == prev_menu_was_separator_:
            menu_[id_] = None
        # end if
        #// This item is a separator, so truthy the toggler and move on.
        prev_menu_was_separator_ = True
    # end if
# end for
id_ = None
data_ = None
prev_menu_was_separator_ = None
#// Remove the last menu item if it is a separator.
last_menu_key_ = php_array_keys(menu_)
last_menu_key_ = php_array_pop(last_menu_key_)
if (not php_empty(lambda : menu_)) and "wp-menu-separator" == menu_[last_menu_key_][4]:
    menu_[last_menu_key_] = None
# end if
last_menu_key_ = None
if (not user_can_access_admin_page()):
    #// 
    #// Fires when access to an admin page is denied.
    #// 
    #// @since 2.5.0
    #//
    do_action("admin_page_access_denied")
    wp_die(__("Sorry, you are not allowed to access this page."), 403)
# end if
menu_ = add_menu_classes(menu_)
