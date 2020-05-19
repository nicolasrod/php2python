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
#// Tools Administration Screen.
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// WordPress Administration Bootstrap
php_include_file(__DIR__ + "/admin.php", once=True)
title_ = __("Site Health Info")
if (not current_user_can("view_site_health_checks")):
    wp_die(__("Sorry, you are not allowed to access the debug data."), "", 403)
# end if
wp_enqueue_style("site-health")
wp_enqueue_script("site-health")
if (not php_class_exists("WP_Debug_Data")):
    php_include_file(ABSPATH + "wp-admin/includes/class-wp-debug-data.php", once=True)
# end if
if (not php_class_exists("WP_Site_Health")):
    php_include_file(ABSPATH + "wp-admin/includes/class-wp-site-health.php", once=True)
# end if
health_check_site_status_ = WP_Site_Health.get_instance()
php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
php_print("""<div class=\"health-check-header\">
<div class=\"health-check-title-section\">
<h1>
""")
_e("Site Health")
php_print("""       </h1>
</div>
<div class=\"health-check-title-section site-health-progress-wrapper loading hide-if-no-js\">
<div class=\"site-health-progress\">
<svg role=\"img\" aria-hidden=\"true\" focusable=\"false\" width=\"100%\" height=\"100%\" viewBox=\"0 0 200 200\" version=\"1.1\" xmlns=\"http://www.w3.org/2000/svg\">
<circle r=\"90\" cx=\"100\" cy=\"100\" fill=\"transparent\" stroke-dasharray=\"565.48\" stroke-dashoffset=\"0\"></circle>
<circle id=\"bar\" r=\"90\" cx=\"100\" cy=\"100\" fill=\"transparent\" stroke-dasharray=\"565.48\" stroke-dashoffset=\"0\"></circle>
</svg>
</div>
<div class=\"site-health-progress-label\">
""")
_e("Results are still loading&hellip;")
php_print("""       </div>
</div>
<nav class=\"health-check-tabs-wrapper hide-if-no-js\" aria-label=\"""")
esc_attr_e("Secondary menu")
php_print("\">\n        <a href=\"")
php_print(esc_url(admin_url("site-health.php")))
php_print("\" class=\"health-check-tab\">\n         ")
#// translators: Tab heading for Site Health Status page.
_ex("Status", "Site Health")
php_print("     </a>\n\n        <a href=\"")
php_print(esc_url(admin_url("site-health.php?tab=debug")))
php_print("\" class=\"health-check-tab active\" aria-current=\"true\">\n            ")
#// translators: Tab heading for Site Health Info page.
_ex("Info", "Site Health")
php_print("""       </a>
</nav>
</div>
<hr class=\"wp-header-end\">
<div class=\"notice notice-error hide-if-js\">
<p>""")
_e("The Site Health check requires JavaScript.")
php_print("""</p>
</div>
<div class=\"health-check-body health-check-debug-tab hide-if-no-js\">
""")
WP_Debug_Data.check_for_updates()
info_ = WP_Debug_Data.debug_data()
php_print("\n   <h2>\n      ")
_e("Site Health Info")
php_print("""   </h2>
<p>
""")
#// translators: %s: URL to Site Health Status page.
php_printf(__("This page can show you every detail about the configuration of your WordPress website. For any improvements that could be made, see the <a href=\"%s\">Site Health Status</a> page."), esc_url(admin_url("site-health.php")))
php_print(" </p>\n  <p>\n       ")
_e("If you want to export a handy list of all the information on this page, you can use the button below to copy it to the clipboard. You can then paste it in a text file and save it to your device, or paste it in an email exchange with a support engineer or theme/plugin developer for example.")
php_print("""   </p>
<div class=\"site-health-copy-buttons\">
<div class=\"copy-button-wrapper\">
<button type=\"button\" class=\"button copy-button\" data-clipboard-text=\"""")
php_print(esc_attr(WP_Debug_Data.format(info_, "debug")))
php_print("\">\n                ")
_e("Copy site info to clipboard")
php_print("         </button>\n         <span class=\"success\" aria-hidden=\"true\">")
_e("Copied!")
php_print("""</span>
</div>
</div>
<div id=\"health-check-debug\" class=\"health-check-accordion\">
""")
sizes_fields_ = Array("uploads_size", "themes_size", "plugins_size", "wordpress_size", "database_size", "total_size")
for section_,details_ in info_.items():
    if (not (php_isset(lambda : details_["fields"]))) or php_empty(lambda : details_["fields"]):
        continue
    # end if
    php_print("         <h3 class=\"health-check-accordion-heading\">\n             <button aria-expanded=\"false\" class=\"health-check-accordion-trigger\" aria-controls=\"health-check-accordion-block-")
    php_print(esc_attr(section_))
    php_print("\" type=\"button\">\n                    <span class=\"title\">\n                        ")
    php_print(esc_html(details_["label"]))
    php_print("                     ")
    if (php_isset(lambda : details_["show_count"])) and details_["show_count"]:
        php_printf("(%d)", php_count(details_["fields"]))
    # end if
    php_print("                 </span>\n                   ")
    if "wp-paths-sizes" == section_:
        php_print("                     <span class=\"health-check-wp-paths-sizes spinner\"></span>\n                       ")
    # end if
    php_print("""                   <span class=\"icon\"></span>
    </button>
    </h3>
    <div id=\"health-check-accordion-block-""")
    php_print(esc_attr(section_))
    php_print("\" class=\"health-check-accordion-panel\" hidden=\"hidden\">\n               ")
    if (php_isset(lambda : details_["description"])) and (not php_empty(lambda : details_["description"])):
        php_printf("<p>%s</p>", details_["description"])
    # end if
    php_print("             <table class=\"widefat striped health-check-table\" role=\"presentation\">\n                    <tbody>\n                   ")
    for field_name_,field_ in details_["fields"].items():
        if php_is_array(field_["value"]):
            values_ = "<ul>"
            for name_,value_ in field_["value"].items():
                values_ += php_sprintf("<li>%s: %s</li>", esc_html(name_), esc_html(value_))
            # end for
            values_ += "</ul>"
        else:
            values_ = esc_html(field_["value"])
        # end if
        if php_in_array(field_name_, sizes_fields_, True):
            php_printf("<tr><td>%s</td><td class=\"%s\">%s</td></tr>", esc_html(field_["label"]), esc_attr(field_name_), values_)
        else:
            php_printf("<tr><td>%s</td><td>%s</td></tr>", esc_html(field_["label"]), values_)
        # end if
    # end for
    php_print("""                   </tbody>
    </table>
    </div>
    """)
# end for
php_print("""   </div>
</div>
""")
php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
