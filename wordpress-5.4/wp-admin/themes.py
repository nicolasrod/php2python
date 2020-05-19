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
#// Themes administration panel.
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// WordPress Administration Bootstrap
php_include_file(__DIR__ + "/admin.php", once=True)
if (not current_user_can("switch_themes")) and (not current_user_can("edit_theme_options")):
    wp_die("<h1>" + __("You need a higher level of permission.") + "</h1>" + "<p>" + __("Sorry, you are not allowed to edit theme options on this site.") + "</p>", 403)
# end if
if current_user_can("switch_themes") and (php_isset(lambda : PHP_REQUEST["action"])):
    if "activate" == PHP_REQUEST["action"]:
        check_admin_referer("switch-theme_" + PHP_REQUEST["stylesheet"])
        theme_ = wp_get_theme(PHP_REQUEST["stylesheet"])
        if (not theme_.exists()) or (not theme_.is_allowed()):
            wp_die("<h1>" + __("Something went wrong.") + "</h1>" + "<p>" + __("The requested theme does not exist.") + "</p>", 403)
        # end if
        switch_theme(theme_.get_stylesheet())
        wp_redirect(admin_url("themes.php?activated=true"))
        php_exit(0)
    elif "resume" == PHP_REQUEST["action"]:
        check_admin_referer("resume-theme_" + PHP_REQUEST["stylesheet"])
        theme_ = wp_get_theme(PHP_REQUEST["stylesheet"])
        if (not current_user_can("resume_theme", PHP_REQUEST["stylesheet"])):
            wp_die("<h1>" + __("You need a higher level of permission.") + "</h1>" + "<p>" + __("Sorry, you are not allowed to resume this theme.") + "</p>", 403)
        # end if
        result_ = resume_theme(theme_.get_stylesheet(), self_admin_url("themes.php?error=resuming"))
        if is_wp_error(result_):
            wp_die(result_)
        # end if
        wp_redirect(admin_url("themes.php?resumed=true"))
        php_exit(0)
    elif "delete" == PHP_REQUEST["action"]:
        check_admin_referer("delete-theme_" + PHP_REQUEST["stylesheet"])
        theme_ = wp_get_theme(PHP_REQUEST["stylesheet"])
        if (not current_user_can("delete_themes")):
            wp_die("<h1>" + __("You need a higher level of permission.") + "</h1>" + "<p>" + __("Sorry, you are not allowed to delete this item.") + "</p>", 403)
        # end if
        if (not theme_.exists()):
            wp_die("<h1>" + __("Something went wrong.") + "</h1>" + "<p>" + __("The requested theme does not exist.") + "</p>", 403)
        # end if
        active_ = wp_get_theme()
        if active_.get("Template") == PHP_REQUEST["stylesheet"]:
            wp_redirect(admin_url("themes.php?delete-active-child=true"))
        else:
            delete_theme(PHP_REQUEST["stylesheet"])
            wp_redirect(admin_url("themes.php?deleted=true"))
        # end if
        php_exit(0)
    # end if
# end if
title_ = __("Manage Themes")
parent_file_ = "themes.php"
#// Help tab: Overview.
if current_user_can("switch_themes"):
    help_overview_ = "<p>" + __("This screen is used for managing your installed themes. Aside from the default theme(s) included with your WordPress installation, themes are designed and developed by third parties.") + "</p>" + "<p>" + __("From this screen you can:") + "</p>" + "<ul><li>" + __("Hover or tap to see Activate and Live Preview buttons") + "</li>" + "<li>" + __("Click on the theme to see the theme name, version, author, description, tags, and the Delete link") + "</li>" + "<li>" + __("Click Customize for the current theme or Live Preview for any other theme to see a live preview") + "</li></ul>" + "<p>" + __("The current theme is displayed highlighted as the first theme.") + "</p>" + "<p>" + __("The search for installed themes will search for terms in their name, description, author, or tag.") + " <span id=\"live-search-desc\">" + __("The search results will be updated as you type.") + "</span></p>"
    get_current_screen().add_help_tab(Array({"id": "overview", "title": __("Overview"), "content": help_overview_}))
# end if
#// End if 'switch_themes'.
#// Help tab: Adding Themes.
if current_user_can("install_themes"):
    if is_multisite():
        help_install_ = "<p>" + __("Installing themes on Multisite can only be done from the Network Admin section.") + "</p>"
    else:
        help_install_ = "<p>" + php_sprintf(__("If you would like to see more themes to choose from, click on the &#8220;Add New&#8221; button and you will be able to browse or search for additional themes from the <a href=\"%s\">WordPress Theme Directory</a>. Themes in the WordPress Theme Directory are designed and developed by third parties, and are compatible with the license WordPress uses. Oh, and they&#8217;re free!"), __("https://wordpress.org/themes/")) + "</p>"
    # end if
    get_current_screen().add_help_tab(Array({"id": "adding-themes", "title": __("Adding Themes"), "content": help_install_}))
# end if
#// End if 'install_themes'.
#// Help tab: Previewing and Customizing.
if current_user_can("edit_theme_options") and current_user_can("customize"):
    help_customize_ = "<p>" + __("Tap or hover on any theme then click the Live Preview button to see a live preview of that theme and change theme options in a separate, full-screen view. You can also find a Live Preview button at the bottom of the theme details screen. Any installed theme can be previewed and customized in this way.") + "</p>" + "<p>" + __("The theme being previewed is fully interactive &mdash; navigate to different pages to see how the theme handles posts, archives, and other page templates. The settings may differ depending on what theme features the theme being previewed supports. To accept the new settings and activate the theme all in one step, click the Publish &amp; Activate button above the menu.") + "</p>" + "<p>" + __("When previewing on smaller monitors, you can use the collapse icon at the bottom of the left-hand pane. This will hide the pane, giving you more room to preview your site in the new theme. To bring the pane back, click on the collapse icon again.") + "</p>"
    get_current_screen().add_help_tab(Array({"id": "customize-preview-themes", "title": __("Previewing and Customizing"), "content": help_customize_}))
# end if
#// End if 'edit_theme_options' && 'customize'.
get_current_screen().set_help_sidebar("<p><strong>" + __("For more information:") + "</strong></p>" + "<p>" + __("<a href=\"https://wordpress.org/support/article/using-themes/\">Documentation on Using Themes</a>") + "</p>" + "<p>" + __("<a href=\"https://wordpress.org/support/\">Support</a>") + "</p>")
if current_user_can("switch_themes"):
    themes_ = wp_prepare_themes_for_js()
else:
    themes_ = wp_prepare_themes_for_js(Array(wp_get_theme()))
# end if
wp_reset_vars(Array("theme", "search"))
wp_localize_script("theme", "_wpThemeSettings", Array({"themes": themes_, "settings": Array({"canInstall": (not is_multisite()) and current_user_can("install_themes"), "installURI": admin_url("theme-install.php") if (not is_multisite()) and current_user_can("install_themes") else None, "confirmDelete": __("Are you sure you want to delete this theme?\n\nClick 'Cancel' to go back, 'OK' to confirm the delete."), "adminUrl": php_parse_url(admin_url(), PHP_URL_PATH)})}, {"l10n": Array({"addNew": __("Add New Theme"), "search": __("Search Installed Themes"), "searchPlaceholder": __("Search installed themes..."), "themesFound": __("Number of Themes found: %d"), "noThemesFound": __("No themes found. Try a different search.")})}))
add_thickbox()
wp_enqueue_script("theme")
wp_enqueue_script("updates")
php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
php_print("\n<div class=\"wrap\">\n <h1 class=\"wp-heading-inline\">")
esc_html_e("Themes")
php_print("     <span class=\"title-count theme-count\">")
php_print(__("&hellip;") if (not php_empty(lambda : PHP_REQUEST["search"])) else php_count(themes_))
php_print("""</span>
</h1>
""")
if (not is_multisite()) and current_user_can("install_themes"):
    php_print("     <a href=\"")
    php_print(admin_url("theme-install.php"))
    php_print("\" class=\"hide-if-no-js page-title-action\">")
    php_print(esc_html_x("Add New", "theme"))
    php_print("</a>\n   ")
# end if
php_print("""
<form class=\"search-form\"></form>
<hr class=\"wp-header-end\">
""")
if (not validate_current_theme()) or (php_isset(lambda : PHP_REQUEST["broken"])):
    php_print(" <div id=\"message1\" class=\"updated notice is-dismissible\"><p>")
    _e("The active theme is broken. Reverting to the default theme.")
    php_print("</p></div>\n ")
elif (php_isset(lambda : PHP_REQUEST["activated"])):
    if (php_isset(lambda : PHP_REQUEST["previewed"])):
        php_print("     <div id=\"message2\" class=\"updated notice is-dismissible\"><p>")
        _e("Settings saved and theme activated.")
        php_print(" <a href=\"")
        php_print(home_url("/"))
        php_print("\">")
        _e("Visit site")
        php_print("</a></p></div>\n     ")
    else:
        php_print("     <div id=\"message2\" class=\"updated notice is-dismissible\"><p>")
        _e("New theme activated.")
        php_print(" <a href=\"")
        php_print(home_url("/"))
        php_print("\">")
        _e("Visit site")
        php_print("</a></p></div>\n     ")
    # end if
elif (php_isset(lambda : PHP_REQUEST["deleted"])):
    php_print(" <div id=\"message3\" class=\"updated notice is-dismissible\"><p>")
    _e("Theme deleted.")
    php_print("</p></div>\n ")
elif (php_isset(lambda : PHP_REQUEST["delete-active-child"])):
    php_print(" <div id=\"message4\" class=\"error\"><p>")
    _e("You cannot delete a theme while it has an active child theme.")
    php_print("</p></div>\n ")
elif (php_isset(lambda : PHP_REQUEST["resumed"])):
    php_print(" <div id=\"message5\" class=\"updated notice is-dismissible\"><p>")
    _e("Theme resumed.")
    php_print("</p></div>\n ")
elif (php_isset(lambda : PHP_REQUEST["error"])) and "resuming" == PHP_REQUEST["error"]:
    php_print(" <div id=\"message6\" class=\"error\"><p>")
    _e("Theme could not be resumed because it triggered a <strong>fatal error</strong>.")
    php_print("</p></div>\n ")
# end if
ct_ = wp_get_theme()
if ct_.errors() and (not is_multisite()) or current_user_can("manage_network_themes"):
    php_print("<div class=\"error\"><p>" + __("Error:") + " " + ct_.errors().get_error_message() + "</p></div>")
# end if
#// 
#// Certain error codes are less fatal than others. We can still display theme information in most cases.
#// if ( ! $ct->errors() || ( 1 == count( $ct->errors()->get_error_codes() )
#// && in_array( $ct->errors()->get_error_code(), array( 'theme_no_parent', 'theme_parent_invalid', 'theme_no_index' ) ) ) ) : ?>
#// 
#// Pretend you didn't see this.
current_theme_actions_ = Array()
if php_is_array(submenu_) and (php_isset(lambda : submenu_["themes.php"])):
    for item_ in submenu_["themes.php"]:
        class_ = ""
        if "themes.php" == item_[2] or "theme-editor.php" == item_[2] or 0 == php_strpos(item_[2], "customize.php"):
            continue
        # end if
        #// 0 = name, 1 = capability, 2 = file.
        if strcmp(self_, item_[2]) == 0 and php_empty(lambda : parent_file_) or parent_file_ and item_[2] == parent_file_:
            class_ = " current"
        # end if
        if (not php_empty(lambda : submenu_[item_[2]])):
            submenu_[item_[2]] = php_array_values(submenu_[item_[2]])
            #// Re-index.
            menu_hook_ = get_plugin_page_hook(submenu_[item_[2]][0][2], item_[2])
            if php_file_exists(WP_PLUGIN_DIR + str("/") + str(submenu_[item_[2]][0][2])) or (not php_empty(lambda : menu_hook_)):
                current_theme_actions_[-1] = str("<a class='button") + str(class_) + str("' href='admin.php?page=") + str(submenu_[item_[2]][0][2]) + str("'>") + str(item_[0]) + str("</a>")
            else:
                current_theme_actions_[-1] = str("<a class='button") + str(class_) + str("' href='") + str(submenu_[item_[2]][0][2]) + str("'>") + str(item_[0]) + str("</a>")
            # end if
        elif (not php_empty(lambda : item_[2])) and current_user_can(item_[1]):
            menu_file_ = item_[2]
            if current_user_can("customize"):
                if "custom-header" == menu_file_:
                    current_theme_actions_[-1] = str("<a class='button hide-if-no-customize") + str(class_) + str("' href='customize.php?autofocus[control]=header_image'>") + str(item_[0]) + str("</a>")
                elif "custom-background" == menu_file_:
                    current_theme_actions_[-1] = str("<a class='button hide-if-no-customize") + str(class_) + str("' href='customize.php?autofocus[control]=background_image'>") + str(item_[0]) + str("</a>")
                # end if
            # end if
            pos_ = php_strpos(menu_file_, "?")
            if False != pos_:
                menu_file_ = php_substr(menu_file_, 0, pos_)
            # end if
            if php_file_exists(ABSPATH + str("wp-admin/") + str(menu_file_)):
                current_theme_actions_[-1] = str("<a class='button") + str(class_) + str("' href='") + str(item_[2]) + str("'>") + str(item_[0]) + str("</a>")
            else:
                current_theme_actions_[-1] = str("<a class='button") + str(class_) + str("' href='themes.php?page=") + str(item_[2]) + str("'>") + str(item_[0]) + str("</a>")
            # end if
        # end if
    # end for
# end if
php_print("\n")
class_name_ = "theme-browser"
if (not php_empty(lambda : PHP_REQUEST["search"])):
    class_name_ += " search-loading"
# end if
php_print("<div class=\"")
php_print(esc_attr(class_name_))
php_print("""\">
<div class=\"themes wp-clearfix\">
""")
#// 
#// This PHP is synchronized with the tmpl-theme template below!
#//
for theme_ in themes_:
    aria_action_ = esc_attr(theme_["id"] + "-action")
    aria_name_ = esc_attr(theme_["id"] + "-name")
    active_class_ = ""
    if theme_["active"]:
        active_class_ = " active"
    # end if
    php_print("<div class=\"theme")
    php_print(active_class_)
    php_print("\" tabindex=\"0\" aria-describedby=\"")
    php_print(aria_action_ + " " + aria_name_)
    php_print("\">\n    ")
    if (not php_empty(lambda : theme_["screenshot"][0])):
        php_print("     <div class=\"theme-screenshot\">\n          <img src=\"")
        php_print(theme_["screenshot"][0])
        php_print("\" alt=\"\" />\n     </div>\n    ")
    else:
        php_print("     <div class=\"theme-screenshot blank\"></div>\n  ")
    # end if
    php_print("\n   ")
    if theme_["hasUpdate"]:
        php_print("     <div class=\"update-message notice inline notice-warning notice-alt\">\n        ")
        if theme_["hasPackage"]:
            php_print("         <p>")
            _e("New version available. <button class=\"button-link\" type=\"button\">Update now</button>")
            php_print("</p>\n       ")
        else:
            php_print("         <p>")
            _e("New version available.")
            php_print("</p>\n       ")
        # end if
        php_print("     </div>\n    ")
    # end if
    php_print("\n   <span class=\"more-details\" id=\"")
    php_print(aria_action_)
    php_print("\">")
    _e("Theme Details")
    php_print("</span>\n    <div class=\"theme-author\">\n      ")
    #// translators: %s: Theme author name.
    php_printf(__("By %s"), theme_["author"])
    php_print("""   </div>
    <div class=\"theme-id-container\">
    """)
    if theme_["active"]:
        php_print("         <h2 class=\"theme-name\" id=\"")
        php_print(aria_name_)
        php_print("\">\n                <span>")
        _ex("Active:", "theme")
        php_print("</span> ")
        php_print(theme_["name"])
        php_print("         </h2>\n     ")
    else:
        php_print("         <h2 class=\"theme-name\" id=\"")
        php_print(aria_name_)
        php_print("\">")
        php_print(theme_["name"])
        php_print("</h2>\n      ")
    # end if
    php_print("\n       <div class=\"theme-actions\">\n     ")
    if theme_["active"]:
        php_print("         ")
        if theme_["actions"]["customize"] and current_user_can("edit_theme_options") and current_user_can("customize"):
            php_print("             <a class=\"button button-primary customize load-customize hide-if-no-customize\" href=\"")
            php_print(theme_["actions"]["customize"])
            php_print("\">")
            _e("Customize")
            php_print("</a>\n           ")
        # end if
        php_print("     ")
    else:
        php_print("         ")
        #// translators: %s: Theme name.
        aria_label_ = php_sprintf(_x("Activate %s", "theme"), "{{ data.name }}")
        php_print("         <a class=\"button activate\" href=\"")
        php_print(theme_["actions"]["activate"])
        php_print("\" aria-label=\"")
        php_print(esc_attr(aria_label_))
        php_print("\">")
        _e("Activate")
        php_print("</a>\n           ")
        if current_user_can("edit_theme_options") and current_user_can("customize"):
            php_print("             <a class=\"button button-primary load-customize hide-if-no-customize\" href=\"")
            php_print(theme_["actions"]["customize"])
            php_print("\">")
            _e("Live Preview")
            php_print("</a>\n           ")
        # end if
        php_print("     ")
    # end if
    php_print("""
    </div>
    </div>
    </div>
    """)
# end for
php_print(" </div>\n</div>\n<div class=\"theme-overlay\" tabindex=\"0\" role=\"dialog\" aria-label=\"")
esc_attr_e("Theme Details")
php_print("\"></div>\n\n<p class=\"no-themes\">")
_e("No themes found. Try a different search.")
php_print("</p>\n\n")
#// List broken themes, if any.
broken_themes_ = wp_get_themes(Array({"errors": True}))
if (not is_multisite()) and current_user_can("edit_themes") and broken_themes_:
    php_print("\n<div class=\"broken-themes\">\n<h3>")
    _e("Broken Themes")
    php_print("</h3>\n<p>")
    _e("The following themes are installed but incomplete.")
    php_print("</p>\n\n ")
    can_resume_ = current_user_can("resume_themes")
    can_delete_ = current_user_can("delete_themes")
    can_install_ = current_user_can("install_themes")
    php_print("<table>\n    <tr>\n      <th>")
    _ex("Name", "theme name")
    php_print("</th>\n      <th>")
    _e("Description")
    php_print("</th>\n      ")
    if can_resume_:
        php_print("         <td></td>\n     ")
    # end if
    php_print("     ")
    if can_delete_:
        php_print("         <td></td>\n     ")
    # end if
    php_print("     ")
    if can_install_:
        php_print("         <td></td>\n     ")
    # end if
    php_print(" </tr>\n ")
    for broken_theme_ in broken_themes_:
        php_print("     <tr>\n          <td>")
        php_print(broken_theme_.display("Name") if broken_theme_.get("Name") else broken_theme_.get_stylesheet())
        php_print("</td>\n          <td>")
        php_print(broken_theme_.errors().get_error_message())
        php_print("</td>\n          ")
        if can_resume_:
            if "theme_paused" == broken_theme_.errors().get_error_code():
                stylesheet_ = broken_theme_.get_stylesheet()
                resume_url_ = add_query_arg(Array({"action": "resume", "stylesheet": urlencode(stylesheet_)}), admin_url("themes.php"))
                resume_url_ = wp_nonce_url(resume_url_, "resume-theme_" + stylesheet_)
                php_print("                 <td><a href=\"")
                php_print(esc_url(resume_url_))
                php_print("\" class=\"button resume-theme\">")
                _e("Resume")
                php_print("</a></td>\n                  ")
            else:
                php_print("                 <td></td>\n                 ")
            # end if
        # end if
        if can_delete_:
            stylesheet_ = broken_theme_.get_stylesheet()
            delete_url_ = add_query_arg(Array({"action": "delete", "stylesheet": urlencode(stylesheet_)}), admin_url("themes.php"))
            delete_url_ = wp_nonce_url(delete_url_, "delete-theme_" + stylesheet_)
            php_print("             <td><a href=\"")
            php_print(esc_url(delete_url_))
            php_print("\" class=\"button delete-theme\">")
            _e("Delete")
            php_print("</a></td>\n              ")
        # end if
        if can_install_ and "theme_no_parent" == broken_theme_.errors().get_error_code():
            parent_theme_name_ = broken_theme_.get("Template")
            parent_theme_ = themes_api("theme_information", Array({"slug": urlencode(parent_theme_name_)}))
            if (not is_wp_error(parent_theme_)):
                install_url_ = add_query_arg(Array({"action": "install-theme", "theme": urlencode(parent_theme_name_)}), admin_url("update.php"))
                install_url_ = wp_nonce_url(install_url_, "install-theme_" + parent_theme_name_)
                php_print("                 <td><a href=\"")
                php_print(esc_url(install_url_))
                php_print("\" class=\"button install-theme\">")
                _e("Install Parent Theme")
                php_print("</a></td>\n                  ")
            # end if
        # end if
        php_print("     </tr>\n ")
    # end for
    php_print("""</table>
    </div>
    """)
# end if
php_print("</div><!-- .wrap -->\n\n")
pass
php_print("""<script id=\"tmpl-theme\" type=\"text/template\">
<# if ( data.screenshot[0] ) { #>
<div class=\"theme-screenshot\">
<img src=\"{{ data.screenshot[0] }}\" alt=\"\" />
</div>
<# } else { #>
<div class=\"theme-screenshot blank\"></div>
<# } #>
<# if ( data.hasUpdate ) { #>
<# if ( data.hasPackage ) { #>
<div class=\"update-message notice inline notice-warning notice-alt\"><p>""")
_e("New version available. <button class=\"button-link\" type=\"button\">Update now</button>")
php_print("</p></div>\n     <# } else { #>\n            <div class=\"update-message notice inline notice-warning notice-alt\"><p>")
_e("New version available.")
php_print("""</p></div>
<# } #>
<# } #>
<span class=\"more-details\" id=\"{{ data.id }}-action\">""")
_e("Theme Details")
php_print("</span>\n    <div class=\"theme-author\">\n      ")
#// translators: %s: Theme author name.
php_printf(__("By %s"), "{{{ data.author }}}")
php_print("""   </div>
<div class=\"theme-id-container\">
<# if ( data.active ) { #>
<h2 class=\"theme-name\" id=\"{{ data.id }}-name\">
<span>""")
_ex("Active:", "theme")
php_print("""</span> {{{ data.name }}}
</h2>
<# } else { #>
<h2 class=\"theme-name\" id=\"{{ data.id }}-name\">{{{ data.name }}}</h2>
<# } #>
<div class=\"theme-actions\">
<# if ( data.active ) { #>
<# if ( data.actions.customize ) { #>
<a class=\"button button-primary customize load-customize hide-if-no-customize\" href=\"{{{ data.actions.customize }}}\">""")
_e("Customize")
php_print("""</a>
<# } #>
<# } else { #>
""")
#// translators: %s: Theme name.
aria_label_ = php_sprintf(_x("Activate %s", "theme"), "{{ data.name }}")
php_print("             <a class=\"button activate\" href=\"{{{ data.actions.activate }}}\" aria-label=\"")
php_print(aria_label_)
php_print("\">")
_e("Activate")
php_print("</a>\n               <a class=\"button button-primary load-customize hide-if-no-customize\" href=\"{{{ data.actions.customize }}}\">")
_e("Live Preview")
php_print("""</a>
<# } #>
</div>
</div>
</script>
<script id=\"tmpl-theme-single\" type=\"text/template\">
<div class=\"theme-backdrop\"></div>
<div class=\"theme-wrap wp-clearfix\" role=\"document\">
<div class=\"theme-header\">
<button class=\"left dashicons dashicons-no\"><span class=\"screen-reader-text\">""")
_e("Show previous theme")
php_print("</span></button>\n           <button class=\"right dashicons dashicons-no\"><span class=\"screen-reader-text\">")
_e("Show next theme")
php_print("</span></button>\n           <button class=\"close dashicons dashicons-no\"><span class=\"screen-reader-text\">")
_e("Close details dialog")
php_print("""</span></button>
</div>
<div class=\"theme-about wp-clearfix\">
<div class=\"theme-screenshots\">
<# if ( data.screenshot[0] ) { #>
<div class=\"screenshot\"><img src=\"{{ data.screenshot[0] }}\" alt=\"\" /></div>
<# } else { #>
<div class=\"screenshot blank\"></div>
<# } #>
</div>
<div class=\"theme-info\">
<# if ( data.active ) { #>
<span class=\"current-label\">""")
_e("Current Theme")
php_print("""</span>
<# } #>
<h2 class=\"theme-name\">{{{ data.name }}}<span class=\"theme-version\">
""")
#// translators: %s: Theme version.
php_printf(__("Version: %s"), "{{ data.version }}")
php_print("             </span></h2>\n              <p class=\"theme-author\">\n                    ")
#// translators: %s: Theme author link.
php_printf(__("By %s"), "{{{ data.authorAndUri }}}")
php_print("""               </p>
<# if ( data.hasUpdate ) { #>
<div class=\"notice notice-warning notice-alt notice-large\">
<h3 class=\"notice-title\">""")
_e("Update Available")
php_print("""</h3>
{{{ data.update }}}
</div>
<# } #>
<p class=\"theme-description\">{{{ data.description }}}</p>
<# if ( data.parent ) { #>
<p class=\"parent-theme\">
""")
#// translators: %s: Theme name.
php_printf(__("This is a child theme of %s."), "<strong>{{{ data.parent }}}</strong>")
php_print("""                   </p>
<# } #>
<# if ( data.tags ) { #>
<p class=\"theme-tags\"><span>""")
_e("Tags:")
php_print("""</span> {{{ data.tags }}}</p>
<# } #>
</div>
</div>
<div class=\"theme-actions\">
<div class=\"active-theme\">
<a href=\"{{{ data.actions.customize }}}\" class=\"button button-primary customize load-customize hide-if-no-customize\">""")
_e("Customize")
php_print("</a>\n               ")
php_print(php_implode(" ", current_theme_actions_))
php_print("         </div>\n            <div class=\"inactive-theme\">\n                ")
#// translators: %s: Theme name.
aria_label_ = php_sprintf(_x("Activate %s", "theme"), "{{ data.name }}")
php_print("             <# if ( data.actions.activate ) { #>\n                  <a href=\"{{{ data.actions.activate }}}\" class=\"button activate\" aria-label=\"")
php_print(aria_label_)
php_print("\">")
_e("Activate")
php_print("</a>\n               <# } #>\n               <a href=\"{{{ data.actions.customize }}}\" class=\"button button-primary load-customize hide-if-no-customize\">")
_e("Live Preview")
php_print("""</a>
</div>
<# if ( ! data.active && data.actions['delete'] ) { #>
<a href=\"{{{ data.actions['delete'] }}}\" class=\"button delete-theme\">""")
_e("Delete")
php_print("""</a>
<# } #>
</div>
</div>
</script>
""")
wp_print_request_filesystem_credentials_modal()
wp_print_admin_notice_templates()
wp_print_update_row_templates()
wp_localize_script("updates", "_wpUpdatesItemCounts", Array({"totals": wp_get_update_data()}))
php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
