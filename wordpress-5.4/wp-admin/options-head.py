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
#// WordPress Options Header.
#// 
#// Displays updated message, if updated variable is part of the URL query.
#// 
#// @package WordPress
#// @subpackage Administration
#//
wp_reset_vars(Array("action"))
if (php_isset(lambda : PHP_REQUEST["updated"])) and (php_isset(lambda : PHP_REQUEST["page"])):
    #// For back-compat with plugins that don't use the Settings API and just set updated=1 in the redirect.
    add_settings_error("general", "settings_updated", __("Settings saved."), "success")
# end if
settings_errors()
