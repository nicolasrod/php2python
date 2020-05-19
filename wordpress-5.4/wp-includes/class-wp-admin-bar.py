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
    def __get(self, name_=None):
        
        
        for case in Switch(name_):
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
            admin_bar_args_ = get_theme_support("admin-bar")
            header_callback_ = admin_bar_args_[0]["callback"]
        # end if
        if php_empty(lambda : header_callback_):
            header_callback_ = "_admin_bar_bump_cb"
        # end if
        add_action("wp_head", header_callback_)
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
    def add_menu(self, node_=None):
        
        
        self.add_node(node_)
    # end def add_menu
    #// 
    #// Remove a node from the admin bar.
    #// 
    #// @since 3.1.0
    #// 
    #// @param string $id The menu slug to remove.
    #//
    def remove_menu(self, id_=None):
        
        
        self.remove_node(id_)
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
    def add_node(self, args_=None):
        
        
        #// Shim for old method signature: add_node( $parent_id, $menu_obj, $args ).
        if php_func_num_args() >= 3 and php_is_string(args_):
            args_ = php_array_merge(Array({"parent": args_}), php_func_get_arg(2))
        # end if
        if php_is_object(args_):
            args_ = get_object_vars(args_)
        # end if
        #// Ensure we have a valid title.
        if php_empty(lambda : args_["id"]):
            if php_empty(lambda : args_["title"]):
                return
            # end if
            _doing_it_wrong(inspect.currentframe().f_code.co_name, __("The menu ID should not be empty."), "3.3.0")
            #// Deprecated: Generate an ID from the title.
            args_["id"] = esc_attr(sanitize_title(php_trim(args_["title"])))
        # end if
        defaults_ = Array({"id": False, "title": False, "parent": False, "href": False, "group": False, "meta": Array()})
        #// If the node already exists, keep any data that isn't provided.
        maybe_defaults_ = self.get_node(args_["id"])
        if maybe_defaults_:
            defaults_ = get_object_vars(maybe_defaults_)
        # end if
        #// Do the same for 'meta' items.
        if (not php_empty(lambda : defaults_["meta"])) and (not php_empty(lambda : args_["meta"])):
            args_["meta"] = wp_parse_args(args_["meta"], defaults_["meta"])
        # end if
        args_ = wp_parse_args(args_, defaults_)
        back_compat_parents_ = Array({"my-account-with-avatar": Array("my-account", "3.3"), "my-blogs": Array("my-sites", "3.3")})
        if (php_isset(lambda : back_compat_parents_[args_["parent"]])):
            new_parent_, version_ = back_compat_parents_[args_["parent"]]
            _deprecated_argument(inspect.currentframe().f_code.co_name, version_, php_sprintf("Use <code>%s</code> as the parent for the <code>%s</code> admin bar node instead of <code>%s</code>.", new_parent_, args_["id"], args_["parent"]))
            args_["parent"] = new_parent_
        # end if
        self._set_node(args_)
    # end def add_node
    #// 
    #// @param array $args
    #//
    def _set_node(self, args_=None):
        
        
        self.nodes[args_["id"]] = args_
    # end def _set_node
    #// 
    #// Gets a node.
    #// 
    #// @param string $id
    #// @return object|void Node.
    #//
    def get_node(self, id_=None):
        
        
        node_ = self._get_node(id_)
        if node_:
            return copy.deepcopy(node_)
        # end if
    # end def get_node
    #// 
    #// @param string $id
    #// @return object|void
    #//
    def _get_node(self, id_=None):
        
        
        if self.bound:
            return
        # end if
        if php_empty(lambda : id_):
            id_ = "root"
        # end if
        if (php_isset(lambda : self.nodes[id_])):
            return self.nodes[id_]
        # end if
    # end def _get_node
    #// 
    #// @return array|void
    #//
    def get_nodes(self):
        
        
        nodes_ = self._get_nodes()
        if (not nodes_):
            return
        # end if
        for node_ in nodes_:
            node_ = copy.deepcopy(node_)
        # end for
        return nodes_
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
    def add_group(self, args_=None):
        
        
        args_["group"] = True
        self.add_node(args_)
    # end def add_group
    #// 
    #// Remove a node.
    #// 
    #// @param string $id The ID of the item.
    #//
    def remove_node(self, id_=None):
        
        
        self._unset_node(id_)
    # end def remove_node
    #// 
    #// @param string $id
    #//
    def _unset_node(self, id_=None):
        
        
        self.nodes[id_] = None
    # end def _unset_node
    #// 
    #//
    def render(self):
        
        
        root_ = self._bind()
        if root_:
            self._render(root_)
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
        for node_ in self._get_nodes():
            node_.children = Array()
            node_.type = "group" if node_.group else "item"
            node_.group = None
            #// The Root wants your orphans. No lonely items allowed.
            if (not node_.parent):
                node_.parent = "root"
            # end if
        # end for
        for node_ in self._get_nodes():
            if "root" == node_.id:
                continue
            # end if
            #// Fetch the parent node. If it isn't registered, ignore the node.
            parent_ = self._get_node(node_.parent)
            if (not parent_):
                continue
            # end if
            #// Generate the group class (we distinguish between top level and other level groups).
            group_class_ = "ab-top-menu" if "root" == node_.parent else "ab-submenu"
            if "group" == node_.type:
                if php_empty(lambda : node_.meta["class"]):
                    node_.meta["class"] = group_class_
                else:
                    node_.meta["class"] += " " + group_class_
                # end if
            # end if
            #// Items in items aren't allowed. Wrap nested items in 'default' groups.
            if "item" == parent_.type and "item" == node_.type:
                default_id_ = parent_.id + "-default"
                default_ = self._get_node(default_id_)
                #// The default group is added here to allow groups that are
                #// added before standard menu items to render first.
                if (not default_):
                    #// Use _set_node because add_node can be overloaded.
                    #// Make sure to specify default settings for all properties.
                    self._set_node(Array({"id": default_id_, "parent": parent_.id, "type": "group", "children": Array(), "meta": Array({"class": group_class_})}, {"title": False, "href": False}))
                    default_ = self._get_node(default_id_)
                    parent_.children[-1] = default_
                # end if
                parent_ = default_
                pass
            elif "group" == parent_.type and "group" == node_.type:
                container_id_ = parent_.id + "-container"
                container_ = self._get_node(container_id_)
                #// We need to create a container for this group, life is sad.
                if (not container_):
                    #// Use _set_node because add_node can be overloaded.
                    #// Make sure to specify default settings for all properties.
                    self._set_node(Array({"id": container_id_, "type": "container", "children": Array(parent_), "parent": False, "title": False, "href": False, "meta": Array()}))
                    container_ = self._get_node(container_id_)
                    #// Link the container node if a grandparent node exists.
                    grandparent_ = self._get_node(parent_.parent)
                    if grandparent_:
                        container_.parent = grandparent_.id
                        index_ = php_array_search(parent_, grandparent_.children, True)
                        if False == index_:
                            grandparent_.children[-1] = container_
                        else:
                            array_splice(grandparent_.children, index_, 1, Array(container_))
                        # end if
                    # end if
                    parent_.parent = container_.id
                # end if
                parent_ = container_
            # end if
            #// Update the parent ID (it might have changed).
            node_.parent = parent_.id
            #// Add the node to the tree.
            parent_.children[-1] = node_
        # end for
        root_ = self._get_node("root")
        self.bound = True
        return root_
    # end def _bind
    #// 
    #// @global bool $is_IE
    #// @param object $root
    #//
    def _render(self, root_=None):
        
        
        global is_IE_
        php_check_if_defined("is_IE_")
        #// Add browser classes.
        #// We have to do this here since admin bar shows on the front end.
        class_ = "nojq nojs"
        if is_IE_:
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
        for group_ in root_.children:
            self._render_group(group_)
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
    def _render_container(self, node_=None):
        
        
        if "container" != node_.type or php_empty(lambda : node_.children):
            return
        # end if
        php_print("<div id=\"" + esc_attr("wp-admin-bar-" + node_.id) + "\" class=\"ab-group-container\">")
        for group_ in node_.children:
            self._render_group(group_)
        # end for
        php_print("</div>")
    # end def _render_container
    #// 
    #// @param object $node
    #//
    def _render_group(self, node_=None):
        
        
        if "container" == node_.type:
            self._render_container(node_)
            return
        # end if
        if "group" != node_.type or php_empty(lambda : node_.children):
            return
        # end if
        if (not php_empty(lambda : node_.meta["class"])):
            class_ = " class=\"" + esc_attr(php_trim(node_.meta["class"])) + "\""
        else:
            class_ = ""
        # end if
        php_print("<ul id='" + esc_attr("wp-admin-bar-" + node_.id) + str("'") + str(class_) + str(">"))
        for item_ in node_.children:
            self._render_item(item_)
        # end for
        php_print("</ul>")
    # end def _render_group
    #// 
    #// @param object $node
    #//
    def _render_item(self, node_=None):
        
        
        if "item" != node_.type:
            return
        # end if
        is_parent_ = (not php_empty(lambda : node_.children))
        has_link_ = (not php_empty(lambda : node_.href))
        is_root_top_item_ = "root-default" == node_.parent
        is_top_secondary_item_ = "top-secondary" == node_.parent
        #// Allow only numeric values, then casted to integers, and allow a tabindex value of `0` for a11y.
        tabindex_ = php_int(node_.meta["tabindex"]) if (php_isset(lambda : node_.meta["tabindex"])) and php_is_numeric(node_.meta["tabindex"]) else ""
        aria_attributes_ = " tabindex=\"" + tabindex_ + "\"" if "" != tabindex_ else ""
        menuclass_ = ""
        arrow_ = ""
        if is_parent_:
            menuclass_ = "menupop "
            aria_attributes_ += " aria-haspopup=\"true\""
        # end if
        if (not php_empty(lambda : node_.meta["class"])):
            menuclass_ += node_.meta["class"]
        # end if
        #// Print the arrow icon for the menu children with children.
        if (not is_root_top_item_) and (not is_top_secondary_item_) and is_parent_:
            arrow_ = "<span class=\"wp-admin-bar-arrow\" aria-hidden=\"true\"></span>"
        # end if
        if menuclass_:
            menuclass_ = " class=\"" + esc_attr(php_trim(menuclass_)) + "\""
        # end if
        php_print("<li id='" + esc_attr("wp-admin-bar-" + node_.id) + str("'") + str(menuclass_) + str(">"))
        if has_link_:
            attributes_ = Array("onclick", "target", "title", "rel", "lang", "dir")
            php_print(str("<a class='ab-item'") + str(aria_attributes_) + str(" href='") + esc_url(node_.href) + "'")
        else:
            attributes_ = Array("onclick", "target", "title", "rel", "lang", "dir")
            php_print("<div class=\"ab-item ab-empty-item\"" + aria_attributes_)
        # end if
        for attribute_ in attributes_:
            if php_empty(lambda : node_.meta[attribute_]):
                continue
            # end if
            if "onclick" == attribute_:
                php_print(str(" ") + str(attribute_) + str("='") + esc_js(node_.meta[attribute_]) + "'")
            else:
                php_print(str(" ") + str(attribute_) + str("='") + esc_attr(node_.meta[attribute_]) + "'")
            # end if
        # end for
        php_print(str(">") + str(arrow_) + str(node_.title))
        if has_link_:
            php_print("</a>")
        else:
            php_print("</div>")
        # end if
        if is_parent_:
            php_print("<div class=\"ab-sub-wrapper\">")
            for group_ in node_.children:
                self._render_group(group_)
            # end for
            php_print("</div>")
        # end if
        if (not php_empty(lambda : node_.meta["html"])):
            php_print(node_.meta["html"])
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
    def recursive_render(self, id_=None, node_=None):
        
        
        _deprecated_function(inspect.currentframe().f_code.co_name, "3.3.0", "WP_Admin_bar::render(), WP_Admin_Bar::_render_item()")
        self._render_item(node_)
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
