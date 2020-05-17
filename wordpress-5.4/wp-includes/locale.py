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
#// Locale API
#// 
#// @package WordPress
#// @subpackage i18n
#// @since 1.2.0
#// @deprecated 4.7.0
#//
_deprecated_file(php_basename(__FILE__), "4.7.0")
