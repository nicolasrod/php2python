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
#// Customize API: WP_Customize_Nav_Menu_Setting class
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
#// @see wp_get_nav_menu_object()
#// @see WP_Customize_Setting
#//
class WP_Customize_Nav_Menu_Setting(WP_Customize_Setting):
    ID_PATTERN = "/^nav_menu\\[(?P<id>-?\\d+)\\]$/"
    TAXONOMY = "nav_menu"
    TYPE = "nav_menu"
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
    #// @see wp_get_nav_menu_object()
    #//
    default = Array({"name": "", "description": "", "parent": 0, "auto_add": False})
    #// 
    #// Default transport.
    #// 
    #// @since 4.3.0
    #// @var string
    #//
    transport = "postMessage"
    #// 
    #// The term ID represented by this setting instance.
    #// 
    #// A negative value represents a placeholder ID for a new menu not yet saved.
    #// 
    #// @since 4.3.0
    #// @var int
    #//
    term_id = Array()
    #// 
    #// Previous (placeholder) term ID used before creating a new menu.
    #// 
    #// This value will be exported to JS via the {@see 'customize_save_response'} filter
    #// so that JavaScript can update the settings to refer to the newly-assigned
    #// term ID. This value is always negative to indicate it does not refer to
    #// a real term.
    #// 
    #// @since 4.3.0
    #// @var int
    #// 
    #// @see WP_Customize_Nav_Menu_Setting::update()
    #// @see WP_Customize_Nav_Menu_Setting::amend_customize_save_response()
    #//
    previous_term_id = Array()
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
    #// When status is inserted, the placeholder term ID is stored in `$previous_term_id`.
    #// When status is error, the error is stored in `$update_error`.
    #// 
    #// @since 4.3.0
    #// @var string updated|inserted|deleted|error
    #// 
    #// @see WP_Customize_Nav_Menu_Setting::update()
    #// @see WP_Customize_Nav_Menu_Setting::amend_customize_save_response()
    #//
    update_status = Array()
    #// 
    #// Any error object returned by wp_update_nav_menu_object() when setting is updated.
    #// 
    #// @since 4.3.0
    #// @var WP_Error
    #// 
    #// @see WP_Customize_Nav_Menu_Setting::update()
    #// @see WP_Customize_Nav_Menu_Setting::amend_customize_save_response()
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
        self.term_id = php_intval(matches_["id"])
        super().__init__(manager_, id_, args_)
    # end def __init__
    #// 
    #// Get the instance data for a given widget setting.
    #// 
    #// @since 4.3.0
    #// 
    #// @see wp_get_nav_menu_object()
    #// 
    #// @return array Instance data.
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
        else:
            value_ = False
            #// Note that a term_id of less than one indicates a nav_menu not yet inserted.
            if self.term_id > 0:
                term_ = wp_get_nav_menu_object(self.term_id)
                if term_:
                    value_ = wp_array_slice_assoc(term_, php_array_keys(self.default))
                    nav_menu_options_ = get_option("nav_menu_options", Array())
                    value_["auto_add"] = False
                    if (php_isset(lambda : nav_menu_options_["auto_add"])) and php_is_array(nav_menu_options_["auto_add"]):
                        value_["auto_add"] = php_in_array(term_.term_id, nav_menu_options_["auto_add"])
                    # end if
                # end if
            # end if
            if (not php_is_array(value_)):
                value_ = self.default
            # end if
        # end if
        return value_
    # end def value
    #// 
    #// Handle previewing the setting.
    #// 
    #// @since 4.3.0
    #// @since 4.4.0 Added boolean return value
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
        is_placeholder_ = self.term_id < 0
        is_dirty_ = undefined_ != self.post_value(undefined_)
        if (not is_placeholder_) and (not is_dirty_):
            return False
        # end if
        self.is_previewed = True
        self._original_value = self.value()
        self._previewed_blog_id = get_current_blog_id()
        add_filter("wp_get_nav_menus", Array(self, "filter_wp_get_nav_menus"), 10, 2)
        add_filter("wp_get_nav_menu_object", Array(self, "filter_wp_get_nav_menu_object"), 10, 2)
        add_filter("default_option_nav_menu_options", Array(self, "filter_nav_menu_options"))
        add_filter("option_nav_menu_options", Array(self, "filter_nav_menu_options"))
        return True
    # end def preview
    #// 
    #// Filters the wp_get_nav_menus() result to ensure the inserted menu object is included, and the deleted one is removed.
    #// 
    #// @since 4.3.0
    #// 
    #// @see wp_get_nav_menus()
    #// 
    #// @param WP_Term[] $menus An array of menu objects.
    #// @param array     $args  An array of arguments used to retrieve menu objects.
    #// @return WP_Term[] Array of menu objects.
    #//
    def filter_wp_get_nav_menus(self, menus_=None, args_=None):
        
        
        if get_current_blog_id() != self._previewed_blog_id:
            return menus_
        # end if
        setting_value_ = self.value()
        is_delete_ = False == setting_value_
        index_ = -1
        #// Find the existing menu item's position in the list.
        for i_,menu_ in menus_:
            if php_int(self.term_id) == php_int(menu_.term_id) or php_int(self.previous_term_id) == php_int(menu_.term_id):
                index_ = i_
                break
            # end if
        # end for
        if is_delete_:
            #// Handle deleted menu by removing it from the list.
            if -1 != index_:
                array_splice(menus_, index_, 1)
            # end if
        else:
            #// Handle menus being updated or inserted.
            menu_obj_ = php_array_merge(Array({"term_id": self.term_id, "term_taxonomy_id": self.term_id, "slug": sanitize_title(setting_value_["name"]), "count": 0, "term_group": 0, "taxonomy": self.TAXONOMY, "filter": "raw"}), setting_value_)
            array_splice(menus_, index_, 0 if -1 == index_ else 1, Array(menu_obj_))
        # end if
        #// Make sure the menu objects get re-sorted after an update/insert.
        if (not is_delete_) and (not php_empty(lambda : args_["orderby"])):
            menus_ = wp_list_sort(menus_, Array({args_["orderby"]: "ASC"}))
        # end if
        #// @todo Add support for $args['hide_empty'] === true.
        return menus_
    # end def filter_wp_get_nav_menus
    #// 
    #// Temporary non-closure passing of orderby value to function.
    #// 
    #// @since 4.3.0
    #// @var string
    #// 
    #// @see WP_Customize_Nav_Menu_Setting::filter_wp_get_nav_menus()
    #// @see WP_Customize_Nav_Menu_Setting::_sort_menus_by_orderby()
    #//
    _current_menus_sort_orderby = Array()
    #// 
    #// Sort menu objects by the class-supplied orderby property.
    #// 
    #// This is a workaround for a lack of closures.
    #// 
    #// @since 4.3.0
    #// @deprecated 4.7.0 Use wp_list_sort()
    #// 
    #// @param object $menu1
    #// @param object $menu2
    #// @return int
    #// 
    #// @see WP_Customize_Nav_Menu_Setting::filter_wp_get_nav_menus()
    #//
    def _sort_menus_by_orderby(self, menu1_=None, menu2_=None):
        
        
        _deprecated_function(__METHOD__, "4.7.0", "wp_list_sort")
        key_ = self._current_menus_sort_orderby
        return strcmp(menu1_.key_, menu2_.key_)
    # end def _sort_menus_by_orderby
    #// 
    #// Filters the wp_get_nav_menu_object() result to supply the previewed menu object.
    #// 
    #// Requesting a nav_menu object by anything but ID is not supported.
    #// 
    #// @since 4.3.0
    #// 
    #// @see wp_get_nav_menu_object()
    #// 
    #// @param object|null $menu_obj Object returned by wp_get_nav_menu_object().
    #// @param string      $menu_id  ID of the nav_menu term. Requests by slug or name will be ignored.
    #// @return object|null
    #//
    def filter_wp_get_nav_menu_object(self, menu_obj_=None, menu_id_=None):
        
        
        ok_ = get_current_blog_id() == self._previewed_blog_id and php_is_int(menu_id_) and menu_id_ == self.term_id
        if (not ok_):
            return menu_obj_
        # end if
        setting_value_ = self.value()
        #// Handle deleted menus.
        if False == setting_value_:
            return False
        # end if
        #// Handle sanitization failure by preventing short-circuiting.
        if None == setting_value_:
            return menu_obj_
        # end if
        menu_obj_ = php_array_merge(Array({"term_id": self.term_id, "term_taxonomy_id": self.term_id, "slug": sanitize_title(setting_value_["name"]), "count": 0, "term_group": 0, "taxonomy": self.TAXONOMY, "filter": "raw"}), setting_value_)
        return menu_obj_
    # end def filter_wp_get_nav_menu_object
    #// 
    #// Filters the nav_menu_options option to include this menu's auto_add preference.
    #// 
    #// @since 4.3.0
    #// 
    #// @param array $nav_menu_options Nav menu options including auto_add.
    #// @return array (Maybe) modified nav menu options.
    #//
    def filter_nav_menu_options(self, nav_menu_options_=None):
        
        
        if get_current_blog_id() != self._previewed_blog_id:
            return nav_menu_options_
        # end if
        menu_ = self.value()
        nav_menu_options_ = self.filter_nav_menu_options_value(nav_menu_options_, self.term_id, False if False == menu_ else menu_["auto_add"])
        return nav_menu_options_
    # end def filter_nav_menu_options
    #// 
    #// Sanitize an input.
    #// 
    #// Note that parent::sanitize() erroneously does wp_unslash() on $value, but
    #// we remove that in this override.
    #// 
    #// @since 4.3.0
    #// 
    #// @param array $value The value to sanitize.
    #// @return array|false|null Null if an input isn't valid. False if it is marked for deletion.
    #// Otherwise the sanitized value.
    #//
    def sanitize(self, value_=None):
        
        
        #// Menu is marked for deletion.
        if False == value_:
            return value_
        # end if
        #// Invalid.
        if (not php_is_array(value_)):
            return None
        # end if
        default_ = Array({"name": "", "description": "", "parent": 0, "auto_add": False})
        value_ = php_array_merge(default_, value_)
        value_ = wp_array_slice_assoc(value_, php_array_keys(default_))
        value_["name"] = php_trim(esc_html(value_["name"]))
        #// This sanitization code is used in wp-admin/nav-menus.php.
        value_["description"] = sanitize_text_field(value_["description"])
        value_["parent"] = php_max(0, php_intval(value_["parent"]))
        value_["auto_add"] = (not php_empty(lambda : value_["auto_add"]))
        if "" == value_["name"]:
            value_["name"] = _x("(unnamed)", "Missing menu name.")
        # end if
        #// This filter is documented in wp-includes/class-wp-customize-setting.php
        return apply_filters(str("customize_sanitize_") + str(self.id), value_, self)
    # end def sanitize
    #// 
    #// Storage for data to be sent back to client in customize_save_response filter.
    #// 
    #// See {@see 'customize_save_response'}.
    #// 
    #// @since 4.3.0
    #// @var array
    #// 
    #// @see WP_Customize_Nav_Menu_Setting::amend_customize_save_response()
    #//
    _widget_nav_menu_updates = Array()
    #// 
    #// Create/update the nav_menu term for this setting.
    #// 
    #// Any created menus will have their assigned term IDs exported to the client
    #// via the {@see 'customize_save_response'} filter. Likewise, any errors will be exported
    #// to the client via the customize_save_response() filter.
    #// 
    #// To delete a menu, the client can send false as the value.
    #// 
    #// @since 4.3.0
    #// 
    #// @see wp_update_nav_menu_object()
    #// 
    #// @param array|false $value {
    #// The value to update. Note that slug cannot be updated via wp_update_nav_menu_object().
    #// If false, then the menu will be deleted entirely.
    #// 
    #// @type string $name        The name of the menu to save.
    #// @type string $description The term description. Default empty string.
    #// @type int    $parent      The id of the parent term. Default 0.
    #// @type bool   $auto_add    Whether pages will auto_add to this menu. Default false.
    #// }
    #// @return null|void
    #//
    def update(self, value_=None):
        
        
        if self.is_updated:
            return
        # end if
        self.is_updated = True
        is_placeholder_ = self.term_id < 0
        is_delete_ = False == value_
        add_filter("customize_save_response", Array(self, "amend_customize_save_response"))
        auto_add_ = None
        if is_delete_:
            #// If the current setting term is a placeholder, a delete request is a no-op.
            if is_placeholder_:
                self.update_status = "deleted"
            else:
                r_ = wp_delete_nav_menu(self.term_id)
                if is_wp_error(r_):
                    self.update_status = "error"
                    self.update_error = r_
                else:
                    self.update_status = "deleted"
                    auto_add_ = False
                # end if
            # end if
        else:
            #// Insert or update menu.
            menu_data_ = wp_array_slice_assoc(value_, Array("description", "parent"))
            menu_data_["menu-name"] = value_["name"]
            menu_id_ = 0 if is_placeholder_ else self.term_id
            r_ = wp_update_nav_menu_object(menu_id_, wp_slash(menu_data_))
            original_name_ = menu_data_["menu-name"]
            name_conflict_suffix_ = 1
            while True:
                
                if not (is_wp_error(r_) and "menu_exists" == r_.get_error_code()):
                    break
                # end if
                name_conflict_suffix_ += 1
                #// translators: 1: Original menu name, 2: Duplicate count.
                menu_data_["menu-name"] = php_sprintf(__("%1$s (%2$d)"), original_name_, name_conflict_suffix_)
                r_ = wp_update_nav_menu_object(menu_id_, wp_slash(menu_data_))
            # end while
            if is_wp_error(r_):
                self.update_status = "error"
                self.update_error = r_
            else:
                if is_placeholder_:
                    self.previous_term_id = self.term_id
                    self.term_id = r_
                    self.update_status = "inserted"
                else:
                    self.update_status = "updated"
                # end if
                auto_add_ = value_["auto_add"]
            # end if
        # end if
        if None != auto_add_:
            nav_menu_options_ = self.filter_nav_menu_options_value(get_option("nav_menu_options", Array()), self.term_id, auto_add_)
            update_option("nav_menu_options", nav_menu_options_)
        # end if
        if "inserted" == self.update_status:
            #// Make sure that new menus assigned to nav menu locations use their new IDs.
            for setting_ in self.manager.settings():
                if (not php_preg_match("/^nav_menu_locations\\[/", setting_.id)):
                    continue
                # end if
                post_value_ = setting_.post_value(None)
                if (not php_is_null(post_value_)) and php_intval(post_value_) == self.previous_term_id:
                    self.manager.set_post_value(setting_.id, self.term_id)
                    setting_.save()
                # end if
            # end for
            #// Make sure that any nav_menu widgets referencing the placeholder nav menu get updated and sent back to client.
            for setting_id_ in php_array_keys(self.manager.unsanitized_post_values()):
                nav_menu_widget_setting_ = self.manager.get_setting(setting_id_)
                if (not nav_menu_widget_setting_) or (not php_preg_match("/^widget_nav_menu\\[/", nav_menu_widget_setting_.id)):
                    continue
                # end if
                widget_instance_ = nav_menu_widget_setting_.post_value()
                #// Note that this calls WP_Customize_Widgets::sanitize_widget_instance().
                if php_empty(lambda : widget_instance_["nav_menu"]) or php_intval(widget_instance_["nav_menu"]) != self.previous_term_id:
                    continue
                # end if
                widget_instance_["nav_menu"] = self.term_id
                updated_widget_instance_ = self.manager.widgets.sanitize_widget_js_instance(widget_instance_)
                self.manager.set_post_value(nav_menu_widget_setting_.id, updated_widget_instance_)
                nav_menu_widget_setting_.save()
                self._widget_nav_menu_updates[nav_menu_widget_setting_.id] = updated_widget_instance_
            # end for
        # end if
    # end def update
    #// 
    #// Updates a nav_menu_options array.
    #// 
    #// @since 4.3.0
    #// 
    #// @see WP_Customize_Nav_Menu_Setting::filter_nav_menu_options()
    #// @see WP_Customize_Nav_Menu_Setting::update()
    #// 
    #// @param array $nav_menu_options Array as returned by get_option( 'nav_menu_options' ).
    #// @param int   $menu_id          The term ID for the given menu.
    #// @param bool  $auto_add         Whether to auto-add or not.
    #// @return array (Maybe) modified nav_menu_otions array.
    #//
    def filter_nav_menu_options_value(self, nav_menu_options_=None, menu_id_=None, auto_add_=None):
        
        
        nav_menu_options_ = nav_menu_options_
        if (not (php_isset(lambda : nav_menu_options_["auto_add"]))):
            nav_menu_options_["auto_add"] = Array()
        # end if
        i_ = php_array_search(menu_id_, nav_menu_options_["auto_add"])
        if auto_add_ and False == i_:
            php_array_push(nav_menu_options_["auto_add"], self.term_id)
        elif (not auto_add_) and False != i_:
            array_splice(nav_menu_options_["auto_add"], i_, 1)
        # end if
        return nav_menu_options_
    # end def filter_nav_menu_options_value
    #// 
    #// Export data for the JS client.
    #// 
    #// @since 4.3.0
    #// 
    #// @see WP_Customize_Nav_Menu_Setting::update()
    #// 
    #// @param array $data Additional information passed back to the 'saved' event on `wp.customize`.
    #// @return array Export data.
    #//
    def amend_customize_save_response(self, data_=None):
        
        
        if (not (php_isset(lambda : data_["nav_menu_updates"]))):
            data_["nav_menu_updates"] = Array()
        # end if
        if (not (php_isset(lambda : data_["widget_nav_menu_updates"]))):
            data_["widget_nav_menu_updates"] = Array()
        # end if
        data_["nav_menu_updates"][-1] = Array({"term_id": self.term_id, "previous_term_id": self.previous_term_id, "error": self.update_error.get_error_code() if self.update_error else None, "status": self.update_status, "saved_value": None if "deleted" == self.update_status else self.value()})
        data_["widget_nav_menu_updates"] = php_array_merge(data_["widget_nav_menu_updates"], self._widget_nav_menu_updates)
        self._widget_nav_menu_updates = Array()
        return data_
    # end def amend_customize_save_response
# end class WP_Customize_Nav_Menu_Setting
