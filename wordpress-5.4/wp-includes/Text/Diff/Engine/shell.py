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
#// This class uses the Unix `diff` program via shell_exec to compute the
#// differences between the two input arrays.
#// 
#// Copyright 2007-2010 The Horde Project (http://www.horde.org/)
#// 
#// See the enclosed file COPYING for license information (LGPL). If you did
#// not receive this file, see http://opensource.org/licenses/lgpl-license.php.
#// 
#// @author  Milian Wolff <mail@milianw.de>
#// @package Text_Diff
#// @since   0.3.0
#//
class Text_Diff_Engine_shell():
    _diffCommand = "diff"
    #// 
    #// Returns the array of differences.
    #// 
    #// @param array $from_lines lines of text from old file
    #// @param array $to_lines   lines of text from new file
    #// 
    #// @return array all changes made (array with Text_Diff_Op_* objects)
    #//
    def diff(self, from_lines=None, to_lines=None):
        
        array_walk(from_lines, Array("Text_Diff", "trimNewlines"))
        array_walk(to_lines, Array("Text_Diff", "trimNewlines"))
        temp_dir = Text_Diff._gettempdir()
        #// Execute gnu diff or similar to get a standard diff file.
        from_file = php_tempnam(temp_dir, "Text_Diff")
        to_file = php_tempnam(temp_dir, "Text_Diff")
        fp = fopen(from_file, "w")
        fwrite(fp, php_implode("\n", from_lines))
        php_fclose(fp)
        fp = fopen(to_file, "w")
        fwrite(fp, php_implode("\n", to_lines))
        php_fclose(fp)
        diff = shell_exec(self._diffCommand + " " + from_file + " " + to_file)
        unlink(from_file)
        unlink(to_file)
        if is_null(diff):
            #// No changes were made
            return Array(php_new_class("Text_Diff_Op_copy", lambda : Text_Diff_Op_copy(from_lines)))
        # end if
        from_line_no = 1
        to_line_no = 1
        edits = Array()
        #// Get changed lines by parsing something like:
        #// 0a1,2
        #// 1,2c4,6
        #// 1,5d6
        preg_match_all("#^(\\d+)(?:,(\\d+))?([adc])(\\d+)(?:,(\\d+))?$#m", diff, matches, PREG_SET_ORDER)
        for match in matches:
            if (not (php_isset(lambda : match[5]))):
                #// This paren is not set every time (see regex).
                match[5] = False
            # end if
            if match[3] == "a":
                from_line_no -= 1
            # end if
            if match[3] == "d":
                to_line_no -= 1
            # end if
            if from_line_no < match[1] or to_line_no < match[4]:
                #// copied lines
                assert("$match[1] - $from_line_no == $match[4] - $to_line_no")
                php_array_push(edits, php_new_class("Text_Diff_Op_copy", lambda : Text_Diff_Op_copy(self._getlines(from_lines, from_line_no, match[1] - 1), self._getlines(to_lines, to_line_no, match[4] - 1))))
            # end if
            for case in Switch(match[3]):
                if case("d"):
                    #// deleted lines
                    php_array_push(edits, php_new_class("Text_Diff_Op_delete", lambda : Text_Diff_Op_delete(self._getlines(from_lines, from_line_no, match[2]))))
                    to_line_no += 1
                    break
                # end if
                if case("c"):
                    #// changed lines
                    php_array_push(edits, php_new_class("Text_Diff_Op_change", lambda : Text_Diff_Op_change(self._getlines(from_lines, from_line_no, match[2]), self._getlines(to_lines, to_line_no, match[5]))))
                    break
                # end if
                if case("a"):
                    #// added lines
                    php_array_push(edits, php_new_class("Text_Diff_Op_add", lambda : Text_Diff_Op_add(self._getlines(to_lines, to_line_no, match[5]))))
                    from_line_no += 1
                    break
                # end if
            # end for
        # end for
        if (not php_empty(lambda : from_lines)):
            #// Some lines might still be pending. Add them as copied
            php_array_push(edits, php_new_class("Text_Diff_Op_copy", lambda : Text_Diff_Op_copy(self._getlines(from_lines, from_line_no, from_line_no + php_count(from_lines) - 1), self._getlines(to_lines, to_line_no, to_line_no + php_count(to_lines) - 1))))
        # end if
        return edits
    # end def diff
    #// 
    #// Get lines from either the old or new text
    #// 
    #// @access private
    #// 
    #// @param array $text_lines Either $from_lines or $to_lines (passed by reference).
    #// @param int   $line_no    Current line number (passed by reference).
    #// @param int   $end        Optional end line, when we want to chop more
    #// than one line.
    #// 
    #// @return array The chopped lines
    #//
    def _getlines(self, text_lines=None, line_no=None, end_=False):
        
        if (not php_empty(lambda : end_)):
            lines = Array()
            #// We can shift even more
            while True:
                
                if not (line_no <= end_):
                    break
                # end if
                php_array_push(lines, php_array_shift(text_lines))
                line_no += 1
            # end while
        else:
            lines = Array(php_array_shift(text_lines))
            line_no += 1
        # end if
        return lines
    # end def _getlines
# end class Text_Diff_Engine_shell
