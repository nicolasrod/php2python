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
if (php_isset(lambda : PHP_REQUEST["tab"])) and "debug" == PHP_REQUEST["tab"]:
    php_include_file(__DIR__ + "/site-health-info.php", once=True)
    sys.exit(-1)
# end if
#// WordPress Administration Bootstrap
php_include_file(__DIR__ + "/admin.php", once=True)
title_ = __("Site Health Status")
if (not current_user_can("view_site_health_checks")):
    wp_die(__("Sorry, you are not allowed to access site health information."), "", 403)
# end if
wp_enqueue_style("site-health")
wp_enqueue_script("site-health")
if (not php_class_exists("WP_Site_Health")):
    php_include_file(ABSPATH + "wp-admin/includes/class-wp-site-health.php", once=True)
# end if
health_check_site_status_ = WP_Site_Health.get_instance()
#// Start by checking if this is a special request checking for the existence of certain filters.
health_check_site_status_.check_wp_version_check_exists()
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
php_print("\" class=\"health-check-tab active\" aria-current=\"true\">\n            ")
#// translators: Tab heading for Site Health Status page.
_ex("Status", "Site Health")
php_print("     </a>\n\n        <a href=\"")
php_print(esc_url(admin_url("site-health.php?tab=debug")))
php_print("\" class=\"health-check-tab\">\n         ")
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
<div class=\"health-check-body hide-if-no-js\">
<div class=\"site-status-all-clear hide\">
<p class=\"icon\">
<span class=\"dashicons dashicons-yes\"></span>
</p>
<p class=\"encouragement\">
""")
_e("Great job!")
php_print("""       </p>
<p>
""")
_e("Everything is running smoothly here.")
php_print("""       </p>
</div>
<div class=\"site-status-has-issues\">
<h2>
""")
_e("Site Health Status")
php_print("     </h2>\n\n       <p>")
_e("The site health check shows critical information about your WordPress configuration and items that require your attention.")
php_print("""</p>
<div class=\"site-health-issues-wrapper\" id=\"health-check-issues-critical\">
<h3 class=\"site-health-issue-count-title\">
""")
#// translators: %s: Number of critical issues found.
printf(_n("%s critical issue", "%s critical issues", 0), "<span class=\"issue-count\">0</span>")
php_print("""           </h3>
<div id=\"health-check-site-status-critical\" class=\"health-check-accordion issues\"></div>
</div>
<div class=\"site-health-issues-wrapper\" id=\"health-check-issues-recommended\">
<h3 class=\"site-health-issue-count-title\">
""")
#// translators: %s: Number of recommended improvements.
printf(_n("%s recommended improvement", "%s recommended improvements", 0), "<span class=\"issue-count\">0</span>")
php_print("""           </h3>
<div id=\"health-check-site-status-recommended\" class=\"health-check-accordion issues\"></div>
</div>
</div>
<div class=\"site-health-view-more\">
<button type=\"button\" class=\"button site-health-view-passed\" aria-expanded=\"false\" aria-controls=\"health-check-issues-good\">
""")
_e("Passed tests")
php_print("""           <span class=\"icon\"></span>
</button>
</div>
<div class=\"site-health-issues-wrapper hidden\" id=\"health-check-issues-good\">
<h3 class=\"site-health-issue-count-title\">
""")
#// translators: %s: Number of items with no issues.
printf(_n("%s item with no issues detected", "%s items with no issues detected", 0), "<span class=\"issue-count\">0</span>")
php_print("""       </h3>
<div id=\"health-check-site-status-good\" class=\"health-check-accordion issues\"></div>
</div>
</div>
<script id=\"tmpl-health-check-issue\" type=\"text/template\">
<h4 class=\"health-check-accordion-heading\">
<button aria-expanded=\"false\" class=\"health-check-accordion-trigger\" aria-controls=\"health-check-accordion-block-{{ data.test }}\" type=\"button\">
<span class=\"title\">{{ data.label }}</span>
<span class=\"badge {{ data.badge.color }}\">{{ data.badge.label }}</span>
<span class=\"icon\"></span>
</button>
</h4>
<div id=\"health-check-accordion-block-{{ data.test }}\" class=\"health-check-accordion-panel\" hidden=\"hidden\">
{{{ data.description }}}
<div class=\"actions\">
<p class=\"button-container\">{{{ data.actions }}}</p>
</div>
</div>
</script>
""")
php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
