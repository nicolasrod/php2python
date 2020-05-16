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
#// WordPress Export Administration Screen
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// Load WordPress Bootstrap
php_include_file(__DIR__ + "/admin.php", once=True)
if (not current_user_can("export")):
    wp_die(__("Sorry, you are not allowed to export the content of this site."))
# end if
#// Load WordPress export API
php_include_file(ABSPATH + "wp-admin/includes/export.php", once=True)
title = __("Export")
#// 
#// Display JavaScript on the page.
#// 
#// @since 3.5.0
#//
def export_add_js(*args_):
    
    php_print("""<script type=\"text/javascript\">
    jQuery(document).ready(function($){
    var form = $('#export-filters'),
    filters = form.find('.export-filters');
    filters.hide();
    form.find('input:radio').change(function() {
    filters.slideUp('fast');
    switch ( $(this).val() ) {
    case 'attachment': $('#attachment-filters').slideDown(); break;
    case 'posts': $('#post-filters').slideDown(); break;
    case 'pages': $('#page-filters').slideDown(); break;
    }
    });
    });
    </script>
    """)
# end def export_add_js
add_action("admin_head", "export_add_js")
get_current_screen().add_help_tab(Array({"id": "overview", "title": __("Overview"), "content": "<p>" + __("You can export a file of your site&#8217;s content in order to import it into another installation or platform. The export file will be an XML file format called WXR. Posts, pages, comments, custom fields, categories, and tags can be included. You can choose for the WXR file to include only certain posts or pages by setting the dropdown filters to limit the export by category, author, date range by month, or publishing status.") + "</p>" + "<p>" + __("Once generated, your WXR file can be imported by another WordPress site or by another blogging platform able to access this format.") + "</p>"}))
get_current_screen().set_help_sidebar("<p><strong>" + __("For more information:") + "</strong></p>" + "<p>" + __("<a href=\"https://wordpress.org/support/article/tools-export-screen/\">Documentation on Export</a>") + "</p>" + "<p>" + __("<a href=\"https://wordpress.org/support/\">Support</a>") + "</p>")
#// If the 'download' URL parameter is set, a WXR export file is baked and returned.
if (php_isset(lambda : PHP_REQUEST["download"])):
    args = Array()
    if (not (php_isset(lambda : PHP_REQUEST["content"]))) or "all" == PHP_REQUEST["content"]:
        args["content"] = "all"
    elif "posts" == PHP_REQUEST["content"]:
        args["content"] = "post"
        if PHP_REQUEST["cat"]:
            args["category"] = php_int(PHP_REQUEST["cat"])
        # end if
        if PHP_REQUEST["post_author"]:
            args["author"] = php_int(PHP_REQUEST["post_author"])
        # end if
        if PHP_REQUEST["post_start_date"] or PHP_REQUEST["post_end_date"]:
            args["start_date"] = PHP_REQUEST["post_start_date"]
            args["end_date"] = PHP_REQUEST["post_end_date"]
        # end if
        if PHP_REQUEST["post_status"]:
            args["status"] = PHP_REQUEST["post_status"]
        # end if
    elif "pages" == PHP_REQUEST["content"]:
        args["content"] = "page"
        if PHP_REQUEST["page_author"]:
            args["author"] = php_int(PHP_REQUEST["page_author"])
        # end if
        if PHP_REQUEST["page_start_date"] or PHP_REQUEST["page_end_date"]:
            args["start_date"] = PHP_REQUEST["page_start_date"]
            args["end_date"] = PHP_REQUEST["page_end_date"]
        # end if
        if PHP_REQUEST["page_status"]:
            args["status"] = PHP_REQUEST["page_status"]
        # end if
    elif "attachment" == PHP_REQUEST["content"]:
        args["content"] = "attachment"
        if PHP_REQUEST["attachment_start_date"] or PHP_REQUEST["attachment_end_date"]:
            args["start_date"] = PHP_REQUEST["attachment_start_date"]
            args["end_date"] = PHP_REQUEST["attachment_end_date"]
        # end if
    else:
        args["content"] = PHP_REQUEST["content"]
    # end if
    #// 
    #// Filters the export args.
    #// 
    #// @since 3.5.0
    #// 
    #// @param array $args The arguments to send to the exporter.
    #//
    args = apply_filters("export_args", args)
    export_wp(args)
    php_exit(0)
# end if
php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
#// 
#// Create the date options fields for exporting a given post type.
#// 
#// @global wpdb      $wpdb      WordPress database abstraction object.
#// @global WP_Locale $wp_locale WordPress date and time locale object.
#// 
#// @since 3.1.0
#// 
#// @param string $post_type The post type. Default 'post'.
#//
def export_date_options(post_type="post", *args_):
    
    global wpdb,wp_locale
    php_check_if_defined("wpdb","wp_locale")
    months = wpdb.get_results(wpdb.prepare(str("\n      SELECT DISTINCT YEAR( post_date ) AS year, MONTH( post_date ) AS month\n        FROM ") + str(wpdb.posts) + str("""\n       WHERE post_type = %s AND post_status != 'auto-draft'\n      ORDER BY post_date DESC\n   """), post_type))
    month_count = php_count(months)
    if (not month_count) or 1 == month_count and 0 == months[0].month:
        return
    # end if
    for date in months:
        if 0 == date.year:
            continue
        # end if
        month = zeroise(date.month, 2)
        php_print("<option value=\"" + date.year + "-" + month + "\">" + wp_locale.get_month(month) + " " + date.year + "</option>")
    # end for
# end def export_date_options
php_print("\n<div class=\"wrap\">\n<h1>")
php_print(esc_html(title))
php_print("</h1>\n\n<p>")
_e("When you click the button below WordPress will create an XML file for you to save to your computer.")
php_print("</p>\n<p>")
_e("This format, which we call WordPress eXtended RSS or WXR, will contain your posts, pages, comments, custom fields, categories, and tags.")
php_print("</p>\n<p>")
_e("Once you&#8217;ve saved the download file, you can use the Import function in another WordPress installation to import the content from this site.")
php_print("</p>\n\n<h2>")
_e("Choose what to export")
php_print("""</h2>
<form method=\"get\" id=\"export-filters\">
<fieldset>
<legend class=\"screen-reader-text\">""")
_e("Content to export")
php_print("</legend>\n<input type=\"hidden\" name=\"download\" value=\"true\" />\n<p><label><input type=\"radio\" name=\"content\" value=\"all\" checked=\"checked\" aria-describedby=\"all-content-desc\" /> ")
_e("All content")
php_print("</label></p>\n<p class=\"description\" id=\"all-content-desc\">")
_e("This will contain all of your posts, pages, comments, custom fields, terms, navigation menus, and custom posts.")
php_print("</p>\n\n<p><label><input type=\"radio\" name=\"content\" value=\"posts\" /> ")
_ex("Posts", "post type general name")
php_print("""</label></p>
<ul id=\"post-filters\" class=\"export-filters\">
<li>
<label><span class=\"label-responsive\">""")
_e("Categories:")
php_print("</span>\n        ")
wp_dropdown_categories(Array({"show_option_all": __("All")}))
php_print("""       </label>
</li>
<li>
<label><span class=\"label-responsive\">""")
_e("Authors:")
php_print("</span>\n        ")
authors = wpdb.get_col(str("SELECT DISTINCT post_author FROM ") + str(wpdb.posts) + str(" WHERE post_type = 'post'"))
wp_dropdown_users(Array({"include": authors, "name": "post_author", "multi": True, "show_option_all": __("All"), "show": "display_name_with_login"}))
php_print("""       </label>
</li>
<li>
<fieldset>
<legend class=\"screen-reader-text\">""")
_e("Date range:")
php_print("</legend>\n      <label for=\"post-start-date\" class=\"label-responsive\">")
_e("Start date:")
php_print("</label>\n       <select name=\"post_start_date\" id=\"post-start-date\">\n          <option value=\"0\">")
_e("&mdash; Select &mdash;")
php_print("</option>\n          ")
export_date_options()
php_print("     </select>\n     <label for=\"post-end-date\" class=\"label-responsive\">")
_e("End date:")
php_print("</label>\n       <select name=\"post_end_date\" id=\"post-end-date\">\n          <option value=\"0\">")
_e("&mdash; Select &mdash;")
php_print("</option>\n          ")
export_date_options()
php_print("""       </select>
</fieldset>
</li>
<li>
<label for=\"post-status\" class=\"label-responsive\">""")
_e("Status:")
php_print("</label>\n       <select name=\"post_status\" id=\"post-status\">\n          <option value=\"0\">")
_e("All")
php_print("</option>\n          ")
post_stati = get_post_stati(Array({"internal": False}), "objects")
for status in post_stati:
    php_print("         <option value=\"")
    php_print(esc_attr(status.name))
    php_print("\">")
    php_print(esc_html(status.label))
    php_print("</option>\n          ")
# end for
php_print("""       </select>
</li>
</ul>
<p><label><input type=\"radio\" name=\"content\" value=\"pages\" /> """)
_e("Pages")
php_print("""</label></p>
<ul id=\"page-filters\" class=\"export-filters\">
<li>
<label><span class=\"label-responsive\">""")
_e("Authors:")
php_print("</span>\n        ")
authors = wpdb.get_col(str("SELECT DISTINCT post_author FROM ") + str(wpdb.posts) + str(" WHERE post_type = 'page'"))
wp_dropdown_users(Array({"include": authors, "name": "page_author", "multi": True, "show_option_all": __("All"), "show": "display_name_with_login"}))
php_print("""       </label>
</li>
<li>
<fieldset>
<legend class=\"screen-reader-text\">""")
_e("Date range:")
php_print("</legend>\n      <label for=\"page-start-date\" class=\"label-responsive\">")
_e("Start date:")
php_print("</label>\n       <select name=\"page_start_date\" id=\"page-start-date\">\n          <option value=\"0\">")
_e("&mdash; Select &mdash;")
php_print("</option>\n          ")
export_date_options("page")
php_print("     </select>\n     <label for=\"page-end-date\" class=\"label-responsive\">")
_e("End date:")
php_print("</label>\n       <select name=\"page_end_date\" id=\"page-end-date\">\n          <option value=\"0\">")
_e("&mdash; Select &mdash;")
php_print("</option>\n          ")
export_date_options("page")
php_print("""       </select>
</fieldset>
</li>
<li>
<label for=\"page-status\" class=\"label-responsive\">""")
_e("Status:")
php_print("</label>\n       <select name=\"page_status\" id=\"page-status\">\n          <option value=\"0\">")
_e("All")
php_print("</option>\n          ")
for status in post_stati:
    php_print("         <option value=\"")
    php_print(esc_attr(status.name))
    php_print("\">")
    php_print(esc_html(status.label))
    php_print("</option>\n          ")
# end for
php_print("""       </select>
</li>
</ul>
""")
for post_type in get_post_types(Array({"_builtin": False, "can_export": True}), "objects"):
    php_print("<p><label><input type=\"radio\" name=\"content\" value=\"")
    php_print(esc_attr(post_type.name))
    php_print("\" /> ")
    php_print(esc_html(post_type.label))
    php_print("</label></p>\n")
# end for
php_print("\n<p><label><input type=\"radio\" name=\"content\" value=\"attachment\" /> ")
_e("Media")
php_print("""</label></p>
<ul id=\"attachment-filters\" class=\"export-filters\">
<li>
<fieldset>
<legend class=\"screen-reader-text\">""")
_e("Date range:")
php_print("</legend>\n      <label for=\"attachment-start-date\" class=\"label-responsive\">")
_e("Start date:")
php_print("</label>\n       <select name=\"attachment_start_date\" id=\"attachment-start-date\">\n          <option value=\"0\">")
_e("&mdash; Select &mdash;")
php_print("</option>\n          ")
export_date_options("attachment")
php_print("     </select>\n     <label for=\"attachment-end-date\" class=\"label-responsive\">")
_e("End date:")
php_print("</label>\n       <select name=\"attachment_end_date\" id=\"attachment-end-date\">\n          <option value=\"0\">")
_e("&mdash; Select &mdash;")
php_print("</option>\n          ")
export_date_options("attachment")
php_print("""       </select>
</fieldset>
</li>
</ul>
</fieldset>
""")
#// 
#// Fires at the end of the export filters form.
#// 
#// @since 3.5.0
#//
do_action("export_filters")
php_print("\n")
submit_button(__("Download Export File"))
php_print("""</form>
</div>
""")
php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
