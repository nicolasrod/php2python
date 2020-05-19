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
    #// 
    #// Setting type.
    #// 
    #// @since 4.3.0
    #// @var string
    #//
    type = self.TYPE
    #// 
    #// Default setting value.
    #// 
    #// @since 4.3.0
    #// @var array
    #// 
    #// @see wp_setup_nav_menu_item()
    #//
    default = Array({"object_id": 0, "object": "", "menu_item_parent": 0, "position": 0, "type": "custom", "title": "", "url": "", "target": "", "attr_title": "", "description": "", "classes": "", "xfn": "", "status": "publish", "original_title": "", "nav_menu_term_id": 0, "_invalid": False})
    #// 
    #// Default transport.
    #// 
    #// @since 4.3.0
    #// @since 4.5.0 Default changed to 'refresh'
    #// @var string
    #//
    transport = "refresh"
    #// 
    #// The post ID represented by this setting instance. This is the db_id.
    #// 
    #// A negative value represents a placeholder ID for a new menu not yet saved.
    #// 
    #// @since 4.3.0
    #// @var int
    #//
    post_id = Array()
    #// 
    #// Storage of pre-setup menu item to prevent wasted calls to wp_setup_nav_menu_item().
    #// 
    #// @since 4.3.0
    #// @var array|null
    #//
    value = Array()
    #// 
    #// Previous (placeholder) post ID used before creating a new menu item.
    #// 
    #// This value will be exported to JS via the customize_save_response filter
    #// so that JavaScript can update the settings to refer to the newly-assigned
    #// post ID. This value is always negative to indicate it does not refer to
    #// a real post.
    #// 
    #// @since 4.3.0
    #// @var int
    #// 
    #// @see WP_Customize_Nav_Menu_Item_Setting::update()
    #// @see WP_Customize_Nav_Menu_Item_Setting::amend_customize_save_response()
    #//
    previous_post_id = Array()
    #// 
    #// When previewing or updating a menu item, this stores the previous nav_menu_term_id
    #// which ensures that we can apply the proper filters.
    #// 
    #// @since 4.3.0
    #// @var int
    #//
    original_nav_menu_term_id = Array()
    #// 
    #// Whether or not update() was called.
    #// 
    #// @since 4.3.0
    #// @var bool
    #//
    is_updated = False
    #// 
    #// Status for calling the update method, used in customize_save_response filter.
    #// 
    #// See {@see 'customize_save_response'}.
    #// 
    #// When status is inserted, the placeholder post ID is stored in $previous_post_id.
    #// When status is error, the error is stored in $update_error.
    #// 
    #// @since 4.3.0
    #// @var string updated|inserted|deleted|error
    #// 
    #// @see WP_Customize_Nav_Menu_Item_Setting::update()
    #// @see WP_Customize_Nav_Menu_Item_Setting::amend_customize_save_response()
    #//
    update_status = Array()
    #// 
    #// Any error object returned by wp_update_nav_menu_item() when setting is updated.
    #// 
    #// @since 4.3.0
    #// @var WP_Error
    #// 
    #// @see WP_Customize_Nav_Menu_Item_Setting::update()
    #// @see WP_Customize_Nav_Menu_Item_Setting::amend_customize_save_response()
    #//
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
    def __init__(self, manager_=None, id_=None, args_=None):
        if args_ is None:
            args_ = Array()
        # end if
        
        if php_empty(lambda : manager_.nav_menus):
            raise php_new_class("Exception", lambda : Exception("Expected WP_Customize_Manager::$nav_menus to be set."))
        # end if
        if (not php_preg_match(self.ID_PATTERN, id_, matches_)):
            raise php_new_class("Exception", lambda : Exception(str("Illegal widget setting ID: ") + str(id_)))
        # end if
        self.post_id = php_intval(matches_["id"])
        add_action("wp_update_nav_menu_item", Array(self, "flush_cached_value"), 10, 2)
        super().__init__(manager_, id_, args_)
        #// Ensure that an initially-supplied value is valid.
        if (php_isset(lambda : self.value)):
            self.populate_value()
            for missing_ in php_array_diff(php_array_keys(self.default), php_array_keys(self.value)):
                raise php_new_class("Exception", lambda : Exception(str("Supplied nav_menu_item value missing property: ") + str(missing_)))
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
    def flush_cached_value(self, menu_id_=None, menu_item_id_=None):
        
        
        menu_id_ = None
        if menu_item_id_ == self.post_id:
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
            undefined_ = php_new_class("stdClass", lambda : stdClass())
            #// Symbol.
            post_value_ = self.post_value(undefined_)
            if undefined_ == post_value_:
                value_ = self._original_value
            else:
                value_ = post_value_
            # end if
            if (not php_empty(lambda : value_)) and php_empty(lambda : value_["original_title"]):
                value_["original_title"] = self.get_original_title(value_)
            # end if
        elif (php_isset(lambda : self.value)):
            value_ = self.value
        else:
            value_ = False
            #// Note that a ID of less than one indicates a nav_menu not yet inserted.
            if self.post_id > 0:
                post_ = get_post(self.post_id)
                if post_ and self.POST_TYPE == post_.post_type:
                    is_title_empty_ = php_empty(lambda : post_.post_title)
                    value_ = wp_setup_nav_menu_item(post_)
                    if is_title_empty_:
                        value_["title"] = ""
                    # end if
                # end if
            # end if
            if (not php_is_array(value_)):
                value_ = self.default
            # end if
            #// Cache the value for future calls to avoid having to re-call wp_setup_nav_menu_item().
            self.value = value_
            self.populate_value()
            value_ = self.value
        # end if
        if (not php_empty(lambda : value_)) and php_empty(lambda : value_["type_label"]):
            value_["type_label"] = self.get_type_label(value_)
        # end if
        return value_
    # end def value
    #// 
    #// Get original title.
    #// 
    #// @since 4.7.0
    #// 
    #// @param object $item Nav menu item.
    #// @return string The original title.
    #//
    def get_original_title(self, item_=None):
        
        
        original_title_ = ""
        if "post_type" == item_.type and (not php_empty(lambda : item_.object_id)):
            original_object_ = get_post(item_.object_id)
            if original_object_:
                #// This filter is documented in wp-includes/post-template.php
                original_title_ = apply_filters("the_title", original_object_.post_title, original_object_.ID)
                if "" == original_title_:
                    #// translators: %d: ID of a post.
                    original_title_ = php_sprintf(__("#%d (no title)"), original_object_.ID)
                # end if
            # end if
        elif "taxonomy" == item_.type and (not php_empty(lambda : item_.object_id)):
            original_term_title_ = get_term_field("name", item_.object_id, item_.object, "raw")
            if (not is_wp_error(original_term_title_)):
                original_title_ = original_term_title_
            # end if
        elif "post_type_archive" == item_.type:
            original_object_ = get_post_type_object(item_.object)
            if original_object_:
                original_title_ = original_object_.labels.archives
            # end if
        # end if
        original_title_ = html_entity_decode(original_title_, ENT_QUOTES, get_bloginfo("charset"))
        return original_title_
    # end def get_original_title
    #// 
    #// Get type label.
    #// 
    #// @since 4.7.0
    #// 
    #// @param object $item Nav menu item.
    #// @return string The type label.
    #//
    def get_type_label(self, item_=None):
        
        
        if "post_type" == item_.type:
            object_ = get_post_type_object(item_.object)
            if object_:
                type_label_ = object_.labels.singular_name
            else:
                type_label_ = item_.object
            # end if
        elif "taxonomy" == item_.type:
            object_ = get_taxonomy(item_.object)
            if object_:
                type_label_ = object_.labels.singular_name
            else:
                type_label_ = item_.object
            # end if
        elif "post_type_archive" == item_.type:
            type_label_ = __("Post Type Archive")
        else:
            type_label_ = __("Custom Link")
        # end if
        return type_label_
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
            menus_ = wp_get_post_terms(self.post_id, WP_Customize_Nav_Menu_Setting.TAXONOMY, Array({"fields": "ids"}))
            if (not php_empty(lambda : menus_)):
                self.value["nav_menu_term_id"] = php_array_shift(menus_)
            else:
                self.value["nav_menu_term_id"] = 0
            # end if
        # end if
        for key_ in Array("object_id", "menu_item_parent", "nav_menu_term_id"):
            if (not php_is_int(self.value[key_])):
                self.value[key_] = php_intval(self.value[key_])
            # end if
        # end for
        for key_ in Array("classes", "xfn"):
            if php_is_array(self.value[key_]):
                self.value[key_] = php_implode(" ", self.value[key_])
            # end if
        # end for
        if (not (php_isset(lambda : self.value["title"]))):
            self.value["title"] = ""
        # end if
        if (not (php_isset(lambda : self.value["_invalid"]))):
            self.value["_invalid"] = False
            is_known_invalid_ = "post_type" == self.value["type"] or "post_type_archive" == self.value["type"] and (not post_type_exists(self.value["object"])) or "taxonomy" == self.value["type"] and (not taxonomy_exists(self.value["object"]))
            if is_known_invalid_:
                self.value["_invalid"] = True
            # end if
        # end if
        #// Remove remaining properties available on a setup nav_menu_item post object which aren't relevant to the setting value.
        irrelevant_properties_ = Array("ID", "comment_count", "comment_status", "db_id", "filter", "guid", "ping_status", "pinged", "post_author", "post_content", "post_content_filtered", "post_date", "post_date_gmt", "post_excerpt", "post_mime_type", "post_modified", "post_modified_gmt", "post_name", "post_parent", "post_password", "post_title", "post_type", "to_ping")
        for property_ in irrelevant_properties_:
            self.value[property_] = None
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
        undefined_ = php_new_class("stdClass", lambda : stdClass())
        is_placeholder_ = self.post_id < 0
        is_dirty_ = undefined_ != self.post_value(undefined_)
        if (not is_placeholder_) and (not is_dirty_):
            return False
        # end if
        self.is_previewed = True
        self._original_value = self.value()
        self.original_nav_menu_term_id = self._original_value["nav_menu_term_id"]
        self._previewed_blog_id = get_current_blog_id()
        add_filter("wp_get_nav_menu_items", Array(self, "filter_wp_get_nav_menu_items"), 10, 3)
        sort_callback_ = Array(self.__class__.__name__, "sort_wp_get_nav_menu_items")
        if (not has_filter("wp_get_nav_menu_items", sort_callback_)):
            add_filter("wp_get_nav_menu_items", Array(self.__class__.__name__, "sort_wp_get_nav_menu_items"), 1000, 3)
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
    def filter_wp_get_nav_menu_items(self, items_=None, menu_=None, args_=None):
        
        
        this_item_ = self.value()
        current_nav_menu_term_id_ = None
        if (php_isset(lambda : this_item_["nav_menu_term_id"])):
            current_nav_menu_term_id_ = this_item_["nav_menu_term_id"]
            this_item_["nav_menu_term_id"] = None
        # end if
        should_filter_ = menu_.term_id == self.original_nav_menu_term_id or menu_.term_id == current_nav_menu_term_id_
        if (not should_filter_):
            return items_
        # end if
        #// Handle deleted menu item, or menu item moved to another menu.
        should_remove_ = False == this_item_ or (php_isset(lambda : this_item_["_invalid"])) and True == this_item_["_invalid"] or self.original_nav_menu_term_id == menu_.term_id and current_nav_menu_term_id_ != self.original_nav_menu_term_id
        if should_remove_:
            filtered_items_ = Array()
            for item_ in items_:
                if item_.db_id != self.post_id:
                    filtered_items_[-1] = item_
                # end if
            # end for
            return filtered_items_
        # end if
        mutated_ = False
        should_update_ = php_is_array(this_item_) and current_nav_menu_term_id_ == menu_.term_id
        if should_update_:
            for item_ in items_:
                if item_.db_id == self.post_id:
                    for key_,value_ in get_object_vars(self.value_as_wp_post_nav_menu_item()).items():
                        item_.key_ = value_
                    # end for
                    mutated_ = True
                # end if
            # end for
            #// Not found so we have to append it..
            if (not mutated_):
                items_[-1] = self.value_as_wp_post_nav_menu_item()
            # end if
        # end if
        return items_
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
    def sort_wp_get_nav_menu_items(self, items_=None, menu_=None, args_=None):
        
        
        args_["include"] = None
        #// Remove invalid items only in front end.
        if (not is_admin()):
            items_ = php_array_filter(items_, "_is_valid_nav_menu_item")
        # end if
        if ARRAY_A == args_["output"]:
            items_ = wp_list_sort(items_, Array({args_["output_key"]: "ASC"}))
            i_ = 1
            for k_,item_ in items_.items():
                items_[k_].args_["output_key"] = i_
                i_ += 1
                i_ += 1
            # end for
        # end if
        return items_
    # end def sort_wp_get_nav_menu_items
    #// 
    #// Get the value emulated into a WP_Post and set up as a nav_menu_item.
    #// 
    #// @since 4.3.0
    #// 
    #// @return WP_Post With wp_setup_nav_menu_item() applied.
    #//
    def value_as_wp_post_nav_menu_item(self):
        
        
        item_ = self.value()
        item_.nav_menu_term_id = None
        item_.post_status = item_.status
        item_.status = None
        item_.post_type = "nav_menu_item"
        item_.menu_order = item_.position
        item_.position = None
        if php_empty(lambda : item_.original_title):
            item_.original_title = self.get_original_title(item_)
        # end if
        if php_empty(lambda : item_.title) and (not php_empty(lambda : item_.original_title)):
            item_.title = item_.original_title
        # end if
        if item_.title:
            item_.post_title = item_.title
        # end if
        item_.ID = self.post_id
        item_.db_id = self.post_id
        post_ = php_new_class("WP_Post", lambda : WP_Post(item_))
        if php_empty(lambda : post_.post_author):
            post_.post_author = get_current_user_id()
        # end if
        if (not (php_isset(lambda : post_.type_label))):
            post_.type_label = self.get_type_label(post_)
        # end if
        #// Ensure nav menu item URL is set according to linked object.
        if "post_type" == post_.type and (not php_empty(lambda : post_.object_id)):
            post_.url = get_permalink(post_.object_id)
        elif "taxonomy" == post_.type and (not php_empty(lambda : post_.object)) and (not php_empty(lambda : post_.object_id)):
            post_.url = get_term_link(php_int(post_.object_id), post_.object)
        elif "post_type_archive" == post_.type and (not php_empty(lambda : post_.object)):
            post_.url = get_post_type_archive_link(post_.object)
        # end if
        if is_wp_error(post_.url):
            post_.url = ""
        # end if
        #// This filter is documented in wp-includes/nav-menu.php
        post_.attr_title = apply_filters("nav_menu_attr_title", post_.attr_title)
        #// This filter is documented in wp-includes/nav-menu.php
        post_.description = apply_filters("nav_menu_description", wp_trim_words(post_.description, 200))
        #// This filter is documented in wp-includes/nav-menu.php
        post_ = apply_filters("wp_setup_nav_menu_item", post_)
        return post_
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
    def sanitize(self, menu_item_value_=None):
        
        
        #// Menu is marked for deletion.
        if False == menu_item_value_:
            return menu_item_value_
        # end if
        #// Invalid.
        if (not php_is_array(menu_item_value_)):
            return None
        # end if
        default_ = Array({"object_id": 0, "object": "", "menu_item_parent": 0, "position": 0, "type": "custom", "title": "", "url": "", "target": "", "attr_title": "", "description": "", "classes": "", "xfn": "", "status": "publish", "original_title": "", "nav_menu_term_id": 0, "_invalid": False})
        menu_item_value_ = php_array_merge(default_, menu_item_value_)
        menu_item_value_ = wp_array_slice_assoc(menu_item_value_, php_array_keys(default_))
        menu_item_value_["position"] = php_intval(menu_item_value_["position"])
        for key_ in Array("object_id", "menu_item_parent", "nav_menu_term_id"):
            #// Note we need to allow negative-integer IDs for previewed objects not inserted yet.
            menu_item_value_[key_] = php_intval(menu_item_value_[key_])
        # end for
        for key_ in Array("type", "object", "target"):
            menu_item_value_[key_] = sanitize_key(menu_item_value_[key_])
        # end for
        for key_ in Array("xfn", "classes"):
            value_ = menu_item_value_[key_]
            if (not php_is_array(value_)):
                value_ = php_explode(" ", value_)
            # end if
            menu_item_value_[key_] = php_implode(" ", php_array_map("sanitize_html_class", value_))
        # end for
        menu_item_value_["original_title"] = sanitize_text_field(menu_item_value_["original_title"])
        #// Apply the same filters as when calling wp_insert_post().
        #// This filter is documented in wp-includes/post.php
        menu_item_value_["title"] = wp_unslash(apply_filters("title_save_pre", wp_slash(menu_item_value_["title"])))
        #// This filter is documented in wp-includes/post.php
        menu_item_value_["attr_title"] = wp_unslash(apply_filters("excerpt_save_pre", wp_slash(menu_item_value_["attr_title"])))
        #// This filter is documented in wp-includes/post.php
        menu_item_value_["description"] = wp_unslash(apply_filters("content_save_pre", wp_slash(menu_item_value_["description"])))
        if "" != menu_item_value_["url"]:
            menu_item_value_["url"] = esc_url_raw(menu_item_value_["url"])
            if "" == menu_item_value_["url"]:
                return php_new_class("WP_Error", lambda : WP_Error("invalid_url", __("Invalid URL.")))
                pass
            # end if
        # end if
        if "publish" != menu_item_value_["status"]:
            menu_item_value_["status"] = "draft"
        # end if
        menu_item_value_["_invalid"] = php_bool(menu_item_value_["_invalid"])
        #// This filter is documented in wp-includes/class-wp-customize-setting.php
        return apply_filters(str("customize_sanitize_") + str(self.id), menu_item_value_, self)
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
    def update(self, value_=None):
        
        
        if self.is_updated:
            return
        # end if
        self.is_updated = True
        is_placeholder_ = self.post_id < 0
        is_delete_ = False == value_
        #// Update the cached value.
        self.value = value_
        add_filter("customize_save_response", Array(self, "amend_customize_save_response"))
        if is_delete_:
            #// If the current setting post is a placeholder, a delete request is a no-op.
            if is_placeholder_:
                self.update_status = "deleted"
            else:
                r_ = wp_delete_post(self.post_id, True)
                if False == r_:
                    self.update_error = php_new_class("WP_Error", lambda : WP_Error("delete_failure"))
                    self.update_status = "error"
                else:
                    self.update_status = "deleted"
                # end if
                pass
            # end if
        else:
            #// Handle saving menu items for menus that are being newly-created.
            if value_["nav_menu_term_id"] < 0:
                nav_menu_setting_id_ = php_sprintf("nav_menu[%s]", value_["nav_menu_term_id"])
                nav_menu_setting_ = self.manager.get_setting(nav_menu_setting_id_)
                if (not nav_menu_setting_) or (not type(nav_menu_setting_).__name__ == "WP_Customize_Nav_Menu_Setting"):
                    self.update_status = "error"
                    self.update_error = php_new_class("WP_Error", lambda : WP_Error("unexpected_nav_menu_setting"))
                    return
                # end if
                if False == nav_menu_setting_.save():
                    self.update_status = "error"
                    self.update_error = php_new_class("WP_Error", lambda : WP_Error("nav_menu_setting_failure"))
                    return
                # end if
                if php_intval(value_["nav_menu_term_id"]) != nav_menu_setting_.previous_term_id:
                    self.update_status = "error"
                    self.update_error = php_new_class("WP_Error", lambda : WP_Error("unexpected_previous_term_id"))
                    return
                # end if
                value_["nav_menu_term_id"] = nav_menu_setting_.term_id
            # end if
            #// Handle saving a nav menu item that is a child of a nav menu item being newly-created.
            if value_["menu_item_parent"] < 0:
                parent_nav_menu_item_setting_id_ = php_sprintf("nav_menu_item[%s]", value_["menu_item_parent"])
                parent_nav_menu_item_setting_ = self.manager.get_setting(parent_nav_menu_item_setting_id_)
                if (not parent_nav_menu_item_setting_) or (not type(parent_nav_menu_item_setting_).__name__ == "WP_Customize_Nav_Menu_Item_Setting"):
                    self.update_status = "error"
                    self.update_error = php_new_class("WP_Error", lambda : WP_Error("unexpected_nav_menu_item_setting"))
                    return
                # end if
                if False == parent_nav_menu_item_setting_.save():
                    self.update_status = "error"
                    self.update_error = php_new_class("WP_Error", lambda : WP_Error("nav_menu_item_setting_failure"))
                    return
                # end if
                if php_intval(value_["menu_item_parent"]) != parent_nav_menu_item_setting_.previous_post_id:
                    self.update_status = "error"
                    self.update_error = php_new_class("WP_Error", lambda : WP_Error("unexpected_previous_post_id"))
                    return
                # end if
                value_["menu_item_parent"] = parent_nav_menu_item_setting_.post_id
            # end if
            #// Insert or update menu.
            menu_item_data_ = Array({"menu-item-object-id": value_["object_id"], "menu-item-object": value_["object"], "menu-item-parent-id": value_["menu_item_parent"], "menu-item-position": value_["position"], "menu-item-type": value_["type"], "menu-item-title": value_["title"], "menu-item-url": value_["url"], "menu-item-description": value_["description"], "menu-item-attr-title": value_["attr_title"], "menu-item-target": value_["target"], "menu-item-classes": value_["classes"], "menu-item-xfn": value_["xfn"], "menu-item-status": value_["status"]})
            r_ = wp_update_nav_menu_item(value_["nav_menu_term_id"], 0 if is_placeholder_ else self.post_id, wp_slash(menu_item_data_))
            if is_wp_error(r_):
                self.update_status = "error"
                self.update_error = r_
            else:
                if is_placeholder_:
                    self.previous_post_id = self.post_id
                    self.post_id = r_
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
    def amend_customize_save_response(self, data_=None):
        
        
        if (not (php_isset(lambda : data_["nav_menu_item_updates"]))):
            data_["nav_menu_item_updates"] = Array()
        # end if
        data_["nav_menu_item_updates"][-1] = Array({"post_id": self.post_id, "previous_post_id": self.previous_post_id, "error": self.update_error.get_error_code() if self.update_error else None, "status": self.update_status})
        return data_
    # end def amend_customize_save_response
# end class WP_Customize_Nav_Menu_Item_Setting
