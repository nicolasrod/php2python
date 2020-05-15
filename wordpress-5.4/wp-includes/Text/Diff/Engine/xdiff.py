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
#// Class used internally by Diff to actually compute the diffs.
#// 
#// This class uses the xdiff PECL package (http://pecl.php.net/package/xdiff)
#// to compute the differences between the two input arrays.
#// 
#// Copyright 2004-2010 The Horde Project (http://www.horde.org/)
#// 
#// See the enclosed file COPYING for license information (LGPL). If you did
#// not receive this file, see http://opensource.org/licenses/lgpl-license.php.
#// 
#// @author  Jon Parise <jon@horde.org>
#// @package Text_Diff
#//
class Text_Diff_Engine_xdiff():
    #// 
    #//
    def diff(self, from_lines=None, to_lines=None):
        
        array_walk(from_lines, Array("Text_Diff", "trimNewlines"))
        array_walk(to_lines, Array("Text_Diff", "trimNewlines"))
        #// Convert the two input arrays into strings for xdiff processing.
        from_string = php_implode("\n", from_lines)
        to_string = php_implode("\n", to_lines)
        #// Diff the two strings and convert the result to an array.
        diff = xdiff_string_diff(from_string, to_string, php_count(to_lines))
        diff = php_explode("\n", diff)
        #// Walk through the diff one line at a time.  We build the $edits
        #// array of diff operations by reading the first character of the
        #// xdiff output (which is in the "unified diff" format).
        #// 
        #// Note that we don't have enough information to detect "changed"
        #// lines using this approach, so we can't add Text_Diff_Op_changed
        #// instances to the $edits array.  The result is still perfectly
        #// valid, albeit a little less descriptive and efficient.
        edits = Array()
        for line in diff:
            if (not php_strlen(line)):
                continue
            # end if
            for case in Switch(line[0]):
                if case(" "):
                    edits[-1] = php_new_class("Text_Diff_Op_copy", lambda : Text_Diff_Op_copy(Array(php_substr(line, 1))))
                    break
                # end if
                if case("+"):
                    edits[-1] = php_new_class("Text_Diff_Op_add", lambda : Text_Diff_Op_add(Array(php_substr(line, 1))))
                    break
                # end if
                if case("-"):
                    edits[-1] = php_new_class("Text_Diff_Op_delete", lambda : Text_Diff_Op_delete(Array(php_substr(line, 1))))
                    break
                # end if
            # end for
        # end for
        return edits
    # end def diff
# end class Text_Diff_Engine_xdiff
