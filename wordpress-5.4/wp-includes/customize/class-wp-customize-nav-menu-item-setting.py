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
#// Customize API: WP_Customize_Nav_Menu_Item_Setting class
#// 
#// @package WordPress
#// @subpackage Customize
#// @since 4.4.0
#// 
#// 
#// Customize Setting to represent a nav_menu.
#// 
#// Subclass of WP_Customize_Setting to represent a nav_menu taxonomy term, and
#// the IDs for the nav_menu_items associated with the nav menu.
#// 
#// @since 4.3.0
#// 
#// @see WP_Customize_Setting
#//
class WP_Customize_Nav_Menu_Item_Setting(WP_Customize_Setting):
    ID_PATTERN = "/^nav_menu_item\\[(?P<id>-?\\d+)\\]$/"
    POST_TYPE = "nav_menu_item"
    TYPE = "nav_menu_item"
    type = self.TYPE
    default = Array({"object_id": 0, "object": "", "menu_item_parent": 0, "position": 0, "type": "custom", "title": "", "url": "", "target": "", "attr_title": "", "description": "", "classes": "", "xfn": "", "status": "publish", "original_title": "", "nav_menu_term_id": 0, "_invalid": False})
    transport = "refresh"
    post_id = Array()
    value = Array()
    previous_post_id = Array()
    original_nav_menu_term_id = Array()
    is_updated = False
    update_status = Array()
    update_error = Array()
    #// 
    #// Constructor.
    #// 
    #// Any supplied $args override class property defaults.
    #// 
    #// @since 4.3.0
    #// 
    #// @param WP_Customize_Manager $manager Customizer bootstrap instance.
    #// @param string               $id      A specific ID of the setting.
    #// Can be a theme mod or option name.
    #// @param array                $args    Optional. Setting arguments.
    #// 
    #// @throws Exception If $id is not valid for this setting type.
    #//
    def __init__(self, manager=None, id=None, args=Array()):
        
        if php_empty(lambda : manager.nav_menus):
            raise php_new_class("Exception", lambda : Exception("Expected WP_Customize_Manager::$nav_menus to be set."))
        # end if
        if (not php_preg_match(self.ID_PATTERN, id, matches)):
            raise php_new_class("Exception", lambda : Exception(str("Illegal widget setting ID: ") + str(id)))
        # end if
        self.post_id = php_intval(matches["id"])
        add_action("wp_update_nav_menu_item", Array(self, "flush_cached_value"), 10, 2)
        super().__init__(manager, id, args)
        #// Ensure that an initially-supplied value is valid.
        if (php_isset(lambda : self.value)):
            self.populate_value()
            for missing in php_array_diff(php_array_keys(self.default), php_array_keys(self.value)):
                raise php_new_class("Exception", lambda : Exception(str("Supplied nav_menu_item value missing property: ") + str(missing)))
            # end for
        # end if
    # end def __init__
    #// 
    #// Clear the cached value when this nav menu item is updated.
    #// 
    #// @since 4.3.0
    #// 
    #// @param int $menu_id       The term ID for the menu.
    #// @param int $menu_item_id  The post ID for the menu item.
    #//
    def flush_cached_value(self, menu_id=None, menu_item_id=None):
        
        menu_id = None
        if menu_item_id == self.post_id:
            self.value = None
        # end if
    # end def flush_cached_value
    #// 
    #// Get the instance data for a given nav_menu_item setting.
    #// 
    #// @since 4.3.0
    #// 
    #// @see wp_setup_nav_menu_item()
    #// 
    #// @return array|false Instance data array, or false if the item is marked for deletion.
    #//
    def value(self):
        
        if self.is_previewed and get_current_blog_id() == self._previewed_blog_id:
            undefined = php_new_class("stdClass", lambda : stdClass())
            #// Symbol.
            post_value = self.post_value(undefined)
            if undefined == post_value:
                value = self._original_value
            else:
                value = post_value
            # end if
            if (not php_empty(lambda : value)) and php_empty(lambda : value["original_title"]):
                value["original_title"] = self.get_original_title(value)
            # end if
        elif (php_isset(lambda : self.value)):
            value = self.value
        else:
            value = False
            #// Note that a ID of less than one indicates a nav_menu not yet inserted.
            if self.post_id > 0:
                post = get_post(self.post_id)
                if post and self.POST_TYPE == post.post_type:
                    is_title_empty = php_empty(lambda : post.post_title)
                    value = wp_setup_nav_menu_item(post)
                    if is_title_empty:
                        value["title"] = ""
                    # end if
                # end if
            # end if
            if (not php_is_array(value)):
                value = self.default
            # end if
            #// Cache the value for future calls to avoid having to re-call wp_setup_nav_menu_item().
            self.value = value
            self.populate_value()
            value = self.value
        # end if
        if (not php_empty(lambda : value)) and php_empty(lambda : value["type_label"]):
            value["type_label"] = self.get_type_label(value)
        # end if
        return value
    # end def value
    #// 
    #// Get original title.
    #// 
    #// @since 4.7.0
    #// 
    #// @param object $item Nav menu item.
    #// @return string The original title.
    #//
    def get_original_title(self, item=None):
        
        original_title = ""
        if "post_type" == item.type and (not php_empty(lambda : item.object_id)):
            original_object = get_post(item.object_id)
            if original_object:
                #// This filter is documented in wp-includes/post-template.php
                original_title = apply_filters("the_title", original_object.post_title, original_object.ID)
                if "" == original_title:
                    #// translators: %d: ID of a post.
                    original_title = php_sprintf(__("#%d (no title)"), original_object.ID)
                # end if
            # end if
        elif "taxonomy" == item.type and (not php_empty(lambda : item.object_id)):
            original_term_title = get_term_field("name", item.object_id, item.object, "raw")
            if (not is_wp_error(original_term_title)):
                original_title = original_term_title
            # end if
        elif "post_type_archive" == item.type:
            original_object = get_post_type_object(item.object)
            if original_object:
                original_title = original_object.labels.archives
            # end if
        # end if
        original_title = html_entity_decode(original_title, ENT_QUOTES, get_bloginfo("charset"))
        return original_title
    # end def get_original_title
    #// 
    #// Get type label.
    #// 
    #// @since 4.7.0
    #// 
    #// @param object $item Nav menu item.
    #// @return string The type label.
    #//
    def get_type_label(self, item=None):
        
        if "post_type" == item.type:
            object = get_post_type_object(item.object)
            if object:
                type_label = object.labels.singular_name
            else:
                type_label = item.object
            # end if
        elif "taxonomy" == item.type:
            object = get_taxonomy(item.object)
            if object:
                type_label = object.labels.singular_name
            else:
                type_label = item.object
            # end if
        elif "post_type_archive" == item.type:
            type_label = __("Post Type Archive")
        else:
            type_label = __("Custom Link")
        # end if
        return type_label
    # end def get_type_label
    #// 
    #// Ensure that the value is fully populated with the necessary properties.
    #// 
    #// Translates some properties added by wp_setup_nav_menu_item() and removes others.
    #// 
    #// @since 4.3.0
    #// 
    #// @see WP_Customize_Nav_Menu_Item_Setting::value()
    #//
    def populate_value(self):
        
        if (not php_is_array(self.value)):
            return
        # end if
        if (php_isset(lambda : self.value["menu_order"])):
            self.value["position"] = self.value["menu_order"]
            self.value["menu_order"] = None
        # end if
        if (php_isset(lambda : self.value["post_status"])):
            self.value["status"] = self.value["post_status"]
            self.value["post_status"] = None
        # end if
        if (not (php_isset(lambda : self.value["original_title"]))):
            self.value["original_title"] = self.get_original_title(self.value)
        # end if
        if (not (php_isset(lambda : self.value["nav_menu_term_id"]))) and self.post_id > 0:
            menus = wp_get_post_terms(self.post_id, WP_Customize_Nav_Menu_Setting.TAXONOMY, Array({"fields": "ids"}))
            if (not php_empty(lambda : menus)):
                self.value["nav_menu_term_id"] = php_array_shift(menus)
            else:
                self.value["nav_menu_term_id"] = 0
            # end if
        # end if
        for key in Array("object_id", "menu_item_parent", "nav_menu_term_id"):
            if (not php_is_int(self.value[key])):
                self.value[key] = php_intval(self.value[key])
            # end if
        # end for
        for key in Array("classes", "xfn"):
            if php_is_array(self.value[key]):
                self.value[key] = php_implode(" ", self.value[key])
            # end if
        # end for
        if (not (php_isset(lambda : self.value["title"]))):
            self.value["title"] = ""
        # end if
        if (not (php_isset(lambda : self.value["_invalid"]))):
            self.value["_invalid"] = False
            is_known_invalid = "post_type" == self.value["type"] or "post_type_archive" == self.value["type"] and (not post_type_exists(self.value["object"])) or "taxonomy" == self.value["type"] and (not taxonomy_exists(self.value["object"]))
            if is_known_invalid:
                self.value["_invalid"] = True
            # end if
        # end if
        #// Remove remaining properties available on a setup nav_menu_item post object which aren't relevant to the setting value.
        irrelevant_properties = Array("ID", "comment_count", "comment_status", "db_id", "filter", "guid", "ping_status", "pinged", "post_author", "post_content", "post_content_filtered", "post_date", "post_date_gmt", "post_excerpt", "post_mime_type", "post_modified", "post_modified_gmt", "post_name", "post_parent", "post_password", "post_title", "post_type", "to_ping")
        for property in irrelevant_properties:
            self.value[property] = None
        # end for
    # end def populate_value
    #// 
    #// Handle previewing the setting.
    #// 
    #// @since 4.3.0
    #// @since 4.4.0 Added boolean return value.
    #// 
    #// @see WP_Customize_Manager::post_value()
    #// 
    #// @return bool False if method short-circuited due to no-op.
    #//
    def preview(self):
        
        if self.is_previewed:
            return False
        # end if
        undefined = php_new_class("stdClass", lambda : stdClass())
        is_placeholder = self.post_id < 0
        is_dirty = undefined != self.post_value(undefined)
        if (not is_placeholder) and (not is_dirty):
            return False
        # end if
        self.is_previewed = True
        self._original_value = self.value()
        self.original_nav_menu_term_id = self._original_value["nav_menu_term_id"]
        self._previewed_blog_id = get_current_blog_id()
        add_filter("wp_get_nav_menu_items", Array(self, "filter_wp_get_nav_menu_items"), 10, 3)
        sort_callback = Array(__CLASS__, "sort_wp_get_nav_menu_items")
        if (not has_filter("wp_get_nav_menu_items", sort_callback)):
            add_filter("wp_get_nav_menu_items", Array(__CLASS__, "sort_wp_get_nav_menu_items"), 1000, 3)
        # end if
        #// @todo Add get_post_metadata filters for plugins to add their data.
        return True
    # end def preview
    #// 
    #// Filters the wp_get_nav_menu_items() result to supply the previewed menu items.
    #// 
    #// @since 4.3.0
    #// 
    #// @see wp_get_nav_menu_items()
    #// 
    #// @param WP_Post[] $items An array of menu item post objects.
    #// @param WP_Term   $menu  The menu object.
    #// @param array     $args  An array of arguments used to retrieve menu item objects.
    #// @return WP_Post[] Array of menu item objects.
    #//
    def filter_wp_get_nav_menu_items(self, items=None, menu=None, args=None):
        
        this_item = self.value()
        current_nav_menu_term_id = None
        if (php_isset(lambda : this_item["nav_menu_term_id"])):
            current_nav_menu_term_id = this_item["nav_menu_term_id"]
            this_item["nav_menu_term_id"] = None
        # end if
        should_filter = menu.term_id == self.original_nav_menu_term_id or menu.term_id == current_nav_menu_term_id
        if (not should_filter):
            return items
        # end if
        #// Handle deleted menu item, or menu item moved to another menu.
        should_remove = False == this_item or (php_isset(lambda : this_item["_invalid"])) and True == this_item["_invalid"] or self.original_nav_menu_term_id == menu.term_id and current_nav_menu_term_id != self.original_nav_menu_term_id
        if should_remove:
            filtered_items = Array()
            for item in items:
                if item.db_id != self.post_id:
                    filtered_items[-1] = item
                # end if
            # end for
            return filtered_items
        # end if
        mutated = False
        should_update = php_is_array(this_item) and current_nav_menu_term_id == menu.term_id
        if should_update:
            for item in items:
                if item.db_id == self.post_id:
                    for key,value in get_object_vars(self.value_as_wp_post_nav_menu_item()):
                        item.key = value
                    # end for
                    mutated = True
                # end if
            # end for
            #// Not found so we have to append it..
            if (not mutated):
                items[-1] = self.value_as_wp_post_nav_menu_item()
            # end if
        # end if
        return items
    # end def filter_wp_get_nav_menu_items
    #// 
    #// Re-apply the tail logic also applied on $items by wp_get_nav_menu_items().
    #// 
    #// @since 4.3.0
    #// 
    #// @see wp_get_nav_menu_items()
    #// 
    #// @param WP_Post[] $items An array of menu item post objects.
    #// @param WP_Term   $menu  The menu object.
    #// @param array     $args  An array of arguments used to retrieve menu item objects.
    #// @return WP_Post[] Array of menu item objects.
    #//
    @classmethod
    def sort_wp_get_nav_menu_items(self, items=None, menu=None, args=None):
        
        args["include"] = None
        #// Remove invalid items only in front end.
        if (not is_admin()):
            items = php_array_filter(items, "_is_valid_nav_menu_item")
        # end if
        if ARRAY_A == args["output"]:
            items = wp_list_sort(items, Array({args["output_key"]: "ASC"}))
            i = 1
            for k,item in items:
                items[k].args["output_key"] = i
                i += 1
            # end for
        # end if
        return items
    # end def sort_wp_get_nav_menu_items
    #// 
    #// Get the value emulated into a WP_Post and set up as a nav_menu_item.
    #// 
    #// @since 4.3.0
    #// 
    #// @return WP_Post With wp_setup_nav_menu_item() applied.
    #//
    def value_as_wp_post_nav_menu_item(self):
        
        item = self.value()
        item.nav_menu_term_id = None
        item.post_status = item.status
        item.status = None
        item.post_type = "nav_menu_item"
        item.menu_order = item.position
        item.position = None
        if php_empty(lambda : item.original_title):
            item.original_title = self.get_original_title(item)
        # end if
        if php_empty(lambda : item.title) and (not php_empty(lambda : item.original_title)):
            item.title = item.original_title
        # end if
        if item.title:
            item.post_title = item.title
        # end if
        item.ID = self.post_id
        item.db_id = self.post_id
        post = php_new_class("WP_Post", lambda : WP_Post(item))
        if php_empty(lambda : post.post_author):
            post.post_author = get_current_user_id()
        # end if
        if (not (php_isset(lambda : post.type_label))):
            post.type_label = self.get_type_label(post)
        # end if
        #// Ensure nav menu item URL is set according to linked object.
        if "post_type" == post.type and (not php_empty(lambda : post.object_id)):
            post.url = get_permalink(post.object_id)
        elif "taxonomy" == post.type and (not php_empty(lambda : post.object)) and (not php_empty(lambda : post.object_id)):
            post.url = get_term_link(int(post.object_id), post.object)
        elif "post_type_archive" == post.type and (not php_empty(lambda : post.object)):
            post.url = get_post_type_archive_link(post.object)
        # end if
        if is_wp_error(post.url):
            post.url = ""
        # end if
        #// This filter is documented in wp-includes/nav-menu.php
        post.attr_title = apply_filters("nav_menu_attr_title", post.attr_title)
        #// This filter is documented in wp-includes/nav-menu.php
        post.description = apply_filters("nav_menu_description", wp_trim_words(post.description, 200))
        #// This filter is documented in wp-includes/nav-menu.php
        post = apply_filters("wp_setup_nav_menu_item", post)
        return post
    # end def value_as_wp_post_nav_menu_item
    #// 
    #// Sanitize an input.
    #// 
    #// Note that parent::sanitize() erroneously does wp_unslash() on $value, but
    #// we remove that in this override.
    #// 
    #// @since 4.3.0
    #// 
    #// @param array $menu_item_value The value to sanitize.
    #// @return array|false|null|WP_Error Null or WP_Error if an input isn't valid. False if it is marked for deletion.
    #// Otherwise the sanitized value.
    #//
    def sanitize(self, menu_item_value=None):
        
        #// Menu is marked for deletion.
        if False == menu_item_value:
            return menu_item_value
        # end if
        #// Invalid.
        if (not php_is_array(menu_item_value)):
            return None
        # end if
        default = Array({"object_id": 0, "object": "", "menu_item_parent": 0, "position": 0, "type": "custom", "title": "", "url": "", "target": "", "attr_title": "", "description": "", "classes": "", "xfn": "", "status": "publish", "original_title": "", "nav_menu_term_id": 0, "_invalid": False})
        menu_item_value = php_array_merge(default, menu_item_value)
        menu_item_value = wp_array_slice_assoc(menu_item_value, php_array_keys(default))
        menu_item_value["position"] = php_intval(menu_item_value["position"])
        for key in Array("object_id", "menu_item_parent", "nav_menu_term_id"):
            #// Note we need to allow negative-integer IDs for previewed objects not inserted yet.
            menu_item_value[key] = php_intval(menu_item_value[key])
        # end for
        for key in Array("type", "object", "target"):
            menu_item_value[key] = sanitize_key(menu_item_value[key])
        # end for
        for key in Array("xfn", "classes"):
            value = menu_item_value[key]
            if (not php_is_array(value)):
                value = php_explode(" ", value)
            # end if
            menu_item_value[key] = php_implode(" ", php_array_map("sanitize_html_class", value))
        # end for
        menu_item_value["original_title"] = sanitize_text_field(menu_item_value["original_title"])
        #// Apply the same filters as when calling wp_insert_post().
        #// This filter is documented in wp-includes/post.php
        menu_item_value["title"] = wp_unslash(apply_filters("title_save_pre", wp_slash(menu_item_value["title"])))
        #// This filter is documented in wp-includes/post.php
        menu_item_value["attr_title"] = wp_unslash(apply_filters("excerpt_save_pre", wp_slash(menu_item_value["attr_title"])))
        #// This filter is documented in wp-includes/post.php
        menu_item_value["description"] = wp_unslash(apply_filters("content_save_pre", wp_slash(menu_item_value["description"])))
        if "" != menu_item_value["url"]:
            menu_item_value["url"] = esc_url_raw(menu_item_value["url"])
            if "" == menu_item_value["url"]:
                return php_new_class("WP_Error", lambda : WP_Error("invalid_url", __("Invalid URL.")))
                pass
            # end if
        # end if
        if "publish" != menu_item_value["status"]:
            menu_item_value["status"] = "draft"
        # end if
        menu_item_value["_invalid"] = bool(menu_item_value["_invalid"])
        #// This filter is documented in wp-includes/class-wp-customize-setting.php
        return apply_filters(str("customize_sanitize_") + str(self.id), menu_item_value, self)
    # end def sanitize
    #// 
    #// Creates/updates the nav_menu_item post for this setting.
    #// 
    #// Any created menu items will have their assigned post IDs exported to the client
    #// via the {@see 'customize_save_response'} filter. Likewise, any errors will be
    #// exported to the client via the customize_save_response() filter.
    #// 
    #// To delete a menu, the client can send false as the value.
    #// 
    #// @since 4.3.0
    #// 
    #// @see wp_update_nav_menu_item()
    #// 
    #// @param array|false $value The menu item array to update. If false, then the menu item will be deleted
    #// entirely. See WP_Customize_Nav_Menu_Item_Setting::$default for what the value
    #// should consist of.
    #// @return null|void
    #//
    def update(self, value=None):
        
        if self.is_updated:
            return
        # end if
        self.is_updated = True
        is_placeholder = self.post_id < 0
        is_delete = False == value
        #// Update the cached value.
        self.value = value
        add_filter("customize_save_response", Array(self, "amend_customize_save_response"))
        if is_delete:
            #// If the current setting post is a placeholder, a delete request is a no-op.
            if is_placeholder:
                self.update_status = "deleted"
            else:
                r = wp_delete_post(self.post_id, True)
                if False == r:
                    self.update_error = php_new_class("WP_Error", lambda : WP_Error("delete_failure"))
                    self.update_status = "error"
                else:
                    self.update_status = "deleted"
                # end if
                pass
            # end if
        else:
            #// Handle saving menu items for menus that are being newly-created.
            if value["nav_menu_term_id"] < 0:
                nav_menu_setting_id = php_sprintf("nav_menu[%s]", value["nav_menu_term_id"])
                nav_menu_setting = self.manager.get_setting(nav_menu_setting_id)
                if (not nav_menu_setting) or (not type(nav_menu_setting).__name__ == "WP_Customize_Nav_Menu_Setting"):
                    self.update_status = "error"
                    self.update_error = php_new_class("WP_Error", lambda : WP_Error("unexpected_nav_menu_setting"))
                    return
                # end if
                if False == nav_menu_setting.save():
                    self.update_status = "error"
                    self.update_error = php_new_class("WP_Error", lambda : WP_Error("nav_menu_setting_failure"))
                    return
                # end if
                if php_intval(value["nav_menu_term_id"]) != nav_menu_setting.previous_term_id:
                    self.update_status = "error"
                    self.update_error = php_new_class("WP_Error", lambda : WP_Error("unexpected_previous_term_id"))
                    return
                # end if
                value["nav_menu_term_id"] = nav_menu_setting.term_id
            # end if
            #// Handle saving a nav menu item that is a child of a nav menu item being newly-created.
            if value["menu_item_parent"] < 0:
                parent_nav_menu_item_setting_id = php_sprintf("nav_menu_item[%s]", value["menu_item_parent"])
                parent_nav_menu_item_setting = self.manager.get_setting(parent_nav_menu_item_setting_id)
                if (not parent_nav_menu_item_setting) or (not type(parent_nav_menu_item_setting).__name__ == "WP_Customize_Nav_Menu_Item_Setting"):
                    self.update_status = "error"
                    self.update_error = php_new_class("WP_Error", lambda : WP_Error("unexpected_nav_menu_item_setting"))
                    return
                # end if
                if False == parent_nav_menu_item_setting.save():
                    self.update_status = "error"
                    self.update_error = php_new_class("WP_Error", lambda : WP_Error("nav_menu_item_setting_failure"))
                    return
                # end if
                if php_intval(value["menu_item_parent"]) != parent_nav_menu_item_setting.previous_post_id:
                    self.update_status = "error"
                    self.update_error = php_new_class("WP_Error", lambda : WP_Error("unexpected_previous_post_id"))
                    return
                # end if
                value["menu_item_parent"] = parent_nav_menu_item_setting.post_id
            # end if
            #// Insert or update menu.
            menu_item_data = Array({"menu-item-object-id": value["object_id"], "menu-item-object": value["object"], "menu-item-parent-id": value["menu_item_parent"], "menu-item-position": value["position"], "menu-item-type": value["type"], "menu-item-title": value["title"], "menu-item-url": value["url"], "menu-item-description": value["description"], "menu-item-attr-title": value["attr_title"], "menu-item-target": value["target"], "menu-item-classes": value["classes"], "menu-item-xfn": value["xfn"], "menu-item-status": value["status"]})
            r = wp_update_nav_menu_item(value["nav_menu_term_id"], 0 if is_placeholder else self.post_id, wp_slash(menu_item_data))
            if is_wp_error(r):
                self.update_status = "error"
                self.update_error = r
            else:
                if is_placeholder:
                    self.previous_post_id = self.post_id
                    self.post_id = r
                    self.update_status = "inserted"
                else:
                    self.update_status = "updated"
                # end if
            # end if
        # end if
    # end def update
    #// 
    #// Export data for the JS client.
    #// 
    #// @since 4.3.0
    #// 
    #// @see WP_Customize_Nav_Menu_Item_Setting::update()
    #// 
    #// @param array $data Additional information passed back to the 'saved' event on `wp.customize`.
    #// @return array Save response data.
    #//
    def amend_customize_save_response(self, data=None):
        
        if (not (php_isset(lambda : data["nav_menu_item_updates"]))):
            data["nav_menu_item_updates"] = Array()
        # end if
        data["nav_menu_item_updates"][-1] = Array({"post_id": self.post_id, "previous_post_id": self.previous_post_id, "error": self.update_error.get_error_code() if self.update_error else None, "status": self.update_status})
        return data
    # end def amend_customize_save_response
# end class WP_Customize_Nav_Menu_Item_Setting
