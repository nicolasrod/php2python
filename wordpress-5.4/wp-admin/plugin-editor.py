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
#// Edit plugin editor administration panel.
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// WordPress Administration Bootstrap
php_include_file(__DIR__ + "/admin.php", once=True)
if is_multisite() and (not is_network_admin()):
    wp_redirect(network_admin_url("plugin-editor.php"))
    php_exit(0)
# end if
if (not current_user_can("edit_plugins")):
    wp_die(__("Sorry, you are not allowed to edit plugins for this site."))
# end if
title_ = __("Edit Plugins")
parent_file_ = "plugins.php"
plugins_ = get_plugins()
if php_empty(lambda : plugins_):
    php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
    php_print(" <div class=\"wrap\">\n      <h1>")
    php_print(esc_html(title_))
    php_print("</h1>\n      <div id=\"message\" class=\"error\"><p>")
    _e("You do not appear to have any plugins available at this time.")
    php_print("</p></div>\n </div>\n    ")
    php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
    php_exit(0)
# end if
file_ = ""
plugin_ = ""
if (php_isset(lambda : PHP_REQUEST["file"])):
    file_ = wp_unslash(PHP_REQUEST["file"])
# end if
if (php_isset(lambda : PHP_REQUEST["plugin"])):
    plugin_ = wp_unslash(PHP_REQUEST["plugin"])
# end if
if php_empty(lambda : plugin_):
    if file_:
        #// Locate the plugin for a given plugin file being edited.
        file_dirname_ = php_dirname(file_)
        for plugin_candidate_ in php_array_keys(plugins_):
            if plugin_candidate_ == file_ or "." != file_dirname_ and php_dirname(plugin_candidate_) == file_dirname_:
                plugin_ = plugin_candidate_
                break
            # end if
        # end for
        #// Fallback to the file as the plugin.
        if php_empty(lambda : plugin_):
            plugin_ = file_
        # end if
    else:
        plugin_ = php_array_keys(plugins_)
        plugin_ = plugin_[0]
    # end if
# end if
plugin_files_ = get_plugin_files(plugin_)
if php_empty(lambda : file_):
    file_ = plugin_files_[0]
# end if
file_ = validate_file_to_edit(file_, plugin_files_)
real_file_ = WP_PLUGIN_DIR + "/" + file_
#// Handle fallback editing of file when JavaScript is not available.
edit_error_ = None
posted_content_ = None
if "POST" == PHP_SERVER["REQUEST_METHOD"]:
    r_ = wp_edit_theme_plugin_file(wp_unslash(PHP_POST))
    if is_wp_error(r_):
        edit_error_ = r_
        if check_ajax_referer("edit-plugin_" + file_, "nonce", False) and (php_isset(lambda : PHP_POST["newcontent"])):
            posted_content_ = wp_unslash(PHP_POST["newcontent"])
        # end if
    else:
        wp_redirect(add_query_arg(Array({"a": 1, "plugin": plugin_, "file": file_}), admin_url("plugin-editor.php")))
        php_exit(0)
    # end if
# end if
#// List of allowable extensions.
editable_extensions_ = wp_get_plugin_file_editable_extensions(plugin_)
if (not php_is_file(real_file_)):
    wp_die(php_sprintf("<p>%s</p>", __("File does not exist! Please double check the name and try again.")))
else:
    #// Get the extension of the file.
    if php_preg_match("/\\.([^.]+)$/", real_file_, matches_):
        ext_ = php_strtolower(matches_[1])
        #// If extension is not in the acceptable list, skip it.
        if (not php_in_array(ext_, editable_extensions_)):
            wp_die(php_sprintf("<p>%s</p>", __("Files of this type are not editable.")))
        # end if
    # end if
# end if
get_current_screen().add_help_tab(Array({"id": "overview", "title": __("Overview"), "content": "<p>" + __("You can use the plugin editor to make changes to any of your plugins&#8217; individual PHP files. Be aware that if you make changes, plugins updates will overwrite your customizations.") + "</p>" + "<p>" + __("Choose a plugin to edit from the dropdown menu and click the Select button. Click once on any file name to load it in the editor, and make your changes. Don&#8217;t forget to save your changes (Update File) when you&#8217;re finished.") + "</p>" + "<p>" + __("The Documentation menu below the editor lists the PHP functions recognized in the plugin file. Clicking Look Up takes you to a web page about that particular function.") + "</p>" + "<p id=\"editor-keyboard-trap-help-1\">" + __("When using a keyboard to navigate:") + "</p>" + "<ul>" + "<li id=\"editor-keyboard-trap-help-2\">" + __("In the editing area, the Tab key enters a tab character.") + "</li>" + "<li id=\"editor-keyboard-trap-help-3\">" + __("To move away from this area, press the Esc key followed by the Tab key.") + "</li>" + "<li id=\"editor-keyboard-trap-help-4\">" + __("Screen reader users: when in forms mode, you may need to press the Esc key twice.") + "</li>" + "</ul>" + "<p>" + __("If you want to make changes but don&#8217;t want them to be overwritten when the plugin is updated, you may be ready to think about writing your own plugin. For information on how to edit plugins, write your own from scratch, or just better understand their anatomy, check out the links below.") + "</p>" + "<p>" + __("Any edits to files from this screen will be reflected on all sites in the network.") + "</p>" if is_network_admin() else ""}))
get_current_screen().set_help_sidebar("<p><strong>" + __("For more information:") + "</strong></p>" + "<p>" + __("<a href=\"https://wordpress.org/support/article/plugins-editor-screen/\">Documentation on Editing Plugins</a>") + "</p>" + "<p>" + __("<a href=\"https://developer.wordpress.org/plugins/\">Documentation on Writing Plugins</a>") + "</p>" + "<p>" + __("<a href=\"https://wordpress.org/support/\">Support</a>") + "</p>")
settings_ = Array({"codeEditor": wp_enqueue_code_editor(Array({"file": real_file_}))})
wp_enqueue_script("wp-theme-plugin-editor")
wp_add_inline_script("wp-theme-plugin-editor", php_sprintf("jQuery( function( $ ) { wp.themePluginEditor.init( $( \"#template\" ), %s ); } )", wp_json_encode(settings_)))
wp_add_inline_script("wp-theme-plugin-editor", php_sprintf("wp.themePluginEditor.themeOrPlugin = \"plugin\";"))
php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
update_recently_edited(WP_PLUGIN_DIR + "/" + file_)
if (not php_empty(lambda : posted_content_)):
    content_ = posted_content_
else:
    content_ = php_file_get_contents(real_file_)
# end if
if ".php" == php_substr(real_file_, php_strrpos(real_file_, ".")):
    functions_ = wp_doc_link_parse(content_)
    if (not php_empty(lambda : functions_)):
        docs_select_ = "<select name=\"docs-list\" id=\"docs-list\">"
        docs_select_ += "<option value=\"\">" + __("Function Name&hellip;") + "</option>"
        for function_ in functions_:
            docs_select_ += "<option value=\"" + esc_attr(function_) + "\">" + esc_html(function_) + "()</option>"
        # end for
        docs_select_ += "</select>"
    # end if
# end if
content_ = esc_textarea(content_)
php_print("<div class=\"wrap\">\n<h1>")
php_print(esc_html(title_))
php_print("</h1>\n\n")
if (php_isset(lambda : PHP_REQUEST["a"])):
    php_print(" <div id=\"message\" class=\"updated notice is-dismissible\">\n      <p>")
    _e("File edited successfully.")
    php_print("</p>\n   </div>\n")
elif is_wp_error(edit_error_):
    php_print(" <div id=\"message\" class=\"notice notice-error\">\n        <p>")
    _e("There was an error while trying to update the file. You may need to fix something and try updating again.")
    php_print("</p>\n       <pre>")
    php_print(esc_html(edit_error_.get_error_message() if edit_error_.get_error_message() else edit_error_.get_error_code()))
    php_print("</pre>\n </div>\n")
# end if
php_print("""
<div class=\"fileedit-sub\">
<div class=\"alignleft\">
<h2>
""")
if is_plugin_active(plugin_):
    if is_writeable(real_file_):
        #// translators: %s: Plugin file name.
        php_print(php_sprintf(__("Editing %s (active)"), "<strong>" + esc_html(file_) + "</strong>"))
    else:
        #// translators: %s: Plugin file name.
        php_print(php_sprintf(__("Browsing %s (active)"), "<strong>" + esc_html(file_) + "</strong>"))
    # end if
else:
    if is_writeable(real_file_):
        #// translators: %s: Plugin file name.
        php_print(php_sprintf(__("Editing %s (inactive)"), "<strong>" + esc_html(file_) + "</strong>"))
    else:
        #// translators: %s: Plugin file name.
        php_print(php_sprintf(__("Browsing %s (inactive)"), "<strong>" + esc_html(file_) + "</strong>"))
    # end if
# end if
php_print("""</h2>
</div>
<div class=\"alignright\">
<form action=\"plugin-editor.php\" method=\"get\">
<strong><label for=\"plugin\">""")
_e("Select plugin to edit:")
php_print(" </label></strong>\n     <select name=\"plugin\" id=\"plugin\">\n        ")
for plugin_key_,a_plugin_ in plugins_:
    plugin_name_ = a_plugin_["Name"]
    if plugin_key_ == plugin_:
        selected_ = " selected='selected'"
    else:
        selected_ = ""
    # end if
    plugin_name_ = esc_attr(plugin_name_)
    plugin_key_ = esc_attr(plugin_key_)
    php_print(str("\n   <option value=\"") + str(plugin_key_) + str("\" ") + str(selected_) + str(">") + str(plugin_name_) + str("</option>"))
# end for
php_print("     </select>\n     ")
submit_button(__("Select"), "", "Submit", False)
php_print("""   </form>
</div>
<br class=\"clear\" />
</div>
<div id=\"templateside\">
<h2 id=\"plugin-files-label\">""")
_e("Plugin Files")
php_print("</h2>\n\n    ")
plugin_editable_files_ = Array()
for plugin_file_ in plugin_files_:
    if php_preg_match("/\\.([^.]+)$/", plugin_file_, matches_) and php_in_array(matches_[1], editable_extensions_):
        plugin_editable_files_[-1] = plugin_file_
    # end if
# end for
php_print("""   <ul role=\"tree\" aria-labelledby=\"plugin-files-label\">
<li role=\"treeitem\" tabindex=\"-1\" aria-expanded=\"true\" aria-level=\"1\" aria-posinset=\"1\" aria-setsize=\"1\">
<ul role=\"group\">
""")
wp_print_plugin_file_tree(wp_make_plugin_file_tree(plugin_editable_files_))
php_print("""       </ul>
</ul>
</div>
<form name=\"template\" id=\"template\" action=\"plugin-editor.php\" method=\"post\">
""")
wp_nonce_field("edit-plugin_" + file_, "nonce")
php_print(" <div>\n     <label for=\"newcontent\" id=\"theme-plugin-editor-label\">")
_e("Selected file content:")
php_print("</label>\n       <textarea cols=\"70\" rows=\"25\" name=\"newcontent\" id=\"newcontent\" aria-describedby=\"editor-keyboard-trap-help-1 editor-keyboard-trap-help-2 editor-keyboard-trap-help-3 editor-keyboard-trap-help-4\">")
php_print(content_)
php_print("</textarea>\n        <input type=\"hidden\" name=\"action\" value=\"update\" />\n        <input type=\"hidden\" name=\"file\" value=\"")
php_print(esc_attr(file_))
php_print("\" />\n      <input type=\"hidden\" name=\"plugin\" value=\"")
php_print(esc_attr(plugin_))
php_print("""\" />
</div>
""")
if (not php_empty(lambda : docs_select_)):
    php_print("     <div id=\"documentation\" class=\"hide-if-no-js\">\n            <label for=\"docs-list\">")
    _e("Documentation:")
    php_print("</label>\n           ")
    php_print(docs_select_)
    php_print("         <input disabled id=\"docs-lookup\" type=\"button\" class=\"button\" value=\"")
    esc_attr_e("Look Up")
    php_print("\" onclick=\"if ( '' != jQuery('#docs-list').val() ) { window.open( 'https://api.wordpress.org/core/handbook/1.0/?function=' + escape( jQuery( '#docs-list' ).val() ) + '&amp;locale=")
    php_print(urlencode(get_user_locale()))
    php_print("&amp;version=")
    php_print(urlencode(get_bloginfo("version")))
    php_print("&amp;redirect=true'); }\" />\n       </div>\n    ")
# end if
php_print("\n   ")
if is_writeable(real_file_):
    php_print("     <div class=\"editor-notices\">\n        ")
    if php_in_array(plugin_, get_option("active_plugins", Array())):
        php_print("         <div class=\"notice notice-warning inline active-plugin-edit-warning\">\n               <p>")
        _e("<strong>Warning:</strong> Making changes to active plugins is not recommended.")
        php_print("</p>\n           </div>\n        ")
    # end if
    php_print("     </div>\n        <p class=\"submit\">\n          ")
    submit_button(__("Update File"), "primary", "submit", False)
    php_print("         <span class=\"spinner\"></span>\n       </p>\n  ")
else:
    php_print("     <p><em>\n           ")
    printf(__("You need to make this file writable before you can save your changes. See <a href=\"%s\">Changing File Permissions</a> for more information."), __("https://wordpress.org/support/article/changing-file-permissions/"))
    php_print("     </em></p>\n ")
# end if
php_print("\n   ")
wp_print_file_editor_templates()
php_print("""</form>
<br class=\"clear\" />
</div>
""")
dismissed_pointers_ = php_explode(",", php_str(get_user_meta(get_current_user_id(), "dismissed_wp_pointers", True)))
if (not php_in_array("plugin_editor_notice", dismissed_pointers_, True)):
    #// Get a back URL.
    referer_ = wp_get_referer()
    excluded_referer_basenames_ = Array("plugin-editor.php", "wp-login.php")
    if referer_ and (not php_in_array(php_basename(php_parse_url(referer_, PHP_URL_PATH)), excluded_referer_basenames_, True)):
        return_url_ = referer_
    else:
        return_url_ = admin_url("/")
    # end if
    php_print("""   <div id=\"file-editor-warning\" class=\"notification-dialog-wrap file-editor-warning hide-if-no-js hidden\">
    <div class=\"notification-dialog-background\"></div>
    <div class=\"notification-dialog\">
    <div class=\"file-editor-warning-content\">
    <div class=\"file-editor-warning-message\">
    <h1>""")
    _e("Heads up!")
    php_print("</h1>\n                  <p>")
    _e("You appear to be making direct edits to your plugin in the WordPress dashboard. We recommend that you don&#8217;t! Editing plugins directly may introduce incompatibilities that break your site and your changes may be lost in future updates.")
    php_print("</p>\n                   <p>")
    _e("If you absolutely have to make direct edits to this plugin, use a file manager to create a copy with a new name and hang on to the original. That way, you can re-enable a functional version if something goes wrong.")
    php_print("""</p>
    </div>
    <p>
    <a class=\"button file-editor-warning-go-back\" href=\"""")
    php_print(esc_url(return_url_))
    php_print("\">")
    _e("Go back")
    php_print("</a>\n                   <button type=\"button\" class=\"file-editor-warning-dismiss button button-primary\">")
    _e("I understand")
    php_print("""</button>
    </p>
    </div>
    </div>
    </div>
    """)
# end if
#// Editor warning notice.
php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
