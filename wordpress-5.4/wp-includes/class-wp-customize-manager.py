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
#// WordPress Customize Manager classes
#// 
#// @package WordPress
#// @subpackage Customize
#// @since 3.4.0
#// 
#// 
#// Customize Manager class.
#// 
#// Bootstraps the Customize experience on the server-side.
#// 
#// Sets up the theme-switching process if a theme other than the active one is
#// being previewed and customized.
#// 
#// Serves as a factory for Customize Controls and Settings, and
#// instantiates default Customize Controls and Settings.
#// 
#// @since 3.4.0
#//
class WP_Customize_Manager():
    theme = Array()
    original_stylesheet = Array()
    previewing = False
    widgets = Array()
    nav_menus = Array()
    selective_refresh = Array()
    settings = Array()
    containers = Array()
    panels = Array()
    components = Array("widgets", "nav_menus")
    sections = Array()
    controls = Array()
    registered_panel_types = Array()
    registered_section_types = Array()
    registered_control_types = Array()
    preview_url = Array()
    return_url = Array()
    autofocus = Array()
    messenger_channel = Array()
    autosaved = False
    branching = True
    settings_previewed = True
    saved_starter_content_changeset = False
    _post_values = Array()
    _changeset_uuid = Array()
    _changeset_post_id = Array()
    _changeset_data = Array()
    #// 
    #// Constructor.
    #// 
    #// @since 3.4.0
    #// @since 4.7.0 Added `$args` parameter.
    #// 
    #// @param array $args {
    #// Args.
    #// 
    #// @type null|string|false $changeset_uuid     Changeset UUID, the `post_name` for the customize_changeset post containing the customized state.
    #// Defaults to `null` resulting in a UUID to be immediately generated. If `false` is provided, then
    #// then the changeset UUID will be determined during `after_setup_theme`: when the
    #// `customize_changeset_branching` filter returns false, then the default UUID will be that
    #// of the most recent `customize_changeset` post that has a status other than 'auto-draft',
    #// 'publish', or 'trash'. Otherwise, if changeset branching is enabled, then a random UUID will be used.
    #// @type string            $theme              Theme to be previewed (for theme switch). Defaults to customize_theme or theme query params.
    #// @type string            $messenger_channel  Messenger channel. Defaults to customize_messenger_channel query param.
    #// @type bool              $settings_previewed If settings should be previewed. Defaults to true.
    #// @type bool              $branching          If changeset branching is allowed; otherwise, changesets are linear. Defaults to true.
    #// @type bool              $autosaved          If data from a changeset's autosaved revision should be loaded if it exists. Defaults to false.
    #// }
    #//
    def __init__(self, args=Array()):
        
        args = php_array_merge(php_array_fill_keys(Array("changeset_uuid", "theme", "messenger_channel", "settings_previewed", "autosaved", "branching"), None), args)
        #// Note that the UUID format will be validated in the setup_theme() method.
        if (not (php_isset(lambda : args["changeset_uuid"]))):
            args["changeset_uuid"] = wp_generate_uuid4()
        # end if
        #// The theme and messenger_channel should be supplied via $args,
        #// but they are also looked at in the $_REQUEST global here for back-compat.
        if (not (php_isset(lambda : args["theme"]))):
            if (php_isset(lambda : PHP_REQUEST["customize_theme"])):
                args["theme"] = wp_unslash(PHP_REQUEST["customize_theme"])
            elif (php_isset(lambda : PHP_REQUEST["theme"])):
                #// Deprecated.
                args["theme"] = wp_unslash(PHP_REQUEST["theme"])
            # end if
        # end if
        if (not (php_isset(lambda : args["messenger_channel"]))) and (php_isset(lambda : PHP_REQUEST["customize_messenger_channel"])):
            args["messenger_channel"] = sanitize_key(wp_unslash(PHP_REQUEST["customize_messenger_channel"]))
        # end if
        self.original_stylesheet = get_stylesheet()
        self.theme = wp_get_theme(args["theme"] if 0 == validate_file(args["theme"]) else None)
        self.messenger_channel = args["messenger_channel"]
        self._changeset_uuid = args["changeset_uuid"]
        for key in Array("settings_previewed", "autosaved", "branching"):
            if (php_isset(lambda : args[key])):
                self.key = php_bool(args[key])
            # end if
        # end for
        php_include_file(ABSPATH + WPINC + "/class-wp-customize-setting.php", once=True)
        php_include_file(ABSPATH + WPINC + "/class-wp-customize-panel.php", once=True)
        php_include_file(ABSPATH + WPINC + "/class-wp-customize-section.php", once=True)
        php_include_file(ABSPATH + WPINC + "/class-wp-customize-control.php", once=True)
        php_include_file(ABSPATH + WPINC + "/customize/class-wp-customize-color-control.php", once=True)
        php_include_file(ABSPATH + WPINC + "/customize/class-wp-customize-media-control.php", once=True)
        php_include_file(ABSPATH + WPINC + "/customize/class-wp-customize-upload-control.php", once=True)
        php_include_file(ABSPATH + WPINC + "/customize/class-wp-customize-image-control.php", once=True)
        php_include_file(ABSPATH + WPINC + "/customize/class-wp-customize-background-image-control.php", once=True)
        php_include_file(ABSPATH + WPINC + "/customize/class-wp-customize-background-position-control.php", once=True)
        php_include_file(ABSPATH + WPINC + "/customize/class-wp-customize-cropped-image-control.php", once=True)
        php_include_file(ABSPATH + WPINC + "/customize/class-wp-customize-site-icon-control.php", once=True)
        php_include_file(ABSPATH + WPINC + "/customize/class-wp-customize-header-image-control.php", once=True)
        php_include_file(ABSPATH + WPINC + "/customize/class-wp-customize-theme-control.php", once=True)
        php_include_file(ABSPATH + WPINC + "/customize/class-wp-customize-code-editor-control.php", once=True)
        php_include_file(ABSPATH + WPINC + "/customize/class-wp-widget-area-customize-control.php", once=True)
        php_include_file(ABSPATH + WPINC + "/customize/class-wp-widget-form-customize-control.php", once=True)
        php_include_file(ABSPATH + WPINC + "/customize/class-wp-customize-nav-menu-control.php", once=True)
        php_include_file(ABSPATH + WPINC + "/customize/class-wp-customize-nav-menu-item-control.php", once=True)
        php_include_file(ABSPATH + WPINC + "/customize/class-wp-customize-nav-menu-location-control.php", once=True)
        php_include_file(ABSPATH + WPINC + "/customize/class-wp-customize-nav-menu-name-control.php", once=True)
        php_include_file(ABSPATH + WPINC + "/customize/class-wp-customize-nav-menu-locations-control.php", once=True)
        php_include_file(ABSPATH + WPINC + "/customize/class-wp-customize-nav-menu-auto-add-control.php", once=True)
        php_include_file(ABSPATH + WPINC + "/customize/class-wp-customize-nav-menus-panel.php", once=True)
        php_include_file(ABSPATH + WPINC + "/customize/class-wp-customize-themes-panel.php", once=True)
        php_include_file(ABSPATH + WPINC + "/customize/class-wp-customize-themes-section.php", once=True)
        php_include_file(ABSPATH + WPINC + "/customize/class-wp-customize-sidebar-section.php", once=True)
        php_include_file(ABSPATH + WPINC + "/customize/class-wp-customize-nav-menu-section.php", once=True)
        php_include_file(ABSPATH + WPINC + "/customize/class-wp-customize-custom-css-setting.php", once=True)
        php_include_file(ABSPATH + WPINC + "/customize/class-wp-customize-filter-setting.php", once=True)
        php_include_file(ABSPATH + WPINC + "/customize/class-wp-customize-header-image-setting.php", once=True)
        php_include_file(ABSPATH + WPINC + "/customize/class-wp-customize-background-image-setting.php", once=True)
        php_include_file(ABSPATH + WPINC + "/customize/class-wp-customize-nav-menu-item-setting.php", once=True)
        php_include_file(ABSPATH + WPINC + "/customize/class-wp-customize-nav-menu-setting.php", once=True)
        #// 
        #// Filters the core Customizer components to load.
        #// 
        #// This allows Core components to be excluded from being instantiated by
        #// filtering them out of the array. Note that this filter generally runs
        #// during the {@see 'plugins_loaded'} action, so it cannot be added
        #// in a theme.
        #// 
        #// @since 4.4.0
        #// 
        #// @see WP_Customize_Manager::__construct()
        #// 
        #// @param string[]             $components Array of core components to load.
        #// @param WP_Customize_Manager $this       WP_Customize_Manager instance.
        #//
        components = apply_filters("customize_loaded_components", self.components, self)
        php_include_file(ABSPATH + WPINC + "/customize/class-wp-customize-selective-refresh.php", once=True)
        self.selective_refresh = php_new_class("WP_Customize_Selective_Refresh", lambda : WP_Customize_Selective_Refresh(self))
        if php_in_array("widgets", components, True):
            php_include_file(ABSPATH + WPINC + "/class-wp-customize-widgets.php", once=True)
            self.widgets = php_new_class("WP_Customize_Widgets", lambda : WP_Customize_Widgets(self))
        # end if
        if php_in_array("nav_menus", components, True):
            php_include_file(ABSPATH + WPINC + "/class-wp-customize-nav-menus.php", once=True)
            self.nav_menus = php_new_class("WP_Customize_Nav_Menus", lambda : WP_Customize_Nav_Menus(self))
        # end if
        add_action("setup_theme", Array(self, "setup_theme"))
        add_action("wp_loaded", Array(self, "wp_loaded"))
        #// Do not spawn cron (especially the alternate cron) while running the Customizer.
        remove_action("init", "wp_cron")
        #// Do not run update checks when rendering the controls.
        remove_action("admin_init", "_maybe_update_core")
        remove_action("admin_init", "_maybe_update_plugins")
        remove_action("admin_init", "_maybe_update_themes")
        add_action("wp_ajax_customize_save", Array(self, "save"))
        add_action("wp_ajax_customize_trash", Array(self, "handle_changeset_trash_request"))
        add_action("wp_ajax_customize_refresh_nonces", Array(self, "refresh_nonces"))
        add_action("wp_ajax_customize_load_themes", Array(self, "handle_load_themes_request"))
        add_filter("heartbeat_settings", Array(self, "add_customize_screen_to_heartbeat_settings"))
        add_filter("heartbeat_received", Array(self, "check_changeset_lock_with_heartbeat"), 10, 3)
        add_action("wp_ajax_customize_override_changeset_lock", Array(self, "handle_override_changeset_lock_request"))
        add_action("wp_ajax_customize_dismiss_autosave_or_lock", Array(self, "handle_dismiss_autosave_or_lock_request"))
        add_action("customize_register", Array(self, "register_controls"))
        add_action("customize_register", Array(self, "register_dynamic_settings"), 11)
        #// Allow code to create settings first.
        add_action("customize_controls_init", Array(self, "prepare_controls"))
        add_action("customize_controls_enqueue_scripts", Array(self, "enqueue_control_scripts"))
        #// Render Common, Panel, Section, and Control templates.
        add_action("customize_controls_print_footer_scripts", Array(self, "render_panel_templates"), 1)
        add_action("customize_controls_print_footer_scripts", Array(self, "render_section_templates"), 1)
        add_action("customize_controls_print_footer_scripts", Array(self, "render_control_templates"), 1)
        #// Export header video settings with the partial response.
        add_filter("customize_render_partials_response", Array(self, "export_header_video_settings"), 10, 3)
        #// Export the settings to JS via the _wpCustomizeSettings variable.
        add_action("customize_controls_print_footer_scripts", Array(self, "customize_pane_settings"), 1000)
        #// Add theme update notices.
        if current_user_can("install_themes") or current_user_can("update_themes"):
            php_include_file(ABSPATH + "wp-admin/includes/update.php", once=True)
            add_action("customize_controls_print_footer_scripts", "wp_print_admin_notice_templates")
        # end if
    # end def __init__
    #// 
    #// Return true if it's an Ajax request.
    #// 
    #// @since 3.4.0
    #// @since 4.2.0 Added `$action` param.
    #// 
    #// @param string|null $action Whether the supplied Ajax action is being run.
    #// @return bool True if it's an Ajax request, false otherwise.
    #//
    def doing_ajax(self, action=None):
        
        if (not wp_doing_ajax()):
            return False
        # end if
        if (not action):
            return True
        else:
            #// 
            #// Note: we can't just use doing_action( "wp_ajax_{$action}" ) because we need
            #// to check before admin-ajax.php gets to that point.
            #//
            return (php_isset(lambda : PHP_REQUEST["action"])) and wp_unslash(PHP_REQUEST["action"]) == action
        # end if
    # end def doing_ajax
    #// 
    #// Custom wp_die wrapper. Returns either the standard message for UI
    #// or the Ajax message.
    #// 
    #// @since 3.4.0
    #// 
    #// @param string|WP_Error $ajax_message Ajax return.
    #// @param string          $message      Optional. UI message.
    #//
    def wp_die(self, ajax_message=None, message=None):
        
        if self.doing_ajax():
            wp_die(ajax_message)
        # end if
        if (not message):
            message = __("Something went wrong.")
        # end if
        if self.messenger_channel:
            ob_start()
            wp_enqueue_scripts()
            wp_print_scripts(Array("customize-base"))
            settings = Array({"messengerArgs": Array({"channel": self.messenger_channel, "url": wp_customize_url()})}, {"error": ajax_message})
            php_print("""           <script>
            ( function( api, settings ) {
            var preview = new api.Messenger( settings.messengerArgs );
            preview.send( 'iframe-loading-error', settings.error );
            } )( wp.customize, """)
            php_print(wp_json_encode(settings))
            php_print(" );\n            </script>\n         ")
            message += ob_get_clean()
        # end if
        wp_die(message)
    # end def wp_die
    #// 
    #// Return the Ajax wp_die() handler if it's a customized request.
    #// 
    #// @since 3.4.0
    #// @deprecated 4.7.0
    #// 
    #// @return callable Die handler.
    #//
    def wp_die_handler(self):
        
        _deprecated_function(__METHOD__, "4.7.0")
        if self.doing_ajax() or (php_isset(lambda : PHP_POST["customized"])):
            return "_ajax_wp_die_handler"
        # end if
        return "_default_wp_die_handler"
    # end def wp_die_handler
    #// 
    #// Start preview and customize theme.
    #// 
    #// Check if customize query variable exist. Init filters to filter the current theme.
    #// 
    #// @since 3.4.0
    #// 
    #// @global string $pagenow
    #//
    def setup_theme(self):
        
        global pagenow
        php_check_if_defined("pagenow")
        #// Check permissions for customize.php access since this method is called before customize.php can run any code.
        if "customize.php" == pagenow and (not current_user_can("customize")):
            if (not is_user_logged_in()):
                auth_redirect()
            else:
                wp_die("<h1>" + __("You need a higher level of permission.") + "</h1>" + "<p>" + __("Sorry, you are not allowed to customize this site.") + "</p>", 403)
            # end if
            return
        # end if
        #// If a changeset was provided is invalid.
        if (php_isset(lambda : self._changeset_uuid)) and False != self._changeset_uuid and (not wp_is_uuid(self._changeset_uuid)):
            self.wp_die(-1, __("Invalid changeset UUID"))
        # end if
        #// 
        #// Clear incoming post data if the user lacks a CSRF token (nonce). Note that the customizer
        #// application will inject the customize_preview_nonce query parameter into all Ajax requests.
        #// For similar behavior elsewhere in WordPress, see rest_cookie_check_errors() which logs out
        #// a user when a valid nonce isn't present.
        #//
        has_post_data_nonce = check_ajax_referer("preview-customize_" + self.get_stylesheet(), "nonce", False) or check_ajax_referer("save-customize_" + self.get_stylesheet(), "nonce", False) or check_ajax_referer("preview-customize_" + self.get_stylesheet(), "customize_preview_nonce", False)
        if (not current_user_can("customize")) or (not has_post_data_nonce):
            PHP_POST["customized"] = None
            PHP_REQUEST["customized"] = None
        # end if
        #// 
        #// If unauthenticated then require a valid changeset UUID to load the preview.
        #// In this way, the UUID serves as a secret key. If the messenger channel is present,
        #// then send unauthenticated code to prompt re-auth.
        #//
        if (not current_user_can("customize")) and (not self.changeset_post_id()):
            self.wp_die(0 if self.messenger_channel else -1, __("Non-existent changeset UUID."))
        # end if
        if (not php_headers_sent()):
            send_origin_headers()
        # end if
        #// Hide the admin bar if we're embedded in the customizer iframe.
        if self.messenger_channel:
            show_admin_bar(False)
        # end if
        if self.is_theme_active():
            #// Once the theme is loaded, we'll validate it.
            add_action("after_setup_theme", Array(self, "after_setup_theme"))
        else:
            #// If the requested theme is not the active theme and the user doesn't have
            #// the switch_themes cap, bail.
            if (not current_user_can("switch_themes")):
                self.wp_die(-1, __("Sorry, you are not allowed to edit theme options on this site."))
            # end if
            #// If the theme has errors while loading, bail.
            if self.theme().errors():
                self.wp_die(-1, self.theme().errors().get_error_message())
            # end if
            #// If the theme isn't allowed per multisite settings, bail.
            if (not self.theme().is_allowed()):
                self.wp_die(-1, __("The requested theme does not exist."))
            # end if
        # end if
        #// Make sure changeset UUID is established immediately after the theme is loaded.
        add_action("after_setup_theme", Array(self, "establish_loaded_changeset"), 5)
        #// 
        #// Import theme starter content for fresh installations when landing in the customizer.
        #// Import starter content at after_setup_theme:100 so that any
        #// add_theme_support( 'starter-content' ) calls will have been made.
        #//
        if get_option("fresh_site") and "customize.php" == pagenow:
            add_action("after_setup_theme", Array(self, "import_theme_starter_content"), 100)
        # end if
        self.start_previewing_theme()
    # end def setup_theme
    #// 
    #// Establish the loaded changeset.
    #// 
    #// This method runs right at after_setup_theme and applies the 'customize_changeset_branching' filter to determine
    #// whether concurrent changesets are allowed. Then if the Customizer is not initialized with a `changeset_uuid` param,
    #// this method will determine which UUID should be used. If changeset branching is disabled, then the most saved
    #// changeset will be loaded by default. Otherwise, if there are no existing saved changesets or if changeset branching is
    #// enabled, then a new UUID will be generated.
    #// 
    #// @since 4.9.0
    #// @global string $pagenow
    #//
    def establish_loaded_changeset(self):
        
        global pagenow
        php_check_if_defined("pagenow")
        if php_empty(lambda : self._changeset_uuid):
            changeset_uuid = None
            if (not self.branching()) and self.is_theme_active():
                unpublished_changeset_posts = self.get_changeset_posts(Array({"post_status": php_array_diff(get_post_stati(), Array("auto-draft", "publish", "trash", "inherit", "private")), "exclude_restore_dismissed": False, "author": "any", "posts_per_page": 1, "order": "DESC", "orderby": "date"}))
                unpublished_changeset_post = php_array_shift(unpublished_changeset_posts)
                if (not php_empty(lambda : unpublished_changeset_post)) and wp_is_uuid(unpublished_changeset_post.post_name):
                    changeset_uuid = unpublished_changeset_post.post_name
                # end if
            # end if
            #// If no changeset UUID has been set yet, then generate a new one.
            if php_empty(lambda : changeset_uuid):
                changeset_uuid = wp_generate_uuid4()
            # end if
            self._changeset_uuid = changeset_uuid
        # end if
        if is_admin() and "customize.php" == pagenow:
            self.set_changeset_lock(self.changeset_post_id())
        # end if
    # end def establish_loaded_changeset
    #// 
    #// Callback to validate a theme once it is loaded
    #// 
    #// @since 3.4.0
    #//
    def after_setup_theme(self):
        
        doing_ajax_or_is_customized = self.doing_ajax() or (php_isset(lambda : PHP_POST["customized"]))
        if (not doing_ajax_or_is_customized) and (not validate_current_theme()):
            wp_redirect("themes.php?broken=true")
            php_exit(0)
        # end if
    # end def after_setup_theme
    #// 
    #// If the theme to be previewed isn't the active theme, add filter callbacks
    #// to swap it out at runtime.
    #// 
    #// @since 3.4.0
    #//
    def start_previewing_theme(self):
        
        #// Bail if we're already previewing.
        if self.is_preview():
            return
        # end if
        self.previewing = True
        if (not self.is_theme_active()):
            add_filter("template", Array(self, "get_template"))
            add_filter("stylesheet", Array(self, "get_stylesheet"))
            add_filter("pre_option_current_theme", Array(self, "current_theme"))
            #// @link: https://core.trac.wordpress.org/ticket/20027
            add_filter("pre_option_stylesheet", Array(self, "get_stylesheet"))
            add_filter("pre_option_template", Array(self, "get_template"))
            #// Handle custom theme roots.
            add_filter("pre_option_stylesheet_root", Array(self, "get_stylesheet_root"))
            add_filter("pre_option_template_root", Array(self, "get_template_root"))
        # end if
        #// 
        #// Fires once the Customizer theme preview has started.
        #// 
        #// @since 3.4.0
        #// 
        #// @param WP_Customize_Manager $this WP_Customize_Manager instance.
        #//
        do_action("start_previewing_theme", self)
    # end def start_previewing_theme
    #// 
    #// Stop previewing the selected theme.
    #// 
    #// Removes filters to change the current theme.
    #// 
    #// @since 3.4.0
    #//
    def stop_previewing_theme(self):
        
        if (not self.is_preview()):
            return
        # end if
        self.previewing = False
        if (not self.is_theme_active()):
            remove_filter("template", Array(self, "get_template"))
            remove_filter("stylesheet", Array(self, "get_stylesheet"))
            remove_filter("pre_option_current_theme", Array(self, "current_theme"))
            #// @link: https://core.trac.wordpress.org/ticket/20027
            remove_filter("pre_option_stylesheet", Array(self, "get_stylesheet"))
            remove_filter("pre_option_template", Array(self, "get_template"))
            #// Handle custom theme roots.
            remove_filter("pre_option_stylesheet_root", Array(self, "get_stylesheet_root"))
            remove_filter("pre_option_template_root", Array(self, "get_template_root"))
        # end if
        #// 
        #// Fires once the Customizer theme preview has stopped.
        #// 
        #// @since 3.4.0
        #// 
        #// @param WP_Customize_Manager $this WP_Customize_Manager instance.
        #//
        do_action("stop_previewing_theme", self)
    # end def stop_previewing_theme
    #// 
    #// Gets whether settings are or will be previewed.
    #// 
    #// @since 4.9.0
    #// @see WP_Customize_Setting::preview()
    #// 
    #// @return bool
    #//
    def settings_previewed(self):
        
        return self.settings_previewed
    # end def settings_previewed
    #// 
    #// Gets whether data from a changeset's autosaved revision should be loaded if it exists.
    #// 
    #// @since 4.9.0
    #// @see WP_Customize_Manager::changeset_data()
    #// 
    #// @return bool Is using autosaved changeset revision.
    #//
    def autosaved(self):
        
        return self.autosaved
    # end def autosaved
    #// 
    #// Whether the changeset branching is allowed.
    #// 
    #// @since 4.9.0
    #// @see WP_Customize_Manager::establish_loaded_changeset()
    #// 
    #// @return bool Is changeset branching.
    #//
    def branching(self):
        
        #// 
        #// Filters whether or not changeset branching is allowed.
        #// 
        #// By default in core, when changeset branching is not allowed, changesets will operate
        #// linearly in that only one saved changeset will exist at a time (with a 'draft' or
        #// 'future' status). This makes the Customizer operate in a way that is similar to going to
        #// "edit" to one existing post: all users will be making changes to the same post, and autosave
        #// revisions will be made for that post.
        #// 
        #// By contrast, when changeset branching is allowed, then the model is like users going
        #// to "add new" for a page and each user makes changes independently of each other since
        #// they are all operating on their own separate pages, each getting their own separate
        #// initial auto-drafts and then once initially saved, autosave revisions on top of that
        #// user's specific post.
        #// 
        #// Since linear changesets are deemed to be more suitable for the majority of WordPress users,
        #// they are the default. For WordPress sites that have heavy site management in the Customizer
        #// by multiple users then branching changesets should be enabled by means of this filter.
        #// 
        #// @since 4.9.0
        #// 
        #// @param bool                 $allow_branching Whether branching is allowed. If `false`, the default,
        #// then only one saved changeset exists at a time.
        #// @param WP_Customize_Manager $wp_customize    Manager instance.
        #//
        self.branching = apply_filters("customize_changeset_branching", self.branching, self)
        return self.branching
    # end def branching
    #// 
    #// Get the changeset UUID.
    #// 
    #// @since 4.7.0
    #// @see WP_Customize_Manager::establish_loaded_changeset()
    #// 
    #// @return string UUID.
    #//
    def changeset_uuid(self):
        
        if php_empty(lambda : self._changeset_uuid):
            self.establish_loaded_changeset()
        # end if
        return self._changeset_uuid
    # end def changeset_uuid
    #// 
    #// Get the theme being customized.
    #// 
    #// @since 3.4.0
    #// 
    #// @return WP_Theme
    #//
    def theme(self):
        
        if (not self.theme):
            self.theme = wp_get_theme()
        # end if
        return self.theme
    # end def theme
    #// 
    #// Get the registered settings.
    #// 
    #// @since 3.4.0
    #// 
    #// @return array
    #//
    def settings(self):
        
        return self.settings
    # end def settings
    #// 
    #// Get the registered controls.
    #// 
    #// @since 3.4.0
    #// 
    #// @return array
    #//
    def controls(self):
        
        return self.controls
    # end def controls
    #// 
    #// Get the registered containers.
    #// 
    #// @since 4.0.0
    #// 
    #// @return array
    #//
    def containers(self):
        
        return self.containers
    # end def containers
    #// 
    #// Get the registered sections.
    #// 
    #// @since 3.4.0
    #// 
    #// @return array
    #//
    def sections(self):
        
        return self.sections
    # end def sections
    #// 
    #// Get the registered panels.
    #// 
    #// @since 4.0.0
    #// 
    #// @return array Panels.
    #//
    def panels(self):
        
        return self.panels
    # end def panels
    #// 
    #// Checks if the current theme is active.
    #// 
    #// @since 3.4.0
    #// 
    #// @return bool
    #//
    def is_theme_active(self):
        
        return self.get_stylesheet() == self.original_stylesheet
    # end def is_theme_active
    #// 
    #// Register styles/scripts and initialize the preview of each setting
    #// 
    #// @since 3.4.0
    #//
    def wp_loaded(self):
        
        #// Unconditionally register core types for panels, sections, and controls
        #// in case plugin unhooks all customize_register actions.
        self.register_panel_type("WP_Customize_Panel")
        self.register_panel_type("WP_Customize_Themes_Panel")
        self.register_section_type("WP_Customize_Section")
        self.register_section_type("WP_Customize_Sidebar_Section")
        self.register_section_type("WP_Customize_Themes_Section")
        self.register_control_type("WP_Customize_Color_Control")
        self.register_control_type("WP_Customize_Media_Control")
        self.register_control_type("WP_Customize_Upload_Control")
        self.register_control_type("WP_Customize_Image_Control")
        self.register_control_type("WP_Customize_Background_Image_Control")
        self.register_control_type("WP_Customize_Background_Position_Control")
        self.register_control_type("WP_Customize_Cropped_Image_Control")
        self.register_control_type("WP_Customize_Site_Icon_Control")
        self.register_control_type("WP_Customize_Theme_Control")
        self.register_control_type("WP_Customize_Code_Editor_Control")
        self.register_control_type("WP_Customize_Date_Time_Control")
        #// 
        #// Fires once WordPress has loaded, allowing scripts and styles to be initialized.
        #// 
        #// @since 3.4.0
        #// 
        #// @param WP_Customize_Manager $this WP_Customize_Manager instance.
        #//
        do_action("customize_register", self)
        if self.settings_previewed():
            for setting in self.settings:
                setting.preview()
            # end for
        # end if
        if self.is_preview() and (not is_admin()):
            self.customize_preview_init()
        # end if
    # end def wp_loaded
    #// 
    #// Prevents Ajax requests from following redirects when previewing a theme
    #// by issuing a 200 response instead of a 30x.
    #// 
    #// Instead, the JS will sniff out the location header.
    #// 
    #// @since 3.4.0
    #// @deprecated 4.7.0
    #// 
    #// @param int $status Status.
    #// @return int
    #//
    def wp_redirect_status(self, status=None):
        
        _deprecated_function(__FUNCTION__, "4.7.0")
        if self.is_preview() and (not is_admin()):
            return 200
        # end if
        return status
    # end def wp_redirect_status
    #// 
    #// Find the changeset post ID for a given changeset UUID.
    #// 
    #// @since 4.7.0
    #// 
    #// @param string $uuid Changeset UUID.
    #// @return int|null Returns post ID on success and null on failure.
    #//
    def find_changeset_post_id(self, uuid=None):
        
        cache_group = "customize_changeset_post"
        changeset_post_id = wp_cache_get(uuid, cache_group)
        if changeset_post_id and "customize_changeset" == get_post_type(changeset_post_id):
            return changeset_post_id
        # end if
        changeset_post_query = php_new_class("WP_Query", lambda : WP_Query(Array({"post_type": "customize_changeset", "post_status": get_post_stati(), "name": uuid, "posts_per_page": 1, "no_found_rows": True, "cache_results": True, "update_post_meta_cache": False, "update_post_term_cache": False, "lazy_load_term_meta": False})))
        if (not php_empty(lambda : changeset_post_query.posts)):
            #// Note: 'fields'=>'ids' is not being used in order to cache the post object as it will be needed.
            changeset_post_id = changeset_post_query.posts[0].ID
            wp_cache_set(uuid, changeset_post_id, cache_group)
            return changeset_post_id
        # end if
        return None
    # end def find_changeset_post_id
    #// 
    #// Get changeset posts.
    #// 
    #// @since 4.9.0
    #// 
    #// @param array $args {
    #// Args to pass into `get_posts()` to query changesets.
    #// 
    #// @type int    $posts_per_page             Number of posts to return. Defaults to -1 (all posts).
    #// @type int    $author                     Post author. Defaults to current user.
    #// @type string $post_status                Status of changeset. Defaults to 'auto-draft'.
    #// @type bool   $exclude_restore_dismissed  Whether to exclude changeset auto-drafts that have been dismissed. Defaults to true.
    #// }
    #// @return WP_Post[] Auto-draft changesets.
    #//
    def get_changeset_posts(self, args=Array()):
        
        default_args = Array({"exclude_restore_dismissed": True, "posts_per_page": -1, "post_type": "customize_changeset", "post_status": "auto-draft", "order": "DESC", "orderby": "date", "no_found_rows": True, "cache_results": True, "update_post_meta_cache": False, "update_post_term_cache": False, "lazy_load_term_meta": False})
        if get_current_user_id():
            default_args["author"] = get_current_user_id()
        # end if
        args = php_array_merge(default_args, args)
        if (not php_empty(lambda : args["exclude_restore_dismissed"])):
            args["exclude_restore_dismissed"] = None
            args["meta_query"] = Array(Array({"key": "_customize_restore_dismissed", "compare": "NOT EXISTS"}))
        # end if
        return get_posts(args)
    # end def get_changeset_posts
    #// 
    #// Dismiss all of the current user's auto-drafts (other than the present one).
    #// 
    #// @since 4.9.0
    #// @return int The number of auto-drafts that were dismissed.
    #//
    def dismiss_user_auto_draft_changesets(self):
        
        changeset_autodraft_posts = self.get_changeset_posts(Array({"post_status": "auto-draft", "exclude_restore_dismissed": True, "posts_per_page": -1}))
        dismissed = 0
        for autosave_autodraft_post in changeset_autodraft_posts:
            if autosave_autodraft_post.ID == self.changeset_post_id():
                continue
            # end if
            if update_post_meta(autosave_autodraft_post.ID, "_customize_restore_dismissed", True):
                dismissed += 1
            # end if
        # end for
        return dismissed
    # end def dismiss_user_auto_draft_changesets
    #// 
    #// Get the changeset post id for the loaded changeset.
    #// 
    #// @since 4.7.0
    #// 
    #// @return int|null Post ID on success or null if there is no post yet saved.
    #//
    def changeset_post_id(self):
        
        if (not (php_isset(lambda : self._changeset_post_id))):
            post_id = self.find_changeset_post_id(self.changeset_uuid())
            if (not post_id):
                post_id = False
            # end if
            self._changeset_post_id = post_id
        # end if
        if False == self._changeset_post_id:
            return None
        # end if
        return self._changeset_post_id
    # end def changeset_post_id
    #// 
    #// Get the data stored in a changeset post.
    #// 
    #// @since 4.7.0
    #// 
    #// @param int $post_id Changeset post ID.
    #// @return array|WP_Error Changeset data or WP_Error on error.
    #//
    def get_changeset_post_data(self, post_id=None):
        
        if (not post_id):
            return php_new_class("WP_Error", lambda : WP_Error("empty_post_id"))
        # end if
        changeset_post = get_post(post_id)
        if (not changeset_post):
            return php_new_class("WP_Error", lambda : WP_Error("missing_post"))
        # end if
        if "revision" == changeset_post.post_type:
            if "customize_changeset" != get_post_type(changeset_post.post_parent):
                return php_new_class("WP_Error", lambda : WP_Error("wrong_post_type"))
            # end if
        elif "customize_changeset" != changeset_post.post_type:
            return php_new_class("WP_Error", lambda : WP_Error("wrong_post_type"))
        # end if
        changeset_data = php_json_decode(changeset_post.post_content, True)
        last_error = php_json_last_error()
        if last_error:
            return php_new_class("WP_Error", lambda : WP_Error("json_parse_error", "", last_error))
        # end if
        if (not php_is_array(changeset_data)):
            return php_new_class("WP_Error", lambda : WP_Error("expected_array"))
        # end if
        return changeset_data
    # end def get_changeset_post_data
    #// 
    #// Get changeset data.
    #// 
    #// @since 4.7.0
    #// @since 4.9.0 This will return the changeset's data with a user's autosave revision merged on top, if one exists and $autosaved is true.
    #// 
    #// @return array Changeset data.
    #//
    def changeset_data(self):
        
        if (php_isset(lambda : self._changeset_data)):
            return self._changeset_data
        # end if
        changeset_post_id = self.changeset_post_id()
        if (not changeset_post_id):
            self._changeset_data = Array()
        else:
            if self.autosaved() and is_user_logged_in():
                autosave_post = wp_get_post_autosave(changeset_post_id, get_current_user_id())
                if autosave_post:
                    data = self.get_changeset_post_data(autosave_post.ID)
                    if (not is_wp_error(data)):
                        self._changeset_data = data
                    # end if
                # end if
            # end if
            #// Load data from the changeset if it was not loaded from an autosave.
            if (not (php_isset(lambda : self._changeset_data))):
                data = self.get_changeset_post_data(changeset_post_id)
                if (not is_wp_error(data)):
                    self._changeset_data = data
                else:
                    self._changeset_data = Array()
                # end if
            # end if
        # end if
        return self._changeset_data
    # end def changeset_data
    pending_starter_content_settings_ids = Array()
    #// 
    #// Import theme starter content into the customized state.
    #// 
    #// @since 4.7.0
    #// 
    #// @param array $starter_content Starter content. Defaults to `get_theme_starter_content()`.
    #//
    def import_theme_starter_content(self, starter_content=Array()):
        
        if php_empty(lambda : starter_content):
            starter_content = get_theme_starter_content()
        # end if
        changeset_data = Array()
        if self.changeset_post_id():
            #// 
            #// Don't re-import starter content into a changeset saved persistently.
            #// This will need to be revisited in the future once theme switching
            #// is allowed with drafted/scheduled changesets, since switching to
            #// another theme could result in more starter content being applied.
            #// However, when doing an explicit save it is currently possible for
            #// nav menus and nav menu items specifically to lose their starter_content
            #// flags, thus resulting in duplicates being created since they fail
            #// to get re-used. See #40146.
            #//
            if "auto-draft" != get_post_status(self.changeset_post_id()):
                return
            # end if
            changeset_data = self.get_changeset_post_data(self.changeset_post_id())
        # end if
        sidebars_widgets = starter_content["widgets"] if (php_isset(lambda : starter_content["widgets"])) and (not php_empty(lambda : self.widgets)) else Array()
        attachments = starter_content["attachments"] if (php_isset(lambda : starter_content["attachments"])) and (not php_empty(lambda : self.nav_menus)) else Array()
        posts = starter_content["posts"] if (php_isset(lambda : starter_content["posts"])) and (not php_empty(lambda : self.nav_menus)) else Array()
        options = starter_content["options"] if (php_isset(lambda : starter_content["options"])) else Array()
        nav_menus = starter_content["nav_menus"] if (php_isset(lambda : starter_content["nav_menus"])) and (not php_empty(lambda : self.nav_menus)) else Array()
        theme_mods = starter_content["theme_mods"] if (php_isset(lambda : starter_content["theme_mods"])) else Array()
        #// Widgets.
        max_widget_numbers = Array()
        for sidebar_id,widgets in sidebars_widgets:
            sidebar_widget_ids = Array()
            for widget in widgets:
                id_base, instance = widget
                if (not (php_isset(lambda : max_widget_numbers[id_base]))):
                    #// When $settings is an array-like object, get an intrinsic array for use with array_keys().
                    settings = get_option(str("widget_") + str(id_base), Array())
                    if type(settings).__name__ == "ArrayObject" or type(settings).__name__ == "ArrayIterator":
                        settings = settings.getarraycopy()
                    # end if
                    #// Find the max widget number for this type.
                    widget_numbers = php_array_keys(settings)
                    if php_count(widget_numbers) > 0:
                        widget_numbers[-1] = 1
                        max_widget_numbers[id_base] = php_max(widget_numbers)
                    else:
                        max_widget_numbers[id_base] = 1
                    # end if
                # end if
                max_widget_numbers[id_base] += 1
                widget_id = php_sprintf("%s-%d", id_base, max_widget_numbers[id_base])
                setting_id = php_sprintf("widget_%s[%d]", id_base, max_widget_numbers[id_base])
                setting_value = self.widgets.sanitize_widget_js_instance(instance)
                if php_empty(lambda : changeset_data[setting_id]) or (not php_empty(lambda : changeset_data[setting_id]["starter_content"])):
                    self.set_post_value(setting_id, setting_value)
                    self.pending_starter_content_settings_ids[-1] = setting_id
                # end if
                sidebar_widget_ids[-1] = widget_id
            # end for
            setting_id = php_sprintf("sidebars_widgets[%s]", sidebar_id)
            if php_empty(lambda : changeset_data[setting_id]) or (not php_empty(lambda : changeset_data[setting_id]["starter_content"])):
                self.set_post_value(setting_id, sidebar_widget_ids)
                self.pending_starter_content_settings_ids[-1] = setting_id
            # end if
        # end for
        starter_content_auto_draft_post_ids = Array()
        if (not php_empty(lambda : changeset_data["nav_menus_created_posts"]["value"])):
            starter_content_auto_draft_post_ids = php_array_merge(starter_content_auto_draft_post_ids, changeset_data["nav_menus_created_posts"]["value"])
        # end if
        #// Make an index of all the posts needed and what their slugs are.
        needed_posts = Array()
        attachments = self.prepare_starter_content_attachments(attachments)
        for attachment in attachments:
            key = "attachment:" + attachment["post_name"]
            needed_posts[key] = True
        # end for
        for post_symbol in php_array_keys(posts):
            if php_empty(lambda : posts[post_symbol]["post_name"]) and php_empty(lambda : posts[post_symbol]["post_title"]):
                posts[post_symbol] = None
                continue
            # end if
            if php_empty(lambda : posts[post_symbol]["post_name"]):
                posts[post_symbol]["post_name"] = sanitize_title(posts[post_symbol]["post_title"])
            # end if
            if php_empty(lambda : posts[post_symbol]["post_type"]):
                posts[post_symbol]["post_type"] = "post"
            # end if
            needed_posts[posts[post_symbol]["post_type"] + ":" + posts[post_symbol]["post_name"]] = True
        # end for
        all_post_slugs = php_array_merge(wp_list_pluck(attachments, "post_name"), wp_list_pluck(posts, "post_name"))
        #// 
        #// Obtain all post types referenced in starter content to use in query.
        #// This is needed because 'any' will not account for post types not yet registered.
        #//
        post_types = php_array_filter(php_array_merge(Array("attachment"), wp_list_pluck(posts, "post_type")))
        #// Re-use auto-draft starter content posts referenced in the current customized state.
        existing_starter_content_posts = Array()
        if (not php_empty(lambda : starter_content_auto_draft_post_ids)):
            existing_posts_query = php_new_class("WP_Query", lambda : WP_Query(Array({"post__in": starter_content_auto_draft_post_ids, "post_status": "auto-draft", "post_type": post_types, "posts_per_page": -1})))
            for existing_post in existing_posts_query.posts:
                post_name = existing_post.post_name
                if php_empty(lambda : post_name):
                    post_name = get_post_meta(existing_post.ID, "_customize_draft_post_name", True)
                # end if
                existing_starter_content_posts[existing_post.post_type + ":" + post_name] = existing_post
            # end for
        # end if
        #// Re-use non-auto-draft posts.
        if (not php_empty(lambda : all_post_slugs)):
            existing_posts_query = php_new_class("WP_Query", lambda : WP_Query(Array({"post_name__in": all_post_slugs, "post_status": php_array_diff(get_post_stati(), Array("auto-draft")), "post_type": "any", "posts_per_page": -1})))
            for existing_post in existing_posts_query.posts:
                key = existing_post.post_type + ":" + existing_post.post_name
                if (php_isset(lambda : needed_posts[key])) and (not (php_isset(lambda : existing_starter_content_posts[key]))):
                    existing_starter_content_posts[key] = existing_post
                # end if
            # end for
        # end if
        #// Attachments are technically posts but handled differently.
        if (not php_empty(lambda : attachments)):
            attachment_ids = Array()
            for symbol,attachment in attachments:
                file_array = Array({"name": attachment["file_name"]})
                file_path = attachment["file_path"]
                attachment_id = None
                attached_file = None
                if (php_isset(lambda : existing_starter_content_posts["attachment:" + attachment["post_name"]])):
                    attachment_post = existing_starter_content_posts["attachment:" + attachment["post_name"]]
                    attachment_id = attachment_post.ID
                    attached_file = get_attached_file(attachment_id)
                    if php_empty(lambda : attached_file) or (not php_file_exists(attached_file)):
                        attachment_id = None
                        attached_file = None
                    elif self.get_stylesheet() != get_post_meta(attachment_post.ID, "_starter_content_theme", True):
                        #// Re-generate attachment metadata since it was previously generated for a different theme.
                        metadata = wp_generate_attachment_metadata(attachment_post.ID, attached_file)
                        wp_update_attachment_metadata(attachment_id, metadata)
                        update_post_meta(attachment_id, "_starter_content_theme", self.get_stylesheet())
                    # end if
                # end if
                #// Insert the attachment auto-draft because it doesn't yet exist or the attached file is gone.
                if (not attachment_id):
                    #// Copy file to temp location so that original file won't get deleted from theme after sideloading.
                    temp_file_name = wp_tempnam(wp_basename(file_path))
                    if temp_file_name and copy(file_path, temp_file_name):
                        file_array["tmp_name"] = temp_file_name
                    # end if
                    if php_empty(lambda : file_array["tmp_name"]):
                        continue
                    # end if
                    attachment_post_data = php_array_merge(wp_array_slice_assoc(attachment, Array("post_title", "post_content", "post_excerpt")), Array({"post_status": "auto-draft"}))
                    attachment_id = media_handle_sideload(file_array, 0, None, attachment_post_data)
                    if is_wp_error(attachment_id):
                        continue
                    # end if
                    update_post_meta(attachment_id, "_starter_content_theme", self.get_stylesheet())
                    update_post_meta(attachment_id, "_customize_draft_post_name", attachment["post_name"])
                # end if
                attachment_ids[symbol] = attachment_id
            # end for
            starter_content_auto_draft_post_ids = php_array_merge(starter_content_auto_draft_post_ids, php_array_values(attachment_ids))
        # end if
        #// Posts & pages.
        if (not php_empty(lambda : posts)):
            for post_symbol in php_array_keys(posts):
                if php_empty(lambda : posts[post_symbol]["post_type"]) or php_empty(lambda : posts[post_symbol]["post_name"]):
                    continue
                # end if
                post_type = posts[post_symbol]["post_type"]
                if (not php_empty(lambda : posts[post_symbol]["post_name"])):
                    post_name = posts[post_symbol]["post_name"]
                elif (not php_empty(lambda : posts[post_symbol]["post_title"])):
                    post_name = sanitize_title(posts[post_symbol]["post_title"])
                else:
                    continue
                # end if
                #// Use existing auto-draft post if one already exists with the same type and name.
                if (php_isset(lambda : existing_starter_content_posts[post_type + ":" + post_name])):
                    posts[post_symbol]["ID"] = existing_starter_content_posts[post_type + ":" + post_name].ID
                    continue
                # end if
                #// Translate the featured image symbol.
                if (not php_empty(lambda : posts[post_symbol]["thumbnail"])) and php_preg_match("/^{{(?P<symbol>.+)}}$/", posts[post_symbol]["thumbnail"], matches) and (php_isset(lambda : attachment_ids[matches["symbol"]])):
                    posts[post_symbol]["meta_input"]["_thumbnail_id"] = attachment_ids[matches["symbol"]]
                # end if
                if (not php_empty(lambda : posts[post_symbol]["template"])):
                    posts[post_symbol]["meta_input"]["_wp_page_template"] = posts[post_symbol]["template"]
                # end if
                r = self.nav_menus.insert_auto_draft_post(posts[post_symbol])
                if type(r).__name__ == "WP_Post":
                    posts[post_symbol]["ID"] = r.ID
                # end if
            # end for
            starter_content_auto_draft_post_ids = php_array_merge(starter_content_auto_draft_post_ids, wp_list_pluck(posts, "ID"))
        # end if
        #// The nav_menus_created_posts setting is why nav_menus component is dependency for adding posts.
        if (not php_empty(lambda : self.nav_menus)) and (not php_empty(lambda : starter_content_auto_draft_post_ids)):
            setting_id = "nav_menus_created_posts"
            self.set_post_value(setting_id, array_unique(php_array_values(starter_content_auto_draft_post_ids)))
            self.pending_starter_content_settings_ids[-1] = setting_id
        # end if
        #// Nav menus.
        placeholder_id = -1
        reused_nav_menu_setting_ids = Array()
        for nav_menu_location,nav_menu in nav_menus:
            nav_menu_term_id = None
            nav_menu_setting_id = None
            matches = Array()
            #// Look for an existing placeholder menu with starter content to re-use.
            for setting_id,setting_params in changeset_data:
                can_reuse = (not php_empty(lambda : setting_params["starter_content"])) and (not php_in_array(setting_id, reused_nav_menu_setting_ids, True)) and php_preg_match("#^nav_menu\\[(?P<nav_menu_id>-?\\d+)\\]$#", setting_id, matches)
                if can_reuse:
                    nav_menu_term_id = php_intval(matches["nav_menu_id"])
                    nav_menu_setting_id = setting_id
                    reused_nav_menu_setting_ids[-1] = setting_id
                    break
                # end if
            # end for
            if (not nav_menu_term_id):
                while True:
                    
                    if not ((php_isset(lambda : changeset_data[php_sprintf("nav_menu[%d]", placeholder_id)]))):
                        break
                    # end if
                    placeholder_id -= 1
                # end while
                nav_menu_term_id = placeholder_id
                nav_menu_setting_id = php_sprintf("nav_menu[%d]", placeholder_id)
            # end if
            self.set_post_value(nav_menu_setting_id, Array({"name": nav_menu["name"] if (php_isset(lambda : nav_menu["name"])) else nav_menu_location}))
            self.pending_starter_content_settings_ids[-1] = nav_menu_setting_id
            #// @todo Add support for menu_item_parent.
            position = 0
            for nav_menu_item in nav_menu["items"]:
                nav_menu_item_setting_id = php_sprintf("nav_menu_item[%d]", placeholder_id)
                placeholder_id -= 1
                if (not (php_isset(lambda : nav_menu_item["position"]))):
                    nav_menu_item["position"] = position
                    position += 1
                # end if
                nav_menu_item["nav_menu_term_id"] = nav_menu_term_id
                if (php_isset(lambda : nav_menu_item["object_id"])):
                    if "post_type" == nav_menu_item["type"] and php_preg_match("/^{{(?P<symbol>.+)}}$/", nav_menu_item["object_id"], matches) and (php_isset(lambda : posts[matches["symbol"]])):
                        nav_menu_item["object_id"] = posts[matches["symbol"]]["ID"]
                        if php_empty(lambda : nav_menu_item["title"]):
                            original_object = get_post(nav_menu_item["object_id"])
                            nav_menu_item["title"] = original_object.post_title
                        # end if
                    else:
                        continue
                    # end if
                else:
                    nav_menu_item["object_id"] = 0
                # end if
                if php_empty(lambda : changeset_data[nav_menu_item_setting_id]) or (not php_empty(lambda : changeset_data[nav_menu_item_setting_id]["starter_content"])):
                    self.set_post_value(nav_menu_item_setting_id, nav_menu_item)
                    self.pending_starter_content_settings_ids[-1] = nav_menu_item_setting_id
                # end if
            # end for
            setting_id = php_sprintf("nav_menu_locations[%s]", nav_menu_location)
            if php_empty(lambda : changeset_data[setting_id]) or (not php_empty(lambda : changeset_data[setting_id]["starter_content"])):
                self.set_post_value(setting_id, nav_menu_term_id)
                self.pending_starter_content_settings_ids[-1] = setting_id
            # end if
        # end for
        #// Options.
        for name,value in options:
            #// Serialize the value to check for post symbols.
            value = maybe_serialize(value)
            if is_serialized(value):
                if php_preg_match("/s:\\d+:\"{{(?P<symbol>.+)}}\"/", value, matches):
                    if (php_isset(lambda : posts[matches["symbol"]])):
                        symbol_match = posts[matches["symbol"]]["ID"]
                    elif (php_isset(lambda : attachment_ids[matches["symbol"]])):
                        symbol_match = attachment_ids[matches["symbol"]]
                    # end if
                    #// If we have any symbol matches, update the values.
                    if (php_isset(lambda : symbol_match)):
                        #// Replace found string matches with post IDs.
                        value = php_str_replace(matches[0], str("i:") + str(symbol_match), value)
                    else:
                        continue
                    # end if
                # end if
            elif php_preg_match("/^{{(?P<symbol>.+)}}$/", value, matches):
                if (php_isset(lambda : posts[matches["symbol"]])):
                    value = posts[matches["symbol"]]["ID"]
                elif (php_isset(lambda : attachment_ids[matches["symbol"]])):
                    value = attachment_ids[matches["symbol"]]
                else:
                    continue
                # end if
            # end if
            #// Unserialize values after checking for post symbols, so they can be properly referenced.
            value = maybe_unserialize(value)
            if php_empty(lambda : changeset_data[name]) or (not php_empty(lambda : changeset_data[name]["starter_content"])):
                self.set_post_value(name, value)
                self.pending_starter_content_settings_ids[-1] = name
            # end if
        # end for
        #// Theme mods.
        for name,value in theme_mods:
            #// Serialize the value to check for post symbols.
            value = maybe_serialize(value)
            #// Check if value was serialized.
            if is_serialized(value):
                if php_preg_match("/s:\\d+:\"{{(?P<symbol>.+)}}\"/", value, matches):
                    if (php_isset(lambda : posts[matches["symbol"]])):
                        symbol_match = posts[matches["symbol"]]["ID"]
                    elif (php_isset(lambda : attachment_ids[matches["symbol"]])):
                        symbol_match = attachment_ids[matches["symbol"]]
                    # end if
                    #// If we have any symbol matches, update the values.
                    if (php_isset(lambda : symbol_match)):
                        #// Replace found string matches with post IDs.
                        value = php_str_replace(matches[0], str("i:") + str(symbol_match), value)
                    else:
                        continue
                    # end if
                # end if
            elif php_preg_match("/^{{(?P<symbol>.+)}}$/", value, matches):
                if (php_isset(lambda : posts[matches["symbol"]])):
                    value = posts[matches["symbol"]]["ID"]
                elif (php_isset(lambda : attachment_ids[matches["symbol"]])):
                    value = attachment_ids[matches["symbol"]]
                else:
                    continue
                # end if
            # end if
            #// Unserialize values after checking for post symbols, so they can be properly referenced.
            value = maybe_unserialize(value)
            #// Handle header image as special case since setting has a legacy format.
            if "header_image" == name:
                name = "header_image_data"
                metadata = wp_get_attachment_metadata(value)
                if php_empty(lambda : metadata):
                    continue
                # end if
                value = Array({"attachment_id": value, "url": wp_get_attachment_url(value), "height": metadata["height"], "width": metadata["width"]})
            elif "background_image" == name:
                value = wp_get_attachment_url(value)
            # end if
            if php_empty(lambda : changeset_data[name]) or (not php_empty(lambda : changeset_data[name]["starter_content"])):
                self.set_post_value(name, value)
                self.pending_starter_content_settings_ids[-1] = name
            # end if
        # end for
        if (not php_empty(lambda : self.pending_starter_content_settings_ids)):
            if did_action("customize_register"):
                self._save_starter_content_changeset()
            else:
                add_action("customize_register", Array(self, "_save_starter_content_changeset"), 1000)
            # end if
        # end if
    # end def import_theme_starter_content
    #// 
    #// Prepare starter content attachments.
    #// 
    #// Ensure that the attachments are valid and that they have slugs and file name/path.
    #// 
    #// @since 4.7.0
    #// 
    #// @param array $attachments Attachments.
    #// @return array Prepared attachments.
    #//
    def prepare_starter_content_attachments(self, attachments=None):
        
        prepared_attachments = Array()
        if php_empty(lambda : attachments):
            return prepared_attachments
        # end if
        #// Such is The WordPress Way.
        php_include_file(ABSPATH + "wp-admin/includes/file.php", once=True)
        php_include_file(ABSPATH + "wp-admin/includes/media.php", once=True)
        php_include_file(ABSPATH + "wp-admin/includes/image.php", once=True)
        for symbol,attachment in attachments:
            #// A file is required and URLs to files are not currently allowed.
            if php_empty(lambda : attachment["file"]) or php_preg_match("#^https?://$#", attachment["file"]):
                continue
            # end if
            file_path = None
            if php_file_exists(attachment["file"]):
                file_path = attachment["file"]
                pass
            elif is_child_theme() and php_file_exists(get_stylesheet_directory() + "/" + attachment["file"]):
                file_path = get_stylesheet_directory() + "/" + attachment["file"]
            elif php_file_exists(get_template_directory() + "/" + attachment["file"]):
                file_path = get_template_directory() + "/" + attachment["file"]
            else:
                continue
            # end if
            file_name = wp_basename(attachment["file"])
            #// Skip file types that are not recognized.
            checked_filetype = wp_check_filetype(file_name)
            if php_empty(lambda : checked_filetype["type"]):
                continue
            # end if
            #// Ensure post_name is set since not automatically derived from post_title for new auto-draft posts.
            if php_empty(lambda : attachment["post_name"]):
                if (not php_empty(lambda : attachment["post_title"])):
                    attachment["post_name"] = sanitize_title(attachment["post_title"])
                else:
                    attachment["post_name"] = sanitize_title(php_preg_replace("/\\.\\w+$/", "", file_name))
                # end if
            # end if
            attachment["file_name"] = file_name
            attachment["file_path"] = file_path
            prepared_attachments[symbol] = attachment
        # end for
        return prepared_attachments
    # end def prepare_starter_content_attachments
    #// 
    #// Save starter content changeset.
    #// 
    #// @since 4.7.0
    #//
    def _save_starter_content_changeset(self):
        
        if php_empty(lambda : self.pending_starter_content_settings_ids):
            return
        # end if
        self.save_changeset_post(Array({"data": php_array_fill_keys(self.pending_starter_content_settings_ids, Array({"starter_content": True}))}, {"starter_content": True}))
        self.saved_starter_content_changeset = True
        self.pending_starter_content_settings_ids = Array()
    # end def _save_starter_content_changeset
    #// 
    #// Get dirty pre-sanitized setting values in the current customized state.
    #// 
    #// The returned array consists of a merge of three sources:
    #// 1. If the theme is not currently active, then the base array is any stashed
    #// theme mods that were modified previously but never published.
    #// 2. The values from the current changeset, if it exists.
    #// 3. If the user can customize, the values parsed from the incoming
    #// `$_POST['customized']` JSON data.
    #// 4. Any programmatically-set post values via `WP_Customize_Manager::set_post_value()`.
    #// 
    #// The name "unsanitized_post_values" is a carry-over from when the customized
    #// state was exclusively sourced from `$_POST['customized']`. Nevertheless,
    #// the value returned will come from the current changeset post and from the
    #// incoming post data.
    #// 
    #// @since 4.1.1
    #// @since 4.7.0 Added `$args` parameter and merging with changeset values and stashed theme mods.
    #// 
    #// @param array $args {
    #// Args.
    #// 
    #// @type bool $exclude_changeset Whether the changeset values should also be excluded. Defaults to false.
    #// @type bool $exclude_post_data Whether the post input values should also be excluded. Defaults to false when lacking the customize capability.
    #// }
    #// @return array
    #//
    def unsanitized_post_values(self, args=Array()):
        
        args = php_array_merge(Array({"exclude_changeset": False, "exclude_post_data": (not current_user_can("customize"))}), args)
        values = Array()
        #// Let default values be from the stashed theme mods if doing a theme switch and if no changeset is present.
        if (not self.is_theme_active()):
            stashed_theme_mods = get_option("customize_stashed_theme_mods")
            stylesheet = self.get_stylesheet()
            if (php_isset(lambda : stashed_theme_mods[stylesheet])):
                values = php_array_merge(values, wp_list_pluck(stashed_theme_mods[stylesheet], "value"))
            # end if
        # end if
        if (not args["exclude_changeset"]):
            for setting_id,setting_params in self.changeset_data():
                if (not php_array_key_exists("value", setting_params)):
                    continue
                # end if
                if (php_isset(lambda : setting_params["type"])) and "theme_mod" == setting_params["type"]:
                    #// Ensure that theme mods values are only used if they were saved under the current theme.
                    namespace_pattern = "/^(?P<stylesheet>.+?)::(?P<setting_id>.+)$/"
                    if php_preg_match(namespace_pattern, setting_id, matches) and self.get_stylesheet() == matches["stylesheet"]:
                        values[matches["setting_id"]] = setting_params["value"]
                    # end if
                else:
                    values[setting_id] = setting_params["value"]
                # end if
            # end for
        # end if
        if (not args["exclude_post_data"]):
            if (not (php_isset(lambda : self._post_values))):
                if (php_isset(lambda : PHP_POST["customized"])):
                    post_values = php_json_decode(wp_unslash(PHP_POST["customized"]), True)
                else:
                    post_values = Array()
                # end if
                if php_is_array(post_values):
                    self._post_values = post_values
                else:
                    self._post_values = Array()
                # end if
            # end if
            values = php_array_merge(values, self._post_values)
        # end if
        return values
    # end def unsanitized_post_values
    #// 
    #// Returns the sanitized value for a given setting from the current customized state.
    #// 
    #// The name "post_value" is a carry-over from when the customized state was exclusively
    #// sourced from `$_POST['customized']`. Nevertheless, the value returned will come
    #// from the current changeset post and from the incoming post data.
    #// 
    #// @since 3.4.0
    #// @since 4.1.1 Introduced the `$default` parameter.
    #// @since 4.6.0 `$default` is now returned early when the setting post value is invalid.
    #// 
    #// @see WP_REST_Server::dispatch()
    #// @see WP_REST_Request::sanitize_params()
    #// @see WP_REST_Request::has_valid_params()
    #// 
    #// @param WP_Customize_Setting $setting A WP_Customize_Setting derived object.
    #// @param mixed                $default Value returned $setting has no post value (added in 4.2.0)
    #// or the post value is invalid (added in 4.6.0).
    #// @return string|mixed $post_value Sanitized value or the $default provided.
    #//
    def post_value(self, setting=None, default=None):
        
        post_values = self.unsanitized_post_values()
        if (not php_array_key_exists(setting.id, post_values)):
            return default
        # end if
        value = post_values[setting.id]
        valid = setting.validate(value)
        if is_wp_error(valid):
            return default
        # end if
        value = setting.sanitize(value)
        if is_null(value) or is_wp_error(value):
            return default
        # end if
        return value
    # end def post_value
    #// 
    #// Override a setting's value in the current customized state.
    #// 
    #// The name "post_value" is a carry-over from when the customized state was
    #// exclusively sourced from `$_POST['customized']`.
    #// 
    #// @since 4.2.0
    #// 
    #// @param string $setting_id ID for the WP_Customize_Setting instance.
    #// @param mixed  $value      Post value.
    #//
    def set_post_value(self, setting_id=None, value=None):
        
        self.unsanitized_post_values()
        #// Populate _post_values from $_POST['customized'].
        self._post_values[setting_id] = value
        #// 
        #// Announce when a specific setting's unsanitized post value has been set.
        #// 
        #// Fires when the WP_Customize_Manager::set_post_value() method is called.
        #// 
        #// The dynamic portion of the hook name, `$setting_id`, refers to the setting ID.
        #// 
        #// @since 4.4.0
        #// 
        #// @param mixed                $value Unsanitized setting post value.
        #// @param WP_Customize_Manager $this  WP_Customize_Manager instance.
        #//
        do_action(str("customize_post_value_set_") + str(setting_id), value, self)
        #// 
        #// Announce when any setting's unsanitized post value has been set.
        #// 
        #// Fires when the WP_Customize_Manager::set_post_value() method is called.
        #// 
        #// This is useful for `WP_Customize_Setting` instances to watch
        #// in order to update a cached previewed value.
        #// 
        #// @since 4.4.0
        #// 
        #// @param string               $setting_id Setting ID.
        #// @param mixed                $value      Unsanitized setting post value.
        #// @param WP_Customize_Manager $this       WP_Customize_Manager instance.
        #//
        do_action("customize_post_value_set", setting_id, value, self)
    # end def set_post_value
    #// 
    #// Print JavaScript settings.
    #// 
    #// @since 3.4.0
    #//
    def customize_preview_init(self):
        
        #// 
        #// Now that Customizer previews are loaded into iframes via GET requests
        #// and natural URLs with transaction UUIDs added, we need to ensure that
        #// the responses are never cached by proxies. In practice, this will not
        #// be needed if the user is logged-in anyway. But if anonymous access is
        #// allowed then the auth cookies would not be sent and WordPress would
        #// not send no-cache headers by default.
        #//
        if (not php_headers_sent()):
            nocache_headers()
            php_header("X-Robots: noindex, nofollow, noarchive")
        # end if
        add_action("wp_head", "wp_no_robots")
        add_filter("wp_headers", Array(self, "filter_iframe_security_headers"))
        #// 
        #// If preview is being served inside the customizer preview iframe, and
        #// if the user doesn't have customize capability, then it is assumed
        #// that the user's session has expired and they need to re-authenticate.
        #//
        if self.messenger_channel and (not current_user_can("customize")):
            self.wp_die(-1, __("Unauthorized. You may remove the customize_messenger_channel param to preview as frontend."))
            return
        # end if
        self.prepare_controls()
        add_filter("wp_redirect", Array(self, "add_state_query_params"))
        wp_enqueue_script("customize-preview")
        wp_enqueue_style("customize-preview")
        add_action("wp_head", Array(self, "customize_preview_loading_style"))
        add_action("wp_head", Array(self, "remove_frameless_preview_messenger_channel"))
        add_action("wp_footer", Array(self, "customize_preview_settings"), 20)
        add_filter("get_edit_post_link", "__return_empty_string")
        #// 
        #// Fires once the Customizer preview has initialized and JavaScript
        #// settings have been printed.
        #// 
        #// @since 3.4.0
        #// 
        #// @param WP_Customize_Manager $this WP_Customize_Manager instance.
        #//
        do_action("customize_preview_init", self)
    # end def customize_preview_init
    #// 
    #// Filter the X-Frame-Options and Content-Security-Policy headers to ensure frontend can load in customizer.
    #// 
    #// @since 4.7.0
    #// 
    #// @param array $headers Headers.
    #// @return array Headers.
    #//
    def filter_iframe_security_headers(self, headers=None):
        
        headers["X-Frame-Options"] = "SAMEORIGIN"
        headers["Content-Security-Policy"] = "frame-ancestors 'self'"
        return headers
    # end def filter_iframe_security_headers
    #// 
    #// Add customize state query params to a given URL if preview is allowed.
    #// 
    #// @since 4.7.0
    #// @see wp_redirect()
    #// @see WP_Customize_Manager::get_allowed_url()
    #// 
    #// @param string $url URL.
    #// @return string URL.
    #//
    def add_state_query_params(self, url=None):
        
        parsed_original_url = wp_parse_url(url)
        is_allowed = False
        for allowed_url in self.get_allowed_urls():
            parsed_allowed_url = wp_parse_url(allowed_url)
            is_allowed = parsed_allowed_url["scheme"] == parsed_original_url["scheme"] and parsed_allowed_url["host"] == parsed_original_url["host"] and 0 == php_strpos(parsed_original_url["path"], parsed_allowed_url["path"])
            if is_allowed:
                break
            # end if
        # end for
        if is_allowed:
            query_params = Array({"customize_changeset_uuid": self.changeset_uuid()})
            if (not self.is_theme_active()):
                query_params["customize_theme"] = self.get_stylesheet()
            # end if
            if self.messenger_channel:
                query_params["customize_messenger_channel"] = self.messenger_channel
            # end if
            url = add_query_arg(query_params, url)
        # end if
        return url
    # end def add_state_query_params
    #// 
    #// Prevent sending a 404 status when returning the response for the customize
    #// preview, since it causes the jQuery Ajax to fail. Send 200 instead.
    #// 
    #// @since 4.0.0
    #// @deprecated 4.7.0
    #//
    def customize_preview_override_404_status(self):
        
        _deprecated_function(__METHOD__, "4.7.0")
    # end def customize_preview_override_404_status
    #// 
    #// Print base element for preview frame.
    #// 
    #// @since 3.4.0
    #// @deprecated 4.7.0
    #//
    def customize_preview_base(self):
        
        _deprecated_function(__METHOD__, "4.7.0")
    # end def customize_preview_base
    #// 
    #// Print a workaround to handle HTML5 tags in IE < 9.
    #// 
    #// @since 3.4.0
    #// @deprecated 4.7.0 Customizer no longer supports IE8, so all supported browsers recognize HTML5.
    #//
    def customize_preview_html5(self):
        
        _deprecated_function(__FUNCTION__, "4.7.0")
    # end def customize_preview_html5
    #// 
    #// Print CSS for loading indicators for the Customizer preview.
    #// 
    #// @since 4.2.0
    #//
    def customize_preview_loading_style(self):
        
        php_print("""       <style>
        body.wp-customizer-unloading {
        opacity: 0.25;
        cursor: progress !important;
        -webkit-transition: opacity 0.5s;
        transition: opacity 0.5s;
        }
        body.wp-customizer-unloading * {
        pointer-events: none !important;
        }
        form.customize-unpreviewable,
        form.customize-unpreviewable input,
        form.customize-unpreviewable select,
        form.customize-unpreviewable button,
        a.customize-unpreviewable,
        area.customize-unpreviewable {
        cursor: not-allowed !important;
        }
        </style>
        """)
    # end def customize_preview_loading_style
    #// 
    #// Remove customize_messenger_channel query parameter from the preview window when it is not in an iframe.
    #// 
    #// This ensures that the admin bar will be shown. It also ensures that link navigation will
    #// work as expected since the parent frame is not being sent the URL to navigate to.
    #// 
    #// @since 4.7.0
    #//
    def remove_frameless_preview_messenger_channel(self):
        
        if (not self.messenger_channel):
            return
        # end if
        php_print("""       <script>
        ( function() {
        var urlParser, oldQueryParams, newQueryParams, i;
    if ( parent !== window ) {
        return;
        }
        urlParser = document.createElement( 'a' );
        urlParser.href = location.href;
        oldQueryParams = urlParser.search.substr( 1 ).split( /&/ );
        newQueryParams = [];
    for ( i = 0; i < oldQueryParams.length; i += 1 ) {
    if ( ! /^customize_messenger_channel=/.test( oldQueryParams[ i ] ) ) {
        newQueryParams.push( oldQueryParams[ i ] );
        }
        }
        urlParser.search = newQueryParams.join( '&' );
    if ( urlParser.search !== location.search ) {
        location.replace( urlParser.href );
        }
        } )();
        </script>
        """)
    # end def remove_frameless_preview_messenger_channel
    #// 
    #// Print JavaScript settings for preview frame.
    #// 
    #// @since 3.4.0
    #//
    def customize_preview_settings(self):
        
        post_values = self.unsanitized_post_values(Array({"exclude_changeset": True}))
        setting_validities = self.validate_setting_values(post_values)
        exported_setting_validities = php_array_map(Array(self, "prepare_setting_validity_for_js"), setting_validities)
        #// Note that the REQUEST_URI is not passed into home_url() since this breaks subdirectory installations.
        self_url = home_url("/") if php_empty(lambda : PHP_SERVER["REQUEST_URI"]) else esc_url_raw(wp_unslash(PHP_SERVER["REQUEST_URI"]))
        state_query_params = Array("customize_theme", "customize_changeset_uuid", "customize_messenger_channel")
        self_url = remove_query_arg(state_query_params, self_url)
        allowed_urls = self.get_allowed_urls()
        allowed_hosts = Array()
        for allowed_url in allowed_urls:
            parsed = wp_parse_url(allowed_url)
            if php_empty(lambda : parsed["host"]):
                continue
            # end if
            host = parsed["host"]
            if (not php_empty(lambda : parsed["port"])):
                host += ":" + parsed["port"]
            # end if
            allowed_hosts[-1] = host
        # end for
        switched_locale = switch_to_locale(get_user_locale())
        l10n = Array({"shiftClickToEdit": __("Shift-click to edit this element."), "linkUnpreviewable": __("This link is not live-previewable."), "formUnpreviewable": __("This form is not live-previewable.")})
        if switched_locale:
            restore_previous_locale()
        # end if
        settings = Array({"changeset": Array({"uuid": self.changeset_uuid(), "autosaved": self.autosaved()})}, {"timeouts": Array({"selectiveRefresh": 250, "keepAliveSend": 1000})}, {"theme": Array({"stylesheet": self.get_stylesheet(), "active": self.is_theme_active()})}, {"url": Array({"self": self_url, "allowed": php_array_map("esc_url_raw", self.get_allowed_urls()), "allowedHosts": array_unique(allowed_hosts), "isCrossDomain": self.is_cross_domain()})}, {"channel": self.messenger_channel, "activePanels": Array(), "activeSections": Array(), "activeControls": Array(), "settingValidities": exported_setting_validities, "nonce": self.get_nonces() if current_user_can("customize") else Array(), "l10n": l10n, "_dirty": php_array_keys(post_values)})
        for panel_id,panel in self.panels:
            if panel.check_capabilities():
                settings["activePanels"][panel_id] = panel.active()
                for section_id,section in panel.sections:
                    if section.check_capabilities():
                        settings["activeSections"][section_id] = section.active()
                    # end if
                # end for
            # end if
        # end for
        for id,section in self.sections:
            if section.check_capabilities():
                settings["activeSections"][id] = section.active()
            # end if
        # end for
        for id,control in self.controls:
            if control.check_capabilities():
                settings["activeControls"][id] = control.active()
            # end if
        # end for
        php_print("     <script type=\"text/javascript\">\n         var _wpCustomizeSettings = ")
        php_print(wp_json_encode(settings))
        php_print(""";
        _wpCustomizeSettings.values = {};
        (function( v ) {
        """)
        #// 
        #// Serialize settings separately from the initial _wpCustomizeSettings
        #// serialization in order to avoid a peak memory usage spike.
        #// @todo We may not even need to export the values at all since the pane syncs them anyway.
        #//
        for id,setting in self.settings:
            if setting.check_capabilities():
                printf("v[%s] = %s;\n", wp_json_encode(id), wp_json_encode(setting.js_value()))
            # end if
        # end for
        php_print("         })( _wpCustomizeSettings.values );\n        </script>\n     ")
    # end def customize_preview_settings
    #// 
    #// Prints a signature so we can ensure the Customizer was properly executed.
    #// 
    #// @since 3.4.0
    #// @deprecated 4.7.0
    #//
    def customize_preview_signature(self):
        
        _deprecated_function(__METHOD__, "4.7.0")
    # end def customize_preview_signature
    #// 
    #// Removes the signature in case we experience a case where the Customizer was not properly executed.
    #// 
    #// @since 3.4.0
    #// @deprecated 4.7.0
    #// 
    #// @param mixed $return Value passed through for {@see 'wp_die_handler'} filter.
    #// @return mixed Value passed through for {@see 'wp_die_handler'} filter.
    #//
    def remove_preview_signature(self, return_=None):
        
        _deprecated_function(__METHOD__, "4.7.0")
        return return_
    # end def remove_preview_signature
    #// 
    #// Is it a theme preview?
    #// 
    #// @since 3.4.0
    #// 
    #// @return bool True if it's a preview, false if not.
    #//
    def is_preview(self):
        
        return php_bool(self.previewing)
    # end def is_preview
    #// 
    #// Retrieve the template name of the previewed theme.
    #// 
    #// @since 3.4.0
    #// 
    #// @return string Template name.
    #//
    def get_template(self):
        
        return self.theme().get_template()
    # end def get_template
    #// 
    #// Retrieve the stylesheet name of the previewed theme.
    #// 
    #// @since 3.4.0
    #// 
    #// @return string Stylesheet name.
    #//
    def get_stylesheet(self):
        
        return self.theme().get_stylesheet()
    # end def get_stylesheet
    #// 
    #// Retrieve the template root of the previewed theme.
    #// 
    #// @since 3.4.0
    #// 
    #// @return string Theme root.
    #//
    def get_template_root(self):
        
        return get_raw_theme_root(self.get_template(), True)
    # end def get_template_root
    #// 
    #// Retrieve the stylesheet root of the previewed theme.
    #// 
    #// @since 3.4.0
    #// 
    #// @return string Theme root.
    #//
    def get_stylesheet_root(self):
        
        return get_raw_theme_root(self.get_stylesheet(), True)
    # end def get_stylesheet_root
    #// 
    #// Filters the current theme and return the name of the previewed theme.
    #// 
    #// @since 3.4.0
    #// 
    #// @param $current_theme {@internal Parameter is not used}
    #// @return string Theme name.
    #//
    def current_theme(self, current_theme=None):
        
        return self.theme().display("Name")
    # end def current_theme
    #// 
    #// Validates setting values.
    #// 
    #// Validation is skipped for unregistered settings or for values that are
    #// already null since they will be skipped anyway. Sanitization is applied
    #// to values that pass validation, and values that become null or `WP_Error`
    #// after sanitizing are marked invalid.
    #// 
    #// @since 4.6.0
    #// 
    #// @see WP_REST_Request::has_valid_params()
    #// @see WP_Customize_Setting::validate()
    #// 
    #// @param array $setting_values Mapping of setting IDs to values to validate and sanitize.
    #// @param array $options {
    #// Options.
    #// 
    #// @type bool $validate_existence  Whether a setting's existence will be checked.
    #// @type bool $validate_capability Whether the setting capability will be checked.
    #// }
    #// @return array Mapping of setting IDs to return value of validate method calls, either `true` or `WP_Error`.
    #//
    def validate_setting_values(self, setting_values=None, options=Array()):
        
        options = wp_parse_args(options, Array({"validate_capability": False, "validate_existence": False}))
        validities = Array()
        for setting_id,unsanitized_value in setting_values:
            setting = self.get_setting(setting_id)
            if (not setting):
                if options["validate_existence"]:
                    validities[setting_id] = php_new_class("WP_Error", lambda : WP_Error("unrecognized", __("Setting does not exist or is unrecognized.")))
                # end if
                continue
            # end if
            if options["validate_capability"] and (not current_user_can(setting.capability)):
                validity = php_new_class("WP_Error", lambda : WP_Error("unauthorized", __("Unauthorized to modify setting due to capability.")))
            else:
                if is_null(unsanitized_value):
                    continue
                # end if
                validity = setting.validate(unsanitized_value)
            # end if
            if (not is_wp_error(validity)):
                #// This filter is documented in wp-includes/class-wp-customize-setting.php
                late_validity = apply_filters(str("customize_validate_") + str(setting.id), php_new_class("WP_Error", lambda : WP_Error()), unsanitized_value, setting)
                if is_wp_error(late_validity) and late_validity.has_errors():
                    validity = late_validity
                # end if
            # end if
            if (not is_wp_error(validity)):
                value = setting.sanitize(unsanitized_value)
                if is_null(value):
                    validity = False
                elif is_wp_error(value):
                    validity = value
                # end if
            # end if
            if False == validity:
                validity = php_new_class("WP_Error", lambda : WP_Error("invalid_value", __("Invalid value.")))
            # end if
            validities[setting_id] = validity
        # end for
        return validities
    # end def validate_setting_values
    #// 
    #// Prepares setting validity for exporting to the client (JS).
    #// 
    #// Converts `WP_Error` instance into array suitable for passing into the
    #// `wp.customize.Notification` JS model.
    #// 
    #// @since 4.6.0
    #// 
    #// @param true|WP_Error $validity Setting validity.
    #// @return true|array If `$validity` was a WP_Error, the error codes will be array-mapped
    #// to their respective `message` and `data` to pass into the
    #// `wp.customize.Notification` JS model.
    #//
    def prepare_setting_validity_for_js(self, validity=None):
        
        if is_wp_error(validity):
            notification = Array()
            for error_code,error_messages in validity.errors:
                notification[error_code] = Array({"message": join(" ", error_messages), "data": validity.get_error_data(error_code)})
            # end for
            return notification
        else:
            return True
        # end if
    # end def prepare_setting_validity_for_js
    #// 
    #// Handle customize_save WP Ajax request to save/update a changeset.
    #// 
    #// @since 3.4.0
    #// @since 4.7.0 The semantics of this method have changed to update a changeset, optionally to also change the status and other attributes.
    #//
    def save(self):
        
        if (not is_user_logged_in()):
            wp_send_json_error("unauthenticated")
        # end if
        if (not self.is_preview()):
            wp_send_json_error("not_preview")
        # end if
        action = "save-customize_" + self.get_stylesheet()
        if (not check_ajax_referer(action, "nonce", False)):
            wp_send_json_error("invalid_nonce")
        # end if
        changeset_post_id = self.changeset_post_id()
        is_new_changeset = php_empty(lambda : changeset_post_id)
        if is_new_changeset:
            if (not current_user_can(get_post_type_object("customize_changeset").cap.create_posts)):
                wp_send_json_error("cannot_create_changeset_post")
            # end if
        else:
            if (not current_user_can(get_post_type_object("customize_changeset").cap.edit_post, changeset_post_id)):
                wp_send_json_error("cannot_edit_changeset_post")
            # end if
        # end if
        if (not php_empty(lambda : PHP_POST["customize_changeset_data"])):
            input_changeset_data = php_json_decode(wp_unslash(PHP_POST["customize_changeset_data"]), True)
            if (not php_is_array(input_changeset_data)):
                wp_send_json_error("invalid_customize_changeset_data")
            # end if
        else:
            input_changeset_data = Array()
        # end if
        #// Validate title.
        changeset_title = None
        if (php_isset(lambda : PHP_POST["customize_changeset_title"])):
            changeset_title = sanitize_text_field(wp_unslash(PHP_POST["customize_changeset_title"]))
        # end if
        #// Validate changeset status param.
        is_publish = None
        changeset_status = None
        if (php_isset(lambda : PHP_POST["customize_changeset_status"])):
            changeset_status = wp_unslash(PHP_POST["customize_changeset_status"])
            if (not get_post_status_object(changeset_status)) or (not php_in_array(changeset_status, Array("draft", "pending", "publish", "future"), True)):
                wp_send_json_error("bad_customize_changeset_status", 400)
            # end if
            is_publish = "publish" == changeset_status or "future" == changeset_status
            if is_publish and (not current_user_can(get_post_type_object("customize_changeset").cap.publish_posts)):
                wp_send_json_error("changeset_publish_unauthorized", 403)
            # end if
        # end if
        #// 
        #// Validate changeset date param. Date is assumed to be in local time for
        #// the WP if in MySQL format (YYYY-MM-DD HH:MM:SS). Otherwise, the date
        #// is parsed with strtotime() so that ISO date format may be supplied
        #// or a string like "+10 minutes".
        #//
        changeset_date_gmt = None
        if (php_isset(lambda : PHP_POST["customize_changeset_date"])):
            changeset_date = wp_unslash(PHP_POST["customize_changeset_date"])
            if php_preg_match("/^\\d\\d\\d\\d-\\d\\d-\\d\\d \\d\\d:\\d\\d:\\d\\d$/", changeset_date):
                mm = php_substr(changeset_date, 5, 2)
                jj = php_substr(changeset_date, 8, 2)
                aa = php_substr(changeset_date, 0, 4)
                valid_date = wp_checkdate(mm, jj, aa, changeset_date)
                if (not valid_date):
                    wp_send_json_error("bad_customize_changeset_date", 400)
                # end if
                changeset_date_gmt = get_gmt_from_date(changeset_date)
            else:
                timestamp = strtotime(changeset_date)
                if (not timestamp):
                    wp_send_json_error("bad_customize_changeset_date", 400)
                # end if
                changeset_date_gmt = gmdate("Y-m-d H:i:s", timestamp)
            # end if
        # end if
        lock_user_id = None
        autosave = (not php_empty(lambda : PHP_POST["customize_changeset_autosave"]))
        if (not is_new_changeset):
            lock_user_id = wp_check_post_lock(self.changeset_post_id())
        # end if
        #// Force request to autosave when changeset is locked.
        if lock_user_id and (not autosave):
            autosave = True
            changeset_status = None
            changeset_date_gmt = None
        # end if
        if autosave and (not php_defined("DOING_AUTOSAVE")):
            #// Back-compat.
            php_define("DOING_AUTOSAVE", True)
        # end if
        autosaved = False
        r = self.save_changeset_post(Array({"status": changeset_status, "title": changeset_title, "date_gmt": changeset_date_gmt, "data": input_changeset_data, "autosave": autosave}))
        if autosave and (not is_wp_error(r)):
            autosaved = True
        # end if
        #// If the changeset was locked and an autosave request wasn't itself an error, then now explicitly return with a failure.
        if lock_user_id and (not is_wp_error(r)):
            r = php_new_class("WP_Error", lambda : WP_Error("changeset_locked", __("Changeset is being edited by other user."), Array({"lock_user": self.get_lock_user_data(lock_user_id)})))
        # end if
        if is_wp_error(r):
            response = Array({"message": r.get_error_message(), "code": r.get_error_code()})
            if php_is_array(r.get_error_data()):
                response = php_array_merge(response, r.get_error_data())
            else:
                response["data"] = r.get_error_data()
            # end if
        else:
            response = r
            changeset_post = get_post(self.changeset_post_id())
            #// Dismiss all other auto-draft changeset posts for this user (they serve like autosave revisions), as there should only be one.
            if is_new_changeset:
                self.dismiss_user_auto_draft_changesets()
            # end if
            #// Note that if the changeset status was publish, then it will get set to Trash if revisions are not supported.
            response["changeset_status"] = changeset_post.post_status
            if is_publish and "trash" == response["changeset_status"]:
                response["changeset_status"] = "publish"
            # end if
            if "publish" != response["changeset_status"]:
                self.set_changeset_lock(changeset_post.ID)
            # end if
            if "future" == response["changeset_status"]:
                response["changeset_date"] = changeset_post.post_date
            # end if
            if "publish" == response["changeset_status"] or "trash" == response["changeset_status"]:
                response["next_changeset_uuid"] = wp_generate_uuid4()
            # end if
        # end if
        if autosave:
            response["autosaved"] = autosaved
        # end if
        if (php_isset(lambda : response["setting_validities"])):
            response["setting_validities"] = php_array_map(Array(self, "prepare_setting_validity_for_js"), response["setting_validities"])
        # end if
        #// 
        #// Filters response data for a successful customize_save Ajax request.
        #// 
        #// This filter does not apply if there was a nonce or authentication failure.
        #// 
        #// @since 4.2.0
        #// 
        #// @param array                $response Additional information passed back to the 'saved'
        #// event on `wp.customize`.
        #// @param WP_Customize_Manager $this     WP_Customize_Manager instance.
        #//
        response = apply_filters("customize_save_response", response, self)
        if is_wp_error(r):
            wp_send_json_error(response)
        else:
            wp_send_json_success(response)
        # end if
    # end def save
    #// 
    #// Save the post for the loaded changeset.
    #// 
    #// @since 4.7.0
    #// 
    #// @param array $args {
    #// Args for changeset post.
    #// 
    #// @type array  $data            Optional additional changeset data. Values will be merged on top of any existing post values.
    #// @type string $status          Post status. Optional. If supplied, the save will be transactional and a post revision will be allowed.
    #// @type string $title           Post title. Optional.
    #// @type string $date_gmt        Date in GMT. Optional.
    #// @type int    $user_id         ID for user who is saving the changeset. Optional, defaults to the current user ID.
    #// @type bool   $starter_content Whether the data is starter content. If false (default), then $starter_content will be cleared for any $data being saved.
    #// @type bool   $autosave        Whether this is a request to create an autosave revision.
    #// }
    #// 
    #// @return array|WP_Error Returns array on success and WP_Error with array data on error.
    #//
    def save_changeset_post(self, args=Array()):
        
        args = php_array_merge(Array({"status": None, "title": None, "data": Array(), "date_gmt": None, "user_id": get_current_user_id(), "starter_content": False, "autosave": False}), args)
        changeset_post_id = self.changeset_post_id()
        existing_changeset_data = Array()
        if changeset_post_id:
            existing_status = get_post_status(changeset_post_id)
            if "publish" == existing_status or "trash" == existing_status:
                return php_new_class("WP_Error", lambda : WP_Error("changeset_already_published", __("The previous set of changes has already been published. Please try saving your current set of changes again."), Array({"next_changeset_uuid": wp_generate_uuid4()})))
            # end if
            existing_changeset_data = self.get_changeset_post_data(changeset_post_id)
            if is_wp_error(existing_changeset_data):
                return existing_changeset_data
            # end if
        # end if
        #// Fail if attempting to publish but publish hook is missing.
        if "publish" == args["status"] and False == has_action("transition_post_status", "_wp_customize_publish_changeset"):
            return php_new_class("WP_Error", lambda : WP_Error("missing_publish_callback"))
        # end if
        #// Validate date.
        now = gmdate("Y-m-d H:i:59")
        if args["date_gmt"]:
            is_future_dated = mysql2date("U", args["date_gmt"], False) > mysql2date("U", now, False)
            if (not is_future_dated):
                return php_new_class("WP_Error", lambda : WP_Error("not_future_date", __("You must supply a future date to schedule.")))
                pass
            # end if
            if (not self.is_theme_active()) and "future" == args["status"] or is_future_dated:
                return php_new_class("WP_Error", lambda : WP_Error("cannot_schedule_theme_switches"))
                pass
            # end if
            will_remain_auto_draft = (not args["status"]) and (not changeset_post_id) or "auto-draft" == get_post_status(changeset_post_id)
            if will_remain_auto_draft:
                return php_new_class("WP_Error", lambda : WP_Error("cannot_supply_date_for_auto_draft_changeset"))
            # end if
        elif changeset_post_id and "future" == args["status"]:
            #// Fail if the new status is future but the existing post's date is not in the future.
            changeset_post = get_post(changeset_post_id)
            if mysql2date("U", changeset_post.post_date_gmt, False) <= mysql2date("U", now, False):
                return php_new_class("WP_Error", lambda : WP_Error("not_future_date", __("You must supply a future date to schedule.")))
            # end if
        # end if
        if (not php_empty(lambda : is_future_dated)) and "publish" == args["status"]:
            args["status"] = "future"
        # end if
        #// Validate autosave param. See _wp_post_revision_fields() for why these fields are disallowed.
        if args["autosave"]:
            if args["date_gmt"]:
                return php_new_class("WP_Error", lambda : WP_Error("illegal_autosave_with_date_gmt"))
            elif args["status"]:
                return php_new_class("WP_Error", lambda : WP_Error("illegal_autosave_with_status"))
            elif args["user_id"] and get_current_user_id() != args["user_id"]:
                return php_new_class("WP_Error", lambda : WP_Error("illegal_autosave_with_non_current_user"))
            # end if
        # end if
        #// The request was made via wp.customize.previewer.save().
        update_transactionally = php_bool(args["status"])
        allow_revision = php_bool(args["status"])
        #// Amend post values with any supplied data.
        for setting_id,setting_params in args["data"]:
            if php_is_array(setting_params) and php_array_key_exists("value", setting_params):
                self.set_post_value(setting_id, setting_params["value"])
                pass
            # end if
        # end for
        #// Note that in addition to post data, this will include any stashed theme mods.
        post_values = self.unsanitized_post_values(Array({"exclude_changeset": True, "exclude_post_data": False}))
        self.add_dynamic_settings(php_array_keys(post_values))
        #// Ensure settings get created even if they lack an input value.
        #// 
        #// Get list of IDs for settings that have values different from what is currently
        #// saved in the changeset. By skipping any values that are already the same, the
        #// subset of changed settings can be passed into validate_setting_values to prevent
        #// an underprivileged modifying a single setting for which they have the capability
        #// from being blocked from saving. This also prevents a user from touching of the
        #// previous saved settings and overriding the associated user_id if they made no change.
        #//
        changed_setting_ids = Array()
        for setting_id,setting_value in post_values:
            setting = self.get_setting(setting_id)
            if setting and "theme_mod" == setting.type:
                prefixed_setting_id = self.get_stylesheet() + "::" + setting.id
            else:
                prefixed_setting_id = setting_id
            # end if
            is_value_changed = (not (php_isset(lambda : existing_changeset_data[prefixed_setting_id]))) or (not php_array_key_exists("value", existing_changeset_data[prefixed_setting_id])) or existing_changeset_data[prefixed_setting_id]["value"] != setting_value
            if is_value_changed:
                changed_setting_ids[-1] = setting_id
            # end if
        # end for
        #// 
        #// Fires before save validation happens.
        #// 
        #// Plugins can add just-in-time {@see 'customize_validate_{$this->ID}'} filters
        #// at this point to catch any settings registered after `customize_register`.
        #// The dynamic portion of the hook name, `$this->ID` refers to the setting ID.
        #// 
        #// @since 4.6.0
        #// 
        #// @param WP_Customize_Manager $this WP_Customize_Manager instance.
        #//
        do_action("customize_save_validation_before", self)
        #// Validate settings.
        validated_values = php_array_merge(php_array_fill_keys(php_array_keys(args["data"]), None), post_values)
        setting_validities = self.validate_setting_values(validated_values, Array({"validate_capability": True, "validate_existence": True}))
        invalid_setting_count = php_count(php_array_filter(setting_validities, "is_wp_error"))
        #// 
        #// Short-circuit if there are invalid settings the update is transactional.
        #// A changeset update is transactional when a status is supplied in the request.
        #//
        if update_transactionally and invalid_setting_count > 0:
            response = Array({"setting_validities": setting_validities, "message": php_sprintf(_n("Unable to save due to %s invalid setting.", "Unable to save due to %s invalid settings.", invalid_setting_count), number_format_i18n(invalid_setting_count))})
            return php_new_class("WP_Error", lambda : WP_Error("transaction_fail", "", response))
        # end if
        #// Obtain/merge data for changeset.
        original_changeset_data = self.get_changeset_post_data(changeset_post_id)
        data = original_changeset_data
        if is_wp_error(data):
            data = Array()
        # end if
        #// Ensure that all post values are included in the changeset data.
        for setting_id,post_value in post_values:
            if (not (php_isset(lambda : args["data"][setting_id]))):
                args["data"][setting_id] = Array()
            # end if
            if (not (php_isset(lambda : args["data"][setting_id]["value"]))):
                args["data"][setting_id]["value"] = post_value
            # end if
        # end for
        for setting_id,setting_params in args["data"]:
            setting = self.get_setting(setting_id)
            if (not setting) or (not setting.check_capabilities()):
                continue
            # end if
            #// Skip updating changeset for invalid setting values.
            if (php_isset(lambda : setting_validities[setting_id])) and is_wp_error(setting_validities[setting_id]):
                continue
            # end if
            changeset_setting_id = setting_id
            if "theme_mod" == setting.type:
                changeset_setting_id = php_sprintf("%s::%s", self.get_stylesheet(), setting_id)
            # end if
            if None == setting_params:
                data[changeset_setting_id] = None
            else:
                if (not (php_isset(lambda : data[changeset_setting_id]))):
                    data[changeset_setting_id] = Array()
                # end if
                #// Merge any additional setting params that have been supplied with the existing params.
                merged_setting_params = php_array_merge(data[changeset_setting_id], setting_params)
                #// Skip updating setting params if unchanged (ensuring the user_id is not overwritten).
                if data[changeset_setting_id] == merged_setting_params:
                    continue
                # end if
                data[changeset_setting_id] = php_array_merge(merged_setting_params, Array({"type": setting.type, "user_id": args["user_id"], "date_modified_gmt": current_time("mysql", True)}))
                #// Clear starter_content flag in data if changeset is not explicitly being updated for starter content.
                if php_empty(lambda : args["starter_content"]):
                    data[changeset_setting_id]["starter_content"] = None
                # end if
            # end if
        # end for
        filter_context = Array({"uuid": self.changeset_uuid(), "title": args["title"], "status": args["status"], "date_gmt": args["date_gmt"], "post_id": changeset_post_id, "previous_data": Array() if is_wp_error(original_changeset_data) else original_changeset_data, "manager": self})
        #// 
        #// Filters the settings' data that will be persisted into the changeset.
        #// 
        #// Plugins may amend additional data (such as additional meta for settings) into the changeset with this filter.
        #// 
        #// @since 4.7.0
        #// 
        #// @param array $data Updated changeset data, mapping setting IDs to arrays containing a $value item and optionally other metadata.
        #// @param array $context {
        #// Filter context.
        #// 
        #// @type string               $uuid          Changeset UUID.
        #// @type string               $title         Requested title for the changeset post.
        #// @type string               $status        Requested status for the changeset post.
        #// @type string               $date_gmt      Requested date for the changeset post in MySQL format and GMT timezone.
        #// @type int|false            $post_id       Post ID for the changeset, or false if it doesn't exist yet.
        #// @type array                $previous_data Previous data contained in the changeset.
        #// @type WP_Customize_Manager $manager       Manager instance.
        #// }
        #//
        data = apply_filters("customize_changeset_save_data", data, filter_context)
        #// Switch theme if publishing changes now.
        if "publish" == args["status"] and (not self.is_theme_active()):
            #// Temporarily stop previewing the theme to allow switch_themes() to operate properly.
            self.stop_previewing_theme()
            switch_theme(self.get_stylesheet())
            update_option("theme_switched_via_customizer", True)
            self.start_previewing_theme()
        # end if
        #// Gather the data for wp_insert_post()/wp_update_post().
        post_array = Array({"post_content": wp_json_encode(data, JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT)})
        if args["title"]:
            post_array["post_title"] = args["title"]
        # end if
        if changeset_post_id:
            post_array["ID"] = changeset_post_id
        else:
            post_array["post_type"] = "customize_changeset"
            post_array["post_name"] = self.changeset_uuid()
            post_array["post_status"] = "auto-draft"
        # end if
        if args["status"]:
            post_array["post_status"] = args["status"]
        # end if
        #// Reset post date to now if we are publishing, otherwise pass post_date_gmt and translate for post_date.
        if "publish" == args["status"]:
            post_array["post_date_gmt"] = "0000-00-00 00:00:00"
            post_array["post_date"] = "0000-00-00 00:00:00"
        elif args["date_gmt"]:
            post_array["post_date_gmt"] = args["date_gmt"]
            post_array["post_date"] = get_date_from_gmt(args["date_gmt"])
        elif changeset_post_id and "auto-draft" == get_post_status(changeset_post_id):
            #// 
            #// Keep bumping the date for the auto-draft whenever it is modified;
            #// this extends its life, preserving it from garbage-collection via
            #// wp_delete_auto_drafts().
            #//
            post_array["post_date"] = current_time("mysql")
            post_array["post_date_gmt"] = ""
        # end if
        self.store_changeset_revision = allow_revision
        add_filter("wp_save_post_revision_post_has_changed", Array(self, "_filter_revision_post_has_changed"), 5, 3)
        #// 
        #// Update the changeset post. The publish_customize_changeset action
        #// will cause the settings in the changeset to be saved via
        #// WP_Customize_Setting::save().
        #// 
        #// Prevent content filters from corrupting JSON in post_content.
        has_kses = False != has_filter("content_save_pre", "wp_filter_post_kses")
        if has_kses:
            kses_remove_filters()
        # end if
        has_targeted_link_rel_filters = False != has_filter("content_save_pre", "wp_targeted_link_rel")
        if has_targeted_link_rel_filters:
            wp_remove_targeted_link_rel_filters()
        # end if
        #// Note that updating a post with publish status will trigger WP_Customize_Manager::publish_changeset_values().
        if changeset_post_id:
            if args["autosave"] and "auto-draft" != get_post_status(changeset_post_id):
                #// See _wp_translate_postdata() for why this is required as it will use the edit_post meta capability.
                add_filter("map_meta_cap", Array(self, "grant_edit_post_capability_for_changeset"), 10, 4)
                post_array["post_ID"] = post_array["ID"]
                post_array["post_type"] = "customize_changeset"
                r = wp_create_post_autosave(wp_slash(post_array))
                remove_filter("map_meta_cap", Array(self, "grant_edit_post_capability_for_changeset"), 10)
            else:
                post_array["edit_date"] = True
                #// Prevent date clearing.
                r = wp_update_post(wp_slash(post_array), True)
                #// Delete autosave revision for user when the changeset is updated.
                if (not php_empty(lambda : args["user_id"])):
                    autosave_draft = wp_get_post_autosave(changeset_post_id, args["user_id"])
                    if autosave_draft:
                        wp_delete_post(autosave_draft.ID, True)
                    # end if
                # end if
            # end if
        else:
            r = wp_insert_post(wp_slash(post_array), True)
            if (not is_wp_error(r)):
                self._changeset_post_id = r
                pass
            # end if
        # end if
        #// Restore removed content filters.
        if has_kses:
            kses_init_filters()
        # end if
        if has_targeted_link_rel_filters:
            wp_init_targeted_link_rel_filters()
        # end if
        self._changeset_data = None
        #// Reset so WP_Customize_Manager::changeset_data() will re-populate with updated contents.
        remove_filter("wp_save_post_revision_post_has_changed", Array(self, "_filter_revision_post_has_changed"))
        response = Array({"setting_validities": setting_validities})
        if is_wp_error(r):
            response["changeset_post_save_failure"] = r.get_error_code()
            return php_new_class("WP_Error", lambda : WP_Error("changeset_post_save_failure", "", response))
        # end if
        return response
    # end def save_changeset_post
    #// 
    #// Trash or delete a changeset post.
    #// 
    #// The following re-formulates the logic from `wp_trash_post()` as done in
    #// `wp_publish_post()`. The reason for bypassing `wp_trash_post()` is that it
    #// will mutate the the `post_content` and the `post_name` when they should be
    #// untouched.
    #// 
    #// @since 4.9.0
    #// @global wpdb $wpdb WordPress database abstraction object.
    #// @see wp_trash_post()
    #// 
    #// @param int|WP_Post $post The changeset post.
    #// @return mixed A WP_Post object for the trashed post or an empty value on failure.
    #//
    def trash_changeset_post(self, post=None):
        
        global wpdb
        php_check_if_defined("wpdb")
        post = get_post(post)
        if (not type(post).__name__ == "WP_Post"):
            return post
        # end if
        post_id = post.ID
        if (not EMPTY_TRASH_DAYS):
            return wp_delete_post(post_id, True)
        # end if
        if "trash" == get_post_status(post):
            return False
        # end if
        #// This filter is documented in wp-includes/post.php
        check = apply_filters("pre_trash_post", None, post)
        if None != check:
            return check
        # end if
        #// This action is documented in wp-includes/post.php
        do_action("wp_trash_post", post_id)
        add_post_meta(post_id, "_wp_trash_meta_status", post.post_status)
        add_post_meta(post_id, "_wp_trash_meta_time", time())
        old_status = post.post_status
        new_status = "trash"
        wpdb.update(wpdb.posts, Array({"post_status": new_status}), Array({"ID": post.ID}))
        clean_post_cache(post.ID)
        post.post_status = new_status
        wp_transition_post_status(new_status, old_status, post)
        #// This action is documented in wp-includes/post.php
        do_action(str("edit_post_") + str(post.post_type), post.ID, post)
        #// This action is documented in wp-includes/post.php
        do_action("edit_post", post.ID, post)
        #// This action is documented in wp-includes/post.php
        do_action(str("save_post_") + str(post.post_type), post.ID, post, True)
        #// This action is documented in wp-includes/post.php
        do_action("save_post", post.ID, post, True)
        #// This action is documented in wp-includes/post.php
        do_action("wp_insert_post", post.ID, post, True)
        wp_trash_post_comments(post_id)
        #// This action is documented in wp-includes/post.php
        do_action("trashed_post", post_id)
        return post
    # end def trash_changeset_post
    #// 
    #// Handle request to trash a changeset.
    #// 
    #// @since 4.9.0
    #//
    def handle_changeset_trash_request(self):
        
        if (not is_user_logged_in()):
            wp_send_json_error("unauthenticated")
        # end if
        if (not self.is_preview()):
            wp_send_json_error("not_preview")
        # end if
        if (not check_ajax_referer("trash_customize_changeset", "nonce", False)):
            wp_send_json_error(Array({"code": "invalid_nonce", "message": __("There was an authentication problem. Please reload and try again.")}))
        # end if
        changeset_post_id = self.changeset_post_id()
        if (not changeset_post_id):
            wp_send_json_error(Array({"message": __("No changes saved yet, so there is nothing to trash."), "code": "non_existent_changeset"}))
            return
        # end if
        if changeset_post_id and (not current_user_can(get_post_type_object("customize_changeset").cap.delete_post, changeset_post_id)):
            wp_send_json_error(Array({"code": "changeset_trash_unauthorized", "message": __("Unable to trash changes.")}))
        # end if
        if "trash" == get_post_status(changeset_post_id):
            wp_send_json_error(Array({"message": __("Changes have already been trashed."), "code": "changeset_already_trashed"}))
            return
        # end if
        r = self.trash_changeset_post(changeset_post_id)
        if (not type(r).__name__ == "WP_Post"):
            wp_send_json_error(Array({"code": "changeset_trash_failure", "message": __("Unable to trash changes.")}))
        # end if
        wp_send_json_success(Array({"message": __("Changes trashed successfully.")}))
    # end def handle_changeset_trash_request
    #// 
    #// Re-map 'edit_post' meta cap for a customize_changeset post to be the same as 'customize' maps.
    #// 
    #// There is essentially a "meta meta" cap in play here, where 'edit_post' meta cap maps to
    #// the 'customize' meta cap which then maps to 'edit_theme_options'. This is currently
    #// required in core for `wp_create_post_autosave()` because it will call
    #// `_wp_translate_postdata()` which in turn will check if a user can 'edit_post', but the
    #// the caps for the customize_changeset post type are all mapping to the meta capability.
    #// This should be able to be removed once #40922 is addressed in core.
    #// 
    #// @since 4.9.0
    #// @link https://core.trac.wordpress.org/ticket/40922
    #// @see WP_Customize_Manager::save_changeset_post()
    #// @see _wp_translate_postdata()
    #// 
    #// @param string[] $caps    Array of the user's capabilities.
    #// @param string   $cap     Capability name.
    #// @param int      $user_id The user ID.
    #// @param array    $args    Adds the context to the cap. Typically the object ID.
    #// @return array Capabilities.
    #//
    def grant_edit_post_capability_for_changeset(self, caps=None, cap=None, user_id=None, args=None):
        
        if "edit_post" == cap and (not php_empty(lambda : args[0])) and "customize_changeset" == get_post_type(args[0]):
            post_type_obj = get_post_type_object("customize_changeset")
            caps = map_meta_cap(post_type_obj.cap.cap, user_id)
        # end if
        return caps
    # end def grant_edit_post_capability_for_changeset
    #// 
    #// Marks the changeset post as being currently edited by the current user.
    #// 
    #// @since 4.9.0
    #// 
    #// @param int  $changeset_post_id Changeset post id.
    #// @param bool $take_over Take over the changeset, default is false.
    #//
    def set_changeset_lock(self, changeset_post_id=None, take_over=False):
        
        if changeset_post_id:
            can_override = (not php_bool(get_post_meta(changeset_post_id, "_edit_lock", True)))
            if take_over:
                can_override = True
            # end if
            if can_override:
                lock = php_sprintf("%s:%s", time(), get_current_user_id())
                update_post_meta(changeset_post_id, "_edit_lock", lock)
            else:
                self.refresh_changeset_lock(changeset_post_id)
            # end if
        # end if
    # end def set_changeset_lock
    #// 
    #// Refreshes changeset lock with the current time if current user edited the changeset before.
    #// 
    #// @since 4.9.0
    #// 
    #// @param int $changeset_post_id Changeset post id.
    #//
    def refresh_changeset_lock(self, changeset_post_id=None):
        
        if (not changeset_post_id):
            return
        # end if
        lock = get_post_meta(changeset_post_id, "_edit_lock", True)
        lock = php_explode(":", lock)
        if lock and (not php_empty(lambda : lock[1])):
            user_id = php_intval(lock[1])
            current_user_id = get_current_user_id()
            if user_id == current_user_id:
                lock = php_sprintf("%s:%s", time(), user_id)
                update_post_meta(changeset_post_id, "_edit_lock", lock)
            # end if
        # end if
    # end def refresh_changeset_lock
    #// 
    #// Filter heartbeat settings for the Customizer.
    #// 
    #// @since 4.9.0
    #// @param array $settings Current settings to filter.
    #// @return array Heartbeat settings.
    #//
    def add_customize_screen_to_heartbeat_settings(self, settings=None):
        
        global pagenow
        php_check_if_defined("pagenow")
        if "customize.php" == pagenow:
            settings["screenId"] = "customize"
        # end if
        return settings
    # end def add_customize_screen_to_heartbeat_settings
    #// 
    #// Get lock user data.
    #// 
    #// @since 4.9.0
    #// 
    #// @param int $user_id User ID.
    #// @return array|null User data formatted for client.
    #//
    def get_lock_user_data(self, user_id=None):
        
        if (not user_id):
            return None
        # end if
        lock_user = get_userdata(user_id)
        if (not lock_user):
            return None
        # end if
        return Array({"id": lock_user.ID, "name": lock_user.display_name, "avatar": get_avatar_url(lock_user.ID, Array({"size": 128}))})
    # end def get_lock_user_data
    #// 
    #// Check locked changeset with heartbeat API.
    #// 
    #// @since 4.9.0
    #// 
    #// @param array  $response  The Heartbeat response.
    #// @param array  $data      The $_POST data sent.
    #// @param string $screen_id The screen id.
    #// @return array The Heartbeat response.
    #//
    def check_changeset_lock_with_heartbeat(self, response=None, data=None, screen_id=None):
        
        if (php_isset(lambda : data["changeset_uuid"])):
            changeset_post_id = self.find_changeset_post_id(data["changeset_uuid"])
        else:
            changeset_post_id = self.changeset_post_id()
        # end if
        if php_array_key_exists("check_changeset_lock", data) and "customize" == screen_id and changeset_post_id and current_user_can(get_post_type_object("customize_changeset").cap.edit_post, changeset_post_id):
            lock_user_id = wp_check_post_lock(changeset_post_id)
            if lock_user_id:
                response["customize_changeset_lock_user"] = self.get_lock_user_data(lock_user_id)
            else:
                #// Refreshing time will ensure that the user is sitting on customizer and has not closed the customizer tab.
                self.refresh_changeset_lock(changeset_post_id)
            # end if
        # end if
        return response
    # end def check_changeset_lock_with_heartbeat
    #// 
    #// Removes changeset lock when take over request is sent via Ajax.
    #// 
    #// @since 4.9.0
    #//
    def handle_override_changeset_lock_request(self):
        
        if (not self.is_preview()):
            wp_send_json_error("not_preview", 400)
        # end if
        if (not check_ajax_referer("customize_override_changeset_lock", "nonce", False)):
            wp_send_json_error(Array({"code": "invalid_nonce", "message": __("Security check failed.")}))
        # end if
        changeset_post_id = self.changeset_post_id()
        if php_empty(lambda : changeset_post_id):
            wp_send_json_error(Array({"code": "no_changeset_found_to_take_over", "message": __("No changeset found to take over")}))
        # end if
        if (not current_user_can(get_post_type_object("customize_changeset").cap.edit_post, changeset_post_id)):
            wp_send_json_error(Array({"code": "cannot_remove_changeset_lock", "message": __("Sorry, you are not allowed to take over.")}))
        # end if
        self.set_changeset_lock(changeset_post_id, True)
        wp_send_json_success("changeset_taken_over")
    # end def handle_override_changeset_lock_request
    store_changeset_revision = Array()
    #// 
    #// Filters whether a changeset has changed to create a new revision.
    #// 
    #// Note that this will not be called while a changeset post remains in auto-draft status.
    #// 
    #// @since 4.7.0
    #// 
    #// @param bool    $post_has_changed Whether the post has changed.
    #// @param WP_Post $last_revision    The last revision post object.
    #// @param WP_Post $post             The post object.
    #// @return bool Whether a revision should be made.
    #//
    def _filter_revision_post_has_changed(self, post_has_changed=None, last_revision=None, post=None):
        
        last_revision = None
        if "customize_changeset" == post.post_type:
            post_has_changed = self.store_changeset_revision
        # end if
        return post_has_changed
    # end def _filter_revision_post_has_changed
    #// 
    #// Publish changeset values.
    #// 
    #// This will the values contained in a changeset, even changesets that do not
    #// correspond to current manager instance. This is called by
    #// `_wp_customize_publish_changeset()` when a customize_changeset post is
    #// transitioned to the `publish` status. As such, this method should not be
    #// called directly and instead `wp_publish_post()` should be used.
    #// 
    #// Please note that if the settings in the changeset are for a non-activated
    #// theme, the theme must first be switched to (via `switch_theme()`) before
    #// invoking this method.
    #// 
    #// @since 4.7.0
    #// @see _wp_customize_publish_changeset()
    #// @global wpdb $wpdb WordPress database abstraction object.
    #// 
    #// @param int $changeset_post_id ID for customize_changeset post. Defaults to the changeset for the current manager instance.
    #// @return true|WP_Error True or error info.
    #//
    def _publish_changeset_values(self, changeset_post_id=None):
        
        global wpdb
        php_check_if_defined("wpdb")
        publishing_changeset_data = self.get_changeset_post_data(changeset_post_id)
        if is_wp_error(publishing_changeset_data):
            return publishing_changeset_data
        # end if
        changeset_post = get_post(changeset_post_id)
        #// 
        #// Temporarily override the changeset context so that it will be read
        #// in calls to unsanitized_post_values() and so that it will be available
        #// on the $wp_customize object passed to hooks during the save logic.
        #//
        previous_changeset_post_id = self._changeset_post_id
        self._changeset_post_id = changeset_post_id
        previous_changeset_uuid = self._changeset_uuid
        self._changeset_uuid = changeset_post.post_name
        previous_changeset_data = self._changeset_data
        self._changeset_data = publishing_changeset_data
        #// Parse changeset data to identify theme mod settings and user IDs associated with settings to be saved.
        setting_user_ids = Array()
        theme_mod_settings = Array()
        namespace_pattern = "/^(?P<stylesheet>.+?)::(?P<setting_id>.+)$/"
        matches = Array()
        for raw_setting_id,setting_params in self._changeset_data:
            actual_setting_id = None
            is_theme_mod_setting = (php_isset(lambda : setting_params["value"])) and (php_isset(lambda : setting_params["type"])) and "theme_mod" == setting_params["type"] and php_preg_match(namespace_pattern, raw_setting_id, matches)
            if is_theme_mod_setting:
                if (not (php_isset(lambda : theme_mod_settings[matches["stylesheet"]]))):
                    theme_mod_settings[matches["stylesheet"]] = Array()
                # end if
                theme_mod_settings[matches["stylesheet"]][matches["setting_id"]] = setting_params
                if self.get_stylesheet() == matches["stylesheet"]:
                    actual_setting_id = matches["setting_id"]
                # end if
            else:
                actual_setting_id = raw_setting_id
            # end if
            #// Keep track of the user IDs for settings actually for this theme.
            if actual_setting_id and (php_isset(lambda : setting_params["user_id"])):
                setting_user_ids[actual_setting_id] = setting_params["user_id"]
            # end if
        # end for
        changeset_setting_values = self.unsanitized_post_values(Array({"exclude_post_data": True, "exclude_changeset": False}))
        changeset_setting_ids = php_array_keys(changeset_setting_values)
        self.add_dynamic_settings(changeset_setting_ids)
        #// 
        #// Fires once the theme has switched in the Customizer, but before settings
        #// have been saved.
        #// 
        #// @since 3.4.0
        #// 
        #// @param WP_Customize_Manager $manager WP_Customize_Manager instance.
        #//
        do_action("customize_save", self)
        #// 
        #// Ensure that all settings will allow themselves to be saved. Note that
        #// this is safe because the setting would have checked the capability
        #// when the setting value was written into the changeset. So this is why
        #// an additional capability check is not required here.
        #//
        original_setting_capabilities = Array()
        for setting_id in changeset_setting_ids:
            setting = self.get_setting(setting_id)
            if setting and (not (php_isset(lambda : setting_user_ids[setting_id]))):
                original_setting_capabilities[setting.id] = setting.capability
                setting.capability = "exist"
            # end if
        # end for
        original_user_id = get_current_user_id()
        for setting_id in changeset_setting_ids:
            setting = self.get_setting(setting_id)
            if setting:
                #// 
                #// Set the current user to match the user who saved the value into
                #// the changeset so that any filters that apply during the save
                #// process will respect the original user's capabilities. This
                #// will ensure, for example, that KSES won't strip unsafe HTML
                #// when a scheduled changeset publishes via WP Cron.
                #//
                if (php_isset(lambda : setting_user_ids[setting_id])):
                    wp_set_current_user(setting_user_ids[setting_id])
                else:
                    wp_set_current_user(original_user_id)
                # end if
                setting.save()
            # end if
        # end for
        wp_set_current_user(original_user_id)
        #// Update the stashed theme mod settings, removing the active theme's stashed settings, if activated.
        if did_action("switch_theme"):
            other_theme_mod_settings = theme_mod_settings
            other_theme_mod_settings[self.get_stylesheet()] = None
            self.update_stashed_theme_mod_settings(other_theme_mod_settings)
        # end if
        #// 
        #// Fires after Customize settings have been saved.
        #// 
        #// @since 3.6.0
        #// 
        #// @param WP_Customize_Manager $manager WP_Customize_Manager instance.
        #//
        do_action("customize_save_after", self)
        #// Restore original capabilities.
        for setting_id,capability in original_setting_capabilities:
            setting = self.get_setting(setting_id)
            if setting:
                setting.capability = capability
            # end if
        # end for
        #// Restore original changeset data.
        self._changeset_data = previous_changeset_data
        self._changeset_post_id = previous_changeset_post_id
        self._changeset_uuid = previous_changeset_uuid
        #// 
        #// Convert all autosave revisions into their own auto-drafts so that users can be prompted to
        #// restore them when a changeset is published, but they had been locked out from including
        #// their changes in the changeset.
        #//
        revisions = wp_get_post_revisions(changeset_post_id, Array({"check_enabled": False}))
        for revision in revisions:
            if False != php_strpos(revision.post_name, str(changeset_post_id) + str("-autosave")):
                wpdb.update(wpdb.posts, Array({"post_status": "auto-draft", "post_type": "customize_changeset", "post_name": wp_generate_uuid4(), "post_parent": 0}), Array({"ID": revision.ID}))
                clean_post_cache(revision.ID)
            # end if
        # end for
        return True
    # end def _publish_changeset_values
    #// 
    #// Update stashed theme mod settings.
    #// 
    #// @since 4.7.0
    #// 
    #// @param array $inactive_theme_mod_settings Mapping of stylesheet to arrays of theme mod settings.
    #// @return array|false Returns array of updated stashed theme mods or false if the update failed or there were no changes.
    #//
    def update_stashed_theme_mod_settings(self, inactive_theme_mod_settings=None):
        
        stashed_theme_mod_settings = get_option("customize_stashed_theme_mods")
        if php_empty(lambda : stashed_theme_mod_settings):
            stashed_theme_mod_settings = Array()
        # end if
        stashed_theme_mod_settings[self.get_stylesheet()] = None
        #// Merge inactive theme mods with the stashed theme mod settings.
        for stylesheet,theme_mod_settings in inactive_theme_mod_settings:
            if (not (php_isset(lambda : stashed_theme_mod_settings[stylesheet]))):
                stashed_theme_mod_settings[stylesheet] = Array()
            # end if
            stashed_theme_mod_settings[stylesheet] = php_array_merge(stashed_theme_mod_settings[stylesheet], theme_mod_settings)
        # end for
        autoload = False
        result = update_option("customize_stashed_theme_mods", stashed_theme_mod_settings, autoload)
        if (not result):
            return False
        # end if
        return stashed_theme_mod_settings
    # end def update_stashed_theme_mod_settings
    #// 
    #// Refresh nonces for the current preview.
    #// 
    #// @since 4.2.0
    #//
    def refresh_nonces(self):
        
        if (not self.is_preview()):
            wp_send_json_error("not_preview")
        # end if
        wp_send_json_success(self.get_nonces())
    # end def refresh_nonces
    #// 
    #// Delete a given auto-draft changeset or the autosave revision for a given changeset or delete changeset lock.
    #// 
    #// @since 4.9.0
    #//
    def handle_dismiss_autosave_or_lock_request(self):
        
        #// Calls to dismiss_user_auto_draft_changesets() and wp_get_post_autosave() require non-zero get_current_user_id().
        if (not is_user_logged_in()):
            wp_send_json_error("unauthenticated", 401)
        # end if
        if (not self.is_preview()):
            wp_send_json_error("not_preview", 400)
        # end if
        if (not check_ajax_referer("customize_dismiss_autosave_or_lock", "nonce", False)):
            wp_send_json_error("invalid_nonce", 403)
        # end if
        changeset_post_id = self.changeset_post_id()
        dismiss_lock = (not php_empty(lambda : PHP_POST["dismiss_lock"]))
        dismiss_autosave = (not php_empty(lambda : PHP_POST["dismiss_autosave"]))
        if dismiss_lock:
            if php_empty(lambda : changeset_post_id) and (not dismiss_autosave):
                wp_send_json_error("no_changeset_to_dismiss_lock", 404)
            # end if
            if (not current_user_can(get_post_type_object("customize_changeset").cap.edit_post, changeset_post_id)) and (not dismiss_autosave):
                wp_send_json_error("cannot_remove_changeset_lock", 403)
            # end if
            delete_post_meta(changeset_post_id, "_edit_lock")
            if (not dismiss_autosave):
                wp_send_json_success("changeset_lock_dismissed")
            # end if
        # end if
        if dismiss_autosave:
            if php_empty(lambda : changeset_post_id) or "auto-draft" == get_post_status(changeset_post_id):
                dismissed = self.dismiss_user_auto_draft_changesets()
                if dismissed > 0:
                    wp_send_json_success("auto_draft_dismissed")
                else:
                    wp_send_json_error("no_auto_draft_to_delete", 404)
                # end if
            else:
                revision = wp_get_post_autosave(changeset_post_id, get_current_user_id())
                if revision:
                    if (not current_user_can(get_post_type_object("customize_changeset").cap.delete_post, changeset_post_id)):
                        wp_send_json_error("cannot_delete_autosave_revision", 403)
                    # end if
                    if (not wp_delete_post(revision.ID, True)):
                        wp_send_json_error("autosave_revision_deletion_failure", 500)
                    else:
                        wp_send_json_success("autosave_revision_deleted")
                    # end if
                else:
                    wp_send_json_error("no_autosave_revision_to_delete", 404)
                # end if
            # end if
        # end if
        wp_send_json_error("unknown_error", 500)
    # end def handle_dismiss_autosave_or_lock_request
    #// 
    #// Add a customize setting.
    #// 
    #// @since 3.4.0
    #// @since 4.5.0 Return added WP_Customize_Setting instance.
    #// 
    #// @see WP_Customize_Setting::__construct()
    #// @link https://developer.wordpress.org/themes/customize-api
    #// 
    #// @param WP_Customize_Setting|string $id   Customize Setting object, or ID.
    #// @param array                       $args Optional. Array of properties for the new Setting object.
    #// See WP_Customize_Setting::__construct() for information
    #// on accepted arguments. Default empty array.
    #// @return WP_Customize_Setting The instance of the setting that was added.
    #//
    def add_setting(self, id=None, args=Array()):
        
        if type(id).__name__ == "WP_Customize_Setting":
            setting = id
        else:
            class_ = "WP_Customize_Setting"
            #// This filter is documented in wp-includes/class-wp-customize-manager.php
            args = apply_filters("customize_dynamic_setting_args", args, id)
            #// This filter is documented in wp-includes/class-wp-customize-manager.php
            class_ = apply_filters("customize_dynamic_setting_class", class_, id, args)
            setting = php_new_class(class_, lambda : {**locals(), **globals()}[class_](self, id, args))
        # end if
        self.settings[setting.id] = setting
        return setting
    # end def add_setting
    #// 
    #// Register any dynamically-created settings, such as those from $_POST['customized']
    #// that have no corresponding setting created.
    #// 
    #// This is a mechanism to "wake up" settings that have been dynamically created
    #// on the front end and have been sent to WordPress in `$_POST['customized']`. When WP
    #// loads, the dynamically-created settings then will get created and previewed
    #// even though they are not directly created statically with code.
    #// 
    #// @since 4.2.0
    #// 
    #// @param array $setting_ids The setting IDs to add.
    #// @return array The WP_Customize_Setting objects added.
    #//
    def add_dynamic_settings(self, setting_ids=None):
        
        new_settings = Array()
        for setting_id in setting_ids:
            #// Skip settings already created.
            if self.get_setting(setting_id):
                continue
            # end if
            setting_args = False
            setting_class = "WP_Customize_Setting"
            #// 
            #// Filters a dynamic setting's constructor args.
            #// 
            #// For a dynamic setting to be registered, this filter must be employed
            #// to override the default false value with an array of args to pass to
            #// the WP_Customize_Setting constructor.
            #// 
            #// @since 4.2.0
            #// 
            #// @param false|array $setting_args The arguments to the WP_Customize_Setting constructor.
            #// @param string      $setting_id   ID for dynamic setting, usually coming from `$_POST['customized']`.
            #//
            setting_args = apply_filters("customize_dynamic_setting_args", setting_args, setting_id)
            if False == setting_args:
                continue
            # end if
            #// 
            #// Allow non-statically created settings to be constructed with custom WP_Customize_Setting subclass.
            #// 
            #// @since 4.2.0
            #// 
            #// @param string $setting_class WP_Customize_Setting or a subclass.
            #// @param string $setting_id    ID for dynamic setting, usually coming from `$_POST['customized']`.
            #// @param array  $setting_args  WP_Customize_Setting or a subclass.
            #//
            setting_class = apply_filters("customize_dynamic_setting_class", setting_class, setting_id, setting_args)
            setting = php_new_class(setting_class, lambda : {**locals(), **globals()}[setting_class](self, setting_id, setting_args))
            self.add_setting(setting)
            new_settings[-1] = setting
        # end for
        return new_settings
    # end def add_dynamic_settings
    #// 
    #// Retrieve a customize setting.
    #// 
    #// @since 3.4.0
    #// 
    #// @param string $id Customize Setting ID.
    #// @return WP_Customize_Setting|void The setting, if set.
    #//
    def get_setting(self, id=None):
        
        if (php_isset(lambda : self.settings[id])):
            return self.settings[id]
        # end if
    # end def get_setting
    #// 
    #// Remove a customize setting.
    #// 
    #// Note that removing the setting doesn't destroy the WP_Customize_Setting instance or remove its filters.
    #// 
    #// @since 3.4.0
    #// 
    #// @param string $id Customize Setting ID.
    #//
    def remove_setting(self, id=None):
        
        self.settings[id] = None
    # end def remove_setting
    #// 
    #// Add a customize panel.
    #// 
    #// @since 4.0.0
    #// @since 4.5.0 Return added WP_Customize_Panel instance.
    #// 
    #// @see WP_Customize_Panel::__construct()
    #// 
    #// @param WP_Customize_Panel|string $id   Customize Panel object, or ID.
    #// @param array                     $args Optional. Array of properties for the new Panel object.
    #// See WP_Customize_Panel::__construct() for information
    #// on accepted arguments. Default empty array.
    #// @return WP_Customize_Panel The instance of the panel that was added.
    #//
    def add_panel(self, id=None, args=Array()):
        
        if type(id).__name__ == "WP_Customize_Panel":
            panel = id
        else:
            panel = php_new_class("WP_Customize_Panel", lambda : WP_Customize_Panel(self, id, args))
        # end if
        self.panels[panel.id] = panel
        return panel
    # end def add_panel
    #// 
    #// Retrieve a customize panel.
    #// 
    #// @since 4.0.0
    #// 
    #// @param string $id Panel ID to get.
    #// @return WP_Customize_Panel|void Requested panel instance, if set.
    #//
    def get_panel(self, id=None):
        
        if (php_isset(lambda : self.panels[id])):
            return self.panels[id]
        # end if
    # end def get_panel
    #// 
    #// Remove a customize panel.
    #// 
    #// Note that removing the panel doesn't destroy the WP_Customize_Panel instance or remove its filters.
    #// 
    #// @since 4.0.0
    #// 
    #// @param string $id Panel ID to remove.
    #//
    def remove_panel(self, id=None):
        
        #// Removing core components this way is _doing_it_wrong().
        if php_in_array(id, self.components, True):
            message = php_sprintf(__("Removing %1$s manually will cause PHP warnings. Use the %2$s filter instead."), id, "<a href=\"" + esc_url("https://developer.wordpress.org/reference/hooks/customize_loaded_components/") + "\"><code>customize_loaded_components</code></a>")
            _doing_it_wrong(__METHOD__, message, "4.5.0")
        # end if
        self.panels[id] = None
    # end def remove_panel
    #// 
    #// Register a customize panel type.
    #// 
    #// Registered types are eligible to be rendered via JS and created dynamically.
    #// 
    #// @since 4.3.0
    #// 
    #// @see WP_Customize_Panel
    #// 
    #// @param string $panel Name of a custom panel which is a subclass of WP_Customize_Panel.
    #//
    def register_panel_type(self, panel=None):
        
        self.registered_panel_types[-1] = panel
    # end def register_panel_type
    #// 
    #// Render JS templates for all registered panel types.
    #// 
    #// @since 4.3.0
    #//
    def render_panel_templates(self):
        
        for panel_type in self.registered_panel_types:
            panel = php_new_class(panel_type, lambda : {**locals(), **globals()}[panel_type](self, "temp", Array()))
            panel.print_template()
        # end for
    # end def render_panel_templates
    #// 
    #// Add a customize section.
    #// 
    #// @since 3.4.0
    #// @since 4.5.0 Return added WP_Customize_Section instance.
    #// 
    #// @see WP_Customize_Section::__construct()
    #// 
    #// @param WP_Customize_Section|string $id   Customize Section object, or ID.
    #// @param array                       $args Optional. Array of properties for the new Section object.
    #// See WP_Customize_Section::__construct() for information
    #// on accepted arguments. Default empty array.
    #// @return WP_Customize_Section The instance of the section that was added.
    #//
    def add_section(self, id=None, args=Array()):
        
        if type(id).__name__ == "WP_Customize_Section":
            section = id
        else:
            section = php_new_class("WP_Customize_Section", lambda : WP_Customize_Section(self, id, args))
        # end if
        self.sections[section.id] = section
        return section
    # end def add_section
    #// 
    #// Retrieve a customize section.
    #// 
    #// @since 3.4.0
    #// 
    #// @param string $id Section ID.
    #// @return WP_Customize_Section|void The section, if set.
    #//
    def get_section(self, id=None):
        
        if (php_isset(lambda : self.sections[id])):
            return self.sections[id]
        # end if
    # end def get_section
    #// 
    #// Remove a customize section.
    #// 
    #// Note that removing the section doesn't destroy the WP_Customize_Section instance or remove its filters.
    #// 
    #// @since 3.4.0
    #// 
    #// @param string $id Section ID.
    #//
    def remove_section(self, id=None):
        
        self.sections[id] = None
    # end def remove_section
    #// 
    #// Register a customize section type.
    #// 
    #// Registered types are eligible to be rendered via JS and created dynamically.
    #// 
    #// @since 4.3.0
    #// 
    #// @see WP_Customize_Section
    #// 
    #// @param string $section Name of a custom section which is a subclass of WP_Customize_Section.
    #//
    def register_section_type(self, section=None):
        
        self.registered_section_types[-1] = section
    # end def register_section_type
    #// 
    #// Render JS templates for all registered section types.
    #// 
    #// @since 4.3.0
    #//
    def render_section_templates(self):
        
        for section_type in self.registered_section_types:
            section = php_new_class(section_type, lambda : {**locals(), **globals()}[section_type](self, "temp", Array()))
            section.print_template()
        # end for
    # end def render_section_templates
    #// 
    #// Add a customize control.
    #// 
    #// @since 3.4.0
    #// @since 4.5.0 Return added WP_Customize_Control instance.
    #// 
    #// @see WP_Customize_Control::__construct()
    #// 
    #// @param WP_Customize_Control|string $id   Customize Control object, or ID.
    #// @param array                       $args Optional. Array of properties for the new Control object.
    #// See WP_Customize_Control::__construct() for information
    #// on accepted arguments. Default empty array.
    #// @return WP_Customize_Control The instance of the control that was added.
    #//
    def add_control(self, id=None, args=Array()):
        
        if type(id).__name__ == "WP_Customize_Control":
            control = id
        else:
            control = php_new_class("WP_Customize_Control", lambda : WP_Customize_Control(self, id, args))
        # end if
        self.controls[control.id] = control
        return control
    # end def add_control
    #// 
    #// Retrieve a customize control.
    #// 
    #// @since 3.4.0
    #// 
    #// @param string $id ID of the control.
    #// @return WP_Customize_Control|void The control object, if set.
    #//
    def get_control(self, id=None):
        
        if (php_isset(lambda : self.controls[id])):
            return self.controls[id]
        # end if
    # end def get_control
    #// 
    #// Remove a customize control.
    #// 
    #// Note that removing the control doesn't destroy the WP_Customize_Control instance or remove its filters.
    #// 
    #// @since 3.4.0
    #// 
    #// @param string $id ID of the control.
    #//
    def remove_control(self, id=None):
        
        self.controls[id] = None
    # end def remove_control
    #// 
    #// Register a customize control type.
    #// 
    #// Registered types are eligible to be rendered via JS and created dynamically.
    #// 
    #// @since 4.1.0
    #// 
    #// @param string $control Name of a custom control which is a subclass of
    #// WP_Customize_Control.
    #//
    def register_control_type(self, control=None):
        
        self.registered_control_types[-1] = control
    # end def register_control_type
    #// 
    #// Render JS templates for all registered control types.
    #// 
    #// @since 4.1.0
    #//
    def render_control_templates(self):
        
        if self.branching():
            l10n = Array({"locked": __("%s is already customizing this changeset. Please wait until they are done to try customizing. Your latest changes have been autosaved."), "locked_allow_override": __("%s is already customizing this changeset. Do you want to take over?")})
        else:
            l10n = Array({"locked": __("%s is already customizing this site. Please wait until they are done to try customizing. Your latest changes have been autosaved."), "locked_allow_override": __("%s is already customizing this site. Do you want to take over?")})
        # end if
        for control_type in self.registered_control_types:
            control = php_new_class(control_type, lambda : {**locals(), **globals()}[control_type](self, "temp", Array({"settings": Array()})))
            control.print_template()
        # end for
        php_print("""
        <script type=\"text/html\" id=\"tmpl-customize-control-default-content\">
        <#
        var inputId = _.uniqueId( 'customize-control-default-input-' );
        var descriptionId = _.uniqueId( 'customize-control-default-description-' );
        var describedByAttr = data.description ? ' aria-describedby=\"' + descriptionId + '\" ' : '';
        #>
        <# switch ( data.type ) {
        case 'checkbox': #>
        <span class=\"customize-inside-control-row\">
        <input
        id=\"{{ inputId }}\"
        {{{ describedByAttr }}}
        type=\"checkbox\"
        value=\"{{ data.value }}\"
        data-customize-setting-key-link=\"default\"
        >
        <label for=\"{{ inputId }}\">
        {{ data.label }}
        </label>
        <# if ( data.description ) { #>
        <span id=\"{{ descriptionId }}\" class=\"description customize-control-description\">{{{ data.description }}}</span>
        <# } #>
        </span>
        <#
        break;
        case 'radio':
    if ( ! data.choices ) {
        return;
        }
        #>
        <# if ( data.label ) { #>
        <label for=\"{{ inputId }}\" class=\"customize-control-title\">
        {{ data.label }}
        </label>
        <# } #>
        <# if ( data.description ) { #>
        <span id=\"{{ descriptionId }}\" class=\"description customize-control-description\">{{{ data.description }}}</span>
        <# } #>
        <# _.each( data.choices, function( val, key ) { #>
        <span class=\"customize-inside-control-row\">
        <#
        var value, text;
    if ( _.isObject( val ) ) {
        value = val.value;
        text = val.text;
        } else {
        value = key;
        text = val;
        }
        #>
        <input
        id=\"{{ inputId + '-' + value }}\"
        type=\"radio\"
        value=\"{{ value }}\"
        name=\"{{ inputId }}\"
        data-customize-setting-key-link=\"default\"
        {{{ describedByAttr }}}
        >
        <label for=\"{{ inputId + '-' + value }}\">{{ text }}</label>
        </span>
        <# } ); #>
        <#
        break;
        default:
        #>
        <# if ( data.label ) { #>
        <label for=\"{{ inputId }}\" class=\"customize-control-title\">
        {{ data.label }}
        </label>
        <# } #>
        <# if ( data.description ) { #>
        <span id=\"{{ descriptionId }}\" class=\"description customize-control-description\">{{{ data.description }}}</span>
        <# } #>
        <#
        var inputAttrs = {
        id: inputId,
        'data-customize-setting-key-link': 'default'
        };
    if ( 'textarea' === data.type ) {
        inputAttrs.rows = '5';
        } else if ( 'button' === data.type ) {
        inputAttrs['class'] = 'button button-secondary';
        inputAttrs.type = 'button';
        } else {
        inputAttrs.type = data.type;
        }
    if ( data.description ) {
        inputAttrs['aria-describedby'] = descriptionId;
        }
        _.extend( inputAttrs, data.input_attrs );
        #>
        <# if ( 'button' === data.type ) { #>
        <button
        <# _.each( _.extend( inputAttrs ), function( value, key ) { #>
        {{{ key }}}=\"{{ value }}\"
        <# } ); #>
        >{{ inputAttrs.value }}</button>
        <# } else if ( 'textarea' === data.type ) { #>
        <textarea
        <# _.each( _.extend( inputAttrs ), function( value, key ) { #>
        {{{ key }}}=\"{{ value }}\"
        <# }); #>
        >{{ inputAttrs.value }}</textarea>
        <# } else if ( 'select' === data.type ) { #>
        <# delete inputAttrs.type; #>
        <select
        <# _.each( _.extend( inputAttrs ), function( value, key ) { #>
        {{{ key }}}=\"{{ value }}\"
        <# }); #>
        >
        <# _.each( data.choices, function( val, key ) { #>
        <#
        var value, text;
    if ( _.isObject( val ) ) {
        value = val.value;
        text = val.text;
        } else {
        value = key;
        text = val;
        }
        #>
        <option value=\"{{ value }}\">{{ text }}</option>
        <# } ); #>
        </select>
        <# } else { #>
        <input
        <# _.each( _.extend( inputAttrs ), function( value, key ) { #>
        {{{ key }}}=\"{{ value }}\"
        <# }); #>
        >
        <# } #>
        <# } #>
        </script>
        <script type=\"text/html\" id=\"tmpl-customize-notification\">
        <li class=\"notice notice-{{ data.type || 'info' }} {{ data.alt ? 'notice-alt' : '' }} {{ data.dismissible ? 'is-dismissible' : '' }} {{ data.containerClasses || '' }}\" data-code=\"{{ data.code }}\" data-type=\"{{ data.type }}\">
        <div class=\"notification-message\">{{{ data.message || data.code }}}</div>
        <# if ( data.dismissible ) { #>
        <button type=\"button\" class=\"notice-dismiss\"><span class=\"screen-reader-text\">""")
        _e("Dismiss")
        php_print("""</span></button>
        <# } #>
        </li>
        </script>
        <script type=\"text/html\" id=\"tmpl-customize-changeset-locked-notification\">
        <li class=\"notice notice-{{ data.type || 'info' }} {{ data.containerClasses || '' }}\" data-code=\"{{ data.code }}\" data-type=\"{{ data.type }}\">
        <div class=\"notification-message customize-changeset-locked-message\">
        <img class=\"customize-changeset-locked-avatar\" src=\"{{ data.lockUser.avatar }}\" alt=\"{{ data.lockUser.name }}\">
        <p class=\"currently-editing\">
        <# if ( data.message ) { #>
        {{{ data.message }}}
        <# } else if ( data.allowOverride ) { #>
        """)
        php_print(esc_html(php_sprintf(l10n["locked_allow_override"], "{{ data.lockUser.name }}")))
        php_print("                     <# } else { #>\n                            ")
        php_print(esc_html(php_sprintf(l10n["locked"], "{{ data.lockUser.name }}")))
        php_print("""                       <# } #>
        </p>
        <p class=\"notice notice-error notice-alt\" hidden></p>
        <p class=\"action-buttons\">
        <# if ( data.returnUrl !== data.previewUrl ) { #>
        <a class=\"button customize-notice-go-back-button\" href=\"{{ data.returnUrl }}\">""")
        _e("Go back")
        php_print("</a>\n                       <# } #>\n                       <a class=\"button customize-notice-preview-button\" href=\"{{ data.frontendPreviewUrl }}\">")
        _e("Preview")
        php_print("</a>\n                       <# if ( data.allowOverride ) { #>\n                         <button class=\"button button-primary wp-tab-last customize-notice-take-over-button\">")
        _e("Take over")
        php_print("""</button>
        <# } #>
        </p>
        </div>
        </li>
        </script>
        <script type=\"text/html\" id=\"tmpl-customize-code-editor-lint-error-notification\">
        <li class=\"notice notice-{{ data.type || 'info' }} {{ data.alt ? 'notice-alt' : '' }} {{ data.dismissible ? 'is-dismissible' : '' }} {{ data.containerClasses || '' }}\" data-code=\"{{ data.code }}\" data-type=\"{{ data.type }}\">
        <div class=\"notification-message\">{{{ data.message || data.code }}}</div>
        <p>
        <# var elementId = 'el-' + String( Math.random() ); #>
        <input id=\"{{ elementId }}\" type=\"checkbox\">
        <label for=\"{{ elementId }}\">""")
        _e("Update anyway, even though it might break your site?")
        php_print("""</label>
        </p>
        </li>
        </script>
        """)
        pass
        php_print("""       <script type=\"text/html\" id=\"tmpl-customize-control-notifications\">
        <ul>
        <# _.each( data.notifications, function( notification ) { #>
        <li class=\"notice notice-{{ notification.type || 'info' }} {{ data.altNotice ? 'notice-alt' : '' }}\" data-code=\"{{ notification.code }}\" data-type=\"{{ notification.type }}\">{{{ notification.message || notification.code }}}</li>
        <# } ); #>
        </ul>
        </script>
        <script type=\"text/html\" id=\"tmpl-customize-preview-link-control\" >
        <# var elementPrefix = _.uniqueId( 'el' ) + '-' #>
        <p class=\"customize-control-title\">
        """)
        esc_html_e("Share Preview Link")
        php_print("         </p>\n          <p class=\"description customize-control-description\">")
        esc_html_e("See how changes would look live on your website, and share the preview with people who can't access the Customizer.")
        php_print("""</p>
        <div class=\"customize-control-notifications-container\"></div>
        <div class=\"preview-link-wrapper\">
        <label for=\"{{ elementPrefix }}customize-preview-link-input\" class=\"screen-reader-text\">""")
        esc_html_e("Preview Link")
        php_print("""</label>
        <a href=\"\" target=\"\">
        <span class=\"preview-control-element\" data-component=\"url\"></span>
        <span class=\"screen-reader-text\">""")
        _e("(opens in a new tab)")
        php_print("""</span>
        </a>
        <input id=\"{{ elementPrefix }}customize-preview-link-input\" readonly tabindex=\"-1\" class=\"preview-control-element\" data-component=\"input\">
        <button class=\"customize-copy-preview-link preview-control-element button button-secondary\" data-component=\"button\" data-copy-text=\"""")
        esc_attr_e("Copy")
        php_print("\" data-copied-text=\"")
        esc_attr_e("Copied")
        php_print("\" >")
        esc_html_e("Copy")
        php_print("""</button>
        </div>
        </script>
        <script type=\"text/html\" id=\"tmpl-customize-selected-changeset-status-control\">
        <# var inputId = _.uniqueId( 'customize-selected-changeset-status-control-input-' ); #>
        <# var descriptionId = _.uniqueId( 'customize-selected-changeset-status-control-description-' ); #>
        <# if ( data.label ) { #>
        <label for=\"{{ inputId }}\" class=\"customize-control-title\">{{ data.label }}</label>
        <# } #>
        <# if ( data.description ) { #>
        <span id=\"{{ descriptionId }}\" class=\"description customize-control-description\">{{{ data.description }}}</span>
        <# } #>
        <# _.each( data.choices, function( choice ) { #>
        <# var choiceId = inputId + '-' + choice.status; #>
        <span class=\"customize-inside-control-row\">
        <input id=\"{{ choiceId }}\" type=\"radio\" value=\"{{ choice.status }}\" name=\"{{ inputId }}\" data-customize-setting-key-link=\"default\">
        <label for=\"{{ choiceId }}\">{{ choice.label }}</label>
        </span>
        <# } ); #>
        </script>
        """)
    # end def render_control_templates
    #// 
    #// Helper function to compare two objects by priority, ensuring sort stability via instance_number.
    #// 
    #// @since 3.4.0
    #// @deprecated 4.7.0 Use wp_list_sort()
    #// 
    #// @param WP_Customize_Panel|WP_Customize_Section|WP_Customize_Control $a Object A.
    #// @param WP_Customize_Panel|WP_Customize_Section|WP_Customize_Control $b Object B.
    #// @return int
    #//
    def _cmp_priority(self, a=None, b=None):
        
        _deprecated_function(__METHOD__, "4.7.0", "wp_list_sort")
        if a.priority == b.priority:
            return a.instance_number - b.instance_number
        else:
            return a.priority - b.priority
        # end if
    # end def _cmp_priority
    #// 
    #// Prepare panels, sections, and controls.
    #// 
    #// For each, check if required related components exist,
    #// whether the user has the necessary capabilities,
    #// and sort by priority.
    #// 
    #// @since 3.4.0
    #//
    def prepare_controls(self):
        
        controls = Array()
        self.controls = wp_list_sort(self.controls, Array({"priority": "ASC", "instance_number": "ASC"}), "ASC", True)
        for id,control in self.controls:
            if (not (php_isset(lambda : self.sections[control.section]))) or (not control.check_capabilities()):
                continue
            # end if
            self.sections[control.section].controls[-1] = control
            controls[id] = control
        # end for
        self.controls = controls
        #// Prepare sections.
        self.sections = wp_list_sort(self.sections, Array({"priority": "ASC", "instance_number": "ASC"}), "ASC", True)
        sections = Array()
        for section in self.sections:
            if (not section.check_capabilities()):
                continue
            # end if
            section.controls = wp_list_sort(section.controls, Array({"priority": "ASC", "instance_number": "ASC"}))
            if (not section.panel):
                #// Top-level section.
                sections[section.id] = section
            else:
                #// This section belongs to a panel.
                if (php_isset(lambda : self.panels[section.panel])):
                    self.panels[section.panel].sections[section.id] = section
                # end if
            # end if
        # end for
        self.sections = sections
        #// Prepare panels.
        self.panels = wp_list_sort(self.panels, Array({"priority": "ASC", "instance_number": "ASC"}), "ASC", True)
        panels = Array()
        for panel in self.panels:
            if (not panel.check_capabilities()):
                continue
            # end if
            panel.sections = wp_list_sort(panel.sections, Array({"priority": "ASC", "instance_number": "ASC"}), "ASC", True)
            panels[panel.id] = panel
        # end for
        self.panels = panels
        #// Sort panels and top-level sections together.
        self.containers = php_array_merge(self.panels, self.sections)
        self.containers = wp_list_sort(self.containers, Array({"priority": "ASC", "instance_number": "ASC"}), "ASC", True)
    # end def prepare_controls
    #// 
    #// Enqueue scripts for customize controls.
    #// 
    #// @since 3.4.0
    #//
    def enqueue_control_scripts(self):
        
        for control in self.controls:
            control.enqueue()
        # end for
        if (not is_multisite()) and current_user_can("install_themes") or current_user_can("update_themes") or current_user_can("delete_themes"):
            wp_enqueue_script("updates")
            wp_localize_script("updates", "_wpUpdatesItemCounts", Array({"totals": wp_get_update_data()}))
        # end if
    # end def enqueue_control_scripts
    #// 
    #// Determine whether the user agent is iOS.
    #// 
    #// @since 4.4.0
    #// 
    #// @return bool Whether the user agent is iOS.
    #//
    def is_ios(self):
        
        return wp_is_mobile() and php_preg_match("/iPad|iPod|iPhone/", PHP_SERVER["HTTP_USER_AGENT"])
    # end def is_ios
    #// 
    #// Get the template string for the Customizer pane document title.
    #// 
    #// @since 4.4.0
    #// 
    #// @return string The template string for the document title.
    #//
    def get_document_title_template(self):
        
        if self.is_theme_active():
            #// translators: %s: Document title from the preview.
            document_title_tmpl = __("Customize: %s")
        else:
            #// translators: %s: Document title from the preview.
            document_title_tmpl = __("Live Preview: %s")
        # end if
        document_title_tmpl = html_entity_decode(document_title_tmpl, ENT_QUOTES, "UTF-8")
        #// Because exported to JS and assigned to document.title.
        return document_title_tmpl
    # end def get_document_title_template
    #// 
    #// Set the initial URL to be previewed.
    #// 
    #// URL is validated.
    #// 
    #// @since 4.4.0
    #// 
    #// @param string $preview_url URL to be previewed.
    #//
    def set_preview_url(self, preview_url=None):
        
        preview_url = esc_url_raw(preview_url)
        self.preview_url = wp_validate_redirect(preview_url, home_url("/"))
    # end def set_preview_url
    #// 
    #// Get the initial URL to be previewed.
    #// 
    #// @since 4.4.0
    #// 
    #// @return string URL being previewed.
    #//
    def get_preview_url(self):
        
        if php_empty(lambda : self.preview_url):
            preview_url = home_url("/")
        else:
            preview_url = self.preview_url
        # end if
        return preview_url
    # end def get_preview_url
    #// 
    #// Determines whether the admin and the frontend are on different domains.
    #// 
    #// @since 4.7.0
    #// 
    #// @return bool Whether cross-domain.
    #//
    def is_cross_domain(self):
        
        admin_origin = wp_parse_url(admin_url())
        home_origin = wp_parse_url(home_url())
        cross_domain = php_strtolower(admin_origin["host"]) != php_strtolower(home_origin["host"])
        return cross_domain
    # end def is_cross_domain
    #// 
    #// Get URLs allowed to be previewed.
    #// 
    #// If the front end and the admin are served from the same domain, load the
    #// preview over ssl if the Customizer is being loaded over ssl. This avoids
    #// insecure content warnings. This is not attempted if the admin and front end
    #// are on different domains to avoid the case where the front end doesn't have
    #// ssl certs. Domain mapping plugins can allow other urls in these conditions
    #// using the customize_allowed_urls filter.
    #// 
    #// @since 4.7.0
    #// 
    #// @return array Allowed URLs.
    #//
    def get_allowed_urls(self):
        
        allowed_urls = Array(home_url("/"))
        if is_ssl() and (not self.is_cross_domain()):
            allowed_urls[-1] = home_url("/", "https")
        # end if
        #// 
        #// Filters the list of URLs allowed to be clicked and followed in the Customizer preview.
        #// 
        #// @since 3.4.0
        #// 
        #// @param string[] $allowed_urls An array of allowed URLs.
        #//
        allowed_urls = array_unique(apply_filters("customize_allowed_urls", allowed_urls))
        return allowed_urls
    # end def get_allowed_urls
    #// 
    #// Get messenger channel.
    #// 
    #// @since 4.7.0
    #// 
    #// @return string Messenger channel.
    #//
    def get_messenger_channel(self):
        
        return self.messenger_channel
    # end def get_messenger_channel
    #// 
    #// Set URL to link the user to when closing the Customizer.
    #// 
    #// URL is validated.
    #// 
    #// @since 4.4.0
    #// 
    #// @param string $return_url URL for return link.
    #//
    def set_return_url(self, return_url=None):
        
        return_url = esc_url_raw(return_url)
        return_url = remove_query_arg(wp_removable_query_args(), return_url)
        return_url = wp_validate_redirect(return_url)
        self.return_url = return_url
    # end def set_return_url
    #// 
    #// Get URL to link the user to when closing the Customizer.
    #// 
    #// @since 4.4.0
    #// 
    #// @global array $_registered_pages
    #// 
    #// @return string URL for link to close Customizer.
    #//
    def get_return_url(self):
        
        global _registered_pages
        php_check_if_defined("_registered_pages")
        referer = wp_get_referer()
        excluded_referer_basenames = Array("customize.php", "wp-login.php")
        if self.return_url:
            return_url = self.return_url
        elif referer and (not php_in_array(wp_basename(php_parse_url(referer, PHP_URL_PATH)), excluded_referer_basenames, True)):
            return_url = referer
        elif self.preview_url:
            return_url = self.preview_url
        else:
            return_url = home_url("/")
        # end if
        return_url_basename = wp_basename(php_parse_url(self.return_url, PHP_URL_PATH))
        return_url_query = php_parse_url(self.return_url, PHP_URL_QUERY)
        if "themes.php" == return_url_basename and return_url_query:
            parse_str(return_url_query, query_vars)
            #// 
            #// If the return URL is a page added by a theme to the Appearance menu via add_submenu_page(),
            #// verify that belongs to the active theme, otherwise fall back to the Themes screen.
            #//
            if (php_isset(lambda : query_vars["page"])) and (not (php_isset(lambda : _registered_pages[str("appearance_page_") + str(query_vars["page"])]))):
                return_url = admin_url("themes.php")
            # end if
        # end if
        return return_url
    # end def get_return_url
    #// 
    #// Set the autofocused constructs.
    #// 
    #// @since 4.4.0
    #// 
    #// @param array $autofocus {
    #// Mapping of 'panel', 'section', 'control' to the ID which should be autofocused.
    #// 
    #// @type string [$control]  ID for control to be autofocused.
    #// @type string [$section]  ID for section to be autofocused.
    #// @type string [$panel]    ID for panel to be autofocused.
    #// }
    #//
    def set_autofocus(self, autofocus=None):
        
        self.autofocus = php_array_filter(wp_array_slice_assoc(autofocus, Array("panel", "section", "control")), "is_string")
    # end def set_autofocus
    #// 
    #// Get the autofocused constructs.
    #// 
    #// @since 4.4.0
    #// 
    #// @return array {
    #// Mapping of 'panel', 'section', 'control' to the ID which should be autofocused.
    #// 
    #// @type string [$control]  ID for control to be autofocused.
    #// @type string [$section]  ID for section to be autofocused.
    #// @type string [$panel]    ID for panel to be autofocused.
    #// }
    #//
    def get_autofocus(self):
        
        return self.autofocus
    # end def get_autofocus
    #// 
    #// Get nonces for the Customizer.
    #// 
    #// @since 4.5.0
    #// 
    #// @return array Nonces.
    #//
    def get_nonces(self):
        
        nonces = Array({"save": wp_create_nonce("save-customize_" + self.get_stylesheet()), "preview": wp_create_nonce("preview-customize_" + self.get_stylesheet()), "switch_themes": wp_create_nonce("switch_themes"), "dismiss_autosave_or_lock": wp_create_nonce("customize_dismiss_autosave_or_lock"), "override_lock": wp_create_nonce("customize_override_changeset_lock"), "trash": wp_create_nonce("trash_customize_changeset")})
        #// 
        #// Filters nonces for Customizer.
        #// 
        #// @since 4.2.0
        #// 
        #// @param string[]             $nonces Array of refreshed nonces for save and
        #// preview actions.
        #// @param WP_Customize_Manager $this   WP_Customize_Manager instance.
        #//
        nonces = apply_filters("customize_refresh_nonces", nonces, self)
        return nonces
    # end def get_nonces
    #// 
    #// Print JavaScript settings for parent window.
    #// 
    #// @since 4.4.0
    #//
    def customize_pane_settings(self):
        
        login_url = add_query_arg(Array({"interim-login": 1, "customize-login": 1}), wp_login_url())
        #// Ensure dirty flags are set for modified settings.
        for setting_id in php_array_keys(self.unsanitized_post_values()):
            setting = self.get_setting(setting_id)
            if setting:
                setting.dirty = True
            # end if
        # end for
        autosave_revision_post = None
        autosave_autodraft_post = None
        changeset_post_id = self.changeset_post_id()
        if (not self.saved_starter_content_changeset) and (not self.autosaved()):
            if changeset_post_id:
                if is_user_logged_in():
                    autosave_revision_post = wp_get_post_autosave(changeset_post_id, get_current_user_id())
                # end if
            else:
                autosave_autodraft_posts = self.get_changeset_posts(Array({"posts_per_page": 1, "post_status": "auto-draft", "exclude_restore_dismissed": True}))
                if (not php_empty(lambda : autosave_autodraft_posts)):
                    autosave_autodraft_post = php_array_shift(autosave_autodraft_posts)
                # end if
            # end if
        # end if
        current_user_can_publish = current_user_can(get_post_type_object("customize_changeset").cap.publish_posts)
        #// @todo Include all of the status labels here from script-loader.php, and then allow it to be filtered.
        status_choices = Array()
        if current_user_can_publish:
            status_choices[-1] = Array({"status": "publish", "label": __("Publish")})
        # end if
        status_choices[-1] = Array({"status": "draft", "label": __("Save Draft")})
        if current_user_can_publish:
            status_choices[-1] = Array({"status": "future", "label": _x("Schedule", "customizer changeset action/button label")})
        # end if
        #// Prepare Customizer settings to pass to JavaScript.
        changeset_post = None
        if changeset_post_id:
            changeset_post = get_post(changeset_post_id)
        # end if
        #// Determine initial date to be at present or future, not past.
        current_time = current_time("mysql", False)
        initial_date = current_time
        if changeset_post:
            initial_date = get_the_time("Y-m-d H:i:s", changeset_post.ID)
            if initial_date < current_time:
                initial_date = current_time
            # end if
        # end if
        lock_user_id = False
        if self.changeset_post_id():
            lock_user_id = wp_check_post_lock(self.changeset_post_id())
        # end if
        settings = Array({"changeset": Array({"uuid": self.changeset_uuid(), "branching": self.branching(), "autosaved": self.autosaved(), "hasAutosaveRevision": (not php_empty(lambda : autosave_revision_post)), "latestAutoDraftUuid": autosave_autodraft_post.post_name if autosave_autodraft_post else None, "status": changeset_post.post_status if changeset_post else "", "currentUserCanPublish": current_user_can_publish, "publishDate": initial_date, "statusChoices": status_choices, "lockUser": self.get_lock_user_data(lock_user_id) if lock_user_id else None})}, {"initialServerDate": current_time, "dateFormat": get_option("date_format"), "timeFormat": get_option("time_format"), "initialServerTimestamp": floor(php_microtime(True) * 1000), "initialClientTimestamp": -1, "timeouts": Array({"windowRefresh": 250, "changesetAutoSave": AUTOSAVE_INTERVAL * 1000, "keepAliveCheck": 2500, "reflowPaneContents": 100, "previewFrameSensitivity": 2000})}, {"theme": Array({"stylesheet": self.get_stylesheet(), "active": self.is_theme_active(), "_canInstall": current_user_can("install_themes")})}, {"url": Array({"preview": esc_url_raw(self.get_preview_url()), "return": esc_url_raw(self.get_return_url()), "parent": esc_url_raw(admin_url()), "activated": esc_url_raw(home_url("/")), "ajax": esc_url_raw(admin_url("admin-ajax.php", "relative")), "allowed": php_array_map("esc_url_raw", self.get_allowed_urls()), "isCrossDomain": self.is_cross_domain(), "home": esc_url_raw(home_url("/")), "login": esc_url_raw(login_url)})}, {"browser": Array({"mobile": wp_is_mobile(), "ios": self.is_ios()})}, {"panels": Array(), "sections": Array(), "nonce": self.get_nonces(), "autofocus": self.get_autofocus(), "documentTitleTmpl": self.get_document_title_template(), "previewableDevices": self.get_previewable_devices(), "l10n": Array({"confirmDeleteTheme": __("Are you sure you want to delete this theme?"), "themeSearchResults": __("%d themes found"), "announceThemeCount": __("Displaying %d themes"), "announceThemeDetails": __("Showing details for theme: %s")})})
        #// Temporarily disable installation in Customizer. See #42184.
        filesystem_method = get_filesystem_method()
        ob_start()
        filesystem_credentials_are_stored = request_filesystem_credentials(self_admin_url())
        ob_end_clean()
        if "direct" != filesystem_method and (not filesystem_credentials_are_stored):
            settings["theme"]["_filesystemCredentialsNeeded"] = True
        # end if
        #// Prepare Customize Section objects to pass to JavaScript.
        for id,section in self.sections():
            if section.check_capabilities():
                settings["sections"][id] = section.json()
            # end if
        # end for
        #// Prepare Customize Panel objects to pass to JavaScript.
        for panel_id,panel in self.panels():
            if panel.check_capabilities():
                settings["panels"][panel_id] = panel.json()
                for section_id,section in panel.sections:
                    if section.check_capabilities():
                        settings["sections"][section_id] = section.json()
                    # end if
                # end for
            # end if
        # end for
        php_print("     <script type=\"text/javascript\">\n         var _wpCustomizeSettings = ")
        php_print(wp_json_encode(settings))
        php_print(""";
        _wpCustomizeSettings.initialClientTimestamp = _.now();
        _wpCustomizeSettings.controls = {};
        _wpCustomizeSettings.settings = {};
        """)
        #// Serialize settings one by one to improve memory usage.
        php_print("(function ( s ){\n")
        for setting in self.settings():
            if setting.check_capabilities():
                printf("s[%s] = %s;\n", wp_json_encode(setting.id), wp_json_encode(setting.json()))
            # end if
        # end for
        php_print("})( _wpCustomizeSettings.settings );\n")
        #// Serialize controls one by one to improve memory usage.
        php_print("(function ( c ){\n")
        for control in self.controls():
            if control.check_capabilities():
                printf("c[%s] = %s;\n", wp_json_encode(control.id), wp_json_encode(control.json()))
            # end if
        # end for
        php_print("})( _wpCustomizeSettings.controls );\n")
        php_print("     </script>\n     ")
    # end def customize_pane_settings
    #// 
    #// Returns a list of devices to allow previewing.
    #// 
    #// @since 4.5.0
    #// 
    #// @return array List of devices with labels and default setting.
    #//
    def get_previewable_devices(self):
        
        devices = Array({"desktop": Array({"label": __("Enter desktop preview mode"), "default": True})}, {"tablet": Array({"label": __("Enter tablet preview mode")})}, {"mobile": Array({"label": __("Enter mobile preview mode")})})
        #// 
        #// Filters the available devices to allow previewing in the Customizer.
        #// 
        #// @since 4.5.0
        #// 
        #// @see WP_Customize_Manager::get_previewable_devices()
        #// 
        #// @param array $devices List of devices with labels and default setting.
        #//
        devices = apply_filters("customize_previewable_devices", devices)
        return devices
    # end def get_previewable_devices
    #// 
    #// Register some default controls.
    #// 
    #// @since 3.4.0
    #//
    def register_controls(self):
        
        #// Themes (controls are loaded via ajax)
        self.add_panel(php_new_class("WP_Customize_Themes_Panel", lambda : WP_Customize_Themes_Panel(self, "themes", Array({"title": self.theme().display("Name"), "description": "<p>" + __("Looking for a theme? You can search or browse the WordPress.org theme directory, install and preview themes, then activate them right here.") + "</p>" + "<p>" + __("While previewing a new theme, you can continue to tailor things like widgets and menus, and explore theme-specific options.") + "</p>", "capability": "switch_themes", "priority": 0}))))
        self.add_section(php_new_class("WP_Customize_Themes_Section", lambda : WP_Customize_Themes_Section(self, "installed_themes", Array({"title": __("Installed themes"), "action": "installed", "capability": "switch_themes", "panel": "themes", "priority": 0}))))
        if (not is_multisite()):
            self.add_section(php_new_class("WP_Customize_Themes_Section", lambda : WP_Customize_Themes_Section(self, "wporg_themes", Array({"title": __("WordPress.org themes"), "action": "wporg", "filter_type": "remote", "capability": "install_themes", "panel": "themes", "priority": 5}))))
        # end if
        #// Themes Setting (unused - the theme is considerably more fundamental to the Customizer experience).
        self.add_setting(php_new_class("WP_Customize_Filter_Setting", lambda : WP_Customize_Filter_Setting(self, "active_theme", Array({"capability": "switch_themes"}))))
        #// Site Identity
        self.add_section("title_tagline", Array({"title": __("Site Identity"), "priority": 20}))
        self.add_setting("blogname", Array({"default": get_option("blogname"), "type": "option", "capability": "manage_options"}))
        self.add_control("blogname", Array({"label": __("Site Title"), "section": "title_tagline"}))
        self.add_setting("blogdescription", Array({"default": get_option("blogdescription"), "type": "option", "capability": "manage_options"}))
        self.add_control("blogdescription", Array({"label": __("Tagline"), "section": "title_tagline"}))
        #// Add a setting to hide header text if the theme doesn't support custom headers.
        if (not current_theme_supports("custom-header", "header-text")):
            self.add_setting("header_text", Array({"theme_supports": Array("custom-logo", "header-text"), "default": 1, "sanitize_callback": "absint"}))
            self.add_control("header_text", Array({"label": __("Display Site Title and Tagline"), "section": "title_tagline", "settings": "header_text", "type": "checkbox"}))
        # end if
        self.add_setting("site_icon", Array({"type": "option", "capability": "manage_options", "transport": "postMessage"}))
        self.add_control(php_new_class("WP_Customize_Site_Icon_Control", lambda : WP_Customize_Site_Icon_Control(self, "site_icon", Array({"label": __("Site Icon"), "description": php_sprintf("<p>" + __("Site Icons are what you see in browser tabs, bookmark bars, and within the WordPress mobile apps. Upload one here!") + "</p>" + "<p>" + __("Site Icons should be square and at least %s pixels.") + "</p>", "<strong>512 &times; 512</strong>"), "section": "title_tagline", "priority": 60, "height": 512, "width": 512}))))
        self.add_setting("custom_logo", Array({"theme_supports": Array("custom-logo"), "transport": "postMessage"}))
        custom_logo_args = get_theme_support("custom-logo")
        self.add_control(php_new_class("WP_Customize_Cropped_Image_Control", lambda : WP_Customize_Cropped_Image_Control(self, "custom_logo", Array({"label": __("Logo"), "section": "title_tagline", "priority": 8, "height": custom_logo_args[0]["height"] if (php_isset(lambda : custom_logo_args[0]["height"])) else None, "width": custom_logo_args[0]["width"] if (php_isset(lambda : custom_logo_args[0]["width"])) else None, "flex_height": custom_logo_args[0]["flex-height"] if (php_isset(lambda : custom_logo_args[0]["flex-height"])) else None, "flex_width": custom_logo_args[0]["flex-width"] if (php_isset(lambda : custom_logo_args[0]["flex-width"])) else None, "button_labels": Array({"select": __("Select logo"), "change": __("Change logo"), "remove": __("Remove"), "default": __("Default"), "placeholder": __("No logo selected"), "frame_title": __("Select logo"), "frame_button": __("Choose logo")})}))))
        self.selective_refresh.add_partial("custom_logo", Array({"settings": Array("custom_logo"), "selector": ".custom-logo-link", "render_callback": Array(self, "_render_custom_logo_partial"), "container_inclusive": True}))
        #// Colors
        self.add_section("colors", Array({"title": __("Colors"), "priority": 40}))
        self.add_setting("header_textcolor", Array({"theme_supports": Array("custom-header", "header-text"), "default": get_theme_support("custom-header", "default-text-color"), "sanitize_callback": Array(self, "_sanitize_header_textcolor"), "sanitize_js_callback": "maybe_hash_hex_color"}))
        #// Input type: checkbox.
        #// With custom value.
        self.add_control("display_header_text", Array({"settings": "header_textcolor", "label": __("Display Site Title and Tagline"), "section": "title_tagline", "type": "checkbox", "priority": 40}))
        self.add_control(php_new_class("WP_Customize_Color_Control", lambda : WP_Customize_Color_Control(self, "header_textcolor", Array({"label": __("Header Text Color"), "section": "colors"}))))
        #// Input type: color.
        #// With sanitize_callback.
        self.add_setting("background_color", Array({"default": get_theme_support("custom-background", "default-color"), "theme_supports": "custom-background", "sanitize_callback": "sanitize_hex_color_no_hash", "sanitize_js_callback": "maybe_hash_hex_color"}))
        self.add_control(php_new_class("WP_Customize_Color_Control", lambda : WP_Customize_Color_Control(self, "background_color", Array({"label": __("Background Color"), "section": "colors"}))))
        #// Custom Header
        if current_theme_supports("custom-header", "video"):
            title = __("Header Media")
            description = "<p>" + __("If you add a video, the image will be used as a fallback while the video loads.") + "</p>"
            width = absint(get_theme_support("custom-header", "width"))
            height = absint(get_theme_support("custom-header", "height"))
            if width and height:
                control_description = php_sprintf(__("Upload your video in %1$s format and minimize its file size for best results. Your theme recommends dimensions of %2$s pixels."), "<code>.mp4</code>", php_sprintf("<strong>%s &times; %s</strong>", width, height))
            elif width:
                control_description = php_sprintf(__("Upload your video in %1$s format and minimize its file size for best results. Your theme recommends a width of %2$s pixels."), "<code>.mp4</code>", php_sprintf("<strong>%s</strong>", width))
            else:
                control_description = php_sprintf(__("Upload your video in %1$s format and minimize its file size for best results. Your theme recommends a height of %2$s pixels."), "<code>.mp4</code>", php_sprintf("<strong>%s</strong>", height))
            # end if
        else:
            title = __("Header Image")
            description = ""
            control_description = ""
        # end if
        self.add_section("header_image", Array({"title": title, "description": description, "theme_supports": "custom-header", "priority": 60}))
        self.add_setting("header_video", Array({"theme_supports": Array("custom-header", "video"), "transport": "postMessage", "sanitize_callback": "absint", "validate_callback": Array(self, "_validate_header_video")}))
        self.add_setting("external_header_video", Array({"theme_supports": Array("custom-header", "video"), "transport": "postMessage", "sanitize_callback": Array(self, "_sanitize_external_header_video"), "validate_callback": Array(self, "_validate_external_header_video")}))
        self.add_setting(php_new_class("WP_Customize_Filter_Setting", lambda : WP_Customize_Filter_Setting(self, "header_image", Array({"default": php_sprintf(get_theme_support("custom-header", "default-image"), get_template_directory_uri(), get_stylesheet_directory_uri()), "theme_supports": "custom-header"}))))
        self.add_setting(php_new_class("WP_Customize_Header_Image_Setting", lambda : WP_Customize_Header_Image_Setting(self, "header_image_data", Array({"theme_supports": "custom-header"}))))
        #// 
        #// Switch image settings to postMessage when video support is enabled since
        #// it entails that the_custom_header_markup() will be used, and thus selective
        #// refresh can be utilized.
        #//
        if current_theme_supports("custom-header", "video"):
            self.get_setting("header_image").transport = "postMessage"
            self.get_setting("header_image_data").transport = "postMessage"
        # end if
        self.add_control(php_new_class("WP_Customize_Media_Control", lambda : WP_Customize_Media_Control(self, "header_video", Array({"theme_supports": Array("custom-header", "video"), "label": __("Header Video"), "description": control_description, "section": "header_image", "mime_type": "video", "active_callback": "is_header_video_active"}))))
        self.add_control("external_header_video", Array({"theme_supports": Array("custom-header", "video"), "type": "url", "description": __("Or, enter a YouTube URL:"), "section": "header_image", "active_callback": "is_header_video_active"}))
        self.add_control(php_new_class("WP_Customize_Header_Image_Control", lambda : WP_Customize_Header_Image_Control(self)))
        self.selective_refresh.add_partial("custom_header", Array({"selector": "#wp-custom-header", "render_callback": "the_custom_header_markup", "settings": Array("header_video", "external_header_video", "header_image"), "container_inclusive": True}))
        #// Custom Background
        self.add_section("background_image", Array({"title": __("Background Image"), "theme_supports": "custom-background", "priority": 80}))
        self.add_setting("background_image", Array({"default": get_theme_support("custom-background", "default-image"), "theme_supports": "custom-background", "sanitize_callback": Array(self, "_sanitize_background_setting")}))
        self.add_setting(php_new_class("WP_Customize_Background_Image_Setting", lambda : WP_Customize_Background_Image_Setting(self, "background_image_thumb", Array({"theme_supports": "custom-background", "sanitize_callback": Array(self, "_sanitize_background_setting")}))))
        self.add_control(php_new_class("WP_Customize_Background_Image_Control", lambda : WP_Customize_Background_Image_Control(self)))
        self.add_setting("background_preset", Array({"default": get_theme_support("custom-background", "default-preset"), "theme_supports": "custom-background", "sanitize_callback": Array(self, "_sanitize_background_setting")}))
        self.add_control("background_preset", Array({"label": _x("Preset", "Background Preset"), "section": "background_image", "type": "select", "choices": Array({"default": _x("Default", "Default Preset"), "fill": __("Fill Screen"), "fit": __("Fit to Screen"), "repeat": _x("Repeat", "Repeat Image"), "custom": _x("Custom", "Custom Preset")})}))
        self.add_setting("background_position_x", Array({"default": get_theme_support("custom-background", "default-position-x"), "theme_supports": "custom-background", "sanitize_callback": Array(self, "_sanitize_background_setting")}))
        self.add_setting("background_position_y", Array({"default": get_theme_support("custom-background", "default-position-y"), "theme_supports": "custom-background", "sanitize_callback": Array(self, "_sanitize_background_setting")}))
        self.add_control(php_new_class("WP_Customize_Background_Position_Control", lambda : WP_Customize_Background_Position_Control(self, "background_position", Array({"label": __("Image Position"), "section": "background_image", "settings": Array({"x": "background_position_x", "y": "background_position_y"})}))))
        self.add_setting("background_size", Array({"default": get_theme_support("custom-background", "default-size"), "theme_supports": "custom-background", "sanitize_callback": Array(self, "_sanitize_background_setting")}))
        self.add_control("background_size", Array({"label": __("Image Size"), "section": "background_image", "type": "select", "choices": Array({"auto": _x("Original", "Original Size"), "contain": __("Fit to Screen"), "cover": __("Fill Screen")})}))
        self.add_setting("background_repeat", Array({"default": get_theme_support("custom-background", "default-repeat"), "sanitize_callback": Array(self, "_sanitize_background_setting"), "theme_supports": "custom-background"}))
        self.add_control("background_repeat", Array({"label": __("Repeat Background Image"), "section": "background_image", "type": "checkbox"}))
        self.add_setting("background_attachment", Array({"default": get_theme_support("custom-background", "default-attachment"), "sanitize_callback": Array(self, "_sanitize_background_setting"), "theme_supports": "custom-background"}))
        self.add_control("background_attachment", Array({"label": __("Scroll with Page"), "section": "background_image", "type": "checkbox"}))
        #// If the theme is using the default background callback, we can update
        #// the background CSS using postMessage.
        if get_theme_support("custom-background", "wp-head-callback") == "_custom_background_cb":
            for prop in Array("color", "image", "preset", "position_x", "position_y", "size", "repeat", "attachment"):
                self.get_setting("background_" + prop).transport = "postMessage"
            # end for
        # end if
        #// 
        #// Static Front Page
        #// See also https://core.trac.wordpress.org/ticket/19627 which introduces the static-front-page theme_support.
        #// The following replicates behavior from options-reading.php.
        #//
        self.add_section("static_front_page", Array({"title": __("Homepage Settings"), "priority": 120, "description": __("You can choose what&#8217;s displayed on the homepage of your site. It can be posts in reverse chronological order (classic blog), or a fixed/static page. To set a static homepage, you first need to create two Pages. One will become the homepage, and the other will be where your posts are displayed."), "active_callback": Array(self, "has_published_pages")}))
        self.add_setting("show_on_front", Array({"default": get_option("show_on_front"), "capability": "manage_options", "type": "option"}))
        self.add_control("show_on_front", Array({"label": __("Your homepage displays"), "section": "static_front_page", "type": "radio", "choices": Array({"posts": __("Your latest posts"), "page": __("A static page")})}))
        self.add_setting("page_on_front", Array({"type": "option", "capability": "manage_options"}))
        self.add_control("page_on_front", Array({"label": __("Homepage"), "section": "static_front_page", "type": "dropdown-pages", "allow_addition": True}))
        self.add_setting("page_for_posts", Array({"type": "option", "capability": "manage_options"}))
        self.add_control("page_for_posts", Array({"label": __("Posts page"), "section": "static_front_page", "type": "dropdown-pages", "allow_addition": True}))
        #// Custom CSS
        section_description = "<p>"
        section_description += __("Add your own CSS code here to customize the appearance and layout of your site.")
        section_description += php_sprintf(" <a href=\"%1$s\" class=\"external-link\" target=\"_blank\">%2$s<span class=\"screen-reader-text\"> %3$s</span></a>", esc_url(__("https://codex.wordpress.org/CSS")), __("Learn more about CSS"), __("(opens in a new tab)"))
        section_description += "</p>"
        section_description += "<p id=\"editor-keyboard-trap-help-1\">" + __("When using a keyboard to navigate:") + "</p>"
        section_description += "<ul>"
        section_description += "<li id=\"editor-keyboard-trap-help-2\">" + __("In the editing area, the Tab key enters a tab character.") + "</li>"
        section_description += "<li id=\"editor-keyboard-trap-help-3\">" + __("To move away from this area, press the Esc key followed by the Tab key.") + "</li>"
        section_description += "<li id=\"editor-keyboard-trap-help-4\">" + __("Screen reader users: when in forms mode, you may need to press the Esc key twice.") + "</li>"
        section_description += "</ul>"
        if "false" != wp_get_current_user().syntax_highlighting:
            section_description += "<p>"
            section_description += php_sprintf(__("The edit field automatically highlights code syntax. You can disable this in your <a href=\"%1$s\" %2$s>user profile%3$s</a> to work in plain text mode."), esc_url(get_edit_profile_url()), "class=\"external-link\" target=\"_blank\"", php_sprintf("<span class=\"screen-reader-text\"> %s</span>", __("(opens in a new tab)")))
            section_description += "</p>"
        # end if
        section_description += "<p class=\"section-description-buttons\">"
        section_description += "<button type=\"button\" class=\"button-link section-description-close\">" + __("Close") + "</button>"
        section_description += "</p>"
        self.add_section("custom_css", Array({"title": __("Additional CSS"), "priority": 200, "description_hidden": True, "description": section_description}))
        custom_css_setting = php_new_class("WP_Customize_Custom_CSS_Setting", lambda : WP_Customize_Custom_CSS_Setting(self, php_sprintf("custom_css[%s]", get_stylesheet()), Array({"capability": "edit_css", "default": ""})))
        self.add_setting(custom_css_setting)
        self.add_control(php_new_class("WP_Customize_Code_Editor_Control", lambda : WP_Customize_Code_Editor_Control(self, "custom_css", Array({"label": __("CSS code"), "section": "custom_css", "settings": Array({"default": custom_css_setting.id})}, {"code_type": "text/css", "input_attrs": Array({"aria-describedby": "editor-keyboard-trap-help-1 editor-keyboard-trap-help-2 editor-keyboard-trap-help-3 editor-keyboard-trap-help-4"})}))))
    # end def register_controls
    #// 
    #// Return whether there are published pages.
    #// 
    #// Used as active callback for static front page section and controls.
    #// 
    #// @since 4.7.0
    #// 
    #// @return bool Whether there are published (or to be published) pages.
    #//
    def has_published_pages(self):
        
        setting = self.get_setting("nav_menus_created_posts")
        if setting:
            for post_id in setting.value():
                if "page" == get_post_type(post_id):
                    return True
                # end if
            # end for
        # end if
        return 0 != php_count(get_pages())
    # end def has_published_pages
    #// 
    #// Add settings from the POST data that were not added with code, e.g. dynamically-created settings for Widgets
    #// 
    #// @since 4.2.0
    #// 
    #// @see add_dynamic_settings()
    #//
    def register_dynamic_settings(self):
        
        setting_ids = php_array_keys(self.unsanitized_post_values())
        self.add_dynamic_settings(setting_ids)
    # end def register_dynamic_settings
    #// 
    #// Load themes into the theme browsing/installation UI.
    #// 
    #// @since 4.9.0
    #//
    def handle_load_themes_request(self):
        
        check_ajax_referer("switch_themes", "nonce")
        if (not current_user_can("switch_themes")):
            wp_die(-1)
        # end if
        if php_empty(lambda : PHP_POST["theme_action"]):
            wp_send_json_error("missing_theme_action")
        # end if
        theme_action = sanitize_key(PHP_POST["theme_action"])
        themes = Array()
        args = Array()
        #// Define query filters based on user input.
        if (not php_array_key_exists("search", PHP_POST)):
            args["search"] = ""
        else:
            args["search"] = sanitize_text_field(wp_unslash(PHP_POST["search"]))
        # end if
        if (not php_array_key_exists("tags", PHP_POST)):
            args["tag"] = ""
        else:
            args["tag"] = php_array_map("sanitize_text_field", wp_unslash(PHP_POST["tags"]))
        # end if
        if (not php_array_key_exists("page", PHP_POST)):
            args["page"] = 1
        else:
            args["page"] = absint(PHP_POST["page"])
        # end if
        php_include_file(ABSPATH + "wp-admin/includes/theme.php", once=True)
        if "installed" == theme_action:
            #// Load all installed themes from wp_prepare_themes_for_js().
            themes = Array({"themes": wp_prepare_themes_for_js()})
            for theme in themes["themes"]:
                theme["type"] = "installed"
                theme["active"] = (php_isset(lambda : PHP_POST["customized_theme"])) and PHP_POST["customized_theme"] == theme["id"]
            # end for
        elif "wporg" == theme_action:
            #// Load WordPress.org themes from the .org API and normalize data to match installed theme objects.
            if (not current_user_can("install_themes")):
                wp_die(-1)
            # end if
            #// Arguments for all queries.
            wporg_args = Array({"per_page": 100, "fields": Array({"reviews_url": True})})
            args = php_array_merge(wporg_args, args)
            if "" == args["search"] and "" == args["tag"]:
                args["browse"] = "new"
                pass
            # end if
            #// Load themes from the .org API.
            themes = themes_api("query_themes", args)
            if is_wp_error(themes):
                wp_send_json_error()
            # end if
            #// This list matches the allowed tags in wp-admin/includes/theme-install.php.
            themes_allowedtags = php_array_fill_keys(Array("a", "abbr", "acronym", "code", "pre", "em", "strong", "div", "p", "ul", "ol", "li", "h1", "h2", "h3", "h4", "h5", "h6", "img"), Array())
            themes_allowedtags["a"] = php_array_fill_keys(Array("href", "title", "target"), True)
            themes_allowedtags["acronym"]["title"] = True
            themes_allowedtags["abbr"]["title"] = True
            themes_allowedtags["img"] = php_array_fill_keys(Array("src", "class", "alt"), True)
            #// Prepare a list of installed themes to check against before the loop.
            installed_themes = Array()
            wp_themes = wp_get_themes()
            for theme in wp_themes:
                installed_themes[-1] = theme.get_stylesheet()
            # end for
            update_php = network_admin_url("update.php?action=install-theme")
            #// Set up properties for themes available on WordPress.org.
            for theme in themes.themes:
                theme.install_url = add_query_arg(Array({"theme": theme.slug, "_wpnonce": wp_create_nonce("install-theme_" + theme.slug)}), update_php)
                theme.name = wp_kses(theme.name, themes_allowedtags)
                theme.version = wp_kses(theme.version, themes_allowedtags)
                theme.description = wp_kses(theme.description, themes_allowedtags)
                theme.stars = wp_star_rating(Array({"rating": theme.rating, "type": "percent", "number": theme.num_ratings, "echo": False}))
                theme.num_ratings = number_format_i18n(theme.num_ratings)
                theme.preview_url = set_url_scheme(theme.preview_url)
                #// Handle themes that are already installed as installed themes.
                if php_in_array(theme.slug, installed_themes, True):
                    theme.type = "installed"
                else:
                    theme.type = theme_action
                # end if
                #// Set active based on customized theme.
                theme.active = (php_isset(lambda : PHP_POST["customized_theme"])) and PHP_POST["customized_theme"] == theme.slug
                #// Map available theme properties to installed theme properties.
                theme.id = theme.slug
                theme.screenshot = Array(theme.screenshot_url)
                theme.authorAndUri = wp_kses(theme.author["display_name"], themes_allowedtags)
                if (php_isset(lambda : theme.parent)):
                    theme.parent = theme.parent["slug"]
                else:
                    theme.parent = False
                # end if
                theme.slug = None
                theme.screenshot_url = None
                theme.author = None
            # end for
            pass
        # end if
        #// End if().
        #// 
        #// Filters the theme data loaded in the customizer.
        #// 
        #// This allows theme data to be loading from an external source,
        #// or modification of data loaded from `wp_prepare_themes_for_js()`
        #// or WordPress.org via `themes_api()`.
        #// 
        #// @since 4.9.0
        #// 
        #// @see wp_prepare_themes_for_js()
        #// @see themes_api()
        #// @see WP_Customize_Manager::__construct()
        #// 
        #// @param array                $themes  Nested array of theme data.
        #// @param array                $args    List of arguments, such as page, search term, and tags to query for.
        #// @param WP_Customize_Manager $manager Instance of Customize manager.
        #//
        themes = apply_filters("customize_load_themes", themes, args, self)
        wp_send_json_success(themes)
    # end def handle_load_themes_request
    #// 
    #// Callback for validating the header_textcolor value.
    #// 
    #// Accepts 'blank', and otherwise uses sanitize_hex_color_no_hash().
    #// Returns default text color if hex color is empty.
    #// 
    #// @since 3.4.0
    #// 
    #// @param string $color
    #// @return mixed
    #//
    def _sanitize_header_textcolor(self, color=None):
        
        if "blank" == color:
            return "blank"
        # end if
        color = sanitize_hex_color_no_hash(color)
        if php_empty(lambda : color):
            color = get_theme_support("custom-header", "default-text-color")
        # end if
        return color
    # end def _sanitize_header_textcolor
    #// 
    #// Callback for validating a background setting value.
    #// 
    #// @since 4.7.0
    #// 
    #// @param string $value Repeat value.
    #// @param WP_Customize_Setting $setting Setting.
    #// @return string|WP_Error Background value or validation error.
    #//
    def _sanitize_background_setting(self, value=None, setting=None):
        
        if "background_repeat" == setting.id:
            if (not php_in_array(value, Array("repeat-x", "repeat-y", "repeat", "no-repeat"))):
                return php_new_class("WP_Error", lambda : WP_Error("invalid_value", __("Invalid value for background repeat.")))
            # end if
        elif "background_attachment" == setting.id:
            if (not php_in_array(value, Array("fixed", "scroll"))):
                return php_new_class("WP_Error", lambda : WP_Error("invalid_value", __("Invalid value for background attachment.")))
            # end if
        elif "background_position_x" == setting.id:
            if (not php_in_array(value, Array("left", "center", "right"), True)):
                return php_new_class("WP_Error", lambda : WP_Error("invalid_value", __("Invalid value for background position X.")))
            # end if
        elif "background_position_y" == setting.id:
            if (not php_in_array(value, Array("top", "center", "bottom"), True)):
                return php_new_class("WP_Error", lambda : WP_Error("invalid_value", __("Invalid value for background position Y.")))
            # end if
        elif "background_size" == setting.id:
            if (not php_in_array(value, Array("auto", "contain", "cover"), True)):
                return php_new_class("WP_Error", lambda : WP_Error("invalid_value", __("Invalid value for background size.")))
            # end if
        elif "background_preset" == setting.id:
            if (not php_in_array(value, Array("default", "fill", "fit", "repeat", "custom"), True)):
                return php_new_class("WP_Error", lambda : WP_Error("invalid_value", __("Invalid value for background size.")))
            # end if
        elif "background_image" == setting.id or "background_image_thumb" == setting.id:
            value = "" if php_empty(lambda : value) else esc_url_raw(value)
        else:
            return php_new_class("WP_Error", lambda : WP_Error("unrecognized_setting", __("Unrecognized background setting.")))
        # end if
        return value
    # end def _sanitize_background_setting
    #// 
    #// Export header video settings to facilitate selective refresh.
    #// 
    #// @since 4.7.0
    #// 
    #// @param array $response Response.
    #// @param WP_Customize_Selective_Refresh $selective_refresh Selective refresh component.
    #// @param array $partials Array of partials.
    #// @return array
    #//
    def export_header_video_settings(self, response=None, selective_refresh=None, partials=None):
        
        if (php_isset(lambda : partials["custom_header"])):
            response["custom_header_settings"] = get_header_video_settings()
        # end if
        return response
    # end def export_header_video_settings
    #// 
    #// Callback for validating the header_video value.
    #// 
    #// Ensures that the selected video is less than 8MB and provides an error message.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_Error $validity
    #// @param mixed $value
    #// @return mixed
    #//
    def _validate_header_video(self, validity=None, value=None):
        
        video = get_attached_file(absint(value))
        if video:
            size = filesize(video)
            if size > 8 * MB_IN_BYTES:
                validity.add("size_too_large", __("This video file is too large to use as a header video. Try a shorter video or optimize the compression settings and re-upload a file that is less than 8MB. Or, upload your video to YouTube and link it with the option below."))
            # end if
            if ".mp4" != php_substr(video, -4) and ".mov" != php_substr(video, -4):
                #// Check for .mp4 or .mov format, which (assuming h.264 encoding) are the only cross-browser-supported formats.
                validity.add("invalid_file_type", php_sprintf(__("Only %1$s or %2$s files may be used for header video. Please convert your video file and try again, or, upload your video to YouTube and link it with the option below."), "<code>.mp4</code>", "<code>.mov</code>"))
            # end if
        # end if
        return validity
    # end def _validate_header_video
    #// 
    #// Callback for validating the external_header_video value.
    #// 
    #// Ensures that the provided URL is supported.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_Error $validity
    #// @param mixed $value
    #// @return mixed
    #//
    def _validate_external_header_video(self, validity=None, value=None):
        
        video = esc_url_raw(value)
        if video:
            if (not php_preg_match("#^https?://(?:www\\.)?(?:youtube\\.com/watch|youtu\\.be/)#", video)):
                validity.add("invalid_url", __("Please enter a valid YouTube URL."))
            # end if
        # end if
        return validity
    # end def _validate_external_header_video
    #// 
    #// Callback for sanitizing the external_header_video value.
    #// 
    #// @since 4.7.1
    #// 
    #// @param string $value URL.
    #// @return string Sanitized URL.
    #//
    def _sanitize_external_header_video(self, value=None):
        
        return esc_url_raw(php_trim(value))
    # end def _sanitize_external_header_video
    #// 
    #// Callback for rendering the custom logo, used in the custom_logo partial.
    #// 
    #// This method exists because the partial object and context data are passed
    #// into a partial's render_callback so we cannot use get_custom_logo() as
    #// the render_callback directly since it expects a blog ID as the first
    #// argument. When WP no longer supports PHP 5.3, this method can be removed
    #// in favor of an anonymous function.
    #// 
    #// @see WP_Customize_Manager::register_controls()
    #// 
    #// @since 4.5.0
    #// 
    #// @return string Custom logo.
    #//
    def _render_custom_logo_partial(self):
        
        return get_custom_logo()
    # end def _render_custom_logo_partial
# end class WP_Customize_Manager
