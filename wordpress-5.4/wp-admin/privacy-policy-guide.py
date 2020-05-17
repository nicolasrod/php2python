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
#// Privacy Policy Guide Screen.
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// WordPress Administration Bootstrap
php_include_file(__DIR__ + "/admin.php", once=True)
if (not current_user_can("manage_privacy_options")):
    wp_die(__("Sorry, you are not allowed to manage privacy on this site."))
# end if
if (not php_class_exists("WP_Privacy_Policy_Content")):
    php_include_file(ABSPATH + "wp-admin/includes/class-wp-privacy-policy-content.php", once=False)
# end if
title_ = __("Privacy Policy Guide")
wp_enqueue_script("privacy-tools")
php_include_file(ABSPATH + "wp-admin/admin-header.php", once=True)
php_print("<div class=\"wrap\">\n   <h1>")
php_print(esc_html(title_))
php_print("""</h1>
<div class=\"wp-privacy-policy-guide\">
""")
WP_Privacy_Policy_Content.privacy_policy_guide()
php_print(" </div>\n</div>\n")
php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
