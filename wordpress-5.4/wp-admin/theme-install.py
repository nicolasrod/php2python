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
#// Install theme administration panel.
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// WordPress Administration Bootstrap
php_include_file(__DIR__ + "/admin.php", once=True)
php_include_file(ABSPATH + "wp-admin/includes/theme-install.php", once=False)
wp_reset_vars(Array("tab"))
if (not current_user_can("install_themes")):
    wp_die(__("Sorry, you are not allowed to install themes on this site."))
# end if
if is_multisite() and (not is_network_admin()):
    wp_redirect(network_admin_url("theme-install.php"))
    php_exit(0)
# end if
title_ = __("Add Themes")
parent_file_ = "themes.php"
if (not is_network_admin()):
    submenu_file_ = "themes.php"
# end if
installed_themes_ = search_theme_directories()
if False == installed_themes_:
    installed_themes_ = Array()
# end if
for k_,v_ in installed_themes_:
    if False != php_strpos(k_, "/"):
        installed_themes_[k_] = None
    # end if
# end for
wp_localize_script("theme", "_wpThemeSettings", Array({"themes": False, "settings": Array({"isInstall": True, "canInstall": current_user_can("install_themes"), "installURI": self_admin_url("theme-install.php") if current_user_can("install_themes") else None, "adminUrl": php_parse_url(self_admin_url(), PHP_URL_PATH)})}, {"l10n": Array({"addNew": __("Add New Theme"), "search": __("Search Themes"), "searchPlaceholder": __("Search themes..."), "upload": __("Upload Theme"), "back": __("Back"), "error": php_sprintf(__("An unexpected error occurred. Something may be wrong with WordPress.org or this server&#8217;s configuration. If you continue to have problems, please try the <a href=\"%s\">support forums</a>."), __("https://wordpress.org/support/forums/")), "tryAgain": __("Try Again"), "themesFound": __("Number of Themes found: %d"), "noThemesFound": __("No themes found. Try a different search."), "collapseSidebar": __("Collapse Sidebar"), "expandSidebar": __("Expand Sidebar"), "selectFeatureFilter": __("Select one or more Theme features to filter by")})}, {"installedThemes": php_array_keys(installed_themes_)}))
wp_enqueue_script("theme")
wp_enqueue_script("updates")
if tab_:
    #// 
    #// Fires before each of the tabs are rendered on the Install Themes page.
    #// 
    #// The dynamic portion of the hook name, `$tab`, refers to the current
    #// theme installation tab. Possible values are 'dashboard', 'search', 'upload',
    #// 'featured', 'new', or 'updated'.
    #// 
    #// @since 2.8.0
    #//
    do_action(str("install_themes_pre_") + str(tab_))
# end if
help_overview_ = "<p>" + php_sprintf(__("You can find additional themes for your site by using the Theme Browser/Installer on this screen, which will display themes from the <a href=\"%s\">WordPress Theme Directory</a>. These themes are designed and developed by third parties, are available free of charge, and are compatible with the license WordPress uses."), __("https://wordpress.org/themes/")) + "</p>" + "<p>" + __("You can Search for themes by keyword, author, or tag, or can get more specific and search by criteria listed in the feature filter.") + " <span id=\"live-search-desc\">" + __("The search results will be updated as you type.") + "</span></p>" + "<p>" + __("Alternately, you can browse the themes that are Featured, Popular, or Latest. When you find a theme you like, you can preview it or install it.") + "</p>" + "<p>" + php_sprintf(__("You can Upload a theme manually if you have already downloaded its ZIP archive onto your computer (make sure it is from a trusted and original source). You can also do it the old-fashioned way and copy a downloaded theme&#8217;s folder via FTP into your %s directory."), "<code>/wp-content/themes</code>") + "</p>"
get_current_screen().add_help_tab(Array({"id": "overview", "title": __("Overview"), "content": help_overview_}))
help_installing_ = "<p>" + __("Once you have generated a list of themes, you can preview and install any of them. Click on the thumbnail of the theme you&#8217;re interested in previewing. It will open up in a full-screen Preview page to give you a better idea of how that theme will look.") + "</p>" + "<p>" + __("To install the theme so you can preview it with your site&#8217;s content and customize its theme options, click the \"Install\" button at the top of the left-hand pane. The theme files will be downloaded to your website automatically. When this is complete, the theme is now available for activation, which you can do by clicking the \"Activate\" link, or by navigating to your Manage Themes screen and clicking the \"Live Preview\" link under any installed theme&#8217;s thumbnail image.") + "</p>"
get_current_screen().add_help_tab(Array({"id": "installing", "title": __("Previewing and Installing"), "content": help_installing_}))
get_current_screen().set_help_sidebar("<p><strong>" + __("For more information:") + "</strong></p>" + "<p>" + __("<a href=\"https://wordpress.org/support/article/using-themes/#adding-new-themes\">Documentation on Adding New Themes</a>") + "</p>" + "<p>" + __("<a href=\"https://wordpress.org/support/\">Support</a>") + "</p>")
php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
php_print("<div class=\"wrap\">\n   <h1 class=\"wp-heading-inline\">")
php_print(esc_html(title_))
php_print("</h1>\n\n    ")
#// 
#// Filters the tabs shown on the Add Themes screen.
#// 
#// This filter is for backward compatibility only, for the suppression of the upload tab.
#// 
#// @since 2.8.0
#// 
#// @param string[] $tabs Associative array of the tabs shown on the Add Themes screen. Default is 'upload'.
#//
tabs_ = apply_filters("install_themes_tabs", Array({"upload": __("Upload Theme")}))
if (not php_empty(lambda : tabs_["upload"])) and current_user_can("upload_themes"):
    php_print(" <button type=\"button\" class=\"upload-view-toggle page-title-action hide-if-no-js\" aria-expanded=\"false\">" + __("Upload Theme") + "</button>")
# end if
php_print("""
<hr class=\"wp-header-end\">
<div class=\"error hide-if-js\">
<p>""")
_e("The Theme Installer screen requires JavaScript.")
php_print("""</p>
</div>
<div class=\"upload-theme\">
""")
install_themes_upload()
php_print(" </div>\n\n  <h2 class=\"screen-reader-text hide-if-no-js\">")
_e("Filter themes list")
php_print("""</h2>
<div class=\"wp-filter hide-if-no-js\">
<div class=\"filter-count\">
<span class=\"count theme-count\"></span>
</div>
<ul class=\"filter-links\">
<li><a href=\"#\" data-sort=\"featured\">""")
_ex("Featured", "themes")
php_print("</a></li>\n          <li><a href=\"#\" data-sort=\"popular\">")
_ex("Popular", "themes")
php_print("</a></li>\n          <li><a href=\"#\" data-sort=\"new\">")
_ex("Latest", "themes")
php_print("</a></li>\n          <li><a href=\"#\" data-sort=\"favorites\">")
_ex("Favorites", "themes")
php_print("""</a></li>
</ul>
<button type=\"button\" class=\"button drawer-toggle\" aria-expanded=\"false\">""")
_e("Feature Filter")
php_print("""</button>
<form class=\"search-form\"></form>
<div class=\"favorites-form\">
""")
action_ = "save_wporg_username_" + get_current_user_id()
if (php_isset(lambda : PHP_REQUEST["_wpnonce"])) and wp_verify_nonce(wp_unslash(PHP_REQUEST["_wpnonce"]), action_):
    user_ = wp_unslash(PHP_REQUEST["user"]) if (php_isset(lambda : PHP_REQUEST["user"])) else get_user_option("wporg_favorites")
    update_user_meta(get_current_user_id(), "wporg_favorites", user_)
else:
    user_ = get_user_option("wporg_favorites")
# end if
php_print("         <p class=\"install-help\">")
_e("If you have marked themes as favorites on WordPress.org, you can browse them here.")
php_print("""</p>
<p>
<label for=\"wporg-username-input\">""")
_e("Your WordPress.org username:")
php_print("</label>\n               <input type=\"hidden\" id=\"wporg-username-nonce\" name=\"_wpnonce\" value=\"")
php_print(esc_attr(wp_create_nonce(action_)))
php_print("\" />\n              <input type=\"search\" id=\"wporg-username-input\" value=\"")
php_print(esc_attr(user_))
php_print("\" />\n              <input type=\"button\" class=\"button favorites-form-submit\" value=\"")
esc_attr_e("Get Favorites")
php_print("""\" />
</p>
</div>
<div class=\"filter-drawer\">
<div class=\"buttons\">
<button type=\"button\" class=\"apply-filters button\">""")
_e("Apply Filters")
php_print("<span></span></button>\n             <button type=\"button\" class=\"clear-filters button\" aria-label=\"")
esc_attr_e("Clear current filters")
php_print("\">")
_e("Clear")
php_print("</button>\n          </div>\n        ")
feature_list_ = get_theme_feature_list(False)
#// Use the core list, rather than the .org API, due to inconsistencies and to ensure tags are translated.
for feature_name_,features_ in feature_list_:
    php_print("<fieldset class=\"filter-group\">")
    feature_name_ = esc_html(feature_name_)
    php_print("<legend>" + feature_name_ + "</legend>")
    php_print("<div class=\"filter-group-feature\">")
    for feature_,feature_name_ in features_:
        feature_ = esc_attr(feature_)
        php_print("<input type=\"checkbox\" id=\"filter-id-" + feature_ + "\" value=\"" + feature_ + "\" /> ")
        php_print("<label for=\"filter-id-" + feature_ + "\">" + feature_name_ + "</label>")
    # end for
    php_print("</div>")
    php_print("</fieldset>")
# end for
php_print("         <div class=\"buttons\">\n               <button type=\"button\" class=\"apply-filters button\">")
_e("Apply Filters")
php_print("<span></span></button>\n             <button type=\"button\" class=\"clear-filters button\" aria-label=\"")
esc_attr_e("Clear current filters")
php_print("\">")
_e("Clear")
php_print("""</button>
</div>
<div class=\"filtered-by\">
<span>""")
_e("Filtering by:")
php_print("</span>\n                <div class=\"tags\"></div>\n                <button type=\"button\" class=\"button-link edit-filters\">")
_e("Edit Filters")
php_print("""</button>
</div>
</div>
</div>
<h2 class=\"screen-reader-text hide-if-no-js\">""")
_e("Themes list")
php_print("""</h2>
<div class=\"theme-browser content-filterable\"></div>
<div class=\"theme-install-overlay wp-full-overlay expanded\"></div>
<p class=\"no-themes\">""")
_e("No themes found. Try a different search.")
php_print("""</p>
<span class=\"spinner\"></span>
""")
if tab_:
    #// 
    #// Fires at the top of each of the tabs on the Install Themes page.
    #// 
    #// The dynamic portion of the hook name, `$tab`, refers to the current
    #// theme installation tab. Possible values are 'dashboard', 'search', 'upload',
    #// 'featured', 'new', or 'updated'.
    #// 
    #// @since 2.8.0
    #// 
    #// @param int $paged Number of the current page of results being viewed.
    #//
    do_action(str("install_themes_") + str(tab_), paged_)
# end if
php_print("""</div>
<script id=\"tmpl-theme\" type=\"text/template\">
<# if ( data.screenshot_url ) { #>
<div class=\"theme-screenshot\">
<img src=\"{{ data.screenshot_url }}\" alt=\"\" />
</div>
<# } else { #>
<div class=\"theme-screenshot blank\"></div>
<# } #>
<span class=\"more-details\">""")
_ex("Details &amp; Preview", "theme")
php_print("</span>\n    <div class=\"theme-author\">\n      ")
#// translators: %s: Theme author name.
printf(__("By %s"), "{{ data.author }}")
php_print("""   </div>
<div class=\"theme-id-container\">
<h3 class=\"theme-name\">{{ data.name }}</h3>
<div class=\"theme-actions\">
<# if ( data.installed ) { #>
""")
#// translators: %s: Theme name.
aria_label_ = php_sprintf(_x("Activate %s", "theme"), "{{ data.name }}")
php_print("             <# if ( data.activate_url ) { #>\n                  <a class=\"button button-primary activate\" href=\"{{ data.activate_url }}\" aria-label=\"")
php_print(esc_attr(aria_label_))
php_print("\">")
_e("Activate")
php_print("""</a>
<# } #>
<# if ( data.customize_url ) { #>
<a class=\"button load-customize\" href=\"{{ data.customize_url }}\">""")
_e("Live Preview")
php_print("</a>\n               <# } else { #>\n                    <button class=\"button preview install-theme-preview\">")
_e("Preview")
php_print("""</button>
<# } #>
<# } else { #>
""")
#// translators: %s: Theme name.
aria_label_ = php_sprintf(__("Install %s"), "{{ data.name }}")
php_print("             <a class=\"button button-primary theme-install\" data-name=\"{{ data.name }}\" data-slug=\"{{ data.id }}\" href=\"{{ data.install_url }}\" aria-label=\"")
php_print(esc_attr(aria_label_))
php_print("\">")
_e("Install")
php_print("</a>\n               <button class=\"button preview install-theme-preview\">")
_e("Preview")
php_print("""</button>
<# } #>
</div>
</div>
<# if ( data.installed ) { #>
<div class=\"notice notice-success notice-alt\"><p>""")
_ex("Installed", "theme")
php_print("""</p></div>
<# } #>
</script>
<script id=\"tmpl-theme-preview\" type=\"text/template\">
<div class=\"wp-full-overlay-sidebar\">
<div class=\"wp-full-overlay-header\">
<button class=\"close-full-overlay\"><span class=\"screen-reader-text\">""")
_e("Close")
php_print("</span></button>\n           <button class=\"previous-theme\"><span class=\"screen-reader-text\">")
_e("Previous theme")
php_print("</span></button>\n           <button class=\"next-theme\"><span class=\"screen-reader-text\">")
_e("Next theme")
php_print("</span></button>\n           <# if ( data.installed ) { #>\n             <a class=\"button button-primary activate\" href=\"{{ data.activate_url }}\">")
_e("Activate")
php_print("</a>\n           <# } else { #>\n                <a href=\"{{ data.install_url }}\" class=\"button button-primary theme-install\" data-name=\"{{ data.name }}\" data-slug=\"{{ data.id }}\">")
_e("Install")
php_print("""</a>
<# } #>
</div>
<div class=\"wp-full-overlay-sidebar-content\">
<div class=\"install-theme-info\">
<h3 class=\"theme-name\">{{ data.name }}</h3>
<span class=\"theme-by\">
""")
#// translators: %s: Theme author name.
printf(__("By %s"), "{{ data.author }}")
php_print("""                   </span>
<img class=\"theme-screenshot\" src=\"{{ data.screenshot_url }}\" alt=\"\" />
<div class=\"theme-details\">
<# if ( data.rating ) { #>
<div class=\"theme-rating\">
{{{ data.stars }}}
<a class=\"num-ratings\" href=\"{{ data.reviews_url }}\">
""")
#// translators: %s: Number of ratings.
php_print(php_sprintf(__("(%s ratings)"), "{{ data.num_ratings }}"))
php_print("""                               </a>
</div>
<# } else { #>
<span class=\"no-rating\">""")
_e("This theme has not been rated yet.")
php_print("""</span>
<# } #>
<div class=\"theme-version\">
""")
#// translators: %s: Theme version.
printf(__("Version: %s"), "{{ data.version }}")
php_print("""                       </div>
<div class=\"theme-description\">{{{ data.description }}}</div>
</div>
</div>
</div>
<div class=\"wp-full-overlay-footer\">
<button type=\"button\" class=\"collapse-sidebar button\" aria-expanded=\"true\" aria-label=\"""")
esc_attr_e("Collapse Sidebar")
php_print("\">\n                    <span class=\"collapse-sidebar-arrow\"></span>\n                    <span class=\"collapse-sidebar-label\">")
_e("Collapse")
php_print("""</span>
</button>
</div>
</div>
<div class=\"wp-full-overlay-main\">
<iframe src=\"{{ data.preview_url }}\" title=\"""")
esc_attr_e("Preview")
php_print("""\"></iframe>
</div>
</script>
""")
wp_print_request_filesystem_credentials_modal()
wp_print_admin_notice_templates()
php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
