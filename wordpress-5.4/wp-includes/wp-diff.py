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
#// WordPress Diff bastard child of old MediaWiki Diff Formatter.
#// 
#// Basically all that remains is the table structure and some method names.
#// 
#// @package WordPress
#// @subpackage Diff
#//
if (not php_class_exists("Text_Diff", False)):
    #// Text_Diff class
    php_include_file(ABSPATH + WPINC + "/Text/Diff.php", once=False)
    #// Text_Diff_Renderer class
    php_include_file(ABSPATH + WPINC + "/Text/Diff/Renderer.php", once=False)
    #// Text_Diff_Renderer_inline class
    php_include_file(ABSPATH + WPINC + "/Text/Diff/Renderer/inline.php", once=False)
# end if
php_include_file(ABSPATH + WPINC + "/class-wp-text-diff-renderer-table.php", once=False)
php_include_file(ABSPATH + WPINC + "/class-wp-text-diff-renderer-inline.php", once=False)
