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
    type = self.TYPE
    default = Array({"name": "", "description": "", "parent": 0, "auto_add": False})
    transport = "postMessage"
    term_id = Array()
    previous_term_id = Array()
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
        self.term_id = php_intval(matches["id"])
        super().__init__(manager, id, args)
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
            undefined = php_new_class("stdClass", lambda : stdClass())
            #// Symbol.
            post_value = self.post_value(undefined)
            if undefined == post_value:
                value = self._original_value
            else:
                value = post_value
            # end if
        else:
            value = False
            #// Note that a term_id of less than one indicates a nav_menu not yet inserted.
            if self.term_id > 0:
                term = wp_get_nav_menu_object(self.term_id)
                if term:
                    value = wp_array_slice_assoc(term, php_array_keys(self.default))
                    nav_menu_options = get_option("nav_menu_options", Array())
                    value["auto_add"] = False
                    if (php_isset(lambda : nav_menu_options["auto_add"])) and php_is_array(nav_menu_options["auto_add"]):
                        value["auto_add"] = php_in_array(term.term_id, nav_menu_options["auto_add"])
                    # end if
                # end if
            # end if
            if (not php_is_array(value)):
                value = self.default
            # end if
        # end if
        return value
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
        undefined = php_new_class("stdClass", lambda : stdClass())
        is_placeholder = self.term_id < 0
        is_dirty = undefined != self.post_value(undefined)
        if (not is_placeholder) and (not is_dirty):
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
    def filter_wp_get_nav_menus(self, menus=None, args=None):
        
        if get_current_blog_id() != self._previewed_blog_id:
            return menus
        # end if
        setting_value = self.value()
        is_delete = False == setting_value
        index = -1
        #// Find the existing menu item's position in the list.
        for i,menu in menus:
            if php_int(self.term_id) == php_int(menu.term_id) or php_int(self.previous_term_id) == php_int(menu.term_id):
                index = i
                break
            # end if
        # end for
        if is_delete:
            #// Handle deleted menu by removing it from the list.
            if -1 != index:
                array_splice(menus, index, 1)
            # end if
        else:
            #// Handle menus being updated or inserted.
            menu_obj = php_array_merge(Array({"term_id": self.term_id, "term_taxonomy_id": self.term_id, "slug": sanitize_title(setting_value["name"]), "count": 0, "term_group": 0, "taxonomy": self.TAXONOMY, "filter": "raw"}), setting_value)
            array_splice(menus, index, 0 if -1 == index else 1, Array(menu_obj))
        # end if
        #// Make sure the menu objects get re-sorted after an update/insert.
        if (not is_delete) and (not php_empty(lambda : args["orderby"])):
            menus = wp_list_sort(menus, Array({args["orderby"]: "ASC"}))
        # end if
        #// @todo Add support for $args['hide_empty'] === true.
        return menus
    # end def filter_wp_get_nav_menus
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
    def _sort_menus_by_orderby(self, menu1=None, menu2=None):
        
        _deprecated_function(__METHOD__, "4.7.0", "wp_list_sort")
        key = self._current_menus_sort_orderby
        return strcmp(menu1.key, menu2.key)
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
    def filter_wp_get_nav_menu_object(self, menu_obj=None, menu_id=None):
        
        ok = get_current_blog_id() == self._previewed_blog_id and php_is_int(menu_id) and menu_id == self.term_id
        if (not ok):
            return menu_obj
        # end if
        setting_value = self.value()
        #// Handle deleted menus.
        if False == setting_value:
            return False
        # end if
        #// Handle sanitization failure by preventing short-circuiting.
        if None == setting_value:
            return menu_obj
        # end if
        menu_obj = php_array_merge(Array({"term_id": self.term_id, "term_taxonomy_id": self.term_id, "slug": sanitize_title(setting_value["name"]), "count": 0, "term_group": 0, "taxonomy": self.TAXONOMY, "filter": "raw"}), setting_value)
        return menu_obj
    # end def filter_wp_get_nav_menu_object
    #// 
    #// Filters the nav_menu_options option to include this menu's auto_add preference.
    #// 
    #// @since 4.3.0
    #// 
    #// @param array $nav_menu_options Nav menu options including auto_add.
    #// @return array (Maybe) modified nav menu options.
    #//
    def filter_nav_menu_options(self, nav_menu_options=None):
        
        if get_current_blog_id() != self._previewed_blog_id:
            return nav_menu_options
        # end if
        menu = self.value()
        nav_menu_options = self.filter_nav_menu_options_value(nav_menu_options, self.term_id, False if False == menu else menu["auto_add"])
        return nav_menu_options
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
    def sanitize(self, value=None):
        
        #// Menu is marked for deletion.
        if False == value:
            return value
        # end if
        #// Invalid.
        if (not php_is_array(value)):
            return None
        # end if
        default = Array({"name": "", "description": "", "parent": 0, "auto_add": False})
        value = php_array_merge(default, value)
        value = wp_array_slice_assoc(value, php_array_keys(default))
        value["name"] = php_trim(esc_html(value["name"]))
        #// This sanitization code is used in wp-admin/nav-menus.php.
        value["description"] = sanitize_text_field(value["description"])
        value["parent"] = php_max(0, php_intval(value["parent"]))
        value["auto_add"] = (not php_empty(lambda : value["auto_add"]))
        if "" == value["name"]:
            value["name"] = _x("(unnamed)", "Missing menu name.")
        # end if
        #// This filter is documented in wp-includes/class-wp-customize-setting.php
        return apply_filters(str("customize_sanitize_") + str(self.id), value, self)
    # end def sanitize
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
    def update(self, value=None):
        
        if self.is_updated:
            return
        # end if
        self.is_updated = True
        is_placeholder = self.term_id < 0
        is_delete = False == value
        add_filter("customize_save_response", Array(self, "amend_customize_save_response"))
        auto_add = None
        if is_delete:
            #// If the current setting term is a placeholder, a delete request is a no-op.
            if is_placeholder:
                self.update_status = "deleted"
            else:
                r = wp_delete_nav_menu(self.term_id)
                if is_wp_error(r):
                    self.update_status = "error"
                    self.update_error = r
                else:
                    self.update_status = "deleted"
                    auto_add = False
                # end if
            # end if
        else:
            #// Insert or update menu.
            menu_data = wp_array_slice_assoc(value, Array("description", "parent"))
            menu_data["menu-name"] = value["name"]
            menu_id = 0 if is_placeholder else self.term_id
            r = wp_update_nav_menu_object(menu_id, wp_slash(menu_data))
            original_name = menu_data["menu-name"]
            name_conflict_suffix = 1
            while True:
                
                if not (is_wp_error(r) and "menu_exists" == r.get_error_code()):
                    break
                # end if
                name_conflict_suffix += 1
                #// translators: 1: Original menu name, 2: Duplicate count.
                menu_data["menu-name"] = php_sprintf(__("%1$s (%2$d)"), original_name, name_conflict_suffix)
                r = wp_update_nav_menu_object(menu_id, wp_slash(menu_data))
            # end while
            if is_wp_error(r):
                self.update_status = "error"
                self.update_error = r
            else:
                if is_placeholder:
                    self.previous_term_id = self.term_id
                    self.term_id = r
                    self.update_status = "inserted"
                else:
                    self.update_status = "updated"
                # end if
                auto_add = value["auto_add"]
            # end if
        # end if
        if None != auto_add:
            nav_menu_options = self.filter_nav_menu_options_value(get_option("nav_menu_options", Array()), self.term_id, auto_add)
            update_option("nav_menu_options", nav_menu_options)
        # end if
        if "inserted" == self.update_status:
            #// Make sure that new menus assigned to nav menu locations use their new IDs.
            for setting in self.manager.settings():
                if (not php_preg_match("/^nav_menu_locations\\[/", setting.id)):
                    continue
                # end if
                post_value = setting.post_value(None)
                if (not is_null(post_value)) and php_intval(post_value) == self.previous_term_id:
                    self.manager.set_post_value(setting.id, self.term_id)
                    setting.save()
                # end if
            # end for
            #// Make sure that any nav_menu widgets referencing the placeholder nav menu get updated and sent back to client.
            for setting_id in php_array_keys(self.manager.unsanitized_post_values()):
                nav_menu_widget_setting = self.manager.get_setting(setting_id)
                if (not nav_menu_widget_setting) or (not php_preg_match("/^widget_nav_menu\\[/", nav_menu_widget_setting.id)):
                    continue
                # end if
                widget_instance = nav_menu_widget_setting.post_value()
                #// Note that this calls WP_Customize_Widgets::sanitize_widget_instance().
                if php_empty(lambda : widget_instance["nav_menu"]) or php_intval(widget_instance["nav_menu"]) != self.previous_term_id:
                    continue
                # end if
                widget_instance["nav_menu"] = self.term_id
                updated_widget_instance = self.manager.widgets.sanitize_widget_js_instance(widget_instance)
                self.manager.set_post_value(nav_menu_widget_setting.id, updated_widget_instance)
                nav_menu_widget_setting.save()
                self._widget_nav_menu_updates[nav_menu_widget_setting.id] = updated_widget_instance
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
    def filter_nav_menu_options_value(self, nav_menu_options=None, menu_id=None, auto_add=None):
        
        nav_menu_options = nav_menu_options
        if (not (php_isset(lambda : nav_menu_options["auto_add"]))):
            nav_menu_options["auto_add"] = Array()
        # end if
        i = php_array_search(menu_id, nav_menu_options["auto_add"])
        if auto_add and False == i:
            php_array_push(nav_menu_options["auto_add"], self.term_id)
        elif (not auto_add) and False != i:
            array_splice(nav_menu_options["auto_add"], i, 1)
        # end if
        return nav_menu_options
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
    def amend_customize_save_response(self, data=None):
        
        if (not (php_isset(lambda : data["nav_menu_updates"]))):
            data["nav_menu_updates"] = Array()
        # end if
        if (not (php_isset(lambda : data["widget_nav_menu_updates"]))):
            data["widget_nav_menu_updates"] = Array()
        # end if
        data["nav_menu_updates"][-1] = Array({"term_id": self.term_id, "previous_term_id": self.previous_term_id, "error": self.update_error.get_error_code() if self.update_error else None, "status": self.update_status, "saved_value": None if "deleted" == self.update_status else self.value()})
        data["widget_nav_menu_updates"] = php_array_merge(data["widget_nav_menu_updates"], self._widget_nav_menu_updates)
        self._widget_nav_menu_updates = Array()
        return data
    # end def amend_customize_save_response
# end class WP_Customize_Nav_Menu_Setting
