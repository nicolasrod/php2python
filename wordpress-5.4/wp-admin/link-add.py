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
#// Add Link Administration Screen.
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// Load WordPress Administration Bootstrap
php_include_file(__DIR__ + "/admin.php", once=True)
if (not current_user_can("manage_links")):
    wp_die(__("Sorry, you are not allowed to add links to this site."))
# end if
title = __("Add New Link")
parent_file = "link-manager.php"
wp_reset_vars(Array("action", "cat_id", "link_id"))
wp_enqueue_script("link")
wp_enqueue_script("xfn")
if wp_is_mobile():
    wp_enqueue_script("jquery-touch-punch")
# end if
link = get_default_link_to_edit()
php_include_file(ABSPATH + "wp-admin/edit-link-form.php", once=False)
php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
