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
#// Toolbar API: WP_Admin_Bar class
#// 
#// @package WordPress
#// @subpackage Toolbar
#// @since 3.1.0
#// 
#// 
#// Core class used to implement the Toolbar API.
#// 
#// @since 3.1.0
#//
class WP_Admin_Bar():
    nodes = Array()
    bound = False
    user = Array()
    #// 
    #// @param string $name
    #// @return string|array|void
    #//
    def __get(self, name=None):
        
        for case in Switch(name):
            if case("proto"):
                return "https://" if is_ssl() else "http://"
            # end if
            if case("menu"):
                _deprecated_argument("WP_Admin_Bar", "3.3.0", "Modify admin bar nodes with WP_Admin_Bar::get_node(), WP_Admin_Bar::add_node(), and WP_Admin_Bar::remove_node(), not the <code>menu</code> property.")
                return Array()
            # end if
        # end for
    # end def __get
    #// 
    #//
    def initialize(self):
        
        self.user = php_new_class("stdClass", lambda : stdClass())
        if is_user_logged_in():
            #// Populate settings we need for the menu based on the current user.
            self.user.blogs = get_blogs_of_user(get_current_user_id())
            if is_multisite():
                self.user.active_blog = get_active_blog_for_user(get_current_user_id())
                self.user.domain = user_admin_url() if php_empty(lambda : self.user.active_blog) else trailingslashit(get_home_url(self.user.active_blog.blog_id))
                self.user.account_domain = self.user.domain
            else:
                self.user.active_blog = self.user.blogs[get_current_blog_id()]
                self.user.domain = trailingslashit(home_url())
                self.user.account_domain = self.user.domain
            # end if
        # end if
        add_action("wp_head", "wp_admin_bar_header")
        add_action("admin_head", "wp_admin_bar_header")
        if current_theme_supports("admin-bar"):
            #// 
            #// To remove the default padding styles from WordPress for the Toolbar, use the following code:
            #// add_theme_support( 'admin-bar', array( 'callback' => '__return_false' ) );
            #//
            admin_bar_args = get_theme_support("admin-bar")
            header_callback = admin_bar_args[0]["callback"]
        # end if
        if php_empty(lambda : header_callback):
            header_callback = "_admin_bar_bump_cb"
        # end if
        add_action("wp_head", header_callback)
        wp_enqueue_script("admin-bar")
        wp_enqueue_style("admin-bar")
        #// 
        #// Fires after WP_Admin_Bar is initialized.
        #// 
        #// @since 3.1.0
        #//
        do_action("admin_bar_init")
    # end def initialize
    #// 
    #// Add a node (menu item) to the Admin Bar menu.
    #// 
    #// @since 3.3.0
    #// 
    #// @param array $node The attributes that define the node.
    #//
    def add_menu(self, node=None):
        
        self.add_node(node)
    # end def add_menu
    #// 
    #// Remove a node from the admin bar.
    #// 
    #// @since 3.1.0
    #// 
    #// @param string $id The menu slug to remove.
    #//
    def remove_menu(self, id=None):
        
        self.remove_node(id)
    # end def remove_menu
    #// 
    #// Adds a node to the menu.
    #// 
    #// @since 3.1.0
    #// @since 4.5.0 Added the ability to pass 'lang' and 'dir' meta data.
    #// 
    #// @param array $args {
    #// Arguments for adding a node.
    #// 
    #// @type string $id     ID of the item.
    #// @type string $title  Title of the node.
    #// @type string $parent Optional. ID of the parent node.
    #// @type string $href   Optional. Link for the item.
    #// @type bool   $group  Optional. Whether or not the node is a group. Default false.
    #// @type array  $meta   Meta data including the following keys: 'html', 'class', 'rel', 'lang', 'dir',
    #// 'onclick', 'target', 'title', 'tabindex'. Default empty.
    #// }
    #//
    def add_node(self, args=None):
        
        #// Shim for old method signature: add_node( $parent_id, $menu_obj, $args ).
        if php_func_num_args() >= 3 and php_is_string(args):
            args = php_array_merge(Array({"parent": args}), php_func_get_arg(2))
        # end if
        if php_is_object(args):
            args = get_object_vars(args)
        # end if
        #// Ensure we have a valid title.
        if php_empty(lambda : args["id"]):
            if php_empty(lambda : args["title"]):
                return
            # end if
            _doing_it_wrong(__METHOD__, __("The menu ID should not be empty."), "3.3.0")
            #// Deprecated: Generate an ID from the title.
            args["id"] = esc_attr(sanitize_title(php_trim(args["title"])))
        # end if
        defaults = Array({"id": False, "title": False, "parent": False, "href": False, "group": False, "meta": Array()})
        #// If the node already exists, keep any data that isn't provided.
        maybe_defaults = self.get_node(args["id"])
        if maybe_defaults:
            defaults = get_object_vars(maybe_defaults)
        # end if
        #// Do the same for 'meta' items.
        if (not php_empty(lambda : defaults["meta"])) and (not php_empty(lambda : args["meta"])):
            args["meta"] = wp_parse_args(args["meta"], defaults["meta"])
        # end if
        args = wp_parse_args(args, defaults)
        back_compat_parents = Array({"my-account-with-avatar": Array("my-account", "3.3"), "my-blogs": Array("my-sites", "3.3")})
        if (php_isset(lambda : back_compat_parents[args["parent"]])):
            new_parent, version = back_compat_parents[args["parent"]]
            _deprecated_argument(__METHOD__, version, php_sprintf("Use <code>%s</code> as the parent for the <code>%s</code> admin bar node instead of <code>%s</code>.", new_parent, args["id"], args["parent"]))
            args["parent"] = new_parent
        # end if
        self._set_node(args)
    # end def add_node
    #// 
    #// @param array $args
    #//
    def _set_node(self, args=None):
        
        self.nodes[args["id"]] = args
    # end def _set_node
    #// 
    #// Gets a node.
    #// 
    #// @param string $id
    #// @return object|void Node.
    #//
    def get_node(self, id=None):
        
        node = self._get_node(id)
        if node:
            return copy.deepcopy(node)
        # end if
    # end def get_node
    #// 
    #// @param string $id
    #// @return object|void
    #//
    def _get_node(self, id=None):
        
        if self.bound:
            return
        # end if
        if php_empty(lambda : id):
            id = "root"
        # end if
        if (php_isset(lambda : self.nodes[id])):
            return self.nodes[id]
        # end if
    # end def _get_node
    #// 
    #// @return array|void
    #//
    def get_nodes(self):
        
        nodes = self._get_nodes()
        if (not nodes):
            return
        # end if
        for node in nodes:
            node = copy.deepcopy(node)
        # end for
        return nodes
    # end def get_nodes
    #// 
    #// @return array|void
    #//
    def _get_nodes(self):
        
        if self.bound:
            return
        # end if
        return self.nodes
    # end def _get_nodes
    #// 
    #// Add a group to a menu node.
    #// 
    #// @since 3.3.0
    #// 
    #// @param array $args {
    #// Array of arguments for adding a group.
    #// 
    #// @type string $id     ID of the item.
    #// @type string $parent Optional. ID of the parent node. Default 'root'.
    #// @type array  $meta   Meta data for the group including the following keys:
    #// 'class', 'onclick', 'target', and 'title'.
    #// }
    #//
    def add_group(self, args=None):
        
        args["group"] = True
        self.add_node(args)
    # end def add_group
    #// 
    #// Remove a node.
    #// 
    #// @param string $id The ID of the item.
    #//
    def remove_node(self, id=None):
        
        self._unset_node(id)
    # end def remove_node
    #// 
    #// @param string $id
    #//
    def _unset_node(self, id=None):
        
        self.nodes[id] = None
    # end def _unset_node
    #// 
    #//
    def render(self):
        
        root = self._bind()
        if root:
            self._render(root)
        # end if
    # end def render
    #// 
    #// @return object|void
    #//
    def _bind(self):
        
        if self.bound:
            return
        # end if
        #// Add the root node.
        #// Clear it first, just in case. Don't mess with The Root.
        self.remove_node("root")
        self.add_node(Array({"id": "root", "group": False}))
        #// Normalize nodes: define internal 'children' and 'type' properties.
        for node in self._get_nodes():
            node.children = Array()
            node.type = "group" if node.group else "item"
            node.group = None
            #// The Root wants your orphans. No lonely items allowed.
            if (not node.parent):
                node.parent = "root"
            # end if
        # end for
        for node in self._get_nodes():
            if "root" == node.id:
                continue
            # end if
            #// Fetch the parent node. If it isn't registered, ignore the node.
            parent = self._get_node(node.parent)
            if (not parent):
                continue
            # end if
            #// Generate the group class (we distinguish between top level and other level groups).
            group_class = "ab-top-menu" if "root" == node.parent else "ab-submenu"
            if "group" == node.type:
                if php_empty(lambda : node.meta["class"]):
                    node.meta["class"] = group_class
                else:
                    node.meta["class"] += " " + group_class
                # end if
            # end if
            #// Items in items aren't allowed. Wrap nested items in 'default' groups.
            if "item" == parent.type and "item" == node.type:
                default_id = parent.id + "-default"
                default = self._get_node(default_id)
                #// The default group is added here to allow groups that are
                #// added before standard menu items to render first.
                if (not default):
                    #// Use _set_node because add_node can be overloaded.
                    #// Make sure to specify default settings for all properties.
                    self._set_node(Array({"id": default_id, "parent": parent.id, "type": "group", "children": Array(), "meta": Array({"class": group_class})}, {"title": False, "href": False}))
                    default = self._get_node(default_id)
                    parent.children[-1] = default
                # end if
                parent = default
                pass
            elif "group" == parent.type and "group" == node.type:
                container_id = parent.id + "-container"
                container = self._get_node(container_id)
                #// We need to create a container for this group, life is sad.
                if (not container):
                    #// Use _set_node because add_node can be overloaded.
                    #// Make sure to specify default settings for all properties.
                    self._set_node(Array({"id": container_id, "type": "container", "children": Array(parent), "parent": False, "title": False, "href": False, "meta": Array()}))
                    container = self._get_node(container_id)
                    #// Link the container node if a grandparent node exists.
                    grandparent = self._get_node(parent.parent)
                    if grandparent:
                        container.parent = grandparent.id
                        index = php_array_search(parent, grandparent.children, True)
                        if False == index:
                            grandparent.children[-1] = container
                        else:
                            array_splice(grandparent.children, index, 1, Array(container))
                        # end if
                    # end if
                    parent.parent = container.id
                # end if
                parent = container
            # end if
            #// Update the parent ID (it might have changed).
            node.parent = parent.id
            #// Add the node to the tree.
            parent.children[-1] = node
        # end for
        root = self._get_node("root")
        self.bound = True
        return root
    # end def _bind
    #// 
    #// @global bool $is_IE
    #// @param object $root
    #//
    def _render(self, root=None):
        
        global is_IE
        php_check_if_defined("is_IE")
        #// Add browser classes.
        #// We have to do this here since admin bar shows on the front end.
        class_ = "nojq nojs"
        if is_IE:
            if php_strpos(PHP_SERVER["HTTP_USER_AGENT"], "MSIE 7"):
                class_ += " ie7"
            elif php_strpos(PHP_SERVER["HTTP_USER_AGENT"], "MSIE 8"):
                class_ += " ie8"
            elif php_strpos(PHP_SERVER["HTTP_USER_AGENT"], "MSIE 9"):
                class_ += " ie9"
            # end if
        elif wp_is_mobile():
            class_ += " mobile"
        # end if
        php_print("     <div id=\"wpadminbar\" class=\"")
        php_print(class_)
        php_print("\">\n            ")
        if (not is_admin()):
            php_print("             <a class=\"screen-reader-shortcut\" href=\"#wp-toolbar\" tabindex=\"1\">")
            _e("Skip to toolbar")
            php_print("</a>\n           ")
        # end if
        php_print("         <div class=\"quicklinks\" id=\"wp-toolbar\" role=\"navigation\" aria-label=\"")
        esc_attr_e("Toolbar")
        php_print("\">\n                ")
        for group in root.children:
            self._render_group(group)
        # end for
        php_print("         </div>\n            ")
        if is_user_logged_in():
            php_print("         <a class=\"screen-reader-shortcut\" href=\"")
            php_print(esc_url(wp_logout_url()))
            php_print("\">")
            _e("Log Out")
            php_print("</a>\n           ")
        # end if
        php_print("     </div>\n\n      ")
    # end def _render
    #// 
    #// @param object $node
    #//
    def _render_container(self, node=None):
        
        if "container" != node.type or php_empty(lambda : node.children):
            return
        # end if
        php_print("<div id=\"" + esc_attr("wp-admin-bar-" + node.id) + "\" class=\"ab-group-container\">")
        for group in node.children:
            self._render_group(group)
        # end for
        php_print("</div>")
    # end def _render_container
    #// 
    #// @param object $node
    #//
    def _render_group(self, node=None):
        
        if "container" == node.type:
            self._render_container(node)
            return
        # end if
        if "group" != node.type or php_empty(lambda : node.children):
            return
        # end if
        if (not php_empty(lambda : node.meta["class"])):
            class_ = " class=\"" + esc_attr(php_trim(node.meta["class"])) + "\""
        else:
            class_ = ""
        # end if
        php_print("<ul id='" + esc_attr("wp-admin-bar-" + node.id) + str("'") + str(class_) + str(">"))
        for item in node.children:
            self._render_item(item)
        # end for
        php_print("</ul>")
    # end def _render_group
    #// 
    #// @param object $node
    #//
    def _render_item(self, node=None):
        
        if "item" != node.type:
            return
        # end if
        is_parent = (not php_empty(lambda : node.children))
        has_link = (not php_empty(lambda : node.href))
        is_root_top_item = "root-default" == node.parent
        is_top_secondary_item = "top-secondary" == node.parent
        #// Allow only numeric values, then casted to integers, and allow a tabindex value of `0` for a11y.
        tabindex = int(node.meta["tabindex"]) if (php_isset(lambda : node.meta["tabindex"])) and php_is_numeric(node.meta["tabindex"]) else ""
        aria_attributes = " tabindex=\"" + tabindex + "\"" if "" != tabindex else ""
        menuclass = ""
        arrow = ""
        if is_parent:
            menuclass = "menupop "
            aria_attributes += " aria-haspopup=\"true\""
        # end if
        if (not php_empty(lambda : node.meta["class"])):
            menuclass += node.meta["class"]
        # end if
        #// Print the arrow icon for the menu children with children.
        if (not is_root_top_item) and (not is_top_secondary_item) and is_parent:
            arrow = "<span class=\"wp-admin-bar-arrow\" aria-hidden=\"true\"></span>"
        # end if
        if menuclass:
            menuclass = " class=\"" + esc_attr(php_trim(menuclass)) + "\""
        # end if
        php_print("<li id='" + esc_attr("wp-admin-bar-" + node.id) + str("'") + str(menuclass) + str(">"))
        if has_link:
            attributes = Array("onclick", "target", "title", "rel", "lang", "dir")
            php_print(str("<a class='ab-item'") + str(aria_attributes) + str(" href='") + esc_url(node.href) + "'")
        else:
            attributes = Array("onclick", "target", "title", "rel", "lang", "dir")
            php_print("<div class=\"ab-item ab-empty-item\"" + aria_attributes)
        # end if
        for attribute in attributes:
            if php_empty(lambda : node.meta[attribute]):
                continue
            # end if
            if "onclick" == attribute:
                php_print(str(" ") + str(attribute) + str("='") + esc_js(node.meta[attribute]) + "'")
            else:
                php_print(str(" ") + str(attribute) + str("='") + esc_attr(node.meta[attribute]) + "'")
            # end if
        # end for
        php_print(str(">") + str(arrow) + str(node.title))
        if has_link:
            php_print("</a>")
        else:
            php_print("</div>")
        # end if
        if is_parent:
            php_print("<div class=\"ab-sub-wrapper\">")
            for group in node.children:
                self._render_group(group)
            # end for
            php_print("</div>")
        # end if
        if (not php_empty(lambda : node.meta["html"])):
            php_print(node.meta["html"])
        # end if
        php_print("</li>")
    # end def _render_item
    #// 
    #// Renders toolbar items recursively.
    #// 
    #// @since 3.1.0
    #// @deprecated 3.3.0 Use WP_Admin_Bar::_render_item() or WP_Admin_bar::render() instead.
    #// @see WP_Admin_Bar::_render_item()
    #// @see WP_Admin_Bar::render()
    #// 
    #// @param string $id    Unused.
    #// @param object $node
    #//
    def recursive_render(self, id=None, node=None):
        
        _deprecated_function(__METHOD__, "3.3.0", "WP_Admin_bar::render(), WP_Admin_Bar::_render_item()")
        self._render_item(node)
    # end def recursive_render
    #// 
    #//
    def add_menus(self):
        
        #// User-related, aligned right.
        add_action("admin_bar_menu", "wp_admin_bar_my_account_menu", 0)
        add_action("admin_bar_menu", "wp_admin_bar_search_menu", 4)
        add_action("admin_bar_menu", "wp_admin_bar_my_account_item", 7)
        add_action("admin_bar_menu", "wp_admin_bar_recovery_mode_menu", 8)
        #// Site-related.
        add_action("admin_bar_menu", "wp_admin_bar_sidebar_toggle", 0)
        add_action("admin_bar_menu", "wp_admin_bar_wp_menu", 10)
        add_action("admin_bar_menu", "wp_admin_bar_my_sites_menu", 20)
        add_action("admin_bar_menu", "wp_admin_bar_site_menu", 30)
        add_action("admin_bar_menu", "wp_admin_bar_customize_menu", 40)
        add_action("admin_bar_menu", "wp_admin_bar_updates_menu", 50)
        #// Content-related.
        if (not is_network_admin()) and (not is_user_admin()):
            add_action("admin_bar_menu", "wp_admin_bar_comments_menu", 60)
            add_action("admin_bar_menu", "wp_admin_bar_new_content_menu", 70)
        # end if
        add_action("admin_bar_menu", "wp_admin_bar_edit_menu", 80)
        add_action("admin_bar_menu", "wp_admin_bar_add_secondary_groups", 200)
        #// 
        #// Fires after menus are added to the menu bar.
        #// 
        #// @since 3.1.0
        #//
        do_action("add_admin_bar_menus")
    # end def add_menus
# end class WP_Admin_Bar
