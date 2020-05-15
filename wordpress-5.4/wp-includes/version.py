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
#// WordPress Version
#// 
#// Contains version information for the current WordPress release.
#// 
#// @package WordPress
#// @since 1.1.0
#// 
#// 
#// The WordPress version string.
#// 
#// @global string $wp_version
#//
wp_version = "5.4"
#// 
#// Holds the WordPress DB revision, increments when changes are made to the WordPress DB schema.
#// 
#// @global int $wp_db_version
#//
wp_db_version = 47018
#// 
#// Holds the TinyMCE version.
#// 
#// @global string $tinymce_version
#//
tinymce_version = "4960-20190918"
#// 
#// Holds the required PHP version.
#// 
#// @global string $required_php_version
#//
required_php_version = "5.6.20"
#// 
#// Holds the required MySQL version.
#// 
#// @global string $required_mysql_version
#//
required_mysql_version = "5.0"
