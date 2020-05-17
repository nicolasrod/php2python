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
    #// 
    #// An instance of the theme being previewed.
    #// 
    #// @since 3.4.0
    #// @var WP_Theme
    #//
    theme = Array()
    #// 
    #// The directory name of the previously active theme (within the theme_root).
    #// 
    #// @since 3.4.0
    #// @var string
    #//
    original_stylesheet = Array()
    #// 
    #// Whether this is a Customizer pageload.
    #// 
    #// @since 3.4.0
    #// @var bool
    #//
    previewing = False
    #// 
    #// Methods and properties dealing with managing widgets in the Customizer.
    #// 
    #// @since 3.9.0
    #// @var WP_Customize_Widgets
    #//
    widgets = Array()
    #// 
    #// Methods and properties dealing with managing nav menus in the Customizer.
    #// 
    #// @since 4.3.0
    #// @var WP_Customize_Nav_Menus
    #//
    nav_menus = Array()
    #// 
    #// Methods and properties dealing with selective refresh in the Customizer preview.
    #// 
    #// @since 4.5.0
    #// @var WP_Customize_Selective_Refresh
    #//
    selective_refresh = Array()
    #// 
    #// Registered instances of WP_Customize_Setting.
    #// 
    #// @since 3.4.0
    #// @var array
    #//
    settings = Array()
    #// 
    #// Sorted top-level instances of WP_Customize_Panel and WP_Customize_Section.
    #// 
    #// @since 4.0.0
    #// @var array
    #//
    containers = Array()
    #// 
    #// Registered instances of WP_Customize_Panel.
    #// 
    #// @since 4.0.0
    #// @var array
    #//
    panels = Array()
    #// 
    #// List of core components.
    #// 
    #// @since 4.5.0
    #// @var array
    #//
    components = Array("widgets", "nav_menus")
    #// 
    #// Registered instances of WP_Customize_Section.
    #// 
    #// @since 3.4.0
    #// @var array
    #//
    sections = Array()
    #// 
    #// Registered instances of WP_Customize_Control.
    #// 
    #// @since 3.4.0
    #// @var array
    #//
    controls = Array()
    #// 
    #// Panel types that may be rendered from JS templates.
    #// 
    #// @since 4.3.0
    #// @var array
    #//
    registered_panel_types = Array()
    #// 
    #// Section types that may be rendered from JS templates.
    #// 
    #// @since 4.3.0
    #// @var array
    #//
    registered_section_types = Array()
    #// 
    #// Control types that may be rendered from JS templates.
    #// 
    #// @since 4.1.0
    #// @var array
    #//
    registered_control_types = Array()
    #// 
    #// Initial URL being previewed.
    #// 
    #// @since 4.4.0
    #// @var string
    #//
    preview_url = Array()
    #// 
    #// URL to link the user to when closing the Customizer.
    #// 
    #// @since 4.4.0
    #// @var string
    #//
    return_url = Array()
    #// 
    #// Mapping of 'panel', 'section', 'control' to the ID which should be autofocused.
    #// 
    #// @since 4.4.0
    #// @var array
    #//
    autofocus = Array()
    #// 
    #// Messenger channel.
    #// 
    #// @since 4.7.0
    #// @var string
    #//
    messenger_channel = Array()
    #// 
    #// Whether the autosave revision of the changeset should be loaded.
    #// 
    #// @since 4.9.0
    #// @var bool
    #//
    autosaved = False
    #// 
    #// Whether the changeset branching is allowed.
    #// 
    #// @since 4.9.0
    #// @var bool
    #//
    branching = True
    #// 
    #// Whether settings should be previewed.
    #// 
    #// @since 4.9.0
    #// @var bool
    #//
    settings_previewed = True
    #// 
    #// Whether a starter content changeset was saved.
    #// 
    #// @since 4.9.0
    #// @var bool
    #//
    saved_starter_content_changeset = False
    #// 
    #// Unsanitized values for Customize Settings parsed from $_POST['customized'].
    #// 
    #// @var array
    #//
    _post_values = Array()
    #// 
    #// Changeset UUID.
    #// 
    #// @since 4.7.0
    #// @var string
    #//
    _changeset_uuid = Array()
    #// 
    #// Changeset post ID.
    #// 
    #// @since 4.7.0
    #// @var int|false
    #//
    _changeset_post_id = Array()
    #// 
    #// Changeset data loaded from a customize_changeset post.
    #// 
    #// @since 4.7.0
    #// @var array|null
    #//
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
    def __init__(self, args_=None):
        if args_ is None:
            args_ = Array()
        # end if
        
        args_ = php_array_merge(php_array_fill_keys(Array("changeset_uuid", "theme", "messenger_channel", "settings_previewed", "autosaved", "branching"), None), args_)
        #// Note that the UUID format will be validated in the setup_theme() method.
        if (not (php_isset(lambda : args_["changeset_uuid"]))):
            args_["changeset_uuid"] = wp_generate_uuid4()
        # end if
        #// The theme and messenger_channel should be supplied via $args,
        #// but they are also looked at in the $_REQUEST global here for back-compat.
        if (not (php_isset(lambda : args_["theme"]))):
            if (php_isset(lambda : PHP_REQUEST["customize_theme"])):
                args_["theme"] = wp_unslash(PHP_REQUEST["customize_theme"])
            elif (php_isset(lambda : PHP_REQUEST["theme"])):
                #// Deprecated.
                args_["theme"] = wp_unslash(PHP_REQUEST["theme"])
            # end if
        # end if
        if (not (php_isset(lambda : args_["messenger_channel"]))) and (php_isset(lambda : PHP_REQUEST["customize_messenger_channel"])):
            args_["messenger_channel"] = sanitize_key(wp_unslash(PHP_REQUEST["customize_messenger_channel"]))
        # end if
        self.original_stylesheet = get_stylesheet()
        self.theme = wp_get_theme(args_["theme"] if 0 == validate_file(args_["theme"]) else None)
        self.messenger_channel = args_["messenger_channel"]
        self._changeset_uuid = args_["changeset_uuid"]
        for key_ in Array("settings_previewed", "autosaved", "branching"):
            if (php_isset(lambda : args_[key_])):
                self.key_ = php_bool(args_[key_])
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
        components_ = apply_filters("customize_loaded_components", self.components, self)
        php_include_file(ABSPATH + WPINC + "/customize/class-wp-customize-selective-refresh.php", once=True)
        self.selective_refresh = php_new_class("WP_Customize_Selective_Refresh", lambda : WP_Customize_Selective_Refresh(self))
        if php_in_array("widgets", components_, True):
            php_include_file(ABSPATH + WPINC + "/class-wp-customize-widgets.php", once=True)
            self.widgets = php_new_class("WP_Customize_Widgets", lambda : WP_Customize_Widgets(self))
        # end if
        if php_in_array("nav_menus", components_, True):
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
    def doing_ajax(self, action_=None):
        if action_ is None:
            action_ = None
        # end if
        
        if (not wp_doing_ajax()):
            return False
        # end if
        if (not action_):
            return True
        else:
            #// 
            #// Note: we can't just use doing_action( "wp_ajax_{$action}" ) because we need
            #// to check before admin-ajax.php gets to that point.
            #//
            return (php_isset(lambda : PHP_REQUEST["action"])) and wp_unslash(PHP_REQUEST["action"]) == action_
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
    def wp_die(self, ajax_message_=None, message_=None):
        if message_ is None:
            message_ = None
        # end if
        
        if self.doing_ajax():
            wp_die(ajax_message_)
        # end if
        if (not message_):
            message_ = __("Something went wrong.")
        # end if
        if self.messenger_channel:
            ob_start()
            wp_enqueue_scripts()
            wp_print_scripts(Array("customize-base"))
            settings_ = Array({"messengerArgs": Array({"channel": self.messenger_channel, "url": wp_customize_url()})}, {"error": ajax_message_})
            php_print("""           <script>
            ( function( api, settings ) {
            var preview = new api.Messenger( settings.messengerArgs );
            preview.send( 'iframe-loading-error', settings.error );
            } )( wp.customize, """)
            php_print(wp_json_encode(settings_))
            php_print(" );\n            </script>\n         ")
            message_ += ob_get_clean()
        # end if
        wp_die(message_)
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
        
        
        global pagenow_
        php_check_if_defined("pagenow_")
        #// Check permissions for customize.php access since this method is called before customize.php can run any code.
        if "customize.php" == pagenow_ and (not current_user_can("customize")):
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
        has_post_data_nonce_ = check_ajax_referer("preview-customize_" + self.get_stylesheet(), "nonce", False) or check_ajax_referer("save-customize_" + self.get_stylesheet(), "nonce", False) or check_ajax_referer("preview-customize_" + self.get_stylesheet(), "customize_preview_nonce", False)
        if (not current_user_can("customize")) or (not has_post_data_nonce_):
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
        if get_option("fresh_site") and "customize.php" == pagenow_:
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
        
        
        global pagenow_
        php_check_if_defined("pagenow_")
        if php_empty(lambda : self._changeset_uuid):
            changeset_uuid_ = None
            if (not self.branching()) and self.is_theme_active():
                unpublished_changeset_posts_ = self.get_changeset_posts(Array({"post_status": php_array_diff(get_post_stati(), Array("auto-draft", "publish", "trash", "inherit", "private")), "exclude_restore_dismissed": False, "author": "any", "posts_per_page": 1, "order": "DESC", "orderby": "date"}))
                unpublished_changeset_post_ = php_array_shift(unpublished_changeset_posts_)
                if (not php_empty(lambda : unpublished_changeset_post_)) and wp_is_uuid(unpublished_changeset_post_.post_name):
                    changeset_uuid_ = unpublished_changeset_post_.post_name
                # end if
            # end if
            #// If no changeset UUID has been set yet, then generate a new one.
            if php_empty(lambda : changeset_uuid_):
                changeset_uuid_ = wp_generate_uuid4()
            # end if
            self._changeset_uuid = changeset_uuid_
        # end if
        if is_admin() and "customize.php" == pagenow_:
            self.set_changeset_lock(self.changeset_post_id())
        # end if
    # end def establish_loaded_changeset
    #// 
    #// Callback to validate a theme once it is loaded
    #// 
    #// @since 3.4.0
    #//
    def after_setup_theme(self):
        
        
        doing_ajax_or_is_customized_ = self.doing_ajax() or (php_isset(lambda : PHP_POST["customized"]))
        if (not doing_ajax_or_is_customized_) and (not validate_current_theme()):
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
            for setting_ in self.settings:
                setting_.preview()
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
    def wp_redirect_status(self, status_=None):
        
        
        _deprecated_function(__FUNCTION__, "4.7.0")
        if self.is_preview() and (not is_admin()):
            return 200
        # end if
        return status_
    # end def wp_redirect_status
    #// 
    #// Find the changeset post ID for a given changeset UUID.
    #// 
    #// @since 4.7.0
    #// 
    #// @param string $uuid Changeset UUID.
    #// @return int|null Returns post ID on success and null on failure.
    #//
    def find_changeset_post_id(self, uuid_=None):
        
        
        cache_group_ = "customize_changeset_post"
        changeset_post_id_ = wp_cache_get(uuid_, cache_group_)
        if changeset_post_id_ and "customize_changeset" == get_post_type(changeset_post_id_):
            return changeset_post_id_
        # end if
        changeset_post_query_ = php_new_class("WP_Query", lambda : WP_Query(Array({"post_type": "customize_changeset", "post_status": get_post_stati(), "name": uuid_, "posts_per_page": 1, "no_found_rows": True, "cache_results": True, "update_post_meta_cache": False, "update_post_term_cache": False, "lazy_load_term_meta": False})))
        if (not php_empty(lambda : changeset_post_query_.posts)):
            #// Note: 'fields'=>'ids' is not being used in order to cache the post object as it will be needed.
            changeset_post_id_ = changeset_post_query_.posts[0].ID
            wp_cache_set(uuid_, changeset_post_id_, cache_group_)
            return changeset_post_id_
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
    def get_changeset_posts(self, args_=None):
        if args_ is None:
            args_ = Array()
        # end if
        
        default_args_ = Array({"exclude_restore_dismissed": True, "posts_per_page": -1, "post_type": "customize_changeset", "post_status": "auto-draft", "order": "DESC", "orderby": "date", "no_found_rows": True, "cache_results": True, "update_post_meta_cache": False, "update_post_term_cache": False, "lazy_load_term_meta": False})
        if get_current_user_id():
            default_args_["author"] = get_current_user_id()
        # end if
        args_ = php_array_merge(default_args_, args_)
        if (not php_empty(lambda : args_["exclude_restore_dismissed"])):
            args_["exclude_restore_dismissed"] = None
            args_["meta_query"] = Array(Array({"key": "_customize_restore_dismissed", "compare": "NOT EXISTS"}))
        # end if
        return get_posts(args_)
    # end def get_changeset_posts
    #// 
    #// Dismiss all of the current user's auto-drafts (other than the present one).
    #// 
    #// @since 4.9.0
    #// @return int The number of auto-drafts that were dismissed.
    #//
    def dismiss_user_auto_draft_changesets(self):
        
        
        changeset_autodraft_posts_ = self.get_changeset_posts(Array({"post_status": "auto-draft", "exclude_restore_dismissed": True, "posts_per_page": -1}))
        dismissed_ = 0
        for autosave_autodraft_post_ in changeset_autodraft_posts_:
            if autosave_autodraft_post_.ID == self.changeset_post_id():
                continue
            # end if
            if update_post_meta(autosave_autodraft_post_.ID, "_customize_restore_dismissed", True):
                dismissed_ += 1
            # end if
        # end for
        return dismissed_
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
            post_id_ = self.find_changeset_post_id(self.changeset_uuid())
            if (not post_id_):
                post_id_ = False
            # end if
            self._changeset_post_id = post_id_
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
    def get_changeset_post_data(self, post_id_=None):
        
        
        if (not post_id_):
            return php_new_class("WP_Error", lambda : WP_Error("empty_post_id"))
        # end if
        changeset_post_ = get_post(post_id_)
        if (not changeset_post_):
            return php_new_class("WP_Error", lambda : WP_Error("missing_post"))
        # end if
        if "revision" == changeset_post_.post_type:
            if "customize_changeset" != get_post_type(changeset_post_.post_parent):
                return php_new_class("WP_Error", lambda : WP_Error("wrong_post_type"))
            # end if
        elif "customize_changeset" != changeset_post_.post_type:
            return php_new_class("WP_Error", lambda : WP_Error("wrong_post_type"))
        # end if
        changeset_data_ = php_json_decode(changeset_post_.post_content, True)
        last_error_ = php_json_last_error()
        if last_error_:
            return php_new_class("WP_Error", lambda : WP_Error("json_parse_error", "", last_error_))
        # end if
        if (not php_is_array(changeset_data_)):
            return php_new_class("WP_Error", lambda : WP_Error("expected_array"))
        # end if
        return changeset_data_
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
        changeset_post_id_ = self.changeset_post_id()
        if (not changeset_post_id_):
            self._changeset_data = Array()
        else:
            if self.autosaved() and is_user_logged_in():
                autosave_post_ = wp_get_post_autosave(changeset_post_id_, get_current_user_id())
                if autosave_post_:
                    data_ = self.get_changeset_post_data(autosave_post_.ID)
                    if (not is_wp_error(data_)):
                        self._changeset_data = data_
                    # end if
                # end if
            # end if
            #// Load data from the changeset if it was not loaded from an autosave.
            if (not (php_isset(lambda : self._changeset_data))):
                data_ = self.get_changeset_post_data(changeset_post_id_)
                if (not is_wp_error(data_)):
                    self._changeset_data = data_
                else:
                    self._changeset_data = Array()
                # end if
            # end if
        # end if
        return self._changeset_data
    # end def changeset_data
    #// 
    #// Starter content setting IDs.
    #// 
    #// @since 4.7.0
    #// @var array
    #//
    pending_starter_content_settings_ids = Array()
    #// 
    #// Import theme starter content into the customized state.
    #// 
    #// @since 4.7.0
    #// 
    #// @param array $starter_content Starter content. Defaults to `get_theme_starter_content()`.
    #//
    def import_theme_starter_content(self, starter_content_=None):
        if starter_content_ is None:
            starter_content_ = Array()
        # end if
        
        if php_empty(lambda : starter_content_):
            starter_content_ = get_theme_starter_content()
        # end if
        changeset_data_ = Array()
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
            changeset_data_ = self.get_changeset_post_data(self.changeset_post_id())
        # end if
        sidebars_widgets_ = starter_content_["widgets"] if (php_isset(lambda : starter_content_["widgets"])) and (not php_empty(lambda : self.widgets)) else Array()
        attachments_ = starter_content_["attachments"] if (php_isset(lambda : starter_content_["attachments"])) and (not php_empty(lambda : self.nav_menus)) else Array()
        posts_ = starter_content_["posts"] if (php_isset(lambda : starter_content_["posts"])) and (not php_empty(lambda : self.nav_menus)) else Array()
        options_ = starter_content_["options"] if (php_isset(lambda : starter_content_["options"])) else Array()
        nav_menus_ = starter_content_["nav_menus"] if (php_isset(lambda : starter_content_["nav_menus"])) and (not php_empty(lambda : self.nav_menus)) else Array()
        theme_mods_ = starter_content_["theme_mods"] if (php_isset(lambda : starter_content_["theme_mods"])) else Array()
        #// Widgets.
        max_widget_numbers_ = Array()
        for sidebar_id_,widgets_ in sidebars_widgets_:
            sidebar_widget_ids_ = Array()
            for widget_ in widgets_:
                id_base_, instance_ = widget_
                if (not (php_isset(lambda : max_widget_numbers_[id_base_]))):
                    #// When $settings is an array-like object, get an intrinsic array for use with array_keys().
                    settings_ = get_option(str("widget_") + str(id_base_), Array())
                    if type(settings_).__name__ == "ArrayObject" or type(settings_).__name__ == "ArrayIterator":
                        settings_ = settings_.getarraycopy()
                    # end if
                    #// Find the max widget number for this type.
                    widget_numbers_ = php_array_keys(settings_)
                    if php_count(widget_numbers_) > 0:
                        widget_numbers_[-1] = 1
                        max_widget_numbers_[id_base_] = php_max(widget_numbers_)
                    else:
                        max_widget_numbers_[id_base_] = 1
                    # end if
                # end if
                max_widget_numbers_[id_base_] += 1
                widget_id_ = php_sprintf("%s-%d", id_base_, max_widget_numbers_[id_base_])
                setting_id_ = php_sprintf("widget_%s[%d]", id_base_, max_widget_numbers_[id_base_])
                setting_value_ = self.widgets.sanitize_widget_js_instance(instance_)
                if php_empty(lambda : changeset_data_[setting_id_]) or (not php_empty(lambda : changeset_data_[setting_id_]["starter_content"])):
                    self.set_post_value(setting_id_, setting_value_)
                    self.pending_starter_content_settings_ids[-1] = setting_id_
                # end if
                sidebar_widget_ids_[-1] = widget_id_
            # end for
            setting_id_ = php_sprintf("sidebars_widgets[%s]", sidebar_id_)
            if php_empty(lambda : changeset_data_[setting_id_]) or (not php_empty(lambda : changeset_data_[setting_id_]["starter_content"])):
                self.set_post_value(setting_id_, sidebar_widget_ids_)
                self.pending_starter_content_settings_ids[-1] = setting_id_
            # end if
        # end for
        starter_content_auto_draft_post_ids_ = Array()
        if (not php_empty(lambda : changeset_data_["nav_menus_created_posts"]["value"])):
            starter_content_auto_draft_post_ids_ = php_array_merge(starter_content_auto_draft_post_ids_, changeset_data_["nav_menus_created_posts"]["value"])
        # end if
        #// Make an index of all the posts needed and what their slugs are.
        needed_posts_ = Array()
        attachments_ = self.prepare_starter_content_attachments(attachments_)
        for attachment_ in attachments_:
            key_ = "attachment:" + attachment_["post_name"]
            needed_posts_[key_] = True
        # end for
        for post_symbol_ in php_array_keys(posts_):
            if php_empty(lambda : posts_[post_symbol_]["post_name"]) and php_empty(lambda : posts_[post_symbol_]["post_title"]):
                posts_[post_symbol_] = None
                continue
            # end if
            if php_empty(lambda : posts_[post_symbol_]["post_name"]):
                posts_[post_symbol_]["post_name"] = sanitize_title(posts_[post_symbol_]["post_title"])
            # end if
            if php_empty(lambda : posts_[post_symbol_]["post_type"]):
                posts_[post_symbol_]["post_type"] = "post"
            # end if
            needed_posts_[posts_[post_symbol_]["post_type"] + ":" + posts_[post_symbol_]["post_name"]] = True
        # end for
        all_post_slugs_ = php_array_merge(wp_list_pluck(attachments_, "post_name"), wp_list_pluck(posts_, "post_name"))
        #// 
        #// Obtain all post types referenced in starter content to use in query.
        #// This is needed because 'any' will not account for post types not yet registered.
        #//
        post_types_ = php_array_filter(php_array_merge(Array("attachment"), wp_list_pluck(posts_, "post_type")))
        #// Re-use auto-draft starter content posts referenced in the current customized state.
        existing_starter_content_posts_ = Array()
        if (not php_empty(lambda : starter_content_auto_draft_post_ids_)):
            existing_posts_query_ = php_new_class("WP_Query", lambda : WP_Query(Array({"post__in": starter_content_auto_draft_post_ids_, "post_status": "auto-draft", "post_type": post_types_, "posts_per_page": -1})))
            for existing_post_ in existing_posts_query_.posts:
                post_name_ = existing_post_.post_name
                if php_empty(lambda : post_name_):
                    post_name_ = get_post_meta(existing_post_.ID, "_customize_draft_post_name", True)
                # end if
                existing_starter_content_posts_[existing_post_.post_type + ":" + post_name_] = existing_post_
            # end for
        # end if
        #// Re-use non-auto-draft posts.
        if (not php_empty(lambda : all_post_slugs_)):
            existing_posts_query_ = php_new_class("WP_Query", lambda : WP_Query(Array({"post_name__in": all_post_slugs_, "post_status": php_array_diff(get_post_stati(), Array("auto-draft")), "post_type": "any", "posts_per_page": -1})))
            for existing_post_ in existing_posts_query_.posts:
                key_ = existing_post_.post_type + ":" + existing_post_.post_name
                if (php_isset(lambda : needed_posts_[key_])) and (not (php_isset(lambda : existing_starter_content_posts_[key_]))):
                    existing_starter_content_posts_[key_] = existing_post_
                # end if
            # end for
        # end if
        #// Attachments are technically posts but handled differently.
        if (not php_empty(lambda : attachments_)):
            attachment_ids_ = Array()
            for symbol_,attachment_ in attachments_:
                file_array_ = Array({"name": attachment_["file_name"]})
                file_path_ = attachment_["file_path"]
                attachment_id_ = None
                attached_file_ = None
                if (php_isset(lambda : existing_starter_content_posts_["attachment:" + attachment_["post_name"]])):
                    attachment_post_ = existing_starter_content_posts_["attachment:" + attachment_["post_name"]]
                    attachment_id_ = attachment_post_.ID
                    attached_file_ = get_attached_file(attachment_id_)
                    if php_empty(lambda : attached_file_) or (not php_file_exists(attached_file_)):
                        attachment_id_ = None
                        attached_file_ = None
                    elif self.get_stylesheet() != get_post_meta(attachment_post_.ID, "_starter_content_theme", True):
                        #// Re-generate attachment metadata since it was previously generated for a different theme.
                        metadata_ = wp_generate_attachment_metadata(attachment_post_.ID, attached_file_)
                        wp_update_attachment_metadata(attachment_id_, metadata_)
                        update_post_meta(attachment_id_, "_starter_content_theme", self.get_stylesheet())
                    # end if
                # end if
                #// Insert the attachment auto-draft because it doesn't yet exist or the attached file is gone.
                if (not attachment_id_):
                    #// Copy file to temp location so that original file won't get deleted from theme after sideloading.
                    temp_file_name_ = wp_tempnam(wp_basename(file_path_))
                    if temp_file_name_ and copy(file_path_, temp_file_name_):
                        file_array_["tmp_name"] = temp_file_name_
                    # end if
                    if php_empty(lambda : file_array_["tmp_name"]):
                        continue
                    # end if
                    attachment_post_data_ = php_array_merge(wp_array_slice_assoc(attachment_, Array("post_title", "post_content", "post_excerpt")), Array({"post_status": "auto-draft"}))
                    attachment_id_ = media_handle_sideload(file_array_, 0, None, attachment_post_data_)
                    if is_wp_error(attachment_id_):
                        continue
                    # end if
                    update_post_meta(attachment_id_, "_starter_content_theme", self.get_stylesheet())
                    update_post_meta(attachment_id_, "_customize_draft_post_name", attachment_["post_name"])
                # end if
                attachment_ids_[symbol_] = attachment_id_
            # end for
            starter_content_auto_draft_post_ids_ = php_array_merge(starter_content_auto_draft_post_ids_, php_array_values(attachment_ids_))
        # end if
        #// Posts & pages.
        if (not php_empty(lambda : posts_)):
            for post_symbol_ in php_array_keys(posts_):
                if php_empty(lambda : posts_[post_symbol_]["post_type"]) or php_empty(lambda : posts_[post_symbol_]["post_name"]):
                    continue
                # end if
                post_type_ = posts_[post_symbol_]["post_type"]
                if (not php_empty(lambda : posts_[post_symbol_]["post_name"])):
                    post_name_ = posts_[post_symbol_]["post_name"]
                elif (not php_empty(lambda : posts_[post_symbol_]["post_title"])):
                    post_name_ = sanitize_title(posts_[post_symbol_]["post_title"])
                else:
                    continue
                # end if
                #// Use existing auto-draft post if one already exists with the same type and name.
                if (php_isset(lambda : existing_starter_content_posts_[post_type_ + ":" + post_name_])):
                    posts_[post_symbol_]["ID"] = existing_starter_content_posts_[post_type_ + ":" + post_name_].ID
                    continue
                # end if
                #// Translate the featured image symbol.
                if (not php_empty(lambda : posts_[post_symbol_]["thumbnail"])) and php_preg_match("/^{{(?P<symbol>.+)}}$/", posts_[post_symbol_]["thumbnail"], matches_) and (php_isset(lambda : attachment_ids_[matches_["symbol"]])):
                    posts_[post_symbol_]["meta_input"]["_thumbnail_id"] = attachment_ids_[matches_["symbol"]]
                # end if
                if (not php_empty(lambda : posts_[post_symbol_]["template"])):
                    posts_[post_symbol_]["meta_input"]["_wp_page_template"] = posts_[post_symbol_]["template"]
                # end if
                r_ = self.nav_menus.insert_auto_draft_post(posts_[post_symbol_])
                if type(r_).__name__ == "WP_Post":
                    posts_[post_symbol_]["ID"] = r_.ID
                # end if
            # end for
            starter_content_auto_draft_post_ids_ = php_array_merge(starter_content_auto_draft_post_ids_, wp_list_pluck(posts_, "ID"))
        # end if
        #// The nav_menus_created_posts setting is why nav_menus component is dependency for adding posts.
        if (not php_empty(lambda : self.nav_menus)) and (not php_empty(lambda : starter_content_auto_draft_post_ids_)):
            setting_id_ = "nav_menus_created_posts"
            self.set_post_value(setting_id_, array_unique(php_array_values(starter_content_auto_draft_post_ids_)))
            self.pending_starter_content_settings_ids[-1] = setting_id_
        # end if
        #// Nav menus.
        placeholder_id_ = -1
        reused_nav_menu_setting_ids_ = Array()
        for nav_menu_location_,nav_menu_ in nav_menus_:
            nav_menu_term_id_ = None
            nav_menu_setting_id_ = None
            matches_ = Array()
            #// Look for an existing placeholder menu with starter content to re-use.
            for setting_id_,setting_params_ in changeset_data_:
                can_reuse_ = (not php_empty(lambda : setting_params_["starter_content"])) and (not php_in_array(setting_id_, reused_nav_menu_setting_ids_, True)) and php_preg_match("#^nav_menu\\[(?P<nav_menu_id>-?\\d+)\\]$#", setting_id_, matches_)
                if can_reuse_:
                    nav_menu_term_id_ = php_intval(matches_["nav_menu_id"])
                    nav_menu_setting_id_ = setting_id_
                    reused_nav_menu_setting_ids_[-1] = setting_id_
                    break
                # end if
            # end for
            if (not nav_menu_term_id_):
                while True:
                    
                    if not ((php_isset(lambda : changeset_data_[php_sprintf("nav_menu[%d]", placeholder_id_)]))):
                        break
                    # end if
                    placeholder_id_ -= 1
                # end while
                nav_menu_term_id_ = placeholder_id_
                nav_menu_setting_id_ = php_sprintf("nav_menu[%d]", placeholder_id_)
            # end if
            self.set_post_value(nav_menu_setting_id_, Array({"name": nav_menu_["name"] if (php_isset(lambda : nav_menu_["name"])) else nav_menu_location_}))
            self.pending_starter_content_settings_ids[-1] = nav_menu_setting_id_
            #// @todo Add support for menu_item_parent.
            position_ = 0
            for nav_menu_item_ in nav_menu_["items"]:
                nav_menu_item_setting_id_ = php_sprintf("nav_menu_item[%d]", placeholder_id_)
                placeholder_id_ -= 1
                if (not (php_isset(lambda : nav_menu_item_["position"]))):
                    nav_menu_item_["position"] = position_
                    position_ += 1
                    position_ += 1
                # end if
                nav_menu_item_["nav_menu_term_id"] = nav_menu_term_id_
                if (php_isset(lambda : nav_menu_item_["object_id"])):
                    if "post_type" == nav_menu_item_["type"] and php_preg_match("/^{{(?P<symbol>.+)}}$/", nav_menu_item_["object_id"], matches_) and (php_isset(lambda : posts_[matches_["symbol"]])):
                        nav_menu_item_["object_id"] = posts_[matches_["symbol"]]["ID"]
                        if php_empty(lambda : nav_menu_item_["title"]):
                            original_object_ = get_post(nav_menu_item_["object_id"])
                            nav_menu_item_["title"] = original_object_.post_title
                        # end if
                    else:
                        continue
                    # end if
                else:
                    nav_menu_item_["object_id"] = 0
                # end if
                if php_empty(lambda : changeset_data_[nav_menu_item_setting_id_]) or (not php_empty(lambda : changeset_data_[nav_menu_item_setting_id_]["starter_content"])):
                    self.set_post_value(nav_menu_item_setting_id_, nav_menu_item_)
                    self.pending_starter_content_settings_ids[-1] = nav_menu_item_setting_id_
                # end if
            # end for
            setting_id_ = php_sprintf("nav_menu_locations[%s]", nav_menu_location_)
            if php_empty(lambda : changeset_data_[setting_id_]) or (not php_empty(lambda : changeset_data_[setting_id_]["starter_content"])):
                self.set_post_value(setting_id_, nav_menu_term_id_)
                self.pending_starter_content_settings_ids[-1] = setting_id_
            # end if
        # end for
        #// Options.
        for name_,value_ in options_:
            #// Serialize the value to check for post symbols.
            value_ = maybe_serialize(value_)
            if is_serialized(value_):
                if php_preg_match("/s:\\d+:\"{{(?P<symbol>.+)}}\"/", value_, matches_):
                    if (php_isset(lambda : posts_[matches_["symbol"]])):
                        symbol_match_ = posts_[matches_["symbol"]]["ID"]
                    elif (php_isset(lambda : attachment_ids_[matches_["symbol"]])):
                        symbol_match_ = attachment_ids_[matches_["symbol"]]
                    # end if
                    #// If we have any symbol matches, update the values.
                    if (php_isset(lambda : symbol_match_)):
                        #// Replace found string matches with post IDs.
                        value_ = php_str_replace(matches_[0], str("i:") + str(symbol_match_), value_)
                    else:
                        continue
                    # end if
                # end if
            elif php_preg_match("/^{{(?P<symbol>.+)}}$/", value_, matches_):
                if (php_isset(lambda : posts_[matches_["symbol"]])):
                    value_ = posts_[matches_["symbol"]]["ID"]
                elif (php_isset(lambda : attachment_ids_[matches_["symbol"]])):
                    value_ = attachment_ids_[matches_["symbol"]]
                else:
                    continue
                # end if
            # end if
            #// Unserialize values after checking for post symbols, so they can be properly referenced.
            value_ = maybe_unserialize(value_)
            if php_empty(lambda : changeset_data_[name_]) or (not php_empty(lambda : changeset_data_[name_]["starter_content"])):
                self.set_post_value(name_, value_)
                self.pending_starter_content_settings_ids[-1] = name_
            # end if
        # end for
        #// Theme mods.
        for name_,value_ in theme_mods_:
            #// Serialize the value to check for post symbols.
            value_ = maybe_serialize(value_)
            #// Check if value was serialized.
            if is_serialized(value_):
                if php_preg_match("/s:\\d+:\"{{(?P<symbol>.+)}}\"/", value_, matches_):
                    if (php_isset(lambda : posts_[matches_["symbol"]])):
                        symbol_match_ = posts_[matches_["symbol"]]["ID"]
                    elif (php_isset(lambda : attachment_ids_[matches_["symbol"]])):
                        symbol_match_ = attachment_ids_[matches_["symbol"]]
                    # end if
                    #// If we have any symbol matches, update the values.
                    if (php_isset(lambda : symbol_match_)):
                        #// Replace found string matches with post IDs.
                        value_ = php_str_replace(matches_[0], str("i:") + str(symbol_match_), value_)
                    else:
                        continue
                    # end if
                # end if
            elif php_preg_match("/^{{(?P<symbol>.+)}}$/", value_, matches_):
                if (php_isset(lambda : posts_[matches_["symbol"]])):
                    value_ = posts_[matches_["symbol"]]["ID"]
                elif (php_isset(lambda : attachment_ids_[matches_["symbol"]])):
                    value_ = attachment_ids_[matches_["symbol"]]
                else:
                    continue
                # end if
            # end if
            #// Unserialize values after checking for post symbols, so they can be properly referenced.
            value_ = maybe_unserialize(value_)
            #// Handle header image as special case since setting has a legacy format.
            if "header_image" == name_:
                name_ = "header_image_data"
                metadata_ = wp_get_attachment_metadata(value_)
                if php_empty(lambda : metadata_):
                    continue
                # end if
                value_ = Array({"attachment_id": value_, "url": wp_get_attachment_url(value_), "height": metadata_["height"], "width": metadata_["width"]})
            elif "background_image" == name_:
                value_ = wp_get_attachment_url(value_)
            # end if
            if php_empty(lambda : changeset_data_[name_]) or (not php_empty(lambda : changeset_data_[name_]["starter_content"])):
                self.set_post_value(name_, value_)
                self.pending_starter_content_settings_ids[-1] = name_
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
    def prepare_starter_content_attachments(self, attachments_=None):
        
        
        prepared_attachments_ = Array()
        if php_empty(lambda : attachments_):
            return prepared_attachments_
        # end if
        #// Such is The WordPress Way.
        php_include_file(ABSPATH + "wp-admin/includes/file.php", once=True)
        php_include_file(ABSPATH + "wp-admin/includes/media.php", once=True)
        php_include_file(ABSPATH + "wp-admin/includes/image.php", once=True)
        for symbol_,attachment_ in attachments_:
            #// A file is required and URLs to files are not currently allowed.
            if php_empty(lambda : attachment_["file"]) or php_preg_match("#^https?://$#", attachment_["file"]):
                continue
            # end if
            file_path_ = None
            if php_file_exists(attachment_["file"]):
                file_path_ = attachment_["file"]
                pass
            elif is_child_theme() and php_file_exists(get_stylesheet_directory() + "/" + attachment_["file"]):
                file_path_ = get_stylesheet_directory() + "/" + attachment_["file"]
            elif php_file_exists(get_template_directory() + "/" + attachment_["file"]):
                file_path_ = get_template_directory() + "/" + attachment_["file"]
            else:
                continue
            # end if
            file_name_ = wp_basename(attachment_["file"])
            #// Skip file types that are not recognized.
            checked_filetype_ = wp_check_filetype(file_name_)
            if php_empty(lambda : checked_filetype_["type"]):
                continue
            # end if
            #// Ensure post_name is set since not automatically derived from post_title for new auto-draft posts.
            if php_empty(lambda : attachment_["post_name"]):
                if (not php_empty(lambda : attachment_["post_title"])):
                    attachment_["post_name"] = sanitize_title(attachment_["post_title"])
                else:
                    attachment_["post_name"] = sanitize_title(php_preg_replace("/\\.\\w+$/", "", file_name_))
                # end if
            # end if
            attachment_["file_name"] = file_name_
            attachment_["file_path"] = file_path_
            prepared_attachments_[symbol_] = attachment_
        # end for
        return prepared_attachments_
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
    def unsanitized_post_values(self, args_=None):
        if args_ is None:
            args_ = Array()
        # end if
        
        args_ = php_array_merge(Array({"exclude_changeset": False, "exclude_post_data": (not current_user_can("customize"))}), args_)
        values_ = Array()
        #// Let default values be from the stashed theme mods if doing a theme switch and if no changeset is present.
        if (not self.is_theme_active()):
            stashed_theme_mods_ = get_option("customize_stashed_theme_mods")
            stylesheet_ = self.get_stylesheet()
            if (php_isset(lambda : stashed_theme_mods_[stylesheet_])):
                values_ = php_array_merge(values_, wp_list_pluck(stashed_theme_mods_[stylesheet_], "value"))
            # end if
        # end if
        if (not args_["exclude_changeset"]):
            for setting_id_,setting_params_ in self.changeset_data():
                if (not php_array_key_exists("value", setting_params_)):
                    continue
                # end if
                if (php_isset(lambda : setting_params_["type"])) and "theme_mod" == setting_params_["type"]:
                    #// Ensure that theme mods values are only used if they were saved under the current theme.
                    namespace_pattern_ = "/^(?P<stylesheet>.+?)::(?P<setting_id>.+)$/"
                    if php_preg_match(namespace_pattern_, setting_id_, matches_) and self.get_stylesheet() == matches_["stylesheet"]:
                        values_[matches_["setting_id"]] = setting_params_["value"]
                    # end if
                else:
                    values_[setting_id_] = setting_params_["value"]
                # end if
            # end for
        # end if
        if (not args_["exclude_post_data"]):
            if (not (php_isset(lambda : self._post_values))):
                if (php_isset(lambda : PHP_POST["customized"])):
                    post_values_ = php_json_decode(wp_unslash(PHP_POST["customized"]), True)
                else:
                    post_values_ = Array()
                # end if
                if php_is_array(post_values_):
                    self._post_values = post_values_
                else:
                    self._post_values = Array()
                # end if
            # end if
            values_ = php_array_merge(values_, self._post_values)
        # end if
        return values_
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
    def post_value(self, setting_=None, default_=None):
        if default_ is None:
            default_ = None
        # end if
        
        post_values_ = self.unsanitized_post_values()
        if (not php_array_key_exists(setting_.id, post_values_)):
            return default_
        # end if
        value_ = post_values_[setting_.id]
        valid_ = setting_.validate(value_)
        if is_wp_error(valid_):
            return default_
        # end if
        value_ = setting_.sanitize(value_)
        if php_is_null(value_) or is_wp_error(value_):
            return default_
        # end if
        return value_
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
    def set_post_value(self, setting_id_=None, value_=None):
        
        
        self.unsanitized_post_values()
        #// Populate _post_values from $_POST['customized'].
        self._post_values[setting_id_] = value_
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
        do_action(str("customize_post_value_set_") + str(setting_id_), value_, self)
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
        do_action("customize_post_value_set", setting_id_, value_, self)
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
    def filter_iframe_security_headers(self, headers_=None):
        
        
        headers_["X-Frame-Options"] = "SAMEORIGIN"
        headers_["Content-Security-Policy"] = "frame-ancestors 'self'"
        return headers_
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
    def add_state_query_params(self, url_=None):
        
        
        parsed_original_url_ = wp_parse_url(url_)
        is_allowed_ = False
        for allowed_url_ in self.get_allowed_urls():
            parsed_allowed_url_ = wp_parse_url(allowed_url_)
            is_allowed_ = parsed_allowed_url_["scheme"] == parsed_original_url_["scheme"] and parsed_allowed_url_["host"] == parsed_original_url_["host"] and 0 == php_strpos(parsed_original_url_["path"], parsed_allowed_url_["path"])
            if is_allowed_:
                break
            # end if
        # end for
        if is_allowed_:
            query_params_ = Array({"customize_changeset_uuid": self.changeset_uuid()})
            if (not self.is_theme_active()):
                query_params_["customize_theme"] = self.get_stylesheet()
            # end if
            if self.messenger_channel:
                query_params_["customize_messenger_channel"] = self.messenger_channel
            # end if
            url_ = add_query_arg(query_params_, url_)
        # end if
        return url_
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
        
        
        post_values_ = self.unsanitized_post_values(Array({"exclude_changeset": True}))
        setting_validities_ = self.validate_setting_values(post_values_)
        exported_setting_validities_ = php_array_map(Array(self, "prepare_setting_validity_for_js"), setting_validities_)
        #// Note that the REQUEST_URI is not passed into home_url() since this breaks subdirectory installations.
        self_url_ = home_url("/") if php_empty(lambda : PHP_SERVER["REQUEST_URI"]) else esc_url_raw(wp_unslash(PHP_SERVER["REQUEST_URI"]))
        state_query_params_ = Array("customize_theme", "customize_changeset_uuid", "customize_messenger_channel")
        self_url_ = remove_query_arg(state_query_params_, self_url_)
        allowed_urls_ = self.get_allowed_urls()
        allowed_hosts_ = Array()
        for allowed_url_ in allowed_urls_:
            parsed_ = wp_parse_url(allowed_url_)
            if php_empty(lambda : parsed_["host"]):
                continue
            # end if
            host_ = parsed_["host"]
            if (not php_empty(lambda : parsed_["port"])):
                host_ += ":" + parsed_["port"]
            # end if
            allowed_hosts_[-1] = host_
        # end for
        switched_locale_ = switch_to_locale(get_user_locale())
        l10n_ = Array({"shiftClickToEdit": __("Shift-click to edit this element."), "linkUnpreviewable": __("This link is not live-previewable."), "formUnpreviewable": __("This form is not live-previewable.")})
        if switched_locale_:
            restore_previous_locale()
        # end if
        settings_ = Array({"changeset": Array({"uuid": self.changeset_uuid(), "autosaved": self.autosaved()})}, {"timeouts": Array({"selectiveRefresh": 250, "keepAliveSend": 1000})}, {"theme": Array({"stylesheet": self.get_stylesheet(), "active": self.is_theme_active()})}, {"url": Array({"self": self_url_, "allowed": php_array_map("esc_url_raw", self.get_allowed_urls()), "allowedHosts": array_unique(allowed_hosts_), "isCrossDomain": self.is_cross_domain()})}, {"channel": self.messenger_channel, "activePanels": Array(), "activeSections": Array(), "activeControls": Array(), "settingValidities": exported_setting_validities_, "nonce": self.get_nonces() if current_user_can("customize") else Array(), "l10n": l10n_, "_dirty": php_array_keys(post_values_)})
        for panel_id_,panel_ in self.panels:
            if panel_.check_capabilities():
                settings_["activePanels"][panel_id_] = panel_.active()
                for section_id_,section_ in panel_.sections:
                    if section_.check_capabilities():
                        settings_["activeSections"][section_id_] = section_.active()
                    # end if
                # end for
            # end if
        # end for
        for id_,section_ in self.sections:
            if section_.check_capabilities():
                settings_["activeSections"][id_] = section_.active()
            # end if
        # end for
        for id_,control_ in self.controls:
            if control_.check_capabilities():
                settings_["activeControls"][id_] = control_.active()
            # end if
        # end for
        php_print("     <script type=\"text/javascript\">\n         var _wpCustomizeSettings = ")
        php_print(wp_json_encode(settings_))
        php_print(""";
        _wpCustomizeSettings.values = {};
        (function( v ) {
        """)
        #// 
        #// Serialize settings separately from the initial _wpCustomizeSettings
        #// serialization in order to avoid a peak memory usage spike.
        #// @todo We may not even need to export the values at all since the pane syncs them anyway.
        #//
        for id_,setting_ in self.settings:
            if setting_.check_capabilities():
                printf("v[%s] = %s;\n", wp_json_encode(id_), wp_json_encode(setting_.js_value()))
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
        if return_ is None:
            return_ = None
        # end if
        
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
    def current_theme(self, current_theme_=None):
        
        
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
    def validate_setting_values(self, setting_values_=None, options_=None):
        if options_ is None:
            options_ = Array()
        # end if
        
        options_ = wp_parse_args(options_, Array({"validate_capability": False, "validate_existence": False}))
        validities_ = Array()
        for setting_id_,unsanitized_value_ in setting_values_:
            setting_ = self.get_setting(setting_id_)
            if (not setting_):
                if options_["validate_existence"]:
                    validities_[setting_id_] = php_new_class("WP_Error", lambda : WP_Error("unrecognized", __("Setting does not exist or is unrecognized.")))
                # end if
                continue
            # end if
            if options_["validate_capability"] and (not current_user_can(setting_.capability)):
                validity_ = php_new_class("WP_Error", lambda : WP_Error("unauthorized", __("Unauthorized to modify setting due to capability.")))
            else:
                if php_is_null(unsanitized_value_):
                    continue
                # end if
                validity_ = setting_.validate(unsanitized_value_)
            # end if
            if (not is_wp_error(validity_)):
                #// This filter is documented in wp-includes/class-wp-customize-setting.php
                late_validity_ = apply_filters(str("customize_validate_") + str(setting_.id), php_new_class("WP_Error", lambda : WP_Error()), unsanitized_value_, setting_)
                if is_wp_error(late_validity_) and late_validity_.has_errors():
                    validity_ = late_validity_
                # end if
            # end if
            if (not is_wp_error(validity_)):
                value_ = setting_.sanitize(unsanitized_value_)
                if php_is_null(value_):
                    validity_ = False
                elif is_wp_error(value_):
                    validity_ = value_
                # end if
            # end if
            if False == validity_:
                validity_ = php_new_class("WP_Error", lambda : WP_Error("invalid_value", __("Invalid value.")))
            # end if
            validities_[setting_id_] = validity_
        # end for
        return validities_
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
    def prepare_setting_validity_for_js(self, validity_=None):
        
        
        if is_wp_error(validity_):
            notification_ = Array()
            for error_code_,error_messages_ in validity_.errors:
                notification_[error_code_] = Array({"message": join(" ", error_messages_), "data": validity_.get_error_data(error_code_)})
            # end for
            return notification_
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
        action_ = "save-customize_" + self.get_stylesheet()
        if (not check_ajax_referer(action_, "nonce", False)):
            wp_send_json_error("invalid_nonce")
        # end if
        changeset_post_id_ = self.changeset_post_id()
        is_new_changeset_ = php_empty(lambda : changeset_post_id_)
        if is_new_changeset_:
            if (not current_user_can(get_post_type_object("customize_changeset").cap.create_posts)):
                wp_send_json_error("cannot_create_changeset_post")
            # end if
        else:
            if (not current_user_can(get_post_type_object("customize_changeset").cap.edit_post, changeset_post_id_)):
                wp_send_json_error("cannot_edit_changeset_post")
            # end if
        # end if
        if (not php_empty(lambda : PHP_POST["customize_changeset_data"])):
            input_changeset_data_ = php_json_decode(wp_unslash(PHP_POST["customize_changeset_data"]), True)
            if (not php_is_array(input_changeset_data_)):
                wp_send_json_error("invalid_customize_changeset_data")
            # end if
        else:
            input_changeset_data_ = Array()
        # end if
        #// Validate title.
        changeset_title_ = None
        if (php_isset(lambda : PHP_POST["customize_changeset_title"])):
            changeset_title_ = sanitize_text_field(wp_unslash(PHP_POST["customize_changeset_title"]))
        # end if
        #// Validate changeset status param.
        is_publish_ = None
        changeset_status_ = None
        if (php_isset(lambda : PHP_POST["customize_changeset_status"])):
            changeset_status_ = wp_unslash(PHP_POST["customize_changeset_status"])
            if (not get_post_status_object(changeset_status_)) or (not php_in_array(changeset_status_, Array("draft", "pending", "publish", "future"), True)):
                wp_send_json_error("bad_customize_changeset_status", 400)
            # end if
            is_publish_ = "publish" == changeset_status_ or "future" == changeset_status_
            if is_publish_ and (not current_user_can(get_post_type_object("customize_changeset").cap.publish_posts)):
                wp_send_json_error("changeset_publish_unauthorized", 403)
            # end if
        # end if
        #// 
        #// Validate changeset date param. Date is assumed to be in local time for
        #// the WP if in MySQL format (YYYY-MM-DD HH:MM:SS). Otherwise, the date
        #// is parsed with strtotime() so that ISO date format may be supplied
        #// or a string like "+10 minutes".
        #//
        changeset_date_gmt_ = None
        if (php_isset(lambda : PHP_POST["customize_changeset_date"])):
            changeset_date_ = wp_unslash(PHP_POST["customize_changeset_date"])
            if php_preg_match("/^\\d\\d\\d\\d-\\d\\d-\\d\\d \\d\\d:\\d\\d:\\d\\d$/", changeset_date_):
                mm_ = php_substr(changeset_date_, 5, 2)
                jj_ = php_substr(changeset_date_, 8, 2)
                aa_ = php_substr(changeset_date_, 0, 4)
                valid_date_ = wp_checkdate(mm_, jj_, aa_, changeset_date_)
                if (not valid_date_):
                    wp_send_json_error("bad_customize_changeset_date", 400)
                # end if
                changeset_date_gmt_ = get_gmt_from_date(changeset_date_)
            else:
                timestamp_ = strtotime(changeset_date_)
                if (not timestamp_):
                    wp_send_json_error("bad_customize_changeset_date", 400)
                # end if
                changeset_date_gmt_ = gmdate("Y-m-d H:i:s", timestamp_)
            # end if
        # end if
        lock_user_id_ = None
        autosave_ = (not php_empty(lambda : PHP_POST["customize_changeset_autosave"]))
        if (not is_new_changeset_):
            lock_user_id_ = wp_check_post_lock(self.changeset_post_id())
        # end if
        #// Force request to autosave when changeset is locked.
        if lock_user_id_ and (not autosave_):
            autosave_ = True
            changeset_status_ = None
            changeset_date_gmt_ = None
        # end if
        if autosave_ and (not php_defined("DOING_AUTOSAVE")):
            #// Back-compat.
            php_define("DOING_AUTOSAVE", True)
        # end if
        autosaved_ = False
        r_ = self.save_changeset_post(Array({"status": changeset_status_, "title": changeset_title_, "date_gmt": changeset_date_gmt_, "data": input_changeset_data_, "autosave": autosave_}))
        if autosave_ and (not is_wp_error(r_)):
            autosaved_ = True
        # end if
        #// If the changeset was locked and an autosave request wasn't itself an error, then now explicitly return with a failure.
        if lock_user_id_ and (not is_wp_error(r_)):
            r_ = php_new_class("WP_Error", lambda : WP_Error("changeset_locked", __("Changeset is being edited by other user."), Array({"lock_user": self.get_lock_user_data(lock_user_id_)})))
        # end if
        if is_wp_error(r_):
            response_ = Array({"message": r_.get_error_message(), "code": r_.get_error_code()})
            if php_is_array(r_.get_error_data()):
                response_ = php_array_merge(response_, r_.get_error_data())
            else:
                response_["data"] = r_.get_error_data()
            # end if
        else:
            response_ = r_
            changeset_post_ = get_post(self.changeset_post_id())
            #// Dismiss all other auto-draft changeset posts for this user (they serve like autosave revisions), as there should only be one.
            if is_new_changeset_:
                self.dismiss_user_auto_draft_changesets()
            # end if
            #// Note that if the changeset status was publish, then it will get set to Trash if revisions are not supported.
            response_["changeset_status"] = changeset_post_.post_status
            if is_publish_ and "trash" == response_["changeset_status"]:
                response_["changeset_status"] = "publish"
            # end if
            if "publish" != response_["changeset_status"]:
                self.set_changeset_lock(changeset_post_.ID)
            # end if
            if "future" == response_["changeset_status"]:
                response_["changeset_date"] = changeset_post_.post_date
            # end if
            if "publish" == response_["changeset_status"] or "trash" == response_["changeset_status"]:
                response_["next_changeset_uuid"] = wp_generate_uuid4()
            # end if
        # end if
        if autosave_:
            response_["autosaved"] = autosaved_
        # end if
        if (php_isset(lambda : response_["setting_validities"])):
            response_["setting_validities"] = php_array_map(Array(self, "prepare_setting_validity_for_js"), response_["setting_validities"])
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
        response_ = apply_filters("customize_save_response", response_, self)
        if is_wp_error(r_):
            wp_send_json_error(response_)
        else:
            wp_send_json_success(response_)
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
    def save_changeset_post(self, args_=None):
        if args_ is None:
            args_ = Array()
        # end if
        
        args_ = php_array_merge(Array({"status": None, "title": None, "data": Array(), "date_gmt": None, "user_id": get_current_user_id(), "starter_content": False, "autosave": False}), args_)
        changeset_post_id_ = self.changeset_post_id()
        existing_changeset_data_ = Array()
        if changeset_post_id_:
            existing_status_ = get_post_status(changeset_post_id_)
            if "publish" == existing_status_ or "trash" == existing_status_:
                return php_new_class("WP_Error", lambda : WP_Error("changeset_already_published", __("The previous set of changes has already been published. Please try saving your current set of changes again."), Array({"next_changeset_uuid": wp_generate_uuid4()})))
            # end if
            existing_changeset_data_ = self.get_changeset_post_data(changeset_post_id_)
            if is_wp_error(existing_changeset_data_):
                return existing_changeset_data_
            # end if
        # end if
        #// Fail if attempting to publish but publish hook is missing.
        if "publish" == args_["status"] and False == has_action("transition_post_status", "_wp_customize_publish_changeset"):
            return php_new_class("WP_Error", lambda : WP_Error("missing_publish_callback"))
        # end if
        #// Validate date.
        now_ = gmdate("Y-m-d H:i:59")
        if args_["date_gmt"]:
            is_future_dated_ = mysql2date("U", args_["date_gmt"], False) > mysql2date("U", now_, False)
            if (not is_future_dated_):
                return php_new_class("WP_Error", lambda : WP_Error("not_future_date", __("You must supply a future date to schedule.")))
                pass
            # end if
            if (not self.is_theme_active()) and "future" == args_["status"] or is_future_dated_:
                return php_new_class("WP_Error", lambda : WP_Error("cannot_schedule_theme_switches"))
                pass
            # end if
            will_remain_auto_draft_ = (not args_["status"]) and (not changeset_post_id_) or "auto-draft" == get_post_status(changeset_post_id_)
            if will_remain_auto_draft_:
                return php_new_class("WP_Error", lambda : WP_Error("cannot_supply_date_for_auto_draft_changeset"))
            # end if
        elif changeset_post_id_ and "future" == args_["status"]:
            #// Fail if the new status is future but the existing post's date is not in the future.
            changeset_post_ = get_post(changeset_post_id_)
            if mysql2date("U", changeset_post_.post_date_gmt, False) <= mysql2date("U", now_, False):
                return php_new_class("WP_Error", lambda : WP_Error("not_future_date", __("You must supply a future date to schedule.")))
            # end if
        # end if
        if (not php_empty(lambda : is_future_dated_)) and "publish" == args_["status"]:
            args_["status"] = "future"
        # end if
        #// Validate autosave param. See _wp_post_revision_fields() for why these fields are disallowed.
        if args_["autosave"]:
            if args_["date_gmt"]:
                return php_new_class("WP_Error", lambda : WP_Error("illegal_autosave_with_date_gmt"))
            elif args_["status"]:
                return php_new_class("WP_Error", lambda : WP_Error("illegal_autosave_with_status"))
            elif args_["user_id"] and get_current_user_id() != args_["user_id"]:
                return php_new_class("WP_Error", lambda : WP_Error("illegal_autosave_with_non_current_user"))
            # end if
        # end if
        #// The request was made via wp.customize.previewer.save().
        update_transactionally_ = php_bool(args_["status"])
        allow_revision_ = php_bool(args_["status"])
        #// Amend post values with any supplied data.
        for setting_id_,setting_params_ in args_["data"]:
            if php_is_array(setting_params_) and php_array_key_exists("value", setting_params_):
                self.set_post_value(setting_id_, setting_params_["value"])
                pass
            # end if
        # end for
        #// Note that in addition to post data, this will include any stashed theme mods.
        post_values_ = self.unsanitized_post_values(Array({"exclude_changeset": True, "exclude_post_data": False}))
        self.add_dynamic_settings(php_array_keys(post_values_))
        #// Ensure settings get created even if they lack an input value.
        #// 
        #// Get list of IDs for settings that have values different from what is currently
        #// saved in the changeset. By skipping any values that are already the same, the
        #// subset of changed settings can be passed into validate_setting_values to prevent
        #// an underprivileged modifying a single setting for which they have the capability
        #// from being blocked from saving. This also prevents a user from touching of the
        #// previous saved settings and overriding the associated user_id if they made no change.
        #//
        changed_setting_ids_ = Array()
        for setting_id_,setting_value_ in post_values_:
            setting_ = self.get_setting(setting_id_)
            if setting_ and "theme_mod" == setting_.type:
                prefixed_setting_id_ = self.get_stylesheet() + "::" + setting_.id
            else:
                prefixed_setting_id_ = setting_id_
            # end if
            is_value_changed_ = (not (php_isset(lambda : existing_changeset_data_[prefixed_setting_id_]))) or (not php_array_key_exists("value", existing_changeset_data_[prefixed_setting_id_])) or existing_changeset_data_[prefixed_setting_id_]["value"] != setting_value_
            if is_value_changed_:
                changed_setting_ids_[-1] = setting_id_
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
        validated_values_ = php_array_merge(php_array_fill_keys(php_array_keys(args_["data"]), None), post_values_)
        setting_validities_ = self.validate_setting_values(validated_values_, Array({"validate_capability": True, "validate_existence": True}))
        invalid_setting_count_ = php_count(php_array_filter(setting_validities_, "is_wp_error"))
        #// 
        #// Short-circuit if there are invalid settings the update is transactional.
        #// A changeset update is transactional when a status is supplied in the request.
        #//
        if update_transactionally_ and invalid_setting_count_ > 0:
            response_ = Array({"setting_validities": setting_validities_, "message": php_sprintf(_n("Unable to save due to %s invalid setting.", "Unable to save due to %s invalid settings.", invalid_setting_count_), number_format_i18n(invalid_setting_count_))})
            return php_new_class("WP_Error", lambda : WP_Error("transaction_fail", "", response_))
        # end if
        #// Obtain/merge data for changeset.
        original_changeset_data_ = self.get_changeset_post_data(changeset_post_id_)
        data_ = original_changeset_data_
        if is_wp_error(data_):
            data_ = Array()
        # end if
        #// Ensure that all post values are included in the changeset data.
        for setting_id_,post_value_ in post_values_:
            if (not (php_isset(lambda : args_["data"][setting_id_]))):
                args_["data"][setting_id_] = Array()
            # end if
            if (not (php_isset(lambda : args_["data"][setting_id_]["value"]))):
                args_["data"][setting_id_]["value"] = post_value_
            # end if
        # end for
        for setting_id_,setting_params_ in args_["data"]:
            setting_ = self.get_setting(setting_id_)
            if (not setting_) or (not setting_.check_capabilities()):
                continue
            # end if
            #// Skip updating changeset for invalid setting values.
            if (php_isset(lambda : setting_validities_[setting_id_])) and is_wp_error(setting_validities_[setting_id_]):
                continue
            # end if
            changeset_setting_id_ = setting_id_
            if "theme_mod" == setting_.type:
                changeset_setting_id_ = php_sprintf("%s::%s", self.get_stylesheet(), setting_id_)
            # end if
            if None == setting_params_:
                data_[changeset_setting_id_] = None
            else:
                if (not (php_isset(lambda : data_[changeset_setting_id_]))):
                    data_[changeset_setting_id_] = Array()
                # end if
                #// Merge any additional setting params that have been supplied with the existing params.
                merged_setting_params_ = php_array_merge(data_[changeset_setting_id_], setting_params_)
                #// Skip updating setting params if unchanged (ensuring the user_id is not overwritten).
                if data_[changeset_setting_id_] == merged_setting_params_:
                    continue
                # end if
                data_[changeset_setting_id_] = php_array_merge(merged_setting_params_, Array({"type": setting_.type, "user_id": args_["user_id"], "date_modified_gmt": current_time("mysql", True)}))
                #// Clear starter_content flag in data if changeset is not explicitly being updated for starter content.
                if php_empty(lambda : args_["starter_content"]):
                    data_[changeset_setting_id_]["starter_content"] = None
                # end if
            # end if
        # end for
        filter_context_ = Array({"uuid": self.changeset_uuid(), "title": args_["title"], "status": args_["status"], "date_gmt": args_["date_gmt"], "post_id": changeset_post_id_, "previous_data": Array() if is_wp_error(original_changeset_data_) else original_changeset_data_, "manager": self})
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
        data_ = apply_filters("customize_changeset_save_data", data_, filter_context_)
        #// Switch theme if publishing changes now.
        if "publish" == args_["status"] and (not self.is_theme_active()):
            #// Temporarily stop previewing the theme to allow switch_themes() to operate properly.
            self.stop_previewing_theme()
            switch_theme(self.get_stylesheet())
            update_option("theme_switched_via_customizer", True)
            self.start_previewing_theme()
        # end if
        #// Gather the data for wp_insert_post()/wp_update_post().
        post_array_ = Array({"post_content": wp_json_encode(data_, JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT)})
        if args_["title"]:
            post_array_["post_title"] = args_["title"]
        # end if
        if changeset_post_id_:
            post_array_["ID"] = changeset_post_id_
        else:
            post_array_["post_type"] = "customize_changeset"
            post_array_["post_name"] = self.changeset_uuid()
            post_array_["post_status"] = "auto-draft"
        # end if
        if args_["status"]:
            post_array_["post_status"] = args_["status"]
        # end if
        #// Reset post date to now if we are publishing, otherwise pass post_date_gmt and translate for post_date.
        if "publish" == args_["status"]:
            post_array_["post_date_gmt"] = "0000-00-00 00:00:00"
            post_array_["post_date"] = "0000-00-00 00:00:00"
        elif args_["date_gmt"]:
            post_array_["post_date_gmt"] = args_["date_gmt"]
            post_array_["post_date"] = get_date_from_gmt(args_["date_gmt"])
        elif changeset_post_id_ and "auto-draft" == get_post_status(changeset_post_id_):
            #// 
            #// Keep bumping the date for the auto-draft whenever it is modified;
            #// this extends its life, preserving it from garbage-collection via
            #// wp_delete_auto_drafts().
            #//
            post_array_["post_date"] = current_time("mysql")
            post_array_["post_date_gmt"] = ""
        # end if
        self.store_changeset_revision = allow_revision_
        add_filter("wp_save_post_revision_post_has_changed", Array(self, "_filter_revision_post_has_changed"), 5, 3)
        #// 
        #// Update the changeset post. The publish_customize_changeset action
        #// will cause the settings in the changeset to be saved via
        #// WP_Customize_Setting::save().
        #// 
        #// Prevent content filters from corrupting JSON in post_content.
        has_kses_ = False != has_filter("content_save_pre", "wp_filter_post_kses")
        if has_kses_:
            kses_remove_filters()
        # end if
        has_targeted_link_rel_filters_ = False != has_filter("content_save_pre", "wp_targeted_link_rel")
        if has_targeted_link_rel_filters_:
            wp_remove_targeted_link_rel_filters()
        # end if
        #// Note that updating a post with publish status will trigger WP_Customize_Manager::publish_changeset_values().
        if changeset_post_id_:
            if args_["autosave"] and "auto-draft" != get_post_status(changeset_post_id_):
                #// See _wp_translate_postdata() for why this is required as it will use the edit_post meta capability.
                add_filter("map_meta_cap", Array(self, "grant_edit_post_capability_for_changeset"), 10, 4)
                post_array_["post_ID"] = post_array_["ID"]
                post_array_["post_type"] = "customize_changeset"
                r_ = wp_create_post_autosave(wp_slash(post_array_))
                remove_filter("map_meta_cap", Array(self, "grant_edit_post_capability_for_changeset"), 10)
            else:
                post_array_["edit_date"] = True
                #// Prevent date clearing.
                r_ = wp_update_post(wp_slash(post_array_), True)
                #// Delete autosave revision for user when the changeset is updated.
                if (not php_empty(lambda : args_["user_id"])):
                    autosave_draft_ = wp_get_post_autosave(changeset_post_id_, args_["user_id"])
                    if autosave_draft_:
                        wp_delete_post(autosave_draft_.ID, True)
                    # end if
                # end if
            # end if
        else:
            r_ = wp_insert_post(wp_slash(post_array_), True)
            if (not is_wp_error(r_)):
                self._changeset_post_id = r_
                pass
            # end if
        # end if
        #// Restore removed content filters.
        if has_kses_:
            kses_init_filters()
        # end if
        if has_targeted_link_rel_filters_:
            wp_init_targeted_link_rel_filters()
        # end if
        self._changeset_data = None
        #// Reset so WP_Customize_Manager::changeset_data() will re-populate with updated contents.
        remove_filter("wp_save_post_revision_post_has_changed", Array(self, "_filter_revision_post_has_changed"))
        response_ = Array({"setting_validities": setting_validities_})
        if is_wp_error(r_):
            response_["changeset_post_save_failure"] = r_.get_error_code()
            return php_new_class("WP_Error", lambda : WP_Error("changeset_post_save_failure", "", response_))
        # end if
        return response_
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
    def trash_changeset_post(self, post_=None):
        
        
        global wpdb_
        php_check_if_defined("wpdb_")
        post_ = get_post(post_)
        if (not type(post_).__name__ == "WP_Post"):
            return post_
        # end if
        post_id_ = post_.ID
        if (not EMPTY_TRASH_DAYS):
            return wp_delete_post(post_id_, True)
        # end if
        if "trash" == get_post_status(post_):
            return False
        # end if
        #// This filter is documented in wp-includes/post.php
        check_ = apply_filters("pre_trash_post", None, post_)
        if None != check_:
            return check_
        # end if
        #// This action is documented in wp-includes/post.php
        do_action("wp_trash_post", post_id_)
        add_post_meta(post_id_, "_wp_trash_meta_status", post_.post_status)
        add_post_meta(post_id_, "_wp_trash_meta_time", time())
        old_status_ = post_.post_status
        new_status_ = "trash"
        wpdb_.update(wpdb_.posts, Array({"post_status": new_status_}), Array({"ID": post_.ID}))
        clean_post_cache(post_.ID)
        post_.post_status = new_status_
        wp_transition_post_status(new_status_, old_status_, post_)
        #// This action is documented in wp-includes/post.php
        do_action(str("edit_post_") + str(post_.post_type), post_.ID, post_)
        #// This action is documented in wp-includes/post.php
        do_action("edit_post", post_.ID, post_)
        #// This action is documented in wp-includes/post.php
        do_action(str("save_post_") + str(post_.post_type), post_.ID, post_, True)
        #// This action is documented in wp-includes/post.php
        do_action("save_post", post_.ID, post_, True)
        #// This action is documented in wp-includes/post.php
        do_action("wp_insert_post", post_.ID, post_, True)
        wp_trash_post_comments(post_id_)
        #// This action is documented in wp-includes/post.php
        do_action("trashed_post", post_id_)
        return post_
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
        changeset_post_id_ = self.changeset_post_id()
        if (not changeset_post_id_):
            wp_send_json_error(Array({"message": __("No changes saved yet, so there is nothing to trash."), "code": "non_existent_changeset"}))
            return
        # end if
        if changeset_post_id_ and (not current_user_can(get_post_type_object("customize_changeset").cap.delete_post, changeset_post_id_)):
            wp_send_json_error(Array({"code": "changeset_trash_unauthorized", "message": __("Unable to trash changes.")}))
        # end if
        if "trash" == get_post_status(changeset_post_id_):
            wp_send_json_error(Array({"message": __("Changes have already been trashed."), "code": "changeset_already_trashed"}))
            return
        # end if
        r_ = self.trash_changeset_post(changeset_post_id_)
        if (not type(r_).__name__ == "WP_Post"):
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
    def grant_edit_post_capability_for_changeset(self, caps_=None, cap_=None, user_id_=None, args_=None):
        
        
        if "edit_post" == cap_ and (not php_empty(lambda : args_[0])) and "customize_changeset" == get_post_type(args_[0]):
            post_type_obj_ = get_post_type_object("customize_changeset")
            caps_ = map_meta_cap(post_type_obj_.cap.cap_, user_id_)
        # end if
        return caps_
    # end def grant_edit_post_capability_for_changeset
    #// 
    #// Marks the changeset post as being currently edited by the current user.
    #// 
    #// @since 4.9.0
    #// 
    #// @param int  $changeset_post_id Changeset post id.
    #// @param bool $take_over Take over the changeset, default is false.
    #//
    def set_changeset_lock(self, changeset_post_id_=None, take_over_=None):
        if take_over_ is None:
            take_over_ = False
        # end if
        
        if changeset_post_id_:
            can_override_ = (not php_bool(get_post_meta(changeset_post_id_, "_edit_lock", True)))
            if take_over_:
                can_override_ = True
            # end if
            if can_override_:
                lock_ = php_sprintf("%s:%s", time(), get_current_user_id())
                update_post_meta(changeset_post_id_, "_edit_lock", lock_)
            else:
                self.refresh_changeset_lock(changeset_post_id_)
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
    def refresh_changeset_lock(self, changeset_post_id_=None):
        
        
        if (not changeset_post_id_):
            return
        # end if
        lock_ = get_post_meta(changeset_post_id_, "_edit_lock", True)
        lock_ = php_explode(":", lock_)
        if lock_ and (not php_empty(lambda : lock_[1])):
            user_id_ = php_intval(lock_[1])
            current_user_id_ = get_current_user_id()
            if user_id_ == current_user_id_:
                lock_ = php_sprintf("%s:%s", time(), user_id_)
                update_post_meta(changeset_post_id_, "_edit_lock", lock_)
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
    def add_customize_screen_to_heartbeat_settings(self, settings_=None):
        
        
        global pagenow_
        php_check_if_defined("pagenow_")
        if "customize.php" == pagenow_:
            settings_["screenId"] = "customize"
        # end if
        return settings_
    # end def add_customize_screen_to_heartbeat_settings
    #// 
    #// Get lock user data.
    #// 
    #// @since 4.9.0
    #// 
    #// @param int $user_id User ID.
    #// @return array|null User data formatted for client.
    #//
    def get_lock_user_data(self, user_id_=None):
        
        
        if (not user_id_):
            return None
        # end if
        lock_user_ = get_userdata(user_id_)
        if (not lock_user_):
            return None
        # end if
        return Array({"id": lock_user_.ID, "name": lock_user_.display_name, "avatar": get_avatar_url(lock_user_.ID, Array({"size": 128}))})
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
    def check_changeset_lock_with_heartbeat(self, response_=None, data_=None, screen_id_=None):
        
        
        if (php_isset(lambda : data_["changeset_uuid"])):
            changeset_post_id_ = self.find_changeset_post_id(data_["changeset_uuid"])
        else:
            changeset_post_id_ = self.changeset_post_id()
        # end if
        if php_array_key_exists("check_changeset_lock", data_) and "customize" == screen_id_ and changeset_post_id_ and current_user_can(get_post_type_object("customize_changeset").cap.edit_post, changeset_post_id_):
            lock_user_id_ = wp_check_post_lock(changeset_post_id_)
            if lock_user_id_:
                response_["customize_changeset_lock_user"] = self.get_lock_user_data(lock_user_id_)
            else:
                #// Refreshing time will ensure that the user is sitting on customizer and has not closed the customizer tab.
                self.refresh_changeset_lock(changeset_post_id_)
            # end if
        # end if
        return response_
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
        changeset_post_id_ = self.changeset_post_id()
        if php_empty(lambda : changeset_post_id_):
            wp_send_json_error(Array({"code": "no_changeset_found_to_take_over", "message": __("No changeset found to take over")}))
        # end if
        if (not current_user_can(get_post_type_object("customize_changeset").cap.edit_post, changeset_post_id_)):
            wp_send_json_error(Array({"code": "cannot_remove_changeset_lock", "message": __("Sorry, you are not allowed to take over.")}))
        # end if
        self.set_changeset_lock(changeset_post_id_, True)
        wp_send_json_success("changeset_taken_over")
    # end def handle_override_changeset_lock_request
    #// 
    #// Whether a changeset revision should be made.
    #// 
    #// @since 4.7.0
    #// @var bool
    #//
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
    def _filter_revision_post_has_changed(self, post_has_changed_=None, last_revision_=None, post_=None):
        
        
        last_revision_ = None
        if "customize_changeset" == post_.post_type:
            post_has_changed_ = self.store_changeset_revision
        # end if
        return post_has_changed_
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
    def _publish_changeset_values(self, changeset_post_id_=None):
        
        
        global wpdb_
        php_check_if_defined("wpdb_")
        publishing_changeset_data_ = self.get_changeset_post_data(changeset_post_id_)
        if is_wp_error(publishing_changeset_data_):
            return publishing_changeset_data_
        # end if
        changeset_post_ = get_post(changeset_post_id_)
        #// 
        #// Temporarily override the changeset context so that it will be read
        #// in calls to unsanitized_post_values() and so that it will be available
        #// on the $wp_customize object passed to hooks during the save logic.
        #//
        previous_changeset_post_id_ = self._changeset_post_id
        self._changeset_post_id = changeset_post_id_
        previous_changeset_uuid_ = self._changeset_uuid
        self._changeset_uuid = changeset_post_.post_name
        previous_changeset_data_ = self._changeset_data
        self._changeset_data = publishing_changeset_data_
        #// Parse changeset data to identify theme mod settings and user IDs associated with settings to be saved.
        setting_user_ids_ = Array()
        theme_mod_settings_ = Array()
        namespace_pattern_ = "/^(?P<stylesheet>.+?)::(?P<setting_id>.+)$/"
        matches_ = Array()
        for raw_setting_id_,setting_params_ in self._changeset_data:
            actual_setting_id_ = None
            is_theme_mod_setting_ = (php_isset(lambda : setting_params_["value"])) and (php_isset(lambda : setting_params_["type"])) and "theme_mod" == setting_params_["type"] and php_preg_match(namespace_pattern_, raw_setting_id_, matches_)
            if is_theme_mod_setting_:
                if (not (php_isset(lambda : theme_mod_settings_[matches_["stylesheet"]]))):
                    theme_mod_settings_[matches_["stylesheet"]] = Array()
                # end if
                theme_mod_settings_[matches_["stylesheet"]][matches_["setting_id"]] = setting_params_
                if self.get_stylesheet() == matches_["stylesheet"]:
                    actual_setting_id_ = matches_["setting_id"]
                # end if
            else:
                actual_setting_id_ = raw_setting_id_
            # end if
            #// Keep track of the user IDs for settings actually for this theme.
            if actual_setting_id_ and (php_isset(lambda : setting_params_["user_id"])):
                setting_user_ids_[actual_setting_id_] = setting_params_["user_id"]
            # end if
        # end for
        changeset_setting_values_ = self.unsanitized_post_values(Array({"exclude_post_data": True, "exclude_changeset": False}))
        changeset_setting_ids_ = php_array_keys(changeset_setting_values_)
        self.add_dynamic_settings(changeset_setting_ids_)
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
        original_setting_capabilities_ = Array()
        for setting_id_ in changeset_setting_ids_:
            setting_ = self.get_setting(setting_id_)
            if setting_ and (not (php_isset(lambda : setting_user_ids_[setting_id_]))):
                original_setting_capabilities_[setting_.id] = setting_.capability
                setting_.capability = "exist"
            # end if
        # end for
        original_user_id_ = get_current_user_id()
        for setting_id_ in changeset_setting_ids_:
            setting_ = self.get_setting(setting_id_)
            if setting_:
                #// 
                #// Set the current user to match the user who saved the value into
                #// the changeset so that any filters that apply during the save
                #// process will respect the original user's capabilities. This
                #// will ensure, for example, that KSES won't strip unsafe HTML
                #// when a scheduled changeset publishes via WP Cron.
                #//
                if (php_isset(lambda : setting_user_ids_[setting_id_])):
                    wp_set_current_user(setting_user_ids_[setting_id_])
                else:
                    wp_set_current_user(original_user_id_)
                # end if
                setting_.save()
            # end if
        # end for
        wp_set_current_user(original_user_id_)
        #// Update the stashed theme mod settings, removing the active theme's stashed settings, if activated.
        if did_action("switch_theme"):
            other_theme_mod_settings_ = theme_mod_settings_
            other_theme_mod_settings_[self.get_stylesheet()] = None
            self.update_stashed_theme_mod_settings(other_theme_mod_settings_)
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
        for setting_id_,capability_ in original_setting_capabilities_:
            setting_ = self.get_setting(setting_id_)
            if setting_:
                setting_.capability = capability_
            # end if
        # end for
        #// Restore original changeset data.
        self._changeset_data = previous_changeset_data_
        self._changeset_post_id = previous_changeset_post_id_
        self._changeset_uuid = previous_changeset_uuid_
        #// 
        #// Convert all autosave revisions into their own auto-drafts so that users can be prompted to
        #// restore them when a changeset is published, but they had been locked out from including
        #// their changes in the changeset.
        #//
        revisions_ = wp_get_post_revisions(changeset_post_id_, Array({"check_enabled": False}))
        for revision_ in revisions_:
            if False != php_strpos(revision_.post_name, str(changeset_post_id_) + str("-autosave")):
                wpdb_.update(wpdb_.posts, Array({"post_status": "auto-draft", "post_type": "customize_changeset", "post_name": wp_generate_uuid4(), "post_parent": 0}), Array({"ID": revision_.ID}))
                clean_post_cache(revision_.ID)
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
    def update_stashed_theme_mod_settings(self, inactive_theme_mod_settings_=None):
        
        
        stashed_theme_mod_settings_ = get_option("customize_stashed_theme_mods")
        if php_empty(lambda : stashed_theme_mod_settings_):
            stashed_theme_mod_settings_ = Array()
        # end if
        stashed_theme_mod_settings_[self.get_stylesheet()] = None
        #// Merge inactive theme mods with the stashed theme mod settings.
        for stylesheet_,theme_mod_settings_ in inactive_theme_mod_settings_:
            if (not (php_isset(lambda : stashed_theme_mod_settings_[stylesheet_]))):
                stashed_theme_mod_settings_[stylesheet_] = Array()
            # end if
            stashed_theme_mod_settings_[stylesheet_] = php_array_merge(stashed_theme_mod_settings_[stylesheet_], theme_mod_settings_)
        # end for
        autoload_ = False
        result_ = update_option("customize_stashed_theme_mods", stashed_theme_mod_settings_, autoload_)
        if (not result_):
            return False
        # end if
        return stashed_theme_mod_settings_
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
        changeset_post_id_ = self.changeset_post_id()
        dismiss_lock_ = (not php_empty(lambda : PHP_POST["dismiss_lock"]))
        dismiss_autosave_ = (not php_empty(lambda : PHP_POST["dismiss_autosave"]))
        if dismiss_lock_:
            if php_empty(lambda : changeset_post_id_) and (not dismiss_autosave_):
                wp_send_json_error("no_changeset_to_dismiss_lock", 404)
            # end if
            if (not current_user_can(get_post_type_object("customize_changeset").cap.edit_post, changeset_post_id_)) and (not dismiss_autosave_):
                wp_send_json_error("cannot_remove_changeset_lock", 403)
            # end if
            delete_post_meta(changeset_post_id_, "_edit_lock")
            if (not dismiss_autosave_):
                wp_send_json_success("changeset_lock_dismissed")
            # end if
        # end if
        if dismiss_autosave_:
            if php_empty(lambda : changeset_post_id_) or "auto-draft" == get_post_status(changeset_post_id_):
                dismissed_ = self.dismiss_user_auto_draft_changesets()
                if dismissed_ > 0:
                    wp_send_json_success("auto_draft_dismissed")
                else:
                    wp_send_json_error("no_auto_draft_to_delete", 404)
                # end if
            else:
                revision_ = wp_get_post_autosave(changeset_post_id_, get_current_user_id())
                if revision_:
                    if (not current_user_can(get_post_type_object("customize_changeset").cap.delete_post, changeset_post_id_)):
                        wp_send_json_error("cannot_delete_autosave_revision", 403)
                    # end if
                    if (not wp_delete_post(revision_.ID, True)):
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
    def add_setting(self, id_=None, args_=None):
        if args_ is None:
            args_ = Array()
        # end if
        
        if type(id_).__name__ == "WP_Customize_Setting":
            setting_ = id_
        else:
            class_ = "WP_Customize_Setting"
            #// This filter is documented in wp-includes/class-wp-customize-manager.php
            args_ = apply_filters("customize_dynamic_setting_args", args_, id_)
            #// This filter is documented in wp-includes/class-wp-customize-manager.php
            class_ = apply_filters("customize_dynamic_setting_class", class_, id_, args_)
            setting_ = php_new_class(class_, lambda : {**locals(), **globals()}[class_](self, id_, args_))
        # end if
        self.settings[setting_.id] = setting_
        return setting_
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
    def add_dynamic_settings(self, setting_ids_=None):
        
        
        new_settings_ = Array()
        for setting_id_ in setting_ids_:
            #// Skip settings already created.
            if self.get_setting(setting_id_):
                continue
            # end if
            setting_args_ = False
            setting_class_ = "WP_Customize_Setting"
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
            setting_args_ = apply_filters("customize_dynamic_setting_args", setting_args_, setting_id_)
            if False == setting_args_:
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
            setting_class_ = apply_filters("customize_dynamic_setting_class", setting_class_, setting_id_, setting_args_)
            setting_ = php_new_class(setting_class_, lambda : {**locals(), **globals()}[setting_class_](self, setting_id_, setting_args_))
            self.add_setting(setting_)
            new_settings_[-1] = setting_
        # end for
        return new_settings_
    # end def add_dynamic_settings
    #// 
    #// Retrieve a customize setting.
    #// 
    #// @since 3.4.0
    #// 
    #// @param string $id Customize Setting ID.
    #// @return WP_Customize_Setting|void The setting, if set.
    #//
    def get_setting(self, id_=None):
        
        
        if (php_isset(lambda : self.settings[id_])):
            return self.settings[id_]
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
    def remove_setting(self, id_=None):
        
        
        self.settings[id_] = None
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
    def add_panel(self, id_=None, args_=None):
        if args_ is None:
            args_ = Array()
        # end if
        
        if type(id_).__name__ == "WP_Customize_Panel":
            panel_ = id_
        else:
            panel_ = php_new_class("WP_Customize_Panel", lambda : WP_Customize_Panel(self, id_, args_))
        # end if
        self.panels[panel_.id] = panel_
        return panel_
    # end def add_panel
    #// 
    #// Retrieve a customize panel.
    #// 
    #// @since 4.0.0
    #// 
    #// @param string $id Panel ID to get.
    #// @return WP_Customize_Panel|void Requested panel instance, if set.
    #//
    def get_panel(self, id_=None):
        
        
        if (php_isset(lambda : self.panels[id_])):
            return self.panels[id_]
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
    def remove_panel(self, id_=None):
        
        
        #// Removing core components this way is _doing_it_wrong().
        if php_in_array(id_, self.components, True):
            message_ = php_sprintf(__("Removing %1$s manually will cause PHP warnings. Use the %2$s filter instead."), id_, "<a href=\"" + esc_url("https://developer.wordpress.org/reference/hooks/customize_loaded_components/") + "\"><code>customize_loaded_components</code></a>")
            _doing_it_wrong(__METHOD__, message_, "4.5.0")
        # end if
        self.panels[id_] = None
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
    def register_panel_type(self, panel_=None):
        
        
        self.registered_panel_types[-1] = panel_
    # end def register_panel_type
    #// 
    #// Render JS templates for all registered panel types.
    #// 
    #// @since 4.3.0
    #//
    def render_panel_templates(self):
        
        
        for panel_type_ in self.registered_panel_types:
            panel_ = php_new_class(panel_type_, lambda : {**locals(), **globals()}[panel_type_](self, "temp", Array()))
            panel_.print_template()
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
    def add_section(self, id_=None, args_=None):
        if args_ is None:
            args_ = Array()
        # end if
        
        if type(id_).__name__ == "WP_Customize_Section":
            section_ = id_
        else:
            section_ = php_new_class("WP_Customize_Section", lambda : WP_Customize_Section(self, id_, args_))
        # end if
        self.sections[section_.id] = section_
        return section_
    # end def add_section
    #// 
    #// Retrieve a customize section.
    #// 
    #// @since 3.4.0
    #// 
    #// @param string $id Section ID.
    #// @return WP_Customize_Section|void The section, if set.
    #//
    def get_section(self, id_=None):
        
        
        if (php_isset(lambda : self.sections[id_])):
            return self.sections[id_]
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
    def remove_section(self, id_=None):
        
        
        self.sections[id_] = None
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
    def register_section_type(self, section_=None):
        
        
        self.registered_section_types[-1] = section_
    # end def register_section_type
    #// 
    #// Render JS templates for all registered section types.
    #// 
    #// @since 4.3.0
    #//
    def render_section_templates(self):
        
        
        for section_type_ in self.registered_section_types:
            section_ = php_new_class(section_type_, lambda : {**locals(), **globals()}[section_type_](self, "temp", Array()))
            section_.print_template()
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
    def add_control(self, id_=None, args_=None):
        if args_ is None:
            args_ = Array()
        # end if
        
        if type(id_).__name__ == "WP_Customize_Control":
            control_ = id_
        else:
            control_ = php_new_class("WP_Customize_Control", lambda : WP_Customize_Control(self, id_, args_))
        # end if
        self.controls[control_.id] = control_
        return control_
    # end def add_control
    #// 
    #// Retrieve a customize control.
    #// 
    #// @since 3.4.0
    #// 
    #// @param string $id ID of the control.
    #// @return WP_Customize_Control|void The control object, if set.
    #//
    def get_control(self, id_=None):
        
        
        if (php_isset(lambda : self.controls[id_])):
            return self.controls[id_]
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
    def remove_control(self, id_=None):
        
        
        self.controls[id_] = None
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
    def register_control_type(self, control_=None):
        
        
        self.registered_control_types[-1] = control_
    # end def register_control_type
    #// 
    #// Render JS templates for all registered control types.
    #// 
    #// @since 4.1.0
    #//
    def render_control_templates(self):
        
        
        if self.branching():
            l10n_ = Array({"locked": __("%s is already customizing this changeset. Please wait until they are done to try customizing. Your latest changes have been autosaved."), "locked_allow_override": __("%s is already customizing this changeset. Do you want to take over?")})
        else:
            l10n_ = Array({"locked": __("%s is already customizing this site. Please wait until they are done to try customizing. Your latest changes have been autosaved."), "locked_allow_override": __("%s is already customizing this site. Do you want to take over?")})
        # end if
        for control_type_ in self.registered_control_types:
            control_ = php_new_class(control_type_, lambda : {**locals(), **globals()}[control_type_](self, "temp", Array({"settings": Array()})))
            control_.print_template()
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
        php_print(esc_html(php_sprintf(l10n_["locked_allow_override"], "{{ data.lockUser.name }}")))
        php_print("                     <# } else { #>\n                            ")
        php_print(esc_html(php_sprintf(l10n_["locked"], "{{ data.lockUser.name }}")))
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
    def _cmp_priority(self, a_=None, b_=None):
        
        
        _deprecated_function(__METHOD__, "4.7.0", "wp_list_sort")
        if a_.priority == b_.priority:
            return a_.instance_number - b_.instance_number
        else:
            return a_.priority - b_.priority
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
        
        
        controls_ = Array()
        self.controls = wp_list_sort(self.controls, Array({"priority": "ASC", "instance_number": "ASC"}), "ASC", True)
        for id_,control_ in self.controls:
            if (not (php_isset(lambda : self.sections[control_.section]))) or (not control_.check_capabilities()):
                continue
            # end if
            self.sections[control_.section].controls[-1] = control_
            controls_[id_] = control_
        # end for
        self.controls = controls_
        #// Prepare sections.
        self.sections = wp_list_sort(self.sections, Array({"priority": "ASC", "instance_number": "ASC"}), "ASC", True)
        sections_ = Array()
        for section_ in self.sections:
            if (not section_.check_capabilities()):
                continue
            # end if
            section_.controls = wp_list_sort(section_.controls, Array({"priority": "ASC", "instance_number": "ASC"}))
            if (not section_.panel):
                #// Top-level section.
                sections_[section_.id] = section_
            else:
                #// This section belongs to a panel.
                if (php_isset(lambda : self.panels[section_.panel])):
                    self.panels[section_.panel].sections[section_.id] = section_
                # end if
            # end if
        # end for
        self.sections = sections_
        #// Prepare panels.
        self.panels = wp_list_sort(self.panels, Array({"priority": "ASC", "instance_number": "ASC"}), "ASC", True)
        panels_ = Array()
        for panel_ in self.panels:
            if (not panel_.check_capabilities()):
                continue
            # end if
            panel_.sections = wp_list_sort(panel_.sections, Array({"priority": "ASC", "instance_number": "ASC"}), "ASC", True)
            panels_[panel_.id] = panel_
        # end for
        self.panels = panels_
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
        
        
        for control_ in self.controls:
            control_.enqueue()
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
            document_title_tmpl_ = __("Customize: %s")
        else:
            #// translators: %s: Document title from the preview.
            document_title_tmpl_ = __("Live Preview: %s")
        # end if
        document_title_tmpl_ = html_entity_decode(document_title_tmpl_, ENT_QUOTES, "UTF-8")
        #// Because exported to JS and assigned to document.title.
        return document_title_tmpl_
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
    def set_preview_url(self, preview_url_=None):
        
        
        preview_url_ = esc_url_raw(preview_url_)
        self.preview_url = wp_validate_redirect(preview_url_, home_url("/"))
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
            preview_url_ = home_url("/")
        else:
            preview_url_ = self.preview_url
        # end if
        return preview_url_
    # end def get_preview_url
    #// 
    #// Determines whether the admin and the frontend are on different domains.
    #// 
    #// @since 4.7.0
    #// 
    #// @return bool Whether cross-domain.
    #//
    def is_cross_domain(self):
        
        
        admin_origin_ = wp_parse_url(admin_url())
        home_origin_ = wp_parse_url(home_url())
        cross_domain_ = php_strtolower(admin_origin_["host"]) != php_strtolower(home_origin_["host"])
        return cross_domain_
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
        
        
        allowed_urls_ = Array(home_url("/"))
        if is_ssl() and (not self.is_cross_domain()):
            allowed_urls_[-1] = home_url("/", "https")
        # end if
        #// 
        #// Filters the list of URLs allowed to be clicked and followed in the Customizer preview.
        #// 
        #// @since 3.4.0
        #// 
        #// @param string[] $allowed_urls An array of allowed URLs.
        #//
        allowed_urls_ = array_unique(apply_filters("customize_allowed_urls", allowed_urls_))
        return allowed_urls_
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
    def set_return_url(self, return_url_=None):
        
        
        return_url_ = esc_url_raw(return_url_)
        return_url_ = remove_query_arg(wp_removable_query_args(), return_url_)
        return_url_ = wp_validate_redirect(return_url_)
        self.return_url = return_url_
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
        
        
        global _registered_pages_
        php_check_if_defined("_registered_pages_")
        referer_ = wp_get_referer()
        excluded_referer_basenames_ = Array("customize.php", "wp-login.php")
        if self.return_url:
            return_url_ = self.return_url
        elif referer_ and (not php_in_array(wp_basename(php_parse_url(referer_, PHP_URL_PATH)), excluded_referer_basenames_, True)):
            return_url_ = referer_
        elif self.preview_url:
            return_url_ = self.preview_url
        else:
            return_url_ = home_url("/")
        # end if
        return_url_basename_ = wp_basename(php_parse_url(self.return_url, PHP_URL_PATH))
        return_url_query_ = php_parse_url(self.return_url, PHP_URL_QUERY)
        if "themes.php" == return_url_basename_ and return_url_query_:
            parse_str(return_url_query_, query_vars_)
            #// 
            #// If the return URL is a page added by a theme to the Appearance menu via add_submenu_page(),
            #// verify that belongs to the active theme, otherwise fall back to the Themes screen.
            #//
            if (php_isset(lambda : query_vars_["page"])) and (not (php_isset(lambda : _registered_pages_[str("appearance_page_") + str(query_vars_["page"])]))):
                return_url_ = admin_url("themes.php")
            # end if
        # end if
        return return_url_
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
    def set_autofocus(self, autofocus_=None):
        
        
        self.autofocus = php_array_filter(wp_array_slice_assoc(autofocus_, Array("panel", "section", "control")), "is_string")
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
        
        
        nonces_ = Array({"save": wp_create_nonce("save-customize_" + self.get_stylesheet()), "preview": wp_create_nonce("preview-customize_" + self.get_stylesheet()), "switch_themes": wp_create_nonce("switch_themes"), "dismiss_autosave_or_lock": wp_create_nonce("customize_dismiss_autosave_or_lock"), "override_lock": wp_create_nonce("customize_override_changeset_lock"), "trash": wp_create_nonce("trash_customize_changeset")})
        #// 
        #// Filters nonces for Customizer.
        #// 
        #// @since 4.2.0
        #// 
        #// @param string[]             $nonces Array of refreshed nonces for save and
        #// preview actions.
        #// @param WP_Customize_Manager $this   WP_Customize_Manager instance.
        #//
        nonces_ = apply_filters("customize_refresh_nonces", nonces_, self)
        return nonces_
    # end def get_nonces
    #// 
    #// Print JavaScript settings for parent window.
    #// 
    #// @since 4.4.0
    #//
    def customize_pane_settings(self):
        
        
        login_url_ = add_query_arg(Array({"interim-login": 1, "customize-login": 1}), wp_login_url())
        #// Ensure dirty flags are set for modified settings.
        for setting_id_ in php_array_keys(self.unsanitized_post_values()):
            setting_ = self.get_setting(setting_id_)
            if setting_:
                setting_.dirty = True
            # end if
        # end for
        autosave_revision_post_ = None
        autosave_autodraft_post_ = None
        changeset_post_id_ = self.changeset_post_id()
        if (not self.saved_starter_content_changeset) and (not self.autosaved()):
            if changeset_post_id_:
                if is_user_logged_in():
                    autosave_revision_post_ = wp_get_post_autosave(changeset_post_id_, get_current_user_id())
                # end if
            else:
                autosave_autodraft_posts_ = self.get_changeset_posts(Array({"posts_per_page": 1, "post_status": "auto-draft", "exclude_restore_dismissed": True}))
                if (not php_empty(lambda : autosave_autodraft_posts_)):
                    autosave_autodraft_post_ = php_array_shift(autosave_autodraft_posts_)
                # end if
            # end if
        # end if
        current_user_can_publish_ = current_user_can(get_post_type_object("customize_changeset").cap.publish_posts)
        #// @todo Include all of the status labels here from script-loader.php, and then allow it to be filtered.
        status_choices_ = Array()
        if current_user_can_publish_:
            status_choices_[-1] = Array({"status": "publish", "label": __("Publish")})
        # end if
        status_choices_[-1] = Array({"status": "draft", "label": __("Save Draft")})
        if current_user_can_publish_:
            status_choices_[-1] = Array({"status": "future", "label": _x("Schedule", "customizer changeset action/button label")})
        # end if
        #// Prepare Customizer settings to pass to JavaScript.
        changeset_post_ = None
        if changeset_post_id_:
            changeset_post_ = get_post(changeset_post_id_)
        # end if
        #// Determine initial date to be at present or future, not past.
        current_time_ = current_time("mysql", False)
        initial_date_ = current_time_
        if changeset_post_:
            initial_date_ = get_the_time("Y-m-d H:i:s", changeset_post_.ID)
            if initial_date_ < current_time_:
                initial_date_ = current_time_
            # end if
        # end if
        lock_user_id_ = False
        if self.changeset_post_id():
            lock_user_id_ = wp_check_post_lock(self.changeset_post_id())
        # end if
        settings_ = Array({"changeset": Array({"uuid": self.changeset_uuid(), "branching": self.branching(), "autosaved": self.autosaved(), "hasAutosaveRevision": (not php_empty(lambda : autosave_revision_post_)), "latestAutoDraftUuid": autosave_autodraft_post_.post_name if autosave_autodraft_post_ else None, "status": changeset_post_.post_status if changeset_post_ else "", "currentUserCanPublish": current_user_can_publish_, "publishDate": initial_date_, "statusChoices": status_choices_, "lockUser": self.get_lock_user_data(lock_user_id_) if lock_user_id_ else None})}, {"initialServerDate": current_time_, "dateFormat": get_option("date_format"), "timeFormat": get_option("time_format"), "initialServerTimestamp": floor(php_microtime(True) * 1000), "initialClientTimestamp": -1, "timeouts": Array({"windowRefresh": 250, "changesetAutoSave": AUTOSAVE_INTERVAL * 1000, "keepAliveCheck": 2500, "reflowPaneContents": 100, "previewFrameSensitivity": 2000})}, {"theme": Array({"stylesheet": self.get_stylesheet(), "active": self.is_theme_active(), "_canInstall": current_user_can("install_themes")})}, {"url": Array({"preview": esc_url_raw(self.get_preview_url()), "return": esc_url_raw(self.get_return_url()), "parent": esc_url_raw(admin_url()), "activated": esc_url_raw(home_url("/")), "ajax": esc_url_raw(admin_url("admin-ajax.php", "relative")), "allowed": php_array_map("esc_url_raw", self.get_allowed_urls()), "isCrossDomain": self.is_cross_domain(), "home": esc_url_raw(home_url("/")), "login": esc_url_raw(login_url_)})}, {"browser": Array({"mobile": wp_is_mobile(), "ios": self.is_ios()})}, {"panels": Array(), "sections": Array(), "nonce": self.get_nonces(), "autofocus": self.get_autofocus(), "documentTitleTmpl": self.get_document_title_template(), "previewableDevices": self.get_previewable_devices(), "l10n": Array({"confirmDeleteTheme": __("Are you sure you want to delete this theme?"), "themeSearchResults": __("%d themes found"), "announceThemeCount": __("Displaying %d themes"), "announceThemeDetails": __("Showing details for theme: %s")})})
        #// Temporarily disable installation in Customizer. See #42184.
        filesystem_method_ = get_filesystem_method()
        ob_start()
        filesystem_credentials_are_stored_ = request_filesystem_credentials(self_admin_url())
        ob_end_clean()
        if "direct" != filesystem_method_ and (not filesystem_credentials_are_stored_):
            settings_["theme"]["_filesystemCredentialsNeeded"] = True
        # end if
        #// Prepare Customize Section objects to pass to JavaScript.
        for id_,section_ in self.sections():
            if section_.check_capabilities():
                settings_["sections"][id_] = section_.json()
            # end if
        # end for
        #// Prepare Customize Panel objects to pass to JavaScript.
        for panel_id_,panel_ in self.panels():
            if panel_.check_capabilities():
                settings_["panels"][panel_id_] = panel_.json()
                for section_id_,section_ in panel_.sections:
                    if section_.check_capabilities():
                        settings_["sections"][section_id_] = section_.json()
                    # end if
                # end for
            # end if
        # end for
        php_print("     <script type=\"text/javascript\">\n         var _wpCustomizeSettings = ")
        php_print(wp_json_encode(settings_))
        php_print(""";
        _wpCustomizeSettings.initialClientTimestamp = _.now();
        _wpCustomizeSettings.controls = {};
        _wpCustomizeSettings.settings = {};
        """)
        #// Serialize settings one by one to improve memory usage.
        php_print("(function ( s ){\n")
        for setting_ in self.settings():
            if setting_.check_capabilities():
                printf("s[%s] = %s;\n", wp_json_encode(setting_.id), wp_json_encode(setting_.json()))
            # end if
        # end for
        php_print("})( _wpCustomizeSettings.settings );\n")
        #// Serialize controls one by one to improve memory usage.
        php_print("(function ( c ){\n")
        for control_ in self.controls():
            if control_.check_capabilities():
                printf("c[%s] = %s;\n", wp_json_encode(control_.id), wp_json_encode(control_.json()))
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
        
        
        devices_ = Array({"desktop": Array({"label": __("Enter desktop preview mode"), "default": True})}, {"tablet": Array({"label": __("Enter tablet preview mode")})}, {"mobile": Array({"label": __("Enter mobile preview mode")})})
        #// 
        #// Filters the available devices to allow previewing in the Customizer.
        #// 
        #// @since 4.5.0
        #// 
        #// @see WP_Customize_Manager::get_previewable_devices()
        #// 
        #// @param array $devices List of devices with labels and default setting.
        #//
        devices_ = apply_filters("customize_previewable_devices", devices_)
        return devices_
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
        custom_logo_args_ = get_theme_support("custom-logo")
        self.add_control(php_new_class("WP_Customize_Cropped_Image_Control", lambda : WP_Customize_Cropped_Image_Control(self, "custom_logo", Array({"label": __("Logo"), "section": "title_tagline", "priority": 8, "height": custom_logo_args_[0]["height"] if (php_isset(lambda : custom_logo_args_[0]["height"])) else None, "width": custom_logo_args_[0]["width"] if (php_isset(lambda : custom_logo_args_[0]["width"])) else None, "flex_height": custom_logo_args_[0]["flex-height"] if (php_isset(lambda : custom_logo_args_[0]["flex-height"])) else None, "flex_width": custom_logo_args_[0]["flex-width"] if (php_isset(lambda : custom_logo_args_[0]["flex-width"])) else None, "button_labels": Array({"select": __("Select logo"), "change": __("Change logo"), "remove": __("Remove"), "default": __("Default"), "placeholder": __("No logo selected"), "frame_title": __("Select logo"), "frame_button": __("Choose logo")})}))))
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
            title_ = __("Header Media")
            description_ = "<p>" + __("If you add a video, the image will be used as a fallback while the video loads.") + "</p>"
            width_ = absint(get_theme_support("custom-header", "width"))
            height_ = absint(get_theme_support("custom-header", "height"))
            if width_ and height_:
                control_description_ = php_sprintf(__("Upload your video in %1$s format and minimize its file size for best results. Your theme recommends dimensions of %2$s pixels."), "<code>.mp4</code>", php_sprintf("<strong>%s &times; %s</strong>", width_, height_))
            elif width_:
                control_description_ = php_sprintf(__("Upload your video in %1$s format and minimize its file size for best results. Your theme recommends a width of %2$s pixels."), "<code>.mp4</code>", php_sprintf("<strong>%s</strong>", width_))
            else:
                control_description_ = php_sprintf(__("Upload your video in %1$s format and minimize its file size for best results. Your theme recommends a height of %2$s pixels."), "<code>.mp4</code>", php_sprintf("<strong>%s</strong>", height_))
            # end if
        else:
            title_ = __("Header Image")
            description_ = ""
            control_description_ = ""
        # end if
        self.add_section("header_image", Array({"title": title_, "description": description_, "theme_supports": "custom-header", "priority": 60}))
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
        self.add_control(php_new_class("WP_Customize_Media_Control", lambda : WP_Customize_Media_Control(self, "header_video", Array({"theme_supports": Array("custom-header", "video"), "label": __("Header Video"), "description": control_description_, "section": "header_image", "mime_type": "video", "active_callback": "is_header_video_active"}))))
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
            for prop_ in Array("color", "image", "preset", "position_x", "position_y", "size", "repeat", "attachment"):
                self.get_setting("background_" + prop_).transport = "postMessage"
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
        section_description_ = "<p>"
        section_description_ += __("Add your own CSS code here to customize the appearance and layout of your site.")
        section_description_ += php_sprintf(" <a href=\"%1$s\" class=\"external-link\" target=\"_blank\">%2$s<span class=\"screen-reader-text\"> %3$s</span></a>", esc_url(__("https://codex.wordpress.org/CSS")), __("Learn more about CSS"), __("(opens in a new tab)"))
        section_description_ += "</p>"
        section_description_ += "<p id=\"editor-keyboard-trap-help-1\">" + __("When using a keyboard to navigate:") + "</p>"
        section_description_ += "<ul>"
        section_description_ += "<li id=\"editor-keyboard-trap-help-2\">" + __("In the editing area, the Tab key enters a tab character.") + "</li>"
        section_description_ += "<li id=\"editor-keyboard-trap-help-3\">" + __("To move away from this area, press the Esc key followed by the Tab key.") + "</li>"
        section_description_ += "<li id=\"editor-keyboard-trap-help-4\">" + __("Screen reader users: when in forms mode, you may need to press the Esc key twice.") + "</li>"
        section_description_ += "</ul>"
        if "false" != wp_get_current_user().syntax_highlighting:
            section_description_ += "<p>"
            section_description_ += php_sprintf(__("The edit field automatically highlights code syntax. You can disable this in your <a href=\"%1$s\" %2$s>user profile%3$s</a> to work in plain text mode."), esc_url(get_edit_profile_url()), "class=\"external-link\" target=\"_blank\"", php_sprintf("<span class=\"screen-reader-text\"> %s</span>", __("(opens in a new tab)")))
            section_description_ += "</p>"
        # end if
        section_description_ += "<p class=\"section-description-buttons\">"
        section_description_ += "<button type=\"button\" class=\"button-link section-description-close\">" + __("Close") + "</button>"
        section_description_ += "</p>"
        self.add_section("custom_css", Array({"title": __("Additional CSS"), "priority": 200, "description_hidden": True, "description": section_description_}))
        custom_css_setting_ = php_new_class("WP_Customize_Custom_CSS_Setting", lambda : WP_Customize_Custom_CSS_Setting(self, php_sprintf("custom_css[%s]", get_stylesheet()), Array({"capability": "edit_css", "default": ""})))
        self.add_setting(custom_css_setting_)
        self.add_control(php_new_class("WP_Customize_Code_Editor_Control", lambda : WP_Customize_Code_Editor_Control(self, "custom_css", Array({"label": __("CSS code"), "section": "custom_css", "settings": Array({"default": custom_css_setting_.id})}, {"code_type": "text/css", "input_attrs": Array({"aria-describedby": "editor-keyboard-trap-help-1 editor-keyboard-trap-help-2 editor-keyboard-trap-help-3 editor-keyboard-trap-help-4"})}))))
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
        
        
        setting_ = self.get_setting("nav_menus_created_posts")
        if setting_:
            for post_id_ in setting_.value():
                if "page" == get_post_type(post_id_):
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
        
        
        setting_ids_ = php_array_keys(self.unsanitized_post_values())
        self.add_dynamic_settings(setting_ids_)
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
        theme_action_ = sanitize_key(PHP_POST["theme_action"])
        themes_ = Array()
        args_ = Array()
        #// Define query filters based on user input.
        if (not php_array_key_exists("search", PHP_POST)):
            args_["search"] = ""
        else:
            args_["search"] = sanitize_text_field(wp_unslash(PHP_POST["search"]))
        # end if
        if (not php_array_key_exists("tags", PHP_POST)):
            args_["tag"] = ""
        else:
            args_["tag"] = php_array_map("sanitize_text_field", wp_unslash(PHP_POST["tags"]))
        # end if
        if (not php_array_key_exists("page", PHP_POST)):
            args_["page"] = 1
        else:
            args_["page"] = absint(PHP_POST["page"])
        # end if
        php_include_file(ABSPATH + "wp-admin/includes/theme.php", once=True)
        if "installed" == theme_action_:
            #// Load all installed themes from wp_prepare_themes_for_js().
            themes_ = Array({"themes": wp_prepare_themes_for_js()})
            for theme_ in themes_["themes"]:
                theme_["type"] = "installed"
                theme_["active"] = (php_isset(lambda : PHP_POST["customized_theme"])) and PHP_POST["customized_theme"] == theme_["id"]
            # end for
        elif "wporg" == theme_action_:
            #// Load WordPress.org themes from the .org API and normalize data to match installed theme objects.
            if (not current_user_can("install_themes")):
                wp_die(-1)
            # end if
            #// Arguments for all queries.
            wporg_args_ = Array({"per_page": 100, "fields": Array({"reviews_url": True})})
            args_ = php_array_merge(wporg_args_, args_)
            if "" == args_["search"] and "" == args_["tag"]:
                args_["browse"] = "new"
                pass
            # end if
            #// Load themes from the .org API.
            themes_ = themes_api("query_themes", args_)
            if is_wp_error(themes_):
                wp_send_json_error()
            # end if
            #// This list matches the allowed tags in wp-admin/includes/theme-install.php.
            themes_allowedtags_ = php_array_fill_keys(Array("a", "abbr", "acronym", "code", "pre", "em", "strong", "div", "p", "ul", "ol", "li", "h1", "h2", "h3", "h4", "h5", "h6", "img"), Array())
            themes_allowedtags_["a"] = php_array_fill_keys(Array("href", "title", "target"), True)
            themes_allowedtags_["acronym"]["title"] = True
            themes_allowedtags_["abbr"]["title"] = True
            themes_allowedtags_["img"] = php_array_fill_keys(Array("src", "class", "alt"), True)
            #// Prepare a list of installed themes to check against before the loop.
            installed_themes_ = Array()
            wp_themes_ = wp_get_themes()
            for theme_ in wp_themes_:
                installed_themes_[-1] = theme_.get_stylesheet()
            # end for
            update_php_ = network_admin_url("update.php?action=install-theme")
            #// Set up properties for themes available on WordPress.org.
            for theme_ in themes_.themes:
                theme_.install_url = add_query_arg(Array({"theme": theme_.slug, "_wpnonce": wp_create_nonce("install-theme_" + theme_.slug)}), update_php_)
                theme_.name = wp_kses(theme_.name, themes_allowedtags_)
                theme_.version = wp_kses(theme_.version, themes_allowedtags_)
                theme_.description = wp_kses(theme_.description, themes_allowedtags_)
                theme_.stars = wp_star_rating(Array({"rating": theme_.rating, "type": "percent", "number": theme_.num_ratings, "echo": False}))
                theme_.num_ratings = number_format_i18n(theme_.num_ratings)
                theme_.preview_url = set_url_scheme(theme_.preview_url)
                #// Handle themes that are already installed as installed themes.
                if php_in_array(theme_.slug, installed_themes_, True):
                    theme_.type = "installed"
                else:
                    theme_.type = theme_action_
                # end if
                #// Set active based on customized theme.
                theme_.active = (php_isset(lambda : PHP_POST["customized_theme"])) and PHP_POST["customized_theme"] == theme_.slug
                #// Map available theme properties to installed theme properties.
                theme_.id = theme_.slug
                theme_.screenshot = Array(theme_.screenshot_url)
                theme_.authorAndUri = wp_kses(theme_.author["display_name"], themes_allowedtags_)
                if (php_isset(lambda : theme_.parent)):
                    theme_.parent = theme_.parent["slug"]
                else:
                    theme_.parent = False
                # end if
                theme_.slug = None
                theme_.screenshot_url = None
                theme_.author = None
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
        themes_ = apply_filters("customize_load_themes", themes_, args_, self)
        wp_send_json_success(themes_)
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
    def _sanitize_header_textcolor(self, color_=None):
        
        
        if "blank" == color_:
            return "blank"
        # end if
        color_ = sanitize_hex_color_no_hash(color_)
        if php_empty(lambda : color_):
            color_ = get_theme_support("custom-header", "default-text-color")
        # end if
        return color_
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
    def _sanitize_background_setting(self, value_=None, setting_=None):
        
        
        if "background_repeat" == setting_.id:
            if (not php_in_array(value_, Array("repeat-x", "repeat-y", "repeat", "no-repeat"))):
                return php_new_class("WP_Error", lambda : WP_Error("invalid_value", __("Invalid value for background repeat.")))
            # end if
        elif "background_attachment" == setting_.id:
            if (not php_in_array(value_, Array("fixed", "scroll"))):
                return php_new_class("WP_Error", lambda : WP_Error("invalid_value", __("Invalid value for background attachment.")))
            # end if
        elif "background_position_x" == setting_.id:
            if (not php_in_array(value_, Array("left", "center", "right"), True)):
                return php_new_class("WP_Error", lambda : WP_Error("invalid_value", __("Invalid value for background position X.")))
            # end if
        elif "background_position_y" == setting_.id:
            if (not php_in_array(value_, Array("top", "center", "bottom"), True)):
                return php_new_class("WP_Error", lambda : WP_Error("invalid_value", __("Invalid value for background position Y.")))
            # end if
        elif "background_size" == setting_.id:
            if (not php_in_array(value_, Array("auto", "contain", "cover"), True)):
                return php_new_class("WP_Error", lambda : WP_Error("invalid_value", __("Invalid value for background size.")))
            # end if
        elif "background_preset" == setting_.id:
            if (not php_in_array(value_, Array("default", "fill", "fit", "repeat", "custom"), True)):
                return php_new_class("WP_Error", lambda : WP_Error("invalid_value", __("Invalid value for background size.")))
            # end if
        elif "background_image" == setting_.id or "background_image_thumb" == setting_.id:
            value_ = "" if php_empty(lambda : value_) else esc_url_raw(value_)
        else:
            return php_new_class("WP_Error", lambda : WP_Error("unrecognized_setting", __("Unrecognized background setting.")))
        # end if
        return value_
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
    def export_header_video_settings(self, response_=None, selective_refresh_=None, partials_=None):
        
        
        if (php_isset(lambda : partials_["custom_header"])):
            response_["custom_header_settings"] = get_header_video_settings()
        # end if
        return response_
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
    def _validate_header_video(self, validity_=None, value_=None):
        
        
        video_ = get_attached_file(absint(value_))
        if video_:
            size_ = filesize(video_)
            if size_ > 8 * MB_IN_BYTES:
                validity_.add("size_too_large", __("This video file is too large to use as a header video. Try a shorter video or optimize the compression settings and re-upload a file that is less than 8MB. Or, upload your video to YouTube and link it with the option below."))
            # end if
            if ".mp4" != php_substr(video_, -4) and ".mov" != php_substr(video_, -4):
                #// Check for .mp4 or .mov format, which (assuming h.264 encoding) are the only cross-browser-supported formats.
                validity_.add("invalid_file_type", php_sprintf(__("Only %1$s or %2$s files may be used for header video. Please convert your video file and try again, or, upload your video to YouTube and link it with the option below."), "<code>.mp4</code>", "<code>.mov</code>"))
            # end if
        # end if
        return validity_
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
    def _validate_external_header_video(self, validity_=None, value_=None):
        
        
        video_ = esc_url_raw(value_)
        if video_:
            if (not php_preg_match("#^https?://(?:www\\.)?(?:youtube\\.com/watch|youtu\\.be/)#", video_)):
                validity_.add("invalid_url", __("Please enter a valid YouTube URL."))
            # end if
        # end if
        return validity_
    # end def _validate_external_header_video
    #// 
    #// Callback for sanitizing the external_header_video value.
    #// 
    #// @since 4.7.1
    #// 
    #// @param string $value URL.
    #// @return string Sanitized URL.
    #//
    def _sanitize_external_header_video(self, value_=None):
        
        
        return esc_url_raw(php_trim(value_))
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
