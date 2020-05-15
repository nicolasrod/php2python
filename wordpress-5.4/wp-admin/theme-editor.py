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
#// Theme editor administration panel.
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// WordPress Administration Bootstrap
php_include_file(__DIR__ + "/admin.php", once=True)
if is_multisite() and (not is_network_admin()):
    wp_redirect(network_admin_url("theme-editor.php"))
    php_exit(0)
# end if
if (not current_user_can("edit_themes")):
    wp_die("<p>" + __("Sorry, you are not allowed to edit templates for this site.") + "</p>")
# end if
title = __("Edit Themes")
parent_file = "themes.php"
get_current_screen().add_help_tab(Array({"id": "overview", "title": __("Overview"), "content": "<p>" + __("You can use the theme editor to edit the individual CSS and PHP files which make up your theme.") + "</p>" + "<p>" + __("Begin by choosing a theme to edit from the dropdown menu and clicking the Select button. A list then appears of the theme&#8217;s template files. Clicking once on any file name causes the file to appear in the large Editor box.") + "</p>" + "<p>" + __("For PHP files, you can use the Documentation dropdown to select from functions recognized in that file. Look Up takes you to a web page with reference material about that particular function.") + "</p>" + "<p id=\"editor-keyboard-trap-help-1\">" + __("When using a keyboard to navigate:") + "</p>" + "<ul>" + "<li id=\"editor-keyboard-trap-help-2\">" + __("In the editing area, the Tab key enters a tab character.") + "</li>" + "<li id=\"editor-keyboard-trap-help-3\">" + __("To move away from this area, press the Esc key followed by the Tab key.") + "</li>" + "<li id=\"editor-keyboard-trap-help-4\">" + __("Screen reader users: when in forms mode, you may need to press the Esc key twice.") + "</li>" + "</ul>" + "<p>" + __("After typing in your edits, click Update File.") + "</p>" + "<p>" + __("<strong>Advice:</strong> Think very carefully about your site crashing if you are live-editing the theme currently in use.") + "</p>" + "<p>" + php_sprintf(__("Upgrading to a newer version of the same theme will override changes made here. To avoid this, consider creating a <a href=\"%s\">child theme</a> instead."), __("https://developer.wordpress.org/themes/advanced-topics/child-themes/")) + "</p>" + "<p>" + __("Any edits to files from this screen will be reflected on all sites in the network.") + "</p>" if is_network_admin() else ""}))
get_current_screen().set_help_sidebar("<p><strong>" + __("For more information:") + "</strong></p>" + "<p>" + __("<a href=\"https://developer.wordpress.org/themes/\">Documentation on Theme Development</a>") + "</p>" + "<p>" + __("<a href=\"https://wordpress.org/support/article/using-themes/\">Documentation on Using Themes</a>") + "</p>" + "<p>" + __("<a href=\"https://wordpress.org/support/article/editing-files/\">Documentation on Editing Files</a>") + "</p>" + "<p>" + __("<a href=\"https://developer.wordpress.org/themes/basics/template-tags/\">Documentation on Template Tags</a>") + "</p>" + "<p>" + __("<a href=\"https://wordpress.org/support/\">Support</a>") + "</p>")
wp_reset_vars(Array("action", "error", "file", "theme"))
if theme:
    stylesheet = theme
else:
    stylesheet = get_stylesheet()
# end if
theme = wp_get_theme(stylesheet)
if (not theme.exists()):
    wp_die(__("The requested theme does not exist."))
# end if
if theme.errors() and "theme_no_stylesheet" == theme.errors().get_error_code():
    wp_die(__("The requested theme does not exist.") + " " + theme.errors().get_error_message())
# end if
allowed_files = Array()
style_files = Array()
has_templates = False
file_types = wp_get_theme_file_editable_extensions(theme)
for type in file_types:
    for case in Switch(type):
        if case("php"):
            allowed_files += theme.get_files("php", -1)
            has_templates = (not php_empty(lambda : allowed_files))
            break
        # end if
        if case("css"):
            style_files = theme.get_files("css", -1)
            allowed_files["style.css"] = style_files["style.css"]
            allowed_files += style_files
            break
        # end if
        if case():
            allowed_files += theme.get_files(type, -1)
            break
        # end if
    # end for
# end for
#// Move functions.php and style.css to the top.
if (php_isset(lambda : allowed_files["functions.php"])):
    allowed_files = Array({"functions.php": allowed_files["functions.php"]}) + allowed_files
# end if
if (php_isset(lambda : allowed_files["style.css"])):
    allowed_files = Array({"style.css": allowed_files["style.css"]}) + allowed_files
# end if
if php_empty(lambda : file):
    relative_file = "style.css"
    file = allowed_files["style.css"]
else:
    relative_file = wp_unslash(file)
    file = theme.get_stylesheet_directory() + "/" + relative_file
# end if
validate_file_to_edit(file, allowed_files)
#// Handle fallback editing of file when JavaScript is not available.
edit_error = None
posted_content = None
if "POST" == PHP_SERVER["REQUEST_METHOD"]:
    r = wp_edit_theme_plugin_file(wp_unslash(PHP_POST))
    if is_wp_error(r):
        edit_error = r
        if check_ajax_referer("edit-theme_" + stylesheet + "_" + relative_file, "nonce", False) and (php_isset(lambda : PHP_POST["newcontent"])):
            posted_content = wp_unslash(PHP_POST["newcontent"])
        # end if
    else:
        wp_redirect(add_query_arg(Array({"a": 1, "theme": stylesheet, "file": relative_file}), admin_url("theme-editor.php")))
        php_exit(0)
    # end if
# end if
settings = Array({"codeEditor": wp_enqueue_code_editor(compact("file"))})
wp_enqueue_script("wp-theme-plugin-editor")
wp_add_inline_script("wp-theme-plugin-editor", php_sprintf("jQuery( function( $ ) { wp.themePluginEditor.init( $( \"#template\" ), %s ); } )", wp_json_encode(settings)))
wp_add_inline_script("wp-theme-plugin-editor", "wp.themePluginEditor.themeOrPlugin = \"theme\";")
php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
update_recently_edited(file)
if (not php_is_file(file)):
    error = True
# end if
content = ""
if (not php_empty(lambda : posted_content)):
    content = posted_content
elif (not error) and filesize(file) > 0:
    f = fopen(file, "r")
    content = fread(f, filesize(file))
    if ".php" == php_substr(file, php_strrpos(file, ".")):
        functions = wp_doc_link_parse(content)
        docs_select = "<select name=\"docs-list\" id=\"docs-list\">"
        docs_select += "<option value=\"\">" + esc_attr__("Function Name&hellip;") + "</option>"
        for function in functions:
            docs_select += "<option value=\"" + esc_attr(urlencode(function)) + "\">" + htmlspecialchars(function) + "()</option>"
        # end for
        docs_select += "</select>"
    # end if
    content = esc_textarea(content)
# end if
file_description = get_file_description(relative_file)
file_show = php_array_search(file, php_array_filter(allowed_files))
description = esc_html(file_description)
if file_description != file_show:
    description += " <span>(" + esc_html(file_show) + ")</span>"
# end if
php_print("<div class=\"wrap\">\n<h1>")
php_print(esc_html(title))
php_print("</h1>\n\n")
if (php_isset(lambda : PHP_REQUEST["a"])):
    php_print(" <div id=\"message\" class=\"updated notice is-dismissible\">\n      <p>")
    _e("File edited successfully.")
    php_print("</p>\n   </div>\n")
elif is_wp_error(edit_error):
    php_print(" <div id=\"message\" class=\"notice notice-error\">\n        <p>")
    _e("There was an error while trying to update the file. You may need to fix something and try updating again.")
    php_print("</p>\n       <pre>")
    php_print(esc_html(edit_error.get_error_message() if edit_error.get_error_message() else edit_error.get_error_code()))
    php_print("</pre>\n </div>\n")
# end if
php_print("\n")
if php_preg_match("/\\.css$/", file):
    php_print(" <div id=\"message\" class=\"notice-info notice\">\n     <p><strong>")
    _e("Did you know?")
    php_print("</strong></p>\n      <p>\n           ")
    php_print(php_sprintf(__("There&#8217;s no need to change your CSS here &mdash; you can edit and live preview CSS changes in the <a href=\"%s\">built-in CSS editor</a>."), esc_url(add_query_arg("autofocus[section]", "custom_css", admin_url("customize.php")))))
    php_print("     </p>\n  </div>\n")
# end if
php_print("""
<div class=\"fileedit-sub\">
<div class=\"alignleft\">
<h2>
""")
php_print(theme.display("Name"))
if description:
    php_print(": " + description)
# end if
php_print("""</h2>
</div>
<div class=\"alignright\">
<form action=\"theme-editor.php\" method=\"get\">
<strong><label for=\"theme\">""")
_e("Select theme to edit:")
php_print(" </label></strong>\n     <select name=\"theme\" id=\"theme\">\n      ")
for a_stylesheet,a_theme in wp_get_themes(Array({"errors": None})):
    if a_theme.errors() and "theme_no_stylesheet" == a_theme.errors().get_error_code():
        continue
    # end if
    selected = " selected=\"selected\"" if a_stylesheet == stylesheet else ""
    php_print("\n   " + "<option value=\"" + esc_attr(a_stylesheet) + "\"" + selected + ">" + a_theme.display("Name") + "</option>")
# end for
php_print("     </select>\n     ")
submit_button(__("Select"), "", "Submit", False)
php_print("""   </form>
</div>
<br class=\"clear\" />
</div>
""")
if theme.errors():
    php_print("<div class=\"error\"><p><strong>" + __("This theme is broken.") + "</strong> " + theme.errors().get_error_message() + "</p></div>")
# end if
php_print("\n<div id=\"templateside\">\n    <h2 id=\"theme-files-label\">")
_e("Theme Files")
php_print("</h2>\n  <ul role=\"tree\" aria-labelledby=\"theme-files-label\">\n      ")
if has_templates or theme.parent() and theme.parent():
    php_print("         <li class=\"howto\">\n              ")
    printf(__("This child theme inherits templates from a parent theme, %s."), php_sprintf("<a href=\"%s\">%s</a>", self_admin_url("theme-editor.php?theme=" + urlencode(theme.get_template())), theme.parent().display("Name")))
    php_print("         </li>\n     ")
# end if
php_print("     <li role=\"treeitem\" tabindex=\"-1\" aria-expanded=\"true\" aria-level=\"1\" aria-posinset=\"1\" aria-setsize=\"1\">\n         <ul role=\"group\">\n               ")
wp_print_theme_file_tree(wp_make_theme_file_tree(allowed_files))
php_print("""           </ul>
</li>
</ul>
</div>
""")
if error:
    php_print("<div class=\"error\"><p>" + __("File does not exist! Please double check the name and try again.") + "</p></div>")
else:
    php_print(" <form name=\"template\" id=\"template\" action=\"theme-editor.php\" method=\"post\">\n      ")
    wp_nonce_field("edit-theme_" + stylesheet + "_" + relative_file, "nonce")
    php_print("     <div>\n         <label for=\"newcontent\" id=\"theme-plugin-editor-label\">")
    _e("Selected file content:")
    php_print("</label>\n           <textarea cols=\"70\" rows=\"30\" name=\"newcontent\" id=\"newcontent\" aria-describedby=\"editor-keyboard-trap-help-1 editor-keyboard-trap-help-2 editor-keyboard-trap-help-3 editor-keyboard-trap-help-4\">")
    php_print(content)
    php_print("</textarea>\n            <input type=\"hidden\" name=\"action\" value=\"update\" />\n            <input type=\"hidden\" name=\"file\" value=\"")
    php_print(esc_attr(relative_file))
    php_print("\" />\n          <input type=\"hidden\" name=\"theme\" value=\"")
    php_print(esc_attr(theme.get_stylesheet()))
    php_print("""\" />
    </div>
    """)
    if (not php_empty(lambda : functions)):
        php_print("         <div id=\"documentation\" class=\"hide-if-no-js\">\n                <label for=\"docs-list\">")
        _e("Documentation:")
        php_print("</label>\n               ")
        php_print(docs_select)
        php_print("             <input disabled id=\"docs-lookup\" type=\"button\" class=\"button\" value=\"")
        esc_attr_e("Look Up")
        php_print("\" onclick=\"if ( '' != jQuery('#docs-list').val() ) { window.open( 'https://api.wordpress.org/core/handbook/1.0/?function=' + escape( jQuery( '#docs-list' ).val() ) + '&amp;locale=")
        php_print(urlencode(get_user_locale()))
        php_print("&amp;version=")
        php_print(urlencode(get_bloginfo("version")))
        php_print("&amp;redirect=true'); }\" />\n           </div>\n        ")
    # end if
    php_print("""
    <div>
    <div class=\"editor-notices\">
    """)
    if is_child_theme() and theme.get_stylesheet() == get_template():
        php_print("                 <div class=\"notice notice-warning inline\">\n                      <p>\n                           ")
        if is_writeable(file):
            php_print("                             <strong>")
            _e("Caution:")
            php_print("</strong>\n                          ")
        # end if
        php_print("                         ")
        _e("This is a file in your current parent theme.")
        php_print("                     </p>\n                  </div>\n                ")
    # end if
    php_print("         </div>\n            ")
    if is_writeable(file):
        php_print("             <p class=\"submit\">\n                  ")
        submit_button(__("Update File"), "primary", "submit", False)
        php_print("                 <span class=\"spinner\"></span>\n               </p>\n          ")
    else:
        php_print("             <p><em>\n                   ")
        printf(__("You need to make this file writable before you can save your changes. See <a href=\"%s\">Changing File Permissions</a> for more information."), __("https://wordpress.org/support/article/changing-file-permissions/"))
        php_print("             </em></p>\n         ")
    # end if
    php_print("     </div>\n\n      ")
    wp_print_file_editor_templates()
    php_print(" </form>\n   ")
# end if
pass
php_print("<br class=\"clear\" />\n</div>\n")
dismissed_pointers = php_explode(",", str(get_user_meta(get_current_user_id(), "dismissed_wp_pointers", True)))
if (not php_in_array("theme_editor_notice", dismissed_pointers, True)):
    #// Get a back URL.
    referer = wp_get_referer()
    excluded_referer_basenames = Array("theme-editor.php", "wp-login.php")
    if referer and (not php_in_array(php_basename(php_parse_url(referer, PHP_URL_PATH)), excluded_referer_basenames, True)):
        return_url = referer
    else:
        return_url = admin_url("/")
    # end if
    php_print("""   <div id=\"file-editor-warning\" class=\"notification-dialog-wrap file-editor-warning hide-if-no-js hidden\">
    <div class=\"notification-dialog-background\"></div>
    <div class=\"notification-dialog\">
    <div class=\"file-editor-warning-content\">
    <div class=\"file-editor-warning-message\">
    <h1>""")
    _e("Heads up!")
    php_print("</h1>\n                  <p>\n                       ")
    _e("You appear to be making direct edits to your theme in the WordPress dashboard. We recommend that you don&#8217;t! Editing your theme directly could break your site and your changes may be lost in future updates.")
    php_print("                 </p>\n                      ")
    if (not theme.parent()):
        php_print("<p>")
        php_print(php_sprintf(__("If you need to tweak more than your theme&#8217;s CSS, you might want to try <a href=\"%s\">making a child theme</a>."), esc_url(__("https://developer.wordpress.org/themes/advanced-topics/child-themes/"))))
        php_print("</p>")
    # end if
    php_print("                 <p>")
    _e("If you decide to go ahead with direct edits anyway, use a file manager to create a copy with a new name and hang on to the original. That way, you can re-enable a functional version if something goes wrong.")
    php_print("""</p>
    </div>
    <p>
    <a class=\"button file-editor-warning-go-back\" href=\"""")
    php_print(esc_url(return_url))
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
