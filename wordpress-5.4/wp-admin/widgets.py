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
#// Widget administration panel
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// WordPress Administration Bootstrap
php_include_file(__DIR__ + "/admin.php", once=True)
#// WordPress Administration Widgets API
php_include_file(ABSPATH + "wp-admin/includes/widgets.php", once=True)
if (not current_user_can("edit_theme_options")):
    wp_die("<h1>" + __("You need a higher level of permission.") + "</h1>" + "<p>" + __("Sorry, you are not allowed to edit theme options on this site.") + "</p>", 403)
# end if
widgets_access_ = get_user_setting("widgets_access")
if (php_isset(lambda : PHP_REQUEST["widgets-access"])):
    check_admin_referer("widgets-access")
    widgets_access_ = "on" if "on" == PHP_REQUEST["widgets-access"] else "off"
    set_user_setting("widgets_access", widgets_access_)
# end if
if "on" == widgets_access_:
    add_filter("admin_body_class", "wp_widgets_access_body_class")
else:
    wp_enqueue_script("admin-widgets")
    if wp_is_mobile():
        wp_enqueue_script("jquery-touch-punch")
    # end if
# end if
#// 
#// Fires early before the Widgets administration screen loads,
#// after scripts are enqueued.
#// 
#// @since 2.2.0
#//
do_action("sidebar_admin_setup")
title_ = __("Widgets")
parent_file_ = "themes.php"
get_current_screen().add_help_tab(Array({"id": "overview", "title": __("Overview"), "content": "<p>" + __("Widgets are independent sections of content that can be placed into any widgetized area provided by your theme (commonly called sidebars). To populate your sidebars/widget areas with individual widgets, drag and drop the title bars into the desired area. By default, only the first widget area is expanded. To populate additional widget areas, click on their title bars to expand them.") + "</p>\n    <p>" + __("The Available Widgets section contains all the widgets you can choose from. Once you drag a widget into a sidebar, it will open to allow you to configure its settings. When you are happy with the widget settings, click the Save button and the widget will go live on your site. If you click Delete, it will remove the widget.") + "</p>"}))
get_current_screen().add_help_tab(Array({"id": "removing-reusing", "title": __("Removing and Reusing"), "content": "<p>" + __("If you want to remove the widget but save its setting for possible future use, just drag it into the Inactive Widgets area. You can add them back anytime from there. This is especially helpful when you switch to a theme with fewer or different widget areas.") + "</p>\n    <p>" + __("Widgets may be used multiple times. You can give each widget a title, to display on your site, but it&#8217;s not required.") + "</p>\n  <p>" + __("Enabling Accessibility Mode, via Screen Options, allows you to use Add and Edit buttons instead of using drag and drop.") + "</p>"}))
get_current_screen().add_help_tab(Array({"id": "missing-widgets", "title": __("Missing Widgets"), "content": "<p>" + __("Many themes show some sidebar widgets by default until you edit your sidebars, but they are not automatically displayed in your sidebar management tool. After you make your first widget change, you can re-add the default widgets by adding them from the Available Widgets area.") + "</p>" + "<p>" + __("When changing themes, there is often some variation in the number and setup of widget areas/sidebars and sometimes these conflicts make the transition a bit less smooth. If you changed themes and seem to be missing widgets, scroll down on this screen to the Inactive Widgets area, where all of your widgets and their settings will have been saved.") + "</p>"}))
get_current_screen().set_help_sidebar("<p><strong>" + __("For more information:") + "</strong></p>" + "<p>" + __("<a href=\"https://wordpress.org/support/article/appearance-widgets-screen/\">Documentation on Widgets</a>") + "</p>" + "<p>" + __("<a href=\"https://wordpress.org/support/\">Support</a>") + "</p>")
if (not current_theme_supports("widgets")):
    wp_die(__("The theme you are currently using isn&#8217;t widget-aware, meaning that it has no sidebars that you are able to change. For information on making your theme widget-aware, please <a href=\"https://developer.wordpress.org/themes/functionality/widgets/\">follow these instructions</a>."))
# end if
#// These are the widgets grouped by sidebar.
sidebars_widgets_ = wp_get_sidebars_widgets()
if php_empty(lambda : sidebars_widgets_):
    sidebars_widgets_ = wp_get_widget_defaults()
# end if
for sidebar_id_,widgets_ in sidebars_widgets_.items():
    if "wp_inactive_widgets" == sidebar_id_:
        continue
    # end if
    if (not is_registered_sidebar(sidebar_id_)):
        if (not php_empty(lambda : widgets_)):
            #// Register the inactive_widgets area as sidebar.
            register_sidebar(Array({"name": __("Inactive Sidebar (not used)"), "id": sidebar_id_, "class": "inactive-sidebar orphan-sidebar", "description": __("This sidebar is no longer available and does not show anywhere on your site. Remove each of the widgets below to fully remove this inactive sidebar."), "before_widget": "", "after_widget": "", "before_title": "", "after_title": ""}))
        else:
            sidebars_widgets_[sidebar_id_] = None
        # end if
    # end if
# end for
#// Register the inactive_widgets area as sidebar.
register_sidebar(Array({"name": __("Inactive Widgets"), "id": "wp_inactive_widgets", "class": "inactive-sidebar", "description": __("Drag widgets here to remove them from the sidebar but keep their settings."), "before_widget": "", "after_widget": "", "before_title": "", "after_title": ""}))
retrieve_widgets()
#// We're saving a widget without JS.
if (php_isset(lambda : PHP_POST["savewidget"])) or (php_isset(lambda : PHP_POST["removewidget"])):
    widget_id_ = PHP_POST["widget-id"]
    check_admin_referer(str("save-delete-widget-") + str(widget_id_))
    number_ = php_int(PHP_POST["multi_number"]) if (php_isset(lambda : PHP_POST["multi_number"])) else ""
    if number_:
        for key_,val_ in PHP_POST.items():
            if php_is_array(val_) and php_preg_match("/__i__|%i%/", key(val_)):
                PHP_POST[key_] = Array({number_: php_array_shift(val_)})
                break
            # end if
        # end for
    # end if
    sidebar_id_ = PHP_POST["sidebar"]
    position_ = php_int(PHP_POST[sidebar_id_ + "_position"]) - 1 if (php_isset(lambda : PHP_POST[sidebar_id_ + "_position"])) else 0
    id_base_ = PHP_POST["id_base"]
    sidebar_ = sidebars_widgets_[sidebar_id_] if (php_isset(lambda : sidebars_widgets_[sidebar_id_])) else Array()
    #// Delete.
    if (php_isset(lambda : PHP_POST["removewidget"])) and PHP_POST["removewidget"]:
        if (not php_in_array(widget_id_, sidebar_, True)):
            wp_redirect(admin_url("widgets.php?error=0"))
            php_exit(0)
        # end if
        sidebar_ = php_array_diff(sidebar_, Array(widget_id_))
        PHP_POST = Array({"sidebar": sidebar_id_, "widget-" + id_base_: Array(), "the-widget-id": widget_id_, "delete_widget": "1"})
        #// 
        #// Fires immediately after a widget has been marked for deletion.
        #// 
        #// @since 4.4.0
        #// 
        #// @param string $widget_id  ID of the widget marked for deletion.
        #// @param string $sidebar_id ID of the sidebar the widget was deleted from.
        #// @param string $id_base    ID base for the widget.
        #//
        do_action("delete_widget", widget_id_, sidebar_id_, id_base_)
    # end if
    PHP_POST["widget-id"] = sidebar_
    for name_,control_ in wp_registered_widget_updates_.items():
        if name_ != id_base_ or (not php_is_callable(control_["callback"])):
            continue
        # end if
        ob_start()
        call_user_func_array(control_["callback"], control_["params"])
        ob_end_clean()
        break
    # end for
    sidebars_widgets_[sidebar_id_] = sidebar_
    #// Remove old position.
    if (not (php_isset(lambda : PHP_POST["delete_widget"]))):
        for key_,sb_ in sidebars_widgets_.items():
            if php_is_array(sb_):
                sidebars_widgets_[key_] = php_array_diff(sb_, Array(widget_id_))
            # end if
        # end for
        array_splice(sidebars_widgets_[sidebar_id_], position_, 0, widget_id_)
    # end if
    wp_set_sidebars_widgets(sidebars_widgets_)
    wp_redirect(admin_url("widgets.php?message=0"))
    php_exit(0)
# end if
#// Remove inactive widgets without JS.
if (php_isset(lambda : PHP_POST["removeinactivewidgets"])):
    check_admin_referer("remove-inactive-widgets", "_wpnonce_remove_inactive_widgets")
    if PHP_POST["removeinactivewidgets"]:
        for key_,widget_id_ in sidebars_widgets_["wp_inactive_widgets"].items():
            pieces_ = php_explode("-", widget_id_)
            multi_number_ = php_array_pop(pieces_)
            id_base_ = php_implode("-", pieces_)
            widget_ = get_option("widget_" + id_base_)
            widget_[multi_number_] = None
            update_option("widget_" + id_base_, widget_)
            sidebars_widgets_["wp_inactive_widgets"][key_] = None
        # end for
        wp_set_sidebars_widgets(sidebars_widgets_)
    # end if
    wp_redirect(admin_url("widgets.php?message=0"))
    php_exit(0)
# end if
#// Output the widget form without JS.
if (php_isset(lambda : PHP_REQUEST["editwidget"])) and PHP_REQUEST["editwidget"]:
    widget_id_ = PHP_REQUEST["editwidget"]
    if (php_isset(lambda : PHP_REQUEST["addnew"])):
        #// Default to the first sidebar.
        keys_ = php_array_keys(wp_registered_sidebars_)
        sidebar_ = reset(keys_)
        if (php_isset(lambda : PHP_REQUEST["base"])) and (php_isset(lambda : PHP_REQUEST["num"])):
            #// Multi-widget.
            #// Copy minimal info from an existing instance of this widget to a new instance.
            for control_ in wp_registered_widget_controls_:
                if PHP_REQUEST["base"] == control_["id_base"]:
                    control_callback_ = control_["callback"]
                    multi_number_ = php_int(PHP_REQUEST["num"])
                    control_["params"][0]["number"] = -1
                    control_["id"] = control_["id_base"] + "-" + multi_number_
                    widget_id_ = control_["id"]
                    wp_registered_widget_controls_[control_["id"]] = control_
                    break
                # end if
            # end for
        # end if
    # end if
    if (php_isset(lambda : wp_registered_widget_controls_[widget_id_])) and (not (php_isset(lambda : control_))):
        control_ = wp_registered_widget_controls_[widget_id_]
        control_callback_ = control_["callback"]
    elif (not (php_isset(lambda : wp_registered_widget_controls_[widget_id_]))) and (php_isset(lambda : wp_registered_widgets_[widget_id_])):
        name_ = esc_html(strip_tags(wp_registered_widgets_[widget_id_]["name"]))
    # end if
    if (not (php_isset(lambda : name_))):
        name_ = esc_html(strip_tags(control_["name"]))
    # end if
    if (not (php_isset(lambda : sidebar_))):
        sidebar_ = PHP_REQUEST["sidebar"] if (php_isset(lambda : PHP_REQUEST["sidebar"])) else "wp_inactive_widgets"
    # end if
    if (not (php_isset(lambda : multi_number_))):
        multi_number_ = control_["params"][0]["number"] if (php_isset(lambda : control_["params"][0]["number"])) else ""
    # end if
    id_base_ = control_["id_base"] if (php_isset(lambda : control_["id_base"])) else control_["id"]
    #// Show the widget form.
    width_ = " style=\"width:" + php_max(control_["width"], 350) + "px\""
    key_ = php_int(PHP_REQUEST["key"]) if (php_isset(lambda : PHP_REQUEST["key"])) else 0
    php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
    php_print(" <div class=\"wrap\">\n  <h1>")
    php_print(esc_html(title_))
    php_print("</h1>\n  <div class=\"editwidget\"")
    php_print(width_)
    php_print(">\n  <h2>\n  ")
    #// translators: %s: Widget name.
    php_printf(__("Widget %s"), name_)
    php_print("""   </h2>
    <form action=\"widgets.php\" method=\"post\">
    <div class=\"widget-inside\">
    """)
    if php_is_callable(control_callback_):
        call_user_func_array(control_callback_, control_["params"])
    else:
        php_print("<p>" + __("There are no options for this widget.") + "</p>\n")
    # end if
    php_print(" </div>\n\n  <p class=\"describe\">")
    _e("Select both the sidebar for this widget and the position of the widget in that sidebar.")
    php_print("</p>\n   <div class=\"widget-position\">\n   <table class=\"widefat\"><thead><tr><th>")
    _e("Sidebar")
    php_print("</th><th>")
    _e("Position")
    php_print("</th></tr></thead><tbody>\n  ")
    for sbname_,sbvalue_ in wp_registered_sidebars_.items():
        php_print("     <tr><td><label><input type='radio' name='sidebar' value='" + esc_attr(sbname_) + "'" + checked(sbname_, sidebar_, False) + str(" /> ") + str(sbvalue_["name"]) + str("</label></td><td>"))
        if "wp_inactive_widgets" == sbname_ or "orphaned_widgets" == php_substr(sbname_, 0, 16):
            php_print("&nbsp;")
        else:
            if (not (php_isset(lambda : sidebars_widgets_[sbname_]))) or (not php_is_array(sidebars_widgets_[sbname_])):
                j_ = 1
                sidebars_widgets_[sbname_] = Array()
            else:
                j_ = php_count(sidebars_widgets_[sbname_])
                if (php_isset(lambda : PHP_REQUEST["addnew"])) or (not php_in_array(widget_id_, sidebars_widgets_[sbname_], True)):
                    j_ += 1
                # end if
            # end if
            selected_ = ""
            php_print(str("     <select name='") + str(sbname_) + str("_position'>\n"))
            php_print("     <option value=''>" + __("&mdash; Select &mdash;") + "</option>\n")
            i_ = 1
            while i_ <= j_:
                
                if php_in_array(widget_id_, sidebars_widgets_[sbname_], True):
                    selected_ = selected(i_, key_ + 1, False)
                # end if
                php_print(str("     <option value='") + str(i_) + str("'") + str(selected_) + str("> ") + str(i_) + str(" </option>\n"))
                i_ += 1
            # end while
            php_print("     </select>\n")
        # end if
        php_print("</td></tr>\n")
    # end for
    php_print("""   </tbody></table>
    </div>
    <div class=\"widget-control-actions\">
    """)
    if (php_isset(lambda : PHP_REQUEST["addnew"])):
        php_print(" <a href=\"widgets.php\" class=\"button alignleft\">")
        _e("Cancel")
        php_print("</a>\n       ")
    else:
        submit_button(__("Delete"), "alignleft", "removewidget", False)
    # end if
    submit_button(__("Save Widget"), "primary alignright", "savewidget", False)
    php_print(" <input type=\"hidden\" name=\"widget-id\" class=\"widget-id\" value=\"")
    php_print(esc_attr(widget_id_))
    php_print("\" />\n  <input type=\"hidden\" name=\"id_base\" class=\"id_base\" value=\"")
    php_print(esc_attr(id_base_))
    php_print("\" />\n  <input type=\"hidden\" name=\"multi_number\" class=\"multi_number\" value=\"")
    php_print(esc_attr(multi_number_))
    php_print("\" />\n  ")
    wp_nonce_field(str("save-delete-widget-") + str(widget_id_))
    php_print("""   <br class=\"clear\" />
    </div>
    </form>
    </div>
    </div>
    """)
    php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
    php_exit(0)
# end if
messages_ = Array(__("Changes saved."))
errors_ = Array(__("Error while saving."), __("Error in displaying the widget settings form."))
php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
php_print("""
<div class=\"wrap\">
<h1 class=\"wp-heading-inline\">
""")
php_print(esc_html(title_))
php_print("</h1>\n\n")
if current_user_can("customize"):
    php_printf(" <a class=\"page-title-action hide-if-no-customize\" href=\"%1$s\">%2$s</a>", esc_url(add_query_arg(Array(Array({"autofocus": Array({"panel": "widgets"})}), {"return": urlencode(remove_query_arg(wp_removable_query_args(), wp_unslash(PHP_SERVER["REQUEST_URI"])))}), admin_url("customize.php"))), __("Manage with Live Preview"))
# end if
nonce_ = wp_create_nonce("widgets-access")
php_print("<div class=\"widget-access-link\">\n <a id=\"access-on\" href=\"widgets.php?widgets-access=on&_wpnonce=")
php_print(urlencode(nonce_))
php_print("\">")
_e("Enable accessibility mode")
php_print("</a><a id=\"access-off\" href=\"widgets.php?widgets-access=off&_wpnonce=")
php_print(urlencode(nonce_))
php_print("\">")
_e("Disable accessibility mode")
php_print("""</a>
</div>
<hr class=\"wp-header-end\">
""")
if (php_isset(lambda : PHP_REQUEST["message"])) and (php_isset(lambda : messages_[PHP_REQUEST["message"]])):
    php_print("<div id=\"message\" class=\"updated notice is-dismissible\"><p>")
    php_print(messages_[PHP_REQUEST["message"]])
    php_print("</p></div>\n")
# end if
if (php_isset(lambda : PHP_REQUEST["error"])) and (php_isset(lambda : errors_[PHP_REQUEST["error"]])):
    php_print("<div id=\"message\" class=\"error\"><p>")
    php_print(errors_[PHP_REQUEST["error"]])
    php_print("</p></div>\n")
# end if
php_print("\n")
#// 
#// Fires before the Widgets administration page content loads.
#// 
#// @since 3.0.0
#//
do_action("widgets_admin_page")
php_print("""
<div class=\"widget-liquid-left\">
<div id=\"widgets-left\">
<div id=\"available-widgets\" class=\"widgets-holder-wrap\">
<div class=\"sidebar-name\">
<button type=\"button\" class=\"handlediv hide-if-no-js\" aria-expanded=\"true\">
<span class=\"screen-reader-text\">""")
_e("Available Widgets")
php_print("""</span>
<span class=\"toggle-indicator\" aria-hidden=\"true\"></span>
</button>
<h2>""")
_e("Available Widgets")
php_print(" <span id=\"removing-widget\">")
_ex("Deactivate", "removing-widget")
php_print(""" <span></span></span></h2>
</div>
<div class=\"widget-holder\">
<div class=\"sidebar-description\">
<p class=\"description\">""")
_e("To activate a widget drag it to a sidebar or click on it. To deactivate a widget and delete its settings, drag it back.")
php_print("""</p>
</div>
<div id=\"widget-list\">
""")
wp_list_widgets()
php_print("""           </div>
<br class='clear' />
</div>
<br class=\"clear\" />
</div>
""")
theme_sidebars_ = Array()
for sidebar_,registered_sidebar_ in wp_registered_sidebars_.items():
    if False != php_strpos(registered_sidebar_["class"], "inactive-sidebar") or "orphaned_widgets" == php_substr(sidebar_, 0, 16):
        wrap_class_ = "widgets-holder-wrap"
        if (not php_empty(lambda : registered_sidebar_["class"])):
            wrap_class_ += " " + registered_sidebar_["class"]
        # end if
        is_inactive_widgets_ = "wp_inactive_widgets" == registered_sidebar_["id"]
        php_print("     <div class=\"")
        php_print(esc_attr(wrap_class_))
        php_print("\">\n            <div class=\"widget-holder inactive\">\n                ")
        wp_list_widget_controls(registered_sidebar_["id"], registered_sidebar_["name"])
        php_print("\n               ")
        if is_inactive_widgets_:
            php_print("""               <div class=\"remove-inactive-widgets\">
            <form action=\"\" method=\"post\">
            <p>
            """)
            attributes_ = Array({"id": "inactive-widgets-control-remove"})
            if php_empty(lambda : sidebars_widgets_["wp_inactive_widgets"]):
                attributes_["disabled"] = ""
            # end if
            submit_button(__("Clear Inactive Widgets"), "delete", "removeinactivewidgets", False, attributes_)
            php_print("                         <span class=\"spinner\"></span>\n                       </p>\n                      ")
            wp_nonce_field("remove-inactive-widgets", "_wpnonce_remove_inactive_widgets")
            php_print("                 </form>\n               </div>\n                ")
        # end if
        php_print("         </div>\n            ")
        if is_inactive_widgets_:
            php_print("         <p class=\"description\">")
            _e("This will clear all items from the inactive widgets list. You will not be able to restore any customizations.")
            php_print("</p>\n           ")
        # end if
        php_print("     </div>\n        ")
    else:
        theme_sidebars_[sidebar_] = registered_sidebar_
    # end if
# end for
php_print("</div>\n</div>\n")
i_ = 0
split_ = 0
single_sidebar_class_ = ""
sidebars_count_ = php_count(theme_sidebars_)
if sidebars_count_ > 1:
    split_ = php_int(ceil(sidebars_count_ / 2))
else:
    single_sidebar_class_ = " single-sidebar"
# end if
php_print("<div class=\"widget-liquid-right\">\n<div id=\"widgets-right\" class=\"wp-clearfix")
php_print(single_sidebar_class_)
php_print("\">\n<div class=\"sidebars-column-1\">\n")
for sidebar_,registered_sidebar_ in theme_sidebars_.items():
    wrap_class_ = "widgets-holder-wrap"
    if (not php_empty(lambda : registered_sidebar_["class"])):
        wrap_class_ += " sidebar-" + registered_sidebar_["class"]
    # end if
    if i_ > 0:
        wrap_class_ += " closed"
    # end if
    if split_ and i_ == split_:
        php_print("     </div><div class=\"sidebars-column-2\">\n       ")
    # end if
    php_print(" <div class=\"")
    php_print(esc_attr(wrap_class_))
    php_print("\">\n        ")
    #// Show the control forms for each of the widgets in this sidebar.
    wp_list_widget_controls(sidebar_, registered_sidebar_["name"])
    php_print(" </div>\n    ")
    i_ += 1
# end for
php_print("""</div>
</div>
</div>
<form method=\"post\">
""")
wp_nonce_field("save-sidebar-widgets", "_wpnonce_widgets", False)
php_print("""</form>
<br class=\"clear\" />
</div>
<div class=\"widgets-chooser\">
<ul class=\"widgets-chooser-sidebars\"></ul>
<div class=\"widgets-chooser-actions\">
<button class=\"button widgets-chooser-cancel\">""")
_e("Cancel")
php_print("</button>\n      <button class=\"button button-primary widgets-chooser-add\">")
_e("Add Widget")
php_print("""</button>
</div>
</div>
""")
#// 
#// Fires after the available widgets and sidebars have loaded, before the admin footer.
#// 
#// @since 2.2.0
#//
do_action("sidebar_admin_page")
php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
