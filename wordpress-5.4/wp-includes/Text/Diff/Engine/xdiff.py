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
    def diff(self, from_lines_=None, to_lines_=None):
        
        
        array_walk(from_lines_, Array("Text_Diff", "trimNewlines"))
        array_walk(to_lines_, Array("Text_Diff", "trimNewlines"))
        #// Convert the two input arrays into strings for xdiff processing.
        from_string_ = php_implode("\n", from_lines_)
        to_string_ = php_implode("\n", to_lines_)
        #// Diff the two strings and convert the result to an array.
        diff_ = xdiff_string_diff(from_string_, to_string_, php_count(to_lines_))
        diff_ = php_explode("\n", diff_)
        #// Walk through the diff one line at a time.  We build the $edits
        #// array of diff operations by reading the first character of the
        #// xdiff output (which is in the "unified diff" format).
        #// 
        #// Note that we don't have enough information to detect "changed"
        #// lines using this approach, so we can't add Text_Diff_Op_changed
        #// instances to the $edits array.  The result is still perfectly
        #// valid, albeit a little less descriptive and efficient.
        edits_ = Array()
        for line_ in diff_:
            if (not php_strlen(line_)):
                continue
            # end if
            for case in Switch(line_[0]):
                if case(" "):
                    edits_[-1] = php_new_class("Text_Diff_Op_copy", lambda : Text_Diff_Op_copy(Array(php_substr(line_, 1))))
                    break
                # end if
                if case("+"):
                    edits_[-1] = php_new_class("Text_Diff_Op_add", lambda : Text_Diff_Op_add(Array(php_substr(line_, 1))))
                    break
                # end if
                if case("-"):
                    edits_[-1] = php_new_class("Text_Diff_Op_delete", lambda : Text_Diff_Op_delete(Array(php_substr(line_, 1))))
                    break
                # end if
            # end for
        # end for
        return edits_
    # end def diff
# end class Text_Diff_Engine_xdiff
